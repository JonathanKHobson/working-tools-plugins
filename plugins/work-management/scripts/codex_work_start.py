#!/usr/bin/env python3
"""Supply an explicit portable workflow route or opted-in recipient context.

This hook supplies context only. The agent uses the native goal tools; the
hook never edits goal storage, reads transcripts, or starts another process.
"""

from __future__ import annotations

import os
import json
import sys
from pathlib import Path

MAX_INPUT_BYTES = 1_048_576
SKILL_PATH = Path(__file__).resolve().parents[1] / "skills/tool-workflow-routing/SKILL.md"
PORTABLE_CONTEXT = (
    f"For work, select the production owner and needed reviewers through {SKILL_PATH}; reuse routing already read. "
    "Follow its production handoff and load the selected skills before applying them. "
    "This reminder grants no access and does not prove execution."
)
CONTEXT = (
    "Native goal reminder: Apply automatic native goals only if the receiving user explicitly requested them "
    "for work requests; verify their current explicit preference and host instructions. "
    "For an actionable user request, use get_goal before substantive work. "
    "If there is no unfinished goal, call create_goal with the concrete "
    "requested outcome without asking again when that explicit request is active. Reuse an "
    "unfinished goal for related follow-ups; never mark it complete just to "
    "replace it. Follow the native tool's lifecycle rules for paused, blocked, "
    "or limited goals. Do not restart after a pause/stop request or override "
    "the user's current opt-out. Greetings, acknowledgments, status-only "
    "questions and goal-control messages need no new goal. Omit token_budget "
    "unless explicitly requested. Complete a goal only after the requested "
    "outcome is achieved and verified. If native goal tools are unavailable, "
    "continue the requested work and briefly disclose that limitation. This "
    "reminder creates no goal itself and grants no new action permissions.\n\n"
    "Work Management: consult work-management:project-structure before creating or reorganizing "
    "files in new or continued projects and when scope changes; reuse guidance already read. "
    "Choose the smallest relevant skill and call its useful tools. Proactively use existing "
    "charts, dashboards or MCP widgets when they improve understanding, comparison, exploration, "
    "editing or verification. Preserve explicit formats and keep simple answers direct. "
    "Use tool-workflow-routing for selection; verify output and relevant interaction. "
    "This grants no new access, installation, publication or recurring-monitoring authority. "
    "For substantial independent work, use worker-delegation while the lead progresses. "
    "Use worker-delegation to offload useful independent work through claude-toolkit, "
    "gemini-toolkit, apple-foundation-model-toolkit or local-model-toolkit. Prefer verified "
    "CLIs and the host’s tested local default for suitable bounded work. Check allowance, "
    "actual model/output and total handoff/repair cost. Keep trivial or "
    "inseparable work local. Deeper research prefers standard ChatGPT Web with Pro visibly "
    "selected through subscription offload; dedicated Deep Research requires a specific "
    "request. Check sources and integrate results. Use subagents for steps within one goal; "
    "separate chats for independent durable goals only under explicit user authorization "
    "and native creation/messaging rules. Do not create skills, catalogs, folders, jobs or "
    "chats merely to satisfy this reminder.\n\n"
    "Chat naming: at the first substantive work turn and when scope changes, "
    "check this chat's native title. Preserve an explicitly user-chosen title. "
    "Otherwise replace an automatic sentence, vague label or obsolete title "
    "with Project or domain · Durable role (for example, Computer · Hook Repair). "
    "For a one-off task use a concise domain and concrete outcome. Use "
    "set_thread_title on this chat and verify native readback; avoid renaming "
    "other chats or repeating an already-correct rename.\n\n"
    "At meaningful closeout under learning-capture authorization, use "
    "evidence-review's feedback-to-method review for consequential signals "
    "already in context. Link source, owner, task fix, transfer decision and "
    "validation/rollback in the project record. Reuse existing methods; apply "
    "only authorized owner changes. Skip trivial/no-signal turns. No history "
    "crawl, automatic skill/memory writes or implied human claim acceptance. "
    "Opted-in activity capture follows ship-log.\n\n"
    "Before final closeout, review resources this chat actually started: "
    "scripts, dev servers, browser sessions and temporary tool helpers. Close "
    "finished task-owned resources and verify exits; retain explicitly ongoing "
    "jobs and name what remains needed. Age, low CPU, a shared cwd, or the same "
    "Codex parent does not prove chat ownership. Preserve other chats' work, "
    "protected services and platform-managed MCP connections. Do not end all "
    "loaded chats' helpers or disable shared MCPs to satisfy closeout."
)


def main(argv: list[str] | None = None) -> None:
    arguments = sys.argv[1:] if argv is None else argv
    if arguments not in ([], ["--portable"]):
        return
    portable = arguments == ["--portable"]
    if not portable and os.environ.get("WORK_MANAGEMENT_CONTEXT_OPT_IN") != "1":
        return
    try:
        raw = sys.stdin.buffer.read(MAX_INPUT_BYTES + 1)
        if not raw or len(raw) > MAX_INPUT_BYTES:
            return
        payload = json.loads(raw)
        if not isinstance(payload, dict):
            return
        if payload.get("hook_event_name") != "UserPromptSubmit":
            return
        prompt = payload.get("prompt")
        if not isinstance(prompt, str) or not prompt.strip():
            return
    except (OSError, ValueError, TypeError, RecursionError):
        return

    json.dump(
        {
            "continue": True,
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": PORTABLE_CONTEXT if portable else CONTEXT,
            },
        },
        sys.stdout,
    )
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
