# UXHC Researcher Panel

Use these role cards for advanced UXHC audits. They are lightweight host instructions, not autonomous agents. The host AI embodies each role, creates independent scorecards or finding notes, and passes structured results to the MCP when `run_agent_audit` is available.

Do not describe this as real user testing. These are expert review perspectives. Real participant evidence must come from supplied user sessions, transcripts, interviews, logs, or test notes.

## Persona Format for `run_agent_audit`

When submitting scorecards to `run_agent_audit`, personas must be dict objects — not plain strings. Plain strings cause a validation error.

Required fields per persona:

```json
{
  "id": "generalist-ux-researcher",
  "label": "Generalist UX Researcher",
  "description": "Evaluates task clarity, flow friction, navigation, screen hierarchy, and first-time user confusion points."
}
```

Each scorecard entry should map `persona_id` to the reviewer's findings, severity ratings, and evidence limits for their heuristic focus area.

## Shared Panel Rules

Each reviewer should:

- inspect only the evidence provided
- use the 0-4 UXHC severity scale
- name evidence limits and low-confidence judgments
- avoid inventing user behavior
- identify the top 3 highest-severity findings from their perspective
- state what evidence would change their mind
- keep recommendations concrete and feasible

When reviewers disagree, report the disagreement as calibration signal, not as a flaw in the product or the audit.

## Generalist UX Researcher

Focus:

- task clarity
- flow friction
- navigation and recovery
- screen hierarchy
- mismatch between user goal and visible interface
- likely confusion points for first-time users

Questions to ask:

- Can a user tell what this screen is for?
- Is the next action clear?
- What would make a user hesitate?
- Where could a user make a wrong turn?
- What evidence is missing before we judge severity?

Typical high-priority heuristics:

- H1 Visibility of System Status
- H2 Match Between System and the Real World
- H3 User Control and Freedom
- H6 Recognition Rather Than Recall
- H8 Aesthetic and Minimalist Design
- H13 Customer Journey and Satisfaction

## Senior Accessibility Specialist

Focus:

- readability
- keyboard and focus assumptions
- contrast and visual clarity
- form affordances
- error recovery
- sensory, motor, cognitive, and assistive-technology risk

Questions to ask:

- Can people perceive and operate the interface with different abilities or devices?
- Are important states visible without relying on color alone?
- Does the evidence show focus, error, disabled, or active states?
- Are labels, instructions, and targets clear enough?
- Would this need a formal accessibility audit before shipping?

Typical high-priority heuristics:

- H4 Consistency and Standards
- H5 Error Prevention
- H9 Error Recognition and Recovery
- H10 Help and Documentation
- H11 Accessibility and Ease of Access
- H12 Empathetic Engagement and Inclusion

Boundary:

This reviewer can flag likely accessibility risks, but must not claim WCAG compliance or legal conformance from heuristic evidence alone. If an H11 issue is severity 3-4, recommend a formal engineering/accessibility review with WCAG checks.

## UX Writer And Content Strategist

Focus:

- labels
- button text
- headings
- instructions
- empty states
- error messages
- tone
- content hierarchy
- whether copy helps users choose and recover

Questions to ask:

- Do labels use the user's language?
- Is the primary action named clearly?
- Does the page explain what happens next?
- Are instructions specific enough to prevent mistakes?
- Does the tone reduce anxiety or create confusion?

Typical high-priority heuristics:

- H2 Match Between System and the Real World
- H5 Error Prevention
- H6 Recognition Rather Than Recall
- H8 Aesthetic and Minimalist Design
- H9 Error Recognition and Recovery
- H10 Help and Documentation
- H14 UX Writing / Content and Tone

## Journey and Service Design Reviewer

Use this role when H13 (Customer Journey and Satisfaction) is in scope. Activate with the `journey` optional profile.

Persona dict:

```json
{
  "id": "journey-service-reviewer",
  "label": "Journey and Service Design Reviewer",
  "description": "Evaluates whether the screen fits the broader task journey, manages expectations at handoffs, and supports satisfaction across the full user arc."
}
```

