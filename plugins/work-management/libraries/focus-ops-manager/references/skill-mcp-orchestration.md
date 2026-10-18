# Task, model and tool routing

Use for substantial work that could benefit from delegation or uncertain tool
ownership. Start from one user goal and its observable completion evidence.
the receiving user’s explicit request authorizes a native goal for actionable work: check the
current goal, create one if none is unfinished, and reuse the unfinished goal for
follow-up work. Do not replace or complete a goal to make room for another; the
lead marks it complete only after verifying the requested outcome.
Ordinary edits, one-step actions and short answers need no orchestration pass.

## Choose the smallest useful worker

Current host metadata (2026-09-10) supports these choices. This table is a routing
heuristic, not measured pricing or a benchmark. Recheck callable tools/model
metadata when starting work; do not assume these aliases exist on other hosts.

| Work | Starting choice | Escalate when |
| --- | --- | --- |
| Inventory, extraction, formatting, known checks | gpt-5.6-luna, low/medium | Sources conflict or a failed check needs diagnosis |
| Bounded code changes, source research, synthesis | gpt-5.6-sol, medium | Architecture or ambiguity spans several systems |
| Everyday coding alternative | gpt-5.6-terra, medium | The current host or task favors another model |
| Judgment, cross-system debugging, visual orchestration, integration | gpt-6-astra, medium/high | High/xhigh only when added reasoning resolves real complexity |
| Fast narrow coding in a supported durable task | gpt-5.3-codex-spark | Not offered by the subagent API on this host |

Use the current task's configured lead model; instructions cannot silently
switch the already-running model. Do not raise reasoning effort by habit. Check
the available API: this host's subagents accept Luna/Sol/Terra/Astra/5.5, but not
Spark. Native task tools expose Spark. If a model override needs an explicit user preference, use only the receiving user's current preference where host policy permits; otherwise preserve the task's model. Tell the user when a specifically requested model is unavailable and name the
fallback. Unsupported overrides should fall
back once to a supported appropriate choice, not trigger retries or a new CLI
agent runtime.

## Delegate when the split pays for itself

Proactively delegate substantial work through a suitable verified worker when
a bounded outcome can progress independently while the lead does useful work.
For authorized Claude access and a useful independent lane, actively dispatch through
`claude-toolkit:claude-operation`, rather than waiting for a per-task request.
That skill owns Sonnet/Opus selection and CLI-first execution. Use another verified
worker when it fits better; keep trivial or inseparable work local.
For Gemini/Antigravity CLI and comparative task fit, use
[CLI model routing](../../../skills/worker-delegation/references/cli-model-routing.md).
The host capability record owns dated availability and tested commands; do not
confuse an installed model or provider claim with a demonstrated best choice.
Use a subagent for a step or subtask within the current goal. Start with 1–2
workers, or 3 for three clear independent lanes when capacity permits. The current host has four total concurrent agent
slots including the lead. Stay within the live limit and check pressure once
before broad/parallel work; pressure remains advisory.

Give the worker only:

- outcome and scope, with a clear stop condition;
- relevant paths or sources and allowed side effects;
- required checks and return format;
- model/effort appropriate to the difficulty.

Prefer `fork_turns="none"` with a compact brief for mechanical work. Use a few
turns only when recent conversational context is essential. Full history is
appropriate only when the worker needs it; on this host full-history forks do
not accept model overrides. Do not ask multiple agents to reread the same
corpus, spawn workers to wait, or make a worker rebuild context the lead already
has. Review findings and inspect relevant edits; do not rerun all their research.
Escalate a failed attempt with its evidence rather than restarting blind.

Example: one lead judges portfolio evidence; Luna checks asset/link manifests;
Sol implements a bounded export fix. The lead integrates and reviews the changed
visual anchors. A ten-word copy change stays local.

