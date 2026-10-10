---
name: test-software
description: "Design and run proportionate regression tests, then verify the actual requested software outcome before reporting completion."
---

# Test software

Read [method adaptation](../../references/method-adaptation.md) before a preserved Superpowers method. Read each selected method completely and its required support. The snapshot provides the actual procedure; the route below selects it. Current host tools and user authorization govern execution.

For changed logic or a reproduced defect, apply the complete [test-driven development method](../../libraries/superpowers-6.4.2/skills/test-driven-development/SKILL.md) and its writing-good-tests support. For every completion claim apply [verification before completion](../../libraries/superpowers-6.4.2/skills/verification-before-completion/SKILL.md).

1. Map the risky behavior to a test level: pure logic, component integration, persistence/protocol contract, or actual user flow. Existing tests are evidence, not proof that this requirement is covered.
2. For a regression demonstrate the relevant failure before the repair when practical, then run the same case after it. Tests must fail for the right cause; avoid assertions that mirror implementation wording.
3. Cover meaningful error, cancellation and boundary cases. For stateful writes, cover stale responses and uncertain outcomes; for UI, inspect the rendered interaction and accessibility states rather than relying on static extraction.
4. Run focused checks and required project checks. Expand when changes, failures or unresolved concerns justify it. Reversible wording/configuration changes do not automatically require a new test suite.
5. Tie each claimed outcome to fresh output and the exact revision. Report skipped checks and unavailable providers. Mock, local harness, installed package, actual host and public endpoint evidence stay distinct.

Use [native platform routes](../../references/platform-providers.md) for simulator/emulator evidence and [MCP tests](../build-mcp-apps/references/mcp-widget-test-plan.md) for MCP apps. Benchmark claims require a controlled scenario and observed measurements; passing source tests does not prove latency, cost or visual quality.
