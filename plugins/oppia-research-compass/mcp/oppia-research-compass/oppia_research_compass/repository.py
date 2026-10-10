"""Read-only SQLite access for the Oppia historical research corpus."""

from __future__ import annotations

import json
import re
import sqlite3
from pathlib import Path
from typing import Any


TOKEN_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{1,}")
STOPWORDS = {
    "about",
    "and",
    "are",
    "did",
    "for",
    "from",
    "have",
    "how",
    "into",
    "oppia",
    "research",
    "that",
    "the",
    "this",
    "what",
    "when",
    "where",
    "with",
}


def safe_source_ref(relative_path: str | None, *, evidence_id: str | None = None) -> str:
    clean = (relative_path or "unknown-source").replace("\\", "/").lstrip("/")
    ref = f"oppia://research/{clean}"
    return f"{ref}#evidence={evidence_id}" if evidence_id else ref


def _json_list(value: str | None) -> list[str]:
    try:
        parsed = json.loads(value or "[]")
        if isinstance(parsed, list):
            return [str(item) for item in parsed]
    except (TypeError, ValueError):
        pass
    return []


def _fts_query(query: str) -> str:
    tokens = [token.lower() for token in TOKEN_RE.findall(query)]
    useful = [token for token in tokens if token not in STOPWORDS]
    selected = useful or tokens
    return " OR ".join(f'"{token.replace(chr(34), chr(34) * 2)}"' for token in selected[:12])