A receiving user may also authorize bounded work through available Claude, standard
ChatGPT Web, Gemini, Stitch, and Claude Design subscriptions. For research,
drafting, or design exploration where offloading pays off, read
[subscription-offload.md](subscription-offload.md). Use this capacity proactively
for a useful substantial lane; trivial work needs
no offload, and no task needs a mandatory second-model vote. Deeper research
defaults to standard ChatGPT Web with Pro mode when available, not the special
Deep Research feature. Use that feature only when explicitly requested.
Continue independent work while an external job runs; preserve unrelated jobs and drafts.

For a local text or speech worker, consult the existing host capability record at
`~/Documents/ChatGPT/Managing My Computer/docs/capabilities.md`.
It contains tested commands and their limits; recheck the selected route and
external mount before use. Keep one local inference active at a time and unload
afterward. On another computer, verify its own runtime and capacity instead of
copying these host-specific paths. No local worker is required for a trivial task.

For a multi-chat initiative, read [one-lead initiative coordination](../../../skills/worker-delegation/references/initiative-coordination.md). Consider coordination at the outset using independent durable outcomes and owner/context boundaries rather than raw step count.

## Subagent or separate task

Subagents are the default for steps and subtasks within one goal that should
return to the lead. Use separate native chats for multiple independent durable
goals that benefit from persistent context or later user follow-up. If the user explicitly requested separate chats for those goals, apply that request only when the current creation tool accepts it, and never interpret
it as permission to create chats for ordinary steps. If the tool requires a new
explicit request, keep the work in the current chat until that request exists.
Reuse an appropriate existing chat where possible. Sending it a prompt requires
explicit user authorization under `send_message_to_thread`; discovery or a
worker's request is not authorization. Never hijack work awaiting a user decision
or unrelated active work.

For native task creation, list projects and respect the tool's repository
isolation defaults. A shared-checkout coordinator is a special project mode:
load `codex-coordinator` only when coordinating actual shared-checkout writers,
read its marker and operations, and follow its declared boundaries. Do not apply
its shared-checkout rules to ordinary worktree tasks or create a claim board for
parent-owned read-only subagents. Do not edit a vendor cache to change policy.

Assign disjoint files/outputs; let one owner integrate shared generated files.
One worker owns a live browser/Figma session. Other workers use exported evidence
or separate files and do not steer the same UI concurrently.

Wait for subagent results through native completion notifications. For separate
tasks use compact `wait_threads` with cursors; read older turns only for missing
evidence. Extract only the messages needed from `read_thread` responses because
commands can be verbose even with `includeOutputs=false`. Avoid repeated polls
or progress ledgers. A durable task does not promise automatic wakeup of its
parent. Do not add a timer, heartbeat or background manager unless requested.

## Tools, skills and memory

Use a purpose-built API/CLI before manual UI when it can inspect and verify the
same result. Discover a narrow tool, not all enabled tool schemas. Use scripts
for deterministic repeated transformations; runtime dependencies already bundled
with Codex are preferable to another install. API availability and edit semantics
must be checked before choosing a fallback.

Proactively load the smallest relevant installed plugin skill that owns the
output; the user need not name it. At the start of every new or continued
project, consult `work-management:project-structure` and its owning project map
or architecture instructions. Consult again when scope changes, reusing
guidance already in context; consultation does not require new folders or a
refactor. If routing is uncertain, read just
the relevant family in `skill-routing-index.md`. Avoid loading both standalone
and packaged copies or all chained reviewers. A skill package groups distribution;
it does not require loading every skill in it.

Keep stable preferences in global instructions, project paths/state in the
project map, reusable procedures in skills, and durable decisions in memory.
Current artifacts come before historical notes. Use narrow KSB search only when
continuity changes the answer. Do not summarize every turn into memory or start
a second transcript store. For recent task lessons record the failure, correction,
verified example and scope in the owning skill reference; avoid product-specific
rules in general orchestration.

Stop after the requested evidence passes. Report uncovered limits once. Track
instruction bytes/estimated tokens, retries and tool round trips as proxies;
actual account spend, electrical energy and quality savings require measurement.
Parallelism may reduce elapsed time while increasing total tokens.
