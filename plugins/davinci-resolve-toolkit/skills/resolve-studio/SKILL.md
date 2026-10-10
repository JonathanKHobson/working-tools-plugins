---
name: davinci-resolve-studio
description: Operate DaVinci Resolve projects from Codex using verified Computer Use, timeline interchange, internally launched scripts, Studio external scripting/MCP, and AI-assisted Resolve workflows.
---

# DaVinci Resolve Toolkit

Use this skill when Resolve is the editing or finishing environment. Own app operation, setup, scripting and Resolve-specific AI workflow integration. Editorial intent, art direction, dialogue selection, motion craft, audio design and final quality acceptance stay with Video Production Studio.

## Verify the route before app changes

Read [Resolve routes and edition boundaries](references/resolve-routes.md) and inspect the current host's About screen, installation and any existing project setup record. Record observations in the current project; no machine setup is implied by this package.

Choose only a demonstrated route:

1. **Computer Use:** attempt to bind the active Resolve window with Computer Use. Continue only if the window and project are visible. Inspect the active project, timeline and relevant settings before editing. Use explicit timecode/frame controls for precision and verify each mutation in the UI.
2. **Internal script:** support depends on edition, build and language. Free 21.1 Python support is not established; the community bridge is limited to 21.0.x. Do not prescribe internal Python as a Free 21.1 fallback. Inspect the actual menu, same-build documentation and a harmless read before using any supported Lua/Fusion or Studio script.
3. **Studio external scripting and MCP:** use only when Studio is installed, external scripting is enabled, and the candidate MCP passes a live read-only request. Tool discovery/configuration alone is not proof. Before writes, confirm project identity and test a bounded change on a disposable project.
4. **Timeline file interchange:** when direct app control is unavailable or a full cut is more reliable as a package, route through Video Production Studio's `exchange-video-timelines`, then manually import/relink/inspect in Resolve. Its current EDL/OTIO exports omit audio tracks; plan audio reconstruction.

Read [control and finishing](references/control-and-finishing.md) for the complete import smoke procedure, precise trims, track protection and finishing workflow.

## Common workflows

- **Review an existing project:** confirm project/timeline, media relink status, frame rate, track map, active page, and save state. Make a short change list before touching it.
- **Assemble a reviewed cut:** use the editorial owner to approve source ranges and order, export a small representative interchange first, then check identities, in/out points, track placement and duration before importing the full cut.
- **Finish a timeline:** use exact frame/timecode edits, isolate affected tracks, inspect changed anchors after each operation, and avoid assumptions about keyboard preset or edition-specific effects.
- **Captions and titles:** derive timing from the final timeline, import reviewed output-timed SRT where appropriate, and verify legibility at delivery size.
- **AI-assisted operations:** use only the currently licensed and visible Resolve features. On Free, do not depend on Voice Isolation, Magic Mask, Smart Reframe, Studio transcription, or other Studio-gated tools; use an approved external or manual substitute.
- **Render and handoff:** save, close and reopen the project when practical, then render to the owning project's output folder. Inspect the actual rendered file and use Video Production Studio's `validate-video-quality` for editorial and media QA.

## Acceptance evidence

Report the exact edition/build, control route, project and timeline, imported/relinked assets, edits verified, whether save/reopen succeeded, render path/hash and QA performed. Keep `.drp` files with the project's media map; a project archive can reference external media. Do not call an import, save, render or MCP setup successful until that exact state was observed.

For current installation details and the Studio/MCP gate, see [Resolve routes and edition boundaries](references/resolve-routes.md). For the earlier source review, consult the existing Video Production Studio Resolve source index. Do not copy its app-operation method back into that plugin; it now routes here.
