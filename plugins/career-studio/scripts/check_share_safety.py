#!/usr/bin/env python3
"""Find common accidental personal-data inclusions without printing their values."""
from pathlib import Path
import argparse
import json
import re

RULES = {
    "machine_private_path": re.compile(r"/(?:Users/[A-Za-z0-9_.-]+/|Volumes/[^\s`\"<>]+)"),
    "email": re.compile(r"[A-Z0-9._%+-]+@([A-Z0-9.-]+\.[A-Z]{2,})", re.I),
    "auth_material": re.compile(r"(?:Bearer\s+[A-Za-z0-9._~-]{20,}|(?:sk|ghp|github_pat)-?[A-Za-z0-9_]{24,})"),
}
PRIVATE_NAMES = {"candidate-facts.json", "preferences.json", "submissions.json", "workspace.json", ".env"}

def scan(root):
    findings = []
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        if path.is_symlink():
            findings.append({"path": rel, "rule": "symlink_requires_review"})
            continue
        if not path.is_file() or path.resolve() == Path(__file__).resolve():
            continue
        if path.name in PRIVATE_NAMES or path.name.startswith(".env."):
            findings.append({"path": rel, "rule": "private_record_name"})
        if path.suffix.lower() not in {".md", ".txt", ".json", ".yaml", ".yml", ".py", ".js", ".html", ".toml"}:
            findings.append({"path": rel, "rule": "nontext_requires_review"})
            continue
        for number, line in enumerate(path.read_text(errors="replace").splitlines(), 1):
            for name, pattern in RULES.items():
                hits = list(pattern.finditer(line))
                if name == "email":
                    hits = [m for m in hits if m.group(1).lower() not in {"example.com", "example.org", "example.net", "example.test"}]
                if hits:
                    findings.append({"path": rel, "line": number, "rule": name})
    return findings

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    if not args.root.is_dir():
        parser.error("root must be an existing staged plugin directory")
    findings = scan(args.root.resolve())
    print(json.dumps({"findings": findings, "scope": "heuristic content scan; manual artifact review still required"}, indent=2))
    raise SystemExit(1 if findings else 0)
