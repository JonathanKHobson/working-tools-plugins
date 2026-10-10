#!/usr/bin/env python3

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class RetrievalBudget:
    mode: str
    max_results: int
    max_lens_cards: int
    max_chunks: int
    max_graph_edges: int
    max_context_chars: int


@dataclass(frozen=True)
class RetrievalTrace:
    budget_mode: str
    requested_limit: int
    effective_limit: int
    returned_count: int
    context_chars: int
    truncated: bool
    notes: list[str]


@dataclass(frozen=True)
class ValidationReport:
    ok: bool
    failures: list[str]
    warnings: list[str]
    metadata: dict[str, Any]


BUDGETS: dict[str, RetrievalBudget] = {
    "quick": RetrievalBudget("quick", max_results=5, max_lens_cards=3, max_chunks=6, max_graph_edges=6, max_context_chars=6000),
    "standard": RetrievalBudget("standard", max_results=10, max_lens_cards=8, max_chunks=16, max_graph_edges=20, max_context_chars=14000),
    "deep": RetrievalBudget("deep", max_results=30, max_lens_cards=20, max_chunks=40, max_graph_edges=60, max_context_chars=36000),
    "debug": RetrievalBudget("debug", max_results=50, max_lens_cards=40, max_chunks=80, max_graph_edges=100, max_context_chars=80000),
}


def budget_definitions() -> dict[str, dict[str, Any]]:
    return {key: asdict(value) for key, value in BUDGETS.items()}


def get_budget(mode: str | None) -> RetrievalBudget:
    return BUDGETS.get((mode or "standard").strip().lower(), BUDGETS["standard"])


def clamp_limit(requested: int | None, maximum: int, default: int) -> int:
    try:
        value = int(requested if requested is not None else default)
    except (TypeError, ValueError):
        value = default
    return max(1, min(value, maximum))


def estimate_json_chars(value: Any) -> int:
    return len(json.dumps(value, ensure_ascii=False, default=str))
