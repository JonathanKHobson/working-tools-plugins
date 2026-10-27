#!/usr/bin/env python3
"""Local, deterministic product-photo ad hypotheses and editable SVG previews."""

import argparse
import base64
import hashlib
import html
import io
import json
import re
import shutil
import unicodedata
from pathlib import Path

from PIL import Image, ImageCms, ImageFont, ImageOps, UnidentifiedImageError

MAX_BRIEF_BYTES = 65536
MAX_IMAGE_BYTES = 20 * 1024 * 1024
MAX_PIXELS = 24_000_000
MAX_OBSERVATIONS = 8
MAX_PHOTOS = 8
ALLOWED_FORMATS = {"JPEG", "PNG", "WEBP"}
ALLOWED_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp"}
ROLES = {"product", "mockup", "personalization_preview", "artwork", "style_reference"}
TARGET_ROLES = ROLES - {"style_reference"}
CONTROL = re.compile(r"[\x00-\x1f\x7f]")


class BriefError(ValueError):
    pass


def clean_text(value, name, limit=120):
    if not isinstance(value, str) or not value.strip() or len(value) > limit or CONTROL.search(value):
        raise BriefError(f"{name} must be nonempty text of at most {limit} characters without controls")
    try:
        value.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise BriefError(f"{name} contains invalid Unicode") from exc
    return value.strip()


def local_path(value, base):
    value = clean_text(value, "photo path", 1024)
    if "://" in value or value.lower().startswith(("data:", "file:", "//")):
        raise BriefError("photo paths must be local filesystem paths, not URLs")
    path = Path(value)
    if path.suffix.lower() not in ALLOWED_SUFFIXES:
        raise BriefError(f"unsupported photo type: {path.suffix or '(none)'}")
    path = (base / path).resolve() if not path.is_absolute() else path.resolve()
    if not path.is_file():
        raise BriefError(f"missing photo: {path}")
    if path.stat().st_size > MAX_IMAGE_BYTES:
        raise BriefError(f"photo exceeds {MAX_IMAGE_BYTES} bytes: {path}")
    return path


def read_photo(path):
    try:
        with Image.open(path) as im:
            if im.format not in ALLOWED_FORMATS:
                raise BriefError(f"unsupported image encoding: {path}")
            if im.width * im.height > MAX_PIXELS or im.width < 100 or im.height < 100:
                raise BriefError(f"photo dimensions outside supported range: {path}")
            im = ImageOps.exif_transpose(im)
            im.thumbnail((1600, 1600), Image.Resampling.LANCZOS)
            profile_bytes = im.info.get("icc_profile")
            if profile_bytes:
                try:
                    alpha = im.getchannel("A") if "A" in im.getbands() else None
                    color_source = im if im.mode in ("RGB", "CMYK", "L") else im.convert("RGB")
                    rgb = ImageCms.profileToProfile(color_source, ImageCms.ImageCmsProfile(io.BytesIO(profile_bytes)), ImageCms.createProfile("sRGB"), outputMode="RGB")
                    if alpha is not None:
                        rgb.putalpha(alpha)
                    im = rgb
                except (OSError, ValueError, ImageCms.PyCMSError) as exc:
                    raise BriefError(f"invalid embedded color profile: {path}") from exc
            mode = "RGBA" if im.mode == "RGBA" else "RGB"
            clean = Image.new(mode, im.size)
            clean.paste(im.convert(mode))
            buffer = io.BytesIO()
            clean.save(buffer, format="PNG", optimize=True)
            source_hash = hashlib.sha256()
            with path.open("rb") as source:
                for chunk in iter(lambda: source.read(1024 * 1024), b""):
                    source_hash.update(chunk)
            return {"width": clean.width, "height": clean.height, "color_handling": "ICC converted to sRGB" if profile_bytes else "untagged, treated as sRGB", "source_sha256": source_hash.hexdigest(), "embedded_sha256": hashlib.sha256(buffer.getvalue()).hexdigest(), "uri": "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode("ascii")}
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError) as exc:
        raise BriefError(f"unreadable raster photo: {path}: {exc}") from exc


