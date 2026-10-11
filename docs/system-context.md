# Behind the tools

A plugin supplies a workflow. The result also depends on the model, the host, its instructions, the available tools and the context supplied for the task. Installing Working Tools gives you the published package. It does not give you my private workspace or reproduce every condition behind a demonstration.

This guide explains those differences so you can adapt the system and diagnose unexpected behavior. The public companion page is [Behind the tools](https://working-tools.jkylehobson.chatgpt.site/behind-the-tools/).

## What changes behavior

| Layer | What it contributes | What you receive |
| --- | --- | --- |
| Plugins and skills | Reusable methods, references, scripts, templates and optional tool connections | The files and declared dependencies in the selected public release |
| Host and project instructions | Expectations about scope, evidence, style, permission and project conventions | This explanation and an illustrative starter, not my private instruction files |
| Hooks | Commands triggered at defined points, such as prompt submission, tool use or closeout | Existing packaged hooks, plus a separate optional host-hook integration; activation requires your host setup and review |
| Current conversation | The brief, corrections, supplied examples, decisions and results available in that chat | Your own task context; no private conversation history |
| Persistent memory and retrieval | Relevant saved preferences or prior decisions, when the host supplies or retrieves them | No personal memories, knowledge stores, client records or memory credentials |
| Other agents and chats | Bounded assignments, returned findings and explicit handoffs | Public coordination guidance; no automatic access to my other chats or accounts |

Model versions, permissions, connected accounts, runtime dependencies and source material can also change the outcome. A successful install proves availability, not the correctness of every answer. [Tested compatibility](compatibility.md) separates installation checks, representative execution and untested integrations.

## Instructions: share the working principles

My setup emphasizes a concrete task, the existing source owner, verified outcomes and careful handling of private data. Project instructions add the local architecture and the commands that actually validate that project. A writing task may call for a final prose review; a visual deliverable may require inspecting its rendered result. Those are working expectations, not evidence that a review occurred.

The [illustrative instruction starter](../examples/AGENTS.starter.md) is a newly written, curated example of those principles. It is not an export or line-by-line redaction of my private instructions. It contains no personal profile, private project names, host paths or account configuration. Review it before adapting it to your own project. It is not loaded automatically by this repository or by installing a package.

Keep durable working agreements in instructions, task-specific facts in the brief and reusable procedures in the relevant skill. Avoid copying a long personal setup simply because it appears in a demonstration. Codex discovers global and project `AGENTS.md` guidance according to its host rules; those files do not override platform protections. See [OpenAI's instruction guide](https://learn.chatgpt.com/docs/agent-configuration/agents-md).

## Hooks: available is different from active

Some hooks are already part of published plugins, and Work Management supplies optional hook definitions. Their source remains with those owners. The [hook coverage record](hook-coverage.md) maps each reviewed hook family to its source and setup boundary.

The separate [Codex host hooks integration](../integrations/codex-host-hooks/) publishes portable prompt-review tracking and closeout behavior that previously lived only in my host setup. It is an optional source integration, not a new plugin or an invisible prerequisite for all 31 packages. Its README identifies what was retained and what was omitted from the private diagnostic helper.

The public integration tracks review obligations in local scoped state. A Stop hook can ask the agent to continue when a scoped obligation remains open. A recorded completion is a claim made by the caller; the hook cannot inspect a screenshot, judge prose or prove that a review was adequate. Its resource reminder does not terminate processes or establish ownership of a running service.

Read the code, run the isolated tests, merge only the hooks you want into your own configuration and review them through your host's hook controls. Do not overwrite existing hooks. Codex combines matching sources, and installing a plugin does not automatically trust its hooks. Duplicate registrations can produce duplicate reminders. [OpenAI's hooks guide](https://learn.chatgpt.com/docs/hooks) describes discovery, trust and disabling a hook.

## Memory and conversation context

In my environment, retained preferences and project decisions can be supplied as context or retrieved through an authorized tool. That may help the agent avoid repeating a decision or locate an existing owner. It can also introduce stale assumptions. Before an action that depends on current state, the agent should check the actual files, settings, source or service.

The public releases contain no personal memory records. This page describes their role without publishing examples from my memory store. A recipient can use a plugin with their own sources and context; optional private-library integrations require the recipient's own authorized data and configuration.

A long conversation can affect a result even when memory is off. Corrections, earlier drafts, examples and previous tool results remain relevant only to the extent they are available to the current run. Compaction and handoffs can omit detail. Restating the accepted goal, source, constraints and unresolved question is more reliable than assuming a new chat knows everything.

The memory behavior described here is specific to my configured environment, not a guarantee about every host. Check the receiving product's [memory controls and limits](https://learn.chatgpt.com/docs/customization/memories).

## How work travels between agents and chats

A lead may give a worker a narrow assignment and selected context, then inspect its returned evidence before integrating a change. Some workers receive more history than others. Separate chats exchange information through explicit tool calls or maintained handoff records; this collection does not make every conversation globally visible.

In this workflow, a reusable lesson becomes shared behavior only when it is deliberately retained in an authorized record or used to revise a maintained instruction, method or implementation. Exchanging messages does not, by itself, retrain the underlying model or update every other chat. Worker agreement is not independent proof: workers can share the same incomplete sources.

Give each worker an owner, inputs, expected output and stop condition. Review concurrent edits together before release. Sending material to another provider is a separate data-sharing decision; a plugin does not supply an account or authorize disclosure. See [OpenAI's subagent guide](https://learn.chatgpt.com/docs/agent-configuration/subagents) for the host mechanism.

## Try the package under known conditions

1. Choose one release and follow its installation guide. Record the package version, host and model you used.
2. Start a fresh chat or isolated test workspace with a fictional task and explicit source facts. A fresh chat may still receive global instructions or memory; inspect those settings rather than assuming they are absent.
3. Ask which skill, instructions, hooks and tools were actually used. Treat an agent's answer as a lead, then check available host records and outputs.
4. Test the basic method before adding optional hooks, private sources or extra agents. Add one influence at a time and compare the same task and acceptance criteria.
5. If a result depends on missing context, supply the smallest relevant facts. Do not copy private memory or a complete conversation to imitate someone else's setup.

For a support report, include the package version, host/model, a sanitized task, expected result, observed result and relevant hook state. Leave out secrets, full instructions, private memories and raw account logs. [Support](../SUPPORT.md) explains where to report it.

## Scope of this record

Reviewed October 11, 2026. Hook source coverage is documented separately from runtime activation. The public hook release has its own tests and provenance. These records describe inspected code and scoped checks, not identical results across models, blanket safety enforcement, a complete audit of every account or evidence that all configured hooks recently fired.
