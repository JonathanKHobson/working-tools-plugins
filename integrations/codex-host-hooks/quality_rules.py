# SPDX-License-Identifier: AGPL-3.0-only
"""Portable operative classifier and review routing, adapted from author source."""
import re
from typing import Any

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

def normalize_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()

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
