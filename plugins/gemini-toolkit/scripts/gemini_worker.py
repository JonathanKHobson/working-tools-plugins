#!/usr/bin/env python3
"""Run one bounded text task through the authenticated Antigravity CLI."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import select
import time
import uuid


DEFAULT_CLI = Path(shutil.which("agy") or Path.home() / ".local/bin/agy")


def record_usage(event):
    """Best-effort optional usage recording; tracking must never affect work."""
    try:
        config_path = Path.home() / ".config/studio-tools/usage-tracking.json"
        if not config_path.is_file():
            return
        config = json.loads(config_path.read_text())
        recorder_path = config.get("recorder_path")
        if not config.get("enabled", True) or not recorder_path:
            return
        spec = importlib.util.spec_from_file_location("usage_ledger", recorder_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if module.record(event) is False:
            print("Usage tracking warning: recorder rejected event", file=sys.stderr)
    except Exception:  # pragma: no cover - fail-open boundary
        print("Usage tracking warning: recorder unavailable", file=sys.stderr)


def parse_stream(raw):
    """Extract only explicit completed assistant fields from stream-json."""
    text = None
    actual = None
    input_tokens = output_tokens = None
    for line in raw.splitlines():
        try:
            item = json.loads(line)
        except ValueError:
            continue
        if not isinstance(item, dict):
            continue
        if item.get("event") == "error":
            raise RuntimeError("Antigravity reported an error event")
        envelope = item.get("result") if item.get("event") == "result" else None
        if isinstance(envelope, dict) and envelope.get("status") not in (None, "SUCCESS"):
            raise RuntimeError("Antigravity did not report successful completion")
        if isinstance(envelope, dict) and envelope.get("status") == "SUCCESS":
            candidate = envelope.get("response")
            if isinstance(candidate, str) and candidate.strip():
                text = candidate
            else:
                raise RuntimeError("Antigravity returned an empty completed response")
            actual = envelope.get("model") or envelope.get("modelId")
            usage = envelope.get("usage") if isinstance(envelope.get("usage"), dict) else {}
            input_tokens = usage.get("input_tokens")
            output_tokens = usage.get("output_tokens")
        else:
            usage = {}
        input_tokens = input_tokens if input_tokens is not None else usage.get("input_tokens")
        output_tokens = output_tokens if output_tokens is not None else usage.get("output_tokens")
    return text, actual, input_tokens, output_tokens


def stream_evidence(raw):
    """Summarize CLI identity and event types without claiming backend attestation."""
    configured_models = []
    event_counts = {}
    for line in raw.splitlines():
        try:
            item = json.loads(line)
        except ValueError:
            continue
        if not isinstance(item, dict):
            continue
        event_type = item.get("event") or item.get("type") or "unknown"
        event_counts[event_type] = event_counts.get(event_type, 0) + 1
        init = item.get("init") if isinstance(item.get("init"), dict) else item
        if (item.get("event") or item.get("type")) == "init":
            model = init.get("model") or init.get("modelId")
            if isinstance(model, str):
                configured_models.append(model)
    return {"cli_init_models": configured_models, "event_counts": event_counts}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True)
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--cli", type=Path, default=Path(os.environ.get("AGY_CLI", DEFAULT_CLI)))
    parser.add_argument("--receipt-file", type=Path,
                        help="Write a local JSON receipt with CLI model and event evidence")
    args = parser.parse_args()
    if not 1 <= args.timeout <= 600:
        parser.error("--timeout must be between 1 and 600")
    if sys.stdin.isatty():
        parser.error("Supply the task on standard input")
    deadline = time.monotonic() + 15
    chunks = []
    total = 0
    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0 or not select.select([sys.stdin], [], [], remaining)[0]:
            raise RuntimeError("Task input did not close within 15 seconds")
        chunk = os.read(sys.stdin.fileno(), 65536)
        if not chunk:
            break
        total += len(chunk)
        if total > 262144:
            raise RuntimeError("Task exceeds 256 KiB")
        chunks.append(chunk)
    prompt = b"".join(chunks).decode("utf-8")
    if not prompt.strip():
        parser.error("Task is empty")
    if not args.cli.is_file() or not os.access(args.cli, os.X_OK):
        raise RuntimeError(f"Antigravity CLI is not executable: {args.cli}")
    payload = json.dumps({"event": "user", "message": {"content": prompt}}) + "\n"
    command = [str(args.cli), "--input-format", "stream-json", "--output-format", "stream-json",
               "--model", args.model, "--print-timeout", "5m", "--sandbox"]
    started = time.monotonic()
    status = "failure"
    raw = ""
    actual = input_tokens = output_tokens = None
    stderr = ""
    try:
        completed = subprocess.run(command, input=payload, capture_output=True, text=True,
                                   timeout=args.timeout)
        raw = completed.stdout
        stderr = completed.stderr
        if completed.returncode:
            status = "failure"
            raise RuntimeError(completed.stderr.strip() or "Antigravity command failed")
        text, actual, input_tokens, output_tokens = parse_stream(raw)
        if text:
            status = "success"
            print(text)
        else:
            # Preserve provider output when its schema is newer than this wrapper.
            print(raw, end="")
            status = "completed_unknown"
    except subprocess.TimeoutExpired:
        status = "timeout"
        raise
    except Exception:
        if status == "success":
            status = "failure"
        raise
    finally:
        if args.receipt_file:
            receipt = {"requested_model": args.model, "completion_model": actual,
                       "status": status, "input_tokens": input_tokens,
                       "output_tokens": output_tokens, **stream_evidence(raw),
                       "stderr_present": bool(stderr.strip())}
            args.receipt_file.parent.mkdir(parents=True, exist_ok=True)
            args.receipt_file.write_text(json.dumps(receipt, indent=2) + "\n")
        record_usage({"provider": "gemini", "plugin": "gemini-toolkit", "operation": "gemini-worker",
                      "requested_model": args.model, "actual_model": actual, "status": status,
                      "duration_ms": round((time.monotonic() - started) * 1000),
                      "input_tokens": input_tokens, "output_tokens": output_tokens,
                      "event_id": str(uuid.uuid4())})


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, OSError, subprocess.TimeoutExpired) as error:
        print(f"Gemini worker stopped: {error}", file=sys.stderr)
        sys.exit(1)
