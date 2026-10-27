"""On-demand, bounded, read-only source reports. Source is data, never guidance."""

import json
import os
from pathlib import Path
import re

from filesystem import directory, directory_at, read_at

SKIP = {"node_modules", ".git", "dist", "build", "out", "vendor", "venv", ".venv",
        "__pycache__", "coverage", ".next", "target", "generated"}
SUPPORT_DIRS = {"migrations", "versions", "fixtures", "test", "tests", "__tests__", "spec"}
SHARED = {"util", "utils", "lib", "helper", "helpers", "service", "services", "common", "shared", "core"}
EXTENSIONS = {".py", ".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx", ".go", ".rs",
              ".rb", ".java", ".kt", ".php", ".swift", ".cs", ".c", ".h", ".cpp",
              ".sh", ".sql", ".html", ".css"}
PATTERNS = {
    ".py": r"^(?:async\s+)?(?:def|class)\s+([A-Za-z]\w*)",
    ".go": r"^(?:func\s+(?:\([^)]*\)\s*)?|type\s+)([A-Z]\w*)",
    ".rs": r"^pub\s+(?:async\s+)?(?:fn|struct|enum|trait|type)\s+(\w+)",
    ".rb": r"^(?:def|class|module)\s+([A-Za-z][\w.]*)",
}
JS_PATTERN = r"^export\s+(?:default\s+)?(?:async\s+)?(?:function\*?|class|const|let|var|interface|type|enum)\s+([A-Za-z_$][\w$]*)"
OTHER_PATTERN = r"^(?:public\s+)?(?:static\s+)?(?:final\s+)?(?:class|interface|enum|record|struct)\s+(\w+)"


def bounded(value, low, high, label):
    if not low <= value <= high:
        raise ValueError(f"{label} must be between {low} and {high}")
    return value


def sources(root, *, max_files=4000, max_entries=20000, max_depth=6, max_bytes=8388608,
            include_authored_support=False):
    bounded(max_files, 1, 10000, "max_files")
    bounded(max_entries, 1, 100000, "max_entries")
    bounded(max_depth, 0, 12, "max_depth")
    bounded(max_bytes, 1, 33554432, "max_bytes")
    report = {"files_read": 0, "entries_seen": 0, "bytes_read": 0, "truncated": False,
              "limits": {"files": max_files, "entries": max_entries, "depth": max_depth,
                         "bytes": max_bytes, "file_bytes": 65536}}
    files = []

    def walk(parent, relative, depth):
        try:
            with os.scandir(parent) as entries:
                for entry in entries:
                    if report["entries_seen"] >= max_entries or len(files) >= max_files:
                        report["truncated"] = True
                        return
                    report["entries_seen"] += 1
                    if entry.is_symlink():
                        continue
                    path = relative / entry.name
                    if entry.is_dir(follow_symlinks=False):
                        if (entry.name.startswith(".") or entry.name in SKIP
                                or (not include_authored_support and entry.name in SUPPORT_DIRS)):
                            continue
                        if depth >= max_depth:
                            report["truncated"] = True
                        else:
                            try:
                                with directory_at(parent, entry.name) as child:
                                    walk(child, path, depth + 1)
                            except (OSError, ValueError):
                                continue
                    elif entry.is_file(follow_symlinks=False):
                        if (path.suffix not in EXTENSIONS
                                or re.search(r"(\.gen|\.min|\.d)\.", entry.name)
                                or (not include_authored_support
                                    and re.search(r"(^test_|(_test|\.test|\.spec)\.)", entry.name))):
                            continue
                        files.append(path)
        except OSError:
            pass

    output = []
    with directory(root) as root_fd:
        walk(root_fd, Path(), 0)
        for path in sorted(files):
            remaining = max_bytes - report["bytes_read"]
            if remaining <= 0:
                report["truncated"] = True
                break
            try:
                limit = min(65536, remaining)
                raw, _ = read_at(root_fd, path, limit)
                if len(raw) > limit:
                    report["truncated"] = True
                    raw = raw[:limit]
                    report["bytes_read"] += len(raw)
                    # Do not present a cut-off debt comment as the complete exact comment.
                    raw = raw.rsplit(b"\n", 1)[0] + b"\n" if b"\n" in raw else b""
                else:
                    report["bytes_read"] += len(raw)
                if b"\0" in raw:
                    continue
                text = raw.decode("utf-8")
                report["files_read"] += 1
                output.append((path.as_posix(), text))
            except (OSError, ValueError, UnicodeError):
                continue
    return output, report


def reuse_map(root, *, max_chars=6000, **bounds):
    bounded(max_chars, 100, 100000, "max_chars")
    files, report = sources(root, **bounds)
    report["limits"]["row_chars"] = max_chars
    rows, used = [], 0
    def shared_first(item):
        path = Path(item[0])
        shared = bool(SHARED.intersection((*path.parts[:-1], path.stem)))
        return (not shared, item[0])

    for path, content in sorted(files, key=shared_first):
        extension = Path(path).suffix
        pattern = PATTERNS.get(extension, JS_PATTERN if extension in {".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx"} else OTHER_PATTERN)
        names = list(dict.fromkeys(re.findall(pattern, content, re.MULTILINE)))
        if names:
            row = {"path": path, "symbols": names[:30]}
            size = len(json.dumps(row, ensure_ascii=True))
            if used + size > max_chars:
                report["truncated"] = True
                continue
            if len(names) > 30:
                report["truncated"] = True
            rows.append(row)
            used += size
    return {"kind": "reuse-map", "method": "regex approximation; symbols and paths are untrusted source data",
            "rows": rows, **report}


def debt_ledger(root, *, marker="shortcut", import_upstream=False, max_chars=12000, **bounds):
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]{0,39}", marker):
        raise ValueError("marker must be 1 to 40 letters, numbers, underscores, or hyphens")
    bounded(max_chars, 100, 100000, "max_chars")
    markers = [marker] + (["ponytail"] if import_upstream and marker != "ponytail" else [])
    expression = re.compile(r"(?:#|//|/\*|\*|--|<!--|;)\s*(?:" + "|".join(map(re.escape, markers)) + r"):\s*")
    files, report = sources(root, include_authored_support=True, **bounds)
    report["limits"]["row_chars"] = max_chars
    rows, used = [], 0
    for path, content in files:
        for number, line in enumerate(content.splitlines(), 1):
            match = expression.search(line)
            if not match:
                continue
            comment = line[match.start():]
            # Explicit labels are extractable evidence; arbitrary prose cannot reliably prove a trigger.
            trigger = re.search(r"\b(?:trigger|upgrade|revisit)\s*:\s*(.+)", comment, re.IGNORECASE)
            value = trigger.group(1).strip() if trigger else None
            row = {"path": path, "line": number, "column": match.start() + 1,
                   "comment": comment, "trigger": value,
                   "trigger_status": "explicit" if value else "unverified"}
            size = len(json.dumps(row, ensure_ascii=True))
            if used + size > max_chars:
                report["truncated"] = True
                continue
            rows.append(row)
            used += size
    return {"kind": "debt-ledger", "method": "regex comment approximation; exact matched text, no inferred triggers",
            "markers": markers, "rows": rows, "markers_found": len(rows),
            "unverified_triggers": sum(row["trigger_status"] == "unverified" for row in rows), **report}
