#!/usr/bin/env python3
"""No-network marketing strategy scaffold helper.

The script prints a Markdown planning scaffold. It does not read credentials,
touch accounts, make network calls, or mutate files unless stdout is redirected
by the caller.
"""
from __future__ import annotations

import argparse
from datetime import date


MODES = [
    "campaign",
    "gtm",
    "launch",
    "seo",
    "paid-ads",
    "email-newsletter",
    "community-pr",
    "analytics-experiment",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Print a safe marketing strategy scaffold.")
    parser.add_argument("name", help="Product, offer, campaign, or page set name.")
    parser.add_argument("--mode", choices=MODES, default="campaign")
    parser.add_argument("--audience", default="[MISSING INFO: audience]")
    parser.add_argument("--goal", default="[MISSING INFO: goal]")
    parser.add_argument("--channels", default="[MISSING INFO: channels]")
    parser.add_argument("--evidence", default="[MISSING INFO: source evidence]")
    parser.add_argument("--constraints", default="[MISSING INFO: constraints]")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    channels = [c.strip() for c in args.channels.split(",") if c.strip()]
    if not channels:
        channels = ["[MISSING INFO: channels]"]

    print(f"# Marketing Scaffold: {args.name}")
    print()
    print(f"- Mode: {args.mode}")
    print(f"- Date: {date.today().isoformat()}")
    print(f"- Audience: {args.audience}")
    print(f"- Goal: {args.goal}")
    print(f"- Evidence: {args.evidence}")
    print(f"- Constraints: {args.constraints}")
    print("- Default boundary: draft/read-only; no account mutation, spend, send, post, or scrape.")
    print()
    print("## Context Spine")
    print()
    print("- Product or offer:")
    print("- Buyer uncertainty:")
    print("- Promise:")
    print("- Proof:")
    print("- Risk or objection:")
    print("- Approval gate:")
    print("- Measurement window:")
    print()
    print("## Channel Matrix")
    print()
    print("| Channel | Hook or angle | Proof | Asset needed | CTA | Status |")
    print("| --- | --- | --- | --- | --- | --- |")
    for channel in channels:
        print(f"| {channel} | [draft] | [proof] | [asset] | [CTA] | needs review |")
    print()
    print("## Measurement Plan")
    print()
    print("| Metric | Source | Denominator | Review date | Decision it informs |")
    print("| --- | --- | --- | --- | --- |")
    print("| [metric] | [source] | [denominator] | [date] | [decision] |")
    print()
    print("## Approval Gates")
    print()
    print("- Human review before public copy.")
    print("- Explicit approval before credentials, automation, publishing, sending, account mutation, or spend.")
    print("- Shareables/public-safety and visual QA before public artifact publish.")
    print()
    print("## Next Concrete Action")
    print()
    print("1. Fill missing context spine fields.")
    print("2. Choose one primary lane.")
    print("3. Draft the smallest reviewable artifact.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