class OppiaResearchRepository:
    """Query the corpus without exposing machine-local source paths."""

    def __init__(self, db_path: Path) -> None:
        resolved = db_path.expanduser().resolve()
        if not resolved.is_file():
            raise FileNotFoundError(f"Oppia research database not found: {resolved}")
        self.db_path = resolved
        self.connection = sqlite3.connect(
            f"file:{resolved}?mode=ro", uri=True, check_same_thread=False
        )
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA query_only = ON")

    def close(self) -> None:
        self.connection.close()

    def _one(self, sql: str, params: tuple[Any, ...] = ()) -> sqlite3.Row | None:
        return self.connection.execute(sql, params).fetchone()

    def _many(self, sql: str, params: tuple[Any, ...] = ()) -> list[sqlite3.Row]:
        return self.connection.execute(sql, params).fetchall()

    def overview(self) -> dict[str, Any]:
        meta = self._one("SELECT * FROM corpus_meta LIMIT 1")
        integrity = self._one("PRAGMA integrity_check")
        return {
            "corpus": "Oppia historical UX research",
            "snapshot_built_at": meta["built_at"] if meta else None,
            "records": int(meta["records"]) if meta else 0,
            "exported_documents": int(meta["exported_docs"]) if meta else 0,
            "evidence_chunks": int(meta["chunks"]) if meta else 0,
            "interview_records": int(meta["interview_records"]) if meta else 0,
            "qa_chunks": int(meta["qa_chunks"]) if meta else 0,
            "database_integrity": integrity[0] if integrity else "unknown",
            "read_only": True,
            "freshness_note": "This is a historical snapshot; use snapshot_built_at when describing currency.",
        }

    def search(self, query: str, limit: int, offset: int = 0) -> dict[str, Any]:
        text = (query or "").strip()
        if not text:
            return {"query": text, "results": [], "count": 0, "has_more": False, "next_offset": None}
        match = _fts_query(text)
        if not match:
            return {"query": text, "results": [], "count": 0, "has_more": False, "next_offset": None}
        rows = self._many(
            """
            SELECT e.evidence_id, e.record_id, r.title, r.kind, r.sheet,
                   r.doc_id, r.is_interview, r.primary_source_rel_path,
                   e.chunk_type, e.chunk_title, e.section_title,
                   e.question_text, e.respondent_label,
                   bm25(evidence_fts) AS rank_score,
                   snippet(evidence_fts, 2, '[', ']', '...', 22) AS excerpt
            FROM evidence_fts
            JOIN evidence e ON e.evidence_id = evidence_fts.evidence_id
            JOIN records r ON r.record_id = e.record_id
            WHERE evidence_fts MATCH ?
            ORDER BY rank_score, r.title COLLATE NOCASE
            LIMIT ? OFFSET ?
            """,
            (match, limit + 1, max(0, offset)),
        )
        has_more = len(rows) > limit
        selected = rows[:limit]
        return {
            "query": text,
            "results": [self._evidence_summary(row) for row in selected],
            "count": len(selected),
            "has_more": has_more,
            "next_offset": offset + len(selected) if has_more else None,
        }

    def browse_records(
        self,
        limit: int,
        offset: int = 0,
        *,
        query: str | None = None,
        interviews_only: bool = False,
    ) -> dict[str, Any]:
        clauses = ["is_interview = ?"]
        params: list[Any] = [1 if interviews_only else 0]
        if query and query.strip():
            like = f"%{query.strip()}%"
            clauses.append("(title LIKE ? OR preview LIKE ? OR persona_summary LIKE ?)")
            params.extend((like, like, like))
        rows = self._many(
            f"""
            SELECT record_id, kind, title, sheet, row_number, doc_id,
                   primary_source_rel_path, preview, word_count, is_interview,
                   persona_summary, chunk_count, section_count, qa_count,
                   headings_json
            FROM records
            WHERE {' AND '.join(clauses)}
            ORDER BY COALESCE(sheet, ''), COALESCE(row_number, 999999), title COLLATE NOCASE
            LIMIT ? OFFSET ?
            """,
            tuple(params + [limit + 1, max(0, offset)]),
        )
        has_more = len(rows) > limit
        selected = rows[:limit]
        key = "interviews" if interviews_only else "studies"
        return {
            key: [self._record_summary(row) for row in selected],
            "count": len(selected),
            "has_more": has_more,
            "next_offset": offset + len(selected) if has_more else None,
        }

    def get_record(self, record_id: str, evidence_limit: int = 12) -> dict[str, Any] | None:
        row = self._one(
            """
            SELECT record_id, kind, title, sheet, row_number, doc_id,
                   primary_source_rel_path, preview, headings_json, word_count,
                   line_count, char_count, is_interview, persona_summary,
                   chunk_count, section_count, qa_count
            FROM records WHERE record_id = ?
            """,
            (record_id,),
        )
        if row is None:
            return None
        evidence = self._many(
            """
            SELECT evidence_id, record_id, chunk_type, chunk_title,
                   section_title, question_text, respondent_label
            FROM evidence WHERE record_id = ?
            ORDER BY chunk_index LIMIT ?
            """,
            (record_id, max(1, evidence_limit)),
        )
        result = self._record_summary(row)
        result["headings"] = _json_list(row["headings_json"])
        result["line_count"] = int(row["line_count"])
        result["char_count"] = int(row["char_count"])
        result["evidence_index"] = [
            {
                "evidence_id": item["evidence_id"],
                "chunk_type": item["chunk_type"],
                "chunk_title": item["chunk_title"],
                "section_title": item["section_title"],
                "question_text": item["question_text"],
                "respondent_label": item["respondent_label"],
            }
            for item in evidence
        ]
        result["evidence_index_truncated"] = int(row["chunk_count"]) > len(evidence)
        return result

    def get_evidence(self, evidence_id: str, max_chars: int = 25_000) -> dict[str, Any] | None:
        row = self._one(
            """
            SELECT e.evidence_id, e.record_id, r.title, r.kind, r.sheet,
                   r.doc_id, r.is_interview, r.primary_source_rel_path,
                   e.chunk_type, e.chunk_title, e.section_title,
                   e.question_text, e.respondent_label, e.content
            FROM evidence e
            JOIN records r ON r.record_id = e.record_id
            WHERE e.evidence_id = ?
            """,
            (evidence_id,),
        )
        if row is None:
            return None
        content = str(row["content"] or "")
        return {
            "evidence_id": row["evidence_id"],
            "record_id": row["record_id"],
            "record_title": row["title"],
            "record_kind": row["kind"],
            "sheet": row["sheet"],
            "document_id": row["doc_id"],
            "is_interview": bool(row["is_interview"]),
            "chunk_type": row["chunk_type"],
            "chunk_title": row["chunk_title"],
            "section_title": row["section_title"],
            "question_text": row["question_text"],
            "respondent_label": row["respondent_label"],
            "content": content[:max_chars],
            "content_truncated": len(content) > max_chars,
            "source_ref": safe_source_ref(row["primary_source_rel_path"], evidence_id=evidence_id),
        }

    @staticmethod
    def _record_summary(row: sqlite3.Row) -> dict[str, Any]:
        return {
            "record_id": row["record_id"],
            "title": row["title"],
            "kind": row["kind"],
            "sheet": row["sheet"],
            "row_number": row["row_number"],
            "document_id": row["doc_id"],
            "preview": row["preview"],
            "word_count": int(row["word_count"]),
            "is_interview": bool(row["is_interview"]),
            "persona_summary": row["persona_summary"],
            "chunk_count": int(row["chunk_count"]),
            "section_count": int(row["section_count"]),
            "qa_count": int(row["qa_count"]),
            "source_ref": safe_source_ref(row["primary_source_rel_path"]),
        }

    @staticmethod
    def _evidence_summary(row: sqlite3.Row) -> dict[str, Any]:
        return {
            "evidence_id": row["evidence_id"],
            "record_id": row["record_id"],
            "record_title": row["title"],
            "record_kind": row["kind"],
            "sheet": row["sheet"],
            "document_id": row["doc_id"],
            "is_interview": bool(row["is_interview"]),
            "chunk_type": row["chunk_type"],
            "chunk_title": row["chunk_title"],
            "section_title": row["section_title"],
            "question_text": row["question_text"],
            "respondent_label": row["respondent_label"],
            "excerpt": row["excerpt"],
            "rank_score": round(float(row["rank_score"] or 0.0), 6),
            "source_ref": safe_source_ref(row["primary_source_rel_path"], evidence_id=row["evidence_id"]),
        }

