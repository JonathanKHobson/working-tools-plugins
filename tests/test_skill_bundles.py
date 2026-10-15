"""Focused tests for portable skill bundles from verified release bytes."""

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import tempfile
import unittest
import zipfile


MODULE = Path(__file__).resolve().parents[1] / "scripts" / "skill_bundles.py"
spec = importlib.util.spec_from_file_location("skill_bundles", MODULE)
skill_bundles = importlib.util.module_from_spec(spec)
spec.loader.exec_module(skill_bundles)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def make_release(path, files, *, executable=(), duplicate=None, symlink=None):
    with zipfile.ZipFile(path, "w") as zf:
        for name, data in files.items():
            info = zipfile.ZipInfo(name)
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | (0o755 if name in executable else 0o644)) << 16
            zf.writestr(info, data)
        if duplicate:
            zf.writestr(duplicate, b"duplicate")
        if symlink:
            info = zipfile.ZipInfo(symlink)
            info.create_system = 3
            info.external_attr = (stat.S_IFLNK | 0o777) << 16
            zf.writestr(info, b"target")


class BundleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=os.environ.get("TMPDIR"))
        self.root = Path(self.temp.name)
        self.archive = self.root / "release.zip"
        self.output = self.root / "site-bundles"
        self.files = {
            "skills/directory-name/SKILL.md": (
                b'---\nname: "quoted: skill"\ndescription: "Skill with a colon: and quotes"\n---\n'
                b'Read ../../references/guide.md and run ../../scripts/tool.sh.\n'
            ),
            "references/guide.md": b"Reviewed guidance\n",
            "scripts/tool.sh": b"#!/bin/sh\nprintf ready\n",
            "README.md": b"Source plugin readme\n",
            ".claude-plugin/plugin.json": b"{}\n",
            "LICENSE": b"License text\n",
        }
        make_release(self.archive, self.files, executable=("scripts/tool.sh",))

    def tearDown(self):
        self.temp.cleanup()

    def build(self, **changes):
        args = {
            "archive": self.archive,
            "expected_files": {name: digest(data) for name, data in self.files.items()},
            "expected_sha256": digest(self.archive.read_bytes()),
            "plugin_id": "sample-plugin",
            "version": "1.2.3",
            "source_commit": "a" * 40,
            "output": self.output,
        }
        args.update(changes)
        return skill_bundles.build_skill_bundles(**args)

    def test_complete_support_wrapper_and_repeatable_bytes(self):
        results = self.build()
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result["id"], "quoted: skill")
        self.assertEqual(result["directory"], "directory-name")
        self.assertEqual(result["original_entry"], "skills/directory-name/SKILL.md")
        self.assertEqual(result["plugin_version"], "1.2.3")
        bundle = self.output / result["file"]
        first = bundle.read_bytes()
        self.assertEqual(result["sha256"], digest(first))
        self.assertEqual(result["size"], len(first))
        base = "sample-plugin-directory-name"
        with zipfile.ZipFile(bundle) as zf:
            names = set(zf.namelist())
            self.assertEqual(names, {f"{base}/{name}" for name in ("SKILL.md", "README.md", "MANIFEST.json")}
                             | {f"{base}/.support/{name}" for name in self.files})
            for name, data in self.files.items():
                self.assertEqual(zf.read(f"{base}/.support/{name}"), data)
            wrapper = zf.read(f"{base}/SKILL.md").decode()
            self.assertIn("name: 'quoted: skill'", wrapper)
            self.assertIn(".support/skills/directory-name/SKILL.md", wrapper)
            self.assertIn("Resolve its relative", wrapper)
            self.assertIn("does not install or activate the full plugin runtime", wrapper)
            readme = zf.read(f"{base}/README.md").decode()
            self.assertIn("docs/install.md", readme)
            self.assertIn("provider setup remain separate", readme)
            manifest = json.loads(zf.read(f"{base}/MANIFEST.json"))
            self.assertEqual(manifest["files"], {f".support/{name}": digest(data) for name, data in self.files.items()})
            mode = zf.getinfo(f"{base}/.support/scripts/tool.sh").external_attr >> 16
            self.assertEqual(mode & 0o111, 0o111)
            self.assertNotIn(f"{base}/.claude-plugin/plugin.json", names)
            self.assertIn(f"{base}/.support/.claude-plugin/plugin.json", names)
            self.assertIn("Run package-root commands from that directory", wrapper)
        self.assertEqual(self.build(), results)
        self.assertEqual(bundle.read_bytes(), first)

    def test_package_root_command_after_extraction(self):
        import subprocess
        self.files["scripts/tool.sh"] = b"#!/bin/sh\ncat references/guide.md\n"
        make_release(self.archive, self.files, executable=("scripts/tool.sh",))
        row = self.build()[0]
        extracted = self.root / "extracted"
        with zipfile.ZipFile(self.output / row["file"]) as zf:
            zf.extractall(extracted)  # Locally authored fixture, not untrusted release code.
        support = extracted / "sample-plugin-directory-name/.support"
        self.assertEqual(subprocess.check_output(["/bin/sh", "scripts/tool.sh"], cwd=support), b"Reviewed guidance\n")

    def test_rejects_tampered_archive_before_output(self):
        with self.assertRaisesRegex(ValueError, "verification"):
            self.build(expected_sha256="0" * 64)
        self.assertFalse(self.output.exists())

    def test_rejects_unsafe_member_and_duplicate(self):
        make_release(self.archive, self.files, symlink="bad-link")
        with self.assertRaisesRegex(ValueError, "verification"):
            self.build()
        self.assertFalse(self.output.exists())
        make_release(self.archive, self.files, duplicate="README.md")
        with self.assertRaisesRegex(ValueError, "verification"):
            self.build()
        self.assertFalse(self.output.exists())

    def test_rejects_unsafe_identifier_and_duplicate_skill_names(self):
        with self.assertRaisesRegex(ValueError, "unsafe plugin id"):
            self.build(plugin_id="../escape")
        self.assertFalse(self.output.exists())
        self.files["skills/other/SKILL.md"] = self.files["skills/directory-name/SKILL.md"]
        make_release(self.archive, self.files)
        with self.assertRaisesRegex(ValueError, "duplicate skill id"):
            self.build()
        self.assertFalse(self.output.exists())

    def test_rejects_invalid_frontmatter_and_output_symlink(self):
        self.files["skills/directory-name/SKILL.md"] = b"---\nname: [oops]\ndescription: desc\n---\n"
        make_release(self.archive, self.files)
        with self.assertRaisesRegex(ValueError, "skill name"):
            self.build()
        self.assertFalse(self.output.exists())
        self.files["skills/directory-name/SKILL.md"] = b"---\nname: valid\ndescription: desc\n---\n"
        make_release(self.archive, self.files)
        self.output.symlink_to(self.root, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "real directory"):
            self.build()


if __name__ == "__main__":
    unittest.main()
