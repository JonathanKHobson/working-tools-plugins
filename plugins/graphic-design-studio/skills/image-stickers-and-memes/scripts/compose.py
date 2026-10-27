#!/usr/bin/env python3
"""Deterministic local PNG sticker and meme composition. No network or installs."""

from __future__ import annotations

import argparse
import io
import os
from pathlib import Path
import sys
import tempfile

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageOps, UnidentifiedImageError


MAX_BYTES = 50 * 1024 * 1024
MAX_PIXELS = 40_000_000
MAX_SIDE = 8192
Image.MAX_IMAGE_PIXELS = MAX_PIXELS
ALLOWED = {".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff", ".bmp"}
DEFAULT_FONTS = (
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
)


def local_path(raw: str, *, output: bool = False) -> Path:
    if "://" in raw or raw.lower().startswith(("data:", "file:")):
        raise ValueError("Use a local filesystem path, not a URL or data URI")
    path = Path(raw).expanduser()
    suffix = path.suffix.lower()
    if (output and suffix != ".png") or (not output and suffix not in ALLOWED):
        raise ValueError("Output must be PNG" if output else "Unsupported input; use a raster PNG, JPEG, WebP, TIFF, or BMP (no SVG)")
    if not output and (not path.is_file() or path.stat().st_size > MAX_BYTES):
        raise ValueError("Input must be a local file of at most 50 MiB")
    return path


def load_image(raw: str) -> Image.Image:
    path = local_path(raw)
    try:
        with Image.open(path) as source:
            if source.width > MAX_SIDE or source.height > MAX_SIDE or source.width * source.height > MAX_PIXELS:
                raise ValueError("Image exceeds 8192 pixels per side or 40 million pixels")
            source.load()
            return ImageOps.exif_transpose(source).copy()
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError) as exc:
        raise ValueError(f"Cannot safely read raster image: {exc}") from exc


def choose_alpha(source: Image.Image, mask_path: str | None) -> Image.Image:
    source_alpha = source.convert("RGBA").getchannel("A")
    if mask_path:
        mask = load_image(mask_path)
        if mask.size != source.size:
            raise ValueError("Mask dimensions must match the oriented source image")
        if "A" in mask.getbands():
            alpha = mask.getchannel("A")
        elif mask.mode in ("L", "1"):
            alpha = mask.convert("L")
        else:
            raise ValueError("Mask must be grayscale or contain an alpha channel")
        alpha = ImageChops.multiply(alpha, source_alpha)
    else:
        if "A" not in source.getbands() and "transparency" not in source.info:
            raise ValueError("A cutout requires source transparency or --mask; choose --shape rectangle/circle for an opaque photo")
        alpha = source_alpha
        if alpha.getextrema() == (255, 255):
            raise ValueError("Source alpha is fully opaque; supply a subject mask or choose a geometric shape")
    if not alpha.getbbox():
        raise ValueError("Alpha/mask contains no visible pixels")
    return alpha


def make_sticker(args: argparse.Namespace) -> Image.Image:
    source = load_image(args.input)
    if args.shape == "cutout":
        alpha = choose_alpha(source, args.mask)
        box = alpha.getbbox()
        source = source.convert("RGBA")
        source.putalpha(alpha)
        source = source.crop(box)
    elif args.mask:
        raise ValueError("--mask is only valid with --shape cutout")
    else:
        source = source.convert("RGBA")
    if args.shape == "circle":
        side = min(source.size)
        left = (source.width - side) // 2
        top = (source.height - side) // 2
        source = source.crop((left, top, left + side, top + side))
        mask = Image.new("L", (side * 2, side * 2), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, side * 2 - 1, side * 2 - 1), fill=255)
        circle_alpha = mask.resize((side, side), Image.Resampling.LANCZOS)
        source.putalpha(ImageChops.multiply(source.getchannel("A"), circle_alpha))
    # Rectangle means the entire source frame; existing alpha is preserved.
    border = args.border
    padding = args.padding
    inset = border + padding
    out = Image.new("RGBA", (source.width + 2 * inset, source.height + 2 * inset))
    if border:
        base_alpha = Image.new("L", out.size)
        base_alpha.paste(source.getchannel("A"), (inset, inset))
        expanded = base_alpha.filter(ImageFilter.MaxFilter(border * 2 + 1))
        backing = Image.new("RGBA", out.size, args.border_color)
        backing.putalpha(expanded)
        out.alpha_composite(backing)
    out.alpha_composite(source, (inset, inset))
    return out


def font_path(raw: str | None) -> Path:
    if raw:
        path = Path(raw).expanduser()
        if "://" in raw or path.suffix.lower() not in {".ttf", ".otf", ".ttc"} or not path.is_file():
            raise ValueError("--font must name a local TTF, OTF or TTC file")
        return path
    for candidate in DEFAULT_FONTS:
        if Path(candidate).is_file():
            return Path(candidate)
    raise ValueError("No supported local bold font found; supply --font /path/to/font.ttf")


def wrap_caption(draw: ImageDraw.ImageDraw, caption: str, font: ImageFont.FreeTypeFont,
                 max_width: int, stroke: int) -> list[str]:
    lines: list[str] = []
    def text_width(value: str) -> int:
        box = draw.textbbox((0, 0), value, font=font, stroke_width=stroke)
        return box[2] - box[0]

    # Split only at explicit LF breaks. Within each segment, added wraps may
    # move a separating space to a line break; all other characters remain.
    for segment in caption.replace("\r\n", "\n").split("\n"):
        if not segment:
            lines.append("")
            continue
        words = segment.split(" ")
        current = words[0]
        if text_width(current) > max_width:
            raise ValueError("A caption word is too wide for the safe area")
        for word in words[1:]:
            if text_width(word) > max_width:
                raise ValueError("A caption word is too wide for the safe area")
            candidate = f"{current} {word}"
            if text_width(candidate) <= max_width:
                current = candidate
            else:
                if not current.strip():
                    raise ValueError("Caption spacing exceeds the safe area")
                lines.append(current)
                current = word
        if text_width(current) > max_width:
            raise ValueError("A caption word is too wide for the safe area")
        lines.append(current)
    return lines


