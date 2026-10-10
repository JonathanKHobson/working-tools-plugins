# Career Studio project map

`plugin.json` is the portable root manifest; `.codex-plugin/plugin.json` and `.claude-plugin/plugin.json` are host manifests. `PROVENANCE.json`, `PUBLIC_FILE_MANIFEST.json` and `LICENSE-SCOPE.json` hold per-file source and rights records. `skills/` contains nine independent entrypoints: `resume`, `cover-letter`, `portfolio`, and `application-statements` create or audit proof and answers; `portfolio-package` assembles requested site/resume/deck sets; `campaign` coordinates role packets and private records; `submissions` handles authorized employer forms, receipts, and reconciliation; `career-interviews` prepares role/stage-specific practice and compensation decisions; `career-outreach` prepares professional messages, proposals and counteroffers. Each skill's `references/`, `templates/`, `design/`, and `agents/` folders retain its substantive source material. `references/providers.md` routes output work to existing document, PDF, presentation, Sites, and UX owners.

Career evidence and application records stay in their owning private project, never in this plugin. Edit a skill's canonical copy here, then validate that skill and the plugin. The optional Atlas MCP launcher uses a recipient-owned external runtime and binding for career methods; no hooks, corpus or user-data store are packaged. Job Application Compass remains a separate private operator-owned runtime.

Validation:

```sh
python3 <system-skills>/plugin-creator/scripts/validate_plugin.py <plugin-root>
python3 <system-skills>/skill-creator/scripts/quick_validate.py <plugin-root>/skills/resume
```

Repeat the skill command for each changed entrypoint and check relative links. Change the relevant skill and its supporting resource, not unrelated skills or the external provider.

`references/private-workspace.md` defines the external personal-data boundary. Candidate records, answers, receipts, case provenance and dashboards never belong in this package. `scripts/check_share_safety.py` checks package content before export; a clean scan is not a substitute for reviewing the actual archive.

The conditional [provider procedure map](../library/source-procedures/INDEX.md) identifies complete official installed skill routes. Affected first-party entrypoints load a matching provider only when discovered and retain their own workflow when it is absent.

`references/compensation-and-offers.md` owns the conditional salary-expectation, offer-comparison and negotiation method shared by Interviews and Outreach. Its worksheet, worked example and provenance stay beside it; personal offers and decision records stay in the private career workspace. This adds no discovery head or tool.

The conditional AI Job Search additions are split among campaign (discovery, evidence intake, posting research, fit and skill gaps), resume (tailoring/readback), cover-letter (language and final checks), application-statements (portal fields) and career-interviews (practice). Full original selected procedures and MIT notice are inactive under `libraries/ai-job-search/`; `PROVENANCE.md` records excluded regional CLIs/installers, custom template/font dependencies, background/provider setup and personality assessment defaults. No new head, provider, hook or personal-data store is added.

- `references/atlas-library.md`: scoped career Atlas retrieval and private human library. `scripts/atlas_library_mcp.py` and `.mcp.json` launch the fixed domain against a shared external index; no corpus is packaged.

LinkedIn profile depth lives in resume/references/linkedin-profile.md and rubric.json; LinkedIn connection/DM/inbox procedures live in career-outreach/references/linkedin-conversations.md. references/evidence-story-bank.md extends existing private evidence for profiles/interviews/social handoffs. Selected exact MIT sources and research/adaptation boundaries are in libraries/linkedin-agent/. No new head, account connection or personal-data store.

The original full local resume/letter/portfolio build and audit methods are conditional `references/local-method.original.md` support in their current skills; existing reference/template/agent trees remain their support owners.

The [provider procedure map](../library/source-procedures/INDEX.md) routes complete externally maintained depth skills when actually discovered. The copied 38-file provider corpus is preserved only in the private baseline archive; public provenance records exact exclusions and hashes. The [example Atlas binding](../examples/runtime-bindings/atlas-library.json) has placeholders only. Codex uses plugin-relative `cwd`; Claude uses `${CLAUDE_PLUGIN_ROOT}` for the same launcher.
