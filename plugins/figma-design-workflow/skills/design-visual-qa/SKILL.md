---
name: design-visual-qa
description: Review rendered Stitch, Figma, FigJam or presentation work for visible usability, structure and craft. Use before handoff or when a design needs focused repair; this is not user research or accessibility certification.
---

# Design Visual QA

Review the actual output against the user's task and accepted design direction. Use current rendered evidence and the smallest useful scope. Do not trigger a redesign or a full research project from a final review.

## Ground the review

Identify the audience, primary task, target viewport(s), accepted visual reference/design system, and required states. Infer them from existing evidence; ask only when a missing answer changes the review materially. Inspect real screenshots, app views, exported images, or a rendered artifact. Source code and an agent's completion claim are not visual evidence.

Before critique, create 3–8 anchors: ID, source and viewport/page, approximate region or normalized bounds, selector/layer/component hint when available, observed fact, intended action, final verification. Distinguish direct observations from inferred problems and untested states.

## Usability and structural checks

- Is the main task obvious, with an understandable primary action and visible state? Check labels, hierarchy, information grouping, errors, and recovery only where evidence exists.
- At the required sizes, inspect wrapping, clipping, overlapping controls, readable text, and touch/focus affordances. Test actual keyboard, scrolling, hotspots, and return paths only when interactive evidence and authorization exist.
- Distinguish a visible overlap from an unintended collision. Check the intended lifetime and layout behavior of temporary overlays before treating them as defects. A transient notice and persistent inline warning may intentionally coexist. In a cleanup, preserve that contract and flag unknown behavior; do not silently remove a layer to simplify the screenshot.
- Do not rely on color alone for status. Do not infer contrast ratios, screen-reader behavior, or accessibility compliance from appearance; measure/test when required.
- For a Stitch/Figma transfer, reconcile screen roots and inspect editable text/shape children, layout sizing, fonts, and bindings. Read [transfer QA](../figma-ui-operator/references/stitch-to-figma.md). A PNG is visual evidence, not native structure.
- For a FigJam workshop, read the [board acceptance checks](../figma-ui-operator/references/figjam-workshops.md#verify-and-deliver). Inspect the actual editor at laptop working scale, including the current prompt, input, evidence access, and comparison. Report reveal, background-only locking, role/multiplayer, and assistive-technology checks separately; a screenshot cannot pass them.

## Design Taste Gate

Apply the existing design system first. Describe the surface's purpose and visual register: operational tool, marketing page, portfolio, or internal review. Match density, expressive variation, motion, and imagery to that purpose.

Check composition and first-scan hierarchy; type roles and legibility; spacing rhythm; meaningful color; image/copy placement; and consistent interaction states. Flag generic decoration only when it weakens this specific task. A centered hero, system font, card, or gradient is not inherently a defect. Do not replace an approved brand direction with an evaluator's preference.

For a presentation, show actual screens with concise element-linked callouts. Check the tallest screen, container heights, and separation between rows at both overview and reading zoom. For a north-star bitmap, inspect generated text and image details and label it as a proposal.

When installed and relevant, the full `design-taste-gate` or `ux-heuristic-compass` can deepen the review. They are optional; this skill contains the focused check and does not require enabling an MCP.

## Fix and verify

Prioritize the few issues that affect comprehension, usability, or credibility. Each finding needs an anchor, user impact, concrete change, and verification step. Make authorized corrections and reread the changed anchors. Avoid tests that only restate implementation or repeated checks after the issues are resolved.

Report what is ready, the changed anchors, material remaining issues, and untested behavior. An attractive static mockup is not a functioning app, shipped website, validated user outcome, or accessibility certification. Keep package-only QA separate: Markdown instructions and manifests require structural checks, not invented screenshots or visual scores.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports Figma Designer, Design Quality Reviewer. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
