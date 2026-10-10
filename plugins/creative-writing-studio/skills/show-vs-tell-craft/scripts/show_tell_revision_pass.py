#!/usr/bin/env python3
"""Deterministic helper for show-vs-tell diagnosis and lightweight rewrites."""

from __future__ import annotations

import argparse
import re
import sys


ABSTRACT = re.compile(
    r"\b(scared|angry|sad|happy|nervous|intimidating|eerie|majestic|beautiful|strange|grand|impressive|horrible|terrifying|suspicious|charming|chaotic|cozy|important|kind|cruel|bustling)\b",
    re.IGNORECASE,
)
WEAK = re.compile(r"\b(was|were|felt|seemed)\b", re.IGNORECASE)
PLAYER_COMMAND = re.compile(r"\b(players?|you)\s+(feel|notice|realize|understand)\b", re.IGNORECASE)
BODY_LOOP = re.compile(
    r"\b(clenched fists?|jaw tightened|heart pounded|racing pulse|shiver down .*spine|narrowed eyes|crossed arms)\b",
    re.IGNORECASE,
)
OVER_SHOW = re.compile(r"\brectangular wooden barrier|cold metal sphere attached to it\b", re.IGNORECASE)


def lint(text: str) -> list[str]:
    flags: list[str] = []
    if ABSTRACT.search(text):
        flags.append("abstract label or judging adjective")
    if WEAK.search(text):
        flags.append("weak summary verb or hedge")
    if PLAYER_COMMAND.search(text):
        flags.append("tells reader/player what to perceive or feel")
    if BODY_LOOP.search(text):
        flags.append("generic body-language loop")
    if OVER_SHOW.search(text) or len(text.split()) > 90 and text.count(",") > 5:
        flags.append("possible over-showing or bloated description")
    if "as you know" in text.lower():
        flags.append("reader-benefit exposition")
    return flags


def diagnose(text: str) -> str:
    flags = lint(text)
    purpose = "felt" if flags and not OVER_SHOW.search(text) else "understood quickly"
    recommendation = "blend" if flags and len(text.split()) > 12 else ("tell" if OVER_SHOW.search(text) else "show")
    return f"""## Show vs Tell Diagnosis

### Passage Purpose
- Audience: unknown
- Mode: diagnose
- Should this be felt, understood, or both? {purpose}

### Current Balance
- Showing: {'some concrete evidence' if not flags else 'limited or unclear'}
- Telling: {'dominant' if flags else 'functional'}
- Problem: {', '.join(flags) if flags else 'No major show/tell lint flags.'}

### Lint Flags
- Abstract labels: {'yes' if ABSTRACT.search(text) else 'no'}
- Unsupported claims: {'yes' if ABSTRACT.search(text) else 'unknown'}
- Generic body language: {'yes' if BODY_LOOP.search(text) else 'no'}
- Reader-benefit exposition: {'yes' if 'as you know' in text.lower() else 'no'}
- Missing sensory/action evidence: {'yes' if flags and not OVER_SHOW.search(text) else 'no'}

### Recommendation
- Show: Use concrete evidence for moments meant to be felt.
- Tell: Use direct summary for procedure, transition, and utility.
- Blend: Tell the organizing idea, then show proof.

### Revision
Recommended mode: {recommendation}
"""


def rewrite_to_show(text: str) -> str:
    if "forest" in text.lower():
        return "Branches clicked in the dark above the path. The moss swallowed each footstep, and something small stopped moving whenever the lantern swung its way."
    if "shrine" in text.lower():
        return "Candles burned behind locked glass. A brass placard read: ONE PRAYER PER TOKEN. Beneath the saint's smile, a clerk counted coins into a velvet bag."
    if "clerk" in text.lower() or "nervous" in text.lower():
        return "The clerk stamped the same form three times, missed the ink pad twice, and smiled without showing teeth."
    return "Replace the abstract claim with one action, one object, and one sensory detail that lets the audience infer the point."


def rewrite_to_tell(text: str) -> str:
    if OVER_SHOW.search(text):
        return "He opened the door."
    if "rules" in text.lower() or "daggerheart" in text.lower():
        return "Tell the rule needed for the current choice, resolve it, then flag anything uncertain for after play."
    return "Summarize the fact plainly so the scene can move."


def blend(text: str) -> str:
    return "Tell the organizing idea in one sentence, then prove it with one concrete image, action, or line of dialogue."


def table_read_aloud(text: str) -> str:
    return rewrite_to_show(text)


def gm_sidebar(text: str) -> str:
    return "Use this like a fantasy DMV mixed with a theme-park ticket booth: bright, procedural, and absurd. The table guidance is simple: make the service feel cheerful while each detail shows that access costs extra."


def story_atlas_entry(text: str) -> str:
    return f"""## Player-Facing Description
{table_read_aloud(text)}

## GM Sidebar
{gm_sidebar(text)}

## Show/Tell Rationale
- What is shown: sensory and object evidence.
- What is told: function, analogy, and table use.
- Why this balance fits: players infer tone; the GM gets clarity.

## Table Use
- Say: Read the player-facing text.
- Let players ask: what can be touched, bought, read, overheard, or challenged.
- Reveal only if: they investigate, spend time, or trigger the secret.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mode",
        choices=[
            "diagnose",
            "rewrite_to_show",
            "rewrite_to_tell",
            "blend_show_and_tell",
            "table_read_aloud",
            "gm_sidebar",
            "line_lint",
            "story_atlas_entry",
        ],
        default="diagnose",
    )
    parser.add_argument("text", nargs="*", help="Text to inspect; stdin is used when omitted.")
    args = parser.parse_args()
    text = " ".join(args.text).strip() or sys.stdin.read().strip()

    if args.mode == "diagnose":
        print(diagnose(text))
    elif args.mode == "rewrite_to_show":
        print(rewrite_to_show(text))
    elif args.mode == "rewrite_to_tell":
        print(rewrite_to_tell(text))
    elif args.mode == "blend_show_and_tell":
        print(blend(text))
    elif args.mode == "table_read_aloud":
        print(table_read_aloud(text))
    elif args.mode == "gm_sidebar":
        print(gm_sidebar(text))
    elif args.mode == "line_lint":
        print("\n".join(lint(text)) or "No show/tell lint flags.")
    elif args.mode == "story_atlas_entry":
        print(story_atlas_entry(text))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
