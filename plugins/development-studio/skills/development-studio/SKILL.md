---
name: development-studio
description: "Explain Development Studio or scope a software change before implementation. Use for software delivery and architecture; games belong to Game Creation Studio."
---

# Development Studio

For capability or setup questions, use the [introduction](../../README.md). Explain one relevant first task without starting a build. For explicit work, identify the repository, user-visible outcome and verification evidence, then select one focused workflow. Do not run every workflow in this package.

Read [method adaptation](../../references/method-adaptation.md) before a preserved Superpowers method. Read each selected method completely and its required support. The snapshot provides the actual procedure; the route below selects it. Current host tools and user authorization govern execution.

## Shape the change

1. Read the project instructions and map, current branch and dirty state. Identify the maintained implementation, related tests and accepted UI when relevant. Use Work Management project-structure when available; preserve current conventions.
2. State the triggering user action, expected result, affected components and the smallest complete behavior slice. Resolve uncertainties that would change architecture; infer routine choices. A narrowly specified fix can go directly to implementation.
3. For meaningful design choices, apply the complete [brainstorming method](../../libraries/superpowers-6.4.2/skills/brainstorming/SKILL.md), including its behavioral questions and tradeoffs. Scale documentation to the decision. Record decisions in the owning project, not plugin-global state.
4. Turn the accepted behavior into an executable implementation through [implement software](../implement-software/SKILL.md). For failures use [debug software](../debug-software/SKILL.md). A plan-only request stops with a reviewable plan.

For a requested interface design or architecture improvement with concrete maintenance friction, read [module design review](../../references/module-design-review.md). Ordinary fixes keep their existing direct route.

## Added complete standalone methods

- Native macOS architecture, menus, windows, files and packaging: [Native macOS App Builder](../native-macos-app-builder/SKILL.md).
- Exact/semantic navigation and rename boundaries: [Code Intelligence](../code-intelligence/SKILL.md).
- ChatGPT Apps SDK: [ChatGPT Apps](../chatgpt-apps/SKILL.md).
- Small web-game implementation/test loop: [Develop Web Game](../develop-web-game/SKILL.md); broader game design/production stays with Game Creation Studio.
- GitHub review comments or CI: [Address Comments](../gh-address-comments/SKILL.md), [Fix CI](../gh-fix-ci/SKILL.md).
- Full local diagnosis and installation review: [Systematic Debugging](../systematic-debugging/SKILL.md), [Safe Install Review](../safe-install-review/SKILL.md).
- Go method and authorized corpus retrieval: [Golang Effective](../golang-effective/SKILL.md).
- Docker/PocketBase/local preview/Quick Tunnel: [Local App Pipeline](../local-app-pipeline/SKILL.md).

## Select by outcome

- Web UI, data or payment feature: [build web software](../build-web-software/SKILL.md).
- iOS/macOS app or Android emulator issue: [build native software](../build-native-software/SKILL.md).
- Interactive MCP app: [build MCP apps](../build-mcp-apps/SKILL.md); local data-backed MCP or attachment failure: [local MCP systems](../local-mcp-systems/SKILL.md).
- Regression confidence: [test software](../test-software/SKILL.md).
- Review feedback or release readiness: [review and release](../review-and-release/SKILL.md).
- Method evaluation or session diagnosis: [evaluate development workflows](../evaluate-dev-workflows/SKILL.md).

For game mechanics, asset production or a playable game, use the separate Game Creation Studio or official Game Studio. Security findings go to the installed security owner. Product strategy outside implementation belongs to Work Management product-definition.

The original [using-superpowers method](../../libraries/superpowers-6.4.2/skills/using-superpowers/SKILL.md) is preserved for provenance and framework migration questions. It is not a universal conversation hook. Discovery in this package uses the focused routes above.
