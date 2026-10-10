"""Read-only catalog and installed template integrity checks for Design Library."""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
from pathlib import Path
from typing import Any


ROOT = Path(__file__).parent
OWNER = "Design Templates"
ID_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
HASH_RE = re.compile(r"[0-9a-f]{64}\Z")
SKILL_RE = re.compile(r"artifact-template-studio-[a-z0-9]+(?:-[a-z0-9]+)*\Z")
PUBLIC_FIELDS = (
    "id", "name", "summary", "category", "tags", "bestFor", "avoidWhen",
    "interactions", "limitations", "skillName", "sourceHash", "availability",
)
GUIDANCE_FILES = ("DESIGN.md", "WORKFLOW.md", "design/foundations.json", "design/ADAPTATION.md")


class CatalogError(ValueError):
    """A catalog entry or installed source is unsafe or invalid."""


def _plain_file(path: Path) -> None:
    try:
        mode = path.lstat().st_mode
    except OSError as exc:
        raise CatalogError(f"Missing file: {path.name}") from exc
    if not stat.S_ISREG(mode):
        raise CatalogError(f"Expected a regular file: {path.name}")


def _plain_dir(path: Path) -> None:
    try:
        mode = path.lstat().st_mode
    except OSError as exc:
        raise CatalogError(f"Missing directory: {path.name}") from exc
    if not stat.S_ISDIR(mode):
        raise CatalogError(f"Expected a real directory: {path.name}")


def _sha256_file(path: Path) -> str:
    _plain_file(path)
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    try:
        fd = os.open(path, flags)
        with os.fdopen(fd, "rb") as stream:
            if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
                raise CatalogError(f"Expected a regular file: {path.name}")
            digest = hashlib.sha256()
            for block in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(block)
            return digest.hexdigest()
    except OSError as exc:
        raise CatalogError(f"Cannot read source file: {path.name}") from exc


