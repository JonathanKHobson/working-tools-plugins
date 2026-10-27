#!/usr/bin/env python3
"""Build a self-contained depth card from an explicit local brief. No network."""
import argparse
import base64
import hashlib
import html
import io
import json
import math
from pathlib import Path
import re
import sys
import warnings

MAX_IMAGE_BYTES = 12 * 1024 * 1024
MAX_PIXELS = 24_000_000
MAX_TOTAL_BYTES = 30 * 1024 * 1024


def text_field(record, key, limit, required=False):
    value = record.get(key, "")
    if not isinstance(value, str) or len(value) > limit or (required and not value.strip()):
        raise ValueError(f"{key} must be {'nonempty ' if required else ''}text up to {limit} characters")
    return html.escape(value, quote=True)


def local_path(value, parent):
    if not isinstance(value, str) or not value or re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", value) or value.startswith('//'):
        raise ValueError("Supply an ordinary local image path, not a URL")
    path = Path(value).expanduser()
    return (parent / path).resolve() if not path.is_absolute() else path.resolve()


def encode_image(path):
    try:
        from PIL import Image, ImageOps
    except ImportError as exc:
        raise ValueError("Pillow is required in the selected local Python; no packages were installed") from exc
    if path.suffix.lower() not in {'.png', '.jpg', '.jpeg', '.webp'}:
        raise ValueError("Only local PNG, JPEG or WebP raster images are supported")
    if not path.is_file() or path.stat().st_size > MAX_IMAGE_BYTES:
        raise ValueError(f"Image missing or exceeds 12 MiB: {path.name}")
    with warnings.catch_warnings():
        warnings.simplefilter('error', Image.DecompressionBombWarning)
        with Image.open(path) as im:
            if im.format not in {'PNG', 'JPEG', 'WEBP'} or getattr(im, 'is_animated', False):
                raise ValueError("Unsupported or animated image")
            if im.width * im.height > MAX_PIXELS:
                raise ValueError("Image exceeds 24 megapixels")
            im = ImageOps.exif_transpose(im).convert('RGBA')
            profile = im.info.get('icc_profile')
            im.info.clear()
            if profile:
                im.info['icc_profile'] = profile
            stream = io.BytesIO()
            im.save(stream, format='PNG')
    return stream.getvalue()


