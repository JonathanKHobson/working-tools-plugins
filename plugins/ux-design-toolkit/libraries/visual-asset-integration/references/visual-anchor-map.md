# Visual Anchor Map

Create a compact anchor map before editing or critiquing a visual surface.

## Required Fields

| Field | Meaning |
| --- | --- |
| ID | Short stable label such as `A1`, `HeroMedia`, `Card03`, or `QuoteArt` |
| Source | Screenshot path, live URL, file, page, slide, or viewport |
| Region | Approximate grid region, coordinates, component, selector, or page area |
| Observation | What is visible now |
| Asset role | Evidence, identity, interface, environment, editorial, or atmosphere |
| Action | Keep, replace, crop, generate, edit, remove, or defer |
| Verification | Screenshot, browser check, static check, source review, or publish smoke test |

## Example

```markdown
| ID | Source | Region | Observation | Asset role | Action | Verification |
| --- | --- | --- | --- | --- | --- | --- |
| HeroMedia | mobile screenshot | top right hero | image stretches hero height | evidence | replace with constrained crop | mobile screenshot at 390px |
| Card02 | desktop screenshot | case grid center | generated art sits near proof claim | atmosphere | replace proof slot with real screenshot | source manifest and desktop screenshot |
```

## Rules

- Use 3-8 anchors for most passes.
- Refer to anchors in fixes and final QA.
- Do not claim visual completion without verifying the changed anchors.
- If there is no rendered surface yet, make anchors from the intended layout or
  content map and update them after the first render.