def layout_caption(draw: ImageDraw.ImageDraw, caption: str, path: Path,
                   width: int, height: int, margin: int, max_size: int,
                   min_size: int, zone_height: int) -> tuple[ImageFont.FreeTypeFont, list[str], int, int]:
    for size in range(max_size, min_size - 1, -1):
        font = ImageFont.truetype(str(path), size)
        stroke = max(1, round(size * 0.09))
        try:
            lines = wrap_caption(draw, caption, font, width - 2 * margin, stroke)
        except ValueError:
            continue
        line_height = int(round(size * 1.18))
        if lines and len(lines) * line_height <= zone_height:
            return font, lines, stroke, line_height
    raise ValueError("Caption does not fit at the minimum readable font size; shorten it or use a larger image")


def make_meme(args: argparse.Namespace) -> tuple[Image.Image, Path]:
    source = load_image(args.input).convert("RGBA")
    if not args.top and not args.bottom:
        raise ValueError("Supply --top or --bottom caption")
    width, height = source.size
    margin = max(8, round(min(width, height) * 0.05))
    zone = max(1, round(height * 0.38) - margin)
    max_size = args.max_font_size or max(12, round(min(width, height) * 0.105))
    min_size = args.min_font_size or max(12, round(min(width, height) * 0.05))
    if min_size > max_size:
        raise ValueError("Minimum font size exceeds maximum")
    path = font_path(args.font)
    draw = ImageDraw.Draw(source)
    layouts = {}
    for position, caption in (("top", args.top), ("bottom", args.bottom)):
        if caption:
            layouts[position] = layout_caption(draw, caption, path, width, height, margin,
                                               max_size, min_size, zone)
    for position, (font, lines, stroke, line_height) in layouts.items():
        block_height = len(lines) * line_height
        y = margin if position == "top" else height - margin - block_height
        for line in lines:
            box = draw.textbbox((0, 0), line, font=font, stroke_width=stroke)
            x = (width - (box[2] - box[0])) / 2 - box[0]
            baseline = y - box[1]
            draw.text((round(x), round(baseline)), line, font=font, fill="white",
                      stroke_width=stroke, stroke_fill="black")
            y += line_height
    return source, path


def save_png(image: Image.Image, raw: str, protected_inputs: list[str], overwrite: bool) -> Path:
    out = local_path(raw, output=True)
    if any(out.resolve() == Path(item).expanduser().resolve() for item in protected_inputs):
        raise ValueError("Output must differ from source and mask inputs")
    if not out.parent.is_dir():
        raise ValueError("Output directory must already exist")
    if out.exists() and not overwrite:
        raise ValueError("Output exists; pass --overwrite to replace it")
    profile = image.info.get("icc_profile")
    image.info.clear()
    if profile:
        image.info["icc_profile"] = profile
    buffer = io.BytesIO()
    image.save(buffer, "PNG")
    if overwrite:
        fd, raw_temp = tempfile.mkstemp(prefix=f".{out.name}.", suffix=".tmp", dir=out.parent)
        temp = Path(raw_temp)
        try:
            with os.fdopen(fd, "wb") as handle:
                handle.write(buffer.getvalue())
            os.replace(temp, out)
        finally:
            temp.unlink(missing_ok=True)
    else:
        with out.open("xb") as handle:
            handle.write(buffer.getvalue())
    return out


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="mode", required=True)
    sticker = sub.add_parser("sticker", help="Local transparent or geometric PNG sticker")
    sticker.add_argument("input")
    sticker.add_argument("output")
    sticker.add_argument("--shape", choices=("cutout", "rectangle", "circle"), default="cutout")
    sticker.add_argument("--mask", help="Matching grayscale or alpha raster mask for cutout")
    sticker.add_argument("--padding", type=int, default=12, help="Transparent outer padding, pixels")
    sticker.add_argument("--border", type=int, default=12, help="Border width, 0–32 pixels; 0 disables")
    sticker.add_argument("--border-color", default="#ffffff", help="Pillow-compatible border color")
    sticker.add_argument("--overwrite", action="store_true")
    meme = sub.add_parser("meme", help="Caption a local raster at native oriented dimensions")
    meme.add_argument("input")
    meme.add_argument("output")
    meme.add_argument("--top", default="")
    meme.add_argument("--bottom", default="")
    meme.add_argument("--font", help="Local TTF/OTF/TTC; otherwise first available documented bold font")
    meme.add_argument("--max-font-size", type=int)
    meme.add_argument("--min-font-size", type=int)
    meme.add_argument("--overwrite", action="store_true")
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.mode == "sticker":
            if not 0 <= args.padding <= 256 or not 0 <= args.border <= 32:
                raise ValueError("Padding must be 0–256 and border 0–32 pixels")
            image = make_sticker(args)
            font = None
        else:
            if any(value is not None and not 12 <= value <= 512 for value in (args.min_font_size, args.max_font_size)):
                raise ValueError("Font sizes must be 12–512 pixels")
            image, font = make_meme(args)
        protected = [args.input]
        if args.mode == "sticker" and args.mask:
            protected.append(args.mask)
        out = save_png(image, args.output, protected, args.overwrite)
        print(f"Saved {out} ({image.width}x{image.height}, PNG){f'; font: {font}' if font else ''}")
        return 0
    except (ValueError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
