"""Read-only local delivery preflight; no upload, approval or publication capability."""
from __future__ import annotations

import json
import math
import re
from pathlib import Path
from typing import Any

from PIL import Image, ImageOps

from .probe import probe_media
from .utils import sha256_file


class DeliveryError(ValueError):
    """The local delivery contract is malformed."""


_HASH = re.compile(r"[a-f0-9]{64}\Z")
_ROLES = {"render", "captions", "transcript", "cover", "courseCard"}
_REQUIRED_ROLES = _ROLES - {"courseCard"}
_REVIEWS = {"visual": {"render"}, "captions": {"render", "captions"},
            "transcript": {"render", "transcript"}, "cover": {"cover"}, "audio": {"render"}}
_FILE_FIELDS = {"path", "sha256", "width", "height", "minWidth", "minHeight",
                "maxBytes", "durationSeconds", "aspectRatio", "renderSha256", "requireAudio"}


def _fingerprint(path: Path) -> tuple[int, int, int]:
    stat = path.stat()
    return stat.st_size, stat.st_mtime_ns, stat.st_ctime_ns


def _positive(value: Any, *, integer: bool = False) -> bool:
    return (type(value) in ((int,) if integer else (int, float))
            and math.isfinite(value) and value > 0)


def preflight_delivery(manifest_path: str | Path) -> dict[str, Any]:
    """Aggregate missing/stale artifacts without modifying inputs or generating media.

    Review records are creator attestations. Fresh hash bindings verify which bytes
    were reviewed; this function cannot perform or prove the underlying review.
    Hashes/probes are reused only within this invocation, never from stale disk caches.
    """
    manifest_path = Path(manifest_path).resolve()
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError) as exc:
        raise DeliveryError(f"cannot read delivery manifest: {exc}") from exc
    if (not isinstance(manifest, dict) or type(manifest.get("schemaVersion")) is not int
            or manifest["schemaVersion"] != 1 or not isinstance(manifest.get("items"), list)
            or not manifest["items"]):
        raise DeliveryError("delivery manifest requires schemaVersion 1 and nonempty items")
    ids: set[str] = set()
    for item in manifest["items"]:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str) or not item["id"].strip():
            raise DeliveryError("each delivery requires a nonblank local id")
        if item["id"] in ids:
            raise DeliveryError(f"duplicate local delivery id: {item['id']}")
        ids.add(item["id"])
        if item.get("format") not in {"portrait", "landscape"} or not isinstance(item.get("files"), dict):
            raise DeliveryError(f"{item['id']}: requires portrait/landscape format and files object")

    cache: dict[tuple[Path, str], dict[str, Any]] = {}
    fingerprints: dict[tuple[Path, str], tuple[int, int, int]] = {}
    rows = []
    for item in manifest["items"]:
        issues: list[dict[str, str]] = []
        files: dict[str, Any] = {}
        actions: list[str] = []

        def issue(code: str, role: str, message: str, action: str) -> None:
            issues.append({"code": code, "role": role, "message": message})
            if action not in actions:
                actions.append(action)

        for role in sorted(_REQUIRED_ROLES | item["files"].keys()):
            spec = item["files"].get(role)
            if role not in _ROLES:
                issue("unknown-role", role, "Unknown delivery role; check the contract.", f"Correct {role} role.")
                continue
            if not isinstance(spec, dict) or not isinstance(spec.get("path"), str) or not spec["path"].strip():
                issue("missing-artifact", role, "Required file record/path is missing.", f"Prepare {role}.")
                continue
            if spec.keys() - _FILE_FIELDS:
                issue("unknown-field", role, f"Unknown file fields: {sorted(spec.keys() - _FILE_FIELDS)}", f"Correct {role} expectations.")
            path = (manifest_path.parent / spec["path"]).resolve()
            if not path.is_file():
                issue("missing-file", role, f"File not found: {path}", f"Prepare {role}.")
                continue
            kind = "video" if role == "render" else "image" if role in {"cover", "courseCard"} else "text"
            key = (path, kind)
            try:
                if key not in cache:
                    before = path.stat()
                    actual: dict[str, Any] = {"path": str(path), "sha256": sha256_file(path), "bytes": before.st_size}
                    if kind == "video":
                        probe = probe_media(path)
                        if not probe.get("video"):
                            raise ValueError("no video stream")
                        actual.update(width=probe["video"]["width"], height=probe["video"]["height"],
                                      durationSeconds=probe["format"]["duration"], audioPresent=bool(probe.get("audio")))
                        if not all(_positive(actual[k], integer=k != "durationSeconds") for k in ("width", "height", "durationSeconds")):
                            raise ValueError("invalid probed dimensions or duration")
                    elif kind == "image":
                        with Image.open(path) as im:
                            im.load()
                            width, height = ImageOps.exif_transpose(im).size
                            actual.update(width=width, height=height)
                    else:
                        if not path.read_text(encoding="utf-8-sig").strip():
                            raise ValueError("empty text artifact")
                    after = path.stat()
                    if (before.st_size, before.st_mtime_ns, before.st_ctime_ns) != (after.st_size, after.st_mtime_ns, after.st_ctime_ns):
                        raise ValueError("file changed during inspection; rerun after writing finishes")
                    if not actual["bytes"]:
                        raise ValueError("empty artifact")
                    cache[key] = actual
                    fingerprints[key] = (after.st_size, after.st_mtime_ns, after.st_ctime_ns)
                files[role] = dict(cache[key])
                # Detect a shared file changed after its first inspection in this batch.
                if _fingerprint(path) != fingerprints[key]:
                    raise ValueError("file changed during batch; rerun")
            except Exception as exc:
                issue("inspection-failed", role, str(exc), f"Repair or inspect {role}.")
                continue

            expected_hash = spec.get("sha256")
            if not isinstance(expected_hash, str) or not _HASH.fullmatch(expected_hash):
                issue("missing-hash", role, "Expected lowercase SHA-256 is missing or malformed.", f"Record reviewed {role} hash.")
            elif expected_hash != files[role]["sha256"]:
                issue("hash-mismatch", role, "Actual bytes differ from the expected delivery.", f"Reconcile changed {role} and invalidate dependent reviews.")
            if "requireAudio" in spec:
                if role != "render" or type(spec["requireAudio"]) is not bool:
                    issue("invalid-expectation", role, "requireAudio is a boolean for render files only.", f"Correct {role} expectations.")
                elif spec["requireAudio"] and not files[role]["audioPresent"]:
                    issue("missing-audio", role, "Expected audio stream is absent.", "Restore and review the intended audio stream.")
            for field in ("width", "height", "minWidth", "minHeight", "maxBytes", "durationSeconds"):
                if field not in spec:
                    continue
                if not _positive(spec[field], integer=field != "durationSeconds"):
                    issue("invalid-expectation", role, f"{field} must be positive and finite.", f"Correct {role} expectations.")
                    continue
                value = spec[field]
                if field == "maxBytes" and files[role]["bytes"] > value:
                    issue("size-exceeded", role, "File exceeds the declared destination byte limit.", f"Conform {role} to the declared byte limit.")
                elif field in {"width", "height"} and files[role].get(field) != value:
                    issue("dimensions-mismatch", role, f"Actual {field} differs from declared dimensions.", f"Conform {role} dimensions.")
                elif field in {"minWidth", "minHeight"} and files[role].get(field[3:].lower(), 0) < value:
                    issue("dimensions-too-small", role, "File is below the explicit minimum dimensions.", f"Conform {role} dimensions.")
                elif field == "durationSeconds" and abs(files[role].get(field, 0) - value) > 0.25:
                    issue("duration-mismatch", role, "Probed duration differs by more than 250ms.", f"Reconcile {role} duration and caption timing.")
            if kind in {"video", "image"}:
                default_ratio = [1, 1] if role == "courseCard" else [9, 16] if item["format"] == "portrait" else [16, 9]
                ratio = spec.get("aspectRatio", default_ratio)
                if (not isinstance(ratio, list) or len(ratio) != 2
                        or not all(_positive(v, integer=True) for v in ratio)):
                    issue("invalid-expectation", role, "aspectRatio requires two positive integers.", f"Correct {role} aspect ratio.")
                elif abs((files[role]["width"] / files[role]["height"]) / (ratio[0] / ratio[1]) - 1) > 0.01:
                    issue("aspect-mismatch", role, "Actual aspect differs by more than 1% from the delivery target.", f"Prepare the appropriate {role} aspect variant.")

        render_hash = files.get("render", {}).get("sha256")
        for role in ("captions", "transcript"):
            spec = item["files"].get(role, {})
            if not isinstance(spec, dict) or not render_hash or spec.get("renderSha256") != render_hash:
                code = "caption-render-mismatch" if role == "captions" else "transcript-render-mismatch"
                issue(code, role, "Text artifact is not bound to the current final render.", f"Review {role} against the final render and record its hash.")
        files_passed = not issues
        reviews = item.get("reviews", {})
        if not isinstance(reviews, dict):
            raise DeliveryError(f"{item['id']}: reviews must be an object")
        review_states = {}
        for kind, required_roles in _REVIEWS.items():
            if kind == "cover" and "courseCard" in item["files"]:
                required_roles = required_roles | {"courseCard"}
            review = reviews.get(kind, {})
            if not isinstance(review, dict) or review.get("status") != "passed" or not isinstance(review.get("evidence"), str) or not review["evidence"].strip():
                review_states[kind] = "held" if isinstance(review, dict) and review.get("status") == "held" else "pending"
                issue("review-pending", kind, "No completed review attestation with evidence.", f"Complete {kind} review or retain its explicit hold.")
                continue
            hashes = review.get("hashes", {})
            if (not isinstance(hashes, dict) or not required_roles <= hashes.keys()
                    or any(not files.get(role) or files[role]["sha256"] != digest for role, digest in hashes.items())):
                review_states[kind] = "stale"
                issue("stale-review", kind, "Review hashes do not match all required current artifacts.", f"Reconcile and repeat {kind} review for changed artifacts.")
            else:
                review_states[kind] = "fresh-attestation"
        rows.append({"id": item["id"], "files": files, "filesPassed": files_passed,
                     "reviews": review_states, "localHandoffReady": not issues,
                     "issues": issues, "nextActions": actions})
    # A later item may reveal an in-progress write to a shared earlier artifact.
    # Do not leave any affected earlier row marked ready in the final report.
    for row in rows:
        for role, actual in row["files"].items():
            kind = "video" if role == "render" else "image" if role in {"cover", "courseCard"} else "text"
            path = Path(actual["path"])
            try:
                fresh = _fingerprint(path) == fingerprints.get((path, kind))
            except OSError:
                fresh = False
            if not fresh:
                row["filesPassed"] = row["localHandoffReady"] = False
                row["issues"].append({"code": "changed-during-batch", "role": role,
                                      "message": "Artifact changed or disappeared before the batch finished."})
                row["nextActions"].append(f"Rerun after {role} stops changing.")
    return {"schemaVersion": 1, "passed": all(r["localHandoffReady"] for r in rows),
            "summary": {"items": len(rows), "ready": sum(r["localHandoffReady"] for r in rows),
                        "filesPassed": sum(r["filesPassed"] for r in rows)}, "items": rows,
            "boundary": "Local files and freshness of review attestations only; no audiovisual approval, caption-speech alignment, native crop, upload, saved state, or publication verification."}
