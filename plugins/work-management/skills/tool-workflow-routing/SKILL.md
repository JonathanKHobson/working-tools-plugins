---
name: tool-workflow-routing
description: "Find the right installed skills and tools for a task, or explain how to start with Work Management."
---

# Find the right workflow

Use this skill to choose an installed method, explain Work Management, or resolve overlapping tools. Bring the intended result, relevant source and constraints. The result is one production owner, the needed specialists and a concrete verification step. A clear task can begin immediately.

For “what can this plugin do?” or getting-started help, read the introduction, first-task examples and skill table in [README](../../README.md). Recommend one useful starting request. Help alone does not start a scan or external action.

## Production handoff

For a software build, load `development-studio:implement-software` before implementation. When people use an interface, also load `ux-design-toolkit:design-studio` to define its information order, interactions and review states. Final reader-facing wording goes through `writing-quality-studio:natural-prose-editor`. These are responsibilities within one task, not automatic worker launches.

Reuse owners already loaded. A small, settled edit needs only the affected method and checks. Before handing off an interface, verify the task's meaningful rendered states and actions through the selected UX and implementation methods. A wording receipt does not establish interaction or layout quality.

## Discover, then load

The startup list contains domain entrypoints and frequently needed safeguards. Specialist skills can remain registered without appearing in that list. Absence there is not evidence of a missing capability.

1. Interpret the user's outcome in ordinary language, then choose the closest domain. Use the host's native skill tool for a known exact ID. If only file tools are available, read the [maintained family map](../../libraries/focus-ops-manager/references/skill-routing-index.md) and follow its entrypoint links. With command execution, use the bundled read-only lookup when ownership is unclear or a specialist is absent from the visible list:

   ```sh
   python3 /path/to/work-management/scripts/skill_discovery.py --json search "survey branching"
   python3 /path/to/work-management/scripts/skill_discovery.py --json search "recovery" --owner ux-design-toolkit
   python3 /path/to/work-management/scripts/skill_discovery.py --json show "writing-quality-studio:natural-prose-editor"
   ```

   Resolve `/path/to/work-management` from this skill's package root (two parent directories). Keep the actual project as `--cwd` when running elsewhere. The lookup queries Codex's live native registry, returns full descriptions and exact paths, excludes disabled skills from search, and exits. It does not call a model, install anything or maintain another catalog.
2. Use a few domain terms, not a whole conversational prompt. The lookup matches words; you supply the semantic translation. If no match, try a broader task term or inspect the relevant owner's README. `owners` lists installed families. An empty match, disabled skill and failed native lookup are different states. For a host without this native API, pass one or more explicitly selected package roots with `--plugin-root /chosen/package` before the command. This portable mode reads only declared package metadata, preserves descriptions and exact paths, and labels installation/host activation as unverified. It honors explicit disabled state and never launches the native server. Optional `--manifest /chosen/selection.json` supplies roots and boolean policy without a generated catalog; the [portable onboarding and input shape](../../README.md#discover-skills-on-another-host) explains it. With no roots, `--portable owners` returns an empty selection. If local execution is unavailable, use the [maintained family map](../../libraries/focus-ops-manager/references/skill-routing-index.md) and its exact entrypoint links.
3. Read the selected `SKILL.md` and its triggered references before applying it. Search results describe capabilities; they are not the full procedure. Resolve same-name collisions by owner and path. Respect native enabled state or the selected portable input's explicit disabled state. Portable `enabled` means eligible for metadata lookup; verify actual host registration and tool access separately. Reuse unchanged material already read, and search again when the task expands into another domain.
4. Assign one production owner, then only the contributors and reviewers this output needs. Give a fresh worker the accepted task, selected skill path, inputs, constraints and acceptance evidence. Keep discarded ideas out of its brief unless they change its decision.

Native `$skill` selection remains available for registered specialists. Template selections retain their assets, previews and instructions. A hidden startup entry is an on-demand method, not a retired capability. Never replace meaningful descriptions with generic labels to fit the startup budget.

## Apply and verify

- A router read alone does not load the specialists. If an owner is unavailable, name that gap and use the supported method; do not report its review as completed.
- For a new or continued project, use `project-structure` before creating or reorganizing files. Reuse its guidance within the current context.
- For substantial unclear intent, use Prompt Playbook's `prompt-refinement` to define observable acceptance. Route by that result.
- When the problem, suspected cause or required method is unclear, use that skill's `references/problem-framing-and-method-selection.md` if available. Start with the smallest discriminating observation or source check, use live discovery and scoped Atlas search/read only for a real gap, then select the simplest sufficient workflow. Retain a supported conventional answer. A missing method or provider is a specific gap, not permission to invent retrieval or expand access. Clear requests proceed directly.
- For all authored reader-facing output, use Writing Quality's `natural-prose-editor`. UX owns information placement and states; the Humanizer owns final wording. A skill read or hook reminder does not prove a review happened.
- For independent substantial work, use `worker-delegation` and its tracked provider toolkit. Verify the returned work and actual provider evidence.
- Call a useful existing tool when it materially improves the authorized task. Verify actual availability, output and action scope; an installed skill is not a working provider.

## Conditional depth

Load only the matching section and required support in [the complete routing method](../../references/workflow-routing-detail.md):

| Need | Read |
| --- | --- |
| Unclear domain, overlapping owners, missing tool or external capability gap | Complete procedures to load; Workflow |
| Software product, codebase, shipped binary or reconstruction | Software artifacts and source questions |
| Chart, interactive panel, library chooser, visual question or artifact editor | Interactive work surfaces |
| Share an idea, create a website or choose a download destination | Sharing an idea versus creating a website; Interactive work surfaces |
| Named professional role | Professional roles |

For repeatable website data or turning a site into callable operations, use the [API Anything route](../../references/operations/api-anything.md). It includes pinned runtime setup, the full teaching procedure, CLI/MCP use and access boundaries for Codex, Claude and Gemini. Prefer an existing suitable official API or connected provider.

For public-page extraction or lightweight browsing, use the [Moli browser route](../../references/operations/moli-browser.md) when appropriate; keep authenticated or visual work with its existing browser. The full method retains provider boundaries, examples, recovery and source links. Ordinary small work does not need those sections. For a blocker, state the observed missing dependency and continue the useful supported part. Verify the requested end state before closeout.