def load_brief(path):
    if not path.is_file() or path.stat().st_size > MAX_BRIEF_BYTES:
        raise BriefError("brief is missing or exceeds 64 KiB")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise BriefError(f"malformed UTF-8 JSON brief: {exc}") from exc
    if not isinstance(data, dict):
        raise BriefError("brief must be a JSON object")
    for field, limit in (("product_name", 36), ("audience", 80), ("destination_label", 24)):
        data[field] = clean_text(data[field], field, limit) if data.get(field) is not None else None
    data["best_first_hypothesis"] = data.get("best_first_hypothesis")
    if data["best_first_hypothesis"] not in (1, 2, 3) or isinstance(data["best_first_hypothesis"], bool):
        raise BriefError("best_first_hypothesis must be 1, 2 or 3")
    data["first_test_assumption"] = clean_text(data.get("first_test_assumption"), "first_test_assumption", 240)
    photos = data.get("photos")
    if not isinstance(photos, list) or not 1 <= len(photos) <= MAX_PHOTOS:
        raise BriefError("photos must contain 1–8 local images")
    validated = []
    for index, photo in enumerate(photos, 1):
        if not isinstance(photo, dict) or photo.get("role") not in ROLES:
            raise BriefError(f"photo {index} needs a supported image role")
        source = local_path(photo.get("path"), path.parent)
        observations = photo.get("observations")
        if not isinstance(observations, list) or not 1 <= len(observations) <= MAX_OBSERVATIONS:
            raise BriefError(f"photo {index} needs 1–8 visible observations")
        obs = [{"id": f"P{index}-O{j}", "text": clean_text(item, f"photo {index} observation {j}", 140)} for j, item in enumerate(observations, 1)]
        validated.append({"id": f"P{index}", "role": photo["role"], "path": str(source), "observations": obs, "pixels": read_photo(source)})
    if not any(p["role"] in TARGET_ROLES for p in validated):
        raise BriefError("at least one product, mockup, preview or artwork image is required")
    claims = data.get("claims", [])
    if not isinstance(claims, list) or len(claims) > 20:
        raise BriefError("claims must be a list of at most 20 entries")
    checked_claims = []
    for index, claim in enumerate(claims, 1):
        if not isinstance(claim, dict) or claim.get("status") not in ("approved", "unverified"):
            raise BriefError(f"claim {index} needs approved or unverified status")
        checked_claims.append({"id": f"C{index}", "text": clean_text(claim.get("text"), f"claim {index} text", 240), "source": clean_text(claim.get("source"), f"claim {index} source", 240), "status": claim["status"]})
    submitted = data.get("hypotheses")
    if not isinstance(submitted, list) or len(submitted) != 3:
        raise BriefError("brief must supply exactly three authored hypotheses")
    obs_roles = {o["id"]: p["role"] for p in validated for o in p["observations"]}
    obs_photos = {o["id"]: p["id"] for p in validated for o in p["observations"]}
    approved_facts = {c["id"] for c in checked_claims if c["status"] == "approved"}
    ideas = []
    for index, item in enumerate(submitted, 1):
        if not isinstance(item, dict):
            raise BriefError(f"hypothesis {index} must be an object")
        refs = item.get("observation_refs")
        if not isinstance(refs, list) or not refs or len(refs) > 8 or any(not isinstance(ref, str) or ref not in obs_roles for ref in refs) or len(set(refs)) != len(refs):
            raise BriefError(f"hypothesis {index} has an unsupported observation ref")
        if not any(obs_roles[ref] in TARGET_ROLES for ref in refs):
            raise BriefError(f"hypothesis {index} must cite a target product image, not style references alone")
        fact_refs = item.get("fact_refs", [])
        if not isinstance(fact_refs, list) or any(not isinstance(ref, str) or ref not in approved_facts for ref in fact_refs) or len(set(fact_refs)) != len(fact_refs):
            raise BriefError(f"hypothesis {index} has an unsupported or unapproved fact ref")
        idea = {"id": f"H{index}", "observation_refs": refs, "photo_refs": sorted({obs_photos[ref] for ref in refs}), "creative": f"ad-{index}.svg"}
        idea["fact_refs"] = fact_refs
        for field, limit in (("angle", 70), ("tension_or_desire", 240), ("premise", 240), ("interpretation", 240), ("competing_explanation", 240), ("confidence_rationale", 240), ("opening", 180), ("reveal", 180), ("hook", 100), ("proposed_extension", 180), ("small_test", 240), ("falsifier", 240), ("metric", 100), ("headline", 120), ("caption", 240)):
            idea[field] = clean_text(item.get(field), f"hypothesis {index} {field}", limit)
        confidence = item.get("confidence")
        if isinstance(confidence, bool) or not isinstance(confidence, int) or not 0 <= confidence <= 100:
            raise BriefError(f"hypothesis {index} confidence must be an integer from 0 to 100")
        idea["confidence"] = confidence
        if item.get("extension_status") not in ("proposed", "confirmed_available"):
            raise BriefError(f"hypothesis {index} extension_status must be proposed or confirmed_available")
        idea["extension_status"] = item["extension_status"]
        if idea["extension_status"] == "confirmed_available":
            idea["extension_source"] = clean_text(item.get("extension_source"), f"hypothesis {index} extension_source", 240)
        ideas.append(idea)
    if len({h["angle"].casefold() for h in ideas}) != 3 or len({h["premise"].casefold() for h in ideas}) != 3:
        raise BriefError("hypotheses need distinct angles and premises")
    return data, validated, checked_claims, ideas


