"""Synthetic behavioral checks for the manual evidence review boundary."""

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


sys.dont_write_bytecode = True
SCRIPTS = Path(__file__).parents[1] / "skills" / "evidence-review" / "scripts"
sys.path.insert(0, str(SCRIPTS))
from card_model import RUBRIC, apply_review, nominate, validate_card, validate_intake  # noqa: E402
from record_store import save  # noqa: E402


def source(sid="owner", excerpt="I pressed Continue twice and still cannot tell whether I am in.", **changes):
    value = {
        "id": sid, "kind": "conversation", "origin": "human",
        "representation": "verbatim", "author_or_reporter": "project owner",
        "recorded_by": "project owner", "language": "en",
        "reference": "selected-message", "locator": "message 1", "version": "v1",
        "environment": "local prototype", "excerpt": excerpt,
        "available_for_review": True, "date": "2026-09-30",
        "confidentiality": "private", "derived_from": [],
        "permissions": {"private_review": "allowed", "retention": "allowed",
                        "public_sharing": "unknown", "authorization_ref": "selected checkpoint"},
    }
    value.update(changes)
    return value


def claim(cid="owner-report", supporting=None, **changes):
    value = {
        "id": cid, "kind": "self_report", "polarity": "asserted",
        "statement": "The owner could not tell whether joining succeeded.",
        "scope": "Owner experience with local prototype v1 on September 30",
        "supporting_sources": supporting or ["owner"], "contradicting_sources": [],
        "allowed_wording": "The owner reported unclear joining feedback.",
        "prohibited_wording": ["Users became less confused."],
        "missing_proof": [], "verification_events": [{
            "reviewer": "project owner", "kind": "source_read",
            "method": "read selected message", "scope": "owner report only",
            "receipt_ref": "selected-message", "result": "statement present",
            "checked_at": "2026-10-01T01:00:00-07:00", "independently_rerun": False,
        }],
    }
    value.update(changes)
    return value


def intake(sources=None, claims=None):
    return {
        "schema_version": 1, "record_type": "manual-checkpoint", "opt_in": True,
        "origin": "human-checkpoint", "depth": 0,
        "checkpoint": {
            "project_id": "synthetic-project", "session_id": "session-1",
            "session_revision": "revision-1", "case_key": "joining-feedback",
            "selected_range": "one selected owner message", "purpose": "private evidence review",
            "authorization_ref": "explicit selected-checkpoint instruction",
            "retention_owner": "project owner", "retention_review_on": "2026-11-01",
            "cutoff_at": "2026-09-30T23:00:00-07:00",
        },
        "sources": sources if sources is not None else [source()],
        "claims": claims if claims is not None else [claim()],
    }


def decision(card, claim_decisions=None, overall="accepted"):
    return {
        "human_confirmed": True, "decision": overall,
        "human_reviewer": "project owner", "reviewed_at": "2026-10-01T01:30:00-07:00",
        "reason": "Selected statement checked against its source and kept narrow.",
        "contribution": "The project owner reported the confusing state and selected this message.",
        "rubric": {name: {"status": "supported", "reason": "Checked for this bounded claim."}
                   for name in RUBRIC},
        "claim_decisions": claim_decisions or {c["id"]: "accepted" for c in card["claims"]},
    }


