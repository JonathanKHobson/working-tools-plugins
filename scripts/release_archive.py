"""release_archive.py

Bounded, read-only verification of a public plugin release ZIP against a
canonical reviewed file manifest. This module never extracts, writes, or
executes any content from the archive; it only reads bytes to compute
SHA256 digests and inspects ZIP metadata.

This is a verification helper for an existing release workflow. It makes no
claim about licensing or runtime correctness of the plugin content; it only
checks that a built/downloaded ZIP matches an approved manifest.
"""

from __future__ import annotations

import hashlib
import pathlib
import posixpath
import re
import stat
import zipfile
import zlib

class _Errors(list):
    def append(self, value):
        if len(self) < 256:
            super().append(str(value)[:1024])
        elif len(self) == 256:
            super().append('Further errors omitted after 256 diagnostics.')

    def extend(self, values):
        for value in values:
            self.append(value)


# Bounds enforced before any decompression of member content.
MAX_TOTAL_UNCOMPRESSED_BYTES = 256 * 1024 * 1024
MAX_FILE_UNCOMPRESSED_BYTES = 16 * 1024 * 1024
MAX_MEMBER_COUNT = 100000

# Chunk size used when reading member content to bound memory use.
_READ_CHUNK = 1024 * 1024

_HEX64_RE = re.compile(r'^[0-9a-f]{64}$')
_CONTROL_CHAR_RE = re.compile(r'[\x00-\x1f\x7f]')


def _is_valid_sha256_hex(value: object) -> bool:
    return isinstance(value, str) and bool(_HEX64_RE.fullmatch(value))


def _validate_manifest(expected_files: dict, expected_sha256) -> list[str]:
    """Validate the shape of the caller-supplied expected manifest itself.

    Returns a list of error strings. If any are present, verification must
    not proceed to open the archive.
    """
    errors: list[str] = _Errors()
    if not isinstance(expected_files, dict):
        errors.append('invalid manifest: expected_files must be a dict')
        return errors
    for name, digest in expected_files.items():
        if not isinstance(name, str) or not name:
            errors.append(f'invalid manifest path: {name!r}')
            continue
        if _CONTROL_CHAR_RE.search(name):
            errors.append(f'invalid manifest path (control chars): {name!r}')
        if '\\' in name:
            errors.append(f'invalid manifest path (backslash): {name!r}')
        if name.startswith('/') or pathlib.PureWindowsPath(name).drive:
            errors.append(f'invalid manifest path (absolute): {name!r}')
        parts = name.split('/')
        if any(p in ('..', '.', '') for p in parts):
            errors.append(f'invalid manifest path (traversal or empty component): {name!r}')
        if not _is_valid_sha256_hex(digest):
            errors.append(f'invalid expected digest for {name!r}')
    if expected_sha256 is not None and not _is_valid_sha256_hex(expected_sha256):
        errors.append('invalid expected archive sha256')
    return errors


def _name_is_structurally_safe(name: str, errors: list[str]) -> bool:
    """Check a ZIP member name for traversal / absolute / noncanonical
    issues. Appends readable errors and returns True only if the name is
    safe to treat as a relative package-root file path.
    """
    safe = True

    if name == '':
        errors.append('empty member name')
        return False

    if _CONTROL_CHAR_RE.search(name):
        errors.append(f'member name contains control characters: {name!r}')
        safe = False

    if '\\' in name:
        errors.append(f'member name uses backslash separators: {name!r}')
        safe = False

    if name.startswith('/') or pathlib.PureWindowsPath(name).drive:
        errors.append(f'member name is an absolute path: {name!r}')
        safe = False

    if name.endswith('/'):
        errors.append(f'explicit directory entry not allowed: {name!r}')
        safe = False

    parts = name.split('/')
    if any(p in ('..', '.', '') for p in parts):
        errors.append(f'member name contains traversal or empty component: {name!r}')
        safe = False

    normalized = posixpath.normpath(name)
    if normalized != name:
        errors.append(f'member name is not canonical: {name!r}')
        safe = False

    return safe


def _member_mode_bits(info: zipfile.ZipInfo) -> int:
    return (info.external_attr >> 16) & 0xFFFF


def _is_symlink(info: zipfile.ZipInfo) -> bool:
    mode = _member_mode_bits(info)
    return mode != 0 and stat.S_ISLNK(mode)


def _is_special_file(info: zipfile.ZipInfo) -> bool:
    mode = _member_mode_bits(info)
    if mode == 0:
        return False
    return stat.S_IFMT(mode) not in (0, stat.S_IFREG, stat.S_IFLNK)


def _is_encrypted(info: zipfile.ZipInfo) -> bool:
    return bool(info.flag_bits & 0x1)


