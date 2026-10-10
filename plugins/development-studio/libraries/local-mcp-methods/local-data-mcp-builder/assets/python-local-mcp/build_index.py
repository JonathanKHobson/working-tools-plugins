#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from contracts import budget_definitions


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a local SQLite index for a data-backed MCP.")
    parser.add_argument("--root", required=True, help="Root folder for the source data.")
    parser.add_argument("--db-path", required=True, help="Output SQLite DB path.")
    return parser.parse_args()


def create_schema(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        CREATE TABLE records (
          record_id TEXT PRIMARY KEY,
          title TEXT NOT NULL,
          preview TEXT NOT NULL
        );

        CREATE TABLE evidence (
          evidence_id TEXT PRIMARY KEY,
          record_id TEXT NOT NULL,
          search_text TEXT NOT NULL,
          FOREIGN KEY (record_id) REFERENCES records (record_id) ON DELETE CASCADE
        );

        CREATE VIRTUAL TABLE evidence_fts USING fts5(
          evidence_id UNINDEXED,
          record_id UNINDEXED,
          search_text,
          tokenize = 'unicode61'
        );

        CREATE TABLE lens_cards (
          lens_id TEXT PRIMARY KEY,
          record_id TEXT NOT NULL UNIQUE,
          name TEXT NOT NULL,
          summary_short TEXT NOT NULL,
          representation_short TEXT NOT NULL,
          representation_standard TEXT NOT NULL,
          use_when_json TEXT NOT NULL,
          do_not_use_when_json TEXT NOT NULL,
          misuse_warning TEXT NOT NULL,
          token_budget_json TEXT NOT NULL,
          FOREIGN KEY (record_id) REFERENCES records (record_id) ON DELETE CASCADE
        );

        CREATE VIRTUAL TABLE lens_cards_fts USING fts5(
          lens_id UNINDEXED,
          record_id UNINDEXED,
          name,
          search_text,
          tokenize = 'unicode61'
        );

        CREATE TABLE build_info (
          key TEXT PRIMARY KEY,
          value TEXT NOT NULL
        );
        """
    )


def to_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def build_index(root: Path, db_path: Path) -> None:
    temp_path = db_path.with_suffix(f"{db_path.suffix}.tmp")
    if temp_path.exists():
        temp_path.unlink()

    connection = sqlite3.connect(temp_path)
    try:
        create_schema(connection)

        # TODO: Replace this placeholder logic with real parsing over local artifacts.
        connection.execute(
            "INSERT INTO records (record_id, title, preview) VALUES (?, ?, ?)",
            ("example-record", "Example Record", "Replace this with real metadata."),
        )
        connection.execute(
            "INSERT INTO evidence (evidence_id, record_id, search_text) VALUES (?, ?, ?)",
            ("example-evidence", "example-record", "Replace this with real full-text content."),
        )
        connection.execute(
            "INSERT INTO evidence_fts (evidence_id, record_id, search_text) VALUES (?, ?, ?)",
            ("example-evidence", "example-record", "Replace this with real full-text content."),
        )
        connection.execute(
            """
            INSERT INTO lens_cards (
              lens_id, record_id, name, summary_short, representation_short,
              representation_standard, use_when_json, do_not_use_when_json,
              misuse_warning, token_budget_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "lens.example.example-record.v1",
                "example-record",
                "Example Record",
                "Replace this with a compact generated summary.",
                "Example Record: compact operational card.",
                "Use this card as a placeholder for retrieval-hardening template work.",
                to_json(["The query matches this source record."]),
                to_json(["A narrower source record is available."]),
                "Generated starter lens; replace with source-grounded guidance.",
                to_json({"short": 80, "standard": 220, "full": 700}),
            ),
        )
        connection.execute(
            "INSERT INTO lens_cards_fts (lens_id, record_id, name, search_text) VALUES (?, ?, ?, ?)",
            ("lens.example.example-record.v1", "example-record", "Example Record", "Example Record compact operational card."),
        )
        build_info = {
            "built_at": now_iso(),
            "source_root": str(root),
            "db_version": 1,
            "record_count": 1,
            "evidence_count": 1,
            "lens_card_count": 1,
            "budget_definitions": budget_definitions(),
            "chroma": {"available": False, "skipped": True},
        }
        for key, value in build_info.items():
            connection.execute("INSERT INTO build_info (key, value) VALUES (?, ?)", (key, to_json(value)))

        connection.commit()
    finally:
        connection.close()

    os.replace(temp_path, db_path)


def main() -> None:
    args = parse_args()
    build_index(Path(args.root).expanduser(), Path(args.db_path).expanduser())


if __name__ == "__main__":
    main()
