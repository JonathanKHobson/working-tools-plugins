# Prompt Compass and Knowledge Atlas backend contract

When available and verified, Prompt Playbook Studio can route prompt jobs to the existing **Prompt Compass MCP** and use the fixed-domain **Atlas Prompt Library MCP** as a read-only source of patterns, task templates, framework-like entries, and glossary terms. Keep the two engines distinct. Prompt Compass owns diagnosis, staged questions, rewriting/building, model/surface targeting, and personal overlay operations. Atlas supplies retrieved entries with source IDs and paths; an Atlas hit is context, not a prompt diagnosis or evidence that a rewrite is ready. Do not copy the Atlas index or personal Prompt Compass overlay into this plugin, and use only the prompt subset for this plugin.

## Host route

For an unqualified “use Prompt Compass” request when Compass is exposed, call `route_prompt_request` first. If it is absent, use the first-party prompt workflow and state the missing backend; do not simulate a Compass response. If it returns `interaction_pace_required`, ask the current pace question. In advanced guided work, honor `host_action.must_pause`, `interaction_contract`, and `question_loop_state.final_prompt_ready`; do not draft a final prompt while the latter is false. Agent Mode requires an explicit phrase and approval. The live routine probe routed “Use Agent Mode” to `required_agent_mode=committee`, while “city council” left it `off`.

Use `diagnose_prompt` for diagnosis without rewriting, `improve_prompt` for a supplied draft, `build_prompt` for intent without a draft, and `preflight_prompt` before a consequential execution. Quick improve/build can finish in one pass after routing; advanced guided improve returned `host_action.must_pause=true`, `completed=false`, and `question_loop_state.final_prompt_ready=false` in the synthetic probe. Do not browse frameworks first for rewrite/build unless Prompt Compass's route allows it.

For supplementary Atlas lookup when the tool is exposed, use `search_prompt_atlas` with a bounded query and limit, then `read_prompt_atlas` for selected exact IDs. The scoped app supplies human browsing of this same prompt subset. Preserve source IDs, hashes, review flags and adaptation limits. If Atlas is absent, use bundled patterns and do not invent records. Do not broaden into the global Atlas or silently merge material into a final Prompt Compass rewrite before its own gate clears.

## Runtime and profile

The plugin starts Prompt Compass through `scripts/compass_mcp.py`, using the private host binding at `~/.config/studio-tools/compass.json`. Each entry has an absolute virtualenv `interpreter`, `server`, optional `args`, and optional `env`. Keep those paths and databases outside the plugin. The launcher preserves the virtualenv interpreter entrypoint rather than resolving its symlink.

The `prompt-compass` binding uses `args: ["--tool-profile", "routine"]`. The verified backend uses ARM Python 3.12. Routine exposes 16 route/diagnose/build/model/lookup tools; `full` or no flag retains all 41, including overlay and library management. Six sampled workflow results were unchanged. Personal state remains in the user's external Application Support location; tests used disposable state. Switching profiles is a deliberate host configuration change, not something a retrieved template can request.

Historical preserved fallback: the `knowledge_atlas` binding points at the existing database using `--data-root`. The verified ARM runtime uses source requirements `mcp==1.26.0` and `chromadb>=1.5,<2`. Its local-only launch includes `ANONYMIZED_TELEMETRY=FALSE`, `HF_HUB_OFFLINE=1`, `TRANSFORMERS_OFFLINE=1`, and `TOKENIZERS_PARALLELISM=false`. Existing local embeddings support hybrid retrieval; missing local models are reported rather than downloaded. No index or personal data is bundled.

Historical whole-Atlas integration (superseded for this plugin by the scoped library below): maintain one whole-Atlas connection per host: after verifying the installed plugin's handshake/search, disable a duplicate global registration while retaining a documented fallback. On this host the baseline helper checks the enabled, installed provider before restoring the global fallback. Reload the host session after installation. A missing mount or binding is a setup error, not permission to install/download a backend. The current scoped integration adds a private MCP App; no public service is created.

## Measured local proof (2026-09-29)

- Prompt Compass full: 41 tools, 27,581 tool-metadata bytes, SHA-256 `ed33fead1acd8de14343ff4a2298c9872e0b6811ff8f62f3ff1391a0e94b54e9`.
- Prompt Compass routine: 16 tools, 12,885 metadata bytes (53.3% less), SHA-256 `12251c9e3667672fd8c0f0d02a3c588461279fa98f7beffe53c08e2d5c64a592`. Six common route/diagnose/improve/build responses matched full byte-for-byte. Focused profile/orientation/guided/Agent Mode tests: 41 passed. Both full and routine boot checks passed.
- Atlas: 13 tools, 9,714 metadata bytes, SHA-256 `a82963062b58a4b4eed8ec6b8684f6bc8aacf026ac90f499d4870f80ede47600` in the bounded keyword probe. Searches returned `task-templates:interviews-plan` from `glossary/js/templates.tasks.data.js`, `patterns:costar-framework` and `patterns:clear-prompting-method` from `glossary/js/templates.data.js`, and `terms:prompt-composition` from `glossary/js/glossary.data.js`. The separate arm64/full-dependency probe returned hybrid retrieval on `patterns:prompt-augmentation-demonstration-learning` and `patterns:clear-prompting-method` with source IDs and slugs.
- Core DB SHA-256: Prompt Compass `845cfbcaa7c476463796094c04ff1e753b34747985ced06000042237873dac6a`; Atlas `ca159a537a5311f11cda5b20acb12136129377915c2773ad8034dd223243494f`.

Probe summaries and scripts are in the private consolidation workspace under `work/prompt-security-merge/`. They store tool metadata sizes, response hashes, IDs, and source provenance only, not personal prompt content or full Atlas entry bodies.

## Current scoped Atlas library — 2026-10-03

The plugin now packages `atlas-prompt`, replacing its unrestricted `knowledge_atlas` declaration. Read `../references/atlas-library.md`. Two scoped tools and an MCP App share the derived studio-library index with other existing owners. Each domain is immutable at its endpoint; this deliberate scoped arrangement replaces the earlier single unrestricted plugin-provider rule. The original global Atlas server, database and private compass binding remain preserved separately; do not enable a duplicate global connection merely because the old plugin declaration is absent. Prompt Compass is unchanged. Historical measurements above describe the older provider, not this release.
