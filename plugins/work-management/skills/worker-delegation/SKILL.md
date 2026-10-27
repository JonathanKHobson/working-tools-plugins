---
name: worker-delegation
description: "Proactively delegate substantial independent work to Codex agents, Claude or another verified worker; use subagents for steps and separate chats for independent durable goals under current tool authorization."
---

# Worker delegation

When orientation helps, briefly name this skill’s outcome, needed input and expected result, then proceed. Broader help uses the [plugin introduction](../../README.md); skip maintainer notes unless needed.


Proactively delegate substantial work when an independent useful lane can advance while the lead works. Consider Claude and other suitable available models or subscription workers alongside Codex agents; select a verified capability for the task. Keep trivial actions local. The lead owns judgment, integration and checked completion.

Use subagents or bounded external workers for steps within one goal. Use separate Codex chats for multiple independent durable goals under a receiving user’s explicit request, subject to the current creation tool's authorization requirements; do not create a chat merely to run a subtask. Existing-chat messaging still requires explicit user authorization under its tool contract.

## Complete procedures to load

Select by the triggers below. Read the complete chosen procedure and its required support; skip unrelated variants. These links preserve the full methods.

- [Task/model orchestration](../../libraries/focus-ops-manager/references/skill-mcp-orchestration.md) — before substantial delegation; select a bounded lane, model and evidence contract.
- [Subscription offload](../../libraries/focus-ops-manager/references/subscription-offload.md) — when using an external subscription worker; dispatch, retain the job, and verify its return.
- `claude-toolkit:claude-operation` — when Claude is the selected worker; start with the official subscription CLI, verify account/model, and use its bounded login recovery before considering Desktop or Web.
- [Provider toolkits and model fit](references/cli-model-routing.md) — when selecting Gemini/Antigravity or DeepSeek/NVIDIA, comparing CLI workers, or deciding whether a local model is useful; verify the host capability record and retain model/output receipts.
- [Bounded worker supervision](../../libraries/focus-ops-manager/references/worker-supervision.md) when an active worker drifts, repeats a failure or returns uncertain completion evidence.
- [Reversible evidence packing](references/reversible-evidence-packing.md) only when a large local tool result or log must be shortened for a worker handoff.

## Workflow

1. Start from the native goal for the requested outcome; create it under the receiving user’s explicit request only if no unfinished goal exists, and reuse an unfinished goal for its follow-up work. Define scope, allowed side effects, ownership, stop condition and return evidence for each independent useful lane. Native goals are managed by the lead, not duplicated by workers.
2. Read the full orchestration method and the chosen provider guide. Check capability and subscription/runtime availability before dispatch.
3. Continue independent lead work. Inspect the completed result, distinguish advice from evidence, reconcile conflicts and verify the combined deliverable.

Give a fresh worker the current accepted outcome, relevant source excerpts, owned files, necessary constraints and acceptance checks. Include the exact applicable skill path or selected method when it governs that assignment; do not copy the whole plugin catalog or make each worker rediscover the same context. Omit brainstorm history and rejected alternatives unless they prevent a plausible error. Correct a superseded instruction explicitly when that worker already received it. A new worker assigned Y does not need the history of an unrelated X.

Check the whole brief, including examples and acceptance criteria, for discarded history. Define success in terms of the accepted task. For a macOS installation-copy assignment, “accurate steps matching the current Quickstart” is sufficient; the checks need not list unrelated ideas that were never assigned to this worker.

## Deliver and verify

Deliver the integrated result and meaningful verification. A dispatched or streaming worker is unfinished. Use parallel-work only for opted-in shared-checkout claims.

## Example boundary

Good: Claude reviews supplied security methods while the lead edits disjoint routing files. Bad: two workers rewrite the same file without ownership.

For substantial work with a useful independent lane and authorized Claude access, use `claude-toolkit:claude-operation` to dispatch that lane proactively while the lead progresses. It owns Sonnet/Opus selection, CLI-first execution, bounded recovery and checked return. Keep trivial or tightly coupled work local; do not require a per-task Claude request when standing authorization applies.

For a new initiative or expanded scope spanning independent durable outcomes, read [initiative coordination](references/initiative-coordination.md). Choose one human-facing lead by outcome, owner and context boundaries; use compact authorized handoffs and retain subagents/local work for shared-context steps.

When delegating design or evaluating an external swarm harness, read [resource-aware design handoffs](references/resource-aware-design-handoffs.md). Pass selected evidence and reuse rights to workers instead of asking each worker to repeat gallery research. Existing native workers remain the first route; a source describing swarms is not a reason to install another harness.

For idea/strategy councils, research perspectives or a decision requiring independent assessments, read [decision review and bounded councils](references/decision-council.md). It defines quick, exploratory, comparison and council modes, selected idea criteria, evidence limits and bounded peer review. A single-model perspective exercise must not be presented as independent reviewers.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports Program Manager, Project Manager, Council Moderator. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