def text_font(size):
    try:
        return ImageFont.truetype("Arial.ttf", size)
    except OSError:
        return ImageFont.load_default(size=size)


def fit_lines(value, size, max_width, max_lines, field):
    font = text_font(size)
    def fits(line):
        measured = font.getlength(line)
        conservative = sum(max(font.getlength(char), size) if unicodedata.east_asian_width(char) in ("W", "F") else font.getlength(char) for char in line)
        return max(measured, conservative) <= max_width
    lines = []
    current = ""
    for word in value.split():
        candidate = (current + " " + word).strip()
        if fits(candidate):
            current = candidate
            continue
        if current:
            lines.append(current)
            current = ""
        if fits(word):
            current = word
            continue
        piece = ""
        for char in word:
            if fits(piece + char):
                piece += char
            else:
                if not piece:
                    raise BriefError(f"{field} contains a glyph too wide for the layout")
                lines.append(piece)
                piece = char
        current = piece
    if current:
        lines.append(current)
    if len(lines) > max_lines:
        raise BriefError(f"{field} does not fit in {max_lines} lines; shorten the authored copy")
    return lines


def text_block(value, x, y, size, color, max_lines, field):
    lines = fit_lines(value, size, 900, max_lines, field)
    return "".join(f'<text x="{x}" y="{y + i * (size + 12)}" font-family="Arial, Helvetica, sans-serif" font-size="{size}" fill="{color}">{html.escape(line, quote=True)}</text>' for i, line in enumerate(lines))


def image_element(photo, x, y, w, h, clip_id):
    uri = photo["pixels"]["uri"]
    return f'<image x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet" href="{uri}" clip-path="url(#{clip_id})"/>'


