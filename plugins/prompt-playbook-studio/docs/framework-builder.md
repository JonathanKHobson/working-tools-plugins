# Framework Builder

The human workflow is a compact library chooser → host-expanded framework editor → source-assembled prompt → deliberate Copy or Send. Assistant retrieval uses separate `search_prompt_frameworks` and `read_prompt_framework` tools without UI metadata. `browse_prompt_frameworks` opens the versioned view. The widget can explicitly save lens/instruction defaults locally; no tool executes a prompt or modifies Atlas.

## Source and ownership

- Canonical plugin: `prompt-playbook-studio/runtime/framework-builder/`.
- Knowledge Atlas active pattern records: the recipient-owned Atlas pattern directory (`PROMPT_ATLAS_ROOT`), Markdown with YAML frontmatter. These supply exact source-slug crosswalks, status and provenance.
- Preserved authored fields, examples and assembly: the recipient-owned authored source file (`PROMPT_FRAMEWORK_SOURCE`). The build statically parses its JSON array; its eval wrapper is excluded.
- Current CLARE website: <https://jonathankhobson.github.io/AI/index.html#/frameworks/clear-path-forward-framework>. Browser inspection confirmed the five Concise / Logical / Explicit / Adaptive / Reflective fields and optional worksheet disclosure. The current catalog export drops original assembly and `ph` hints, so it is a comparison surface, not the assembly authority.
- Legacy fuller builder and Pattern Picker: `glossary/prompt-builder.html` in the preserved source and CLARE checkout. The new widget preserves applicable source semantics without importing the old application's multi-tab/history subsystem.
- Shared visual shell and host bridge: `ux-design-toolkit/runtime/library-chooser/`. `ux-design-toolkit/scripts/sync_library_chooser.py` projects the four shared files into this runtime's `shared/`; framework controls belong in `ui/`.

`build_catalog.mjs` records source hashes and coverage; generated files are `data/catalog.json` and `data/assembly.js`. At runtime, three historical person-name placeholders are shown as generic project-owner examples; the source and catalog remain unchanged for provenance. Rebuilding requires explicit `PROMPT_FRAMEWORK_SOURCE`, `PROMPT_ATLAS_ROOT` and `PROMPT_PARSER_ROOT` environment paths, plus the authorized external source and Node parser dependencies. Normal use of the bundled catalog requires none of those build inputs. Never hand-edit those files. Rebuild only after source admission. Atlas-only records lacking authored assembly and the separate task-template corpus are exclusions, not generic synthesized builders.

## State and host contract

Protocols: MCP Apps UI `2026-01-26`, using the existing shared bridge; the fresh stdio SDK `mcp 1.26.0` negotiated core MCP `2025-11-25`. Tools/resources use the existing Atlas Python MCP environment from the private `studio-tools/atlas-library.json` binding. No dependency install, network request, credential access, or private draft persistence occurs in the view.

Field drafts live only in the current iframe's memory. A minimal selected ID/view may be restored through the shared session intent mechanism, but field contents are never persisted there. Remount loses private input. Preview text is populated before Send; source examples are placeholders, not silently supplied answers. An accepted host message is a transport receipt, not proof that the assistant executed the prompt.

Expansion is requested through the host bridge and requires acknowledgment. An ordinary web preview and a simulated host do not prove a native side panel. Copy failure selects the preview with an honest manual-copy instruction. Return to chat requests inline mode; Back to frameworks remains library navigation.

## Design anchors and intent

Change: add source-specific editing and metadata recommendations. Keep: approved shared chooser, title left, paired arrows upper right, search/Filters, names below wide cards, separate Back and Return actions, prompt before Send. Historical baseline native activation and Send were reported after a Codex restart; this release needs fresh host verification. New collaboration/default behavior requires a fresh resource and separate verification.

| ID | Source and region | Observed fact / intended action |
| --- | --- | --- |
| F1 | Shared chooser, inline upper row | Preserve title, named Create and paired arrows; one stable compact row. |
| F2 | Shared chooser, search and card row | Preserve search/Filters, keyboard menus, card names below source previews. |
| F3 | CLARE CLEAR Path worksheet, five fields | Preserve exact field keys/labels, types, hints and authored assembly rather than generic brief fields. |
| F4 | Existing prompt-first-use.png, expanded prompt/actions | Show populated preview before deliberate Copy/Send, optional additions distinct. |
| F5 | Expanded navigation upper corners | Back retains library; Return requests actual host inline mode. |
| F6 | Legacy Pattern Picker, source metadata | Recommend from matched metadata with reasons; no claims of measured effectiveness. |

## Verification and activation

Run `node runtime/framework-builder/source_assembly.test.mjs`, `node runtime/framework-builder/ui.test.cjs`, and the existing Atlas Python against `runtime/framework-builder/protocol_test.py`. Shared chooser regressions are under the Managing My Computer workspace's `work/library-widgets-2026-10-06/qa/`. Earlier QA receipts and screenshots remain in the private pre-change archive; generated local test output may use `runtime/framework-builder/qa/`. UI tests also require Playwright, resolved from the installed Node dependency or `PROMPT_PLAYWRIGHT_MODULE`. Native acceptance requires a fresh host readback.

Installation and source parity do not activate a new server in an already-running Codex host. Native tool exposure, resource freshness, expansion, remount and delivered-message behavior remain separately testable after the user is ready to restart.

## Collaborative drafts and additions

`prepare_framework_prompt` validates supplied values against the exact catalog field schema, then opens a selected framework with a rationale and optional lens/instructions. It does not save or execute the draft. The assistant uses native MCP App browser controls for subsequent edits in the same visible widget, reading the current fields first. **Ask AI to refine** shares an explicitly labeled refinement request and the exact preview with the current conversation; Send to conversation remains a separate final prompt handoff.

Prompt additions starts collapsed and supports one of five response lenses, reusable instructions, a per-draft off switch, and a saved panel-expansion preference. Lens text is condensed from the legacy AIGlossary builder; it is prompt text, not a browsing or model-reasoning setting. `read_framework_preferences` and `save_framework_preferences` are app-only tools. Explicit defaults are atomically saved with private permissions at `~/.config/studio-tools/prompt-framework-preferences.json`; fields and one-time instructions remain ephemeral. Invalid preference files produce errors without replacement.

No shared draft database, polling or backend synchronization is implied. Iframe reload may lose fields. The model should not prepare replacement widgets while collaborating; duplicate results are ignored and edited drafts reject replacement prefills. Browser actions are sequential collaboration, not simultaneous multiplayer editing.

Historical review: Claude subscription CLI confirmed `claude-opus-5-5` and completed a bounded design review; its dated receipt remains in the private pre-change archive. Adopted explicit refinement wording and a clear lens/panel hint. Deferred suggestion inboxes, per-field author labels and simultaneous typing promises: current frontend controls cannot reliably distinguish AI keystrokes from human keystrokes.
