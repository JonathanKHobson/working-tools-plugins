---
name: implement-software
description: "Implement an accepted feature, bounded refactor or software plan with task ownership and reviewable verification."
---

# Implement software

Read [method adaptation](../../references/method-adaptation.md) before a preserved Superpowers method. Read each selected method completely and its required support. The snapshot provides the actual procedure; the route below selects it. Current host tools and user authorization govern execution.

1. Confirm the behavior contract, owning files and existing test commands. For uncertain locations read [code navigation](../../references/code-navigation.md). Preserve unrelated changes; do not treat a dirty checkout as permission to reset it.
2. For a multi-step change apply the complete [writing plans method](../../libraries/superpowers-6.4.2/skills/writing-plans/SKILL.md). Each step names files, an observable result and a verification command. Keep simple changes direct, and use the project’s established plan home.
3. Choose the execution route deliberately. Apply [executing plans](../../libraries/superpowers-6.4.2/skills/executing-plans/SKILL.md) for sequential local work. When bounded independent tasks justify authorized delegation, use [subagent-driven development](../../libraries/superpowers-6.4.2/skills/subagent-driven-development/SKILL.md) with its full implementer and reviewer prompts. Use [dispatching parallel agents](../../libraries/superpowers-6.4.2/skills/dispatching-parallel-agents/SKILL.md) for independent failures or lanes. Give disjoint file ownership and integration criteria; do not duplicate exploration.
4. When isolation is needed, apply [using git worktrees](../../libraries/superpowers-6.4.2/skills/using-git-worktrees/SKILL.md). First inspect existing attachments and the host’s worktree tools. Preserve the intended base and current uncommitted changes. Reuse a suitable worktree; a skill is not permission to discard one.
5. Implement the smallest coherent slice, exercise the behavior, and integrate the result. Route regression work to [test software](../test-software/SKILL.md); UI changes also use their platform’s rendered verification.
6. Review the final diff and report changed behavior, actual check outputs and unresolved gates. Use [review and release](../review-and-release/SKILL.md) for a requested PR/release. A local change does not imply deployment.

The preserved plan/SDD helper scripts are source assets. Read their complete call path and the admission notes before execution; no helper starts automatically on skill load. Native host task tools take precedence over historical config edits.
