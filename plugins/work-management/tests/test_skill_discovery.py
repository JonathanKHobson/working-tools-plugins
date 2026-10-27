"""Offline checks for the native registry lookup; no Codex session is started."""

import importlib.util
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/skill_discovery.py"
spec = importlib.util.spec_from_file_location("skill_discovery", SCRIPT)
discovery = importlib.util.module_from_spec(spec)
spec.loader.exec_module(discovery)


class DiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.paths = [root / f"skill-{number}" / "SKILL.md" for number in range(6)]
        for path in self.paths:
            path.parent.mkdir()
            path.write_text("# Skill instructions remain unread\n")
        self.records = [
            self.record("invoice-preparation", 0, "billing@personal",
                        "Prepare a verified client invoice from agreed terms and work evidence.",
                        short="Make accurate service invoices"),
            self.record("client-receivables", 1, "billing@personal",
                        "Review overdue invoices, then draft a proportionate follow-up.",
                        short="Follow up on unpaid invoices"),
            self.record("email-sender", 2, "mail@personal",
                        "Send reviewed email messages and invoice attachments."),
            self.record("invoice-preparation", 3, "legacy@personal",
                        "Older invoice method that policy has disabled.", enabled=False),
            self.record("survey-strategist", 4, "research@personal",
                        "Plan and analyze surveys for a decision."),
            self.record("survey-strategist", 5, None,
                        "Standalone copy of the survey skill."),
        ]
        self.inventory = {"data": [{"cwd": str(root), "skills": self.records}]}
        self.skills = discovery.skills_from_inventory(self.inventory)

    def record(self, name, index, owner, description, *, short="", enabled=True):
        return {"name": name, "description": description,
                "path": str(self.paths[index]), "pluginId": owner,
                "enabled": enabled, "interface": {"shortDescription": short}}

    def test_ranking_uses_name_before_description_and_short_description(self):
        found = discovery.search(self.skills, "invoice", None, 5)
        self.assertEqual([s["name"] for s in found],
                         ["invoice-preparation", "client-receivables", "email-sender"])
        self.assertTrue(found[0]["score"] > found[1]["score"] > found[2]["score"])
        service = discovery.search(self.skills, "service invoices", None, 5)
        self.assertEqual(service[0]["name"], "invoice-preparation")
        self.assertEqual(service[0]["matchedTerms"], ["service", "invoices"])
        self.assertTrue(any(result["partialMatch"] for result in service[1:]))
        self.assertEqual(discovery.search(self.skills, "completely unrelated", None, 5), [])

    def test_disabled_excluded_from_search_but_exact_show_is_labeled(self):
        result = discovery.search(self.skills, "invoice-preparation", None, 5)
        self.assertEqual(result[0]["name"], "invoice-preparation")
        self.assertTrue(all(skill["enabled"] for skill in result))
        disabled = next(s for s in self.skills if s["owner"] == "legacy@personal")
        shown = discovery.show(self.skills, disabled["id"])
        self.assertFalse(shown["enabled"])
        self.assertTrue(shown["entrypointExists"])
        self.assertEqual(shown["description"], self.records[3]["description"])

    def test_collision_uses_plugin_and_path_canonical_id(self):
        survey = [s for s in self.skills if s["name"] == "survey-strategist"]
        self.assertEqual(len({s["id"] for s in survey}), 2)
        with self.assertRaisesRegex(discovery.DiscoveryError, "Ambiguous"):
            discovery.show(self.skills, "survey-strategist")
        for skill in survey:
            self.assertEqual(discovery.show(self.skills, skill["id"]), skill)
            self.assertEqual(discovery.show(self.skills, skill["qualifiedName"]), skill)
        with self.assertRaisesRegex(discovery.DiscoveryError, "No registered skill"):
            discovery.show(self.skills, "missing-owner::missing-skill")

    def test_owner_filter_punctuation_limit_and_counts(self):
        billing = discovery.search(self.skills, "invoice-preparation", "billing@personal", 5)
        self.assertEqual(billing[0]["name"], "invoice-preparation")
        self.assertTrue(all(s["owner"] == "billing@personal" for s in billing))
        self.assertEqual(discovery.search(self.skills, "invoice", "research", 5), [])
        self.assertEqual(len(discovery.search(self.skills, "survey", None, 1)), 1)
        counts = {entry["owner"]: entry for entry in discovery.owners(self.skills)}
        self.assertEqual(counts["legacy@personal"],
                         {"owner": "legacy@personal", "enabled": 0, "total": 1})

    def test_conventional_plugin_skill_aliases_preserve_native_and_portable_names(self):
        self.assertEqual(discovery.show(self.skills, "billing:invoice-preparation")["owner"], "billing@personal")
        self.assertEqual(discovery.show(self.skills, "billing@personal:invoice-preparation")["owner"], "billing@personal")
        native = dict(self.skills[0], id="native-id", owner="writing-quality-studio@personal",
                      name="writing-quality-studio:natural-prose-editor",
                      qualifiedName="writing-quality-studio@personal::writing-quality-studio:natural-prose-editor")
        portable = dict(native, id="portable-id", owner="writing-quality-studio",
                        name="natural-prose-editor", qualifiedName="writing-quality-studio::natural-prose-editor")
        for record in (native, portable):
            self.assertEqual(discovery.show([record], "writing-quality-studio:natural-prose-editor"), record)
        with self.assertRaisesRegex(discovery.DiscoveryError, "Ambiguous"):
            discovery.show([native, portable], "writing-quality-studio:natural-prose-editor")
        self.assertEqual(discovery.show([native, portable], "writing-quality-studio@personal:natural-prose-editor"), native)
        self.assertEqual(discovery.show([native, portable], portable["qualifiedName"]), portable)
        self.assertEqual(discovery.show([native, portable], native["id"]), native)
        team = dict(native, id="team-id", owner="writing-quality-studio@team",
                    qualifiedName="writing-quality-studio@team::writing-quality-studio:natural-prose-editor")
        with self.assertRaisesRegex(discovery.DiscoveryError, "Ambiguous"):
            discovery.show([native, team], "writing-quality-studio:natural-prose-editor")
        self.assertEqual(discovery.show([native, team], "writing-quality-studio@team:natural-prose-editor"), team)
        self.assertEqual(discovery.show([portable], "natural-prose-editor"), portable)
        for malformed in ("writing-quality-studio:", ":natural-prose-editor"):
            with self.assertRaisesRegex(discovery.DiscoveryError, "No registered skill"):
                discovery.show([native, portable], malformed)

    def test_alias_preserves_disabled_state_and_does_not_strip_unrelated_prefix(self):
        disabled = discovery.show(self.skills, "legacy:invoice-preparation")
        self.assertFalse(disabled["enabled"])
        record = dict(self.skills[0], owner="billing", name="foreign:invoice-preparation")
        with self.assertRaisesRegex(discovery.DiscoveryError, "No registered skill"):
            discovery.show([record], "billing:invoice-preparation")
        self.assertEqual(discovery.show([record], "billing:foreign:invoice-preparation"), record)

    def test_partial_relevance_finds_grant_workflow_and_generalizes_to_mac_recovery(self):
        native_like = {"data": [{"skills": [
            self.record("writing-quality-studio:grant-process-crafter", 0,
                        "writing-quality-studio@personal",
                        "Guide the full grant lifecycle: opportunity discovery, eligibility and go/no-go, "
                        "NOFO/RFP compliance, project and evaluation design, budget narrative handoff, "
                        "proposal drafting and review, human submission readiness, award reporting, "
                        "closeout and resubmission."),
            self.record("artifact-template-studio-grant-project-summary", 1, None,
                        "Create an editable community project proposal summary with bounded evidence, "
                        "an activity and evaluation plan, exact cost assumptions and explicit funding status."),
            self.record("career-studio:application-statements", 2, "career-studio@personal",
                        "Write evidence-backed application statements for a job search."),
            self.record("mac-ops-toolkit:app-window-recovery", 3, "mac-ops-toolkit@personal",
                        "Recover an app that is running without a usable window while preserving user state."),
            self.record("development-studio:native-macos-app-builder", 4,
                        "development-studio@personal",
                        "Build native macOS applications; implement app architecture, views and window management."),
        ]}]}
        skills = discovery.skills_from_inventory(native_like)
        funding = discovery.search(skills,
                                   "funding application eligibility budget explanation progress reporting funder",
                                   None, 5)
        self.assertIn("writing-quality-studio:grant-process-crafter",
                      [skill["name"] for skill in funding[:3]])
        self.assertTrue(funding[0]["partialMatch"])
        self.assertEqual(funding[0]["matchedTerms"], ["eligibility", "budget", "reporting"])
        self.assertTrue(discovery.search(skills, "grant application", None, 5))
        self.assertEqual(discovery.search(skills, "zibber flobber nonsense", None, 5), [])
        mac = discovery.search(skills, "Mac window disappeared app running", None, 5)
        self.assertEqual(mac[0]["name"], "mac-ops-toolkit:app-window-recovery")

    def test_invalid_relative_paths_are_not_displayed_as_registered(self):
        records = list(self.records) + [dict(self.records[0], path="../fake/SKILL.md")]
        skills = discovery.skills_from_inventory({"data": [{"skills": records}]})
        self.assertEqual(len(skills), len(self.records))
        with self.assertRaisesRegex(discovery.DiscoveryError, "data list"):
            discovery.skills_from_inventory({"skills": records})
        self.paths[5].unlink()
        stale = discovery.skills_from_inventory(self.inventory)
        self.assertFalse(discovery.show(stale, "standalone::survey-strategist")["entrypointExists"])

    def test_group_errors_are_reported_even_when_skills_are_present(self):
        inventory = {"data": [{"cwd": self.temp.name, "skills": self.records,
                                "errors": [{"message": "skill registration failed"}]}]}
        with self.assertRaisesRegex(discovery.DiscoveryError,
                                    "skill registration failed"):
            discovery.skills_from_inventory(inventory)

    def test_snapshot_cli_is_labeled_and_never_spawns_process(self):
        snapshot = Path(self.temp.name) / "registry.json"
        snapshot.write_text(json.dumps(self.inventory))
        out = io.StringIO()
        with patch.object(discovery.subprocess, "Popen") as popen, patch("sys.stdout", out):
            status = discovery.main(["--inventory", str(snapshot), "--json", "search", "survey", "--limit", "1"])
            popen.assert_not_called()
        self.assertEqual(status, 0)
        result = json.loads(out.getvalue())
        self.assertEqual(result["mode"], "snapshot")
        self.assertEqual(len(result["skills"]), 1)
        self.assertIn("entrypoint", result["skills"][0])

    def test_native_rpc_calls_are_read_only_and_process_is_reaped(self):
        process = FakeProcess()
        calls = []
        with patch.object(discovery.shutil, "which", return_value="/fake/codex"), \
             patch.object(discovery.subprocess, "Popen", return_value=process), \
             patch.object(discovery, "_rpc", side_effect=lambda p, i, method, params, pending:
                          calls.append((method, params)) or ({"data": []} if method == "skills/list" else {})):
            result = discovery.native_inventory(Path(self.temp.name), "codex")
        self.assertEqual(result, {"data": []})
        self.assertEqual([method for method, _ in calls], ["initialize", "skills/list"])
        self.assertEqual(calls[1][1], {"cwds": [self.temp.name], "forceReload": True})
        self.assertEqual(process.terminated, 1)
        self.assertEqual(process.waited, 1)
        self.assertIn('"method": "initialized"', process.stdin.data.decode())

    def test_native_error_still_reaps_process(self):
        process = FakeProcess()
        with patch.object(discovery.shutil, "which", return_value="/fake/codex"), \
             patch.object(discovery.subprocess, "Popen", return_value=process), \
             patch.object(discovery, "_rpc", side_effect=discovery.DiscoveryError("timed out")):
            with self.assertRaisesRegex(discovery.DiscoveryError, "timed out"):
                discovery.native_inventory(Path(self.temp.name), "codex")
        self.assertEqual((process.terminated, process.waited), (1, 1))

    def test_unresponsive_native_process_is_killed_and_reaped(self):
        process = FakeProcess()
        process.hang_on_first_wait = True
        with patch.object(discovery.shutil, "which", return_value="/fake/codex"), \
             patch.object(discovery.subprocess, "Popen", return_value=process), \
             patch.object(discovery, "_rpc", side_effect=discovery.DiscoveryError("timed out")):
            with self.assertRaises(discovery.DiscoveryError):
                discovery.native_inventory(Path(self.temp.name), "codex")
        self.assertEqual((process.terminated, process.killed, process.waited), (1, 1, 2))

    def test_rpc_caps_total_bytes_across_many_small_notifications(self):
        process = FakeProcess()
        notifications = [b'{"method":"tick"}\n'] * 20
        with patch.object(discovery, "MAX_RESPONSE_BYTES", 100), \
             patch.object(discovery.select, "select", return_value=([process.stdout], [], [])), \
             patch.object(discovery.os, "read", side_effect=notifications):
            with self.assertRaisesRegex(discovery.DiscoveryError, "response limit"):
                discovery._rpc(process, 1, "skills/list", {}, bytearray())
        self.assertLess(len(process.stdin.data), 100)


class PortableDiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="portable roots ")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()

    def package(self, folder="writing package", *, owner="writing", enabled=None):
        root = self.root / folder
        (root / ".codex-plugin").mkdir(parents=True)
        (root / "skills").mkdir()
        metadata = {"name": owner, "skills": "./skills/"}
        if enabled is not None:
            metadata["enabled"] = enabled
        (root / ".codex-plugin/plugin.json").write_text(json.dumps(metadata))
        return root

    def skill(self, root, folder="editor", *, name="natural-prose-editor", description="Review final reader-facing writing for natural voice.", short="Everyday Humanizer", enabled=None, frontmatter=None):
        path = root / "skills" / folder / "SKILL.md"
        path.parent.mkdir(parents=True)
        if frontmatter is None:
            frontmatter = f"name: {name}\ndescription: {json.dumps(description)}\nshort-description: {short}\n"
            if enabled is not None:
                frontmatter += f"enabled: {str(enabled).lower()}\n"
        path.write_text("---\n" + frontmatter + "---\n# Body is not indexed\nsecret-body-keyword\n")
        return path

    def inventory(self, roots=None, manifest=None):
        return discovery.portable_inventory(roots or [], manifest)

    def test_explicit_package_search_preserves_descriptions_and_short_metadata(self):
        root = self.package()
        path = self.skill(root)
        skills, sources = self.inventory([root])
        found = discovery.search(skills, "Humanizer", None, 5)
        self.assertEqual(found[0]["entrypoint"], str(path))
        self.assertEqual(found[0]["shortDescription"], "Everyday Humanizer")
        self.assertEqual(found[0]["description"], "Review final reader-facing writing for natural voice.")
        self.assertEqual(discovery.search(skills, "secret-body-keyword", None, 5), [])
        self.assertEqual(sources[0]["installationState"], "unverified")
        self.assertEqual(found[0]["activationState"], "unverified")

    def test_portable_cli_never_launches_native_process_and_empty_is_explicit(self):
        root = self.package()
        self.skill(root)
        for arguments, expected in [(["--plugin-root", str(root)], 1), (["--portable"], 0)]:
            output = io.StringIO()
            with patch.object(discovery.subprocess, "Popen") as popen, patch("sys.stdout", output):
                status = discovery.main(arguments + ["--json", "search", "Humanizer"])
            popen.assert_not_called()
            self.assertEqual(status, 0)
            result = json.loads(output.getvalue())
            self.assertEqual(result["mode"], "portable")
            self.assertEqual(len(result["skills"]), expected)
            self.assertFalse(result["capabilities"]["nativeRegistrationVerified"])
        with patch.object(discovery, "native_inventory", return_value={"data": []}) as native, patch("sys.stdout", io.StringIO()):
            self.assertEqual(discovery.main(["owners"]), 0)
        native.assert_called_once()  # Default remains native rather than scanning directories.

    def test_manifest_relative_roots_and_disabled_skill_are_honored(self):
        root = self.package()
        path = self.skill(root)
        manifest = self.root / "selection.json"
        manifest.write_text(json.dumps({"plugins": [{"root": root.name, "enabled": True,
                                                     "skills": {"skills/editor/SKILL.md": False}}]}))
        skills, _ = self.inventory(manifest=manifest)
        self.assertEqual(discovery.search(skills, "Humanizer", None, 5), [])
        shown = discovery.show(skills, "writing::natural-prose-editor")
        self.assertFalse(shown["enabled"])
        self.assertEqual(shown["entrypoint"], str(path))
        self.assertEqual(discovery.owners(skills), [{"owner": "writing", "enabled": 0, "total": 1}])

    def test_package_and_frontmatter_disable_are_never_reenabled(self):
        root = self.package(enabled=False)
        self.skill(root, enabled=True)
        manifest = self.root / "selection.json"
        manifest.write_text(json.dumps({"plugins": [{"root": root.name, "enabled": True}]}))
        skills, _ = self.inventory([root], manifest)
        self.assertFalse(skills[0]["enabled"])
        root2 = self.package("second", owner="second")
        self.skill(root2, enabled=False)
        self.assertFalse(self.inventory([root2])[0][0]["enabled"])
        manifest.write_text(json.dumps({"plugins": [{"root": root2.name, "enabled": False}]}))
        self.assertFalse(self.inventory([root2], manifest)[0][0]["enabled"])

    def test_duplicate_names_and_duplicate_owners_need_canonical_path(self):
        first = self.package("first", owner="same")
        second = self.package("second", owner="same")
        self.skill(first)
        self.skill(second)
        skills, _ = self.inventory([first, second, first])
        self.assertEqual(len(skills), 2)
        for name in ("natural-prose-editor", "same::natural-prose-editor"):
            with self.assertRaisesRegex(discovery.DiscoveryError, "Ambiguous"):
                discovery.show(skills, name)
        self.assertEqual(discovery.show(skills, skills[0]["id"]), skills[0])
        self.assertEqual(len(discovery.search(skills, "Humanizer", "same", 5)), 2)

    def test_missing_required_metadata_and_malformed_values_fail_visibly(self):
        for frontmatter in ("name: editor\n", "description: Review text\n", "name: editor\ndescription: []\n", "name: editor\ndescription: \"bad\n", "name: editor\nname: another\ndescription: review\n", "name: editor\ndescription: review\nenabled: yes\n"):
            with self.subTest(frontmatter=frontmatter):
                root = self.package("case-" + str(len(list(self.root.iterdir()))))
                self.skill(root, frontmatter=frontmatter)
                with self.assertRaises(discovery.DiscoveryError):
                    self.inventory([root])

    def test_folded_and_literal_descriptions_remain_meaningful(self):
        root = self.package()
        self.skill(root, frontmatter="name: editor\ndescription: >-\n  Review final prose\n  for natural voice.\nshort-description: 'Everyday humanizer'\n")
        skills, _ = self.inventory([root])
        self.assertEqual(skills[0]["description"], "Review final prose for natural voice.")
        self.assertTrue(discovery.search(skills, "natural voice", None, 5))

    def test_manifest_and_skills_paths_cannot_escape_or_use_symlinks(self):
        root = self.package()
        self.skill(root)
        package = root / ".codex-plugin/plugin.json"
        for declaration in ("../", "/tmp", "skills/../../"):
            package.write_text(json.dumps({"name": "writing", "skills": declaration}))
            with self.subTest(declaration=declaration), self.assertRaises(discovery.DiscoveryError):
                self.inventory([root])
        package.write_text(json.dumps({"name": "writing", "skills": "skills"}))
        (root / "skills/escape").symlink_to(self.root, target_is_directory=True)
        with self.assertRaisesRegex(discovery.DiscoveryError, "Symlink|escapes"):
            self.inventory([root])

    def test_manifest_policy_paths_and_types_are_checked(self):
        root = self.package()
        self.skill(root)
        manifest = self.root / "selection.json"
        for entry in ({"root": root.name, "enabled": "false"},
                      {"root": root.name, "skills": {"../escape": False}},
                      {"root": root.name, "skills": {"skills/missing/SKILL.md": False}},
                      {"root": root.name, "unknownPolicy": False}):
            manifest.write_text(json.dumps({"plugins": [entry]}))
            with self.subTest(entry=entry), self.assertRaises(discovery.DiscoveryError):
                self.inventory(manifest=manifest)
        manifest.write_text('{"plugins": []}')
        self.assertEqual(self.inventory(manifest=manifest), ([], []))

    def test_missing_root_invalid_json_and_metadata_size_are_errors(self):
        with self.assertRaisesRegex(discovery.DiscoveryError, "not a directory"):
            self.inventory([self.root / "missing"])
        root = self.package()
        path = self.skill(root)
        with patch.object(discovery, "MAX_METADATA_BYTES", 10):
            with self.assertRaisesRegex(discovery.DiscoveryError, "exceeds"):
                self.inventory([root])
        (root / ".codex-plugin/plugin.json").write_text("{")
        with self.assertRaisesRegex(discovery.DiscoveryError, "Invalid JSON"):
            self.inventory([root])

    def test_traversal_depth_and_entry_count_are_bounded(self):
        root = self.package()
        self.skill(root, "nested/deep/editor")
        with patch.object(discovery, "MAX_PACKAGE_DEPTH", 1):
            with self.assertRaisesRegex(discovery.DiscoveryError, "traversal limits"):
                self.inventory([root])
        with patch.object(discovery, "MAX_PACKAGE_ENTRIES", 1):
            with self.assertRaisesRegex(discovery.DiscoveryError, "traversal limits"):
                self.inventory([root])

    def test_nested_short_description_and_roots_on_both_sides_of_command(self):
        first = self.package("first", owner="first")
        second = self.package("second", owner="second")
        for root in (first, second):
            self.skill(root, frontmatter="name: editor\ndescription: Review prose\nmetadata:\n  short-description: Everyday Humanizer\n")
        output = io.StringIO()
        with patch("sys.stdout", output), patch.object(discovery.subprocess, "Popen") as popen:
            self.assertEqual(discovery.main(["--plugin-root", str(first), "--json", "search", "Humanizer", "--plugin-root", str(second)]), 0)
        popen.assert_not_called()
        self.assertEqual(len(json.loads(output.getvalue())["skills"]), 2)

    def test_declared_root_manifest_and_unreadable_tree_are_reported(self):
        root = self.package()
        self.skill(root)
        (root / ".codex-plugin/plugin.json").rename(root / "plugin.json")
        self.assertEqual(len(self.inventory([root])[0]), 1)
        def inaccessible(*args, **kwargs):
            kwargs["onerror"](PermissionError("unreadable tree"))
        with patch.object(discovery.os, "walk", side_effect=inaccessible):
            with self.assertRaisesRegex(discovery.DiscoveryError, "unreadable tree"):
                self.inventory([root])

    def test_snapshot_cannot_be_mixed_with_portable_inputs(self):
        with patch("sys.stderr", io.StringIO()), patch.object(discovery.subprocess, "Popen") as popen:
            self.assertEqual(discovery.main(["--portable", "--inventory", "unused.json", "owners"]), 2)
        popen.assert_not_called()


class FakeStream:
    def __init__(self):
        self.data = bytearray()
        self.closed = False

    def write(self, data):
        self.data.extend(data)

    def flush(self):
        pass

    def close(self):
        self.closed = True

    def fileno(self):
        return 0


class FakeProcess:
    def __init__(self):
        self.stdin = FakeStream()
        self.stdout = FakeStream()
        self.terminated = 0
        self.killed = 0
        self.waited = 0
        self.hang_on_first_wait = False

    def poll(self):
        return None

    def terminate(self):
        self.terminated += 1

    def wait(self, timeout):
        self.waited += 1
        if self.hang_on_first_wait and self.waited == 1:
            raise subprocess.TimeoutExpired("codex", timeout)

    def kill(self):
        self.killed += 1


if __name__ == "__main__":
    unittest.main()
