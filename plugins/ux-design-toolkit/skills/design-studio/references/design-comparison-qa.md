# Design-to-implementation comparison

Use when recreating an approved image, Figma frame or other visible source, or comparing a changed implementation with its incumbent. This original method strengthens the existing [verification method](verification.md); broad task audits still use [Design Review](../../design-review/SKILL.md). It contains no copied vendor rubric or fixed aesthetic mandate.

## Establish comparable evidence

Open both the actual visual target and the latest rendered implementation. Record source identity/revision and capture, implementation build/route, viewport in CSS units, screenshot pixel dimensions, device scale/density, crop, theme, content, authentication and interaction state. If those conditions differ, reconcile them or declare the mismatch before judging fidelity. An image path or source code alone cannot establish a rendered comparison.

For a phone-stage prototype, compare the app-owned screen region with app content, and compare the frame only if the target actually includes it. Determine the receiving runtime's screen bounds and stage scaling from its actual contract; do not compare a scaled phone preview with a full-size source. Use an element/region capture when supported. If a capture is double-density, normalize both inputs to equivalent dimensions using the authorized image/asset tool or take a matching-density capture. Preserve original evidence and record any derivative, scale and crop. Do not prescribe one universal phone size or assume the browser viewport equals the app screen.

Place source and implementation together in one comparison view/input with explicit labels. A side-by-side montage or matched split view is suitable when supported; otherwise describe that comparison as separate inspected views and avoid claiming simultaneous comparison. Inspect the full view for hierarchy and proportions, then readable focused pairs for details that the overview cannot reveal. Explain why a focused pair is unnecessary if none is used. Reject incorrect route/window, blocked/loading, accidental crop or unsettled fonts/images/hydration as final-state evidence; an intentional loading-state test remains legitimate when labeled.

## Inspect all relevant fidelity surfaces

Check each surface and explicitly mark not applicable or unobserved where appropriate:

- Type and copy: real family/fallback, weight, scale, line-height/tracking, optical treatment, wrapping/truncation, hierarchy and actual app wording. A generated concept's text may contain errors; approved copy controls the implementation.
- Geometry and grouping: region proportions, crop, alignment, margins/padding/gaps, grid, density, shape/elevation, above-the-fold content and overlaps. Normalize device/browser chrome before attributing a defect.
- Color and effects: semantic pairs, source palette/tokens, contrast, opacity, gradients, shadows and state distinctions in the actual context.
- Assets and icons: correct subject/meaning, source/rights, proportions, crop, sharpness, compression, masking/transparency, optical size/alignment and state variants. A placeholder or code drawing is a problem when it loses the source's intended asset or task meaning; an intentional native vector/icon is not inherently defective.
- Behavior and access: core links/controls, focus/keyboard, states, disabled/repeated actions, empty/error/recovery and requested responsive widths/text scaling. Visual similarity cannot prove these; exercise them separately.

Respect deliberate constraints and the project's authority. Identify a source-specification omission separately from implementation drift. Classify the finding by effect: blocking the task/access, material mismatch, moderate actionable drift or optional refinement. Do not convert preference into a failure or use a detector match as independent observation.

## Correct and close with evidence

For each material issue record location/anchor, source versus implementation evidence, impact, concrete fix and acceptance check. Preserve the original finding, apply authorized changes, recapture the same state/viewport and compare the revised render. Build/lint/server troubleshooting does not count as a visual comparison iteration. Keep a concise history linking finding, fix and post-fix evidence.

Pass only the requested comparison scope when no unresolved material defect remains and relevant fidelity surfaces have been inspected. If source/render access or normalization is blocked, report that part unverified or blocked; delivery of useful editable source may still be appropriate if that is the requested stage, but do not call it visually accepted. Optional refinements can remain without an endless loop. The record can live in the project's existing QA/issue file rather than requiring a new filename.

A useful record includes source and implementation references, captured dimensions/density/crop, route/state, full-view and focused evidence, findings/iterations, interaction checks, result and limits. Keep prepared, visually accepted, behavior-tested and published distinct.

## Calibration fixtures

A 786 × 1704 image and a 393 × 852 CSS phone screen at density 1 represent comparable geometry only after density is accounted for. Comparing them as raw pixel sizes creates a false spacing/size finding. A phone stage scaled to 80% requires an unscaled content capture or explicit matched scale. These values illustrate a fixture, not a runtime requirement.

If a correction changes a wrapping headline and shifts the action below the fold, recapture both the full view and that region after the fix; a passing build cannot close the visible defect. If an illustration was replaced by a crude placeholder while the rest matches, record that asset mismatch even when the screen layout passes.
