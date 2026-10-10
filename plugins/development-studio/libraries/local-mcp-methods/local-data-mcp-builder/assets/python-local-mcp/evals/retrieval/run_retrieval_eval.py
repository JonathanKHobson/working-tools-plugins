#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run starter retrieval evals for a local-data MCP.")
    parser.add_argument("--db-path", required=True, help="SQLite DB path built by build_index.py.")
    parser.add_argument("--fixtures", default=str(Path(__file__).with_name("lens_queries.jsonl")), help="JSONL fixture path.")
    return parser.parse_args()


def load_cases(path: Path) -> list[dict[str, Any]]:
    cases = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            case = json.loads(line)
            case["_line"] = line_number
            cases.append(case)
    return cases


def retrieve_lens_ids(connection: sqlite3.Connection, query: str, limit: int = 5) -> list[str]:
    tokens = [token for token in query.lower().replace("-", " ").split() if token]
    fts_query = " OR ".join(f"{token}*" for token in tokens[:8])
    if not fts_query:
        return []
    rows = connection.execute(
        """
        SELECT lc.lens_id
        FROM lens_cards_fts
        JOIN lens_cards lc ON lc.lens_id = lens_cards_fts.lens_id
        WHERE lens_cards_fts MATCH ?
        ORDER BY bm25(lens_cards_fts) ASC, lc.name ASC
        LIMIT ?
        """,
        (fts_query, limit),
    ).fetchall()
    return [str(row[0]) for row in rows]


def main() -> None:
    args = parse_args()
    cases = load_cases(Path(args.fixtures).expanduser())
    must_not_violations = []
    recall_scores = []

    connection = sqlite3.connect(Path(args.db_path).expanduser())
    try:
        for case in cases:
            returned_ids = retrieve_lens_ids(connection, case["query"])
            expected = set(case.get("expected_ids") or [])
            must_not = set(case.get("must_not_include") or [])
            hits = [lens_id for lens_id in returned_ids if lens_id in expected]
            violations = [lens_id for lens_id in returned_ids if lens_id in must_not]
            recall_scores.append(len(hits) / len(expected) if expected else 1.0)
            if violations:
                must_not_violations.append({"line": case["_line"], "query": case["query"], "violations": violations})
    finally:
        connection.close()

    summary = {
        "fixture_count": len(cases),
        "recall_at_5": round(sum(recall_scores) / len(recall_scores), 4) if recall_scores else 0.0,
        "must_not_include_violations": len(must_not_violations),
        "violations": must_not_violations,
        "hard_gate": "must_not_include_violations == 0",
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    if must_not_violations:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
