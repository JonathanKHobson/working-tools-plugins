"""Video family catalog with pinned staged animate-methods references."""

from __future__ import annotations

import base64
import hashlib
import json
import os
from pathlib import Path

from video_catalog import family_handoff, load_families

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "libraries" / "animate-methods"
STYLES = SOURCE / "styles"
SOURCE_REVISION = "7e5eb56feb2dd573f890e1b7b34748af43d58263"
STYLE_IDS = ("cut-paper", "crosshatch", "riso", "sketchbook", "math", "pixel", "isometric")
LOOKS = {
    "cut-paper": ("Cut paper", "Torn paper, shadows, crayon, patterns, and playful character worlds.", "Warm character stories and tactile explainers", "Layered collage with animation on twos"),
    "crosshatch": ("Crosshatch", "Boiling sketch ink, hatch shading, warm paper, and navy machine interiors.", "Process and mechanism explainers", "Sketchy ink with animation on twos"),
    "riso": ("Riso", "Three-ink risograph texture with halftone screens, overprints, and misregistration.", "Print-like editorial storytelling", "Halftone print with animation on twos"),
    "sketchbook": ("Sketchbook", "Graphite, one accent color, hand lettering, and an open notebook feel.", "Informal educational walkthroughs", "Pencil drawing with animation on twos"),
    "math": ("Math", "Black stage, axes, graphs, color-coded variables, and smooth easing.", "Quantitative ideas and visual proofs", "Precise diagrams with animation on ones"),
    "pixel": ("Pixel", "True low-resolution drawing enlarged with nearest-neighbor scaling.", "Retro timelines and digital history", "Pixel motion on ones or twos"),
    "isometric": ("Isometric", "Product line art with constant hairlines, white faces, rounded slabs, and one dark accent.", "System and product architecture", "Isometric movement on ones with spring settles"),
}


def _path(style_id: str, filename: str) -> Path:
    if style_id not in STYLE_IDS:
        raise ValueError("Unknown video style ID")
    path = STYLES / style_id / filename
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"Style source missing: {style_id}/{filename}")
    return path


def source_hash(style_id: str) -> str:
    h = hashlib.sha256()
    manifest = json.loads((SOURCE / 'SOURCE-MANIFEST.json').read_text())
    if manifest['revision'] != SOURCE_REVISION:
        raise ValueError('Source revision does not match the pinned inventory')
    for name in ("STYLE.md", "kit.js", "sample.png"):
        h.update(name.encode())
        raw = _path(style_id, name).read_bytes()
        expected = manifest['sha256'].get(f'styles/{style_id}/{name}')
        if hashlib.sha256(raw).hexdigest() != expected:
            raise ValueError('Style source differs from the pinned inventory; review before adoption')
        h.update(raw)
    return h.hexdigest()


def item(style_id: str, *, preview: bool = False, full: bool = False) -> dict:
    if style_id not in STYLE_IDS:
        raise ValueError("Unknown video style ID")
    name, summary, best_for, motion = LOOKS[style_id]
    result = {
        "id": style_id,
        "name": name,
        "summary": summary,
        "bestFor": best_for,
        "motion": motion,
        "kind": "visual-style",
        "status": "demo frame smoke passed; full film/audio unverified" if style_id != "sketchbook" else "demo smoke passed; caption overlap needs project repair; full film/audio unverified",
        "license": "MIT",
        "sourceProject": "cth9191/animate",
        "sourceRevision": SOURCE_REVISION,
        "sourcePath": f"libraries/animate-methods/styles/{style_id}/STYLE.md",
        "sourceHash": source_hash(style_id),
    }
    if preview:
        thumbnail = Path(os.environ.get("VIDEO_LIBRARY_PREVIEW_ROOT", ROOT / "runtime" / "video-style-library" / "ui" / "previews")) / f"{style_id}.jpg"
        if thumbnail.is_symlink() or not thumbnail.is_file():
            raise ValueError(f"Preview missing: {style_id}")
        raw = thumbnail.read_bytes()
        if not raw.startswith(b"\xff\xd8"):
            raise ValueError(f"Invalid JPEG preview: {style_id}")
        result["preview"] = "data:image/jpeg;base64," + base64.b64encode(raw).decode("ascii")
    if full:
        result["styleRules"] = _path(style_id, "STYLE.md").read_text(encoding="utf-8")
        result["kitPath"] = f"libraries/animate-methods/styles/{style_id}/kit.js"
    return result


def search(query: str = "", limit: int = 7) -> dict:
    if len(query) > 300 or not 1 <= limit <= 7:
        raise ValueError("Query must be at most 300 characters; limit must be 1–7")
    terms = query.casefold().split()
    results = []
    for style_id in STYLE_IDS:
        record = item(style_id)
        haystack = " ".join(str(record[k]) for k in ("id", "name", "summary", "bestFor", "motion")).casefold()
        score = sum(term in haystack for term in terms)
        if not terms or score:
            results.append((score, record))
    results.sort(key=lambda pair: -pair[0])
    fallback = bool(terms) and not results
    records = [record for _, record in results] if results else [item(i) for i in STYLE_IDS]
    return {'schemaVersion': 1, 'query': query, 'total': len(records), 'fallback': fallback,
            'notice': 'No exact terms matched; showing all seven styles for exploration.' if fallback else '',
            'items': records[:limit]}


