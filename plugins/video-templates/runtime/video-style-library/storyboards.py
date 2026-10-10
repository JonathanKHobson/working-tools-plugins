"""Private, revisioned shot-card storyboards for the Video Studio MCP widget."""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
import sqlite3
import textwrap
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

from storyboard_media import MAX_BOARD_BYTES, sketch, reference

DEFAULT_DB = Path(os.environ.get("VIDEO_STORYBOARD_DB", Path.home() / ".local/share/video-production-studio/storyboards.sqlite3")).expanduser()
ID_RE = re.compile(r"^[A-Za-z0-9_-]{1,64}$")
OP_RE = re.compile(r"^[A-Za-z0-9_-]{1,128}$")


class StoryboardError(ValueError):
    def __init__(self, code: str, message: str, current: dict | None = None):
        super().__init__(message)
        self.code = code
        self.current = current


def _title(value: str) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > 200 or any(ord(c) < 32 for c in value):
        raise StoryboardError("invalid_title", "Title must be 1–200 printable characters")
    return value.strip()


def _shots(value: list[dict]) -> list[dict]:
    if not isinstance(value, list) or not 1 <= len(value) <= 20:
        raise StoryboardError("invalid_shots", "Use 1–20 ordered shots")
    clean = []
    seen = set()
    for raw in value:
        if not isinstance(raw, dict) or not {"id", "visual", "duration_seconds", "narration"} <= set(raw) <= {"id", "visual", "duration_seconds", "narration", "sketch", "reference"}:
            raise StoryboardError("invalid_shots", "Shot fields must be id, visual, duration_seconds, narration")
        sid = raw["id"]
        if not isinstance(sid, str) or not ID_RE.fullmatch(sid) or sid in seen:
            raise StoryboardError("invalid_shots", "Shot IDs must be unique and use letters, digits, _ or -")
        seen.add(sid)
        duration = raw["duration_seconds"]
        if isinstance(duration, bool) or not isinstance(duration, (int, float)) or not math.isfinite(duration) or not .5 <= duration <= 600:
            raise StoryboardError("invalid_shots", "Duration must be 0.5–600 seconds")
        visual = raw["visual"]
        narration = raw["narration"]
        if not isinstance(visual, str) or not isinstance(narration, str) or len(visual) > 2000 or len(narration) > 2000:
            raise StoryboardError("invalid_shots", "Visual and narration must be text up to 2000 characters")
        shot = {"id": sid, "visual": visual, "duration_seconds": duration, "narration": narration}
        for field, validate in (("sketch", sketch), ("reference", reference)):
            if field in raw:
                try:
                    shot[field] = validate(raw[field])
                except ValueError as exc:
                    raise StoryboardError("invalid_media", str(exc)) from exc
        clean.append(shot)
    return clean


def _operation(value: str) -> str:
    if not isinstance(value, str) or not OP_RE.fullmatch(value):
        raise StoryboardError("invalid_operation", "Operation ID must use 1–128 letters, digits, _ or -")
    return value


