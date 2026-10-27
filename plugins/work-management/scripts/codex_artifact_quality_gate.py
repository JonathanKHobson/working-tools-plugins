#!/usr/bin/env python3
"""Scoped artifact quality evidence gate for Codex hooks and manual closeout.

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
    "visual_qa": "Inspect the actual rendered artifact using the available native app/browser tools (cua_repl for computer use) or document/PDF rendering tools; map 3–8 visual anchors and verify changed regions and relevant states. Extraction alone is not visual QA. Read " + str(Path(__file__).resolve().parents[1] / "references/operations/artifact-quality-evidence.md") + " for the required scoped receipt and verification procedure.",
    "design_taste": "Use ux-design-toolkit:design-review for interfaces, graphic-design-studio:graphic-design-review for graphics, or figma-design-workflow:design-visual-qa for Figma/Stitch handoffs. Review usability, accessibility, states and visual craft against the accepted direction; cite observed anchor IDs and untested behavior.",
    "communication_review": "Use Writing Quality Studio: writing-quality-studio:natural-prose-editor for routine copy; writing-quality-studio:communication-crafter for strategic messages, audience, evidence, tone and intended action. Reuse completed reviews for unchanged drafts.",
}
COMMUNICATION_REVIEWER = "writing-quality-studio:natural-prose-editor"

VISUAL_RE = re.compile(
    r"\b("
    r"app|artifact|brochure|canvas|component|dashboard|deck|docx?|figma|flyer|"
    r"frontend|html|image|interface|landing page|mockup|page|pdf|poster|prototype|"
    r"screen|screenshot|shareable|site|slide|ui|visual|web app|website"
    r")\b",
    re.IGNORECASE,
)
VISUAL_VERB_RE = re.compile(
    r"\b(build|create|design|edit|fix|generate|make|polish|produce|render|repair|restore|ship|stage|update|write)\b",
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
    previous = read_state(state_path, scope_key=scope_key)
    unresolved = {name: data for name, data in (previous.obligations.items() if previous else [])
                  if name in OBLIGATION_ORDER and obligation_errors(name, data)}
    state = build_state(prompt, obligations, source="prompt-submit")
    combined = dict(unresolved)
    combined.update(state.obligations)
    state = QualityGateState(**{**asdict(state), "obligations": combined})
    write_state(state, state_path=state_path, scope_key=scope_key)
    return state


REVIEW_CATEGORIES = ('accessibility', 'usability', 'qa', 'aesthetics')
VISUAL_CHECKS = {'visual_qa', 'design_taste'}


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def contrast_ratio(foreground: str, background: str) -> float:
    """Opaque sRGB colors only; compositing/gradients need resolved backgrounds."""
    def luminance(color: str) -> float:
        if not isinstance(color, str) or not re.fullmatch(r'#[0-9a-fA-F]{6}', color):
            raise ValueError('Contrast needs resolved opaque #rrggbb colors')
        channels = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
        linear = [c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4 for c in channels]
        return sum(c * w for c, w in zip(linear, (.2126, .7152, .0722)))
    a, b = sorted((luminance(foreground), luminance(background)))
    return (b + .05) / (a + .05)


def _validate_review(evidence: str) -> list[str]:
    """Validate scoped receipts, not the truth of reviewer claims or conformance."""
    errors: list[str] = []
    try:
        report_path = Path(evidence).expanduser()
        report = json.loads(report_path.read_text())
        if not isinstance(report, dict) or report.get('schema_version') != 1:
            return ['Review requires supported schema_version 1']
    except (OSError, ValueError, TypeError):
        return ['Visual completion requires a readable structured JSON review report']
    kind = report.get('artifact_kind')
    if kind not in {'interface', 'document', 'graphic'}:
        errors.append('Unsupported or missing artifact_kind')
    files = report.get('files')
    roles: dict[str, str] = {}
    if not isinstance(files, list) or not files:
        errors.append('Missing source and rendered file fingerprints')
        files = []
    for entry in files:
        if not isinstance(entry, dict):
            errors.append('Invalid file fingerprint')
            continue
        path = Path(str(entry.get('path', ''))).expanduser()
        role = entry.get('role')
        if not path.is_absolute() or role not in {'source', 'render', 'measurement'}:
            errors.append('Files need absolute paths and source/render/measurement roles')
            continue
        roles[str(path)] = role
        try:
            if file_digest(path) != entry.get('sha256'):
                errors.append(f'Stale fingerprint: {path}')
        except OSError:
            errors.append(f'Missing evidence file: {path}')
    for role in ('source', 'render'):
        if role not in roles.values():
            errors.append(f'Missing {role} fingerprint')
    scope = report.get('scope', {})
    if not isinstance(scope, dict):
        scope = {}
    regions, states = scope.get('regions'), scope.get('states')
    def names(value: Any) -> list[str]:
        return value if isinstance(value, list) and value and all(isinstance(v, str) and v.strip() for v in value) else []
    regions, states = names(regions), names(states)
    if not regions or not states:
        errors.append('Scope requires nonempty region and state inventories')
    exclusions = scope.get('exclusions', [])
    excluded: set[str] = set()
    if not isinstance(exclusions, list):
        errors.append('Scope exclusions must be a list')
        exclusions = []
    for exclusion in exclusions:
        if not isinstance(exclusion, dict) or not normalize_text(exclusion.get('scope')) or not normalize_text(exclusion.get('reason')):
            errors.append('Each scope exclusion needs a scope and concrete reason')
        else:
            excluded.add(exclusion['scope'])
    # These applicability decisions prevent silently omitting responsive/theme states.
    if kind == 'interface':
        for dimension in ('responsive', 'themes'):
            decision = scope.get(dimension)
            if not isinstance(decision, dict) or not isinstance(decision.get('applicable'), bool) or not normalize_text(decision.get('reason')):
                errors.append(f'Interface scope needs a reasoned {dimension} applicability decision')
            elif decision['applicable']:
                selected = names(decision.get('states'))
                if len(set(selected)) < 2 or not set(selected).issubset(states):
                    errors.append(f'Applicable {dimension} needs at least two named scoped states')
    checks = report.get('checks', {})
    if not isinstance(checks, dict):
        checks = {}
    for category in REVIEW_CATEGORIES:
        check = checks.get(category)
        if not isinstance(check, dict):
            errors.append(f'Missing category: {category}')
            continue
        status = check.get('status')
        if status == 'not_applicable' and category != 'aesthetics' and kind != 'interface':
            if not normalize_text(check.get('reason')):
                errors.append(f'{category}: not_applicable needs a reason')
        elif status != 'pass' or not normalize_text(check.get('evidence')):
            errors.append(f'{category}: requires passing observed evidence (got {status!r})')
    coverage = report.get('coverage', [])
    if not isinstance(coverage, list):
        coverage = []
    seen: set[tuple[str, str]] = set()
    required_targets: set[tuple[str, str, str]] = set()
    for entry in coverage:
        if not isinstance(entry, dict):
            errors.append('Invalid coverage entry')
            continue
        region, state = entry.get('region'), entry.get('state')
        if region not in regions or state not in states:
            errors.append('Coverage references undeclared region/state')
            continue
        seen.add((region, state))
        if roles.get(entry.get('render')) != 'render':
            errors.append(f'{region}@{state}: missing fingerprinted rendered proof')
        targets = names(entry.get('text_targets'))
        if not targets and not normalize_text(entry.get('no_text_reason')):
            errors.append(f'{region}@{state}: inventory visible descendant text targets or explain no text')
        required_targets.update((region, state, target) for target in targets)
    for region in regions:
        for state in states:
            if (region, state) not in seen and f'{region}@{state}' not in excluded:
                errors.append(f'Missing rendered coverage: {region}@{state}')
    samples = report.get('contrast', [])
    if not isinstance(samples, list):
        samples = []
    measured: set[tuple[str, str, str]] = set()
    for sample in samples:
        if not isinstance(sample, dict):
            errors.append('Invalid contrast sample')
            continue
        key = (sample.get('region'), sample.get('state'), sample.get('target'))
        if key not in required_targets:
            errors.append('Contrast sample references an undeclared text target')
            continue
        measured.add(key)
        try:
            size, weight = float(sample['font_size_px']), float(sample['font_weight'])
            if not 0 < size < 10000 or not 0 < weight <= 1000:
                raise ValueError('Invalid font metrics')
            threshold = 3.0 if size >= 24 or (size >= 18.6666666667 and weight >= 700) else 4.5
            ratio = contrast_ratio(sample['foreground'], sample['background'])
            if ratio < threshold:
                errors.append(f'Contrast failed {key}: {ratio:.2f}:1 < {threshold}:1')
        except (KeyError, TypeError, ValueError):
            errors.append(f'Unsupported or incomplete computed contrast sample: {key}')
    for key in sorted(required_targets - measured):
        errors.append(f'Missing descendant contrast measurement: {key}')
    if report.get('blockers') not in (None, []):
        errors.append('Unresolved review blockers')
    return errors


def validate_review(evidence: str) -> list[str]:
    try:
        return _validate_review(evidence)
    except (KeyError, TypeError, ValueError, OverflowError) as error:
        return [f'Malformed review evidence: {type(error).__name__}']


def obligation_errors(name: str, data: Any) -> list[str]:
    if not isinstance(data, dict):
        return ['Missing obligation record']
    status = data.get('status')
    if status == 'skipped':
        return [] if normalize_text(data.get('note')) else ['Not-applicable decision needs a reason']
    if status != 'done':
        return [f'Unresolved status: {status}']
    if not normalize_text(data.get('reviewer')) or not normalize_text(data.get('evidence')):
        return ['Missing reviewer/evidence']
    if name in VISUAL_CHECKS:
        evidence = data.get('evidence', '')
        errors = validate_review(evidence)
        if errors:
            return errors
        try:
            if file_digest(Path(evidence).expanduser()) != data.get('evidence_sha256'):
                errors.append('Review report changed or lacks a recorded fingerprint; re-review and mark')
        except OSError:
            pass  # validate_review already reports inaccessible evidence.
        return errors
    if name == 'communication_review':
        if data.get('reviewer') != COMMUNICATION_REVIEWER:
            return ['Communication review needs writing-quality-studio:natural-prose-editor']
        artifact = Path(str(data.get('artifact', ''))).expanduser()
        if not artifact.is_absolute() or not data.get('artifact_sha256'):
            return ['Communication mark lacks a fingerprinted final local artifact; re-review and mark']
        try:
            if file_digest(artifact) != data['artifact_sha256']:
                return ['Final communication artifact changed; re-review and mark']
        except OSError:
            return ['Final communication artifact is missing; re-review and mark']
    return []

def pending_obligations(state: QualityGateState | None) -> list[str]:
    if state is None:
        return []
    pending: list[str] = []
    for name in OBLIGATION_ORDER:
        data = state.obligations.get(name)
        if data is not None and obligation_errors(name, data):
            pending.append(name)
    return pending


def quality_guidance(obligations: list[str]) -> str:
    if not obligations:
        return ""
    labels = ", ".join(OBLIGATION_LABELS[name] for name in obligations)
    return (
        f"Artifact quality gate: if you produce this artifact, run/mark {labels} before final. "
        "For screenshot or rendered-surface review, use a compact visual anchor map. "
        "Use `codex_artifact_quality_gate.py mark <check> --artifact ... --reviewer ... --evidence ...` "
        "For visual checks --evidence must point to a fingerprinted structured review JSON. "
        "Use `verify --json` before a completion claim or native goal completion; "
        "skip only for a reasoned not-applicable decision."
    )


def stop_advisory(state_path: Path = STATE_PATH, *, scope_key: str | None = None) -> str:
    state = read_state(state_path, scope_key=scope_key)
    pending = pending_obligations(state)
    if not pending:
        return ""
    return pending_advisory(pending)


def pending_advisory(pending: list[str]) -> str:
    if not pending:
        return ""
    labels = ", ".join(OBLIGATION_LABELS[name] for name in pending)
    routes = []
    if 'visual_qa' in pending:
        routes.append('rendered visual QA')
    if 'design_taste' in pending:
        routes.append('ux-design-toolkit:design-review, graphic-design-studio:graphic-design-review or figma-design-workflow:design-visual-qa')
    if 'communication_review' in pending:
        routes.append(COMMUNICATION_REVIEWER)
    return (f"Artifact quality gate pending: {labels}. Check {Path(__file__).name} status --json; "
            f"use {', '.join(routes)}, then mark with final evidence or reasoned skip.")


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
    if status not in {'pending', 'done', 'failed', 'skipped'}:
        raise ValueError(f"Unsupported status: {status}")
    if status == 'skipped' and not normalize_text(note):
        raise ValueError('Skipping a check requires a concrete not-applicable reason')
    if status == 'done' and (not normalize_text(reviewer) or not normalize_text(evidence)):
        raise ValueError('Completion requires reviewer and evidence')
    if status == 'done' and name in VISUAL_CHECKS:
        errors = validate_review(evidence)
        if errors:
            raise ValueError('; '.join(errors))
    artifact_sha256 = None
    if status == 'done' and name == 'communication_review':
        if reviewer != COMMUNICATION_REVIEWER:
            raise ValueError(f'Communication completion requires reviewer {COMMUNICATION_REVIEWER}')
        artifact_path = Path(artifact).expanduser()
        if not artifact_path.is_absolute() or not artifact_path.is_file():
            raise ValueError('Communication completion requires an existing absolute final local artifact path')
        artifact_sha256 = file_digest(artifact_path)
    state = read_state(state_path, scope_key=scope_key) or build_state("", [], source="manual")
    obligations = dict(state.obligations)
    current = dict(obligations.get(name) or default_obligation_state())
    review_evidence_sha256 = hashlib.sha256(evidence.encode('utf-8')).hexdigest() if artifact_sha256 is not None else None
    current.update(
        {
            "status": status,
            "artifact": compact(artifact or current.get("artifact", ""), limit=260),
            "reviewer": compact(reviewer or current.get("reviewer", ""), limit=120),
            "evidence": evidence if name in VISUAL_CHECKS else compact(evidence or current.get("evidence", ""), limit=260),
            "note": compact(note or current.get("note", ""), limit=220),
            "updated_at": utc_now(),
        }
    )
    if status == 'done' and name in VISUAL_CHECKS:
        current['evidence_sha256'] = file_digest(Path(evidence).expanduser())
    if artifact_sha256 is not None:
        current['artifact'] = str(Path(artifact).expanduser())
        current['artifact_sha256'] = artifact_sha256
        current['review_evidence_sha256'] = review_evidence_sha256
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
    if state_path.exists():
        try:
            raw = json.loads(state_path.read_text())
            if not isinstance(raw, dict) or not isinstance(raw.get('scopes', raw.get('obligations')), dict):
                raise ValueError('Invalid state structure')
            scopes = raw.get('scopes', {})
            if resolved_scope_key in scopes and parse_state(scopes[resolved_scope_key]) is None:
                raise ValueError('Invalid current scope state')
        except (OSError, ValueError, TypeError):
            return {"status": "pending", "scope_key": resolved_scope_key,
                    "pending": ["state_integrity"], "state": None,
                    "errors": {"state_integrity": ["Unreadable quality state; recover or reassess scoped obligations"]},
                    "advisory": "Artifact review state is unreadable; recover or reassess the current scope before completion."}
    state = read_state(state_path, scope_key=resolved_scope_key)
    errors = {name: problems for name, data in (state.obligations.items() if state else [])
              if name in OBLIGATION_ORDER and (problems := obligation_errors(name, data))}
    pending = [name for name in OBLIGATION_ORDER if name in errors]
    return {
        "status": "pending" if pending else "clear",
        "scope_key": resolved_scope_key,
        "pending": pending,
        "errors": errors,
        "state": asdict(state) if state else None,
        "advisory": pending_advisory(pending),
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
        communication_artifact = Path(tmp) / 'final-email.txt'
        communication_artifact.write_text('Example final copy')
        state = update_obligation(
            "communication_review",
            status="done",
            reviewer=COMMUNICATION_REVIEWER,
            artifact=str(communication_artifact),
            evidence="Reviewed final copy for natural phrasing and clarity",
            state_path=state_path,
        )
        if "communication_review" in pending_obligations(state):
            failures.append("mark communication_review did not clear pending")
        state = update_obligation("visual_qa", status="skipped", note="Test-only nonvisual scope", state_path=state_path)
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
        if status_payload(state_path)["status"] != "pending":
            failures.append("corrupt state did not retain a review blocker")

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

    verify = subparsers.add_parser("verify", help="Exit nonzero when scoped review obligations are unresolved")
    verify.add_argument("--state-path", type=Path, default=STATE_PATH)
    verify.add_argument("--json", action="store_true")

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
    elif args.command == "verify":
        payload = status_payload(args.state_path)
        if payload['state'] is None and not payload['pending']:
            payload.update(status='unassessed', advisory='Assess this session scope with detect or a reasoned manual review before completion.')
        emit(payload, json_mode=args.json)
        return 1 if payload['pending'] or payload['state'] is None else 0
    elif args.command == "status":
        emit(status_payload(args.state_path), json_mode=args.json)
    elif args.command == "clear":
        clear_state(args.state_path)
        emit(status_payload(args.state_path), json_mode=args.json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
