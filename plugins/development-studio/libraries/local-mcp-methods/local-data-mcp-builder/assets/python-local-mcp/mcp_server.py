#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from contracts import budget_definitions, clamp_limit, estimate_json_chars, get_budget

READ_ONLY = ToolAnnotations(
    readOnlyHint=True,
    destructiveHint=False,
    idempotentHint=True,
    openWorldHint=False,
)


class Repository:
    def __init__(self, db_path: Path) -> None:
        self.connection = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA query_only = ON")

    def _build_info(self) -> dict[str, Any]:
        rows = self.connection.execute("SELECT key, value FROM build_info ORDER BY key").fetchall()
        result: dict[str, Any] = {}
        for row in rows:
            try:
                result[row["key"]] = json.loads(row["value"])
            except json.JSONDecodeError:
                result[row["key"]] = row["value"]
        return result

    def overview(self) -> dict[str, Any]:
        record_count = self.connection.execute("SELECT COUNT(*) FROM records").fetchone()[0]
        evidence_count = self.connection.execute("SELECT COUNT(*) FROM evidence").fetchone()[0]
        lens_card_count = self.connection.execute("SELECT COUNT(*) FROM lens_cards").fetchone()[0]
        return {
            "record_count": record_count,
            "evidence_count": evidence_count,
            "lens_card_count": lens_card_count,
            "build_info": self._build_info(),
        }

    def list_records(self, limit: int, budget_mode: str = "standard") -> dict[str, Any]:
        budget = get_budget(budget_mode)
        bounded_limit = clamp_limit(limit, budget.max_results, 20)
        rows = self.connection.execute(
            "SELECT record_id, title, preview FROM records ORDER BY title ASC LIMIT ?",
            (bounded_limit,),
        ).fetchall()
        records = [dict(row) for row in rows]
        return {
            "records": records,
            "trace": {
                "budget_mode": budget.mode,
                "requested_limit": limit,
                "effective_limit": bounded_limit,
                "returned_count": len(records),
                "context_chars": estimate_json_chars(records),
            },
        }

    def retrieve_lens_cards(self, query: str, budget_mode: str = "standard") -> dict[str, Any]:
        budget = get_budget(budget_mode)
        tokens = [token for token in query.lower().replace("-", " ").split() if token]
        fts_query = " OR ".join(f"{token}*" for token in tokens[:8])
        if not fts_query:
            return {"query": query, "lens_cards": [], "trace": {"budget_mode": budget.mode, "returned_count": 0}}
        rows = self.connection.execute(
            """
            SELECT lc.*, snippet(lens_cards_fts, 3, '[', ']', ' ... ', 24) AS snippet
            FROM lens_cards_fts
            JOIN lens_cards lc ON lc.lens_id = lens_cards_fts.lens_id
            WHERE lens_cards_fts MATCH ?
            ORDER BY bm25(lens_cards_fts) ASC, lc.name ASC
            LIMIT ?
            """,
            (fts_query, budget.max_lens_cards),
        ).fetchall()
        cards = [
            {
                "lens_id": row["lens_id"],
                "record_id": row["record_id"],
                "name": row["name"],
                "summary": row["summary_short"],
                "representation": row["representation_short"],
                "misuse_warning": row["misuse_warning"],
                "snippet": row["snippet"],
            }
            for row in rows
        ]
        return {
            "query": query,
            "lens_cards": cards,
            "trace": {
                "budget_mode": budget.mode,
                "returned_count": len(cards),
                "max_lens_cards": budget.max_lens_cards,
                "context_chars": estimate_json_chars(cards),
            },
        }


def build_server(repository: Repository) -> FastMCP:
    server = FastMCP(name="example-local-data", instructions="Starter local read-only MCP.", log_level="ERROR")

    @server.tool(description="Return high-level index stats.", annotations=READ_ONLY, structured_output=True)
    def get_overview() -> dict[str, Any]:
        return repository.overview()

    @server.tool(description="List indexed records with a retrieval budget cap.", annotations=READ_ONLY, structured_output=True)
    def list_records(limit: int = 20, budget_mode: str = "standard") -> dict[str, Any]:
        return repository.list_records(limit, budget_mode)

    @server.tool(description="Retrieve compact operational lens cards from the local index.", annotations=READ_ONLY, structured_output=True)
    def retrieve_lens_cards(query: str, budget_mode: str = "standard") -> dict[str, Any]:
        return repository.retrieve_lens_cards(query, budget_mode)

    return server


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the starter local-data MCP.")
    parser.add_argument("--db-path", required=True, help="SQLite DB path.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    repository = Repository(Path(args.db_path).expanduser())
    server = build_server(repository)
    server.run(transport="stdio")


if __name__ == "__main__":
    main()
