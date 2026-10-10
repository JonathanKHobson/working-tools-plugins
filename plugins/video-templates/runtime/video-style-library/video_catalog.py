"""Public-safe projection of Activity Atlas video families for the MCP chooser."""

from __future__ import annotations

import json
import os
from pathlib import Path
from urllib.parse import unquote, urlsplit

PUBLIC_BASE = "https://activity-atlas.jkylehobson.chatgpt.site/video-library/"
PUBLIC_HOST = urlsplit(PUBLIC_BASE).hostname
RELEASE_BASE = "https://github.com/JonathanKHobson/shareables/releases/download/video-library-2026-10-08-v1/"
DEFAULT_CATALOG = Path(__file__).resolve().parents[2] / "data/catalog.json"


def public_url(value: object) -> str | None:
    """Reject private, off-site, and traversal URLs before embedding widget media."""
    if not isinstance(value, str) or not value.strip():
        return None
    value = value.strip()
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc:
        if parsed.scheme != "https" or parsed.hostname != PUBLIC_HOST or parsed.username or parsed.password:
            return None
        path = parsed.path
        if not path.startswith("/video-library/"):
            return None
    else:
        path = value.split("?", 1)[0].split("#", 1)[0]
        if path.startswith("/"):
            if not path.startswith("/video-library/"):
                return None
            value = "https://" + PUBLIC_HOST + value
        else:
            value = PUBLIC_BASE + value
    decoded = unquote(path)
    if any(part in (".", "..") for part in decoded.split("/")) or "\\" in decoded:
        return None
    return value


