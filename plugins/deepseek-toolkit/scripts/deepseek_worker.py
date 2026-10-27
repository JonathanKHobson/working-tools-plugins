#!/usr/bin/env python3
"""Bounded supplied-text delegation through NVIDIA's fixed DeepSeek endpoint."""
import argparse
import getpass
import importlib.util
import json
import os
from pathlib import Path
import re
import socket
import stat
import sys
import tempfile
import time
import urllib.error
import urllib.request

ENDPOINT = "https://integrate.api.nvidia.com/v1/chat/completions"
MODEL = "deepseek-ai/deepseek-v4.1-flash"
MAX_INPUT_BYTES = 65536
MAX_RESPONSE_BYTES = 4 * 1024 * 1024


def record_usage(event):
    """Fail-open, metadata-only opt-in recorder. Never starts a process."""
    try:
        path = Path.home() / ".config/studio-tools/usage-tracking.json"
        if not path.is_file():
            return
        config = json.loads(path.read_text())
        if config.get("enabled") is not True or not config.get("recorder_path"):
            return
        spec = importlib.util.spec_from_file_location("deepseek_usage_ledger", config["recorder_path"])
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if module.record(event) is False:
            print("Usage tracking warning: recorder rejected event", file=sys.stderr)
    except Exception:
        print("Usage tracking warning: recorder unavailable", file=sys.stderr)


def key_path():
    return Path(os.environ.get("DEEPSEEK_API_KEY_FILE") or
                Path.home() / ".config/deepseek-toolkit/nvidia-api-key").expanduser()


def credential_configured():
    # Presence is configuration evidence only, never an authentication claim.
    return bool(os.environ.get("NVIDIA_API_KEY", "").strip()) or key_path().is_file()


def load_key():
    key = os.environ.get("NVIDIA_API_KEY", "").strip()
    if not key:
        path = key_path()
        try:
            with path.open("r") as stream:
                info = os.fstat(stream.fileno())
                if not stat.S_ISREG(info.st_mode) or info.st_mode & 0o077:
                    raise ValueError("Credential file must be private (mode 0600).")
                key = stream.read(8193).strip()
        except (OSError, UnicodeError):
            raise ValueError("Credential unavailable. Use --set-key or NVIDIA_API_KEY.") from None
    if not key or len(key) > 8192 or any(c.isspace() for c in key):
        raise ValueError("Credential missing or invalid. Use --set-key or NVIDIA_API_KEY.")
    return key


