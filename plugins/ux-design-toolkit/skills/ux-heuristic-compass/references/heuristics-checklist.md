# UXHC Heuristics Checklist Reference

This reference is the compact standalone rubric for UX Heuristics Compass. Use it when the MCP is unavailable, when explaining the rubric, or when drafting host prompts.

## What The Audit Scores

UXHC scores visible or documented usability issues in an interface. It does not score the people who built the interface, the product's total value, or whether the design is legally compliant.

The score asks: given the evidence available, how severe are the visible usability issues?

## Rating Scale

Every active checklist item receives one severity rating.

| Score | Meaning | Use when |
| ---: | --- | --- |
| 0 | No issue | The evidence shows the item is handled well or no visible problem appears. |
| 1 | Cosmetic | The issue is small, low-friction, or mainly polish. Fix if time permits. |
| 2 | Minor | The issue may slow or confuse users but probably does not block the task. |
| 3 | Major | The issue creates meaningful friction, uncertainty, exclusion, or recovery trouble. |
| 4 | Catastrophic | The issue can block the task, cause serious error, or make the experience near-unusable. |

Higher quality percentages mean better UX quality. Severe issues lower the score.

## Core Heuristics

| ID | Heuristic | What To Look For |
| --- | --- | --- |
| H1 | Visibility of System Status | The interface keeps users informed about where they are, what changed, what is loading, and what happened after an action. |
| H2 | Match Between System and the Real World | Labels, concepts, ordering, and language match the user's mental model instead of internal system terms. |
| H3 | User Control and Freedom | Users can undo, cancel, go back, exit, recover, or change direction without feeling trapped. |
| H4 | Consistency and Standards | Similar things look and behave similarly, and the interface follows familiar platform and web conventions. |
| H5 | Error Prevention | The design helps users avoid mistakes before they happen, especially destructive or hard-to-recover errors. |
| H6 | Recognition Rather Than Recall | The interface shows useful choices, labels, context, and instructions instead of forcing users to remember hidden information. |
| H7 | Flexibility and Efficiency of Use | The design supports both new and experienced users through shortcuts, efficient paths, defaults, and adaptable workflows. Calibrate severity against the user's ability cost: low bandwidth, mobile-only access, low literacy, cognitive load, or time pressure can turn a small friction into a major issue. |
| H8 | Aesthetic and Minimalist Design | The screen reduces clutter, prioritizes what matters, and avoids making low-value content compete with core actions. |
| H9 | Help Users Recognize, Diagnose, and Recover From Errors | Error states are visible, understandable, specific, and paired with a clear recovery path. |
| H10 | Help and Documentation | Help, instructions, and support content are easy to find, task-relevant, and not a substitute for a broken core flow. |

## Optional General Profiles

These are first-class optional heuristics. Include them when the user asks for expanded coverage, when the interface materially raises those issues, or when the MCP/user selects the corresponding profile.

| ID | Profile ID | Accepted Aliases | Heuristic | Use when |
| --- | --- | --- | --- | --- |
| H11 | `accessibility` | `a11y` | Accessibility and Ease of Access | The audit should consider keyboard, readable text, contrast, form affordances, focus, captions, sensory assumptions, or ease of access. If H11 has severity 3-4 findings, hand off to a real accessibility/WCAG review; UXHC is not a compliance audit. |
| H12 | `inclusion` | `empathy` | Empathetic Engagement and Inclusion | The experience may affect users with different emotional states, identities, contexts, abilities, language backgrounds, or safety needs. Permanent, temporary, and situational constraints can produce the same usability barrier. |
| H13 | `journey` | `cx` | Customer Journey and Satisfaction | The audit needs to consider whether the screen fits the broader task journey, expectation, handoff, or service moment. Use audience ability and task stakes to calibrate journey severity, especially when a small friction compounds across steps. |
| H14 | `ux_writing` | `content_strategy` | UX Writing / Content and Tone | Labels, microcopy, instructions, error messages, empty states, or tone may affect comprehension and trust. |

When `quick_scan_ux` or `audit_ux_surface` is called without optional profiles, the MCP returns `audit_scope_lock` listing the omitted profiles and instructions for re-running with expanded coverage. Surface this to the user before summarizing audit results.

## Checklist Counts

Use these counts when explaining scope. Do not invent additional baseline checklist items.

| ID | Heuristic | Desktop items | Mobile items |
| --- | --- | ---: | ---: |
| H1 | Visibility of System Status | 9 | 9 |
| H2 | Match Between System and the Real World | 3 | 3 |
| H3 | User Control and Freedom | 5 | 5 |
| H4 | Consistency and Standards | 21 | 21 |
| H5 | Error Prevention | 5 | 5 |
| H6 | Recognition Rather Than Recall | 4 | 4 |
| H7 | Flexibility and Efficiency of Use | 9 | 9 |
| H8 | Aesthetic and Minimalist Design | 16 | 16 |
| H9 | Help Users Recognize, Diagnose, and Recover From Errors | 2 | 2 |
| H10 | Help and Documentation | 5 | 5 |
| H11 | Accessibility and Ease of Access | 4 | 4 |
| H12 | Empathetic Engagement and Inclusion | 6 | 6 |
| H13 | Customer Journey and Satisfaction | 6 | 6 |
| H14 | UX Writing / Content and Tone | 7 | 7 |

Core scope is H1-H10. Expanded scope can include H11-H14. Full dual-platform all-optionals coverage is 204 checklist items.

## Checklist ID Pattern

Checklist IDs follow this shape:

```text
h{heuristic_number_zero_padded}_{platform_initial}_{item_index_zero_padded}
```

Examples:

- `h01_d_01` means H1 desktop item 1.
- `h07_m_09` means H7 mobile item 9.
- `h11_d_01` means H11 desktop item 1.

Use the MCP for exact checklist IDs and item text. In standalone mode, name the heuristic and evidence clearly even when you do not know the exact checklist ID.

## Evidence Limits

Always name evidence limits. Common limits:

- screenshot does not show hover, focus, loading, visited, disabled, or error states
- mobile and desktop states are not both available
- page capture is cropped, low-resolution, stale, or partially hidden
- task flow is inferred from one screen
- user goal, audience, or success criteria are missing
- code suggests an issue but rendered behavior was not observed

Do not score hidden states with high confidence. If a state is not visible, either ask for more evidence or mark the rating as low confidence.

## Attributed optional-profile observation prompts

For H11–H13 standalone observations, read [the complete attributed prompts](../../design-studio/references/human-systems/optional-heuristic-observations.md). These do not add checklist items, alter MCP scores/counts, rename existing profiles or claim official Nielsen status. Keep MCP rubric behavior separate from these additional inspection questions.
