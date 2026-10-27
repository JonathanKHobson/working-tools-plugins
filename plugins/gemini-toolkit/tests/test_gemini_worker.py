"""Offline invariants for the bounded Gemini wrapper."""
import importlib.util
from pathlib import Path
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "gemini_worker.py"
SPEC = importlib.util.spec_from_file_location("gemini_worker", SCRIPT)
gemini_worker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gemini_worker)


class GeminiWorkerTests(unittest.TestCase):
    def test_completed_assistant_and_explicit_usage_are_parsed(self):
        raw = '\n'.join([
            '{"event":"init","init":{"model":"configured-alias"}}',
            '{"event":"result","result":{"status":"SUCCESS","response":"Done","model":"gemini-3.8-flash-medium","usage":{"input_tokens":12,"output_tokens":4}}}',
        ])
        self.assertEqual(
            gemini_worker.parse_stream(raw),
            ("Done", "gemini-3.8-flash-medium", 12, 4),
        )

    def test_terminal_failure_is_not_success(self):
        with self.assertRaises(RuntimeError):
            gemini_worker.parse_stream('{"event":"result","result":{"status":"ERROR","response":"partial"}}')

    def test_unknown_schema_is_preserved(self):
        self.assertEqual(gemini_worker.parse_stream('{"type":"future"}'), (None, None, None, None))

    def test_init_model_is_not_actual_model(self):
        raw = '{"type":"init","model":"configured-alias"}\n{"type":"future"}'
        self.assertIsNone(gemini_worker.parse_stream(raw)[1])
        self.assertEqual(gemini_worker.stream_evidence(raw)["cli_init_models"], ["configured-alias"])


if __name__ == "__main__":
    unittest.main()