def store_key(key):
    key = key.strip()
    if not key or len(key) > 8192 or any(c.isspace() for c in key):
        raise ValueError("Credential must be nonempty and contain no whitespace.")
    path = key_path()
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".key-", dir=path.parent)
    try:
        with os.fdopen(fd, "w") as stream:
            os.fchmod(stream.fileno(), 0o600)
            stream.write(key + "\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise urllib.error.HTTPError(req.full_url, code, "Redirect rejected", headers, fp)


def token_count(value):
    return value if type(value) is int and 0 <= value <= 10**12 else None


def ledger_model(value):
    # Returned identity is untrusted; never record URLs, paths, email or free text.
    if (isinstance(value, str) and re.fullmatch(r"[A-Za-z0-9_.+-]+(?:/[A-Za-z0-9_.+-]+)?", value)
            and len(value) <= 120):
        return value
    return None


def infer(prompt, key, max_tokens=4096, timeout=300):
    payload = {"model": MODEL, "messages": [
        {"role": "system", "content": "Complete the supplied text task. You have no tools, filesystem, shell, or external actions. Return only your text result."},
        {"role": "user", "content": prompt}], "max_tokens": max_tokens,
        "stream": False, "chat_template_kwargs": {"thinking": False}}
    request = urllib.request.Request(ENDPOINT, data=json.dumps(payload).encode("utf-8"),
                                     headers={"Authorization": "Bearer " + key,
                                              "Content-Type": "application/json", "Accept": "application/json"},
                                     method="POST")
    opener = urllib.request.build_opener(NoRedirect())
    event = {"kind": "provider", "provider": "deepseek", "plugin": "deepseek-toolkit",
             "operation": "deepseek-worker", "requested_model": MODEL,
             "actual_model": None, "status": "failure", "input_tokens": None,
             "output_tokens": None}
    started = time.monotonic()
    try:
        # Exactly one attempt. Redirects and all failures terminate without fallback.
        with opener.open(request, timeout=timeout) as response:
            raw = response.read(MAX_RESPONSE_BYTES + 1)
        if len(raw) > MAX_RESPONSE_BYTES:
            raise ValueError("response limit")
        data = json.loads(raw)
        if not isinstance(data, dict):
            raise ValueError("response shape")
        actual_model = data.get("model") if isinstance(data.get("model"), str) else None
        event["actual_model"] = ledger_model(actual_model)
        usage = data.get("usage") if isinstance(data.get("usage"), dict) else {}
        event["input_tokens"] = token_count(usage.get("prompt_tokens"))
        event["output_tokens"] = token_count(usage.get("completion_tokens"))
        choice = data["choices"][0]
        result = choice["message"]["content"]
        if not isinstance(result, str) or not result.strip() or data.get("error"):
            raise ValueError("response content")
        finish_reason = choice.get("finish_reason")
        if not isinstance(finish_reason, str) or not finish_reason.strip():
            finish_reason = None
        completed = None if finish_reason is None else finish_reason == "stop"
        event["status"] = ("completed_unknown" if completed is None else
                           "success" if completed else "failure")
        return {"response": result, "requested_model": MODEL, "actual_model": actual_model,
                "finish_reason": finish_reason, "completed": completed,
                "truncated": finish_reason == "length" if finish_reason is not None else None,
                "status": event["status"],
                "usage": {"input_tokens": event["input_tokens"], "output_tokens": event["output_tokens"]},
                "duration_ms": round((time.monotonic() - started) * 1000),
                "endpoint": ENDPOINT, "provider": "deepseek", "backend": "nvidia",
                "inferenceTested": True}
    except (TimeoutError, socket.timeout):
        event["status"] = "timeout"
        raise RuntimeError("Inference timed out; no retry or fallback was attempted.") from None
    except urllib.error.HTTPError as error:
        category = {401: "credential/access", 403: "credential/access",
                    429: "throttle", 402: "allowance"}.get(error.code, "HTTP request")
        raise RuntimeError(f"Inference {category} failure (HTTP {error.code}); no retry or fallback was attempted.") from None
    except urllib.error.URLError as error:
        if isinstance(error.reason, (TimeoutError, socket.timeout)):
            event["status"] = "timeout"
            raise RuntimeError("Inference timed out; no retry or fallback was attempted.") from None
        raise RuntimeError("Inference request failed; no retry or fallback was attempted.") from None
    except Exception:
        raise RuntimeError("Inference failed or returned an invalid response; no retry or fallback was attempted.") from None
    finally:
        event["duration_ms"] = round((time.monotonic() - started) * 1000)
        try:
            record_usage(event)
        except Exception:
            pass  # Even a replaced/broken recorder cannot affect task completion.


def bounded_integer(low, high):
    def parse(value):
        number = int(value)
        if not low <= number <= high:
            raise argparse.ArgumentTypeError(f"must be between {low} and {high}")
        return number
    return parse


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="Check configuration without inference or authentication test")
    mode.add_argument("--set-key", action="store_true", help="Securely prompt for and store the NVIDIA key")
    parser.add_argument("--json", action="store_true", help="Return result and provider metadata as JSON")
    parser.add_argument("--max-tokens", type=bounded_integer(1, 16384), default=4096)
    parser.add_argument("--timeout", type=bounded_integer(1, 300), default=300)
    args = parser.parse_args(argv)
    try:
        if args.check:
            print(json.dumps({"credentialConfigured": credential_configured(), "inferenceTested": False,
                              "authenticationVerified": False, "requested_model": MODEL,
                              "endpoint": ENDPOINT, "backend": "nvidia"}))
            return 0
        if args.set_key:
            store_key(getpass.getpass("NVIDIA API key (hidden): "))
            print("Credential stored privately. Authentication and inference remain untested.")
            return 0
        if sys.stdin.isatty():
            raise ValueError("Supply a bounded text task through stdin.")
        raw = sys.stdin.buffer.read(MAX_INPUT_BYTES + 1)
        if len(raw) > MAX_INPUT_BYTES:
            raise ValueError("Input exceeds 65536 bytes.")
        try:
            prompt = raw.decode("utf-8")
        except UnicodeError:
            raise ValueError("Input must be UTF-8 text.") from None
        if not prompt.strip() or "\x00" in prompt:
            raise ValueError("Input must be nonempty text without NUL bytes.")
        result = infer(prompt, load_key(), args.max_tokens, args.timeout)
        print(json.dumps(result, ensure_ascii=False) if args.json else result["response"])
        if result["completed"] is not True:
            print("Inference completion is unverified." if result["completed"] is None else
                  "Inference output is incomplete; no retry or fallback was attempted.", file=sys.stderr)
            return 2
        return 0
    except (ValueError, RuntimeError, OSError, EOFError):
        # Only controlled errors are exposed; OS/provider exception details can contain secrets.
        error = sys.exc_info()[1]
        message = str(error) if type(error) in (ValueError, RuntimeError) else "Configuration operation failed."
        print(message, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
