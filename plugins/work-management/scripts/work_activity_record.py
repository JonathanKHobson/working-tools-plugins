#!/usr/bin/env python3
"""Bounded, local workflow activity observation and capture.

This module is deliberately zero-model and zero-network.  Scans observe files
named by an explicit project-root/glob allowlist; ``record`` stores caller
declared workflow outcomes and hashes explicitly supplied evidence files.
Neither operation infers publication, receipt, or human acceptance.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import fnmatch
import hashlib
import json
import os
from pathlib import Path
import stat
import tempfile
import time
import uuid

class BusyError(RuntimeError):
    pass

SCHEMA = 1
STATUSES = {"proposed", "implemented", "tested", "published", "user_reported"}
MAX_TEXT = 4000
MAX_EVIDENCE_REFS = 40
SKIP_PARTS = {".git", "node_modules", ".venv", "venv", "__pycache__",
              ".pytest_cache", ".mypy_cache", "build", "dist", "backup", "backups",
              ".backup", ".backups", "vendor", "third_party"}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _parse_time(value: str) -> datetime:
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    parsed = datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        raise ValueError("timestamps must include a timezone")
    return parsed.astimezone(timezone.utc)


def _atomic(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=f".{path.name}-", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            os.fchmod(stream.fileno(), 0o600)
            json.dump(value, stream, indent=2, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def _load(path: Path) -> dict | None:
    if not path.exists():
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        if (not isinstance(value, dict) or value.get("schema_version") != SCHEMA
                or not isinstance(value.get("files"), dict)
                or not isinstance(value.get("activities"), list)):
            raise ValueError("invalid activity journal")
        return value
    except (OSError, UnicodeError, json.JSONDecodeError, TypeError, ValueError) as exc:
        raise ValueError("Activity journal is corrupt; original bytes preserved") from exc


def _config(config: dict) -> tuple[Path, list[dict], int, int]:
    if not isinstance(config, dict) or not config.get("state_dir"):
        raise ValueError("state_dir is required")
    roots = config.get("project_roots", [])
    if not isinstance(roots, list):
        raise ValueError("project_roots must be a list")
    checked = []
    for item in roots:
        if not isinstance(item, dict) or not isinstance(item.get("root"), str):
            raise ValueError("each project root requires root")
        globs = item.get("globs", item.get("allowlist", []))
        if isinstance(globs, str):
            globs = [globs]
        if not isinstance(globs, list) or not globs or any(not isinstance(x, str) or not x for x in globs):
            raise ValueError("each project root requires a nonempty glob allowlist")
        root = Path(item["root"]).expanduser()
        if root.is_symlink():
            raise ValueError("project roots may not be symlinks")
        checked.append({"name": str(item.get("name") or root.name),
                        "root": root, "globs": globs,
                        "max_depth": int(item.get("max_depth", config.get("max_depth", 12)))})
    max_files = int(config.get("max_files", 500))
    max_bytes = int(config.get("max_bytes", 5 * 1024 * 1024))
    if max_files < 1 or max_bytes < 1:
        raise ValueError("limits must be positive")
    return Path(config["state_dir"]).expanduser(), checked, max_files, max_bytes


def _excluded(relative: str) -> bool:
    return any(part in SKIP_PARTS or part.startswith(".") and part in {".git"}
               for part in Path(relative).parts)


def _allowed(relative: str, globs: list[str]) -> bool:
    return any(fnmatch.fnmatch(relative, pattern) or Path(relative).match(pattern)
               for pattern in globs)


def _hash(path: Path, max_bytes: int) -> tuple[str, int, int]:
    digest = hashlib.sha256()
    total = 0
    before = path.lstat()
    if not stat.S_ISREG(before.st_mode):
        raise OSError("not a regular file")
    with path.open("rb") as stream:
        opened = os.fstat(stream.fileno())
        if (opened.st_dev, opened.st_ino) != (before.st_dev, before.st_ino):
            raise OSError("file replaced during scan")
        while True:
            chunk = stream.read(min(1024 * 1024, max_bytes - total + 1))
            if not chunk:
                break
            total += len(chunk)
            if total > max_bytes:
                raise ValueError("file exceeds max_bytes")
            digest.update(chunk)
        after = os.fstat(stream.fileno())
    if ((before.st_size, before.st_mtime_ns, before.st_ctime_ns) !=
            (after.st_size, after.st_mtime_ns, after.st_ctime_ns)):
        raise OSError("file changed during scan")
    return digest.hexdigest(), total, before.st_mtime_ns


def _files(roots: list[dict], max_files: int, max_bytes: int) -> tuple[dict, set[str]]:
    found, unavailable = {}, set()
    count = 0
    byte_total = 0
    for item in roots:
        root = item["root"]
        if not root.is_dir():
            unavailable.add(item["name"])
            continue
        local = {}
        errors = False
        def walk_error(_exc):
            nonlocal errors
            errors = True
        prefixes = {pattern.split("*", 1)[0].rstrip("/") for pattern in item["globs"]
                    if "*" in pattern}
        for directory, dirs, names in os.walk(root, followlinks=False, onerror=walk_error):
            base = Path(directory)
            relative_dir = base.relative_to(root).as_posix() if base != root else ""
            if len(Path(relative_dir).parts) > item["max_depth"]:
                dirs[:] = []
                continue
            dirs[:] = sorted(d for d in dirs if d not in SKIP_PARTS and not (base / d).is_symlink()
                             and (not prefixes or any((relative_dir + "/" + d).strip("/").startswith(prefix)
                                                       or prefix.startswith((relative_dir + "/" + d).strip("/"))
                                                       for prefix in prefixes)))
            for name in sorted(names):
                path = base / name
                if path.is_symlink():
                    continue
                relative = path.relative_to(root).as_posix()
                if _excluded(relative) or not _allowed(relative, item["globs"]):
                    continue
                count += 1
                if count > max_files:
                    raise ValueError("max_files exceeded")
                try:
                    remaining = max_bytes - byte_total
                    if remaining <= 0:
                        raise ValueError("max_bytes exceeded")
                    digest, size, mtime_ns = _hash(path, remaining)
                except (OSError, ValueError):
                    errors = True
                    continue
                byte_total += size
                key = f"{item['name']}:{relative}"
                local[key] = {"project": item["name"], "path": relative,
                              "sha256": digest, "size": size, "source_mtime": mtime_ns}
        if errors:
            unavailable.add(item["name"])
        else:
            found.update(local)
    return found, unavailable


@contextmanager
def _with_lock(state: Path):
    state.mkdir(parents=True, exist_ok=True)
    lock = (state / "activity.lock").open("a")
    os.fchmod(lock.fileno(), 0o600)
    try:
        deadline = time.monotonic() + 0.5
        while True:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                if time.monotonic() >= deadline:
                    raise BusyError("activity journal busy")
                time.sleep(0.025)
        yield lock
    finally:
        lock.close()


def scan(config: dict) -> dict:
    state, roots, max_files, max_bytes = _config(config)
    journal_path = state / "activity.json"
    with _with_lock(state):
        previous = _load(journal_path)
        current, unavailable = _files(roots, max_files, max_bytes)
        now = _now()
        document = previous or {"schema_version": SCHEMA, "initialized_at": now,
                                "observed_at": now, "files": {}, "activities": [],
                                "last_unavailable": []}
        old = document["files"]
        prior_gap = document.get("last_unavailable")
        events = [] if previous is None else document["activities"]
        changed = 0
        if previous is not None:
            for key in sorted(set(old) | set(current)):
                before, after = old.get(key), current.get(key)
                if before and after and before.get("sha256") == after.get("sha256"):
                    continue
                if key.split(":", 1)[0] in unavailable:
                    continue
                row = after or before
                events.append({"id": uuid.uuid4().hex, "type": "file_observation",
                               "project": row["project"], "path": row["path"],
                               "hash": after.get("sha256") if after else None,
                               "observed_at": now,
                               "source_mtime": after.get("source_mtime") if after else before.get("source_mtime"),
                               "status": "changed_unverified"})
                changed += 1
        available_names = {item["name"] for item in roots} - unavailable
        next_files = dict(old)
        for key in list(next_files):
            if key.split(":", 1)[0] in available_names and key not in current:
                del next_files[key]
        next_files.update(current)
        document["files"] = next_files
        document["last_unavailable"] = sorted(unavailable)
        prior_scan_at = document.get("last_scan_at")
        document["last_scan_at"] = now
        state_changed = (previous is None or next_files != old or prior_gap != sorted(unavailable)
                         or prior_scan_at != now)
        if state_changed:
            document["observed_at"] = now
            _atomic(journal_path, document)
        return {"status": "recorded" if previous is None else "changed" if changed else "unchanged",
                "changed": changed, "unavailable": sorted(unavailable)}


def _evidence(path: Path, max_bytes: int) -> dict:
    path = path.expanduser()
    if not path.is_absolute():
        path = Path.cwd() / path
    current = path
    while current != current.parent:
        if current.is_symlink() and not os.path.realpath(current).startswith("/private/"):
            raise ValueError(f"evidence path traverses symlink: {path}")
        current = current.parent
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"evidence file unavailable: {path}")
    digest, size, mtime_ns = _hash(path, max_bytes)
    return {"path": str(path), "sha256": digest, "size": size, "source_mtime": mtime_ns}


def record(config: dict, payload: dict) -> dict:
    state, _, _, max_bytes = _config(config)
    if not isinstance(payload, dict) or not all(isinstance(payload.get(k), str) and payload[k]
                                                for k in ("workflow", "method", "outcome")):
        raise ValueError("workflow, method, and outcome are required")
    if any(len(payload[key]) > MAX_TEXT for key in ("workflow", "method", "outcome")):
        raise ValueError("workflow, method, and outcome are too long")
    status = payload.get("status")
    if status not in STATUSES:
        raise ValueError("invalid status")
    refs = payload.get("evidence_refs", [])
    if not isinstance(refs, list) or any(not isinstance(ref, str) or not ref for ref in refs):
        raise ValueError("evidence_refs must be a list of paths")
    if len(refs) > MAX_EVIDENCE_REFS:
        raise ValueError("too many evidence_refs")
    if status in {"implemented", "tested", "published"} and not refs:
        raise ValueError("evidence_refs are required for this status")
    occurrence_at = payload.get("occurrence_at")
    if occurrence_at is not None:
        _parse_time(occurrence_at)
    evidence = [_evidence(Path(ref).expanduser(), max_bytes) for ref in refs]
    identity = hashlib.sha256(json.dumps({"workflow": payload["workflow"], "method": payload["method"],
                                          "outcome": payload["outcome"], "status": status,
                                          "evidence": [{"path": x["path"], "sha256": x["sha256"]}
                                                       for x in evidence]}, sort_keys=True).encode()).hexdigest()
    with _with_lock(state):
        path = state / "activity.json"
        document = _load(path) or {"schema_version": SCHEMA, "initialized_at": _now(),
                                   "observed_at": _now(), "files": {}, "activities": [],
                                   "last_unavailable": []}
        if any(item.get("identity") == identity for item in document["activities"]):
            return {"status": "duplicate", "identity": identity}
        row = {"id": uuid.uuid4().hex, "type": "workflow_record", "identity": identity,
               "workflow": payload["workflow"], "method": payload["method"],
               "outcome": payload["outcome"], "status": status,
               "status_source": "caller_declared", "human_accepted": False,
               "evidence": evidence, "observed_at": _now()}
        if occurrence_at is not None:
            row["occurrence_at"] = occurrence_at
        document["activities"].append(row)
        _atomic(path, document)
        return {"status": "recorded", "identity": identity}


def query(config: dict, since: str | None = None, until: str | None = None) -> dict:
    state, _, _, _ = _config(config)
    low, high = (_parse_time(since) if since else None), (_parse_time(until) if until else None)
    if low is not None and high is not None and low > high:
        raise ValueError("since must be before or equal to until")
    path = state / "activity.json"
    document = _load(path) or {"activities": [], "initialized_at": None,
                               "observed_at": None, "last_unavailable": []}
    def in_range(row):
        at = _parse_time(row.get("observed_at", row.get("at", "")))
        return (low is None or at >= low) and (high is None or at <= high)
    activities = [row for row in document["activities"] if in_range(row)]
    plugin_rows, limitations = [], ["baseline scan records observed facts only; it does not infer completion"]
    plugin_path = config.get("plugin_journal") or config.get("plugin_change_journal")
    if not plugin_path and config.get("plugin_change_config"):
        try:
            plugin_config = json.loads(Path(config["plugin_change_config"]).expanduser().read_text(encoding="utf-8"))
            if plugin_config.get("state_dir"):
                plugin_path = str(Path(plugin_config["state_dir"]).expanduser() / "journal.json")
        except (OSError, UnicodeError, json.JSONDecodeError, TypeError):
            limitations.append("configured plugin journal unavailable or corrupt")
    if plugin_path:
        try:
            source = json.loads(Path(plugin_path).expanduser().read_text(encoding="utf-8"))
            for event in source.get("events", []):
                at = _parse_time(event["at"])
                if (low is None or at >= low) and (high is None or at <= high):
                    plugin_rows.append({"type": "plugin_source_changed", "status": "changed_unverified",
                                        "observed_at": event["at"], "source": str(plugin_path),
                                        "event_id": event.get("id"), "origin": event.get("origin"),
                                        "plugins": sorted({change.get("plugin", "unknown") for change in event.get("changes", [])}),
                                        "changed_paths": [{"plugin": change.get("plugin"), "path": change.get("path"), "operation": change.get("operation")} for change in event.get("changes", [])[:100]],
                                        "paths_truncated": len(event.get("changes", [])) > 100,
                                        "change_count": len(event.get("changes", []))})
        except (OSError, UnicodeError, json.JSONDecodeError, KeyError, ValueError):
            limitations.append("configured plugin journal unavailable or corrupt")
    return {"activities": activities, "plugin_events": plugin_rows,
            "baseline": {"initialized_at": document.get("initialized_at"),
                         "observed_at": document.get("observed_at"),
                         "last_scan_at": document.get("last_scan_at")},
            "observation_gaps": document.get("last_unavailable", []),
            "limitations": limitations}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    scan_parser = sub.add_parser("scan"); scan_parser.add_argument("--config", type=Path, required=True)
    rec_parser = sub.add_parser("record"); rec_parser.add_argument("--config", type=Path, required=True); rec_parser.add_argument("--input", type=Path, required=True)
    query_parser = sub.add_parser("query"); query_parser.add_argument("--config", type=Path, required=True); query_parser.add_argument("--since"); query_parser.add_argument("--until")
    args = parser.parse_args()
    config = json.loads(args.config.expanduser().read_text(encoding="utf-8"))
    if args.command == "scan": result = scan(config)
    elif args.command == "record": result = record(config, json.loads(args.input.expanduser().read_text(encoding="utf-8")))
    else: result = query(config, args.since, args.until)
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
