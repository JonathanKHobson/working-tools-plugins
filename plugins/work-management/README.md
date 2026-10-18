# Work Management Studio

This edition uses the [Compass licensing model](LICENSING.md): first-party code AGPL-3.0-only; first-party docs, prompts, skills, methods and eligible creative templates CC BY-SA 4.0. Upstream grants and prior release permissions remain valid. Author: Jonathan Kyle Hobson.

Turn a competing set of ideas or a complex assignment into a concrete deliverable, choose the right tools, and carry work through verified handoff.

## What you can do

- Choose the next useful outcome and keep scope from expanding.
- Define a feature, locate its owning project, or delegate a bounded piece of work.
- Review selected evidence, maintain plugins, or hand over work with its actual completion state.

## How to start

1. Select this plugin in a supported host, or name the workflow in your request. Describe the result you want and provide the inputs listed below.
2. Start with one useful task. The assistant should explain the relevant capability, required input/access and expected result briefly when that helps; an explicit task can begin immediately.
3. Check the result and its reported state. A draft, local file, sent message and published result are different outcomes. Ask “what else can this plugin do?” or “help me get started” whenever you need the wider menu.

## Try a first task

| Ask | Bring | Expect |
| --- | --- | --- |
| “I have three competing ideas; help me finish one useful thing.” | Current commitments, constraints and candidate outcomes. | One chosen deliverable and immediate action, with the displaced work explicit. |
| “What can Work Management Studio do, and where should I start?” | A brief description of the work or blocker. | A short capability introduction and the smallest relevant skill. |

## Choose a skill

The table is a selection guide. Once a task matches, read that complete skill; follow only its applicable support-file routes.

| Skill | Use it for |
| --- | --- |
| [evidence-review](skills/evidence-review/SKILL.md) | Review a deliberately selected project checkpoint for portfolio evidence, feedback and decisions; create scoped claim cards with human review before saving private evidence. |
| [find-skills](skills/find-skills/SKILL.md) | Find and fill demonstrated ecosystem gaps using repositories, skills, plugins, research or proven project methods; security-review and integrate into existing Studios and Toolkits first. |
| [focus-work](skills/focus-work/SKILL.md) | Evaluate new ideas, compare directions, resolve competing priorities and define one shippable outcome. |
| [parallel-work](skills/parallel-work/SKILL.md) | Coordinate explicitly opted-in tasks sharing one Git checkout, with clear file ownership. |
| [plugin-maintenance](skills/plugin-maintenance/SKILL.md) | Audit, merge, split, validate and update maintained plugins while preserving full procedures and actual provider capabilities. |
| [product-definition](skills/product-definition/SKILL.md) | Turn a product idea or feature request into the smallest useful brief, buildable requirements, or developer-language translation. |
| [project-structure](skills/project-structure/SKILL.md) | Consult the owning architecture at the start of every new or continued project and when scope changes; choose or repair file boundaries only when the current work needs them. |
| [tool-workflow-routing](skills/tool-workflow-routing/SKILL.md) | Choose the smallest useful skill, app or MCP for the requested result; explain the available Work Management workflows. |
| [work-handoff](skills/work-handoff/SKILL.md) | Package an idea or finished work as a shared-site page or a handoff with current state, next action and verification evidence. |
| [claude-delegation](skills/claude-delegation/SKILL.md) | Compatibility pointer to `claude-toolkit:claude-operation`; provider execution moved to that toolkit. |
| [worker-delegation](skills/worker-delegation/SKILL.md) | Proactively delegate substantial independent work to Codex agents, Claude or another verified worker; use subagents for steps and separate chats for independent durable goals under current tool authorization. |

## Tools, setup and access

When a recipient separately configures and registers the optional `atlas-work-management` launcher, it can retrieve scoped planning and collaboration methods from that recipient’s Atlas backend. Read [Atlas guidance](references/atlas-library.md) only when a reference lookup helps; after confirming the tool is available, search a few candidates and read selected IDs. Open the human browser only when the user is choosing or inspecting options. Without Atlas access, use the complete methods in this package and the user’s supplied sources. Hooks and evidence helpers are separate from this retrieval MCP.

The plugin supplies methods, selected local helpers and bounded hooks. Native host tools own goals/chats/automations; a request to plan or draft does not authorize sending or publishing.

Installation makes a package available; it does not establish a working server or permission for every action. The distributable package installs no automatic provider registration. The author's separate private checkout retains host-bound hook configuration, which is not a recipient default. For optional Atlas access, explicitly choose the receiving-host binding and inspect its runtime/data files. Verify tool discovery and one harmless scoped read/overview. Keep credentials in the provider’s supported setup, never in a chat or this README. Report missing configuration, unreachable service, insufficient permission and an empty search as different conditions. Preserve the original task through setup; verify uncertain writes before retrying. Any historical verification notes are dated evidence, not current readiness.

## Reading routes for the assistant