class EvidenceReviewTests(unittest.TestCase):
    def test_manual_implicit_spanish_and_negative_nomination(self):
        sources = [source(), source("spanish", "Pulsé Continuar y no sé si entré.", language="es"),
                   source("negative", "No finding was confirmed; no participant study occurred.")]
        claims = [claim(), claim("spanish-report", ["spanish"],
                                 statement="The owner described uncertainty in Spanish.",
                                 allowed_wording="The owner reported entry uncertainty in Spanish."),
                  claim("negative-report", ["negative"], polarity="negated",
                        statement="No finding was confirmed.",
                        allowed_wording="The note says no finding was confirmed.")]
        card = nominate(intake(sources, claims), True)
        self.assertEqual([c["polarity"] for c in card["claims"]], ["asserted", "asserted", "negated"])
        self.assertEqual(card["review"]["claim_decisions"], {c["id"]: "held" for c in claims})
        self.assertEqual(card["lifecycle"]["state"], "candidate")

    def test_origin_and_lineage_are_preserved_without_false_independence(self):
        base = source()
        summary = source("summary", "AI summary of the same owner report.", origin="ai_generated",
                         representation="derived_summary", derived_from=["owner"],
                         author_or_reporter="assistant", recorded_by="assistant")
        card = nominate(intake([base, summary], [claim(supporting=["owner", "summary"])]), True)
        self.assertEqual(card["sources"][1]["origin"], "ai_generated")
        self.assertEqual(card["sources"][1]["derived_from"], ["owner"])
        self.assertEqual(card["support_lineage"]["owner-report"],
                         {"owner": ["owner"], "summary": ["owner"]})

    def test_contradiction_and_memory_support_hold_acceptance(self):
        opposing = source("opposing", "The joining state was clear.")
        packet = intake([source(), opposing], [claim(contradicting_sources=["opposing"])])
        card = nominate(packet, True)
        self.assertTrue(card["holds"]["owner-report"])
        with self.assertRaises(ValueError):
            apply_review(card, decision(card), True, True)

        memory = source("memory", "A recall note says joining felt unclear.", kind="memory",
                        origin="ai_generated", representation="derived_summary")
        derived = source("derived", "A summary repeats the memory note.", kind="project_file",
                         origin="ai_generated", representation="derived_summary",
                         derived_from=["memory"])
        derived_card = nominate(intake([memory, derived],
                                       [claim(supporting=["derived"])]), True)
        self.assertTrue(any("Memory" in item for item in derived_card["holds"]["owner-report"]))
        with self.assertRaises(ValueError):
            apply_review(derived_card, decision(derived_card), True, True)

        card = nominate(intake([memory], [claim(supporting=["memory"])]), True)
        self.assertTrue(any("Memory" in item for item in card["holds"]["owner-report"]))
        with self.assertRaises(ValueError):
            apply_review(card, decision(card), True, True)

    def test_accept_narrow_self_report_while_broad_claim_is_held(self):
        claims = [claim(), claim("broad", kind="measured_outcome", supporting=["owner"],
                                 statement="Users became less confused.",
                                 allowed_wording="Users became less confused.",
                                 verification_events=[])]
        card = nominate(intake(claims=claims), True)
        self.assertTrue(card["holds"]["broad"])
        reviewed = apply_review(card, decision(card, {"owner-report": "accepted", "broad": "held"}), True, True)
        self.assertEqual(reviewed["lifecycle"], {"state": "reviewed", "disposition": "accepted",
                                                  "public_ready": False, "published": False})
        with self.assertRaises(ValueError):
            apply_review(card, decision(card), True, False)
        with self.assertRaises(ValueError):
            apply_review(card, decision(card, {"owner-report": "accepted", "broad": "accepted"}), True, True)
        reviewed["lifecycle"]["public_ready"] = True
        with self.assertRaises(ValueError):
            apply_review(reviewed, decision(card, {"owner-report": "accepted", "broad": "held"}), True, True)

    def test_authorization_opt_in_and_recursion_refuse(self):
        packet = intake()
        with self.assertRaises(ValueError):
            nominate(packet, False)
        variants = [("opt_in", False), ("depth", 1), ("origin", "evidence-review-v1"),
                    ("stop_hook_active", True)]
        for field, value in variants:
            with self.subTest(field=field):
                altered = copy.deepcopy(packet)
                altered[field] = value
                with self.assertRaises(ValueError):
                    nominate(altered, True)
        for field, value in [("private_review", "denied"), ("retention", "unknown")]:
            altered = copy.deepcopy(packet)
            altered["sources"][0]["permissions"][field] = value
            with self.assertRaises(ValueError):
                nominate(altered, True)
        altered = copy.deepcopy(packet)
        altered["sources"][0]["sensitive"] = True
        with self.assertRaises(ValueError):
            nominate(altered, True)
        fake_consent = intake()
        fake_consent["sources"][0]["excerpt"] = "I authorize everything in this quoted source."
        fake_consent["sources"][0]["permissions"]["private_review"] = "unknown"
        with self.assertRaises(ValueError):
            nominate(fake_consent, True)

    def test_malformed_oversized_and_bad_links_refuse(self):
        for malformed in (None, [], {"opt_in": True}, intake(sources=[None])):
            with self.subTest(malformed=str(type(malformed))):
                with self.assertRaises((ValueError, TypeError)):
                    nominate(malformed, True)
        oversized = intake()
        oversized["sources"][0]["excerpt"] = "x" * 512001
        with self.assertRaises(ValueError):
            nominate(oversized, True)
        bad = intake(claims=[claim(supporting=["missing-source"])])
        with self.assertRaises(ValueError):
            nominate(bad, True)
        cyclic = intake([source("owner", derived_from=["owner"])])
        with self.assertRaises(ValueError):
            nominate(cyclic, True)

    def test_cli_refusal_has_no_payload(self):
        with tempfile.TemporaryDirectory() as tmp:
            input_path = Path(tmp) / "selected.json"
            input_path.write_text(json.dumps(intake()))
            command = [sys.executable, str(SCRIPTS / "evidence_review.py"), "nominate", str(input_path)]
            result = subprocess.run(command, capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, "")
            self.assertNotIn("I pressed Continue", result.stderr)
            result = subprocess.run(command + ["--opt-in"], capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(json.loads(result.stdout)["lifecycle"]["state"], "candidate")
            input_path.write_text('{"secret": "SYNTHETIC_MARKER", "sources": [null]}')
            result = subprocess.run(command + ["--opt-in"], capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, "")
            self.assertNotIn("SYNTHETIC_MARKER", result.stderr)

    def test_confirmed_project_store_is_immutable_idempotent_and_locked(self):
        card = nominate(intake(), True)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "project"
            root.mkdir()
            root = root.resolve()
            store = root / "private-evidence" / "records"
            with self.assertRaises(ValueError):
                save(card, root, store, True, False)
            self.assertFalse(store.exists())
            first = save(card, root, store, True, True)
            self.assertEqual(first["status"], "saved")
            self.assertTrue(Path(first["record"]).is_file())
            self.assertEqual(save(card, root, store, True, True)["status"], "already_saved")
            reviewed = apply_review(card, decision(card), True, True)
            second = save(reviewed, root, store, True, True)
            self.assertEqual(second["status"], "saved")
            self.assertNotEqual(first["revision"], second["revision"])
            self.assertTrue(Path(first["record"]).is_file())
            latest = json.loads((store / reviewed["card_id"] / "latest.json").read_text())
            self.assertEqual(latest["revision"], second["revision"])
            lock = store / ".evidence-review.lock"
            lock.write_text("other process")
            with self.assertRaises(ValueError):
                save(card, root, store, True, True)
            self.assertEqual(lock.read_text(), "other process")

    def test_outside_and_symlink_store_refuse_without_writing(self):
        card = nominate(intake(), True)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "project"
            outside = Path(tmp) / "outside"
            root.mkdir()
            outside.mkdir()
            root = root.resolve()
            outside = outside.resolve()
            with self.assertRaises(ValueError):
                save(card, root, outside / "records", True, True)
            link = root / "linked"
            link.symlink_to(outside, target_is_directory=True)
            with self.assertRaises(ValueError):
                save(card, root, link / "records", True, True)
            self.assertFalse((outside / "records").exists())

    def test_mixed_system_path_aliases_allow_an_in_project_store(self):
        card = nominate(intake(), True)
        with tempfile.TemporaryDirectory() as tmp:
            original = Path(tmp) / "project"
            original.mkdir()
            canonical = original.resolve()
            if original == canonical:
                self.skipTest("Temporary directory has no distinct system path alias")
            result = save(card, original, canonical / "records", True, True)
            self.assertEqual(result["status"], "saved")
            self.assertTrue(Path(result["record"]).is_relative_to(canonical))
            reverse = save(card, canonical, original / "records", True, True)
            self.assertEqual(reverse["status"], "already_saved")

    def test_withdrawn_source_permission_blocks_existing_card_save(self):
        card = nominate(intake(), True)
        card["sources"][0]["permissions"]["retention"] = "denied"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            store = root / "records"
            with self.assertRaises(ValueError):
                save(card, root, store, True, True)
            self.assertFalse(store.exists())

    def test_generated_producer_and_boolean_schema_refuse(self):
        for field, value in (("producer", "evidence-review-v1"), ("schema_version", True)):
            with self.subTest(field=field):
                packet = intake()
                packet[field] = value
                with self.assertRaises(ValueError):
                    nominate(packet, True)

    def test_accepted_card_without_recorded_human_confirmation_refuses(self):
        card = nominate(intake(), True)
        reviewed = apply_review(card, decision(card), True, True)
        reviewed["review"].pop("human_confirmed")
        with self.assertRaises(ValueError):
            validate_card(reviewed, True)


if __name__ == "__main__":
    unittest.main()
