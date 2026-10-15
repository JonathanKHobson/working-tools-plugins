"""Build portable, standalone skill ZIPs from a verified plugin release ZIP.

The source archive must be a reviewed release with an exact file manifest.
No canonical checkout or installed plugin is read by this builder.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import stat
import tempfile
import zipfile

import yaml

try:
    from .release_archive import verify_archive
except ImportError:  # Direct script-path imports used by repository tests.
    _spec = importlib.util.spec_from_file_location("release_archive", Path(__file__).with_name("release_archive.py"))
    _release_archive = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_release_archive)
    verify_archive = _release_archive.verify_archive


_ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
_VERSION = re.compile(r"[0-9]+(?:\.[0-9]+){1,2}(?:[-+][0-9A-Za-z.-]+)?\Z")
_COMMIT = re.compile(r"[0-9a-f]{40}\Z")
_STAMP = (2026, 1, 1, 0, 0, 0)
_SETUP_URL = "https://github.com/JonathanKHobson/working-tools-plugins/blob/main/docs/install.md"


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _entry_metadata(data: bytes, path: str) -> tuple[str, str]:
    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ValueError(f"skill entry is not UTF-8: {path}") from exc
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"skill entry lacks YAML frontmatter: {path}")
    end = next((i for i, line in enumerate(lines[1:], 1) if line.strip() == "---"), None)
    if end is None:
        raise ValueError(f"skill entry has unclosed YAML frontmatter: {path}")
    try:
        metadata = yaml.safe_load("".join(lines[1:end]))
    except yaml.YAMLError as exc:
        raise ValueError(f"invalid skill frontmatter: {path}") from exc
    if not isinstance(metadata, dict):
        raise ValueError(f"skill frontmatter must be a mapping: {path}")
    name, description = metadata.get("name"), metadata.get("description")
    if not isinstance(name, str) or not name.strip():
        raise ValueError(f"skill name is missing: {path}")
    if not isinstance(description, str) or not description.strip():
        raise ValueError(f"skill description is missing: {path}")
    return name.strip(), description.strip()


def _zip_info(path: str, mode: int) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(path, _STAMP)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    info.external_attr = (stat.S_IFREG | mode) << 16
    return info


def _write_member(zf: zipfile.ZipFile, name: str, data: bytes, mode: int) -> None:
    zf.writestr(_zip_info(name, mode), data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def build_skill_bundles(
    archive: Path,
    expected_files: dict[str, str],
    expected_sha256: str,
    plugin_id: str,
    version: str,
    source_commit: str,
    output: Path,
) -> list[dict]:
    """Build one ZIP per top-level skill and return its publication metadata.

    `output` is a destination directory. Raises ValueError on unverified or
    unsafe input, before writing any bundle. Existing bundle names are replaced
    atomically after each bundle is complete.
    """
    if not isinstance(plugin_id, str) or not _ID.fullmatch(plugin_id):
        raise ValueError("unsafe plugin id")
    if not isinstance(version, str) or not _VERSION.fullmatch(version):
        raise ValueError("unsafe plugin version")
    if not isinstance(source_commit, str) or not _COMMIT.fullmatch(source_commit):
        raise ValueError("source_commit must be a full lowercase Git commit")
    if not isinstance(expected_sha256, str):
        raise ValueError("expected archive sha256 is required")
    verification = verify_archive(Path(archive), expected_files, expected_sha256)
    if not verification["passed"]:
        raise ValueError("source release ZIP failed verification: " + "; ".join(verification["errors"]))

    output = Path(output)
    if output.is_symlink() or (output.exists() and not output.is_dir()):
        raise ValueError("output must be a real directory")

    with zipfile.ZipFile(archive) as source:
        infos = {info.filename: info for info in source.infolist()}
        entries = sorted(
            path for path in expected_files
            if len(path.split("/")) == 3 and path.startswith("skills/") and path.endswith("/SKILL.md")
        )
        # Validate all entries before creating output, including ID collisions.
        skills = []
        ids = set()
        for entry in entries:
            directory = entry.split("/")[1]
            if not _ID.fullmatch(directory):
                raise ValueError(f"unsafe skill directory: {directory!r}")
            skill_id, description = _entry_metadata(source.read(entry), entry)
            if skill_id in ids:
                raise ValueError(f"duplicate skill id: {skill_id!r}")
            ids.add(skill_id)
            skills.append((directory, entry, skill_id, description))

        if not skills:
            return []
        output.mkdir(parents=True, exist_ok=True)
        results = []
        for directory, entry, skill_id, description in skills:
            filename = f"{plugin_id}-{directory}-{version}.zip"
            root = f"{plugin_id}-{directory}"
            original_entry = f".support/{entry}"
            frontmatter = yaml.safe_dump(
                {"name": skill_id, "description": description},
                allow_unicode=True, sort_keys=False, default_flow_style=False,
            )
            wrapper = (
                f"---\n{frontmatter}---\n\n"
                f"# {skill_id}\n\n"
                f"Before any work, read `{original_entry}` in this bundle. "
                "That file is the original procedure for this selected skill. "
                "Use other bundled skills only when this procedure calls for them. "
                "Resolve its relative "
                "document links from its own directory inside `.support/`, including any "
                "references, scripts, assets, and sibling plugin files. Treat `.support/` as the "
                "plugin root. Run package-root commands from that directory unless the "
                "original procedure explicitly specifies another working directory. Expand "
                "plugin-root placeholders to that directory; do not assume the caller cwd.\n\n"
                "This standalone archive includes the reviewed source tree for "
                "reference. It does not install or activate the full plugin runtime, "
                "accounts, MCP servers, or hooks. Follow the original procedure's "
                "external setup requirements where applicable.\n"
            ).encode("utf-8")
            readme = (
                f"# {skill_id}\n\n"
                f"Standalone skill from `{plugin_id}` version `{version}` at source commit `{source_commit}`.\n\n"
                f"Entry: `SKILL.md`. Original procedure: `{original_entry}`.\n\n"
                "Place this bundle's top-level folder in a host's standalone skills directory "
                "and read `SKILL.md`. The `.support/` directory conserves the complete, "
                "byte-exact reviewed plugin tree so relative and dynamic references remain "
                "available. It is supporting material, not an installed plugin or automatic "
                "registration of plugin, MCP, or hook configuration. External tools, accounts, "
                "and provider setup remain separate.\n\n"
                f"Setup: {_SETUP_URL}\n"
            ).encode("utf-8")
            bundle_manifest = {
                "plugin_id": plugin_id,
                "plugin_version": version,
                "source_commit": source_commit,
                "source_archive_sha256": expected_sha256,
                "original_entry": entry,
                "files": {f".support/{path}": digest for path, digest in sorted(expected_files.items())},
                "generated_files": {"SKILL.md": _digest(wrapper), "README.md": _digest(readme)},
            }
            manifest = (json.dumps(bundle_manifest, sort_keys=True, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
            temporary = None
            try:
                with tempfile.NamedTemporaryFile(prefix=f".{filename}.", suffix=".tmp", dir=output, delete=False) as raw:
                    temporary = Path(raw.name)
                with zipfile.ZipFile(temporary, "w", allowZip64=True) as target:
                    _write_member(target, f"{root}/SKILL.md", wrapper, 0o644)
                    _write_member(target, f"{root}/README.md", readme, 0o644)
                    _write_member(target, f"{root}/MANIFEST.json", manifest, 0o644)
                    for path in sorted(expected_files):
                        info = infos[path]
                        mode = 0o755 if ((info.external_attr >> 16) & 0o111) else 0o644
                        _write_member(target, f"{root}/.support/{path}", source.read(path), mode)
                # The new archive must round-trip every reviewed support byte.
                with zipfile.ZipFile(temporary) as check:
                    for path, digest in expected_files.items():
                        if _digest(check.read(f"{root}/.support/{path}")) != digest:
                            raise ValueError(f"bundle support mismatch: {path}")
                    if _digest(check.read(f"{root}/SKILL.md")) != _digest(wrapper):
                        raise ValueError("bundle wrapper mismatch")
                    if f"{root}/{original_entry}" not in check.namelist():
                        raise ValueError("original skill entry missing from bundle")
                os.replace(temporary, output / filename)
                temporary = None
            finally:
                if temporary is not None:
                    temporary.unlink(missing_ok=True)
            bundle_path = output / filename
            results.append({
                "id": skill_id,
                "directory": directory,
                "file": filename,
                "sha256": _digest(bundle_path.read_bytes()),
                "size": bundle_path.stat().st_size,
                "source_commit": source_commit,
                "original_entry": entry,
                "plugin_version": version,
            })
        return results
