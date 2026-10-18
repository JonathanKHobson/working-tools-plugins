---
name: apple-model-operations
description: Check and use Apple Foundation Models through the native fm CLI, evaluate bounded on-device tasks, or explain supported SDK and interface alternatives. Use when Apple is the selected model provider.
---

# Apple model operations

Operate a bounded Apple model task and return checked output with the actual route, readiness and limitations. For help, use the [toolkit introduction](../../README.md); help alone does not accept terms, enable services or run inference.

1. Read [CLI operation](references/cli-operation.md) for readiness, prompting and result collection. Check live command help and availability on the selected Mac. The default route is native `fm` where supported.
2. For model/surface selection or suitability, read [capabilities and task fit](references/capabilities.md). Distinguish local inference from Private Cloud Compute and distinguish Foundation Models from Siri.
3. Give one bounded task with relevant supplied context and a checkable output. For extraction, retain exact source wording, negatives and unknowns. Use a schema when supported; a valid schema does not prove factual correctness.
4. Execute within the authorized scope and time limit. Keep private prompts out of process arguments when a supported input mechanism is available. Do not enable tool calling, execute generated shell commands or move files merely because the model suggested them.
5. Verify successful nonempty output, factual correspondence, any truncation and actual model route. Record command/version or OS build and elapsed time in the owning project, not in shared plugin instructions. Close task-owned sessions. A local model failure is a reason to reconsider the task or prompt, not to silently send private data to a cloud model.

For substantial work, return the result to the coordinating lead; do not reproduce Work Management’s goal, delegation or provider-selection machinery. For a task too small to justify offloading, the lead can answer directly. Compare quality and overhead before claiming efficiency gains.
