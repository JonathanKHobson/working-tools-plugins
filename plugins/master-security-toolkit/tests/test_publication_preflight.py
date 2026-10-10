"""Synthetic behavioral checks; no real credentials or source archive execution."""

import base64
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "publication_preflight.py"
spec = importlib.util.spec_from_file_location("publication_preflight", SCRIPT)
preflight = importlib.util.module_from_spec(spec)
spec.loader.exec_module(preflight)


class PreflightTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        # macOS /var is a system symlink; use its physical path for normal cases.
        self.root = Path(self.temp.name).resolve()

    def tearDown(self):
        self.temp.cleanup()

    def file(self, name="frame.html", content="<h1>Public workshop</h1>"):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def scan(self, target=None, files=1000, size=1_000_000, total=20_000_000):
        scan = preflight.Scan(files, size, total)
        scan.target(str(target or self.root), 1)
        return scan.report()

    def cli(self, *args):
        return subprocess.run([sys.executable, "-B", str(SCRIPT), *map(str, args)],
                              capture_output=True, text=True, check=False)

    def test_benign_supported_build_assets_and_hashes(self):
        for extension in ["html", "css", "js", "json", "md", "txt"]:
            self.file("site/file." + extension, "Public introduction 2026-10-03")
        report = self.scan()
        self.assertEqual(report["status"], "no-matches")
        self.assertEqual(len(report["files"]), 6)
        self.assertEqual(report["files"][0]["sha256"], hashlib.sha256(b"Public introduction 2026-10-03").hexdigest())

    def test_secret_in_script_style_comment_and_attribute(self):
        token = "gh" + "p_" + "a" * 36
        path = self.file(content=f'<script>let key="{token}";</script>\n<style>/*{token}*/</style>\n<!--{token}-->\n<p data-private="{token}">Hi</p>')
        report = self.scan(path)
        findings = [f for f in report["findings"] if f["rule"] == "secret.github-token"]
        self.assertEqual([f["line"] for f in findings], [1, 2, 3, 4])
        self.assertEqual(report["status"], "blocked")
        output = json.dumps(report)
        self.assertNotIn(token, output)
        self.assertNotIn("frame.html", output)

    def test_html_entities_source_line_and_deduplication(self):
        token = "AK" + "IA" + "B" * 16
        encoded = "".join("&#" + str(ord(c)) + ";" for c in token)
        report = self.scan(self.file(content="First line\n<script>\n" + encoded + "</script>"))
        finding = next(f for f in report["findings"] if f["rule"] == "secret.aws-access-key")
        self.assertEqual(finding["line"], 3)
        self.assertEqual(finding["view"], "html-entities-1")
        report2 = self.scan(self.file(content=token + " &amp; public"))
        self.assertEqual(len([f for f in report2["findings"] if f["rule"] == "secret.aws-access-key"]), 1)

    def test_base64_secret_is_blocked_at_encoded_source_line(self):
        token = "sk" + "_live_" + "a" * 32
        encoded = base64.b64encode(token.encode()).decode()
        report = self.scan(self.file(content="Public\n<script>atob('" + encoded + "')</script>"))
        self.assertEqual(report["status"], "blocked")
        finding = next(f for f in report["findings"] if f["rule"] == "secret.stripe-live-key")
        self.assertEqual(finding["line"], 2)

    def test_privacy_review_is_distinct_from_block(self):
        report = self.scan(self.file(content="Contact: public@example.com\nInternal-only draft\n/" + "Users/demo/private"))
        self.assertEqual(report["status"], "review")
        self.assertEqual(report["summary"]["block_findings"], 0)
        self.assertGreaterEqual(report["summary"]["review_findings"], 3)

    def test_all_known_format_rules(self):
        values = ["-----BEGIN " + "PRIVATE KEY-----", "AK" + "IA" + "C" * 16,
                  "gh" + "p_" + "b" * 36, "sk" + "-proj-" + "c" * 40,
                  "sk" + "_live_" + "d" * 24, "xox" + "b-" + "e" * 32]
        report = self.scan(self.file(content="\n".join(values)))
        self.assertEqual(report["summary"]["block_findings"], 6)

    def test_near_misses_do_not_block(self):
        report = self.scan(self.file(content="github public documentation\nAKIAshort\nsk-short\nghp_short\n2026-10-03\nA public RSA PUBLIC KEY"))
        self.assertEqual(report["status"], "no-matches")

    def test_additional_distinctive_formats_and_short_near_misses(self):
        examples = [("secret.google-legacy-api-key", "AI" + "za" + "A" * 35),
                    ("secret.npm-token", "np" + "m_" + "B" * 36),
                    ("secret.sendgrid-key", "S" + "G." + "C" * 22 + "." + "D" * 43),
                    ("secret.anthropic-key", "sk" + "-ant-api03-" + "E" * 40)]
        for rule, value in examples:
            with self.subTest(rule=rule):
                report = self.scan(self.file(content=value))
                self.assertEqual(report["status"], "blocked")
                self.assertEqual([f["rule"] for f in report["findings"]], [rule])
                self.assertNotIn(value, json.dumps(report))
        report = self.scan(self.file(content="AIza-short npm_short SG.short.short sk-ant-short"))
        self.assertEqual(report["status"], "no-matches")

    def test_jwt_and_url_credentials_require_review_not_certification(self):
        jwt = "ey" + "J" + "A" * 20 + "." + "B" * 20 + "." + "C" * 20
        report = self.scan(self.file(content=jwt + "\npostgresql://user:password@localhost/db"))
        self.assertEqual(report["status"], "review")
        self.assertEqual({f["rule"] for f in report["findings"]},
                         {"privacy.jwt-shape", "privacy.url-credentials"})

    def test_nested_base64_cannot_be_false_clean(self):
        token = "gh" + "p_" + "a" * 36
        for inner in [base64.b64encode(token.encode()).decode(),
                      "".join("&#" + str(ord(c)) + ";" for c in token)]:
            encoded = base64.b64encode(inner.encode()).decode()
            report = self.scan(self.file(content="<script>" + encoded + "</script>"))
            self.assertEqual(report["status"], "review")
            self.assertEqual({f["rule"] for f in report["findings"]}, {"privacy.base64-text"})

    def test_same_occurrence_across_views_has_one_fingerprint(self):
        token = "gh" + "p_" + "a" * 36
        report = self.scan(self.file(content=token + " &amp; &amp;amp; " + token))
        findings = [f for f in report["findings"] if f["rule"] == "secret.github-token"]
        self.assertEqual(len(findings), 2)
        self.assertNotEqual(findings[0]["source_character_offset"], findings[1]["source_character_offset"])
        self.assertNotEqual(findings[0]["fingerprint"], findings[1]["fingerprint"])

    def test_findings_ceiling_uses_overflow_sentinel_and_explicit_gap(self):
        old_limit = preflight.MAX_FINDINGS
        preflight.MAX_FINDINGS = 2
        try:
            report = self.scan(self.file(content="one@example.com\ntwo@example.com"))
            self.assertEqual(len(report["findings"]), 2)
            self.assertEqual(report["status"], "review")
            report = self.scan(self.file(content="one@example.com\ntwo@example.com\nthree@example.com"))
            self.assertEqual(len(report["findings"]), 2)
            self.assertEqual(report["status"], "incomplete")
            self.assertEqual(report["gaps"][0]["reason"], "finding-limit")
        finally:
            preflight.MAX_FINDINGS = old_limit

    def test_no_target_and_sensitive_invalid_argument_are_not_echoed(self):
        self.assertEqual(self.cli().returncode, 2)
        response = self.cli("--bad-public@example.com")
        self.assertEqual(response.returncode, 2)
        self.assertNotIn("public@example.com", response.stderr)

    def test_flags_before_and_after_target(self):
        path = self.file()
        for args in [("--max-files", "1", path), (path, "--max-files", "1")]:
            self.assertEqual(self.cli(*args).returncode, 0)

    def test_limits_cannot_be_raised(self):
        self.assertEqual(self.cli(self.file(), "--max-files", "1001").returncode, 2)
        self.assertEqual(self.cli(self.root, "--max-bytes", "0").returncode, 2)

    def test_symlink_target_and_nested_symlink_never_followed(self):
        target = self.file("private.txt", "private@example.com")
        link = self.root / "alias.html"
        link.symlink_to(target)
        report = self.scan(link)
        self.assertEqual(report["status"], "incomplete")
        self.assertFalse(report["files"])
        folder = self.root / "build"
        folder.mkdir()
        (folder / "alias.html").symlink_to(target)
        report = self.scan(folder)
        self.assertEqual(report["gaps"][0]["reason"], "symlink-refused")
        self.assertFalse(report["findings"])

    def test_symlink_ancestor_refused(self):
        folder = self.root / "build"
        folder.mkdir()
        self.file("build/frame.html")
        alias = self.root / "alias"
        alias.symlink_to(folder, target_is_directory=True)
        report = self.scan(alias / "frame.html")
        self.assertEqual(report["status"], "incomplete")
        self.assertFalse(report["files"])

    def test_vault_directory_and_vault_ancestor_refused(self):
        vault = self.root / "Notes"
        (vault / ".obsidian").mkdir(parents=True)
        target = self.file("Notes/note.md", "private@example.com")
        for path in [vault, target]:
            report = self.scan(path)
            self.assertEqual(report["status"], "incomplete")
            self.assertFalse(report["files"])

    def test_unsupported_binary_and_nonutf8_are_explicit_gaps(self):
        self.file("photo.png", "image")
        self.file("null.txt", "\x00binary")
        (self.root / "latin.txt").write_bytes(b"\xff")
        report = self.scan()
        self.assertEqual(report["status"], "incomplete")
        self.assertEqual({g["reason"] for g in report["gaps"]},
                         {"unsupported-type-or-binary", "binary-content", "non-utf8-text"})

    def test_missing_and_empty_targets_incomplete(self):
        for target in [self.root / "missing.html", self.root]:
            self.assertEqual(self.scan(target)["status"], "incomplete")

    def test_total_file_and_perfile_limits_incomplete(self):
        self.file("one.txt", "abc")
        self.file("two.txt", "def")
        for settings in [{"files": 1}, {"size": 2}, {"total": 4}]:
            self.assertEqual(self.scan(**settings)["status"], "incomplete")

    def test_filename_contents_are_never_output(self):
        report = self.scan(self.file("private@example.com.html", "Public"))
        output = json.dumps(report)
        self.assertNotIn("private@example.com", output)
        self.assertNotIn(str(self.root), output)

    def test_repeated_occurrences_and_fingerprints_change_with_artifact(self):
        path = self.file(content="public@example.com\npublic@example.com")
        report = self.scan(path)
        self.assertEqual([f["line"] for f in report["findings"]], [1, 2])
        fingerprints = [f["fingerprint"] for f in report["findings"]]
        self.assertNotEqual(fingerprints[0], fingerprints[1])
        path.write_text(path.read_text() + "\nChanged", encoding="utf-8")
        self.assertNotEqual(fingerprints[0], self.scan(path)["findings"][0]["fingerprint"])

    def test_no_asset_following_and_no_file_modification(self):
        secret = self.file("outside.txt", "private@example.com")
        path = self.file("build/frame.html", '<script src="../outside.txt"></script>')
        before = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in [path, secret]}
        response = self.cli(path)
        self.assertEqual(response.returncode, 0)
        self.assertFalse(json.loads(response.stdout)["findings"])
        self.assertEqual(before, {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in [path, secret]})

    def test_cli_status_codes_and_no_allowlist_override(self):
        path = self.file(content="public@example.com")
        self.assertEqual(self.cli(path).returncode, 1)
        self.assertEqual(self.cli(path, "--allowlist", "*").returncode, 2)
        self.assertEqual(self.cli(self.root / "missing.html").returncode, 2)


if __name__ == "__main__":
    unittest.main()