def make_svg(data, variant, idea, photos):
    title_text = data["product_name"] or "Product concept"
    title = html.escape(title_text, quote=True)
    cta_text = data["destination_label"]
    cta = html.escape(cta_text, quote=True) if cta_text else None
    if text_font(26).getlength(title_text) + 3 * len(title_text) > 900:
        raise BriefError("product_name does not fit the top label")
    if cta_text and text_font(32).getlength(cta_text + "  →") > 850:
        raise BriefError("destination_label does not fit the action panel")
    by_id = {p["id"]: p for p in photos}
    selected = [by_id[ref] for ref in idea["photo_refs"] if by_id[ref]["role"] in TARGET_ROLES]
    labels = {"product": "PRODUCT PHOTO", "mockup": "PRODUCT MOCKUP", "personalization_preview": "PERSONALIZATION PREVIEW", "artwork": "PRODUCT ARTWORK"}
    if variant == 3 and len(selected) >= 2:
        first, second = selected[:2]
        definitions = '<clipPath id="left"><rect x="64" y="260" width="462" height="760" rx="24"/></clipPath><clipPath id="right"><rect x="554" y="260" width="462" height="760" rx="24"/></clipPath>'
        layout = '<rect x="64" y="260" width="952" height="760" rx="24" fill="#e9e8e4"/>' + image_element(first, 64, 260, 462, 760, "left") + image_element(second, 554, 260, 462, 760, "right")
        label = labels[first["role"]] + "  /  " + labels[second["role"]]
    else:
        photo = selected[0]
        layout = '<rect x="64" y="260" width="952" height="760" rx="32" fill="#e9e8e4"/>' + image_element(photo, 64, 260, 952, 760, "hero")
        definitions = '<clipPath id="hero"><rect x="64" y="260" width="952" height="760" rx="32"/></clipPath>'
        label = labels[photo["role"]]
    action = f'<rect x="64" y="1302" width="952" height="88" rx="18" fill="#172c2c"/><text x="100" y="1358" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="700" fill="#ffffff">{cta}  →</text>' if cta else ""
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1080" height="1440" viewBox="0 0 1080 1440" role="img" aria-label="{title} ad concept">
<defs>{definitions}</defs><rect width="1080" height="1440" fill="#f7f5f0"/>
<text x="64" y="94" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="700" fill="#353c3a" letter-spacing="3">{title}</text>
{text_block(idea['headline'], 64, 164, 48, '#172c2c', 2, f'hypothesis {variant} headline')}
{layout}<text x="64" y="1075" font-family="Arial, Helvetica, sans-serif" font-size="19" fill="#4b5752" letter-spacing="2">{label}</text>
{text_block(idea['caption'], 64, 1140, 29, '#172c2c', 3, f'hypothesis {variant} caption')}
{action}
</svg>'''
    return svg


def make_review(data, photos, claims, ideas):
    e = lambda value: html.escape(str(value), quote=True)
    cards = "".join(f'<article><h2>{e(h["id"])} · {e(h["angle"])}</h2><img src="{e(h["creative"])}" alt="{e(h["angle"])} portrait ad"><p><b>Tension or desire:</b> {e(h["tension_or_desire"])}</p><p><b>Premise:</b> {e(h["premise"])}</p><p><b>Interpretation:</b> {e(h["interpretation"])}</p><p><b>Alternative:</b> {e(h["competing_explanation"])}</p><p><b>Confidence:</b> {h["confidence"]}/100, subjective interpretation only. {e(h["confidence_rationale"])}</p><p><b>Evidence:</b> {e(", ".join(h["observation_refs"]))} · Facts: {e(", ".join(h["fact_refs"]) or "none")}</p><p><b>Opening / reveal / hook:</b> {e(h["opening"])} / {e(h["reveal"])} / {e(h["hook"])}</p><p><b>Extension:</b> {e(h["proposed_extension"])} [{e(h["extension_status"])}]</p><p><b>Small test:</b> {e(h["small_test"])}</p><p><b>Falsifier:</b> {e(h["falsifier"])}</p><p><b>Metric:</b> {e(h["metric"])}</p><a href="{e(h["creative"])}" download>Open editable SVG</a></article>' for h in ideas)
    obs = "".join(f'<li><b>{e(o["id"])}</b> ({e(p["role"])}, {e(p["id"])}): {e(o["text"])}</li>' for p in photos for o in p["observations"])
    ledger = "".join(f'<li><b>{e(c["id"])}</b> [{e(c["status"])}] {e(c["text"])} · Source: {e(c["source"])}</li>' for c in claims) or "<li>No nonvisual claims supplied.</li>"
    return f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(data["product_name"] or "Product concept")} · ad hypotheses</title><style>body{{font:17px/1.5 system-ui,sans-serif;margin:0;background:#f7f5f0;color:#172c2c}}main{{max-width:1260px;margin:auto;padding:32px}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:24px}}article{{background:white;padding:20px;border-radius:18px}}img{{width:100%;height:auto}}li{{margin:8px 0}}a{{color:#123b56}}</style><main><h1>{e(data["product_name"] or "Product concept")} · three ad hypotheses</h1><p>Local draft. Photo observations were supplied in the brief and need visual review. Scores concern interpretation only; metrics are proposed, not measured.</p><p><b>Best first test:</b> H{data["best_first_hypothesis"]}. <b>Assumption:</b> {e(data["first_test_assumption"])}</p><div class="grid">{cards}</div><h2>Observation ledger</h2><ul>{obs}</ul><h2>Nonvisual fact and claim ledger</h2><ul>{ledger}</ul><p>Review product fidelity, observation accuracy, rights, destination and platform requirements before use. No ad is published by this helper.</p></main></html>'''