def build(brief_path, output, overwrite=False):
    brief_path = Path(brief_path).resolve()
    output = Path(output).resolve()
    template = Path(__file__).resolve().parent.parent / 'assets' / 'depth-card.html'
    if output in {brief_path, template.resolve()}:
        raise ValueError("Output cannot replace the source brief or template")
    if output.suffix.lower() != '.html':
        raise ValueError("Output must be an .html file")
    if brief_path.stat().st_size > 256 * 1024:
        raise ValueError("Brief exceeds 256 KiB")
    brief = json.loads(brief_path.read_text(encoding='utf-8'))
    if not isinstance(brief, dict):
        raise ValueError("Brief must be a JSON object")
    fields = {'__TITLE__': text_field(brief, 'title', 100, True),
              '__SUBTITLE__': text_field(brief, 'subtitle', 180),
              '__BODY__': text_field(brief, 'body', 700)}
    finish = brief.get('finish', 'holographic')
    if finish not in {'holographic', 'gold', 'silver'}:
        raise ValueError('finish must be holographic, gold or silver')
    card_depth = brief.get('card_depth', 70)
    if isinstance(card_depth, bool) or not isinstance(card_depth, (int, float)) or not math.isfinite(card_depth) or not 0 <= card_depth <= 100:
        raise ValueError('card_depth must be a finite number from 0 to 100')
    for flag in ('foil', 'auto_rotate', 'exploded'):
        if flag in brief and not isinstance(brief[flag], bool):
            raise ValueError(f'{flag} must be boolean')
    fields['__CONFIG__'] = html.escape(json.dumps({'finish': finish, 'depth': card_depth,
        'foil': brief.get('foil', True), 'autoRotate': brief.get('auto_rotate', False),
        'exploded': brief.get('exploded', False)}), quote=True)
    layers = brief.get('layers')
    if not isinstance(layers, list) or not 1 <= len(layers) <= 5:
        raise ValueError("Supply one to five image layers")
    images, sources, total = [], [], 0
    for layer in layers:
        if not isinstance(layer, dict):
            raise ValueError("Each layer must be an object")
        depth = layer.get('depth', 0)
        if isinstance(depth, bool) or not isinstance(depth, (int, float)) or not math.isfinite(depth) or not 0 <= depth <= 48:
            raise ValueError("Depth must be a finite number between 0 and 48")
        if 'alt' not in layer:
            raise ValueError("Each layer needs alt text (empty only for a decorative layer)")
        alt = text_field(layer, 'alt', 240)
        path = local_path(layer.get('path'), brief_path.parent)
        if output == path:
            raise ValueError("Output cannot replace an input image")
        data = encode_image(path)
        total += len(data)
        if total > MAX_TOTAL_BYTES:
            raise ValueError("Combined normalized images exceed 30 MiB")
        sources.append({'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
        role = layer.get('role', 'background' if len(images) == 0 else 'foreground')
        if role not in {'background', 'foreground', 'particles'}:
            raise ValueError('role must be background, foreground or particles')
        shift = -6 if role == 'background' else depth * (0.14 if role == 'particles' else 0.36)
        images.append(f'<img class="depth-layer role-{role}" src="data:image/png;base64,{base64.b64encode(data).decode()}" alt="{alt}" style="--z:{depth}px;--shift:{shift:.3f}px">')
    facts = brief.get('facts', [])
    if not isinstance(facts, list) or len(facts) > 4 or any(not isinstance(f, dict) for f in facts):
        raise ValueError("Facts must be a list of up to four objects")
    fact_html = []
    for fact in facts:
        label = text_field(fact, 'label', 80, True)
        value = text_field(fact, 'value', 160, True)
        source = text_field(fact, 'source', 240, True)
        fact_html.append(f'<div class="fact"><dt>{label}</dt><dd>{value}<span class="source">Source: {source}</span></dd></div>')
    fields['__FACTS__'] = '<dl class="facts">' + ''.join(fact_html) + '</dl>' if facts else ''
    fields['__LAYERS__'] = ''.join(images)
    sparkles = brief.get('sparkles', 0)
    if isinstance(sparkles, bool) or not isinstance(sparkles, int) or not 0 <= sparkles <= 24:
        raise ValueError('sparkles must be an integer from 0 to 24')
    fields['__SPARKLES__'] = '<div class="sparkles" aria-hidden="true">' + ''.join(
        f'<i style="left:{(i * 47 + 13) % 91}%;top:{(i * 31 + 17) % 87}%;animation-delay:-{i * 0.37:.2f}s"></i>'
        for i in range(sparkles)) + '</div>' if sparkles else ''
    card_text = brief.get('card_text', [])
    if not isinstance(card_text, list) or len(card_text) > 4 or any(not isinstance(item, str) or len(item) > 160 for item in card_text):
        raise ValueError('card_text must be up to four short text lines')
    fields['__CARD_TEXT__'] = ''.join(f'<span>{html.escape(item, quote=True)}</span>' for item in card_text)
    back = brief.get('back')
    if back is not None:
        if not isinstance(back, dict):
            raise ValueError('back must be an object')
        back_title = text_field(back, 'title', 100, True)
        back_body = text_field(back, 'body', 700)
        fields['__BACK__'] = f'<div class="back-copy"><strong>{back_title}</strong><p>{back_body}</p></div>'
        fields['__FLIP_CONTROL__'] = '<button id="flip" type="button" aria-pressed="false">Show back</button>'
        fields['__HAS_BACK__'] = 'true'
        fields['__FLIP_HINT__'] = '; Enter or Space flips'
        fields['__CARD_ROLE__'] = 'button'
    else:
        fields['__BACK__'] = ''
        fields['__FLIP_CONTROL__'] = ''
        fields['__HAS_BACK__'] = 'false'
        fields['__FLIP_HINT__'] = ''
        fields['__CARD_ROLE__'] = 'group'
    document = template.read_text(encoding='utf-8')
    script = re.search(r'<script>(.*?)</script>', document, re.S).group(1)
    fields['__SCRIPT_HASH__'] = "'sha256-" + base64.b64encode(hashlib.sha256(script.encode()).digest()).decode() + "'"
    # A single substitution pass prevents user text from becoming a template token.
    document = re.sub(r'__[A-Z_]+__', lambda m: fields[m.group(0)], document)
    if not output.parent.is_dir():
        raise ValueError("Output parent directory must already exist")
    with output.open('w' if overwrite else 'x', encoding='utf-8') as handle:
        handle.write(document)
    return {'output': str(output), 'layers': len(layers), 'sources': sources,
            'status': 'generated; rendered and interaction review still required'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--brief', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--overwrite', action='store_true')
    args = parser.parse_args()
    try:
        result = build(args.brief, args.output, args.overwrite)
    except (ValueError, OSError, KeyError, json.JSONDecodeError) as exc:
        parser.exit(2, f"Error: {exc}\n")
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
