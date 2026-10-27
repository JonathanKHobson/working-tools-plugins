#!/usr/bin/env python3
"""Run reviewed offline installers once after a source journal changes.

This is an opt-in local maintenance boundary, not an AI worker or scheduler.
Provider adapters own conflict checks, native installation and rollback.
"""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import stat
import subprocess
import sys
import tempfile
import time


def digest(path):
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def read_json(path):
    with Path(path).open("rb") as stream:
        raw = stream.read(32 * 1024 * 1024 + 1)
    if len(raw) > 32 * 1024 * 1024:
        raise ValueError("Maintenance JSON exceeds the bounded reader limit.")
    result = json.loads(raw)
    if not isinstance(result, dict):
        raise ValueError("Maintenance JSON must be an object.")
    return result


def atomic_json(path, value):
    fd, temporary = tempfile.mkstemp(prefix="." + path.name, dir=path.parent)
    try:
        with os.fdopen(fd, "w") as stream:
            os.fchmod(stream.fileno(), 0o600)
            json.dump(value, stream, sort_keys=True, indent=2)
            stream.write("\n")
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def read_config(path):
    resolved = Path(path).resolve(strict=True)
    info = resolved.stat()
    if info.st_uid != os.getuid() or info.st_mode & 0o022:
        raise ValueError("Sync configuration must be user-owned and not group/world writable.")
    return read_json(resolved)


def validate(config):
    if config.get("schema_version") != 1 or not isinstance(config.get("adapters"), dict):
        raise ValueError("Unsupported provider sync configuration.")
    for raw in config.get("required_mounts", []):
        if not Path(raw).is_mount():
            raise ValueError("Required source/storage mount is unavailable: " + raw)
    state = Path(config["state_dir"]).resolve()
    storage = Path(config["storage_root"]).resolve()
    if not state.is_relative_to(storage) or state == storage:
        raise ValueError("Sync state must be inside its configured storage root.")
    allowed = {"claude": "sync_claude_native.py", "gemini": "sync_antigravity.py",
               "codex": "sync_codex_plugins.py"}
    for name, adapter in config["adapters"].items():
        if (not re.fullmatch(r"[a-z][a-z0-9_-]{0,63}", name)
                or not isinstance(adapter.get("owners"), list) or not adapter["owners"]):
            raise ValueError("Each offline adapter needs explicit source owners.")
        argv = adapter.get("argv")
        if (not isinstance(argv, list) or len(argv) < 3
                or not all(isinstance(a, str) and "\0" not in a for a in argv)
                or not Path(argv[0]).is_absolute()
                or not Path(argv[1]).is_absolute()
                or Path(argv[0]).resolve() != Path(sys.executable).resolve()
                or name not in allowed or Path(argv[1]).name != allowed[name]
                or len(argv) != 5 or argv[2] != "--config"
                or not Path(argv[3]).is_absolute() or argv[4] != "--apply"):
            raise ValueError("Only explicit reviewed Python offline adapters are accepted.")
        read_config(argv[3])
        reviewed = adapter.get("reviewed_files", {})
        if any(str(Path(p)) not in reviewed for p in (argv[1], argv[3])):
            raise ValueError("The offline adapter and its configuration need reviewed hashes.")
        for raw, expected in reviewed.items():
            if not Path(raw).is_absolute() or not Path(raw).is_file() or digest(raw) != expected:
                raise ValueError("Offline adapter changed; review required: " + raw)
        if not 1 <= adapter.get("timeout_seconds", 30) <= 21600:
            raise ValueError("Offline adapter timeout must be 1–21600 seconds.")
    return state


def plans(config, journal, state):
    products = journal.get("products")
    if not isinstance(products, dict):
        raise ValueError("Source journal has no product inventory.")
    result = {}
    for name, adapter in config["adapters"].items():
        selected = {}
        for owner in adapter["owners"]:
            if owner not in products:
                raise ValueError("Source owner unavailable in journal: " + owner)
            files = products[owner].get("files", {})
            selected[owner] = {p: v["sha256"] for p, v in files.items()}
        signature = hashlib.sha256(json.dumps(
            {"sources": selected, "adapter": adapter}, sort_keys=True).encode()).hexdigest()
        prior = state.get("adapters", {}).get(name, {})
        result[name] = {"signature": signature,
                        "dirty": prior.get("signature") != signature,
                        "held": prior.get("last_attempt_signature") == signature
                                and prior.get("last_exit_code", 0) != 0}
    return result


def run_adapter(argv, timeout, output):
    """No shell, provider inference CLI, polling, retry or permission override."""
    with output.open("w") as log:
        os.chmod(output, 0o600)
        environment = {k: v for k, v in os.environ.items()
                       if k not in ("PYTHONPATH", "PYTHONHOME", "PYTHONSTARTUP")}
        process = subprocess.Popen(argv, stdout=log, stderr=subprocess.STDOUT,
                                   start_new_session=True, env=environment)
        try:
            return process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
            return 124