def verify_archive(
    path: pathlib.Path,
    expected_files: dict,
    expected_sha256: str | None = None,
) -> dict:
    """Verify a plugin release ZIP against an approved file manifest.

    Never extracts or executes any member. Returns a result dict with keys
    'passed', 'errors', 'files', 'sha256'.
    """
    errors: list[str] = _Errors()
    result = {'passed': False, 'errors': errors, 'files': len(expected_files) if isinstance(expected_files, dict) else 0, 'sha256': ''}

    manifest_errors = _validate_manifest(expected_files, expected_sha256)
    if manifest_errors:
        errors.extend(manifest_errors)
        errors.sort()
        return result

    path = pathlib.Path(path)

    try:
        if not path.exists():
            errors.append(f'archive does not exist: {path}')
            errors.sort()
            return result
        if not path.is_file():
            errors.append(f'archive is not a regular file: {path}')
            errors.sort()
            return result
    except OSError as exc:
        errors.append(f'cannot stat archive: {exc}')
        errors.sort()
        return result

    # Whole-archive sha256, computed by streaming the raw file bytes.
    hasher = hashlib.sha256()
    try:
        with open(path, 'rb') as raw:
            while True:
                chunk = raw.read(_READ_CHUNK)
                if not chunk:
                    break
                hasher.update(chunk)
    except OSError as exc:
        errors.append(f'cannot read archive: {exc}')
        errors.sort()
        return result

    archive_sha256 = hasher.hexdigest()
    result['sha256'] = archive_sha256

    if expected_sha256 is not None and archive_sha256 != expected_sha256:
        errors.append('archive sha256 mismatch')

    try:
        zf = zipfile.ZipFile(path, 'r')
    except zipfile.BadZipFile as exc:
        errors.append(f'archive is not a valid zip file: {exc}')
        errors.sort()
        return result
    except OSError as exc:
        errors.append(f'cannot open archive: {exc}')
        errors.sort()
        return result

    try:
        with zf:
            infolist = zf.infolist()

            if len(infolist) > MAX_MEMBER_COUNT:
                errors.append(f'too many members in archive: {len(infolist)} > {MAX_MEMBER_COUNT}')
                errors.sort()
                return result

            seen_names: set[str] = set()
            safe_names: set[str] = set()
            total_declared_size = 0

            for info in infolist:
                name = info.filename
                if info.orig_filename != name:
                    errors.append(f'member name was normalized or truncated: {info.orig_filename!r}')
                    continue

                if name in seen_names:
                    errors.append(f'duplicate member name: {name!r}')
                    continue
                seen_names.add(name)

                if not _name_is_structurally_safe(name, errors):
                    continue

                if _is_symlink(info):
                    errors.append(f'symbolic link member not allowed: {name!r}')
                    continue

                if _is_special_file(info):
                    errors.append(f'special filesystem entry not allowed: {name!r}')
                    continue

                if _is_encrypted(info):
                    errors.append(f'encrypted member not allowed: {name!r}')
                    continue

                if info.file_size > MAX_FILE_UNCOMPRESSED_BYTES:
                    errors.append(
                        f'member exceeds per-file size limit: {name!r} '
                        f'({info.file_size} > {MAX_FILE_UNCOMPRESSED_BYTES})'
                    )
                    continue

                total_declared_size += info.file_size
                if total_declared_size > MAX_TOTAL_UNCOMPRESSED_BYTES:
                    errors.append(
                        'total declared uncompressed size exceeds limit: '
                        f'{total_declared_size} > {MAX_TOTAL_UNCOMPRESSED_BYTES}'
                    )
                    continue

                safe_names.add(name)

            expected_names = set(expected_files.keys())

            missing = sorted(expected_names - safe_names)
            for name in missing:
                errors.append(f'missing required file in archive: {name!r}')

            unexpected = sorted(safe_names - expected_names)
            for name in unexpected:
                errors.append(f'unexpected member not in manifest: {name!r}')

            for name in sorted(safe_names & expected_names):
                expected_digest = expected_files[name]
                try:
                    file_hasher = hashlib.sha256()
                    total_read = 0
                    read_limit = min(MAX_FILE_UNCOMPRESSED_BYTES, zf.getinfo(name).file_size)
                    with zf.open(name, 'r') as member:
                        while True:
                            chunk = member.read(min(_READ_CHUNK, read_limit - total_read + 1))
                            if not chunk:
                                break
                            total_read += len(chunk)
                            if total_read > read_limit:
                                errors.append(f'member actual size exceeds declared limit: {name!r}')
                                break
                            file_hasher.update(chunk)
                    if total_read != zf.getinfo(name).file_size:
                        errors.append(f'member actual size differs from declared size: {name!r}')
                    elif file_hasher.hexdigest() != expected_digest:
                        errors.append(f'content hash mismatch for file: {name!r}')
                except (NotImplementedError, EOFError, zlib.error) as exc:
                    errors.append(f'unsupported or corrupt member data: {name!r}: {exc}')
                except RuntimeError as exc:
                    errors.append(f'cannot read member (possibly encrypted): {name!r}: {exc}')
                except zipfile.BadZipFile as exc:
                    errors.append(f'corrupt member data: {name!r}: {exc}')
                except OSError as exc:
                    errors.append(f'io error reading member: {name!r}: {exc}')
    except zipfile.BadZipFile as exc:
        errors.append(f'archive is corrupt: {exc}')

    errors.sort()
    result['passed'] = len(errors) == 0
    return result
