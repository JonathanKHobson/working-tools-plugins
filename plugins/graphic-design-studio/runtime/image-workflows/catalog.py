"""Validated, read-only image workflow catalog and generation handoffs."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "catalog.json"
DOMAINS = ("graphic", "ux", "creative", "video")
RATIOS = ("Auto", "1:1", "4:5", "3:2", "2:3", "16:9", "9:16")
DETAILS = ("Concise", "Balanced", "Detailed")
BACKGROUNDS = ("Scene", "Transparent")
REFERENCES = ("none", "optional", "required")


def _bounded(value: str, label: str, maximum: int, *, required: bool = False) -> str:
    if not isinstance(value, str) or len(value) > maximum or (required and not value.strip()):
        raise ValueError(f"{label} must be a {'nonempty ' if required else ''}string of at most {maximum} characters")
    return value.strip()


def catalog() -> dict:
    """Load the owned static catalog; no user paths or remote content are read."""
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schemaVersion") != 1:
        raise ValueError("Unsupported image workflow catalog schema")
    revision = _bounded(data.get("revision"), "Catalog revision", 80, required=True)
    rows = data.get("items")
    if not isinstance(rows, list) or not 1 <= len(rows) <= 100:
        raise ValueError("Image workflow catalog must contain 1–100 items")
    seen = set()
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("Invalid image workflow item")
        item_id = _bounded(row.get("id"), "Workflow ID", 80, required=True)
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", item_id) or item_id in seen:
            raise ValueError("Image workflow IDs must be unique lowercase slugs")
        seen.add(item_id)
        for key, maximum in (("name", 120), ("category", 80), ("useCase", 300),
                             ("summary", 700), ("prompt", 10000), ("exampleSubject", 300)):
            _bounded(row.get(key), key, maximum, required=True)
        domains = row.get("domains")
        if not isinstance(domains, list) or not domains or any(d not in DOMAINS for d in domains):
            raise ValueError(f"Invalid domains for {item_id}")
        if row.get("ratio") not in RATIOS or row.get("detail") not in DETAILS:
            raise ValueError(f"Invalid image controls for {item_id}")
        if row.get("reference") not in REFERENCES:
            raise ValueError(f"Invalid reference requirement for {item_id}")
        checks = row.get("checks")
        if not isinstance(checks, list) or len(checks) > 20 or any(
            not isinstance(x, str) or not x.strip() or len(x) > 300 for x in checks
        ):
            raise ValueError(f"Invalid checks for {item_id}")
        if "previewAsset" in row and (not isinstance(row["previewAsset"], str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*\.(?:png|jpg|jpeg)", row["previewAsset"])):
            raise ValueError(f"Invalid preview asset for {item_id}")
    return data


def item(workflow_id: str) -> dict:
    _bounded(workflow_id, "Workflow ID", 80, required=True)
    data = catalog()
    for row in data["items"]:
        if row["id"] == workflow_id:
            return {"schemaVersion": 1, "revision": data["revision"], "item": row}
    raise ValueError("Unknown image workflow ID")


def search(query: str = "", domain: str = "all", limit: int = 30) -> dict:
    query = _bounded(query, "Query", 300)
    if domain not in ("all", *DOMAINS):
        raise ValueError("Unknown image workflow domain")
    if type(limit) is not int or not 1 <= limit <= 100:
        raise ValueError("Limit must be 1–100")
    data = catalog()
    terms = query.casefold().split()
    ranked = []
    for index, row in enumerate(data["items"]):
        if domain != "all" and domain not in row["domains"]:
            continue
        haystack = " ".join(str(row[k]) for k in ("id", "name", "category", "useCase", "summary"))
        haystack = haystack.casefold()
        if all(term in haystack for term in terms):
            score = sum(3 * (term in row["name"].casefold()) + (term in haystack) for term in terms)
            ranked.append((score, index, row))
    ranked.sort(key=lambda r: (-r[0], r[1]))
    return {"schemaVersion": 1, "revision": data["revision"], "query": query,
            "domain": domain, "total": len(ranked), "items": [r[2] for r in ranked[:limit]]}


def handoff(workflow_id: str, subject: str, aspect_ratio: str = "Auto",
            detail: str = "Balanced", reference_notes: str = "", background: str = "Scene",
            prompt_override: str = "", additional_instructions: str = "",
            revision: str = "") -> dict:
    selected = item(workflow_id)
    revision = _bounded(revision, "Catalog revision", 80)
    if revision and revision != selected["revision"]:
        raise ValueError("Catalog revision changed; refresh the workflow before using it")
    subject = _bounded(subject, "Subject", 1000, required=True)
    reference_notes = _bounded(reference_notes, "Reference notes", 2000)
    prompt_override = _bounded(prompt_override, "Prompt override", 10000)
    additional_instructions = _bounded(additional_instructions, "Additional instructions", 2000)
    if aspect_ratio not in RATIOS or detail not in DETAILS or background not in BACKGROUNDS:
        raise ValueError("Invalid image controls")
    workflow = selected["item"]
    prompt = prompt_override or workflow["prompt"]
    lines = [
        "Generate one image using the official imagegen tool, following this selected workflow. This is a request, not a generated image or confirmed result.",
        f"Workflow: {workflow['name']} (ID: {workflow_id}; catalog revision: {selected['revision']})",
        f"Subject: {subject}",
        f"Aspect ratio guidance: {aspect_ratio}. Compose to this ratio where the image tool supports it; inspect the returned dimensions before claiming that the ratio was met.",
        f"Detail guidance: {detail}. Use this as prompt direction, not as an imagegen API parameter.",
        f"Background: {background}." + (" Set imagegen transparent_background=true; verify the returned image has an alpha channel." if background == "Transparent" else " Set imagegen transparent_background=false."),
        "Image direction:\n" + prompt,
    ]
    if reference_notes:
        lines.append("Reference notes (description only; these are not uploaded images):\n" + reference_notes)
    if workflow["reference"] == "required":
        lines.append("A source image is required for this workflow. Check that an image is actually available before generation; if absent, ask the user to attach it and stop. Do not invent or substitute a reference.")
    elif workflow["reference"] == "optional":
        lines.append("If an actual reference image is supplied, use it. Notes alone are not an image upload.")
    lines.append("For actual image references: inspect any local file with view_image before editing and use referenced_image_paths when every target has a local path. Otherwise use the smallest recent conversation image window that includes all targets (maximum five). Never use both mechanisms; if targets cannot all be included, ask for reattachment.")
    if workflow["checks"]:
        lines.append("Review the returned image against these workflow checks:\n" + "\n".join("- " + check for check in workflow["checks"]))
    if additional_instructions:
        lines.append("Additional instructions:\n" + additional_instructions)
    lines.append("After generation, show the image and report only verified properties. A prepared or sent request does not establish generation.")
    return {"schemaVersion": 1, "revision": selected["revision"], "workflowId": workflow_id,
            "status": "prepared", "handoffText": "\n\n".join(lines)}
