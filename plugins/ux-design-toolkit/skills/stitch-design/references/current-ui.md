# Dated manual UI observations

Observed through an existing signed-in Chrome tab on **2026-09-08**. This is a capability snapshot, not a fixed selector map. Re-check current UI and tool documentation on every task. Private project identifiers and content are intentionally excluded.

- Stitch displayed a project canvas, agent/chat panel, existing draft text and attachment, model/mode control, preview screens, and Export/Share controls.
- Host and app content were in nested frames, including rendered preview frames. Frame indexes and internal URLs are implementation details; do not hardcode them.
- Export with no screen selected displayed “No screens selected” and disabled the export action.
- Selecting a screen exposed design controls and added the screen to the prompt context. Removing the temporary composer context chip restored the selection state without deleting the canvas design or changing the user's draft.
- Export destinations displayed in that session included AI Studio preview, Figma, MCP, Netlify preview, Lovable preview, Bolt preview, ZIP, Code to Clipboard, and Project Brief. These are UI observations, not promises of account access, compatible output, successful transfer, or deployment.
- The AI Studio option described a partner handoff and downloads. Such a destination is a separate external transfer; a local export need not use it.

The smoke check inspected controls and restored temporary selection. **It did not generate a design, download/export a file, transfer to Figma, publish, or validate a running application.** Do not cite this snapshot as end-to-end execution proof.

Prefer the fresh UI over old online screenshots. If an expected option is absent, choose another available authorized output or state the specific limitation. Do not install MCP or change browser launch flags to force parity with an old tutorial.