def library_items(*, preview: bool = False) -> list[dict]:
    """One family per catalog card, with staged methods as distinct references."""
    families = load_families()
    methods = []
    for style_id in STYLE_IDS:
        record = item(style_id, preview=preview)
        record.update(id="method/" + style_id, methodId=style_id,
                      kind="staged-method", referenceOnly=True,
                      relatedFamilyIds=[family["id"] for family in families
                                        if style_id in family.get("relatedMethodIds", [])])
        methods.append(record)
    return families + methods


def library_search(query: str = "", limit: int = 50) -> dict:
    if len(query) > 300 or not 1 <= limit <= 100:
        raise ValueError("Query must be at most 300 characters; limit must be 1–100")
    records = library_items()
    terms = query.casefold().split()
    scored = []
    for record in records:
        fragments = [record.get(key, "") for key in ("id", "name", "summary", "bestFor", "motion")]
        fragments += [str(v) for v in record.get("facets", {}).values()]
        fragments += [str(e.get("title", "")) + " " + str(e.get("producer", ""))
                      for e in record.get("examples", [])]
        haystack = " ".join(map(str, fragments)).casefold()
        score = sum(term in haystack for term in terms)
        if not terms or score:
            scored.append((score, record))
    scored.sort(key=lambda pair: -pair[0])
    fallback = bool(terms) and not scored
    selected = [record for _, record in scored] if scored else records
    selected = [record if record["kind"] == "staged-method" else
                {**{key: record[key] for key in ("id", "name", "summary", "kind", "sourceHash", "sourceRevision")
                    if key in record},
                 "facets": record.get("facets", {}),
                 "exampleCount": len(record.get("examples", [])),
                 "examples": [{"id": example["id"], "title": example["title"],
                               "masterSha256": example["master"].get("sha256")}
                              for example in record.get("examples", [])]}
                for record in selected]
    return {"schemaVersion": 2, "query": query, "total": len(selected),
            "familyCount": sum(row["kind"] == "video-family" for row in records),
            "methodCount": len(STYLE_IDS), "fallback": fallback,
            "notice": "No exact terms matched; showing the library for exploration." if fallback else "",
            "items": selected[:limit]}


def library_item(style_id: str, *, full: bool = False) -> dict:
    if style_id in STYLE_IDS or style_id.startswith("method/"):
        method_id = style_id.removeprefix("method/")
        return item(method_id, full=full)
    record = next((row for row in load_families() if row["id"] == style_id), None)
    if record is None:
        raise ValueError("Unknown video style ID")
    return record


def library_handoff(style_id: str, source_hash_expected: str, brief: str = "", example_id: str = "") -> dict:
    if style_id in STYLE_IDS or style_id.startswith("method/"):
        return handoff(style_id.removeprefix("method/"), source_hash_expected, brief)
    family = library_item(style_id)
    return family_handoff(family, example_id or family["defaultExampleId"], source_hash_expected, brief)


def storyboard_elements(style_id: str) -> list[dict]:
    """Minimal Excalidraw elements for three editable storyboard beats."""
    label = LOOKS[style_id][0]
    elements = [{"id": "story_title", "type": "text", "x": 24, "y": 20,
                 "text": f"Video storyboard · {label}", "fontSize": 30}]
    for index, title in enumerate(("Opening", "Development", "Resolution")):
        x = 24 + index * 340
        elements.extend((
            {"id": f"beat_{index+1}_frame", "type": "rectangle", "x": x, "y": 95,
             "width": 310, "height": 230, "backgroundColor": "#f5f3ed"},
            {"id": f"beat_{index+1}_label", "type": "text", "x": x+14, "y": 345,
             "text": f"{index+1}. {title}", "fontSize": 20},
            {"id": f"beat_{index+1}_note", "type": "text", "x": x+14, "y": 385,
             "text": "Visual action:\nNarration / text:\nSound / transition:", "fontSize": 15},
        ))
    return elements


def handoff(style_id: str, source_hash_expected: str, brief: str = "") -> dict:
    if len(brief) > 4000:
        raise ValueError("Brief must be at most 4000 characters")
    selected = item(style_id, full=True)
    if source_hash_expected != selected["sourceHash"]:
        raise ValueError("Style source changed; refresh the library before using this selection")
    payload = {
        "styleId": style_id, "styleName": selected["name"],
        "sourceRevision": SOURCE_REVISION, "sourceHash": selected["sourceHash"],
        "sourcePath": selected["sourcePath"], "kitPath": selected["kitPath"],
        "license": selected["license"], "adoptionState": selected["status"],
        "brief": brief, "storyboardState": "editable scaffold; beats not yet authored or approved", "storyboard": {"title": f"Video storyboard · {selected['name']}",
                                      "elements": storyboard_elements(style_id)},
    }
    prompt = (
        "Use this selected Video Production Studio style for the next storyboard. "
        "Keep the source ID and hash attached to the work; inspect the exact STYLE.md before adapting. "
        "This is a staged method, not evidence that its kit has been run in this project. "
        "For a visual storyboard, use Draw and Think's existing draw_create_board with the included "
        "title and editable elements, then draw_open_board with the returned board_id. "
        "Treat board creation and opening as separate verified steps; do not overwrite an existing board. "
        "Replace the placeholder beats with the supplied brief and style rules, keeping motion and sound notes.\n\n"
        "Selected handoff JSON:\n" + json.dumps(payload, ensure_ascii=False, indent=2)
    )
    return {"styleId": style_id, "sourceHash": selected["sourceHash"],
            "sourceRevision": SOURCE_REVISION, "handoffText": prompt, "storyboard": payload["storyboard"]}
