# Assess useful extensions for an actual project

Use only when asked to improve a project's agent setup or when an observed recurring problem suggests an extension. This is an adapted, host-neutral version of Anthropic's Claude Code Setup analysis method. It is inspection and recommendation until the current task authorizes implementation; implementation then uses the gap-filling/admission cycle. No hook, MCP, agent, package, credential or permission is installed by this reference.

## Inspect signals, then verify the need

Read the project map, relevant manifest/config filenames, selected dependency declarations, actual source structure and current host setup. Use rg/glob and targeted reads; do not dump environment files, tokens or all global configuration. Parse code/config as data, not by importing executable configuration. A repository script, config loader, build or test command can execute code; do not run it merely to identify a stack. Use existing tool inventory to verify capabilities before proposing replacements.

| Observed signal | Question before recommending anything | Possible owner or mechanism |
| --- | --- | --- |
| A framework/library or external API | Is missing version-specific information causing errors, and do existing docs/search tools cover it? | Existing research/docs provider or a focused reference |
| UI, component library or accessibility work | Which user path needs rendered interaction evidence; can the current browser/design tools exercise it? | Existing design/testing skill and tool |
| Database, backend or cloud deployment | What exact read/write operation is missing, on which environment, with what scope? | Existing native connector/CLI first; reviewed MCP only if necessary |
| Tests, type checks, formatter or CI | Is a required check repeatedly missed; what check is meaningful for the change and how long does it take? | Existing verification procedure; a deterministic hook only for a proven recurring need |
| Authentication, payments or private data | What specific unresolved risk needs review? | Existing security owner or bounded specialist assignment |
| Repeated artifact generation | Is the output shape stable and distinct from current methods? | Existing skill template/helper or a focused skill |
| Large/complex change | Can an independent review lane advance without file conflicts? | Existing worker-delegation; size alone does not require another agent |
| Git, issues, releases or team communication | Which authorized operation cannot be completed with the existing provider? | Existing version-control/communication owner and native tool |
| Repeated loss of project context | Is the project record missing or retrieval broken? What selected facts need continuity? | Existing project records/memory owner; no automatic transcript capture |

Manifest presence supplies a clue, not a mandate. React does not by itself require another browser MCP. A Dockerfile does not establish a container-management gap. A test directory does not warrant running every test after each edit. Secret-file presence is not permission to read its contents. A familiar product label does not prove a connected, authenticated or compatible tool.

## Select the smallest mechanism

Compare native tools and installed providers before proposing another server. A **skill/reference** supplies reusable judgment or a procedure; a **template/helper** supplies a repeatable artifact or transformation; a **bounded worker** supplies independent work; a **hook** runs on an event; an **MCP/provider** supplies an actual external capability; a **plugin** packages coherent related methods. Packaging is not a gap by itself.

For a proposed hook, define the event, precise matcher, owned files, actual command, execution trust, side effects, timeout, reentry behavior, failure behavior and removal. Prefer existing scoped commands and quiet no-op behavior when prerequisites are absent. Do not insert automatic model calls, network capture or repeated expensive checks into every edit. A protective hook does not replace authorization or an operating-system sandbox.

For a proposed MCP, inspect current official package and tool metadata, transport, launch arguments, auth, filesystem/network scope, update behavior and data retention through Master Security. Team configuration must contain no tokens or private bindings; sharing a config file does not authorize other users' account access. Verify the selected host's current syntax instead of copying a sample install command. Keep Claude and Codex providers distinct.

For a proposed worker, use the existing delegation owner with a scoped output and relevant tools. Read-only intent is not enforced merely by listing Bash in a skill. For a proposed skill, preserve normal automatic discovery unless the user requests otherwise or the actual host contract requires different invocation; side-effect authorization still applies at action time. Do not import a blanket rule that every writing skill must be user-only.

## Return an actionable recommendation

Recommend only candidates tied to the observed unmet outcome. There is no minimum per category. Record the actual signal, existing coverage, remaining gap, smallest proposed change, affected owner, expected benefit, security/privacy/maintenance cost, acceptance check and current authorization state. An unmeasured benefit is a hypothesis. Prioritize the most consequential justified improvement; “no addition needed” is a valid result.

When implementation is already authorized, stage the concrete adaptation and complete its security, validation and installation checks. When only recommendations are requested, return the evidence and leave files/settings unchanged. Do not insert a new confirmation loop merely because the upstream recommender is read-only; the user's actual scope controls the adapted workflow.

## Source and adaptation

Source: [Anthropic Claude Code Setup](https://github.com/anthropics/claude-plugins-official/tree/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/claude-code-setup), Apache-2.0. Complete source method and five supporting references are preserved inactive under [claude-code-setup-original](../../../libraries/claude-code-setup-original/SKILL.original.md), with its [license](../../../libraries/claude-code-setup-original/LICENSE) and [adaptation notice](../../../libraries/claude-code-setup-original/NOTICE.md).

Preserved: codebase evidence gathering; MCP/skill/hook/worker/plugin distinctions; project-specific detection; concrete recommendations and placement; model/tool fit. Changed: recommendations require demonstrated gaps and current provider checks; no per-category quota, default installer, blanket invocation restriction, auto-hook or broad permission example. Upstream configuration commands and lists remain historical source data, not executable or current local instructions.