def download_url(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    if safe := public_url(value):
        return safe
    if not value.startswith(RELEASE_BASE):
        return None
    parsed = urlsplit(value)
    decoded = unquote(parsed.path)
    if parsed.username or parsed.password or not parsed.path or decoded.endswith("/"):
        return None
    if any(part in (".", "..") for part in decoded.split("/")) or "\\" in decoded:
        return None
    return value


def _media(value: object, *, allow_release: bool = False) -> dict:
    raw = value if isinstance(value, dict) else {}
    return {key: raw.get(key) for key in (
        "sha256", "mimeType", "duration", "width", "height", "encodedFps",
        "sceneEvaluationHz", "actorPoseCadence", "textUpdateHz", "timeSeconds",
        "sourceMasterSha256", "label", "role", "id") if raw.get(key) is not None} | {
            "url": download_url(raw.get("url")) if allow_release else public_url(raw.get("url"))}


def _download(value: object, kind: str) -> dict:
    raw = value if isinstance(value, dict) else {}
    url = download_url(raw.get("url"))
    names = raw.get("contents", raw.get("includedFiles", []))
    included = [name for name in names if isinstance(name, str) and name and len(name) <= 240
                and not name.startswith(("/", "~")) and ":" not in name and "\\" not in name
                and all(part not in (".", "..") for part in name.split("/"))] if isinstance(names, list) else []
    paths = raw.get("includedFilePaths")
    valid_paths = ([name for name in paths if isinstance(name, str) and name and len(name) <= 240
                    and not name.startswith(("/", "~")) and ":" not in name and "\\" not in name
                    and all(part not in (".", "..") for part in name.split("/"))]
                   if isinstance(paths, list) else [])
    declared_count = raw.get("includedFiles")
    inventory_valid = (isinstance(declared_count, int) and not isinstance(declared_count, bool)
                       and declared_count > 0 and declared_count == len(valid_paths) == len(paths)) if isinstance(paths, list) else False
    if isinstance(declared_count, list):
        inventory_valid = bool(included) and len(included) == len(declared_count)
    file_count = declared_count if inventory_valid and isinstance(declared_count, int) else len(included)
    prerequisites = raw.get("externalPrerequisites", [])
    if isinstance(prerequisites, dict):
        runtime = prerequisites.get("runtime", [])
        prerequisites = ([name for name in runtime if isinstance(name, str) and len(name) <= 240]
                         if isinstance(runtime, list) else [])
        packages = raw["externalPrerequisites"].get("packageDependencies")
        if isinstance(packages, dict) and packages:
            prerequisites.append(f"{len(packages)} package dependencies listed in the bundle guide")
    else:
        prerequisites = [name for name in prerequisites if isinstance(name, str) and len(name) <= 240] if isinstance(prerequisites, list) else []
    available = bool(raw.get("available")) and bool(url) and (kind != "bundle" or inventory_valid)
    reason = raw.get("reason") or ("Bundle file inventory is missing or mismatched" if kind == "bundle" and not inventory_valid
                                   else "Not available for download")
    license_value = raw.get("license")
    license_summary = license_value.get("summary", "") if isinstance(license_value, dict) else license_value
    return {"available": available, "url": url if available else None,
            "reason": "" if available else str(reason),
            "sha256": raw.get("sha256"), "bytes": raw.get("bytes"),
            "includedFiles": included, "includedFileCount": file_count,
            "externalPrerequisites": prerequisites,
            "license": str(license_summary or "")}


def _review(value: object) -> dict:
    raw = value if isinstance(value, dict) else {"state": value} if isinstance(value, str) else {}
    return {key: raw.get(key) for key in ("state", "scope", "artifactSha256", "date", "limitations")
            if isinstance(raw.get(key), str)}


def _example(family_id: str, raw: dict) -> dict:
    master = _media(raw.get("master"), allow_release=True)
    preview_video = _media(raw.get("previewVideo"))
    if preview_video.get("sourceMasterSha256") and preview_video["sourceMasterSha256"] != master.get("sha256"):
        preview_video["url"] = None
    poster = _media(raw.get("poster"))
    if poster.get("sourceMasterSha256") and poster["sourceMasterSha256"] != master.get("sha256"):
        poster["url"] = None
    gallery = [_media(entry) for entry in raw.get("gallery", []) if isinstance(entry, dict)]
    downloads = raw.get("downloads") if isinstance(raw.get("downloads"), dict) else {}
    normalized_downloads = {kind: _download(downloads.get(kind), kind)
                            for kind in ("bundle", "video", "source", "prompt")}
    if not normalized_downloads["video"]["available"] and master["url"] and master["url"].startswith(RELEASE_BASE):
        master["url"] = None
    review = raw.get("review") if isinstance(raw.get("review"), dict) else {}
    producer = raw.get("producer")
    if isinstance(producer, dict):
        producer = producer.get("displayName") or producer.get("label") or producer.get("name")
    if isinstance(producer, list):
        producer = ", ".join(value for value in producer if isinstance(value, str))
    return {
        "id": str(raw.get("id") or ""), "familyId": family_id,
        "title": str(raw.get("title") or raw.get("id") or "Untitled example"),
        "relationship": str(raw.get("relationship") or ""),
        "producer": producer if isinstance(producer, str) else "", "format": str(raw.get("format") or ""),
        "master": master, "previewVideo": preview_video, "poster": poster, "gallery": gallery,
        "starterPrompt": str(raw.get("starterPrompt") or ""),
        "usageGuidance": str(raw.get("usageGuidance") or ""),
        "review": {kind: _review(review.get(kind)) for kind in ("technical", "creative", "listening", "reproduction")},
        "downloads": normalized_downloads,
        "detailUrl": public_url(raw.get("detailUrl")),
    }


def load_families(path: Path | None = None) -> list[dict]:
    path = path or Path(os.environ.get("VIDEO_LIBRARY_CATALOG", DEFAULT_CATALOG))
    if not path.is_file():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schemaVersion") != 2 or not isinstance(data.get("families"), list):
        raise ValueError("Video catalog must provide schemaVersion 2 and families")
    items = []
    for raw in data["families"]:
        if not isinstance(raw, dict):
            continue
        family_id = str(raw.get("id") or raw.get("slug") or "")
        if not family_id or "/" in family_id or ".." in family_id:
            continue
        examples = [_example(family_id, e) for e in raw.get("examples", []) if isinstance(e, dict) and e.get("id")]
        if not examples:
            continue
        default_id = raw.get("defaultExampleId")
        default = next((e for e in examples if e["id"] == default_id), examples[0])
        raw_facets = raw.get("facets") if isinstance(raw.get("facets"), dict) else {}
        facets = {key: [value for value in raw_facets.get(key, []) if isinstance(value, str)]
                  for key in ("producer", "format", "motion", "material", "useCase")
                  if isinstance(raw_facets.get(key), list)}
        items.append({
            "id": "family/" + family_id, "familyId": family_id,
            "name": str(raw.get("title") or raw.get("name") or family_id),
            "summary": str(raw.get("premise") or raw.get("summary") or ""),
            "usageGuidance": str(raw.get("usageGuidance") or raw.get("adaptationGuidance") or ""),
            "kind": "video-family", "defaultExampleId": default["id"],
            "examples": examples, "facets": facets, "relatedMethodIds": raw.get("relatedMethodIds") or [],
            "preview": default["poster"]["url"], "sourceHash": default["master"].get("sha256"),
            "sourceRevision": str(data.get("revision") or "catalog-v2"),
            "detailUrl": public_url(raw.get("detailUrl")) or default["detailUrl"] or PUBLIC_BASE + "#" + family_id,
        })
    return items


def family_handoff(family: dict, example_id: str, source_hash: str, brief: str = "") -> dict:
    if len(brief) > 4000:
        raise ValueError("Brief must be at most 4000 characters")
    example = next((e for e in family["examples"] if e["id"] == example_id), None)
    if example is None:
        raise ValueError("Unknown video example ID")
    master_hash = example["master"].get("sha256")
    if not master_hash or source_hash != master_hash:
        raise ValueError("Video master changed; refresh the library before using this selection")
    storyboard_title = f"Video storyboard · {family['name']} · {example['title']}"
    elements = [{"id": "story_title", "type": "text", "x": 24, "y": 20,
                 "text": storyboard_title, "fontSize": 30}]
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
    storyboard = {"title": storyboard_title, "elements": elements}
    payload = {"styleId": family["id"], "familyId": family["familyId"],
               "exampleId": example_id, "sourceHash": master_hash,
               "sourceRevision": family["sourceRevision"], "brief": brief,
               "usageGuidance": family["usageGuidance"], "exampleGuidance": example["usageGuidance"],
               "starterPrompt": example["starterPrompt"], "review": example["review"],
               "downloads": example["downloads"], "detailUrl": example["detailUrl"] or family["detailUrl"],
               "storyboardState": "editable scaffold; beats not yet authored or approved", "storyboard": storyboard}
    prompt = ("Use this selected Video Library family and exact example as a reference for a new storyboard. "
              "Inspect its media, recipe, rights, and review state before adapting it. "
              "Do not infer listening, creative approval, or cold-start reproduction from a technical pass. "
              "For a visual storyboard, use Draw and Think draw_create_board and draw_open_board as separate verified steps. "
              "Make three editable beats for opening, development, and resolution; then replace them with the supplied brief.\n\n"
              "Selected handoff JSON:\n" + json.dumps(payload, ensure_ascii=False, indent=2))
    return {"styleId": family["id"], "exampleId": example_id,
            "sourceHash": master_hash, "sourceRevision": family["sourceRevision"],
            "handoffText": prompt, "storyboard": storyboard}