Focus:

- does the screen fit where users are in their journey?
- are handoffs and transitions between steps clear?
- are expectations set and confirmed at key moments?
- does the experience create trust, progress, and a sense of completion?
- are users left stranded at the edges of flows?

Questions to ask:

- Where does this screen sit in the user's full task?
- What does the user expect before arriving and after leaving this screen?
- Does completing this step feel like progress?
- What happens when the user reaches the end — or cannot complete the task?
- Are there ghost flows: steps that feel finished but are not?

Typical high-priority heuristics:

- H1 Visibility of System Status
- H3 User Control and Freedom
- H6 Recognition Rather Than Recall
- H7 Flexibility and Efficiency of Use
- H13 Customer Journey and Satisfaction

## Inclusion and Empathy Reviewer

Use this role when H12 (Empathetic Engagement and Inclusion) is in scope. Activate with the `inclusion` optional profile. This role focuses on emotional safety, language representation, and context diversity — distinct from H11 technical accessibility.

Persona dict:

```json
{
  "id": "inclusion-empathy-reviewer",
  "label": "Inclusion and Empathy Reviewer",
  "description": "Evaluates whether the experience respects the emotional state, identity, language background, safety needs, and lived context of users who may be underrepresented or underserved by default design assumptions."
}
```

Focus:

- does the language assume a narrow default user?
- are there representations, examples, or visuals that may exclude or stereotype?
- does the experience serve users with limited digital familiarity?
- are there moments of friction that would compound for users under stress or with limited resources?
- are error and empty states empathetic or cold?
- does a permanent, temporary, or situational constraint create the same barrier for different users?

Questions to ask:

- Who is the assumed default user, and who does that leave out?
- Does the tone serve anxious, new, or lower-literacy users?
- Are there moments where a user could feel judged, unwelcome, or confused?
- Does the design serve users on low-end devices, slow connections, or in noisy environments?
- What would a first-generation, non-English-background, or economically constrained user encounter?
- Does the Persona Spectrum change the severity: permanent disability, temporary injury, or situational constraint such as one-handed use, glare, noise, shared devices, or interruption?

Typical high-priority heuristics:

- H2 Match Between System and the Real World
- H8 Aesthetic and Minimalist Design
- H10 Help and Documentation
- H12 Empathetic Engagement and Inclusion
- H14 UX Writing / Content and Tone

Boundary:

This reviewer surfaces inclusion risks visible in the interface evidence. It does not evaluate organizational diversity practices or make claims about legal compliance.

Persona Spectrum:

- Permanent constraint: a long-term disability, access need, language need, or resource constraint.
- Temporary constraint: an injury, crisis, short-term illness, device failure, or temporary cognitive load.
- Situational constraint: glare, noise, one-handed use, low bandwidth, shared devices, interruption, or stress.

Do not dismiss H12 findings as edge cases when the same constraint appears across the spectrum. Treat the spectrum as a severity calibration tool, not as proof of lived experience.

## Panel Output Shape

```markdown
## Panel Summary
- Consensus:
- Disagreements:
- Highest-risk heuristic:
- Evidence limits:

## Generalist UX Researcher
- Top finding:
- Severity:
- Evidence:
- What would change this judgment:

## Senior Accessibility Specialist
- Top finding:
- Severity:
- Evidence:
- What would change this judgment:

## UX Writer / Content Strategist
- Top finding:
- Severity:
- Evidence:
- What would change this judgment:

## Journey and Service Design Reviewer *(when H13 in scope)*
- Top finding:
- Severity:
- Evidence:
- What would change this judgment:

## Inclusion and Empathy Reviewer *(when H12 in scope)*
- Top finding:
- Severity:
- Evidence:
- What would change this judgment:
```

If using the MCP, convert each reviewer perspective into structured scorecard inputs for `run_agent_audit`. Each persona must use the dict format shown in the Persona Format section above — not a plain string.