def reconcile(config, mode="check", runner=run_adapter, lock_fd=None, retry_failed=False):
    folder = validate(config)
    # A check never creates a folder or lock or updates timestamps.
    state_path = folder / "state.json"
    state = read_json(state_path) if state_path.exists() else {"adapters": {}}
    journal = read_json(config["journal"])
    plan = plans(config, journal, state)
    if mode == "check":
        return {"status": "pending" if any(p["dirty"] and not p["held"] for p in plan.values())
                else "attention_required" if any(p["held"] for p in plan.values()) else "unchanged",
                "plan": plan, "provider_invocations": 0}
    if mode not in ("apply", "baseline"):
        raise ValueError("Unknown sync mode.")
    if not any(p["dirty"] and (not p["held"] or retry_failed) for p in plan.values()):
        return {"status": "attention_required" if any(p["held"] for p in plan.values())
                else "unchanged", "provider_invocations": 0}
    folder.mkdir(parents=True, exist_ok=True, mode=0o700)
    if lock_fd is not None:
        inherited = os.fstat(lock_fd)
        expected = (folder / "sync.lock").stat()
        if (not stat.S_ISREG(inherited.st_mode)
                or (inherited.st_dev, inherited.st_ino) != (expected.st_dev, expected.st_ino)):
            raise ValueError("Inherited maintenance lock is not the expected lock file.")
    with (os.fdopen(os.dup(lock_fd), "a") if lock_fd is not None
          else (folder / "sync.lock").open("a")) as lock:
        os.chmod(folder / "sync.lock", 0o600)
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return {"status": "busy", "provider_invocations": 0}
        state = read_json(state_path) if state_path.exists() else {"adapters": {}}
        journal = read_json(config["journal"])
        plan = plans(config, journal, state)
        results = {}
        invocations = 0
        for name, entry in plan.items():
            if not entry["dirty"] or (entry["held"] and not retry_failed):
                continue
            if mode == "baseline":
                code = 0
            else:
                adapter = config["adapters"][name]
                # Recheck pins immediately before calling any adapter.
                validate(config)
                try:
                    code = runner(adapter["argv"], adapter.get("timeout_seconds", 30),
                                  folder / (name + "-last-run.log"))
                except OSError:
                    code = 126
                invocations += 1
            results[name] = code
            prior = state.setdefault("adapters", {}).setdefault(name, {})
            prior.update(last_attempt_signature=entry["signature"], last_exit_code=code)
            if code == 0:
                prior.update(signature=entry["signature"], journal_revision=journal.get("revision"))
            atomic_json(state_path, state)
            # A failed adapter keeps its previous cursor; unrelated successful
            # providers remain correctly recorded, rather than claimed rolled back.
        held = [name for name, entry in plan.items() if entry["held"] and not retry_failed]
        result = {"status": "failed" if any(results.values())
                  else "attention_required" if held else "synchronized",
                  "adapters": results, "provider_invocations": invocations,
                  "held": held, "model_invocations": 0}
        atomic_json(folder / "last-result.json", result)
        return result


def enqueue(config_path):
    """Start at most one finite maintenance job, only when work is pending."""
    config = read_config(config_path)
    if not config.get("enabled", False):
        return {"status": "disabled"}
    plan = reconcile(config)
    if plan["status"] in ("unchanged", "attention_required"):
        return plan
    folder = validate(config)
    folder.mkdir(parents=True, exist_ok=True, mode=0o700)
    with (folder / "dispatch.lock").open("a") as dispatch:
        fcntl.flock(dispatch, fcntl.LOCK_EX | fcntl.LOCK_NB)
        # Nonblocking application lock check avoids launching a second worker.
        with (folder / "sync.lock").open("a") as lock:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                return {"status": "busy"}
            # Transfer this already-held lock to the child. No gap in ownership.
            with (folder / "last-dispatch.log").open("w") as output:
                os.chmod(folder / "last-dispatch.log", 0o600)
                process = subprocess.Popen([sys.executable, "-B", str(Path(__file__).resolve()),
                                            "--config", str(Path(config_path).resolve()), "--apply",
                                            "--inherited-lock-fd", str(lock.fileno())],
                                           stdin=subprocess.DEVNULL, stdout=output,
                                           stderr=subprocess.STDOUT, start_new_session=True,
                                           close_fds=True, pass_fds=(lock.fileno(),))
        atomic_json(folder / "owned-job.json", {"pid": process.pid, "started": time.time(),
                                                "command": "provider_sync --apply"})
        return {"status": "dispatched", "pid": process.pid}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--inherited-lock-fd", type=int, help=argparse.SUPPRESS)
    parser.add_argument("--retry-failed", action="store_true",
                        help="Explicitly retry a corrected failed adapter.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--apply", action="store_true")
    mode.add_argument("--baseline", action="store_true",
                      help="Record only after independent current installation verification.")
    args = parser.parse_args()
    try:
        result = reconcile(read_config(args.config),
                           "apply" if args.apply else "baseline" if args.baseline else "check",
                           lock_fd=args.inherited_lock_fd, retry_failed=args.retry_failed)
        print(json.dumps(result, sort_keys=True))
        return 1 if result["status"] in ("failed", "attention_required") else 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
