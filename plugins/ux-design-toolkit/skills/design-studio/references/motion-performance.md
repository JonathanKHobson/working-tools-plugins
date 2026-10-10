# Purposeful motion and measured performance

Use when motion is being added/changed, or when a screen or interaction is reported or suspected slow. Ambitious visual effects are in scope only when the task or brief actually asks for them; do not add hero animation, parallax or elaborate transitions to a request that didn't ask for delight.

## Shared motion-design principles

Motion design can use a clear beat sequence, persistent elements changing visual role, deliberate holds, type hierarchy and sound cues to carry meaning. Apply those principles to a product interface only when they help a real state change or requested brand moment. In UX, the interactive state is authoritative: check what the person can do, where focus goes, what feedback confirms, and how a new action interrupts the transition. A beautiful styleframe or video sequence cannot establish those behaviors.

For visual direction on a standalone motion piece, use Graphic Design Studio's `motion-design`; for code-authored scenes, render and audio/narration production, use Video Production's `create-motion-graphics`. This UX reference retains state transitions and rendering-performance judgment. A shared palette, typeface, subject or soundtrack from one example is not a cross-product rule.

## Motion must be purposeful

Every added animation should do one of: orient the user across a state change, communicate cause/effect of their action, or draw attention to something that needs it. If an animation does none of these, it's decoration competing with the task. A "delight moment" is acceptable when it also advances the task or the product's story (e.g., a checkout confirmation that reinforces the purchase just made) — motion that is delightful but tells the user nothing about their task is lower priority than motion that does both.

## Interruptions and reduced motion

Check what happens when an animated transition is interrupted mid-flight by a new user action or a new state (data arrives, user navigates again, dismiss triggered before entrance finishes): confirm the interruption doesn't leave an element stuck mid-transform, doesn't fight the new state, and doesn't queue up a backlog of pending animations. Respect `prefers-reduced-motion` (or the platform equivalent): define what "reduced" means for the actual effect in question — for most cases this means removing large-scale movement/parallax/auto-play while keeping simple opacity or instant-state changes, not simply speeding up the same animation. Verify the reduced-motion path actually renders correctly, not just that a media query exists in the stylesheet.

## Device and network cost

Motion has a real cost on lower-end devices and constrained networks: prefer compositor-friendly properties (transform/opacity) over layout-triggering properties (width/height/top/left) for anything animated repeatedly or on scroll. Confirm large images/video used in motion-heavy sections have a real size/format budget, not just an assumption that lazy-loading fixes it — blind hero lazy-loading that delays the very content the user came for is a defect, not an optimization. State the actual devices/conditions checked (or that this was not exercised) rather than asserting smoothness from source review alone.

## Measuring performance for real

1. Define the user-visible slow outcome precisely (e.g., "list view takes 4s to become interactive after data returns," not "the app feels slow").
2. Baseline it on an actual device/network condition relevant to the audience — not just a fast local dev machine on a wired connection. State what was used as the baseline.
3. Locate the actual bottleneck (render-blocking request, layout thrash, oversized asset, unnecessary re-render, unbounded list) before changing anything. Do not guess-optimize.
4. Make the targeted change, then re-measure the same defined outcome under the same conditions to confirm it actually improved.
5. Guard against regressions: confirm the change didn't break loading/empty/error states or accessibility (e.g., skeleton screens that never resolve, content that never becomes focusable).

Never report a performance number that wasn't actually measured in this session. If a number is asserted from memory or a general claim ("this pattern is X% faster"), label it as an unverified claim, not a result.

## Numerical standards and API/tooling choice

Current thresholds (Core Web Vitals targets, frame-budget numbers, etc.) change over time; verify the current published standard from its source when a specific number is being cited as a requirement, rather than repeating a remembered figure as current fact. The specific animation API, profiling tool or build-level optimization technique belongs to the actual implementation stack and its owning provider (Build Web Apps, the native platform specialist, etc.) — this reference sets the judgment and process, not the tool.

## Provenance and scope

Original local synthesis addressing gaps identified when comparing existing UX guidance against Impeccable's motion and performance review methods (source inspected via [design sources](design-sources.md), revision 114ea1d, 2026-09-29). No Impeccable text, metrics or tooling is reproduced; no numerical standard here is asserted as current without source verification at time of use.

## Future research intake

Record a candidate here only when it changes a UI motion decision: source and access date, observed behavior, interaction context, credible limit or counterexample, and a rendered state/interruption/reduced-motion check that could test it. Prefer primary platform guidance and directly inspected behavior. Keep visual-only styleframe findings with Graphic Design Studio and rendering/audio findings with Video Production; do not create another motion catalog.
