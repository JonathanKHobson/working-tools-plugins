---
name: parallel-work
description: Coordinate opted-in parallel Codex tasks in one shared Git checkout using a bounded per-thread claim board. Use for an explicit shared-checkout coordination request or an already enabled project marker; ordinary work and Claude delegation do not use this native Codex board.
---

# Parallel Work

When orientation helps, briefly name this skill’s outcome, needed input and expected result, then proceed. Broader help uses the [plugin introduction](../../README.md); skip maintainer notes unless needed.


Use this skill only for an explicit shared-checkout coordination request or a repository with an enabled `.codex/coordination/project.yaml` marker. Its task-boundary board adds visibility to native Codex tasks; native task tools still own creation, status, messaging and transcripts. Claude delegation follows Work Management's ordinary task/model routing and never receives a Codex claim. A global plugin install enrolls no project.

Check the marker before other board state. `coordination_enabled: false` is an opt-out: continue normally and read no board records. An absent marker creates nothing unless the user directly requests project enablement or invokes this skill for real parallel work. An enabled schema-2 marker requires the exact project identity; enabled schema 1 must be migrated before coordinated writes. A task claims only its own exact native thread UUID. The board is advisory ownership metadata, not a filesystem lock or new source of permission.

| Action | Read only these references |
| --- | --- |
| Start, join, split, claim, complete or integrate | [operations](references/operations.md), [operational contract](references/operational-contract.md), then [execution](references/execution.md) |
| Send or act on a concrete peer collision or dependency | Above, plus [messaging](references/messaging.md) |
| Enable, disable or migrate project state | [installation](references/installation.md), [operational contract](references/operational-contract.md) |
| Recover a stale claim | [recovery](references/recovery.md), [operational contract](references/operational-contract.md) |
| Change this package or check compatibility | [maintenance](references/maintenance.md) or [doctor](references/doctor.md) |

The default is one task. Use two or three durable verticals only when the user requests coordination and the current native task tool permits their creation in the shared checkout. Reuse a suitable task before creating one. Do not poll, create background management, force worktrees, or promise automatic fan-in. Claims update at real lifecycle boundaries; the exact owner releases its claim when work ends. The SessionStart hook reads only the marker, and Stop reads only this task's claim. Neither hook enrolls a project or grants action authority.

For ordinary subagents, model choice, or Claude work, use `work-management:focus-work`. For project layout, use `work-management:project-structure`.

## Complete coordinator source

On an opted-in coordination task, **read the complete [original Coordinator procedure](../../libraries/codex-coordinator-original/skills/codex-coordinator/SKILL.md)** and its matching lifecycle, recovery, messaging, execution, installation and maintenance references. The full original package is retained, including scripts and hook declarations, as conditional operational/source material. Use this Studio's reviewed live scripts and stable hook paths for execution; the nested original hook file is not a second registration. Current explicit opt-in, exact-thread ownership and host authorization rules above govern all historical examples. Claude uses its real delegation tools, never the Codex-native board or hook commands.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports Program Manager, Council Moderator. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
