# Prompt Playbook Studio

Write, repair and test prompts that preserve the intended task, using focused methods, optional Prompt Compass workflows and selected pattern references.

## What you can do

- Turn an objective into a ready-to-use prompt.
- Repair a prompt from an observed failure without losing useful constraints.
- Build a traceable handoff brief or compare prompt behavior on meaningful cases.

## How to start

1. Select this plugin in a supported host, or name the workflow in your request. Describe the result you want and provide the inputs listed below.
2. Start with one useful task. The assistant should explain the relevant capability, required input/access and expected result briefly when that helps; an explicit task can begin immediately.
3. Check the result and its reported state. A draft, local file, sent message and published result are different outcomes. Ask “what else can this plugin do?” or “help me get started” whenever you need the wider menu.

## Try a first task

| Ask | Bring | Expect |
| --- | --- | --- |
| “Fix this prompt; it keeps dropping the second deliverable.” | Original prompt and a failed output. | A bounded revision and explanation of what changed. |
| “Help me get started with Prompt Playbook Studio.” | A task you want an AI to accomplish. | A suitable prompt workflow and one usable first prompt. |

## Choose a skill

The table is a selection guide. Once a task matches, read that complete skill; follow only its applicable support-file routes.

| Skill | Use it for |
| --- | --- |
| [execution-briefs](skills/execution-briefs/SKILL.md) | Compile a complex request into a reviewable handoff brief with traceable constraints and authorization. |
| [prompt-design](skills/prompt-design/SKILL.md) | Design a new prompt from an objective, with explicit inputs, constraints, examples, output shape and success checks. |
| [prompt-evaluation](skills/prompt-evaluation/SKILL.md) | Compare prompt versions or build repeatable tests for prompt behavior, using observable criteria and preserved run evidence. |
| [prompt-knowledge-retrieval](skills/prompt-knowledge-retrieval/SKILL.md) | Retrieve reusable patterns, task templates and glossary entries from Knowledge Atlas, or route an explicit Prompt Compass diagnosis. |
| [prompt-patterns](skills/prompt-patterns/SKILL.md) | Select and adapt reusable prompt patterns or templates for organizing, refining, role framing and structured outputs. |
| [prompt-playbook](skills/prompt-playbook/SKILL.md) | Choose the right prompt workflow when the request is ambiguous or spans several modes. |
| [prompt-refinement](skills/prompt-refinement/SKILL.md) | Repair an existing prompt using observed failure, preserving its intent, examples, constraints and useful voice. |
| [prompt-safety](skills/prompt-safety/SKILL.md) | Review privacy, source boundaries, authorization and persuasion integrity in a prompt before use. |

## Recipient setup

Install this package in a supported host and select one of its eight skills. Supply your own task facts, prompt drafts, test cases and private profile in your project. The complete Prompt Engineer design, refinement, routing, evaluation and safety methods are a separate dependency: in Codex, enable the official `prompt-engineer@openai-curated-remote` plugin and use the [installed-provider handoff](references/provider-prompt-engineer.md) after verifying live discovery. That provider route is not verified in Claude. If it is absent, use the complete first-party Playbook, original patterns, evaluator and MIT compiler; identify the missing optional provider pass accurately. No provider method body or personal data is bundled.

## Tools, setup and access

When configured and discovered, `prompt-compass` supplies diagnosis/build/refinement workflows and `atlas-prompt` supplies scoped references. If Compass is missing, design or refine directly with the selected first-party skill and state that no Compass diagnosis occurred. If Atlas is missing, use the bundled original patterns and templates, and do not invent a retrieved record. Read the [backend contract](docs/backend-integration.md) before a Compass workflow, then use `route_prompt_request` for an unqualified Compass request. Preserve actual pace questions and pause states. Read [Atlas guidance](references/atlas-library.md) only for reference lookup; search then read selected IDs. Private runtime paths live in `~/.config/studio-tools/compass.json` and `atlas-library.json`, not in prompts. The optional Framework Builder needs a recipient-configured Atlas Python environment with Python 3.10 or newer and its MCP dependencies; the package does not install that backend.

Writing a prompt does not execute the task inside it. Prompt Compass interaction gates remain in force; a pattern lookup is not a completed diagnosis or rewrite.

Installation makes a package available; it does not establish a working server or permission for every action. These private bindings are host-specific; another host needs its own supported configuration. For a local backend, check the Codex launcher in `.mcp.json` or the Claude launcher in `.claude-plugin/plugin.json`, a recipient-owned binding and required mounted files. Verify tool discovery and one harmless scoped read/overview. Keep credentials in the provider’s supported setup, never in a chat or this README. Report missing configuration, unreachable service, insufficient permission and an empty search as different conditions. Preserve the original task through setup; verify uncertain writes before retrying. Any historical verification notes are dated evidence, not current readiness.

## Submission advisory

In Codex, the package-owned `hooks/hooks.json` is discovered automatically. Claude declares `hooks/claude-hooks.json` through its plugin manifest. Once the host activates and trusts the hook, `UserPromptSubmit` runs the read-only advisory for each submitted prompt; it emits a brief hint only for relevant prompt-crafting requests. It makes no backend calls, changes no submitted prompt and persists no prompt data. Review and trust any non-managed hook definition in the host before activation. To stop the advisory, disable Prompt Playbook Studio in the host plugin manager; Codex also lets a recipient review or revoke hook trust through `/hooks`. The local script checks verify only its logic, not native hook firing. See [hook behavior and verification](docs/prompt-hook.md).

## Reading routes for the assistant

- For a concrete task, go directly to the selected `SKILL.md`; this README is not required reading for every run.
- For a capability/help question, use the introduction, first-task examples, skill table and relevant setup section, then recommend one first request. Skip maintainer notes unless the question concerns an update. On first relevant use, give a brief task-specific orientation; do not replay a tour on every invocation or claim the user has been permanently onboarded.
- Load the full selected procedure and its required support. References explain methods; scripts execute only the authorized operation; templates/assets are output material. Preserved libraries are conditional depth, not a bulk context load.
- Check actual callable tools and action/resource scope before promising access or completion.

## Maintenance

Edit this maintained `prompt-playbook-studio` source; the public package is its byte-identical distribution copy. See [project map](docs/project-map.md). Validate changed skills and links, update through the native personal marketplace, and compare installed files with source. Source files and cached installations are distinct; never patch a generated cache.

## Interactive framework builder

Ask “Open the framework builder” to choose a source-backed framework, fill its specific fields and inspect the assembled prompt before Copy or Send. “Find a framework” uses source metadata to suggest candidates. Assistant-only searches stay separate from the widget. The catalog preserves original field hints and assembly and records Atlas provenance. [Coverage, checks and host setup](docs/framework-builder.md). A newly installed server needs a later host activation; local browser tests do not prove native acceptance.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional agents

[Studio roles and assignments](references/professional-agents/README.md) connect these skills to named jobs. Work Management maintains cross-studio coverage and handoffs; native registrations are installed separately for each host.
<!-- END PROFESSIONAL-AGENTS -->
