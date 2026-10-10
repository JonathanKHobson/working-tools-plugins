#!/usr/bin/env python3
"""Original, read-only local publication privacy preflight (Python 3.10+)."""

from __future__ import annotations

import argparse
from array import array
import base64
from bisect import bisect_right
import binascii
import hashlib
import html
import json
import os
from pathlib import Path
import re
import stat
import sys

VERSION = "1.0.0"
EXTENSIONS = {".html", ".htm", ".css", ".js", ".mjs", ".cjs", ".json", ".md", ".txt"}
EXCLUDED_DIRS = {".git", ".obsidian", "vault", "vaults", "node_modules"}
MAX_FILES, MAX_BYTES, MAX_TOTAL_BYTES, MAX_ENTRIES, MAX_FINDINGS = 1000, 1_000_000, 20_000_000, 10000, 2000

# Deliberately bounded heuristics. No sample values, excerpts or target names appear
# in output. A recognizable secret format is stronger evidence than a prose hint.
RULES = [
    ("secret.private-key", "block", re.compile(r"-----BEGIN (?:(?:RSA |EC |DSA |OPENSSH |ENCRYPTED )?PRIVATE KEY|PGP PRIVATE KEY BLOCK)-----")),
    ("secret.aws-access-key", "block", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    ("secret.github-token", "block", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{36,255}|github_pat_[A-Za-z0-9_]{40,255})\b")),
    ("secret.openai-key", "block", re.compile(r"\bsk-(?!ant-)(?:proj-|svcacct-)?[A-Za-z0-9_-]{32,255}\b")),
    ("secret.anthropic-key", "block", re.compile(r"\bsk-ant-[A-Za-z0-9_-]{20,255}\b")),
    ("secret.stripe-live-key", "block", re.compile(r"\b(?:sk|rk)_live_[A-Za-z0-9]{16,255}\b")),
    ("secret.slack-token", "block", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,255}\b")),
    ("secret.google-legacy-api-key", "block", re.compile(r"\bAIza[A-Za-z0-9_-]{35}\b")),
    ("secret.npm-token", "block", re.compile(r"\bnpm_[A-Za-z0-9]{36}\b")),
    ("secret.sendgrid-key", "block", re.compile(r"\bSG\.[A-Za-z0-9_-]{16,128}\.[A-Za-z0-9_-]{16,128}\b")),
    ("privacy.email", "review", re.compile(r"\b[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]{1,64}@[A-Za-z0-9.-]{1,190}\.[A-Za-z]{2,24}\b")),
    ("privacy.local-user-path", "review", re.compile(r"(?:/" r"Users/|/home/|[A-Za-z]:\\Users\\)[^\s<>\"']{1,180}")),
    ("privacy.phone", "review", re.compile(r"(?<!\d)(?:\+1[ .-]?)?(?:\(\d{3}\)|\d{3})[ .-]\d{3}[ .-]\d{4}(?!\d)")),
    ("privacy.credential-assignment", "review", re.compile(r"\b(?:api[_-]?key|access[_-]?token|auth[_-]?token|password|passwd|secret|client[_-]?secret|authorization|bearer)\s*[\"']?\s*[:=]\s*[\"']?[^\s\"'<>;,}]{8,255}", re.I)),
    ("privacy.url-credentials", "review", re.compile(r"\b[a-z][a-z0-9+.-]{0,24}://[^\s:@/\"'<>]{1,64}:[^\s@/\"'<>]{1,128}@[^\s/\"'<>]{1,128}", re.I)),
    ("privacy.jwt-shape", "review", re.compile(r"\beyJ[A-Za-z0-9_-]{10,1024}\.[A-Za-z0-9_-]{10,2048}\.[A-Za-z0-9_-]{10,1024}\b")),
    ("privacy.confidential-marker", "review", re.compile(r"\b(?:confidential|internal[ -]only|do[ -]not[ -]publish|social[ -]security)\b", re.I)),
]
ENTITY = re.compile(r"&(?:#[xX][0-9a-fA-F]{1,8}|#\d{1,10}|[A-Za-z][A-Za-z0-9]{1,31});?")
BASE64 = re.compile(r"(?<![A-Za-z0-9+/])[A-Za-z0-9+/]{40,4096}={0,2}(?![A-Za-z0-9+/=])")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def decoded_entities(text: str, mapping: array) -> tuple[str, array]:
    """Map decoded characters to the source offset, keeping physical line evidence."""
    chunks, offsets, cursor = [], array("I"), 0
    for match in ENTITY.finditer(text):
        chunks.append(text[cursor:match.start()])
        offsets.extend(mapping[cursor:match.start()])
        value = html.unescape(match.group())
        chunks.append(value)
        offsets.extend([mapping[match.start()]] * len(value))
        cursor = match.end()
    chunks.append(text[cursor:])
    offsets.extend(mapping[cursor:])
    return "".join(chunks), offsets


def text_findings(text: str, file_hash: str, path_id: str) -> list[dict]:
    findings, seen = [], set()
    views = [("raw", text, array("I", range(len(text))))]
    newlines = [index for index, char in enumerate(text) if char == "\n"]
    value, mapping = views[0][1:]
    for round_number in range(1, 4):
        decoded, decoded_map = decoded_entities(value, mapping)
        if decoded == value:
            break
        views.append((f"html-entities-{round_number}", decoded, decoded_map))
        value, mapping = decoded, decoded_map

    def add(rule: str, tier: str, offset: int, view: str) -> None:
        key = (rule, offset)
        if key in seen:
            return
        seen.add(key)
        fingerprint = digest(f"{VERSION}:{rule}:{file_hash}:{offset}".encode())
        findings.append({"rule": rule, "tier": tier, "path_id": path_id,
                         "file_sha256": file_hash, "line": bisect_right(newlines, offset) + 1,
                         "source_character_offset": offset, "view": view,
                         "fingerprint": fingerprint})

    for view, value, mapping in views:
        for rule, tier, pattern in RULES:
            for match in pattern.finditer(value):
                add(rule, tier, mapping[match.start()], view)
                if len(findings) > MAX_FINDINGS:
                    return findings
        # Bounded static decoding only; no eval, imports, commands or asset fetches.
        for match in BASE64.finditer(value):
            try:
                raw = base64.b64decode(match.group(), validate=True)
                decoded = raw.decode("utf-8")
            except (ValueError, binascii.Error, UnicodeDecodeError):
                continue
            if not decoded or any(ord(c) < 32 and c not in "\r\n\t" for c in decoded):
                continue
            add("privacy.base64-text", "review", mapping[match.start()], view)
            for rule, tier, pattern in RULES:
                if pattern.search(decoded):
                    add(rule, tier, mapping[match.start()], f"{view}+base64")
            if len(findings) > MAX_FINDINGS:
                return findings
    return findings


class Scan:
    def __init__(self, max_files: int, max_bytes: int, max_total_bytes: int):
        self.max_files, self.max_bytes, self.max_total_bytes = max_files, max_bytes, max_total_bytes
        self.files, self.gaps, self.findings, self.entries, self.bytes_read = [], [], [], 0, 0
        self.stopped = False

    def gap(self, path_id: str, reason: str) -> None:
        self.gaps.append({"path_id": path_id, "reason": reason})

    def walk(self, parent_fd: int, name: str, relative: str, target_index: int, depth: int = 0) -> None:
        if self.stopped:
            return
        path_id = f"target-{target_index}:" + digest(os.fsencode(relative))
        self.entries += 1
        if self.entries > MAX_ENTRIES or depth > 64:
            self.gap(path_id, "entry-or-depth-limit")
            self.stopped = True
            return
        try:
            info = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
            if stat.S_ISLNK(info.st_mode):
                self.gap(path_id, "symlink-refused")
                return
            if not stat.S_ISREG(info.st_mode) and not stat.S_ISDIR(info.st_mode):
                self.gap(path_id, "nonregular-file-refused")
                return
            flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
            if stat.S_ISDIR(info.st_mode):
                flags |= os.O_DIRECTORY
            fd = os.open(name, flags, dir_fd=parent_fd)
            try:
                opened = os.fstat(fd)
                if (info.st_dev, info.st_ino, info.st_mode) != (opened.st_dev, opened.st_ino, opened.st_mode):
                    self.gap(path_id, "changed-before-open")
                    return
                if stat.S_ISDIR(opened.st_mode):
                    if name.lower() in EXCLUDED_DIRS:
                        self.gap(path_id, "excluded-directory")
                        return
                    # An Obsidian vault is never traversed, including a supplied root.
                    try:
                        os.stat(".obsidian", dir_fd=fd, follow_symlinks=False)
                    except FileNotFoundError:
                        pass
                    else:
                        self.gap(path_id, "vault-refused")
                        return
                    # scandir streams entries so directory inventory is also bounded.
                    with os.scandir(fd) as children:
                        for child in children:
                            self.walk(fd, child.name, relative + "/" + child.name, target_index, depth + 1)
                            if self.stopped:
                                break
                    return
                if Path(name).suffix.lower() not in EXTENSIONS:
                    self.gap(path_id, "unsupported-type-or-binary")
                    return
                if len(self.files) >= self.max_files:
                    self.gap(path_id, "file-limit")
                    self.stopped = True
                    return
                if opened.st_size > self.max_bytes:
                    self.gap(path_id, "file-byte-limit")
                    return
                remaining = self.max_total_bytes - self.bytes_read
                limit = min(self.max_bytes, remaining)
                if opened.st_size > remaining:
                    self.gap(path_id, "total-byte-limit")
                    self.stopped = True
                    return
                chunks, count = [], 0
                while count <= limit:
                    chunk = os.read(fd, min(65536, limit + 1 - count))
                    if not chunk:
                        break
                    chunks.append(chunk)
                    count += len(chunk)
                raw = b"".join(chunks)
                self.bytes_read += len(raw)
                after = os.fstat(fd)
                if len(raw) > limit:
                    self.gap(path_id, "byte-limit-during-read")
                    return
                if (opened.st_size, opened.st_mtime_ns, opened.st_ctime_ns) != (after.st_size, after.st_mtime_ns, after.st_ctime_ns):
                    self.gap(path_id, "changed-during-read")
                    return
                try:
                    text = raw.decode("utf-8")
                except UnicodeDecodeError:
                    self.gap(path_id, "non-utf8-text")
                    return
                if "\x00" in text:
                    self.gap(path_id, "binary-content")
                    return
                file_hash = digest(raw)
                self.files.append({"path_id": path_id, "sha256": file_hash, "bytes": len(raw)})
                self.findings.extend(text_findings(text, file_hash, path_id))
                if len(self.findings) > MAX_FINDINGS:
                    self.findings = self.findings[:MAX_FINDINGS]
                    self.gap(path_id, "finding-limit")
                    self.stopped = True
            finally:
                os.close(fd)
        except OSError:
            # Exception messages may contain secrets in filenames: fixed reasons only.
            self.gap(path_id, "read-or-traversal-error")

    def target(self, supplied: str, index: int) -> None:
        path_id = f"target-{index}:" + digest(b".")
        absolute = Path(os.path.abspath(supplied))
        fd = os.open(absolute.anchor, os.O_RDONLY | os.O_DIRECTORY)
        try:
            # Open every ancestor relative to its held descriptor, refusing symlinks.
            for component in absolute.parts[1:-1]:
                if component.lower() in EXCLUDED_DIRS:
                    self.gap(path_id, "excluded-ancestor")
                    return
                next_fd = os.open(component, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
                os.close(fd)
                fd = next_fd
                try:
                    os.stat(".obsidian", dir_fd=fd, follow_symlinks=False)
                except FileNotFoundError:
                    pass
                else:
                    self.gap(path_id, "vault-ancestor-refused")
                    return
            self.walk(fd, absolute.name or ".", ".", index)
        except OSError:
            self.gap(path_id, "target-or-ancestor-refused")
        finally:
            os.close(fd)

    def report(self) -> dict:
        if not self.files and not self.gaps:
            self.gap("scan", "no-supported-files")
        blocks = sum(f["tier"] == "block" for f in self.findings)
        reviews = len(self.findings) - blocks
        return {"scanner": "local-publication-preflight", "version": VERSION,
                "status": "incomplete" if self.gaps else "blocked" if blocks else "review" if reviews else "no-matches",
                "summary": {"files_scanned": len(self.files), "bytes_read": self.bytes_read,
                            "block_findings": blocks, "review_findings": reviews, "gaps": len(self.gaps)},
                "files": self.files, "findings": self.findings, "gaps": self.gaps,
                "noncoverage": ["Names, addresses, private prose and images require manual review.",
                                "No remote or referenced assets are fetched; supply local build assets explicitly.",
                                "Only UTF-8 supported extensions; no arbitrary encodings, runtime behavior or all-secret guarantee.",
                                "HTML entities (up to three rounds) and bounded standard base64 text are heuristic views.",
                                "A concurrently changing tree is outside this stable-copy review guarantee."]}


class SafeParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        self.print_usage(sys.stderr)
        self.exit(2, "publication-preflight: invalid arguments; supply explicit targets and reviewed limits\n")


def main(argv: list[str] | None = None) -> int:
    parser = SafeParser(description=__doc__)
    parser.add_argument("targets", nargs="+", help="Explicit local files or directories; paths omitted from output")
    parser.add_argument("--max-files", type=int, default=MAX_FILES)
    parser.add_argument("--max-bytes", type=int, default=MAX_BYTES)
    parser.add_argument("--max-total-bytes", type=int, default=MAX_TOTAL_BYTES)
    parser.add_argument("--version", action="version", version=VERSION)
    args = parser.parse_args(argv)
    for value, ceiling in [(args.max_files, MAX_FILES), (args.max_bytes, MAX_BYTES), (args.max_total_bytes, MAX_TOTAL_BYTES)]:
        if not 1 <= value <= ceiling:
            parser.error("invalid limit")
    if len(args.targets) > MAX_FILES:
        parser.error("too many targets")
    scan = Scan(args.max_files, args.max_bytes, args.max_total_bytes)
    for index, target in enumerate(args.targets, 1):
        if scan.stopped:
            scan.gap(f"target-{index}:" + digest(b"."), "not-scanned-after-limit")
        else:
            scan.target(target, index)
    report = scan.report()
    print(json.dumps(report, indent=2, ensure_ascii=True))
    return 2 if report["gaps"] else 1 if report["findings"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