def make_manifest(data, photos, claims, ideas, insights_only=False):
    hypotheses = []
    for idea in ideas:
        item = dict(idea)
        if insights_only:
            item.pop("creative", None)
        hypotheses.append(item)
    return {"product_name": data["product_name"], "audience": data["audience"], "best_first_hypothesis": data["best_first_hypothesis"], "first_test_assumption": data["first_test_assumption"], "observations": [{"photo_id": p["id"], "role": p["role"], "source_path": p["path"], "source_sha256": p["pixels"]["source_sha256"], "embedded_sha256": p["pixels"]["embedded_sha256"], "color_handling": p["pixels"]["color_handling"], "width": p["pixels"]["width"], "height": p["pixels"]["height"], "observations": p["observations"]} for p in photos], "claims": claims, "hypotheses": hypotheses, "status": "insights only; no render" if insights_only else "local SVG draft; authored hypotheses; unmeasured"}


def build(brief_path, output_dir):
    data, photos, claims, ideas = load_brief(brief_path)
    if output_dir.exists():
        raise BriefError(f"output directory already exists: {output_dir}")
    output_dir.mkdir(parents=True)
    try:
        for i in range(1, 4):
            (output_dir / f"ad-{i}.svg").write_text(make_svg(data, i, ideas[i - 1], photos), encoding="utf-8")
        manifest = make_manifest(data, photos, claims, ideas)
        (output_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (output_dir / "review.html").write_text(make_review(data, photos, claims, ideas), encoding="utf-8")
    except Exception:
        shutil.rmtree(output_dir)
        raise
    return output_dir


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("brief", type=Path)
    parser.add_argument("output_directory", type=Path, nargs="?")
    parser.add_argument("--insights-only", action="store_true", help="print validated hypotheses as JSON without rendering or creating files")
    args = parser.parse_args(argv)
    try:
        if args.insights_only:
            if args.output_directory is not None:
                raise BriefError("--insights-only does not take an output directory")
            data, photos, claims, ideas = load_brief(args.brief.resolve())
            print(json.dumps(make_manifest(data, photos, claims, ideas, insights_only=True), ensure_ascii=False, indent=2))
            return
        if args.output_directory is None:
            raise BriefError("output directory is required unless --insights-only is used")
        result = build(args.brief.resolve(), args.output_directory.resolve())
    except (BriefError, OSError) as exc:
        parser.exit(2, f"error: {exc}\n")
    print(result)


if __name__ == "__main__":
    main()
