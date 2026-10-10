"""Resolve one installed font file for both text measurement and FFmpeg drawing."""
from __future__ import annotations
import os
from pathlib import Path
from PIL import ImageFont


def resolve_font_file(font: str | None = None, *, base_dir: Path | None = None) -> Path:
    override = os.environ.get('VIDEO_WORKFLOW_FONT')
    if override:
        path = Path(override).expanduser()
        if not path.is_file():
            raise ValueError(f'VIDEO_WORKFLOW_FONT is not an existing font file: {path}')
        return path.resolve()
    if font:
        path = Path(font).expanduser()
        if not path.is_absolute() and base_dir:
            path = base_dir / path
        if path.is_file():
            return path.resolve()
        if Path(font).suffix.lower() in {'.ttf', '.otf', '.ttc'} and (Path(font).is_absolute() or base_dir):
            raise ValueError(f'Declared font file does not exist: {path}')
        try:
            face = ImageFont.truetype(font, 16)
            resolved = Path(face.path)
            if resolved.is_file():
                return resolved.resolve()
        except OSError:
            pass
    # The default DejaVu family falls back to the platform's Arial file. No font
    # bytes are bundled. Custom production typography should declare a file.
    if font not in {None, '', 'DejaVu Sans', 'Arial', 'sans-serif'}:
        raise ValueError(f'Cannot resolve font {font!r}; declare a licensed font file or VIDEO_WORKFLOW_FONT')
    candidates = [Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'),
                  Path('/System/Library/Fonts/Supplemental/Arial.ttf'),
                  Path('/Library/Fonts/Arial.ttf')]
    if windows_root := os.environ.get('WINDIR'):
        candidates.append(Path(windows_root) / 'Fonts' / 'arial.ttf')
    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve()
    try:
        face = ImageFont.truetype('DejaVuSans.ttf', 16)
        candidate = Path(face.path)
        if candidate.is_file():
            return candidate.resolve()
    except OSError:
        pass
    raise ValueError('No usable font file found; supply VIDEO_WORKFLOW_FONT or a project-relative licensed TTF/OTF file')
