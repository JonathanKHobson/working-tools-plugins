---
name: stitch-design-review
description: Review and improve a Stitch design or its implemented site using rendered evidence. Use for visual quality, mobile behavior, navigation, usability, accessibility or performance questions.
---

# Stitch Design Review

Review a bounded journey and representative pages. Use the applicable UX heuristic skill when available; do not turn every small component review into an exhaustive checklist ceremony.

## Ground observations

1. Inspect the actual source/render. Create 3–8 anchors before visual claims: ID, screenshot/source and viewport, region or normalized coordinates, selector/component if available, observed fact, intended action, and verification status. See [the anchor template](../stitch-workbench/references/brief-and-handoff.md).
2. Evaluate the audience’s path: understand the offer/role, find relevant proof, scan a case or detail page, and take the intended next action. Check information scent, hierarchy, density, chunking, line length, affordances, and consistent global/local wayfinding.
3. Apply Nielsen’s ten heuristics: system status; real-world language; control/freedom; consistency; error prevention; recognition over recall; flexibility/efficiency; aesthetic/minimalist design; error recognition/recovery; help/documentation. Mark irrelevant items with a reason. Use additional design principles only when they explain an observed issue; do not present psychology “laws” as universal guarantees.
4. Separate observation, plausible user impact, severity, proposed fix, and evidence needed. AI critique and expert inspection do not establish user-study results or legal conformance.

## Verify the implementation

- Wait for fonts, image loading/decode, and stable layout before judging crops or measuring overflow. After text resizing or orientation changes, wait again. Record viewport and rendering state.
- Sample the sizes relevant to the product: narrow mobile (often 320/390 CSS px), tablet, desktop, wide desktop, and short landscape where useful. These samples do not certify every device.
- At small widths and 200% text size, verify every required navigation destination is still visible or reachable through its intended menu, not clipped or hidden. Check sticky overlap, scroll targets, dialogs, tap targets, keyboard order, focus visibility/return, reduced motion, contrast, labels, and reading order.
- Test links, forms, menus, download files, back behavior, and important recovery states. Check input validation, sending lock, preserved drafts, failure/retry, and status announcements when forms exist. Mock external sends unless a real delivery test is authorized.
- Check meaningful performance risks: image bytes/dimensions, primary image loading, layout shift, fonts, unnecessary animation/scripts, console/network failures, and long content. Distinguish measured lab results from assumptions and real-user data.
- Preserve original evidence screenshots and intentionally distinctive artwork. Replace generic filler and decorative complexity only when it weakens the user’s task or violates the accepted brief.

## Finish a useful pass

Prioritize blocking task failures, misleading claims, inaccessible controls, and severe small-screen issues. Fix the selected issues, re-render the changed anchors, and run relevant checks once more. Broaden testing only for new failures or remaining risks.

Deliver verified anchor changes, a short list of unresolved material issues, and exact artifact/build locations. Keep QA screenshots and private evidence out of the public release; mark temporary review material for later approved cleanup.
