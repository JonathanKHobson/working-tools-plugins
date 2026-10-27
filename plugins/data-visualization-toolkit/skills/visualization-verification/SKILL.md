---
name: visualization-verification
description: Test and review data visualizations for analytical correctness, visual regression, accessibility, interaction and export. Use when verification or inclusive access is the main task.
---

# Visualization verification

Read the complete original procedure matching the risk, then its relevant linked references and templates:

- [Testing Data Visualizations](../../libraries/build-web-data-visualization/skills/testing-data-visualizations/SKILL.md) for risk-first test selection, deterministic fixtures, data/component/image/E2E layers, mocks, live states and brittle-test avoidance.
- [Accessibility and Inclusive Visualization](../../libraries/build-web-data-visualization/skills/accessibility-and-inclusive-visualization/SKILL.md) for text alternatives, contrast/redundant encoding, keyboard and touch paths, reduced motion, mobile and export access.

Read both for full product or publication review. The preserved [visualization test plan](../../libraries/build-web-data-visualization/assets/templates/visualization-test-plan.md), [accessibility checklist](../../libraries/build-web-data-visualization/assets/templates/accessibility-review-checklist.md), [Playwright visual starter](../../libraries/build-web-data-visualization/assets/templates/playwright-visual-regression-starter.ts) and other templates are examples to adapt, not proof of a passing run. Verify the artifact actually rendered and report test, export and publication states separately.

## Reader-comprehension gate

Use this gate for the actual rendered default view and expanded details. An explicitly scientific or academic audience may need technical terms upfront; that exception does not waive scale meaning, arithmetic or evidence honesty. Capture 3–8 anchors with ID, source/viewport/page, approximate region, selector/node when available, observed fact and intended action. Recheck changed anchors; source extraction alone cannot pass this gate.

- **First glance:** state the question each upfront view answers and the answer a reader can see without opening methods. Remove or defer views that repeat a dimension without a distinct decision or comparison. A reviewer walkthrough supports a design judgment; it is not participant comprehension evidence.
- **Plain labels:** replace scientific jargon, raw IDs, coefficients, ordinal terminology, MATTR and opaque decimals with accurate everyday meaning for lay readers. Retain exact definitions and useful precision in a named details view. Do not replace a measured construct with an easier but different one.
- **Scale interpretation:** check each scale's meaningful ends and middle, units, numeric values/ranges and direction. Explain the span's meaning beside it: observed minimum-to-maximum, uncertainty around an estimate, or recommended target. Use trait-specific labels when meaningful; high does not imply good, and the midpoint is not automatically neutral or desirable. If middle meaning or thresholds are unsupported, say so instead of inventing categories.
- **Numerical and epistemic honesty:** compare displayed values, ranges, thresholds and rounding to their source. Preserve missingness and plain-language uncertainty. Keep observed, inferred, synthetic, predicted and target values visibly distinct. A claim of empirical validity requires relevant observed evidence and its limits; agreement among models or reviewers is not empirical validation.
- **Effort and layout:** preserve the familiar compact incumbent structure when it serves the question. Keep essential meaning visible; use a clearly named details button for secondary evidence and methods, without blanket accordions. Inspect ordinary web reading text at 16px or larger, long labels, narrow layouts and zoom. Do not shrink core labels to fit a crowded view.
- **Access:** check keyboard/touch and non-hover access to the same values and scale meaning, with redundant cues where color carries information. Details disclosure must be reachable and return cleanly to the primary view.

Use relevant acceptance scenarios as review cases in the existing task, not a new test framework:

| Scenario | Passing evidence | Failure that blocks signoff |
| --- | --- | --- |
| A style measure uses 0–100 with declared bands 0–33, 34–66 and 67–100 | Accurate Casual / Neutral / Formal labels, numeric mapping and the actual middle meaning; state that these are declared bands, not empirically discovered cutoffs | Low / Medium / High implies quality, or the bands are called measured norms without evidence |
| A shaded 40–60 span is a recommended target while observations run 22–74 | Both are labeled by role and retain their source values | The target is described as the observed spread or an uncertainty interval |
| Two default charts show the same trait scores | One is deferred, or the second has a demonstrably distinct question and comparison | Decorative re-encoding adds decoding work without new meaning |
| A lay-reader view exposes MATTR, internal trait IDs or unexplained 0.734 | Accurate everyday labels and appropriately rounded values are visible; exact method and precision remain available through Details | The reader must decode jargon to understand the primary answer, or rounding changes the conclusion |
| Several models agree a scale is valid | Consensus is labeled a review judgment or hypothesis; any validity claim cites relevant empirical evidence and limits | Consensus is presented as measured validity or improved human performance |

For comparative dashboards, also apply the [construction and interaction checkpoint](../live-dashboards/references/exploration-state-and-comparison.md#comparative-dashboard-construction-and-review). Verify a shared-time comparison, consistent filter scope, hover versus selection, and any claimed motion in the actual rendered states. Record partial user acceptance separately from a reviewer pass.

Report which rendered checks passed and which remain untested. Do not claim reduced cognitive effort, comprehension improvement or empirical validity from a checklist, screenshot or model vote alone.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports Data Analyst, Data Scientist. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
