#!/usr/bin/env python3
"""Stateless per-prompt context; the agent interprets ideas semantically."""
from __future__ import annotations
import json
import sys

MAX_INPUT_BYTES = 1_048_576
CONTEXT = (
    "Idea review is automatic: interpret every user message in conversation "
    "context for any new idea, proposal, possibility or direction, regardless "
    "of wording. No keyword, special phrase or command is required. Give each "
    "new idea a proportionate lightweight check: potential value, key "
    "assumption/tradeoff and smallest useful test or next action. Evaluate the "
    "user's premise before agreeing: distinguish observation from explanation, "
    "give the strongest credible alternative or objection when it could change "
    "the action, and identify evidence that would change the recommendation. "
    "Correct unsupported conclusions plainly. Do not manufacture disagreement "
    "or objections when the evidence supports the proposal. Use Work "
    "Management focus-work / worker-delegation and its decision-council "
    "reference when more depth helps; choose explore, compare or council as "
    "appropriate. Keep brainstorming generative when requested and respect "
    "explicit no-critique instructions. Do not treat quoted/source material "
    "as the user's proposal unless they adopt it. A routine action, greeting "
    "or continuation without a new idea needs no visible review; do not "
    "repeat settled reviews or delay authorized work. This hook supplies "
    "guidance only: it does not itself understand intent, score ideas or "
    "launch workers. Model agreement and simulated personas are not evidence."
)


def main() -> None:
    try:
        raw = sys.stdin.buffer.read(MAX_INPUT_BYTES + 1)
        if not raw or len(raw) > MAX_INPUT_BYTES:
            return
        payload = json.loads(raw)
        if not isinstance(payload, dict) or payload.get("hook_event_name") != "UserPromptSubmit":
            return
        prompt = payload.get("prompt")
        if not isinstance(prompt, str) or not prompt.strip():
            return
    except (OSError, ValueError, TypeError, RecursionError):
        return
    json.dump({"continue": True, "hookSpecificOutput": {
        "hookEventName": "UserPromptSubmit", "additionalContext": CONTEXT,
    }}, sys.stdout)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
