"""Explicit project authorization and frontend file boundaries."""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import urlsplit

MARKER = Path(".ux-design-toolkit/design-runtime.json")
EXTENSIONS = {".html", ".htm", ".css", ".scss", ".sass", ".less", ".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte", ".astro"}
EXCLUDED_PARTS = {".git", "node_modules", "vendor", "dist", "build", "coverage", ".next", ".nuxt", ".svelte-kit", ".astro", "target", "out", "public", "generated", "__generated__", ".impeccable"}
SENSITIVE = re.compile(r"(^\.env(?:\..*)?$|secret|credential|token|password|private[_-]?key|\.pem$|\.key$|id_rsa|id_ed25519|\.p12$|\.pfx$)", re.I)


def project_root(path: str | Path) -> Path:
    root = Path(path).expanduser().resolve(strict=True)
    if not root.is_dir():
        raise ValueError("Project root must be a directory")
    return root


def marker_path(root: Path) -> Path:
    return root / MARKER


def enabled(root: Path) -> bool:
    try:
        marker = marker_path(root)
        if marker.is_symlink():
            return False
        data = json.loads(marker.read_text(encoding="utf-8"))
        return data == {"schemaVersion": 1, "projectRoot": str(root), "hooksEnabled": True}
    except (OSError, ValueError):
        return False


def enable(root: Path) -> Path:
    marker = marker_path(root)
    marker.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    if marker.is_symlink():
        raise ValueError("Project marker cannot be a symlink")
    marker.write_text(json.dumps({"schemaVersion": 1, "projectRoot": str(root), "hooksEnabled": True}) + "\n", encoding="utf-8")
    marker.chmod(0o600)
    return marker


def disable(root: Path) -> bool:
    marker = marker_path(root)
    if not enabled(root):
        return False
    marker.unlink()
    return True


def allowed_file(root: Path, raw: str) -> Path | None:
    if not isinstance(raw, str) or not raw or "\x00" in raw:
        return None
    candidate = Path(raw)
    candidate = candidate if candidate.is_absolute() else root / candidate
    try:
        resolved = candidate.resolve(strict=True)
        rel = resolved.relative_to(root)
    except (OSError, ValueError, RuntimeError):
        return None
    if not resolved.is_file() or resolved.suffix.lower() not in EXTENSIONS:
        return None
    if any(part.lower() in EXCLUDED_PARTS or SENSITIVE.search(part) for part in rel.parts):
        return None
    return resolved


def explicit_target(root: Path, raw: str, *, allow_url: bool) -> str:
    url = urlsplit(raw)
    if url.scheme in {"http", "https"}:
        if not allow_url or not url.hostname or url.username or url.password:
            raise ValueError("A scan URL must be an explicit http(s) URL without embedded credentials")
        return raw
    if url.scheme:
        raise ValueError("Unsupported target URL scheme")
    path = allowed_file(root, raw)
    if path is None:
        raise ValueError(f"Target must be an existing frontend file inside the project: {raw}")
    return str(path)


def loopback_url(raw: str) -> str:
    parsed = urlsplit(raw)
    if parsed.scheme not in {"http", "https"} or parsed.hostname not in {"localhost", "127.0.0.1", "::1"}:
        raise ValueError("Live mode requires an explicit loopback dev URL")
    if parsed.username or parsed.password or parsed.fragment:
        raise ValueError("Live dev URL cannot contain credentials or a fragment")
    return raw
