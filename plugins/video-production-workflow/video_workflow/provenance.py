from __future__ import annotations

import hashlib
import json
import mimetypes
import re
import stat
from collections.abc import Mapping
from pathlib import Path, PurePosixPath
from typing import Any, Iterable


def hash_file(path: str | Path, *, algorithm: str = "sha256", chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.new(algorithm)
    with Path(path).open("rb") as handle:
        while chunk := handle.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def inventory_paths(paths: Iterable[str | Path], *, recursive: bool = True) -> list[dict[str, Any]]:
    files: list[Path] = []
    for raw in paths:
        path = Path(raw).expanduser().resolve()
        if path.is_dir():
            iterator = path.rglob("*") if recursive else path.glob("*")
            files.extend(p for p in iterator if p.is_file())
        elif path.is_file():
            files.append(path)
    unique = sorted(set(files))
    return [
        {
            "name": path.name,
            "path": str(path),
            "bytes": path.stat().st_size,
            "modified_ns": path.stat().st_mtime_ns,
            "mime": mimetypes.guess_type(path.name)[0],
            "sha256": hash_file(path),
        }
        for path in unique
    ]


def cache_key(settings: Any, *, files: Iterable[str | Path] = (), namespace: str = "video-workflow-v1") -> str:
    digest = hashlib.sha256()
    digest.update(namespace.encode("utf-8"))
    digest.update(json.dumps(settings, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8"))
    for raw in sorted((Path(p).expanduser().resolve() for p in files), key=str):
        digest.update(str(raw).encode("utf-8"))
        digest.update(hash_file(raw).encode("ascii"))
    return digest.hexdigest()


def _portable_inventory_path(name: Any) -> str | None:
    if not isinstance(name, str) or not name or "\\" in name or "\0" in name:
        return None
    path = PurePosixPath(name)
    if path.is_absolute() or ".." in path.parts or re.match(r"^[A-Za-z]:", name):
        return None
    return path.as_posix() if path.parts else None


def _file_state(path: Path, root: Path) -> tuple[Any, ...]:
    resolved = path.resolve()
    resolved.relative_to(root)
    info = path.stat()
    return (
        resolved, info.st_dev, info.st_ino, info.st_mode, info.st_size,
        info.st_mtime_ns, info.st_ctime_ns,
    )


def _has_exact_spelling(root: Path, key: str) -> bool:
    """Do not let a case-insensitive host conceal nonportable path spelling."""
    parent = root
    for component in PurePosixPath(key).parts:
        if not any(child.name == component for child in parent.iterdir()):
            return False
        parent = parent / component
    return True


def verify_relative_inventory(
    root: str | Path, entries: Iterable[dict[str, Any]], *, required_paths: Iterable[str] = ()
) -> dict[str, Any]:
    """Check local declared files and required-entry coverage without modifying them.

    Metadata is checked around each hash and again after all reads to detect
    ordinary concurrent edits. This is not a locked snapshot or protection from
    hostile replacement, and does not infer undeclared runtime dependencies.
    """
    issues: list[dict[str, Any]] = []
    verified: list[str] = []
    seen: set[str] = set()
    states: list[tuple[str, Path, tuple[Any, ...]]] = []

    def issue(code: str, name: Any = None) -> None:
        # Malformed values must remain JSON serializable in CLI reports.
        issues.append({"code": code, "path": name if isinstance(name, str) else None})

    def report(count: int) -> dict[str, Any]:
        return {
            "passed": not issues,
            "declaredFileCount": count,
            "verifiedFiles": verified,
            "issues": issues,
            "scope": (
                "Local declared file identity and required-entry coverage only; "
                "metadata rechecks detect ordinary edits but provide no locked snapshot "
                "or hostile-replacement guarantee. No rendering, dependency inference, "
                "creative approval or listening."
            ),
        }

    try:
        if isinstance(entries, (str, bytes, Mapping)):
            raise TypeError
        records = list(entries)
    except TypeError:
        issue("invalid-inventory")
        return report(0)
    try:
        root = Path(root).expanduser().resolve()
        if not root.is_dir():
            issue("invalid-root")
            return report(len(records))
    except (OSError, RuntimeError, ValueError, TypeError):
        issue("invalid-root")
        return report(len(records))

    for record in records:
        name = record.get("path") if isinstance(record, dict) else None
        key = _portable_inventory_path(name)
        if key is None:
            issue("unsafe-path", name)
            continue
        path = root / key
        try:
            path.resolve().relative_to(root)
        except (ValueError, RuntimeError):
            issue("unsafe-path", name)
            continue
        except OSError:
            issue("io-error", name)
            continue
        if key in seen:
            issue("duplicate-entry", name)
            continue
        seen.add(key)
        expected = record.get("sha256")
        if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", expected):
            issue("invalid-sha256", name)
            continue
        size = record.get("bytes")
        if "bytes" in record and (type(size) is not int or size < 0):
            issue("invalid-bytes", name)
            continue
        try:
            before = _file_state(path, root)
            if not stat.S_ISREG(before[3]):
                issue("missing-file", name)
                continue
            if not _has_exact_spelling(root, key):
                issue("case-mismatch", name)
                continue
            if "bytes" in record and size != before[4]:
                issue("size-mismatch", name)
            actual = hash_file(path)
            after = _file_state(path, root)
        except FileNotFoundError:
            issue("missing-file", name)
            continue
        except (ValueError, RuntimeError):
            issue("unsafe-path", name)
            continue
        except OSError:
            issue("io-error", name)
            continue
        states.append((name, path, after))
        if before != after:
            issue("changed-during-read", name)
        elif actual.lower() != expected.lower():
            issue("hash-mismatch", name)
        elif not any(item["path"] == name for item in issues):
            verified.append(name)

    # An earlier entry may change while a later entry is being hashed.
    for name, path, previous in states:
        try:
            changed = _file_state(path, root) != previous
        except (OSError, ValueError, RuntimeError):
            changed = True
        if changed:
            issue("changed-during-verification", name)
            if name in verified:
                verified.remove(name)

    try:
        if isinstance(required_paths, (str, bytes, Mapping)):
            raise TypeError
        required = list(required_paths)
    except TypeError:
        issue("invalid-required-paths")
        required = []
    for name in required:
        key = _portable_inventory_path(name)
        if key is None:
            issue("unsafe-required-path", name)
        elif key not in seen:
            issue("required-entry-missing", name)
    if not records:
        issue("empty-inventory")
    return report(len(records))
