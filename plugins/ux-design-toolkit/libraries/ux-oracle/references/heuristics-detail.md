# UX Oracle Heuristics Detail

## Contents

- Severity scale
- Nielsen heuristics
- Cognitive and physical laws
- Emotional heuristics
- Finding template

## Severity scale

Use a 1-5 severity scale where `5` means pass and `1` means catastrophic failure.

| Score | Meaning | Typical urgency |
|---|---|---|
| 5 | Pass | No action required |
| 4 | Cosmetic issue | Fix when convenient |
| 3 | Minor issue | Fix soon if the flow matters |
| 2 | Major issue | High priority |
| 1 | Catastrophic issue | Immediate attention |

## Nielsen heuristics

### 1. Visibility of system status

- Check whether the system shows progress, saving, loading, completion, and failure states promptly.
- Flag missing feedback, silent waits, and ambiguous success states.

### 2. Match between system and the real world

- Check whether the language, labels, and conceptual model match user expectations.
- Flag internal jargon, mismatched metaphors, and unnatural task sequencing.

### 3. User control and freedom

- Check whether users can undo, go back, cancel, or exit without penalty.
- Flag dead ends, irreversible actions without review, and sticky modals.

### 4. Consistency and standards

- Check whether patterns, labels, and behaviors align across the product and common platform norms.
- Flag one-off interactions, renamed common actions, and inconsistent icon meanings.

### 5. Error prevention

- Check whether the design helps users avoid mistakes before they occur.
- Flag dangerous defaults, unclear destructive actions, and validation that appears too late.

### 6. Recognition rather than recall

- Check whether users can see available options and context without remembering hidden rules.
- Flag buried settings, memory-heavy workflows, and weak navigation cues.

### 7. Flexibility and efficiency of use

- Check whether the design supports both new and experienced users.
- Flag missing shortcuts, slow repeated flows, and no path to expert efficiency.

### 8. Aesthetic and minimalist design

- Check whether the interface shows the right amount of information for the moment.
- Flag clutter, repeated explanations, and decorative noise that blocks the task.

### 9. Help users recognize, diagnose, and recover from errors

- Check whether errors explain what happened and how to recover.
- Flag blame, vague wording, and dead-end recovery states.

### 10. Help and documentation

- Check whether help exists where needed and supports self-guided learning.
- Flag walls of documentation that replace good design, or total absence of guidance for complex tasks.

## Cognitive and physical laws

### Fitts' Law

- Small or distant targets increase interaction cost and mis-taps.
- Flag tiny tap areas, edge cases near destructive actions, and controls placed far from the user's active focus.

### Hick's Law

- More choices increase decision time.
- Flag overloaded menus, bloated settings pages, and action clusters with weak prioritization.

### Miller's Law

- Working memory is limited.
- Flag long unchunked lists, multi-step instructions shown all at once, and complex forms without grouping.

### Gestalt principles

- Proximity: related things should appear together.
- Similarity: related controls should look related.
- Continuity: visual flow should support scanning.
- Closure: incomplete shapes can still form a coherent group.
- Figure/ground: important content should stand out from background noise.

### Accessibility and inclusive interaction

- Check keyboard use, focus visibility, contrast, zoom behavior, semantics, screen-reader clarity, motion sensitivity, and alternative input flexibility.
- Treat inaccessible flows as usability failures, not optional polish.

## Emotional heuristics

Apply this second pass after standard usability review.

### Emotional affordance

- Check whether the experience gives reassurance, trust cues, and social-emotional clarity.

### Cognitive milestones

- Check whether progress is visible and meaningful, especially in longer or stressful flows.

### Affirmative feedback loops

- Check whether the interface confirms control after user actions.

### Chromatic resonance

- Check whether color supports clarity and calm rather than confusion or alarm inflation.

### Universal access

- Check whether input modes and interaction pathways are flexible.

### Mental white space

- Check whether layout and information density reduce cognitive strain.

### Inclusive empathy

- Check whether the flow respects different abilities, identities, and emotional states.

### Compassionate consistency

- Check whether tone and interaction patterns stay steady across normal and edge states.

### Therapeutic error recovery

- Check whether errors are informative, respectful, and emotionally stabilizing.

### Self-guided learning

- Check whether the design teaches itself contextually instead of forcing a user into documentation.

## Finding template

Use this structure for heuristic findings:

```markdown
## [Heuristic name] - Severity: [1-5]
Finding: ...
Impact: ...
Recommendation: ...
Priority: High / Medium / Low
```

## Review pattern

Use this order:

1. Review Nielsen heuristics.
2. Review cognitive and physical laws.
3. Review emotional heuristics.
4. Summarize the highest-severity issues first.

When possible, tie every finding to:

- the affected task
- the likely user impact
- the fix with the best effort-to-impact ratio
