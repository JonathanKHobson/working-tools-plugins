#!/usr/bin/env python3
"""Build a safe current-social research source plan.

This is intentionally planner-only: it emits source lanes, query variants,
coverage expectations, and risk gates without logging into accounts, reading
browser profiles, calling paid APIs, or scraping platforms.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import date, timedelta
from typing import Iterable


@dataclass(frozen=True)
class SourceLane:
    name: str
    purpose: str
    safe_methods: list[str]
    risk_gate: str
    output_clues: list[str]


PUBLIC_LANES: list[SourceLane] = [
    SourceLane(
        name="Reddit public web",
        purpose="Community objections, practical use cases, strong comments, and recurring phrases.",
        safe_methods=[
            "Use web search scoped to reddit.com with the chosen date window.",
            "Prefer directly accessible threads and comments; cite URLs close to claims.",
        ],
        risk_gate="No account login, private cookies, or API-token scraping.",
        output_clues=["subreddit", "date", "upvotes/comments when visible", "representative quote"],
    ),
    SourceLane(
        name="Hacker News",
        purpose="Developer consensus, technical objections, launch reception, and maintainer context.",
        safe_methods=[
            "Search HN items/comments through public pages or search-engine results.",
            "Separate launch posts from second-order discussion.",
        ],
        risk_gate="No private account state or vote scraping.",
        output_clues=["points/comments", "thread URL", "technical pattern"],
    ),
    SourceLane(
        name="GitHub public activity",
        purpose="Shipping velocity, issue pain, release freshness, maintainer behavior, and adoption clues.",
        safe_methods=[
            "Read public releases, issues, discussions, commits, PRs, and stars.",
            "For people, prefer author-scoped public activity when available.",
        ],
        risk_gate="Use unauthenticated public data unless the user explicitly authorizes a token.",
        output_clues=["repo", "release/issue/PR URL", "stars or merge counts when visible"],
    ),
    SourceLane(
        name="First-party sources",
        purpose="Official claims, changelogs, pricing, roadmap hints, and source-of-truth corrections.",
        safe_methods=[
            "Resolve official site, blog, docs, changelog, release notes, careers, and public social handles.",
            "Treat first-party claims as intent, not independent proof.",
        ],
        risk_gate="No admin portals, dashboards, or private newsletters unless supplied by the user.",
        output_clues=["official URL", "publication/update date", "claim"],
    ),
    SourceLane(
        name="Public social/video",
        purpose="Creator framing, cultural resonance, tutorials, demos, and memorable language.",
        safe_methods=[
            "Use publicly viewable posts, videos, transcripts, descriptions, and search snippets.",
            "Prefer accessible YouTube transcripts and clearly dated posts.",
        ],
        risk_gate="No browser-session extraction, private cookies, auth tokens, or paid creator APIs by default.",
        output_clues=["creator/channel", "date", "views/likes/comments when visible", "quote or summary"],
    ),
    SourceLane(
        name="Markets and hiring signals",
        purpose="What money, hiring, or public commitments suggest about direction and demand.",
        safe_methods=[
            "Use public job boards, company career pages, prediction markets, funding/news, and pricing pages.",
            "State that hiring/market data is a signal, not proof of roadmap.",
        ],
        risk_gate="No auto-apply, account login, or credentialed job-board scraping.",
        output_clues=["job/market URL", "date", "role/odds/price", "inference confidence"],
    ),
]


CREDENTIAL_LANES: list[SourceLane] = [
    SourceLane(
        name="Credentialed social APIs",
        purpose="Broader X, TikTok, Instagram, Threads, Pinterest, Bluesky, or Perplexity coverage.",
        safe_methods=[
            "Use only after the user explicitly approves the exact provider, key, cost, and data path.",
            "Prefer scoped API keys over browser cookies.",
        ],
        risk_gate="Requires separate security review and explicit approval before use.",
        output_clues=["provider", "credential scope", "cost/rate limit", "retention path"],
    ),
    SourceLane(
        name="Browser-cookie/profile extraction",
        purpose="Private-session-only platform search where public access is insufficient.",
        safe_methods=[
            "Default to excluded. Revisit only for a narrow, user-approved, high-value task.",
        ],
        risk_gate="Do not read Chrome/Safari/Firefox cookies or profiles without exact-step approval.",
        output_clues=["explicit approval", "profile path", "platform", "data minimization plan"],
    ),
]


def _split_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def _query_variants(topic: str, aliases: Iterable[str], mode: str) -> list[str]:
    base_terms = [topic, *aliases]
    variants: list[str] = []
    for term in base_terms:
        variants.extend(
            [
                f'"{term}" review OR reaction',
                f'"{term}" problem OR issue OR complaint',
                f'"{term}" recommendation OR alternative',
                f'"{term}" changelog OR release OR launch',
            ]
        )
        if mode in {"person", "repo"}:
            variants.append(f'"{term}" GitHub PR OR issue OR release')
        if mode in {"company", "product"}:
            variants.append(f'"{term}" careers OR hiring OR pricing')
    return list(dict.fromkeys(variants))


def build_plan(args: argparse.Namespace) -> dict:
    today = date.today()
    start = today - timedelta(days=args.window)
    aliases = _split_csv(args.aliases)
    excluded = _split_csv(args.exclude_sources)
    lanes = [lane for lane in PUBLIC_LANES if lane.name.lower() not in {e.lower() for e in excluded}]
    return {
        "topic": args.topic,
        "aliases": aliases,
        "mode": args.mode,
        "decision": args.decision or "",
        "window": {
            "days": args.window,
            "start": start.isoformat(),
            "end": today.isoformat(),
        },
        "public_lanes": [asdict(lane) for lane in lanes],
        "credentialed_lanes_excluded_by_default": [asdict(lane) for lane in CREDENTIAL_LANES],
        "query_variants": _query_variants(args.topic, aliases, args.mode),
        "coverage_ledger_template": [
            {
                "url": "",
                "date": "",
                "source_type": "",
                "observed_signal": "",
                "engagement_or_authority": "",
                "confidence": "strong | moderate | thin | conflicting | stale",
            }
        ],
        "synthesis_requirements": [
            "Group findings into 3-7 signal clusters rather than a link dump.",
            "Include strongest sources, community wording when useful, confidence, and decision relevance.",
            "Report strong, thin, missing, and explicitly excluded source lanes.",
            "For shareables, preserve date window, citations, uncertainty, and private-source exclusions.",
        ],
    }


def render_markdown(plan: dict) -> str:
    lines = [
        f"# Current Social Research Plan: {plan['topic']}",
        "",
        f"Window: {plan['window']['start']} to {plan['window']['end']} ({plan['window']['days']} days)",
        f"Mode: {plan['mode']}",
    ]
    if plan["aliases"]:
        lines.append(f"Aliases: {', '.join(plan['aliases'])}")
    if plan["decision"]:
        lines.append(f"Decision: {plan['decision']}")
    lines.extend(["", "## Public Source Lanes"])
    for lane in plan["public_lanes"]:
        lines.extend(
            [
                f"- {lane['name']}: {lane['purpose']}",
                f"  Risk gate: {lane['risk_gate']}",
                f"  Evidence clues: {', '.join(lane['output_clues'])}",
            ]
        )
    lines.extend(["", "## Excluded Unless Explicitly Approved"])
    for lane in plan["credentialed_lanes_excluded_by_default"]:
        lines.append(f"- {lane['name']}: {lane['risk_gate']}")
    lines.extend(["", "## Query Variants"])
    lines.extend(f"- {query}" for query in plan["query_variants"])
    lines.extend(["", "## Synthesis Requirements"])
    lines.extend(f"- {item}" for item in plan["synthesis_requirements"])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Plan a safe current-social research run.")
    parser.add_argument("topic")
    parser.add_argument("--aliases", default="", help="Comma-separated aliases, handles, or related names.")
    parser.add_argument("--decision", default="", help="Decision this research should inform.")
    parser.add_argument("--mode", choices=["topic", "person", "company", "product", "repo"], default="topic")
    parser.add_argument("--window", type=int, default=30, help="Recent-days window, default 30.")
    parser.add_argument("--exclude-sources", default="", help="Comma-separated public lane names to omit.")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()

    plan = build_plan(args)
    if args.format == "json":
        print(json.dumps(plan, indent=2))
    else:
        print(render_markdown(plan), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
