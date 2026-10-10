# Review: evidence before verdict

Use for a screen, user flow, website, prototype, Figma frame, or graphic artifact. Decide what question the review must answer: Can the user find the next action? Can they complete the task? Does the artifact communicate in the intended order? Does the rendered output match the approved source?

Capture the actual current surface and relevant states. A source file, token list, saved revision, or previous screenshot is context, not proof of today's rendered behavior. For a multi-step flow, note each step and the transition after the user action. If a screenshot is missing or stale, mark that portion unverified. Do not infer keyboard or screen-reader behavior from pixels.

Map 3–8 anchors before visual claims:

| ID | Source and state | Viewport/page and region | Observed fact | Action |
|---|---|---|---|---|
| A1 | Named frame or live capture | e.g. desktop first viewport, upper left | What is visibly there | Change, Keep, or Defer |

Use the anchors to assess first-read hierarchy, content order, task affordances, spatial grouping, typography, contrast, density, responsive structure, trust signals, and source fidelity. Identify the user impact of each issue. Separate a broken task path, an access barrier, an inconsistent pattern, and a taste preference. Group repeated symptoms when one shared component or token causes them.

For a concise audit, report strengths worth preserving, prioritized findings with anchor IDs and evidence, a proposed correction for each finding, and verification gaps. Use severity for impact, not visual drama. An attractive screen can still have a high-severity access barrier; a preferred style is not a blocker. The recommendation should say which part of the artifact changes and what remains intact.

When source and implementation differ, compare like with like: same route, content, state, theme, viewport, and image density when possible. Normalize browser chrome and device framing before calling a mismatch. Compare the overall composition and a few focused regions that affect meaning. Recheck changed anchors after a fix. Stop once material differences in the requested scope are resolved.

For system-level defects or a detailed web polish pass, apply the relevant [system craft checks](system-craft.md), including native browser states. Automated aesthetic flags are prompts to inspect, not proof of a defect; approved brand choices and the reader's task govern the correction.

For generic or template-driven output, apply [context-sensitive design review](../../design-review/references/intentional-design.md). Keep observation, supported risk, preference and unknown distinct; preserve appropriate patterns explicitly. Use its bounded task-change test only when structural reuse is the concern, and carry important claim qualifications through the content model.
