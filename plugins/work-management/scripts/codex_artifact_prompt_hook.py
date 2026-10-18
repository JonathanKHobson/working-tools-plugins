#!/usr/bin/env python3
"""Keep the existing artifact quality obligation detector on prompt submission."""

from __future__ import annotations

import json
import sys

from codex_artifact_quality_gate import detect_and_store, scope_key_from_hook_payload


def text(value):
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "\n".join(filter(None, (text(item) for item in value)))
    if isinstance(value, dict):
        return text(value.get("text") or value.get("content") or value.get("value"))
    return ""


def prompt(data):
    if not isinstance(data, dict):
        return ""
    messages = data.get("messages")
    if isinstance(messages, list):
        for item in reversed(messages):
            if isinstance(item, dict) and item.get("role") in ("user", "human"):
                value = text(item.get("content"))
                if value:
                    return value
    for key in ("prompt", "user_prompt", "message", "input", "text"):
        value = text(data.get(key))
        if value:
            return value
    return ""


def main():
    try:
        raw = sys.stdin.read(64_001)
        if not raw or len(raw) > 64_000:
            return 0
        data = json.loads(raw)
        value = prompt(data)
        if value:
            detect_and_store(value, scope_key=scope_key_from_hook_payload(data))
    except (OSError, ValueError, TypeError, RecursionError):
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
