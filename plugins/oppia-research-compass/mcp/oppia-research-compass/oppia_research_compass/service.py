"""Oppia-first routing and research support behavior."""

from __future__ import annotations

from typing import Any

from .contracts import (
    CORE_TOOLS,
    PUBLIC_TOOLS,
    SUPPORTING_TOOLS,
    clamp_limit,
    get_budget,
    public_envelope,
)
from .repository import OppiaResearchRepository


EXTERNAL_CUES = (
    "academic paper",
    "external source",
    "external research",
    "find papers",
    "on the web",
    "scholarly",
    "web search",
)


class OppiaResearchService:
    def __init__(self, repository: OppiaResearchRepository) -> None:
        self.repository = repository

    def overview(self) -> dict[str, Any]:
        payload = {
            "purpose": "Search and reuse Oppia historical UX research before gathering new evidence.",
            "corpus": self.repository.overview(),
            "tool_hierarchy": {
                "oppia_corpus_tools": list(CORE_TOOLS),
                "supporting_research_tools": list(SUPPORTING_TOOLS),
                "oppia_tool_share": f"{len(CORE_TOOLS)}/{len(PUBLIC_TOOLS)}",
            },
            "runtime_policy": {
                "default_route": "oppia_corpus_first",
                "external_lookup": "never_automatic",
                "writes": False,
                "ai_glossary": "not_included",
            },
            "start_here": {
                "tool": "oppia_research",
                "example": "What have we learned about learner onboarding?",
            },
        }
        return public_envelope("oppia_research_overview", payload, role="oppia_core")

    def route(self, query: str, *, mode: str = "quick", limit: int | None = None) -> dict[str, Any]:
        budget = get_budget(mode)
        selected_limit = clamp_limit(limit, budget)
        normalized = (query or "").strip()
        if not normalized:
            return self.overview()
        lower = normalized.lower()
        external_requested = any(cue in lower for cue in EXTERNAL_CUES)
        results = self.repository.search(normalized, selected_limit)
        route = {
            "primary_lane": "oppia_corpus",
            "selected_tool": "search_oppia_research",
            "oppia_search_performed": True,
            "external_research_requested": external_requested,
            "external_lookup_performed": False,
            "reason": "Oppia evidence is the primary product surface and is searched before supporting research.",
        }
        payload: dict[str, Any] = {
            "answer_contract": {
                "separate_verbatim_evidence_from_interpretation": True,
                "if_no_evidence_say_no_evidence": True,
                "include_limitations_and_disconfirming_evidence": True,
            },
            "oppia_evidence": results,
            "next_action": (
                "Retrieve the strongest evidence IDs before synthesizing."
                if results["count"]
                else "Use plan_oppia_research to define the specific evidence gap."
            ),
        }
        if external_requested:
            payload["supporting_research_handoff"] = {
                "recommended_tool": "plan_oppia_research",
                "recommended_arguments": {"question": normalized, "include_external_follow_up": True},
                "reason": "External research is supporting work and requires an explicit follow-up plan.",
                "no_external_lookup_performed": True,
            }
        return public_envelope(
            "oppia_research", payload, role="oppia_core", budget=budget, route=route
        )

    def search(
        self,
        query: str,
        *,
        mode: str = "standard",
        limit: int | None = None,
        offset: int = 0,
    ) -> dict[str, Any]:
        budget = get_budget(mode)
        payload = self.repository.search(query, clamp_limit(limit, budget), max(0, offset))
        payload["retrieval_trace"] = {
            "lane": "oppia_corpus",
            "returned": payload["count"],
            "truncated": payload["has_more"],
            "external_lookup_performed": False,
        }
        return public_envelope(
            "search_oppia_research",
            payload,
            role="oppia_core",
            budget=budget,
            route={"primary_lane": "oppia_corpus", "selected_tool": "search_oppia_research"},
        )

    def browse_studies(
        self,
        *,
        query: str | None = None,
        limit: int = 10,
        offset: int = 0,
    ) -> dict[str, Any]:
        budget = get_budget("standard")
        payload = self.repository.browse_records(
            clamp_limit(limit, budget), max(0, offset), query=query, interviews_only=False
        )
        return public_envelope("browse_oppia_studies", payload, role="oppia_core", budget=budget)

    def browse_interviews(
        self,
        *,
        query: str | None = None,
        limit: int = 10,
        offset: int = 0,
    ) -> dict[str, Any]:
        budget = get_budget("standard")
        payload = self.repository.browse_records(
            clamp_limit(limit, budget), max(0, offset), query=query, interviews_only=True
        )
        return public_envelope("browse_oppia_interviews", payload, role="oppia_core", budget=budget)

    def get_record(self, record_id: str) -> dict[str, Any]:
        record = self.repository.get_record(record_id)
        payload = {"record": record, "found": record is not None}
        if record is None:
            payload["next_action"] = "Search or browse Oppia research to obtain a valid record_id."
        return public_envelope("get_oppia_record", payload, role="oppia_core")

    def get_evidence(self, evidence_id: str, *, mode: str = "standard") -> dict[str, Any]:
        budget = get_budget(mode)
        evidence = self.repository.get_evidence(evidence_id, max_chars=budget.context_chars)
        payload = {"evidence": evidence, "found": evidence is not None}
        if evidence is None:
            payload["next_action"] = "Search Oppia research to obtain a valid evidence_id."
        return public_envelope(
            "get_oppia_evidence", payload, role="oppia_core", budget=budget
        )

    def compare(
        self,
        left_query: str,
        right_query: str,
        *,
        mode: str = "standard",
        limit_per_side: int | None = None,
    ) -> dict[str, Any]:
        budget = get_budget(mode)
        per_side_cap = max(1, budget.results // 2)
        if limit_per_side is not None:
            per_side_cap = min(per_side_cap, max(1, int(limit_per_side)))
        left = self.repository.search(left_query, per_side_cap)
        right = self.repository.search(right_query, per_side_cap)
        left_records = {item["record_id"] for item in left["results"]}
        right_records = {item["record_id"] for item in right["results"]}
        payload = {
            "left": left,
            "right": right,
            "shared_record_ids": sorted(left_records & right_records),
            "comparison_boundary": "The MCP returns evidence sets and overlap; the host must label interpretation separately.",
            "external_lookup_performed": False,
        }
        return public_envelope(
            "compare_oppia_findings", payload, role="oppia_core", budget=budget
        )

    def plan_research(
        self,
        question: str,
        *,
        include_external_follow_up: bool = False,
    ) -> dict[str, Any]:
        evidence = self.repository.search(question, 5)
        lower = question.lower()
        if any(cue in lower for cue in ("label", "terminology", "word", "chapter", "unit")):
            method = "concept and label comprehension testing"
        elif any(cue in lower for cue in ("accessibility", "keyboard", "screen reader")):
            method = "accessibility review followed by research with affected users"
        elif any(cue in lower for cue in ("onboarding", "navigation", "first-time", "usability")):
            method = "task-based moderated usability testing"
        elif any(cue in lower for cue in ("teacher", "volunteer", "recruitment")):
            method = "semi-structured interviews with purposive recruitment"
        else:
            method = "targeted interviews or usability testing chosen after reviewing the retrieved evidence"
        payload = {
            "question": question,
            "oppia_evidence_review": {
                "result_count": evidence["count"],
                "evidence_ids": [item["evidence_id"] for item in evidence["results"]],
                "required_first_step": "Review retrieved Oppia evidence before commissioning new research.",
            },
            "proposed_follow_up": {
                "method": method,
                "decision_to_support": "State the product or research decision before recruiting participants.",
                "stop_condition": "Stop when the named evidence gap is answered well enough for that decision.",
            },
            "external_research": {
                "requested": bool(include_external_follow_up),
                "lookup_performed": False,
                "recommended_only_when": "The Oppia corpus lacks decision-relevant evidence or comparison context.",
                "handoff": (
                    "Ask the host AI to run an explicit, source-cited external search."
                    if include_external_follow_up
                    else None
                ),
            },
        }
        return public_envelope("plan_oppia_research", payload, role="research_support")

    def audit_evidence(self, evidence_ids: list[str]) -> dict[str, Any]:
        unique_ids = list(dict.fromkeys(str(item) for item in evidence_ids if str(item).strip()))[:20]
        found = [self.repository.get_evidence(item, max_chars=1) for item in unique_ids]
        records = [item for item in found if item is not None]
        missing = [item for item, record in zip(unique_ids, found) if record is None]
        record_ids = {item["record_id"] for item in records}
        chunk_types = {item["chunk_type"] for item in records}
        warnings: list[str] = []
        if missing:
            warnings.append("One or more evidence IDs were not found.")
        if len(records) > 1 and len(record_ids) == 1:
            warnings.append("All evidence comes from one Oppia record; triangulate before generalizing.")
        if records and len(chunk_types) == 1:
            warnings.append("The bundle uses one chunk type; check whether another evidence form is needed.")
        if not records:
            warnings.append("No retrievable Oppia evidence was supplied.")
        payload = {
            "requested_ids": unique_ids,
            "found_ids": [item["evidence_id"] for item in records],
            "missing_ids": missing,
            "record_count": len(record_ids),
            "chunk_types": sorted(chunk_types),
            "warnings": warnings,
            "quality_rules": [
                "Quote accurately and preserve the evidence ID.",
                "Separate verbatim evidence, researcher interpretation, and speculation.",
                "Report disconfirming evidence and limitations.",
                "If the corpus contains no support, say so.",
            ],
            "ready_for_synthesis": bool(records) and not missing,
        }
        return public_envelope("audit_oppia_evidence", payload, role="research_support")

