# Codex hook coverage

Reviewed October 27, 2026. This record distinguishes reusable source, registration and runtime behavior. It is a curated inventory, not an export of the author's configuration. The release registry identifies the downloadable version of each owner.

| Hook family | Event | Public owner | Setup boundary |
| --- | --- | --- | --- |
| Artifact-review tracking and scoped closeout | `UserPromptSubmit`, `Stop` | [Work Management](../plugins/work-management/) and the earlier [standalone host integration](../integrations/codex-host-hooks/) | Work Management owns the reusable review engine. The standalone integration remains available for manual setup. Avoid duplicate handlers; private diagnostic and account adapters are excluded. |
| Task setup, continuity and decision reminders | `UserPromptSubmit`, `SessionStart`, `Stop` | [Work Management optional hooks](../plugins/work-management/optional-hooks/) | Review the receiving host's registration and trust settings. A reminder is not proof that work or review happened. |
| Writing review reminder | `UserPromptSubmit` | [Writing Quality Studio](../plugins/writing-quality-studio/) | The portable editorial-context hook points to the writing review workflow. It contains no personal voice profile or correspondence. |
| Gmail send review | Tool-specific `PreToolUse` where configured | [Published Gmail send review](../plugins/solo-service-operations/skills/gmail-send-review/) | The public method remains in Solo Service Operations; the current local setup routes this work through Writing Quality Studio. Personal sender bindings and private host registration stay private. This is not a universal interceptor for browser or other-provider sends. |
| Prompt-crafting advice | `UserPromptSubmit` | [Prompt Playbook hooks](../plugins/prompt-playbook-studio/hooks/) | Keep the host's supported declaration with its owning package. It is distinct from artifact-review state tracking. |
| Interface craft review | `PostToolUse`, `Stop` | [UX Design hooks](../plugins/ux-design-toolkit/hooks/) | Project opt-in, receiving runtime and trust must be checked. Imported upstream reference hooks are not additional recommended registrations. |
| Implementation context | `SessionStart`, `UserPromptSubmit`, `SubagentStart` | [Development Studio](../plugins/development-studio/) | The package owns its implementation runtime and host-specific declarations. Check the installed host and exact release; a source declaration alone does not establish execution. |
| Personal brand/client context, usage records and release bookkeeping | Host-dependent | Private host setup | These depend on personal sources, local records or publication controls. Their roles are disclosed here; private bindings, data and operational configuration are not distributed. |

## What the inventory established

The inspected global `hooks.json` is now empty. The author's current installed plugin declarations supply the lifecycle behaviors instead. Some remain private adapters around reusable public methods. This replaces the October 11 snapshot, when three commands were registered globally.

The check covered the global file, current installed plugin hook declarations and the matching canonical/public package owners. Hook definitions retained inside an upstream reference library are source material, not evidence that the host activates them. No personal instruction files, memory records or conversation contents were copied into this record.

Source inspection does not prove that a hook recently fired. This refresh did not alter personal hook registration, trust or runtime state. Isolated public tests use fictional inputs and separate local state. Native activation and execution must be verified on the receiving machine.

## Choose one implementation for each job

Use a hook's existing plugin owner when it supplies the behavior you need. The [optional standalone host integration](../integrations/codex-host-hooks/) remains a documented alternative for scoped review tracking and closeout. It adds no marketplace plugin and is not required for unrelated workflows.

The portable editions omit personal paths, account-specific services, private instructions, prompt excerpts, memories and conversation content. Work Management's quality recorder can keep project-local review receipts without the author's private host adapter. A completion mark records the caller's claim; it does not independently judge a screenshot or prose. A closeout reminder does not terminate processes or establish their ownership.

Read the source and setup instructions, merge only the hooks you want, and review them through the host's controls. Do not overwrite unrelated configuration. Check for duplicate registrations and review changed definitions before trusting them. See the [official hook discovery and trust documentation](https://learn.chatgpt.com/docs/hooks).

For the wider context, see [Behind the tools](system-context.md). Package versions remain in the [release registry](../catalog/packages.json); installation and execution evidence remain in the [compatibility record](compatibility.md).
