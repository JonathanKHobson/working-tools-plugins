#!/usr/bin/env python3
"""Quiet, read-only prompt-crafting hint for Codex/Claude UserPromptSubmit."""

from __future__ import annotations

import json
import re
import sys
from typing import Any

MAX_INPUT = 64_000
MAX_PROMPT = 8_000
CRAFT = re.compile(
    r"\b(?:rewrite|refine|improve|craft|create|build|draft|design|evaluate|debug|"
    r"optimi[sz]e|review|test|compare|template|playbook)\b", re.I
)
PROMPT = re.compile(
    r"\b(?:prompt(?:s|ing)?|system instructions?|custom instructions?|"
    r"agent instructions?|prompt compass|prompt playbook)\b", re.I
)
IMPLEMENTATION = re.compile(
    r"\b(?:hook|script|python|javascript|typescript|mcp server|plugin manifest|"
    r"implement|code|repo(?:sitory)?|unit tests?)\b", re.I
)
SUCCESS = re.compile(
    r"\b(?:success|done when|pass(?:es)?|verify|test|evaluate|compare|"
    r"measure|criteria|check)\b", re.I
)
MISSING_TARGET = re.compile(
    r"^(?:improve|rewrite|refine|fix)\s+(?:this|my|the)\s+prompt[.!?\s]*$", re.I
)


def content_text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "\n".join(filter(None, (content_text(item) for item in value)))
    if isinstance(value, dict):
        return content_text(value.get("text") or value.get("content") or value.get("value"))
    return ""


def prompt_from_payload(payload: Any) -> str:
    if not isinstance(payload, dict):
        return ""
    messages = payload.get("messages")
    if isinstance(messages, list):
        for item in reversed(messages):
            if isinstance(item, dict) and item.get("role") in ("user", "human"):
                found = content_text(item.get("content"))
                if found:
                    return found[:MAX_PROMPT]
    for key in ("prompt", "user_prompt", "message", "input", "text"):
        found = content_text(payload.get(key))
        if found:
            return found[:MAX_PROMPT]
    for key in ("payload", "event", "data", "request"):
        found = prompt_from_payload(payload.get(key))
        if found:
            return found[:MAX_PROMPT]
    return ""


def advisory(prompt: str) -> str:
    compact = " ".join(prompt.split())[:MAX_PROMPT]
    if not PROMPT.search(compact) or not CRAFT.search(compact):
        return ""
    # Requests to implement prompt tooling are code tasks, not candidates for
    # an extra prompt-writing workflow on every turn.
    if IMPLEMENTATION.search(compact) and not re.search(r"\b(?:write|rewrite|refine)\s+(?:a|the|my)?\s*prompt\b", compact, re.I):
        return ""
    if MISSING_TARGET.fullmatch(compact):
        return "Prompt Playbook advisory: identify the prompt text or intended use; ask for it only if current context does not supply it."
    if len(compact) < 90 and not SUCCESS.search(compact):
        return "Prompt Playbook advisory: clarify the audience or use and one observable success check if context does not already provide them."
    if not SUCCESS.search(compact):
        return "Prompt Playbook advisory: include a proportionate success check when revising the prompt; keep the user's original intent and constraints."
    return ""


def main() -> int:
    try:
        raw = sys.stdin.read(MAX_INPUT + 1)
        if not raw or len(raw) > MAX_INPUT:
            return 0
        payload = json.loads(raw)
        message = advisory(prompt_from_payload(payload))
        if message:
            print(json.dumps({"hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit", "additionalContext": message
            }}, separators=(",", ":")))
    except (OSError, ValueError, TypeError, RecursionError):
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
