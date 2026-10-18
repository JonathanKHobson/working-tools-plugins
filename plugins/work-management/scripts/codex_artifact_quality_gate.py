#!/usr/bin/env python3
"""Advisory artifact quality gate for Codex hooks.

This script is intentionally local and lightweight. It detects likely artifact
review obligations, stores compact local state, and lets Codex mark or skip
checks after running the appropriate reviewer. It never runs reviewer skills
itself.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CODEX_DIR = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
STATE_PATH = CODEX_DIR / "state" / "codex-artifact-quality-gate.json"
SCHEMA_VERSION = 1
STORE_SCHEMA_VERSION = 2
LEGACY_SCOPE_KEY = "legacy:unscoped"
SCOPE_ENV_KEYS = (
    "CODEX_SESSION_ID",
    "CODEX_THREAD_ID",
    "CODEX_CONVERSATION_ID",
    "CODEX_TASK_ID",
    "CODEX_TURN_ID",
)

OBLIGATION_ORDER = ("visual_qa", "design_taste", "communication_review")
OBLIGATION_LABELS = {
    "visual_qa": "visual QA",
    "design_taste": "design review",
    "communication_review": "Writing Quality Studio review",
}
ROUTING_HINTS = {
    "visual_qa": "Inspect the actual rendered artifact using the available native app/browser tools (cua_repl for computer use) or document/PDF rendering tools; map 3–8 visual anchors and verify changed regions and relevant states. Extraction alone is not visual QA.",
    "design_taste": "Use ux-design-toolkit:design-review for interfaces, graphic-design-studio:graphic-design-review for graphics, or figma-design-workflow:design-visual-qa for Figma/Stitch handoffs. Review usability, accessibility, states and visual craft against the accepted direction; cite observed anchor IDs and untested behavior.",
    "communication_review": "Use Writing Quality Studio: writing-quality-studio:natural-prose-editor for routine copy; writing-quality-studio:communication-crafter for strategic messages, audience, evidence, tone and intended action. Reuse completed reviews for unchanged drafts.",
}

VISUAL_RE = re.compile(
    r"\b("
    r"app|artifact|brochure|canvas|component|dashboard|deck|docx?|figma|flyer|"
    r"frontend|html|image|interface|landing page|mockup|page|pdf|poster|prototype|"
    r"screen|screenshot|shareable|site|slide|ui|visual|web app|website"
    r")\b",
    re.IGNORECASE,
)
VISUAL_VERB_RE = re.compile(
    r"\b(build|create|design|generate|make|produce|render|ship|stage|write)\b",
    re.IGNORECASE,
)
COMM_RE = re.compile(
    r"\b("
    r"audience|brief|case study|cover letter|deck narrative|email|executive|"
    r"hiring manager|linkedin|message|narrative|pitch|portfolio|post|proposal|"
    r"readout|recruiter|resume|stakeholders?|story|teaching material"
    r")\b",
    re.IGNORECASE,
)
COMMUNICATION_ACTION_RE = re.compile(
    r"\b(write|draft|compose|create|prepare|send|edit|revise|polish|rewrite)\b"
    r"(?:\W+(?:a|an|the|my|our|your|short|quick|formal|strategic|stakeholder|followup)){0,3}\W+"
    r"(email|messages?|cover letters?|linkedin posts?|pitches?|proposals?|readouts?)\b"
    r"(?!\s+(?:hook|config(?:uration)?|script|routing|handler|integration|api)\b)",
    re.IGNORECASE,
)
REPORT_WITH_AUDIENCE_RE = re.compile(
    r"\b(report|presentation)\b.*\b(audience|client|executive|manager|stakeholder|team|reader|public)\b|"
    r"\b(audience|client|executive|manager|stakeholder|team|reader|public)\b.*\b(report|presentation)\b",
    re.IGNORECASE,
)
AUTHORED_DOC_WITH_AUDIENCE_RE = re.compile(
    r"\b(build|create|draft|generate|make|prepare|produce|write)\b.*"
    r"\b(brief|document|guide|memo|report|presentation)\b.*"
    r"\b(audience|client|executive|manager|stakeholders?|team|reader|public)\b|"
    r"\b(audience|client|executive|manager|stakeholders?|team|reader|public)\b.*"
    r"\b(build|create|draft|generate|make|prepare|produce|write)\b.*"
    r"\b(brief|document|guide|memo|report|presentation)\b",
    re.IGNORECASE,
)
BACKEND_ONLY_RE = re.compile(
    r"\b(api|backend|bug|cli|database|db|server|unit test|pytest|schema|migration)\b",
    re.IGNORECASE,
)

SECRET_PATTERNS = [
    re.compile(r"(?i)\b(api[_-]?key|token|secret|password|bearer)\b\s*[:=]\s*[^ \t,;]+"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{12,}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{12,}\b"),
]


@dataclass(frozen=True)
class QualityGateState:
    schema_version: int
    updated_at: str
    prompt_hash: str
    prompt_preview: str
    obligations: dict[str, dict[str, Any]]
    source: str


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def redact(text: str) -> str:
    for pattern in SECRET_PATTERNS:
        text = pattern.sub("[REDACTED]", text)
    return text


def compact(value: Any, *, limit: int = 220) -> str:
    text = normalize_text(redact(str(value or "")))
    return text if len(text) <= limit else text[: limit - 3].rstrip() + "..."


def prompt_hash(prompt: str) -> str:
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:16]


def current_workspace() -> str:
    workspace = os.getenv("CODEX_WORKSPACE") or os.getenv("PWD")
    if workspace:
        return str(Path(workspace).expanduser())
    try:
        return str(Path.cwd())
    except Exception:
        return str(CODEX_DIR)


def current_scope_key() -> str:
    for key in SCOPE_ENV_KEYS:
        value = normalize_text(os.getenv(key))
        if value:
            if key in {"CODEX_SESSION_ID", "CODEX_THREAD_ID", "CODEX_CONVERSATION_ID"}:
                return f"session:{value}"
            if key == "CODEX_TASK_ID":
                return f"task:{value}"
            return f"turn:{value}"
    return f"workspace:{current_workspace()}"


def scope_key_from_hook_payload(payload: Any) -> str | None:
    if not isinstance(payload, dict):
        return None
    session_id = normalize_text(payload.get("session_id"))
    if session_id:
        return f"session:{session_id}"
    turn_id = normalize_text(payload.get("turn_id"))
    if turn_id:
        return f"turn:{turn_id}"
    return None


def detect_obligations(prompt: str) -> list[str]:
    prompt = normalize_text(prompt)
    if not prompt:
        return []

    obligations: set[str] = set()
    technical_context = bool(re.search(
        r"\b(api|backend|bug|cli|config(?:uration)?|database|db|hook|mcp|plugin|"
        r"routing|script|server|skill|unit test|pytest|schema|migration)\b",
        prompt,
        re.IGNORECASE,
    ))
    explicit_visual_artifact = bool(re.search(
        r"\b(ui|interface|screen|screenshot|brochure|dashboard|deck|docx?|flyer|"
        r"html|landing page|mockup|pdf|poster|prototype|shareable|site|slide|"
        r"web app|website)\b",
        prompt,
        re.IGNORECASE,
    ))
    visual_like = bool(
        VISUAL_RE.search(prompt)
        and VISUAL_VERB_RE.search(prompt)
        and (not technical_context or explicit_visual_artifact)
    )
    communication_like = bool(
        COMMUNICATION_ACTION_RE.search(prompt)
        or REPORT_WITH_AUDIENCE_RE.search(prompt)
        or AUTHORED_DOC_WITH_AUDIENCE_RE.search(prompt)
        or (COMM_RE.search(prompt) and not technical_context)
    )

    if visual_like:
        obligations.update({"visual_qa", "design_taste"})
    if communication_like:
        obligations.add("communication_review")

    if obligations == {"visual_qa", "design_taste"} and BACKEND_ONLY_RE.search(prompt) and not VISUAL_RE.search(prompt):
        obligations.clear()

    return [item for item in OBLIGATION_ORDER if item in obligations]


def default_obligation_state() -> dict[str, Any]:
    return {
        "status": "pending",
        "artifact": "",
        "reviewer": "",
        "evidence": "",
        "note": "",
        "updated_at": utc_now(),
    }


def build_state(prompt: str, obligations: list[str], *, source: str = "prompt-submit") -> QualityGateState:
    return QualityGateState(
        schema_version=SCHEMA_VERSION,
        updated_at=utc_now(),
        prompt_hash=prompt_hash(prompt),
        prompt_preview=compact(prompt, limit=180),
        obligations={name: default_obligation_state() for name in obligations},
        source=source,
    )


def parse_state(raw: dict[str, Any] | None) -> QualityGateState | None:
    if not isinstance(raw, dict):
        return None
    obligations = raw.get("obligations")
    if not isinstance(obligations, dict):
        return None
    try:
        schema_version = int(raw.get("schema_version", 0))
    except Exception:
        schema_version = 0
    return QualityGateState(
        schema_version=schema_version,
        updated_at=str(raw.get("updated_at", "")),
        prompt_hash=str(raw.get("prompt_hash", "")),
        prompt_preview=str(raw.get("prompt_preview", "")),
        obligations=obligations,
        source=str(raw.get("source", "")),
    )


def empty_store() -> dict[str, Any]:
    return {"schema_version": STORE_SCHEMA_VERSION, "updated_at": utc_now(), "scopes": {}}


def read_store(state_path: Path = STATE_PATH) -> dict[str, Any]:
    try:
        raw = json.loads(state_path.read_text())
    except Exception:
        return empty_store()
    if isinstance(raw, dict) and isinstance(raw.get("scopes"), dict):
        return raw
    if isinstance(raw, dict) and isinstance(raw.get("obligations"), dict):
        return {
            "schema_version": STORE_SCHEMA_VERSION,
            "updated_at": utc_now(),
            "active_scope": LEGACY_SCOPE_KEY,
            "scopes": {LEGACY_SCOPE_KEY: raw},
        }
    return empty_store()


def read_state(state_path: Path = STATE_PATH, *, scope_key: str | None = None) -> QualityGateState | None:
    store = read_store(state_path)
    scopes = store.get("scopes")
    if not isinstance(scopes, dict):
        return None
    return parse_state(scopes.get(scope_key or current_scope_key()))


def write_state(state: QualityGateState, state_path: Path = STATE_PATH, *, scope_key: str | None = None) -> None:
    key = scope_key or current_scope_key()
    store = read_store(state_path)
    scopes = store.get("scopes")
    if not isinstance(scopes, dict):
        scopes = {}
    entry = asdict(state)
    entry["scope_key"] = key
    entry["workspace"] = current_workspace()
    scopes[key] = entry
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(
        json.dumps(
            {
                "schema_version": STORE_SCHEMA_VERSION,
                "updated_at": utc_now(),
                "active_scope": key,
                "scopes": scopes,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )


def clear_state(state_path: Path = STATE_PATH, *, scope_key: str | None = None) -> None:
    state_path.parent.mkdir(parents=True, exist_ok=True)
    write_state(build_state("", [], source="clear"), state_path=state_path, scope_key=scope_key)


def detect_and_store(prompt: str, *, state_path: Path = STATE_PATH, scope_key: str | None = None) -> QualityGateState:
    obligations = detect_obligations(prompt)
    state = build_state(prompt, obligations, source="prompt-submit")
    write_state(state, state_path=state_path, scope_key=scope_key)
    return state


def pending_obligations(state: QualityGateState | None) -> list[str]:
    if state is None:
        return []
    pending: list[str] = []
    for name in OBLIGATION_ORDER:
        data = state.obligations.get(name)
        if isinstance(data, dict) and data.get("status") == "pending":
            pending.append(name)
    return pending


def quality_guidance(obligations: list[str]) -> str:
    if not obligations:
        return ""
    labels = ", ".join(OBLIGATION_LABELS[name] for name in obligations)
    return (
        f"Artifact quality gate: if you produce this artifact, run/mark {labels} before final. "
        "For screenshot or rendered-surface review, use a compact visual anchor map. "
        "Use `codex_artifact_quality_gate.py mark <check> --reviewer ... --evidence ...` "
        "or `skip <check> --reason ...` when not applicable."
    )


def stop_advisory(state_path: Path = STATE_PATH, *, scope_key: str | None = None) -> str:
    state = read_state(state_path, scope_key=scope_key)
    pending = pending_obligations(state)
    if not pending:
        return ""
    labels = ", ".join(OBLIGATION_LABELS[name] for name in pending)
    hints = " ".join(ROUTING_HINTS[name] for name in pending)
    return (
        f"Codex artifact quality gate: pending {labels}. {hints} "
        "Mark completed checks or skip with a reason before final."
    )


def update_obligation(
    name: str,
    *,
    status: str,
    artifact: str = "",
    reviewer: str = "",
    evidence: str = "",
    note: str = "",
    state_path: Path = STATE_PATH,
    scope_key: str | None = None,
) -> QualityGateState:
    if name not in OBLIGATION_ORDER:
        raise ValueError(f"Unknown check: {name}")
    state = read_state(state_path, scope_key=scope_key) or build_state("", [], source="manual")
    obligations = dict(state.obligations)
    current = dict(obligations.get(name) or default_obligation_state())
    current.update(
        {
            "status": status,
            "artifact": compact(artifact or current.get("artifact", ""), limit=260),
            "reviewer": compact(reviewer or current.get("reviewer", ""), limit=120),
            "evidence": compact(evidence or current.get("evidence", ""), limit=260),
            "note": compact(note or current.get("note", ""), limit=220),
            "updated_at": utc_now(),
        }
    )
    obligations[name] = current
    updated = QualityGateState(
        schema_version=SCHEMA_VERSION,
        updated_at=utc_now(),
        prompt_hash=state.prompt_hash,
        prompt_preview=state.prompt_preview,
        obligations=obligations,
        source=state.source or "manual",
    )
    write_state(updated, state_path=state_path, scope_key=scope_key)
    return updated


def status_payload(state_path: Path = STATE_PATH, *, scope_key: str | None = None) -> dict[str, Any]:
    resolved_scope_key = scope_key or current_scope_key()
    state = read_state(state_path, scope_key=resolved_scope_key)
    pending = pending_obligations(state)
    return {
        "status": "pending" if pending else "clear",
        "scope_key": resolved_scope_key,
        "pending": pending,
        "state": asdict(state) if state else None,
        "advisory": stop_advisory(state_path, scope_key=resolved_scope_key),
    }


def run_self_test() -> int:
    cases = [
        ("Build an HTML landing page", ["visual_qa", "design_taste"]),
        ("Create a stakeholder email", ["communication_review"]),
        ("Make a portfolio case-study page", ["visual_qa", "design_taste", "communication_review"]),
        ("Fix this backend bug and run tests", []),
        ("Generate a PDF report", ["visual_qa", "design_taste"]),
        ("Generate a PDF report for stakeholders", ["visual_qa", "design_taste", "communication_review"]),
        ("Set up a Gmail send hook that checks writing skills", []),
        ("Update hook config to mention email, message, image, and app behavior", []),
        ("Create a backend hook to route email messages", []),
        ("Create a config for email message handling", []),
        ("Create an email configuration guide for stakeholders", ["communication_review"]),
        ("Build the app UI for email configuration", ["visual_qa", "design_taste"]),
        ("Write the email copy for the hook configuration notice", ["communication_review"]),
        ("Generate a PDF configuration guide for stakeholders", ["visual_qa", "design_taste", "communication_review"]),
    ]
    failures: list[str] = []
    for prompt, expected in cases:
        actual = detect_obligations(prompt)
        if actual != expected:
            failures.append(f"{prompt!r}: expected {expected}, got {actual}")

    with tempfile.TemporaryDirectory() as tmp:
        state_path = Path(tmp) / "quality.json"
        state = detect_and_store("Build an HTML landing page", state_path=state_path)
        if pending_obligations(state) != ["visual_qa", "design_taste"]:
            failures.append("detect_and_store pending obligations mismatch")
        state = update_obligation(
            "visual_qa",
            status="done",
            reviewer="cua_repl",
            artifact="/tmp/page.html",
            evidence="desktop and mobile screenshots checked",
            state_path=state_path,
        )
        if "visual_qa" in pending_obligations(state):
            failures.append("mark visual_qa did not clear pending")
        state = update_obligation(
            "design_taste",
            status="skipped",
            reviewer="ux-design-toolkit:design-review",
            note="not a user-facing visual artifact",
            state_path=state_path,
        )
        if pending_obligations(state):
            failures.append("skip design_taste did not clear pending")
        clear_state(state_path)
        if status_payload(state_path)["status"] != "clear":
            failures.append("clear did not reset state")
        state_path.write_text("{not-json")
        if status_payload(state_path)["status"] != "clear":
            failures.append("corrupt state did not fail open")

    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1
    print("codex_artifact_quality_gate self-test passed")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--state-path", type=Path, default=STATE_PATH)
    parser.add_argument("--json", action="store_true")
    subparsers = parser.add_subparsers(dest="command")

    detect = subparsers.add_parser("detect")
    detect.add_argument("prompt", nargs="*")
    detect.add_argument("--state-path", type=Path, default=STATE_PATH)
    detect.add_argument("--json", action="store_true")

    mark = subparsers.add_parser("mark")
    mark.add_argument("check", choices=OBLIGATION_ORDER)
    mark.add_argument("--artifact", default="")
    mark.add_argument("--reviewer", required=True)
    mark.add_argument("--evidence", required=True)
    mark.add_argument("--note", default="")
    mark.add_argument("--state-path", type=Path, default=STATE_PATH)
    mark.add_argument("--json", action="store_true")

    skip = subparsers.add_parser("skip")
    skip.add_argument("check", choices=OBLIGATION_ORDER)
    skip.add_argument("--reason", required=True)
    skip.add_argument("--reviewer", default="codex")
    skip.add_argument("--artifact", default="")
    skip.add_argument("--state-path", type=Path, default=STATE_PATH)
    skip.add_argument("--json", action="store_true")

    status = subparsers.add_parser("status")
    status.add_argument("--state-path", type=Path, default=STATE_PATH)
    status.add_argument("--json", action="store_true")

    clear = subparsers.add_parser("clear")
    clear.add_argument("--state-path", type=Path, default=STATE_PATH)
    clear.add_argument("--json", action="store_true")
    return parser


def emit(payload: Any, *, json_mode: bool) -> None:
    if json_mode:
        if isinstance(payload, QualityGateState):
            payload = asdict(payload)
        print(json.dumps(payload, indent=2, sort_keys=True))
        return
    if isinstance(payload, QualityGateState):
        pending = pending_obligations(payload)
        if pending:
            print(quality_guidance(pending))
    elif isinstance(payload, dict):
        advisory = payload.get("advisory")
        if advisory:
            print(advisory)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.self_test:
        return run_self_test()
    if not args.command:
        parser.print_help()
        return 2

    if args.command == "detect":
        prompt = normalize_text(" ".join(args.prompt))
        state = detect_and_store(prompt, state_path=args.state_path)
        emit(state, json_mode=args.json)
    elif args.command == "mark":
        state = update_obligation(
            args.check,
            status="done",
            artifact=args.artifact,
            reviewer=args.reviewer,
            evidence=args.evidence,
            note=args.note,
            state_path=args.state_path,
        )
        emit(status_payload(args.state_path), json_mode=args.json)
    elif args.command == "skip":
        state = update_obligation(
            args.check,
            status="skipped",
            artifact=args.artifact,
            reviewer=args.reviewer,
            evidence=args.reason,
            note=args.reason,
            state_path=args.state_path,
        )
        emit(status_payload(args.state_path), json_mode=args.json)
    elif args.command == "status":
        emit(status_payload(args.state_path), json_mode=args.json)
    elif args.command == "clear":
        clear_state(args.state_path)
        emit(status_payload(args.state_path), json_mode=args.json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
