#!/usr/bin/env python3
"""
Scan for large source files that may be monolith candidates.

Usage:
  python scripts/audit_monoliths.py --root .
"""
from __future__ import annotations

import argparse
from pathlib import Path

SOURCE_EXTS = {
    ".js", ".jsx", ".ts", ".tsx", ".py", ".cs", ".cpp", ".h", ".hpp",
    ".gd", ".java", ".kt", ".swift", ".go", ".rs", ".php", ".rb",
    ".html", ".css", ".scss", ".sql"
}

IGNORE_DIRS = {
    "node_modules", "dist", "build", ".git", ".next", ".nuxt", ".cache",
    "coverage", "Library", "Temp", "Obj", "Binaries", "DerivedDataCache",
    "Intermediate", "Saved", "__pycache__", ".venv"
}

def line_count(path: Path) -> int:
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as f:
            return sum(1 for _ in f)
    except OSError:
        return 0

def should_skip(path: Path) -> bool:
    return any(part in IGNORE_DIRS for part in path.parts)

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--warn", type=int, default=500)
    parser.add_argument("--high", type=int, default=1500)
    args = parser.parse_args()

    root = Path(args.root)
    results = []
    for path in root.rglob("*"):
        if should_skip(path):
            continue
        if path.is_file() and path.suffix.lower() in SOURCE_EXTS:
            count = line_count(path)
            if count >= args.warn:
                severity = "HIGH" if count >= args.high else "WARN"
                results.append((count, severity, path))

    for count, severity, path in sorted(results, reverse=True):
        print(f"{severity:4} {count:6} lines  {path}")

    if not results:
        print("No large source files found.")

if __name__ == "__main__":
    main()
