#!/usr/bin/env python3
"""Deliver a bounded editorial route; no model, file reads, or usage claim."""
import json
import sys
from pathlib import Path

SKILL_PATH = Path(__file__).resolve().parents[1] / "skills/natural-prose-editor/SKILL.md"
CONTEXT = (
    "For authored reader-facing artifacts in any medium, apply "
    "writing-quality-studio:natural-prose-editor, the everyday Humanizer, before delivery. "
    f"Read {SKILL_PATH} when the guide is not already loaded. "
    "UX owns placement. Reuse loaded guidance; conversational status needs no skill reload. "
    "For substantial saved artifacts, record exact-content communication_review evidence "
    "through Work Management's gate. Reminders and reads do not prove review."
)


def main():
    try:
        raw = sys.stdin.buffer.read(64001)
        if not raw or len(raw) > 64000:
            return
        data = json.loads(raw)
        if not isinstance(data, dict) or data.get("hook_event_name") != "UserPromptSubmit":
            return
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit", "additionalContext": CONTEXT
        }}, separators=(",", ":")))
    except (OSError, ValueError, TypeError):
        return


if __name__ == "__main__":
    main()
