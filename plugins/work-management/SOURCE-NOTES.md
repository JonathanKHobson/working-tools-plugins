# Release status

Promoted to the maintained personal plugin on 2026-09-23. The notes below document staging decisions and are historical. Use README and the shared skill-plugin-map for current ownership.

# Work-management consolidation notes

Staging only. This directory is not installed or registered. The **three** entry points and shared references are new synthesis. Local supporting references, templates, examples, and scripts have been copied under `libraries/` so the retained depth is available on demand. No vendor executable, hook, generated prompt corpus, or global source was copied or changed.

## Source to target disposition

| Source | Target / disposition | Packaging requirement |
|---|---|---|
| Local `focus-ops-manager` | `skills/focus-work`; full reference copy in `libraries/focus-ops-manager/references/` | The core loads operations selectively. Profile, goals, weekly log, old investigations and routing history stay on demand; they are not injected into the core prompt or treated as current approval. |
| Local `prd-strategist` | `skills/product-definition`; references and `create_change_packet.py` in `libraries/prd-strategist/` | Formal PRD, table patterns, and change-packet paths are linked conditionally. The script's runtime creates files only under the caller's chosen output root. |
| Local `plain-to-dev` | `skills/product-definition`; all four reference files in `libraries/plain-to-dev/references/` | The core handles ordinary translation; glossaries and beginner/idea-to-spec detail remain optional. |
| Local `project-structure-architect` | `skills/project-structure`; references, templates, examples and scripts in `libraries/project-structure-architect/` | Domain-specific detail and scaffold/audit helpers remain on demand. No scaffold is run by default. |
| Local `critical-compass` | **Distinct full specialist remains enabled**; `references/reasoning-check.md` is only a shared lightweight decision check for focus/product | Its 12-file library, MCP bridge, scored snapshot, culturally grounded lens guidance, and distribution artifacts are not replicated. No overlapping reasoning-review entry point remains. |
| Local `vibe-check` (MIT, upstream `TexasBedouin/vibe-check`, local commit `f675bbe`) | Optional `references/beginner-discovery.md` synthesis; keep original specialist for full beginner mentoring, diagrams, checkup, distribution/cold-start and visual blueprint | Do not bundle its renderer, templates, examples, or release helper by default. Preserve attribution and review license if any source text/assets are later copied. Do not route human-writing requests to it. |
| External `ai-psychiatry` 0.6.0 (MIT) | No runtime dependency | One useful idea—observable completion rather than semantic loopholes—is represented by ordinary verification. Its always-on compiled inventory, generated files, and execution-control framework are not adopted. Safe to disable for this plugin only after confirming no other task depends on it. |
| External `superpowers` 6.4.1 (MIT) | Retain as separate developer specialist | Its TDD, debugging, Git worktrees, code review, and plan execution are outside this management consolidation. Its universal skill trigger and approval hard gates conflict with the user's scope and standing authorization; do not import them. Disabling it globally is **not** justified by this candidate. |

The external plugin identities and versions above were checked against `work/plugins-before-consolidation.json` and the installed manifests. AI-Psychiatry and Superpowers each declare MIT in their manifests and include a LICENSE file. Their text was not copied.

## Caller and release risks

- Search and update exact references to `focus-ops-manager`, `prd-strategist`, `plain-to-dev`, `project-structure-architect`, `critical-compass`, and `vibe-check` in local skills, AGENTS files, routing index JSON/Markdown, automations, and any package manifests before disabling those names. A new description alone will not repair a direct skill call.
- Known high-impact callers include `~/.codex/skills/skill-authoring/SKILL.md`, `~/.codex/skills/focus-ops-manager/references/skill-routing-index.md` and `.json`, and cross-links in `frontend-ux`, `local-data-mcp-builder`, `ux-writer`, `pattern-picker`, and `native-macos-app-builder`. The user-provided AGENTS.md also names Focus Ops operational paths. Migrate active pointers, not historical mentions.
- The copied Focus Ops operational references still contain absolute machine paths and old skill-name references. Their meaning is local and some older inventory/history may be stale. Update active commands and routing records deliberately before replacing the old owner; do not bulk-rewrite historical evidence.
- Keep Critical Compass and Vibe Check available as distinct specialists. Disabling them would remove formal scored audits/MCP distribution and the full beginner mentoring/diagram journey respectively.
- Copied project-structure and PRD scripts/templates are available but are not automatically invoked. Before moving them to a shared public package, inspect provenance and personal paths. This is a private candidate.
- Remaining absolute paths in the staged library appear in `libraries/focus-ops-manager/references/skill-provenance-catalog.md`, `skill-mcp-improvement-backlog.md`, and `mcp-registry.md`; these are local inventory/history, not portable commands. The operating-protocol file also names local Codex scripts and mounted volumes by design. Review those live paths when the host changes.
- Before release, validate YAML/frontmatter, relative links, intended direct and bypass prompts, and any copied script with representative input. Inspect plugin registration and disablement only after the new package is installed and callable. Confirm operational and deep-specialist paths in the actual host, not just this staging folder.

## Staging checks

- Three entrypoints pass the system skill-creator `quick_validate.py` using the supplied PyYAML path. Manifest JSON parses, and all relative Markdown links in the staged package resolve.
- The copied PRD change-packet script produced a six-file sample packet under sibling `work/consolidation/work-management-validation/`. The copied project-structure scaffold script produced a generic sample there; its audit helper reported no large source files. Their `--help` commands succeeded.
- No provider, hook, browser, install, or live task workflow was run. Script samples establish basic execution and output shape, not full behavior across project types.
