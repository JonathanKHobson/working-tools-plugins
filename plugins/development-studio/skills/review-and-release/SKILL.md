---
name: review-and-release
description: "Review a diff or whole codebase, audit shortcut debt, handle feedback and finish a software branch or release with evidence."
---

# Review and release

For a diff review or whole-repository audit, read and apply the complete [quality review method](../../references/quality-review.md). It checks connected code, correctness, security, expected load, meaningful tests, speed and unnecessary complexity. For a requested shortcut/deferred-work ledger, use the read-only debt procedure in [runtime operations](../../references/efficient-operations.md). These are one-shot reports and do not switch implementation mode or authorize fixes.

Read [method adaptation](../../references/method-adaptation.md) before a preserved Superpowers method. Read each selected method completely and its required support. The snapshot provides the actual procedure; the route below selects it. Current host tools and user authorization govern execution.

- To prepare or request a review, apply [requesting code review](../../libraries/superpowers-6.4.2/skills/requesting-code-review/SKILL.md) and its full reviewer prompt.
- To act on comments, apply [receiving code review](../../libraries/superpowers-6.4.2/skills/receiving-code-review/SKILL.md). Verify a proposed defect against source and behavior before implementing it. Clarify ambiguous requirements only when they change the repair.
- To finish a branch, apply [finishing a development branch](../../libraries/superpowers-6.4.2/skills/finishing-a-development-branch/SKILL.md), adapted to the host’s actual worktree/PR controls.

Start with the final diff, relevant base revision, acceptance criteria and check outputs. Review behavior, regressions, edge cases and scope, and attach findings to concrete lines. Distinguish blocking defects from optional refinements. Follow each fix with the relevant check and review the integrated result.

Choose the delivery state the user requested. Preparing a PR body or build does not authorize a public release; existing explicit send/push/deploy authorization can be reused. When creating a PR in Codex attach it through the native artifact tool. Preserve required branch history and other workers’ changes. Remove only resources this task owns after verifying their work is saved.

Before declaring completion use [verification before completion](../../libraries/superpowers-6.4.2/skills/verification-before-completion/SKILL.md). Report local, committed, installed, merged, deployed and verified states separately. Signing, notarization, credentials and hosting remain external platform responsibilities in [provider setup](../../references/platform-providers.md).
