import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch
import urllib.error

SPEC = importlib.util.spec_from_file_location("deepseek_worker", Path(__file__).parents[1] / "scripts/deepseek_worker.py")
worker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(worker)


class WorkerTests(unittest.TestCase):
    def response(self, model="returned-model"):
        data = {"choices": [{"message": {"content": "answer"}, "finish_reason": "stop"}],
                "usage": {"prompt_tokens": 7, "completion_tokens": 3}}
        if model is not None:
            data["model"] = model
        response = Mock()
        response.read.return_value = json.dumps(data).encode()
        response.__enter__ = Mock(return_value=response)
        response.__exit__ = Mock(return_value=False)
        return response

    def test_success_fixed_backend_payload_identity_and_one_event(self):
        opener = Mock()
        opener.open.return_value = self.response()
        with patch.object(worker.urllib.request, "build_opener", return_value=opener), patch.object(worker, "record_usage") as record:
            result = worker.infer("private supplied task", "dummy", 100, 25)
        request = opener.open.call_args.args[0]
        self.assertEqual(request.full_url, worker.ENDPOINT)
        payload = json.loads(request.data)
        self.assertEqual(payload["model"], worker.MODEL)
        self.assertEqual(payload["chat_template_kwargs"], {"thinking": False})
        self.assertNotIn("tools", payload)
        self.assertEqual(result["actual_model"], "returned-model")
        self.assertIs(result["completed"], True)
        self.assertEqual(result["finish_reason"], "stop")
        self.assertEqual(result["usage"], {"input_tokens": 7, "output_tokens": 3})
        self.assertEqual(result["endpoint"], worker.ENDPOINT)
        opener.open.assert_called_once()
        record.assert_called_once()
        event = record.call_args.args[0]
        self.assertEqual(event["status"], "success")
        self.assertEqual(event["actual_model"], "returned-model")
        self.assertEqual(event["provider"], "deepseek")
        self.assertNotIn("private", json.dumps(event))
        self.assertNotIn("https", json.dumps(event))

    def test_missing_identity_and_usage_stay_unknown(self):
        opener = Mock()
        response = self.response(None)
        data = json.loads(response.read.return_value)
        data["usage"] = {"prompt_tokens": True, "completion_tokens": -1}
        response.read.return_value = json.dumps(data).encode()
        opener.open.return_value = response
        with patch.object(worker.urllib.request, "build_opener", return_value=opener), patch.object(worker, "record_usage") as record:
            result = worker.infer("task", "dummy")
        self.assertIsNone(result["actual_model"])
        self.assertIsNone(record.call_args.args[0]["actual_model"])
        self.assertEqual(result["usage"], {"input_tokens": None, "output_tokens": None})

    def test_failures_sanitized_single_attempt_single_event(self):
        cases = [(TimeoutError("private secret"), "timeout"),
                 (urllib.error.URLError(TimeoutError("private secret")), "timeout"),
                 (urllib.error.HTTPError(worker.ENDPOINT, 401, "private secret", {}, None), "failure"),
                 (ValueError("private secret"), "failure")]
        for error, status in cases:
            with self.subTest(status=status, error=type(error)):
                opener = Mock()
                opener.open.side_effect = error
                with patch.object(worker.urllib.request, "build_opener", return_value=opener), patch.object(worker, "record_usage") as record:
                    with self.assertRaises(RuntimeError) as caught:
                        worker.infer("private task", "dummy")
                self.assertNotIn("private", str(caught.exception))
                opener.open.assert_called_once()
                record.assert_called_once()
                self.assertEqual(record.call_args.args[0]["status"], status)

    def test_empty_content_is_failure(self):
        for content in ("", " \n\t"):
            opener = Mock()
            response = self.response()
            data = json.loads(response.read.return_value)
            data["choices"][0]["message"]["content"] = content
            response.read.return_value = json.dumps(data).encode()
            opener.open.return_value = response
            with patch.object(worker.urllib.request, "build_opener", return_value=opener), patch.object(worker, "record_usage") as record:
                with self.assertRaises(RuntimeError): worker.infer("task", "dummy")
            opener.open.assert_called_once()
            record.assert_called_once()
            self.assertEqual(record.call_args.args[0]["status"], "failure")

    def test_truncation_and_unknown_completion_preserve_partial_output(self):
        for reason, completed, status in (("length", False, "failure"), (None, None, "completed_unknown")):
            with self.subTest(reason=reason):
                opener = Mock()
                response = self.response()
                data = json.loads(response.read.return_value)
                if reason is None:
                    del data["choices"][0]["finish_reason"]
                else:
                    data["choices"][0]["finish_reason"] = reason
                response.read.return_value = json.dumps(data).encode()
                opener.open.return_value = response
                with patch.object(worker.urllib.request, "build_opener", return_value=opener), patch.object(worker, "record_usage") as record:
                    result = worker.infer("task", "dummy")
                self.assertEqual(result["response"], "answer")
                self.assertIs(result["completed"], completed)
                self.assertEqual(result["finish_reason"], reason)
                self.assertEqual(result["status"], status)
                self.assertEqual(record.call_args.args[0]["status"], status)
                opener.open.assert_called_once()
                record.assert_called_once()
                stdin = Mock()
                stdin.isatty.return_value = False
                stdin.buffer = io.BytesIO(b"task")
                output = io.StringIO()
                with patch.object(worker.sys, "stdin", stdin), patch.object(worker, "load_key", return_value="dummy"), patch.object(worker, "infer", return_value=result), contextlib.redirect_stdout(output), contextlib.redirect_stderr(io.StringIO()):
                    self.assertEqual(worker.main(["--json"]), 2)
                self.assertEqual(json.loads(output.getvalue())["response"], "answer")

    def test_http_categories_expose_no_provider_detail(self):
        for code, category in ((401, "credential/access"), (403, "credential/access"), (429, "throttle"), (402, "allowance"), (500, "HTTP request")):
            opener = Mock()
            opener.open.side_effect = urllib.error.HTTPError(worker.ENDPOINT, code, "private body key", {}, None)
            with patch.object(worker.urllib.request, "build_opener", return_value=opener), patch.object(worker, "record_usage") as record:
                with self.assertRaises(RuntimeError) as caught: worker.infer("task", "dummy")
            self.assertIn(category, str(caught.exception))
            self.assertIn(str(code), str(caught.exception))
            self.assertNotIn("private", str(caught.exception))
            opener.open.assert_called_once()
            record.assert_called_once()

    def test_redirect_rejected(self):
        request = worker.urllib.request.Request(worker.ENDPOINT)
        with self.assertRaises(urllib.error.HTTPError):
            worker.NoRedirect().redirect_request(request, None, 302, "moved", {}, "https://elsewhere.invalid")

    def test_unsafe_reported_identity_never_enters_ledger(self):
        opener = Mock()
        opener.open.return_value = self.response("https://private.invalid/secret")
        with patch.object(worker.urllib.request, "build_opener", return_value=opener), patch.object(worker, "record_usage") as record:
            worker.infer("task", "dummy")
        self.assertIsNone(record.call_args.args[0]["actual_model"])

    def test_recorder_failure_does_not_fail_inference(self):
        opener = Mock()
        opener.open.return_value = self.response()
        with patch.object(worker.urllib.request, "build_opener", return_value=opener), patch.object(worker, "record_usage", side_effect=RuntimeError):
            self.assertEqual(worker.infer("task", "dummy")["response"], "answer")

    def test_preflight_input_missing_key_and_check_no_inference_or_event(self):
        class Input:
            def __init__(self, raw): self.buffer = io.BytesIO(raw)
            def isatty(self): return False
        with tempfile.TemporaryDirectory() as root, patch.dict(os.environ, {"DEEPSEEK_API_KEY_FILE": str(Path(root) / "absent"), "NVIDIA_API_KEY": ""}), patch.object(worker, "infer") as infer, patch.object(worker, "record_usage") as record:
            for raw in (b"", b"a" * 65537, b"\xff", b"task"):
                with patch.object(worker.sys, "stdin", Input(raw)), contextlib.redirect_stderr(io.StringIO()):
                    self.assertEqual(worker.main([]), 1)
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(worker.main(["--check"]), 0)
            check = json.loads(output.getvalue())
            self.assertFalse(check["credentialConfigured"])
            self.assertFalse(check["inferenceTested"])
            self.assertFalse(check["authenticationVerified"])
            infer.assert_not_called()
            record.assert_not_called()

    def test_credential_atomic_private_and_insecure_file_rejected(self):
        with tempfile.TemporaryDirectory() as root, patch.dict(os.environ, {"DEEPSEEK_API_KEY_FILE": str(Path(root) / "key"), "NVIDIA_API_KEY": ""}):
            worker.store_key("test-only-placeholder")
            path = worker.key_path()
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            self.assertEqual(worker.load_key(), "test-only-placeholder")
            self.assertEqual(list(Path(root).iterdir()), [path])
            path.chmod(0o644)
            with self.assertRaises(ValueError): worker.load_key()

    def test_set_key_and_configuration_check_do_not_test_auth_or_log(self):
        with tempfile.TemporaryDirectory() as root, patch.dict(os.environ, {"DEEPSEEK_API_KEY_FILE": str(Path(root) / "key"), "NVIDIA_API_KEY": ""}), patch.object(worker, "infer") as infer, patch.object(worker, "record_usage") as record, patch.object(worker.getpass, "getpass", return_value="test-only-placeholder"):
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(worker.main(["--set-key"]), 0)
            self.assertNotIn("test-only-placeholder", output.getvalue())
            output = io.StringIO()
            with patch.object(worker, "load_key", side_effect=AssertionError("must not read credential")), contextlib.redirect_stdout(output):
                self.assertEqual(worker.main(["--check"]), 0)
            check = json.loads(output.getvalue())
            self.assertTrue(check["credentialConfigured"])
            self.assertFalse(check["authenticationVerified"])
            self.assertFalse(check["inferenceTested"])
            infer.assert_not_called()
            record.assert_not_called()

    def test_bounds_and_no_model_or_endpoint_override(self):
        for args in (["--max-tokens", "16385"], ["--timeout", "301"], ["--model", "other"], ["--endpoint", "other"]):
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                worker.main(args)

    def test_disabled_tracking_does_not_load_recorder(self):
        with tempfile.TemporaryDirectory() as root:
            home = Path(root)
            config = home / ".config/studio-tools/usage-tracking.json"
            config.parent.mkdir(parents=True)
            config.write_text(json.dumps({"enabled": False, "recorder_path": "/never-import"}))
            with patch.object(worker.Path, "home", return_value=home), patch.object(worker.importlib.util, "spec_from_file_location") as load:
                worker.record_usage({"status": "success"})
            load.assert_not_called()


if __name__ == "__main__":
    unittest.main()