def _board_id(value: str) -> str:
    if not isinstance(value, str):
        raise StoryboardError("invalid_id", "Storyboard ID must be a UUID")
    try:
        if str(uuid.UUID(value)) != value:
            raise ValueError
    except ValueError as exc:
        raise StoryboardError("invalid_id", "Storyboard ID must be a UUID") from exc
    return value


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _canonical(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _board_size(title, shots):
    # Include envelope overhead with maximal stored revision and timestamp lengths.
    envelope = {"storyboard_id": "0" * 36, "title": title, "shots": shots,
                "revision": 9223372036854775807, "updated_at": "0" * 32}
    if len(_canonical(envelope).encode("utf-8")) > MAX_BOARD_BYTES:
        raise StoryboardError("board_too_large", "Encoded storyboard exceeds 8 MiB")


def _revision(value):
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise StoryboardError("invalid_revision", "Expected revision must be a positive integer")
    return value


class StoryboardStore:
    def __init__(self, path: Path | str = DEFAULT_DB, *, create: bool = True):
        self.path = Path(path).expanduser()
        if self.path.is_symlink():
            raise StoryboardError("storage_error", "Storyboard database must not be a symlink")
        if create:
            self.path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
            self._initialize()
        elif not self.path.is_file():
            raise StoryboardError("not_found", "Storyboard was not found")

    @contextmanager
    def _connect(self):
        conn = sqlite3.connect(self.path, timeout=10)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys=ON")
        try:
            with conn:
                yield conn
        finally:
            conn.close()

    def _initialize(self):
        with self._connect() as conn:
            conn.executescript("""
              CREATE TABLE IF NOT EXISTS storyboards (
                id TEXT PRIMARY KEY, title TEXT NOT NULL, revision INTEGER NOT NULL,
                shots TEXT NOT NULL, updated_at TEXT NOT NULL
              );
              CREATE TABLE IF NOT EXISTS operations (
                operation_id TEXT PRIMARY KEY, request_hash TEXT NOT NULL,
                result TEXT NOT NULL
              );
            """)
        try:
            os.chmod(self.path, 0o600)
        except OSError:
            pass

    @staticmethod
    def _decode(row) -> dict:
        return {"storyboard_id": row["id"], "title": row["title"],
                "revision": row["revision"], "shots": json.loads(row["shots"]),
                "updated_at": row["updated_at"]}

    @staticmethod
    def _idempotent(conn, operation_id: str, request: dict) -> dict | None:
        request_hash = hashlib.sha256(_canonical(request).encode()).hexdigest()
        row = conn.execute("SELECT request_hash,result FROM operations WHERE operation_id=?", (operation_id,)).fetchone()
        if row:
            if row["request_hash"] != request_hash:
                raise StoryboardError("operation_conflict", "Operation ID was already used for a different request")
            return json.loads(row["result"])
        return None

    @staticmethod
    def _remember(conn, operation_id: str, request: dict, result: dict):
        request_hash = hashlib.sha256(_canonical(request).encode()).hexdigest()
        conn.execute("INSERT INTO operations(operation_id,request_hash,result) VALUES(?,?,?)",
                     (operation_id, request_hash, _canonical(result)))

    def create(self, title: str, shots: list[dict], operation_id: str) -> dict:
        title, shots, operation_id = _title(title), _shots(shots), _operation(operation_id)
        _board_size(title, shots)
        request = {"method": "create", "title": title, "shots": shots}
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            existing = self._idempotent(conn, operation_id, request)
            if existing:
                return existing
            sid = str(uuid.uuid4())
            now = _now()
            conn.execute("INSERT INTO storyboards VALUES(?,?,?,?,?)", (sid, title, 1, _canonical(shots), now))
            result = {"storyboard_id": sid, "title": title, "revision": 1, "shots": shots, "updated_at": now}
            self._remember(conn, operation_id, request, result)
            return result

    def read(self, storyboard_id: str) -> dict:
        storyboard_id = _board_id(storyboard_id)
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM storyboards WHERE id=?", (storyboard_id,)).fetchone()
        if row is None:
            raise StoryboardError("not_found", "Storyboard was not found")
        return self._decode(row)

    def save(self, storyboard_id: str, expected_revision: int, operation_id: str,
             title: str, shots: list[dict]) -> dict:
        storyboard_id, title, shots, operation_id = _board_id(storyboard_id), _title(title), _shots(shots), _operation(operation_id)
        _revision(expected_revision)
        _board_size(title, shots)
        request = {"method": "save", "storyboard_id": storyboard_id, "expected_revision": expected_revision,
                   "title": title, "shots": shots}
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            existing = self._idempotent(conn, operation_id, request)
            if existing:
                return existing
            row = conn.execute("SELECT * FROM storyboards WHERE id=?", (storyboard_id,)).fetchone()
            if row is None:
                raise StoryboardError("not_found", "Storyboard was not found")
            current = self._decode(row)
            if current["revision"] != expected_revision:
                raise StoryboardError("revision_conflict", "Storyboard changed; reload before saving", current)
            if current["title"] == title and current["shots"] == shots:
                result = current
            else:
                now = _now()
                result = {"storyboard_id": storyboard_id, "title": title,
                          "revision": expected_revision + 1, "shots": shots, "updated_at": now}
                conn.execute("UPDATE storyboards SET title=?, revision=?, shots=?, updated_at=? WHERE id=?",
                             (title, result["revision"], _canonical(shots), now, storyboard_id))
            self._remember(conn, operation_id, request, result)
            return result


    def patch(self, storyboard_id: str, expected_revision: int, operation_id: str,
              operations: list[dict]) -> dict:
        storyboard_id, operation_id = _board_id(storyboard_id), _operation(operation_id)
        _revision(expected_revision)
        if not isinstance(operations, list) or not 1 <= len(operations) <= 40:
            raise StoryboardError("invalid_patch", "Use 1–40 patch operations")
        # Bound the request before canonicalization or storing an idempotency result.
        try:
            encoded = _canonical(operations).encode("utf-8")
        except (TypeError, ValueError) as exc:
            raise StoryboardError("invalid_patch", "Patch must contain JSON values") from exc
        if len(encoded) > MAX_BOARD_BYTES:
            raise StoryboardError("board_too_large", "Encoded patch exceeds 8 MiB")
        request = {"method": "patch", "storyboard_id": storyboard_id,
                   "expected_revision": expected_revision, "operations": operations}
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            existing = self._idempotent(conn, operation_id, request)
            if existing:
                return existing
            row = conn.execute("SELECT * FROM storyboards WHERE id=?", (storyboard_id,)).fetchone()
            if row is None:
                raise StoryboardError("not_found", "Storyboard was not found")
            current = self._decode(row)
            if current["revision"] != expected_revision:
                raise StoryboardError("revision_conflict", "Storyboard changed; reload before patching", current)
            title, shots = current["title"], json.loads(_canonical(current["shots"]))
            def locate(shot_id):
                for index, shot in enumerate(shots):
                    if shot["id"] == shot_id:
                        return index
                raise StoryboardError("invalid_patch", "Target shot ID was not found")
            for operation in operations:
                if not isinstance(operation, dict):
                    raise StoryboardError("invalid_patch", "Each patch operation must be an object")
                op = operation.get("op")
                if op == "update" and set(operation) == {"op", "shot_id", "changes"}:
                    changes = operation["changes"]
                    if not isinstance(changes, dict) or not changes or not set(changes) <= {"visual", "duration_seconds", "narration", "sketch", "reference"}:
                        raise StoryboardError("invalid_patch", "Update changes must use editable shot fields; ID is stable")
                    shot = shots[locate(operation["shot_id"])]
                    for key, value in changes.items():
                        if key in {"sketch", "reference"} and value is None:
                            shot.pop(key, None)
                        else:
                            shot[key] = value
                elif op == "add" and {"op", "shot"} <= set(operation) <= {"op", "shot", "after_shot_id"}:
                    added = _shots([operation["shot"]])[0]
                    index = len(shots) if "after_shot_id" not in operation else (0 if operation["after_shot_id"] is None else locate(operation["after_shot_id"]) + 1)
                    shots.insert(index, added)
                elif op == "remove" and set(operation) == {"op", "shot_id"}:
                    shots.pop(locate(operation["shot_id"]))
                elif op == "reorder" and set(operation) == {"op", "shot_ids"}:
                    ids = operation["shot_ids"]
                    if not isinstance(ids, list) or any(not isinstance(sid, str) for sid in ids) or len(ids) != len(shots) or set(ids) != {shot["id"] for shot in shots}:
                        raise StoryboardError("invalid_patch", "Reorder must include every shot ID exactly once")
                    by_id = {shot["id"]: shot for shot in shots}
                    shots = [by_id[sid] for sid in ids]
                elif op == "title" and set(operation) == {"op", "title"}:
                    title = _title(operation["title"])
                else:
                    raise StoryboardError("invalid_patch", "Unknown patch operation or fields")
                shots = _shots(shots)
            _board_size(title, shots)
            result = current
            if title != current["title"] or shots != current["shots"]:
                now = _now()
                result = {"storyboard_id": storyboard_id, "title": title,
                          "revision": expected_revision + 1, "shots": shots, "updated_at": now}
                conn.execute("UPDATE storyboards SET title=?,revision=?,shots=?,updated_at=? WHERE id=?",
                             (title, result["revision"], _canonical(shots), now, storyboard_id))
            self._remember(conn, operation_id, request, result)
            return result


def draw_payload(storyboard: dict) -> dict:
    """Prepare only: Draw and Think remains the owner of board creation and editing."""
    elements = [{"id": "story_title", "type": "text", "x": 24, "y": 24,
                 "text": storyboard["title"], "fontSize": 30},
                {"id": "story_source", "type": "text", "x": 24, "y": 65,
                 "text": f"Video Studio storyboard {storyboard['storyboard_id']} · revision {storyboard['revision']} · full shot text in Video Studio",
                 "fontSize": 13}]
    def excerpt(value: str) -> str:
        compact = " ".join(value.split()) or "(to author)"
        return compact if len(compact) <= 180 else compact[:177].rstrip() + "…"
    row_y = 100
    for row_start in range(0, len(storyboard["shots"]), 3):
        row_shots = storyboard["shots"][row_start:row_start+3]
        note_texts = []
        for shot in row_shots:
            visual = textwrap.fill(excerpt(shot["visual"]), width=34)
            narration = textwrap.fill(excerpt(shot["narration"]), width=34)
            note_texts.append(f"Visual:\n{visual}\nNarration:\n{narration}")
        row_height = max(400, 285 + max(text.count("\n") + 1 for text in note_texts) * 20)
        for col, (shot, notes) in enumerate(zip(row_shots, note_texts)):
            index = row_start + col
            x, y = 24 + col * 350, row_y
            elements.extend((
                {"id": f"frame_{index+1}", "type": "rectangle", "x": x, "y": y,
                 "width": 320, "height": 210, "backgroundColor": "#f5f3ed"},
                {"id": f"label_{index+1}", "type": "text", "x": x+10, "y": y+225,
                 "text": f"Shot {index+1} · {shot['duration_seconds']:g}s", "fontSize": 19},
                {"id": f"notes_{index+1}", "type": "text", "x": x+10, "y": y+260,
                 "text": notes, "fontSize": 15},
            ))
        row_y += row_height
    return {"title": storyboard["title"], "elements": elements,
            "sourceStoryboardId": storyboard["storyboard_id"], "sourceRevision": storyboard["revision"]}