- For a concrete task, go directly to the selected `SKILL.md`; this README is not required reading for every run.
- For a capability/help question, use the introduction, first-task examples, skill table and relevant setup section, then recommend one first request. Skip maintainer notes unless the question concerns an update. On first relevant use, give a brief task-specific orientation; do not replay a tour on every invocation or claim the user has been permanently onboarded.
- Load the full selected procedure and its required support. References explain methods; scripts execute only the authorized operation; templates/assets are output material. Preserved libraries are conditional depth, not a bulk context load.
- Check actual callable tools and action/resource scope before promising access or completion.

## Maintainer and existing integration notes

Maintain the recipient’s own source checkout or chosen install source for `work-management`. Entry points live in `skills/`; detailed resources are conditional. Edit the maintained source, validate it, then update through the native plugin manager using the recipient’s selected marketplace or source, such as `work-management@working-tools` when installed from Working Tools. Never edit a generated cache. Start a fresh Codex task after an update when discovery does not refresh in the current task.

Historical standalone entrypoints are disabled compatibility redirects. Their old reference paths may remain for existing project instructions. The shared ownership/routing map is in [docs/skill-plugin-map.md](docs/skill-plugin-map.md).

The complete original UserPromptSubmit, SessionStart and Stop declarations are preserved as nonautoloaded templates in `optional-hooks/hooks.json`; the Claude template is `optional-hooks/claude-hooks.json`. No hook is installed by this package. If the recipient explicitly adopts a hook, select the actual stable package root/interpreter under current host support, preserve active sessions through an update and verify supported lifecycle events. The reminder also needs explicit WORK_MANAGEMENT_CONTEXT_OPT_IN=1 and actual recipient preferences. The Stop guard is quiet when there is no own active claim or `stop_hook_active` is true; it never blocks a turn on malformed input.

Manual project evidence review is available through `skills/evidence-review/`. The local Python helper nominates grouped claim cards from selected excerpts, validates provenance and human decisions, and saves confirmed private revisions inside the selected project. It adds no hook, service or MCP and does not bundle project evidence.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional agents

[Studio roles and assignments](references/professional-agents/README.md) connect these skills to named jobs. Work Management maintains cross-studio coverage and handoffs; native registrations are installed separately for each host.
<!-- END PROFESSIONAL-AGENTS -->

## Prerequisites and missing-provider behavior

All fourteen skill heads and complete operative method/helper closures remain. The original private profile/health/relationship facts, goal entries and session record are excluded; same-path blank recipient templates preserve the selected continuity procedure. No hook or MCP registration is bundled in the public payload; private author-host bindings are separately preserved. Full optional hook declarations are in `optional-hooks/`; adopt only under current recipient authorization after reviewing host support and tools. `scripts/codex_work_start.py` emits no context unless `WORK_MANAGEMENT_CONTEXT_OPT_IN=1` is explicitly selected; verify actual user preferences rather than treating this package as standing permission.

Core methods work from supplied task/project evidence without an Atlas service. Optional Atlas helper requires Python3 and an explicitly chosen `--binding` JSON with reviewed interpreter, server and database. Other providers and native goals/chats/automations remain host capabilities. Dependencies are separately installed; exact callable tools and permission scope must be checked. All source examples using `PROJECT_VOLUME`, `RUNTIME_VOLUME`, `SYSTEM_DATA_ROOT` or `PLUGIN_ROOT` must be rebound to verified recipient-owned paths before execution. Historical inventories are provenance, not a deployment recipe or live availability claim.

For “delegate two tasks” when no authorized worker tool is available, report that worker execution is unavailable, retain the bounded assignments/acceptance evidence and complete independent local work. Do not claim a worker ran or create unrelated chats. For “save reviewed evidence” without a supplied output owner or human disposition, retain the pending card and required inputs; a draft does not authorize a private save. Synthetic tests establish local helper behavior only, not real worker integration, provider reads or permission adoption.

The source's closeout-hook regression suite targets an optional separately maintained host diagnostic, not a package implementation. Its entire test body remains, but runs only when `WORK_MANAGEMENT_CLOSEOUT_HELPER` explicitly selects a reviewed recipient helper; otherwise it reports a skipped external integration. The package's own coordinator, evidence-review, reminder, decision hint, role installation, scaffold and change-packet helpers are tested independently. Use Python3.11 or newer (`tomllib` is required for the role installer).

## Complete standalone methods

15 complete skill heads are retained. The added methods are `cross-codex-workflow-exchange`, `github-conventions`, `skill-authoring`, `obsidian-vault-router`. Complete references and operative helpers are included; only originating private binding/input records are projected to recipient templates. No automatic installation of providers, hooks or global configuration occurs.

For a first task, supply two fictional vault roots or a synthetic GitHub response and ask for the authorized next action. Cross-host access and vault providers must be verified separately. The GitHub refresh helper requires explicit `--owner` and `--output`, keeps the full original branch/tree metadata behavior and writes only to the selected recipient output. An unconfigured host map must yield a missing-binding explanation, not a fabricated successful synchronization.
