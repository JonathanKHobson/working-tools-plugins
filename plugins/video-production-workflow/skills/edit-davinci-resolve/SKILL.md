---
name: edit-davinci-resolve
description: Route a reviewed editorial plan to DaVinci Resolve for native project assembly or finishing.
---

# Edit in DaVinci Resolve

Resolve app operation is owned by the dedicated `davinci-resolve-toolkit:davinci-resolve-studio` skill. Use it for edition/build checks, app controls, scripts, MCP eligibility, imports, native project saves and Resolve renders.

This skill remains the editorial handoff point: gather the approved cut map, captions, media inventory, audio decisions and review holds, then give Resolve Toolkit the exact timeline and delivery requirements. Use **exchange-video-timelines** for an interchange package and its round-trip procedure. The current EDL/OTIO exporters omit audio tracks, so call out reconstruction requirements. Use **mix-video-audio**, **create-video-typography** and motion skills for craft decisions; use **validate-video-quality** for the rendered deliverable.

Before handoff, state the intended project/timeline, source mapping, rational frame rate, color space and delivery target. Resolve Toolkit verifies the installed edition and supported operation route. Require saved-project and rendered-file evidence separately; route a native project to save/reopen proof and the render to actual media inspection. A `.drp` references external media, so retain the project media map and only package media within the user's requested scope and rights.

Source research and edition evidence are retained in the toolkit's route reference and the existing [Resolve source index](references/sources/source-index.md).
