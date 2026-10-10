"""Bounded local storyboard media validation and deterministic sketch rendering."""
from __future__ import annotations

import base64
import binascii
import io
import math
import re
import warnings
from PIL import Image, ImageDraw

MAX_REFERENCE_BYTES = 1024 * 1024
MAX_BOARD_BYTES = 8 * 1024 * 1024
DATA_URL = re.compile(r'^data:image/(png|jpeg|webp);base64,([A-Za-z0-9+/]*={0,2})$')


def sketch(value):
    if not isinstance(value, dict) or set(value) != {'strokes'}:
        raise ValueError('Sketch must contain strokes only')
    strokes = value['strokes']
    if not isinstance(strokes, list) or len(strokes) > 64:
        raise ValueError('Sketch allows at most 64 strokes')
    clean = []
    for stroke in strokes:
        if not isinstance(stroke, dict) or set(stroke) != {'points'}:
            raise ValueError('Stroke must contain points only')
        points = stroke['points']
        if not isinstance(points, list) or not 1 <= len(points) <= 512:
            raise ValueError('Stroke allows 1–512 points')
        for point in points:
            if (not isinstance(point, list) or len(point) != 2 or
                any(isinstance(n, bool) or not isinstance(n, (int, float)) or
                    not math.isfinite(n) or not 0 <= n <= 1 for n in point)):
                raise ValueError('Sketch points must be normalized coordinates from 0 to 1')
        clean.append({'points': [list(point) for point in points]})
    return {'strokes': clean}


def reference(value):
    if not isinstance(value, dict) or not {'data_url'} <= set(value) <= {'data_url', 'name', 'description'}:
        raise ValueError('Reference fields are data_url, optional name and description')
    url = value['data_url']
    if not isinstance(url, str) or len(url) > 4 * ((MAX_REFERENCE_BYTES + 2) // 3) + 32:
        raise ValueError('Reference image exceeds 1 MiB')
    match = DATA_URL.fullmatch(url)
    if not match:
        raise ValueError('Reference must be a base64 PNG, JPEG or WebP data URL; remote URLs and SVG are unsupported')
    try:
        data = base64.b64decode(match[2], validate=True)
        if not data or len(data) > MAX_REFERENCE_BYTES:
            raise ValueError('Reference image exceeds 1 MiB')
        with warnings.catch_warnings():
            warnings.simplefilter('error', Image.DecompressionBombWarning)
            with Image.open(io.BytesIO(data)) as image:
                if image.format != {'png': 'PNG', 'jpeg': 'JPEG', 'webp': 'WEBP'}[match[1]]:
                    raise ValueError('Reference bytes do not match the declared image type')
                if not 1 <= image.width <= 4096 or not 1 <= image.height <= 4096 or image.width * image.height > 16_000_000:
                    raise ValueError('Reference dimensions exceed 4096 per side or 16 million pixels')
                image.verify()
            with Image.open(io.BytesIO(data)) as image:
                image.load()
    except (OSError, SyntaxError, binascii.Error, Image.DecompressionBombError, Image.DecompressionBombWarning) as exc:
        raise ValueError('Reference contains invalid or unsafe image bytes') from exc
    result = {'data_url': url}
    for field, limit in (('name', 120), ('description', 2000)):
        if field in value:
            if not isinstance(value[field], str) or len(value[field]) > limit:
                raise ValueError(f'Reference {field} must be text up to {limit} characters')
            result[field] = value[field]
    return result


def reference_image(value):
    match = DATA_URL.fullmatch(value['data_url'])
    return match[1], match[2]


def render_sketch(value):
    image = Image.new('RGB', (960, 540), 'white')
    draw = ImageDraw.Draw(image)
    for stroke in sketch(value)['strokes']:
        points = [(round(x * 959), round(y * 539)) for x, y in stroke['points']]
        if len(points) == 1:
            x, y = points[0]
            draw.ellipse((x-2, y-2, x+2, y+2), fill='#202020')
        else:
            draw.line(points, fill='#202020', width=4, joint='curve')
    output = io.BytesIO()
    image.save(output, format='PNG')
    return base64.b64encode(output.getvalue()).decode('ascii')
