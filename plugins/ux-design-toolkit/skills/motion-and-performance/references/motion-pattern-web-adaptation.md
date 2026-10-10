# Adapt motion patterns to a working website

Choose implementation using [motion technique selection](motion-technique-selection.md), including path compatibility, interruption, reveal direction and context-specific performance budgets.

Use with the [motion contract and Sites handoff](motion-prompts-and-sites.md). The companion original recipes live in `graphic-design-studio:motion-design`, reference `motion-pattern-recipes.md`; read only a selected recipe when that plugin is available. This table remains sufficient for UX behavior when it is not. The source was two batches of user-supplied stills covering examples 01–16, not a played animation or imported code.

| Pattern | Web contract | Stable alternative / failure check |
| --- | --- | --- |
| Button to player | Real media and controls for functional mode; appropriate focus/close behavior; no unexpected audio. | Usable player/poster with honest error state; test close/reopen. |
| Query to results | Separate real retrieval state from illustrative typing; preserve input and latest response. | Readable result list; test empty/error, keyboard and rapid query changes. |
| Card to workspace | Preserve item identity, edits and route/dialog semantics; do not infer a new backend. | Immediate workspace; test focus return, unsaved work and interruption. |
| Tabs to panels | Selection, panel visibility and accessible keyboard behavior agree; hidden content cannot receive focus. | Immediate switch; test unequal heights and rapid selection. |
| Bar to line | Consult Data Visualization on valid encoding; same ordered data, scales, units and identity throughout. | Static chart/table; verify values and avoid invented intermediate meaning. |
| Dashboard expansion | Preserve metric period, units, comparison and filters; restore context on close. | Immediate detail view; test value consistency, focus and scroll return. |
| Card fan | Preserve item IDs, logical reading order and access to obscured content. Interrupt from the current state rather than queuing full replays. | Readable list/grid; test rapid selection and long copy. |
| Proximity dock | Stable hit areas with visual scaling inside; labels on focus and touch; no hover-only action. | Fixed labeled controls; test pointer exit, zoom, keyboard and touch. |
| Image-filled lettering | One semantic heading; decorative duplicates hidden from assistive technology. Image motion cannot remove text contrast. | Solid readable text; test blocked image and font loading. |
| Elastic lettering | Preserve baseline, meaning and layout extent; verify actual font axes before using them. | Undistorted text; test longest heading and narrow width. |
| Headline to layout | Reserve final geometry; semantic source order follows final reading order; no focus theft or content delay. | Complete responsive layout immediately; test resize mid-transition. |
| Segmented reveal | Underlying image remains semantic; overlays ignore pointer input; reveal cannot wait forever for a resource. | Uncovered image or honest failure state; test slow/failed asset. |
| Perspective layers | Depth is illustration, not a new tab order; labels reflect verified relationships. | Flat labeled diagram; test crop and zoom. |
| Focus band | Never blur required comparison data; emphasis is distinct from keyboard focus, selection and disabled state. | Static highlight; all rows remain readable and operable. |
| Connection pulses | Preserve directed relationships and textual equivalent; illustrative timing is not live data. | Static arrows; test resizing, paused state and truthful status labels. |
| Particle mark | Decorative particles have one accessible brand name; cap complexity and clean up owned animation work. | Static logo; test small size, offscreen behavior and frame cost on target device. |

Choose an interaction trigger when the change responds to the visitor. An illustrative hero may play once when appropriate; repeated motion needs the applicable pause/stop/hide treatment from the existing animation playbook. Reduced motion preserves meaning and control rather than merely slowing everything down. Respect changes to the preference during the session where supported by the implementation.

Use the existing implementation stack and inspect its current APIs when needed. CSS/SVG is often enough; multi-step interruption may justify a timeline already used by the project. Particle quantity, large blurs, filters and layered perspective should earn their rendering cost through observed benefit. Measure on representative devices before performance claims; an attractive desktop screenshot is not evidence of frame stability.

For Sites, attach the selected pattern, exact route/component, approved content/assets, static alternative and acceptance checks to the existing handoff. Keep the Site's delivery constraint, especially local-only requests. No extra provider, site, library, feature or real search backend is implied by a motion reference.

Prompt: “Implement [selected pattern] within [existing component] to help [user task]. Preserve [content and behavior]. Use [explicit states/trigger/interruption] with [stable alternative]. Verify [pattern-specific checks above] and the actual primary action. Report playback, interaction, accessibility and deployment checks separately; do not call a static frame a verified animation.”