def source_fingerprint(source: Path) -> str:
    """Hash every file relative to assets/source, refusing symlinks and special files."""
    _plain_dir(source)
    files: list[dict[str, str]] = []
    for directory, dirs, names in os.walk(source, followlinks=False):
        here = Path(directory)
        _plain_dir(here)
        for name in dirs:
            _plain_dir(here / name)
        for name in names:
            path = here / name
            relative = path.relative_to(source).as_posix()
            files.append({"path": relative, "sha256": _sha256_file(path)})
    if not files:
        raise CatalogError("Installed template source is empty")
    files.sort(key=lambda entry: entry["path"])
    payload = json.dumps(files, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _codex_home(codex_home: Path | None = None) -> Path:
    if codex_home is not None:
        return codex_home
    return Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex")


def _source_path(item: dict[str, Any], codex_home: Path | None = None) -> Path:
    skill_name = item["skillName"]
    if not SKILL_RE.fullmatch(skill_name):
        raise CatalogError("Template skill name is invalid")
    bundled = Path(os.environ.get("DESIGN_TEMPLATES_DATA_ROOT", ROOT.parents[1])) / "templates"
    if codex_home is None and bundled.is_dir():
        _plain_dir(bundled)
        package = bundled / skill_name
    else:
        home = _codex_home(codex_home)
        _plain_dir(home)
        _plain_dir(home / "skills")
        package = home / "skills" / skill_name
    # Check each package component before traversal. The skill name cannot escape.
    for part in (package, package / "assets", package / "assets" / "source"):
        _plain_dir(part)
    manifest = package / "artifact-template.json"
    _plain_file(manifest)
    try:
        details = json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise CatalogError("Installed template manifest is invalid") from exc
    if not isinstance(details, dict) or details.get("kind") != "site" or details.get("reference") != "assets/source":
        raise CatalogError("Installed template is not a Site source package")
    return package / "assets" / "source"


def source_status(item: dict[str, Any], codex_home: Path | None = None) -> tuple[str, Path | None]:
    try:
        path = _source_path(item, codex_home)
        actual_hash = source_fingerprint(path)
    except CatalogError as exc:
        return ("missing" if str(exc).startswith("Missing ") else "changed", None)
    return ("ready" if actual_hash == item["sourceHash"] else "changed", path)


def _guidance_refs(item: dict[str, Any], source: Path, manifest_path: Path | None = None) -> list[dict[str, str]]:
    """Bind package guidance to the same retained source using the release baseline."""
    baseline = manifest_path or Path(os.environ.get("DESIGN_TEMPLATES_DATA_ROOT", ROOT.parents[1])) / "provenance" / "template-assets.json"
    _plain_dir(baseline.parent)
    _plain_file(baseline)
    try:
        document = json.loads(baseline.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise CatalogError("Template provenance cannot be read") from exc
    if not isinstance(document, dict) or document.get("schemaVersion") != 1 or not isinstance(document.get("files"), list):
        raise CatalogError("Template provenance is invalid")
    prefix = f"templates/{item['skillName']}/"
    expected: dict[str, str] = {}
    for entry in document["files"]:
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
            raise CatalogError("Template provenance entry is invalid")
        name = entry["path"]
        if not name.startswith(prefix):
            continue
        relative = name[len(prefix):]
        parts = relative.split("/")
        digest = entry.get("sha256")
        if not relative or any(part in ("", ".", "..") for part in parts) or "\\" in relative:
            raise CatalogError("Template provenance path is unsafe")
        if relative in expected or not isinstance(digest, str) or not HASH_RE.fullmatch(digest):
            raise CatalogError("Template provenance hash is invalid or duplicated")
        expected[relative] = digest
    source_files = sorted(
        ({"path": name[len("assets/source/"):], "sha256": digest}
         for name, digest in expected.items() if name.startswith("assets/source/")),
        key=lambda entry: entry["path"],
    )
    payload = json.dumps(source_files, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    if not source_files or hashlib.sha256(payload).hexdigest() != item["sourceHash"]:
        raise CatalogError("Template provenance does not match the selected sourceHash")
    package = source.parents[1]
    refs = []
    # The package manifest controls the source path, so verify it before handing off.
    for name in ("artifact-template.json", *GUIDANCE_FILES):
        path = package / name
        digest = expected.get(name)
        mandatory = name in ("artifact-template.json", "DESIGN.md", "WORKFLOW.md")
        if digest is None:
            if mandatory or path.exists() or path.is_symlink():
                raise CatalogError(f"Template guidance has no provenance hash: {name}")
            continue
        for parent in path.parents:
            if parent == package:
                break
            _plain_dir(parent)
        if _sha256_file(path) != digest:
            raise CatalogError(f"Template guidance has changed: {name}")
        refs.append({"path": str(path), "sha256": digest})
    # foundations.sourceHash has a narrower documented scope than source_fingerprint.
    # Its bytes are verified above; the provenance source-file set supplies the binding.
    return refs


def _validate_item(item: Any) -> dict[str, Any]:
    if not isinstance(item, dict):
        raise CatalogError("Catalog item must be an object")
    required_strings = ("id", "name", "summary", "category", "skillName", "sourceHash")
    required_lists = ("tags", "bestFor", "avoidWhen", "interactions", "limitations")
    for key in required_strings:
        if not isinstance(item.get(key), str) or not item[key].strip():
            raise CatalogError(f"Catalog item has invalid {key}")
    for key in required_lists:
        if not isinstance(item.get(key), list) or not all(isinstance(value, str) for value in item[key]):
            raise CatalogError(f"Catalog item has invalid {key}")
    if not ID_RE.fullmatch(item["id"]):
        raise CatalogError("Catalog item ID is invalid")
    if not SKILL_RE.fullmatch(item["skillName"]):
        raise CatalogError("Catalog item skill name is invalid")
    if not HASH_RE.fullmatch(item["sourceHash"]):
        raise CatalogError("Catalog item source hash is invalid")
    for key, suffix in (("desktopPreview", "desktop"), ("mobilePreview", "mobile")):
        expected = f"assets/{item['id']}-{suffix}.png"
        if item.get(key) != expected:
            raise CatalogError(f"Catalog item {key} must be {expected}")
    if item.get("sourceKind", "site") != "site":
        raise CatalogError("Only Site templates are supported")
    return item


def load_catalog(catalog_path: Path | None = None) -> list[dict[str, Any]]:
    path = catalog_path or (Path(os.environ["DESIGN_LIBRARY_CATALOG"]) if "DESIGN_LIBRARY_CATALOG" in os.environ else ROOT / "catalog.json")
    _plain_file(path)
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise CatalogError("Catalog JSON cannot be read") from exc
    if not isinstance(document, dict) or document.get("schemaVersion") != 1 or document.get("owner") != OWNER:
        raise CatalogError("Catalog schema or owner is invalid")
    items = document.get("items")
    if not isinstance(items, list):
        raise CatalogError("Catalog items must be an array")
    validated = [_validate_item(item) for item in items]
    ids = [item["id"] for item in validated]
    if len(ids) != len(set(ids)):
        raise CatalogError("Catalog contains duplicate IDs")
    return validated


def _public_item(item: dict[str, Any], codex_home: Path | None = None) -> dict[str, Any]:
    status, _ = source_status(item, codex_home)
    return {**{key: item[key] for key in PUBLIC_FIELDS if key in item and key != "availability"}, "availability": status}


def browse(query: str = "", category: str = "all", *, catalog_path: Path | None = None, codex_home: Path | None = None) -> dict[str, Any]:
    if not isinstance(query, str) or not isinstance(category, str):
        raise CatalogError("Query and category must be text")
    if len(query) > 500 or len(category) > 100:
        raise CatalogError("Query or category is too long")
    needle = query.casefold().strip()
    items = []
    for item in load_catalog(catalog_path):
        if category.casefold() != "all" and item["category"].casefold() != category.casefold():
            continue
        haystack = " ".join(str(item.get(key, "")) for key in ("name", "summary", "category", "tags", "bestFor", "avoidWhen", "interactions"))
        if needle and needle not in haystack.casefold():
            continue
        items.append(_public_item(item, codex_home))
    return {"schemaVersion": 1, "items": items, "query": query, "category": category, "owner": OWNER}


def handoff(template_id: str, brief: str = "", *, catalog_path: Path | None = None, codex_home: Path | None = None,
            guidance_manifest_path: Path | None = None) -> dict[str, Any]:
    if not isinstance(template_id, str) or not ID_RE.fullmatch(template_id):
        raise CatalogError("Choose a registered template ID")
    if not isinstance(brief, str) or len(brief) > 10000:
        raise CatalogError("Brief must be text under 10,000 characters")
    item = next((candidate for candidate in load_catalog(catalog_path) if candidate["id"] == template_id), None)
    if item is None:
        raise CatalogError("Choose a registered template ID")
    availability, source_path = source_status(item, codex_home)
    if availability != "ready" or source_path is None:
        raise CatalogError(f"{item['name']} source is {availability}; selection cannot be handed off")
    guidance_refs = _guidance_refs(item, source_path, guidance_manifest_path)
    instructions = (
        "Use the verified Design Templates Site source at sourcePath as the complete template. "
        "Verify sourceHash and guidanceRefs hashes, then read the selected authoritative guidanceRefs "
        "before adapting. Preserve approved facts, explicit unknowns and the current design unless "
        "the brief authorizes change. Then copy the source into a new working directory and adapt that copy "
        "to the user's brief with Sites. Never edit the retained package in place. "
        "This selection is not creation or deployment."
    )
    handoff_text = (
        f"Selected Design Library template: {item['name']} ({template_id}).\n"
        f"Skill: {item['skillName']}\nSource: {source_path}\n"
        f"Source SHA-256: {item['sourceHash']}\nMode: complete-template\n"
        "Authoritative guidanceRefs (path | SHA-256):\n"
        + "\n".join(f"{ref['path']} | {ref['sha256']}" for ref in guidance_refs) + "\n"
        f"Brief: {brief or '(none provided)'}\n{instructions}"
    )
    return {
        "templateId": template_id, "name": item["name"], "skillName": item["skillName"],
        "sourcePath": str(source_path), "sourceHash": item["sourceHash"],
        "guidanceRefs": guidance_refs,
        "mode": "complete-template", "brief": brief, "instructions": instructions,
        "handoffText": handoff_text,
    }
