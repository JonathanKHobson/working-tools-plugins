import copy
from datetime import date
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "inspect_queue.py"
spec = importlib.util.spec_from_file_location("inspect_queue", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def ledger(**changes):
    item = {"youtube_id": "AbCdEfGhI_1", "youtube_url": "https://youtu.be/AbCdEfGhI_1",
            "youtube_state": "schedule_accepted_processing",
            "youtube_publish_at": "2030-04-01T09:00:00-07:00",
            "linkedin_state": "prepared_outside_native_horizon",
            "linkedin_publish_at": "2030-04-01T09:30:00-07:00"}
    item.update(changes)
    return {"timezone": "America/Phoenix", "items": {"lesson-a": item}}


class QueueTests(unittest.TestCase):
    def check(self, data, as_of=date(2030, 1, 1), horizon=90):
        return module.inspect_queue(data, as_of, horizon)

    def test_boundary_is_advisory_and_states_are_not_inferred(self):
        data = ledger()
        before = copy.deepcopy(data)
        result = self.check(data)
        self.assertTrue(result["valid"])
        self.assertEqual(data, before)
        self.assertEqual(result["state_counts"]["youtube"], {"schedule_accepted_processing": 1})
        candidate = result["prepared_linkedin_candidates"][0]
        self.assertEqual(candidate["advisory_status"], "boundary_check_live_composer")
        self.assertEqual(candidate["next_check"], "check_live_composer")

    def test_window_inside_outside_and_missing_target(self):
        for day, expected in [("2030-03-31", "within_advisory_window"),
                              ("2030-04-02", "outside_advisory_window")]:
            result = self.check(ledger(youtube_publish_at=day + "T09:00:00-07:00",
                                       linkedin_publish_at=day + "T09:30:00-07:00"))
            self.assertEqual(result["prepared_linkedin_candidates"][0]["advisory_status"], expected)
        result = self.check(ledger(linkedin_publish_at=None))
        self.assertEqual(result["prepared_linkedin_candidates"][0]["advisory_status"], "needs_publish_at")
        self.assertIsNone(result["prepared_linkedin_candidates"][0]["linkedin_publish_at"])

    def test_duplicate_ids_error_but_date_collision_only_warns(self):
        data = ledger(linkedin_id="post-1")
        data["items"]["lesson-b"] = copy.deepcopy(data["items"]["lesson-a"])
        result = self.check(data)
        self.assertEqual(sum(x["code"] == "duplicate_platform_id" for x in result["errors"]), 2)
        data["items"]["lesson-b"].update(youtube_id="JkLmNoPqR_2", youtube_url="https://youtube.com/shorts/JkLmNoPqR_2", linkedin_id="post-2")
        result = self.check(data)
        self.assertTrue(result["valid"])
        self.assertEqual(sum(x["code"] == "platform_date_collision" for x in result["warnings"]), 2)

    def test_candidate_order_uses_instants_across_offsets(self):
        data = ledger(youtube_publish_at="2030-04-01T08:00:00-07:00",
                      linkedin_publish_at="2030-04-01T09:30:00-07:00")
        data["items"]["lesson-b"] = {
            "youtube_id": "JkLmNoPqR_2", "youtube_state": "schedule_accepted_processing",
            "youtube_publish_at": "2030-04-01T13:00:00Z", "linkedin_state": "prepared",
            "linkedin_publish_at": "2030-04-01T15:00:00Z"}
        result = self.check(data)
        self.assertTrue(result["valid"])
        self.assertEqual([item["release_id"] for item in result["prepared_linkedin_candidates"]], ["lesson-b", "lesson-a"])
        self.assertEqual(result["prepared_linkedin_candidates"][0]["linkedin_publish_at"], "2030-04-01T15:00:00Z")

    def test_prepared_without_dates_warns_without_inventing_target(self):
        data = ledger(youtube_publish_at=None, linkedin_publish_at=None)
        result = self.check(data)
        self.assertTrue(result["valid"])
        self.assertEqual(result["prepared_linkedin_candidates"], [])
        self.assertIn("prepared_linkedin_missing_publish_at", [item["code"] for item in result["warnings"]])
        self.assertIsNone(data["items"]["lesson-a"]["linkedin_publish_at"])

    def test_horizon_overflow_returns_invalid_result(self):
        for as_of, horizon in ((date(9999, 12, 31), 90), (date(2030, 1, 1), 10**30)):
            result = self.check(ledger(), as_of, horizon)
            self.assertFalse(result["valid"])
            self.assertEqual(result["errors"][0]["code"], "invalid_horizon_days")

    def test_url_variants_and_mismatch(self):
        for url in ("https://youtube.com/shorts/AbCdEfGhI_1",
                    "https://www.youtube.com/watch?v=AbCdEfGhI_1&feature=share"):
            self.assertTrue(self.check(ledger(youtube_url=url))["valid"])
        for url in ("https://youtu.be/JkLmNoPqR_2", "https://youtube.com.evil.example/watch?v=AbCdEfGhI_1", "https://[broken"):
            self.assertFalse(self.check(ledger(youtube_url=url))["valid"])

    def test_aware_timestamps_and_after_youtube_required(self):
        for stamp in ("2030-04-01", "2030-04-01T09:30:00", "bad", 42):
            self.assertFalse(self.check(ledger(linkedin_publish_at=stamp))["valid"])
        for stamp in ("2030-04-01T09:00:00-07:00", "2030-04-01T08:59:00-07:00"):
            self.assertIn("linkedin_must_follow_youtube", [x["code"] for x in self.check(ledger(linkedin_publish_at=stamp))["errors"]])

    def test_dst_order_uses_instants_not_wall_clock(self):
        data = ledger(youtube_publish_at="2030-11-03T01:50:00-04:00",
                      linkedin_publish_at="2030-11-03T01:10:00-05:00")
        data["timezone"] = "America/New_York"
        self.assertTrue(self.check(data, date(2030, 11, 1))["valid"])
        data["items"]["lesson-a"]["linkedin_publish_at"] = "2030-11-03T01:10:00-04:00"
        self.assertFalse(self.check(data, date(2030, 11, 1))["valid"])

    def test_local_date_normalization_and_historical_recheck(self):
        result = self.check(ledger(youtube_publish_at="2030-04-02T00:00:00Z",
                                  linkedin_publish_at="2030-04-02T00:30:00Z"))
        self.assertEqual(result["prepared_linkedin_candidates"][0]["advisory_status"], "boundary_check_live_composer")
        result = self.check(ledger(), date(2030, 4, 2))
        self.assertTrue(result["valid"])
        self.assertEqual(result["prepared_linkedin_candidates"], [])
        self.assertEqual(sum(x["code"] == "past_record_recheck_live" for x in result["warnings"]), 2)

    def test_malformed_shape_timezone_and_states(self):
        for data in ([], {"items": []}, {"timezone": "Unknown/Zone", "items": {}},
                     {"timezone": "America/Phoenix", "items": {"bad": []}},
                     ledger(linkedin_state=[]), ledger(youtube_id=42)):
            self.assertFalse(self.check(data)["valid"])
        self.assertFalse(self.check(ledger(), horizon=0)["valid"])

    def test_cli_compact_json_exit_codes_and_no_write(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "ledger.json"
            for content, code in ((json.dumps(ledger()), 0), ("{bad", 1),
                                  ('{"timezone":"UTC","items":{},"items":{}}', 1)):
                source.write_text(content)
                completed = subprocess.run([sys.executable, str(SCRIPT), str(source), "--as-of", "2030-01-01"], capture_output=True, text=True)
                self.assertEqual(completed.returncode, code)
                self.assertEqual(json.loads(completed.stdout)["valid"], code == 0)
                self.assertEqual(source.read_text(), content)
            completed = subprocess.run([sys.executable, str(SCRIPT), str(source), "--as-of", "2030-1-1"], capture_output=True, text=True)
            self.assertEqual(completed.returncode, 1)
            self.assertEqual(json.loads(completed.stdout)["errors"][0]["code"], "invalid_input")
            completed = subprocess.run([sys.executable, str(SCRIPT), str(source), "--as-of", "2030-01-01", "--horizon-days", "bad"], capture_output=True, text=True)
            self.assertEqual(completed.returncode, 1)
            self.assertFalse(json.loads(completed.stdout)["valid"])
            source.write_text(json.dumps(ledger()))
            for arguments in (("--as-of", "9999-12-31"),
                              ("--as-of", "2030-01-01", "--horizon-days", str(10**30))):
                completed = subprocess.run([sys.executable, str(SCRIPT), str(source), *arguments], capture_output=True, text=True)
                self.assertEqual(completed.returncode, 1)
                self.assertFalse(json.loads(completed.stdout)["valid"])
                self.assertEqual(completed.stderr, "")


if __name__ == "__main__":
    unittest.main()
