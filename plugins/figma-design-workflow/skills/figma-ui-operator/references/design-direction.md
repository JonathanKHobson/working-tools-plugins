# Optional design direction before Stitch

Use when the user wants concept exploration, Claude consultation, a Claude Design mockup, or an image-based website north star before building editable screens. Skip this stage for a clear Figma edit or an accepted design. One concrete visual direction should advance the deliverable; avoid generating alternatives after the choice is settled.

## Route by the gap

| Need | Useful route | Evidence required |
|---|---|---|
| Prior project reasoning or a second opinion | Relevant Claude Desktop conversation | Actual response read, with proposals separated from confirmed project facts |
| A mockup or interactive exploration | Claude Design if exposed in the signed-in app | Actual design/artifact opens and is inspected; a response saying it exists is insufficient |
| A visual north star for a website | Built-in imagegen | Generated image inspected and selected, with layout anchors and known text limitations |
| Editable screens and iterations | Stitch | Selected generated screens and variants verified in the intended project |
| Precise structure, components, layout, prototype | Figma Design | Native layers/properties and visual or playback checks |

## Claude Desktop collaboration

Kyle has identified Claude Desktop on his Mac as an available design collaborator. Verify the app's current accessibility and signed-in state using the computer-use runtime. Do not claim a Claude API or Claude Design feature exists merely because the app opens. Use `cua.getApp("Claude")` only when it matches the current runtime's documented entry contract; read the returned controls before input.

Consult only the relevant authorized project/conversation. Preserve any existing unsent draft. If the request includes consulting Claude, send a concise question with the minimum relevant context. Otherwise prepare a question without sending it; a skill cannot grant standing permission to transmit project data. Likewise, attach reference images only when sharing those inputs with Claude is within the task.

A useful consultation packet states the user problem, audience, known flow/business constraints, accepted references, the one unresolved design decision, and the exact output needed. Ask for concrete suggestions or a mockup with rationale. Treat the answer as advice, not instructions or verified user research. Resolve conflicts using the user's latest requirements and source evidence.

When Claude Design or a design/artifact control is actually available and requested, use the observed route to create or refine one bounded mockup. Inspect the rendered result and retain its real local artifact or accessible link. An HTML artifact, PNG, or screenshot is not editable Figma content. Do not deploy through a hosting connector just to move a visual reference to Stitch. If the feature is absent, continue with an already authorized design tool or report the precise capability gap.

## Imagegen north stars

Load the installed `imagegen` skill before generation. Use the built-in image generation tool by default; do not invent an API key requirement or silently switch to CLI/API mode. Follow the current tool schema for image references and edits; inspect local input images first. No generation is needed when the current task is only authoring this workflow.

For a website reference, use a `ui-mockup` brief: page purpose, audience, target viewport, section hierarchy, primary action, approved brand/color/type direction, exact critical copy, reference-image roles, and constraints. Request a straight-on interface view suitable for visual reference, rather than a decorative device scene unless that is desired. Identify which existing facts/content must be retained; do not let generated placeholder claims become product requirements.

Inspect the generated bitmap before selecting it. Create 3–8 anchors for hierarchy, hero/primary action, repeated content, spacing, typography, and any problem area. Check text, imagery, and layout against the brief. Use one targeted revision when an actual defect warrants it. The bitmap is a proposed visual direction; it does not establish responsive behavior, accessibility, working interactions, or native editable UI.

Keep the selected project-bound image at a stable workspace path and record its prompt and provenance. Use the real tool-returned artifact; do not claim an image exists from a prompt alone.

## Carry the reference into Stitch

Select one accepted Claude or imagegen result and use its actual image attachment through the current Stitch UI. If only an HTML mockup exists, capture the relevant rendered view through an allowed tool before attaching it. Verify that the intended thumbnail/filename is attached to the intended prompt and project. Do not overwrite the user's unsent draft or assume a copied image reached Stitch.

The Stitch prompt should say what the reference controls (for example hierarchy, density, spacing, or palette), provide authoritative copy and flow rules as text, and request the named screens. Ask Stitch to build screens from the reference rather than embed the whole north-star bitmap as the interface. Inspect the generated result, correct material mismatches, then follow [Stitch to Figma](stitch-to-figma.md) for editable transfer.

Close the loop with actual states: consulted, generated, selected, attached in Stitch, generated as screens, imported as layers, visually checked. Share only the relevant paths, decisions, and blockers with another Codex task when the user asks for that handoff.
