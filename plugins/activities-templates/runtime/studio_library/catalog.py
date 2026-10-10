"""Build and read a private, fixed-domain catalog from the Obsidian vault.

The catalog is a derived snapshot. Search never rebuilds it or writes to the vault.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sqlite3
import sys
import tempfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from atlas_common import COLLECTION_DIRS, slugify


DOMAINS: dict[str, dict[str, Any]] = json.loads(
    (Path(__file__).with_name("domains.json")).read_text(encoding="utf-8")
)
_LINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
_FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", re.DOTALL)
_WORDS = re.compile(r"[\w]+", re.UNICODE)
_WORD_HYPHENS = re.compile(r"(?<=\w)[\-\u2010-\u2015](?=\w)", re.UNICODE)


def _list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(v).strip() for v in value if isinstance(v, (str, int, float)) and str(v).strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


def _text(value: Any) -> str:
    return str(value).strip() if isinstance(value, (str, int, float)) else ""


def _integer(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    try:
        return int(value) if value is not None and str(value).strip() else None
    except (ValueError, TypeError):
        return None


def _duration(value: Any) -> tuple[int | None, int | None]:
    text = _text(value).lower()
    match = re.search(r"(\d+)\s*(?:-|–|to)\s*(\d+)\s*(?:min|minute)", text)
    if match:
        return int(match.group(1)), int(match.group(2))
    match = re.search(r"(\d+)\s*(?:min|minute)", text)
    if match:
        return int(match.group(1)), int(match.group(1))
    return None, None


def _split(raw: str, path: Path) -> tuple[dict[str, Any], str]:
    normalized = raw.replace("\r\n", "\n")
    match = _FRONTMATTER.match(normalized)
    if not match:
        raise ValueError(f"Missing frontmatter: {path}")
    metadata = yaml.safe_load(match.group(1))
    if not isinstance(metadata, dict):
        raise ValueError(f"Frontmatter is not a mapping: {path}")
    return metadata, normalized[match.end():].strip()


def _membership(atlas_id: str, collection: str, metadata: dict[str, Any]) -> dict[str, str]:
    cats = {value.casefold() for value in _list(metadata.get("categories"))}
    group = _text(metadata.get("browse_group")).casefold()
    hits = {}
    for domain, config in DOMAINS.items():
        rule = config.get("collections", {}).get(collection)
        if not isinstance(rule, dict):
            continue
        if rule.get("all") is True:
            hits[domain] = "collection"
            continue
        if atlas_id in rule.get("ids", []):
            hits[domain] = "explicit_id"
            continue
        matched = sorted(cats.intersection(str(x).casefold() for x in rule.get("categories", [])))
        if matched:
            hits[domain] = "category:" + matched[0]
        elif group and group in {str(x).casefold() for x in rule.get("groups", [])}:
            hits[domain] = "browse_group:" + group
    return hits


def _summary(metadata: dict[str, Any], body: str) -> str:
    for key in ("objective", "definition", "summary"):
        value = _text(metadata.get(key))
        if value:
            return value[:500]
    match = re.search(r"^##\s+(?:Definition|Summary|Objective)\s*\n(.*?)(?=^##\s+|\Z)", body, re.I | re.M | re.S)
    if match:
        return re.sub(r"\s+", " ", match.group(1)).strip()[:500]
    for line in body.splitlines():
        line = re.sub(r"^[#>*\-\s]+", "", line).strip()
        if line:
            return line[:500]
    return ""


def _read_record(vault: Path, collection: str, path: Path) -> tuple[dict[str, Any], list[str], dict[str, str]]:
    raw_bytes = path.read_bytes()
    raw = raw_bytes.decode("utf-8")
    metadata, body = _split(raw, path)
    relative = path.relative_to(vault).as_posix()
    source_slug = slugify(metadata.get("source_slug") or metadata.get("slug") or path.stem)
    # Match the Atlas ID convention, including File-O-Fun expansion slugs.
    atlas_id = f"{collection}:{source_slug}"
    category = _text(metadata.get("browse_group") or metadata.get("category"))
    duration_min, duration_max = _duration(metadata.get("timebox") or metadata.get("duration_estimate"))
    activity = None
    if collection == "file-o-fun":
        activity = {
            "players_min": _integer(metadata.get("players_min")),
            "players_max": _integer(metadata.get("players_max")),
            "duration_minutes_min": duration_min,
            "duration_minutes_max": duration_max,
            "delivery_mode": _text(metadata.get("delivery_mode")),
            "energy": _text(metadata.get("energy_level")),
            "interaction": _text(metadata.get("interaction_pattern")),
        }
    status = _text(metadata.get("status")) or "unknown"
    record = {
        "id": atlas_id,
        "title": _text(metadata.get("title")) or path.stem,
        "collection": collection,
        "category": category,
        "summary": _summary(metadata, body),
        "body": body,
        "source_path": str(path),
        "source_hash": hashlib.sha256(raw_bytes).hexdigest(),
        "status": status,
        "readiness": "not_ready" if status == "unusable" else "review_before_use" if collection == "file-o-fun" else "source_reference",
        "provenance": {
            "canonical_path": _text(metadata.get("canonical_path")) or relative,
            "source_id": _text(metadata.get("source_id") or metadata.get("id")),
            "source_slug": source_slug,
            "source_file": _text(metadata.get("source_file") or metadata.get("source")),
            "original_source_path": _text(metadata.get("source_path")),
            "review_flags": _list(metadata.get("review_flags")),
        },
        "tags": _list(metadata.get("tags")),
        "aliases": _list(metadata.get("aliases")),
        "activity": activity,
    }
    links = _list(metadata.get("related")) + _LINK.findall(body)
    return record, links, _membership(atlas_id, collection, metadata)


def _resolve_link(link: str, paths: dict[str, str], stems: dict[str, list[str]]) -> str | None:
    link = _LINK.sub(lambda match: match.group(1), link).split("|", 1)[0].split("#", 1)[0].strip()
    key = link.removesuffix(".md") + ".md"
    if key in paths:
        return paths[key]
    candidates = stems.get(Path(key).stem, [])
    return candidates[0] if len(candidates) == 1 else None


def build_index(vault: Path, db: Path) -> dict[str, Any]:
    """Create a complete snapshot in a temporary SQLite file, then replace atomically."""
    vault = Path(vault).resolve(strict=True)
    db = Path(db).expanduser().resolve()
    if db.is_relative_to(vault) or db.suffix != ".sqlite":
        raise ValueError("Derived index must be a .sqlite file outside the canonical vault")
    if db.exists():
        try:
            with sqlite3.connect(db.as_uri() + "?mode=ro", uri=True) as existing:
                marker = existing.execute("SELECT value FROM meta WHERE key='catalog_type'").fetchone()
            if marker != ("studio-library-v1",):
                raise ValueError("Refusing to overwrite a file not marked as a derived studio library")
        except sqlite3.Error as exc:
            raise ValueError("Refusing to overwrite an unrelated file") from exc
    db.parent.mkdir(parents=True, exist_ok=True)
    records: dict[str, dict[str, Any]] = {}
    membership: dict[str, dict[str, str]] = {}
    raw_links: dict[str, list[str]] = {}
    paths: dict[str, str] = {}
    stems: dict[str, list[str]] = defaultdict(list)
    skipped: list[dict[str, str]] = []
    for collection, directory in COLLECTION_DIRS.items():
        entry_dir = vault / directory
        if not entry_dir.is_dir():
            continue
        for path in sorted(entry_dir.rglob("*.md")):
            if path.name.startswith("._") or not path.resolve().is_relative_to(vault):
                continue
            try:
                record, links, domains = _read_record(vault, collection, path)
            except (OSError, UnicodeError, yaml.YAMLError, ValueError) as exc:
                skipped.append({"path": str(path), "error": str(exc)[:200]})
                continue
            atlas_id = record["id"]
            if atlas_id in records:
                skipped.append({"path": str(path), "error": f"duplicate id: {atlas_id}"})
                continue
            records[atlas_id] = record
            membership[atlas_id] = domains
            raw_links[atlas_id] = links
            relative = path.relative_to(vault).as_posix()
            paths[relative] = atlas_id
            stems[path.stem].append(atlas_id)
    related: dict[str, list[str]] = {}
    for atlas_id, links in raw_links.items():
        related[atlas_id] = sorted({target for link in links if (target := _resolve_link(link, paths, stems)) and target != atlas_id})
    built_at = datetime.now(timezone.utc).isoformat()
    fd, temporary = tempfile.mkstemp(prefix=db.name + ".", suffix=".tmp", dir=db.parent)
    os.close(fd)
    try:
        connection = sqlite3.connect(temporary)
        with connection:
            connection.executescript("""
                CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
                CREATE TABLE items (id TEXT PRIMARY KEY, title TEXT NOT NULL, collection TEXT NOT NULL,
                    category TEXT NOT NULL, status TEXT NOT NULL, body TEXT NOT NULL, payload TEXT NOT NULL);
                CREATE TABLE membership (domain TEXT NOT NULL, item_id TEXT NOT NULL, reason TEXT NOT NULL,
                    PRIMARY KEY(domain,item_id));
                CREATE TABLE links (source_id TEXT NOT NULL, target_id TEXT NOT NULL,
                    PRIMARY KEY(source_id,target_id));
                CREATE VIRTUAL TABLE item_fts USING fts5(title, summary, tags, aliases, body, content='');
                CREATE INDEX membership_by_item ON membership(item_id);
                CREATE INDEX items_filter ON items(collection,category,status);
            """)
            connection.execute("INSERT INTO meta VALUES (?,?)", ("catalog_type", "studio-library-v1"))
            connection.execute("INSERT INTO meta VALUES (?,?)", ("built_at", built_at))
            connection.execute("INSERT INTO meta VALUES (?,?)", ("source_count", str(len(records))))
            connection.execute("INSERT INTO meta VALUES (?,?)", ("vault_path", str(vault)))
            for rowid, (atlas_id, record) in enumerate(sorted(records.items()), 1):
                connection.execute("INSERT INTO items(rowid,id,title,collection,category,status,body,payload) VALUES (?,?,?,?,?,?,?,?)",
                                   (rowid, atlas_id, record["title"], record["collection"], record["category"], record["status"], record["body"], json.dumps(record, ensure_ascii=False)))
                connection.execute("INSERT INTO item_fts(rowid,title,summary,tags,aliases,body) VALUES (?,?,?,?,?,?)",
                                   (rowid, record["title"], record["summary"], " ".join(record["tags"]), " ".join(record["aliases"]), record["body"]))
                for domain, reason in membership[atlas_id].items():
                    connection.execute("INSERT INTO membership VALUES (?,?,?)", (domain, atlas_id, reason))
                for target in related[atlas_id]:
                    connection.execute("INSERT INTO links VALUES (?,?)", (atlas_id, target))
        connection.close()
        os.replace(temporary, db)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    counts = dict(Counter(domain for domains in membership.values() for domain in domains))
    return {"built_at": built_at, "source_count": len(records), "domain_counts": counts,
            "unassigned_count": sum(not domains for domains in membership.values()), "skipped": skipped, "db_path": str(db)}


class Catalog:
    def __init__(self, db: Path, domain: str):
        if domain not in DOMAINS:
            raise ValueError(f"Unknown domain: {domain}")
        self.db = Path(db)
        self.domain = domain
        with self._connect() as conn:
            self.vault = Path(conn.execute("SELECT value FROM meta WHERE key='vault_path'").fetchone()[0]).resolve(strict=True)

    def _connect(self) -> sqlite3.Connection:
        uri = self.db.resolve(strict=True).as_uri() + "?mode=ro"
        connection = sqlite3.connect(uri, uri=True)
        connection.row_factory = sqlite3.Row
        return connection

    def status(self) -> dict[str, Any]:
        with self._connect() as conn:
            metadata = dict(conn.execute("SELECT key,value FROM meta"))
            rows = conn.execute("SELECT i.payload FROM membership m JOIN items i ON i.id=m.item_id WHERE m.domain=?", (self.domain,)).fetchall()
        states = Counter(self._source_state(json.loads(row["payload"])) for row in rows)
        return {"domain": self.domain, "built_at": metadata["built_at"],
                "source_count": int(metadata["source_count"]), "domain_count": len(rows),
                "source_state_counts": dict(states), "stale_count": states["changed"] + states["missing"] + states["invalid"],
                "vault_path": metadata["vault_path"], "db_path": str(self.db)}

    def _source_state(self, item: dict[str, Any]) -> str:
        try:
            source = Path(item["source_path"]).resolve(strict=True)
            if not source.is_relative_to(self.vault):
                return "invalid"
            digest = hashlib.sha256(source.read_bytes()).hexdigest()
        except OSError:
            return "missing"
        return "current" if digest == item["source_hash"] else "changed"

    def _item(self, conn: sqlite3.Connection, row: sqlite3.Row) -> dict[str, Any]:
        result = json.loads(row["payload"])
        result["reason"] = row["reason"]
        result["source_state"] = self._source_state(result)
        result["related"] = [dict(target) for target in conn.execute(
            "SELECT i.id,i.title FROM links l JOIN membership m ON m.item_id=l.target_id AND m.domain=? "
            "JOIN items i ON i.id=l.target_id WHERE l.source_id=? ORDER BY i.title LIMIT 20",
            (self.domain, result["id"]),
        )]
        return result

    def get(self, id: str) -> dict[str, Any]:
        with self._connect() as conn:
            row = conn.execute("SELECT i.payload,m.reason FROM items i JOIN membership m ON m.item_id=i.id "
                               "WHERE m.domain=? AND i.id=?", (self.domain, id)).fetchone()
            if row is None:
                raise KeyError("Entry is not available in this domain")
            return self._item(conn, row)

    def search(self, query: str = "", collection: str = "", category: str = "", status: str = "",
               limit: int = 20, offset: int = 0, participants: int | None = None,
               minutes: int | None = None, mode: str = "", include_unknown: bool = False) -> dict[str, Any]:
        limit = max(1, min(int(limit), 100))
        offset = max(0, int(offset))
        conditions = ["m.domain=?"]
        params: list[Any] = [self.domain]
        for column, value in (("collection", collection), ("category", category), ("status", status)):
            if value:
                conditions.append(f"i.{column}=?")
                params.append(value)
        tokens = _WORDS.findall(query)[:12]
        joins = ""
        order = "i.title COLLATE NOCASE"
        if tokens:
            expression = " AND ".join('"' + token.replace('"', '') + '"*' for token in tokens)
            compact_tokens = _WORDS.findall(_WORD_HYPHENS.sub("", query))[:12]
            if compact_tokens != tokens:
                compact_expression = " AND ".join('"' + token.replace('"', '') + '"*' for token in compact_tokens)
                expression = f"({expression}) OR ({compact_expression})"
            joins = " JOIN item_fts ON item_fts.rowid=i.rowid"
            conditions.append("item_fts MATCH ?")
            params.append(expression)
            order = "bm25(item_fts, 8.0, 4.0, 2.0, 2.0, 1.0), i.title COLLATE NOCASE"
        if participants is not None or minutes is not None or mode:
            conditions.append("i.collection='file-o-fun'")
            if participants is not None:
                if int(participants) <= 0:
                    raise ValueError("participants must be positive")
                conditions.append("(" + ("json_extract(i.payload,'$.activity.players_min') IS NULL OR " if include_unknown else "") + "json_extract(i.payload,'$.activity.players_min')<=?)")
                params.append(int(participants))
                conditions.append("(" + ("json_extract(i.payload,'$.activity.players_max') IS NULL OR " if include_unknown else "") + "json_extract(i.payload,'$.activity.players_max')>=?)")
                params.append(int(participants))
            if minutes is not None:
                if int(minutes) <= 0:
                    raise ValueError("minutes must be positive")
                conditions.append("(" + ("json_extract(i.payload,'$.activity.duration_minutes_max') IS NULL OR " if include_unknown else "") + "json_extract(i.payload,'$.activity.duration_minutes_max')<=?)")
                params.append(int(minutes))
            if mode:
                conditions.append("LOWER(json_extract(i.payload,'$.activity.delivery_mode'))=LOWER(?)")
                params.append(mode)
        where = " AND ".join(conditions)
        with self._connect() as conn:
            base = f"FROM membership m JOIN items i ON i.id=m.item_id{joins} WHERE {where}"
            total = conn.execute(f"SELECT COUNT(*) {base}", params).fetchone()[0]
            rows = conn.execute(f"SELECT i.payload,m.reason {base} ORDER BY {order} LIMIT ? OFFSET ?", params + [limit, offset]).fetchall()
            items = [self._item(conn, row) for row in rows]
        return {"domain": self.domain, "items": items, "total": total, "limit": limit, "offset": offset}

    def export(self) -> dict[str, Any]:
        with self._connect() as conn:
            metadata = dict(conn.execute("SELECT key,value FROM meta"))
            rows = conn.execute("SELECT i.payload,m.reason FROM items i JOIN membership m ON m.item_id=i.id "
                                "WHERE m.domain=? ORDER BY i.title COLLATE NOCASE", (self.domain,)).fetchall()
            items = [self._item(conn, row) for row in rows]
        config = DOMAINS[self.domain]
        return {"domain": {"id": self.domain, "title": config["title"], "description": config["description"]},
                "built_at": metadata["built_at"], "source_count": int(metadata["source_count"]), "items": items}
