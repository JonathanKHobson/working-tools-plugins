# Prompt Playbook Studio

- `skills/prompt-playbook/`: create/refine/debug, conditional templates, private style, library retrieval and Compass handoff.
- `skills/prompt-evaluation/`: observable tests and comparisons.
- `scripts/`, `libraries/` and `runtime/`: reviewed first-party methods, retained MIT compiler and optional local tooling, described by their owning integration documents.
- `scripts/prompt_submit_advisory.py`: read-only, bounded UserPromptSubmit hint for explicit prompt-crafting requests; no backend calls or prompt storage.
- `hooks/hooks.json`: Codex plugin-owned prompt advisory.
- `hooks/claude-hooks.json`: Claude plugin hook declaration for the same advisory; declared by the Claude plugin manifest; native activation still requires verification.
- `.mcp.json`: Codex launcher declarations. `.claude-plugin/plugin.json`: Claude absolute plugin-root launcher arguments and advisory hook. Bindings, databases, overlays and saved prompts remain external.
- `.app.json`: optional registered Promptbanken provider for compatible Codex hosts; Claude does not inherit that connector.
- `docs/source-coverage.md`: source capabilities, owners and deliberate exclusions.

Validate the plugin and each skill with the system plugin/skill validators. Runtime integration and compiler documentation contain their specific checks. Edit methods in their owning skill, runtime behavior in its implementation, and personal preferences only in the private external profile.

- `references/atlas-library.md`: scoped prompt Atlas retrieval and private human library. `scripts/atlas_library_mcp.py` and `.mcp.json` launch the fixed domain against a shared external index; no corpus is packaged.

- `runtime/framework-builder/`: collaborative framework chooser/editor, statically projected source catalog and assembly, server, focused tests and QA receipts. `scripts/framework_builder_mcp.py` launches it through the existing Atlas interpreter. [Framework builder](framework-builder.md) documents source ownership, shared-shell projection, build/check commands, state and native activation limits.

- `runtime/framework-builder/preferences.py` owns private local defaults; `prefill.py` validates assistant-prepared fields. `ui/additions.js` owns optional lenses/default controls; `ui/editor.js` owns live drafts and refinement handoff.

The canonical source and public package are maintained implementation copies. `docs/full-procedures.md` selects complete native methods. `references/provider-prompt-engineer.md` is an internal compatibility pointer; copied no-grant bodies and branding stay excluded. Recipient-owned bindings remain external. Historical evidence stays recoverable in the private archive; active runtime, assembly and tests remain here.
