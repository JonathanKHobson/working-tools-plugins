# Idea to Spec

Use this file when the user has described a feature, workflow, or product direction but not yet a buildable requirement.

## Five-Field Minimum

Always structure the result with:

```markdown
PROBLEM:
USER:
OUTCOME:
RULES:
DONE MEANS:
OPEN QUESTIONS:
```

Do not skip `OPEN QUESTIONS` when key policy or flow details are missing.

## Structural Checklist

Work through these categories and only keep the ones that matter to the request:

### 1. Problem
- What user or business problem is being solved?
- Is the problem validated, observed, or assumed?
- Is this a symptom or the root problem?

### 2. Outcome
- What changes for the user?
- What changes for the business?
- How will success be measured?

### 3. User
- Who is the primary user?
- What role, account state, or permission level matters?
- What device or environment matters?

### 4. Scope
- What is in scope now?
- What is explicitly out of scope?
- Is this MVP, V1, or future-state thinking?

### 5. Flow
- Entry point
- Main path
- Alternate paths
- Exit point
- Save, resume, cancel, refresh, or back-button behavior

### 6. Rules
- Allowed behavior
- Forbidden behavior
- Validation logic
- Defaults
- Limits
- Role, plan, geography, or account-based differences

### 7. States
Call out the states that must be designed or implemented:
- default
- hover or focus
- active or selected
- disabled
- loading
- success
- error
- empty
- partial completion
- offline or expired session
- conflict or concurrent edit

### 8. Content
- final copy vs placeholder copy
- helper text
- confirmation text
- error text
- notification text
- emails or side-channel messaging triggered by the flow

### 9. Technical Constraints
- browser or device support
- latency or real-time expectations
- integrations and source of truth
- analytics events
- security or privacy needs
- accessibility requirements
- localization needs

### 10. Acceptance
Write done criteria in a verifiable form:

`When [user] does [action], the system [behavior], and [outcome is verifiable].`

## Vague Adjective Translator

Convert vague product language into decision-ready questions or measurable conditions:

| They say | Translate into |
| --- | --- |
| Easy | Which friction is reduced: clicks, typing, decision load, wait time, or perceived risk? |
| Intuitive | Which familiar mental model should it match? |
| Seamless | What transition, latency, persistence, or auth behavior must feel uninterrupted? |
| Smart | What inputs, rules, model behavior, confidence threshold, and fallback exist? |
| Flexible | Which cases vary, for whom, and where are the guardrails? |
| Customizable | What can change, where is it saved, what are the defaults, and how does reset work? |
| Real-time | What latency target, polling interval, or push behavior is expected? |
| Simple | What gets removed, hidden, or defaulted? |
| Clean | What visual or content density is being reduced? |
| Premium | Which qualities matter: motion, typography, copy tone, responsiveness, or polish? |

## Common Translation Failures

Watch for these failure modes and fix them explicitly:
- solution before problem
- subjective words treated as requirements
- screens without interaction logic
- missing rationale
- one happy path treated as universal
- no distinction between critical, preferred, and flexible details
- missing loading, error, and empty states
- research insight mistaken for product requirement
- placeholder content mistaken for real content
- accessibility treated as optional polish
- no acceptance criteria
- no shared vocabulary across teams

## Critical / Preferred / Flexible

Use these labels when the request mixes hard requirements and design preferences:
- `Critical`: do not change without discussion
- `Preferred`: aim for this unless there is a real constraint
- `Flexible`: implementation choice does not materially change the user experience

## Output Rules

- Separate the observed problem from the proposed UI solution.
- Name only the open questions that would change implementation.
- Do not invent validation rules, role matrices, or integration policy unless the request establishes them.
- If acceptance criteria are missing, write the minimum viable version and flag the rest as open questions.
