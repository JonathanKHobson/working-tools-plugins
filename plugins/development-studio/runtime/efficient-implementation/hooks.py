"""Optional fail-open lifecycle adapter. No registration or host settings writes."""

import json
from pathlib import Path
import re
import sys
import threading

from state import Session, set_default
from filesystem import directory, read_at

EVENTS = ("SessionStart", "UserPromptSubmit", "SubagentStart")


def trusted_reference():
    plugin = Path(__file__).resolve().parents[2]
    relative = Path("references/efficient-implementation.md")
    with directory(plugin) as parent:
        content, _ = read_at(parent, relative, 1)
    if not content:
        raise ValueError("trusted implementation reference is empty")
    return plugin / relative


def read_payload(stream=None, timeout=0.5):
    """Never wait indefinitely for EOF, including hosts with a stuck stdin pipe."""
    result = []

    def read():
        try:
            raw = (stream or sys.stdin).read(65537)
            if len(raw) <= 65536:
                value = json.loads(raw.lstrip("\ufeff"))
                if isinstance(value, dict):
                    result.append(value)
        except (OSError, ValueError, UnicodeError):
            pass

    worker = threading.Thread(target=read, daemon=True)
    worker.start()
    worker.join(max(0.01, min(timeout, 1.0)))
    return result[0] if result else {}


def handle(event, data, directory, *, root=None, session_id=None, host="generic"):
    if event not in EVENTS or not isinstance(data, dict) or host not in {"generic", "codex"}:
        return None
    root = root or data.get("cwd") or data.get("project_root")
    identity = session_id or data.get("session_id")
    if event == "SubagentStart":
        if host == "codex":
            # Codex's documented native payload uses session_id for the parent.
            # Require its event and child identity before interpreting that field.
            agent = data.get("agent_id")
            if (data.get("hook_event_name") != "SubagentStart"
                    or not isinstance(agent, str) or not agent.strip()):
                return None
            identity = data.get("session_id")
        else:
            # Generic hosts must name the parent explicitly; never infer from a repo flag.
            identity = data.get("parent_session_id")
    if not isinstance(root, str) or not isinstance(identity, str):
        return None
    session = Session(directory, root, identity)
    scope = data.get("scope") if isinstance(data.get("scope"), str) else None
    if session.status(scope)["reason"] == "scope-changed":
        session.off("scope-changed")
        return None
    if event == "UserPromptSubmit":
        prompt = data.get("prompt")
        if not isinstance(prompt, str):
            return None
        prompt = prompt.strip()
        # Exact complete commands only: quotes, code fences, extra arguments, and prose do not match.
        match = re.fullmatch(r"/efficient-implementation(?: (lite|full|ultra|off|reopen|status|help|default (?:lite|full|ultra|off)))?", prompt)
        if match:
            command = match.group(1) or "status"
            if command.startswith("default "):
                set_default(directory, command.split()[1])
                return None
            if command in {"off", "reopen"}:
                session.off(command)
                return None
            if command in {"help", "status"}:
                return None
            # Ready status is checked again before changing a mode. Default/help/report commands never latch.
            if not session.status(scope)["active"]:
                return None
            session.switch(command)
        else:
            return None
    status = session.status(scope)
    if not status["active"]:
        return None
    context = ("Efficient implementation: mode=" + status["mode"] + "; state=ready; contract_sha256=" +
               status["contract_sha256"] + ". Read trusted installed reference " +
               json.dumps(str(trusted_reference()), ensure_ascii=True) +
               ". Applies only to the accepted implementation scope; reopen before changing task or scope. "
               "Normal safety and user instructions still apply.")
    return {"hookSpecificOutput": {"hookEventName": event, "additionalContext": context}}
