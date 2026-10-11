# Codex hook coverage

Reviewed October 11, 2026. This record distinguishes source availability, optional registration and runtime behavior. It is a curated inventory, not an export of the author's configuration.

| Hook family | Event | Published source | Setup boundary |
| --- | --- | --- | --- |
| Artifact-review tracking | `UserPromptSubmit` | [Codex host hooks](../integrations/codex-host-hooks/) | New portable edition of the previously host-local helper and its quality-state dependency; opt-in configuration |
| Scoped closeout reminder | `Stop` | [Codex host hooks](../integrations/codex-host-hooks/) | New portable edition of registered lifecycle behavior; private diagnostic CLI, global process/MCP scans and memory logging omitted |
| Gmail review gate | `PreToolUse` for supported send and forward tools | [Solo Service Operations: Gmail send review](../plugins/solo-service-operations/skills/gmail-send-review/) | Already published; recipient setup is optional and must match the receiving tool names. It is not a universal interceptor for browser or other-provider sends |
| Prompt-crafting advice | `UserPromptSubmit` | [Prompt Playbook hooks](../plugins/prompt-playbook-studio/hooks/) | Already published with its owner; distinct from artifact-review state tracking |
| Interface craft review | `PostToolUse`, `Stop` | [UX Design hooks](../plugins/ux-design-toolkit/hooks/) | Already published with its owner; receiving runtime and trust must be checked |
| Work setup, continuity and review reminders | `UserPromptSubmit`, `SessionStart`, `Stop` | [Work Management optional hooks](../plugins/work-management/optional-hooks/) | Already published as optional templates and helpers. The author's local automatic registration is not installed by the public package |

## What the inventory established

Three commands were registered in the author's global hook file: artifact-review tracking, closeout and Gmail review. Current personal plugin sources also supplied Prompt Playbook, UX Design and Work Management hook declarations. The last four families in the table already had published implementations and have not been duplicated or repackaged in this addition.

Prompt Playbook and UX Design declarations matched their public counterparts. Work Management's local default declaration maps to the public optional template. The local Gmail helper differs from the public helper in one validation message about voice review; the inspected checks and control flow match. This wording difference is disclosed rather than described as exact byte parity.

Configuration and trust-state inspection do not prove that a hook recently fired. The inventory did not execute personal hooks or alter their trust, registration or runtime state. Public integration tests use fictional inputs and isolated local state; their scope is documented in the integration README.

## Portable host integration

The two previously uncovered lifecycle hooks share artifact-quality state, so they ship together as an [optional source integration](../integrations/codex-host-hooks/). They do not add a plugin to either marketplace. Their owner boundaries follow the existing prompt-quality and Work Management responsibilities.

The public edition retains scoped review tracking and closeout reminders. It excludes the author's diagnostic integrations, account-specific service names, private paths, instruction text, prompt excerpts, memory store and conversation content. Its provenance file describes transformations from the source helpers. It is a portable edition, not a claim that every byte of the private host helper is included.

Review the source and tests before using it. Follow the manual merge and disable instructions in its README. Never copy a complete personal `hooks.json` from someone else, overwrite unrelated hook entries or trust a changed definition without inspecting it. Codex hook sources accumulate, so check for duplicate handlers. [Official hook discovery and trust documentation](https://learn.chatgpt.com/docs/hooks).

For the wider context, see [Behind the tools](system-context.md). Package versions and plugin install evidence remain in the existing [release registry](../catalog/packages.json) and [compatibility record](compatibility.md).
