---
name: debug-software
description: "Reproduce and diagnose a software failure using evidence, a falsifiable cause and a verified repair."
---

# Debug software

Read [method adaptation](../../references/method-adaptation.md) before a preserved Superpowers method. Read each selected method completely and its required support. The snapshot provides the actual procedure; the route below selects it. Current host tools and user authorization govern execution.

Use one primary debugging procedure: this route selects the preserved method below; if the existing `systematic-debugging` skill is already active, continue there and use the same conditional reproduction reference without starting a second diagnosis.

Apply the complete [systematic debugging method](../../libraries/superpowers-6.4.2/skills/systematic-debugging/SKILL.md) before changing code. Its root-cause tracing, defense-in-depth and condition-based waiting references remain available beside the source method.

For intermittent failures, performance problems or a reproduction that may miss the reported symptom, read [reproduction quality](../../references/reproduction-quality.md).

When the failure concerns a shipped app/native binary/bundle, source is unavailable, or shipped behavior conflicts with the repository, proactively use [Reverse engineer software](../reverse-engineer-software/SKILL.md) for the missing artifact evidence. The user need not name REA. Return findings to this diagnosis; do not start a second debugging loop or replace ordinary source navigation when it answers the question.

1. Capture the actual failure, expected result, environment, inputs and last known good state. Separate the observation from proposed causes.
2. Trace the failing data or state across boundaries. Use [code navigation](../../references/code-navigation.md) for definitions, call sites and exact configuration references. Find a working comparison and form one falsifiable hypothesis.
3. Run the smallest discriminating check. Change one causal factor; retain evidence when a hypothesis fails. After repeated failed fixes reassess the model of the fault rather than layering workarounds.
4. Repair the cause at the correct owner and add a meaningful regression check through [test software](../test-software/SKILL.md). Keep timing work condition-based rather than adding arbitrary waits.
5. Reproduce the original flow again and check nearby affected behavior. State what the evidence establishes and what remains environment-dependent.

For frontend rendering use Build Web Apps frontend-testing-debugging; for Apple runtime evidence or Android profiling use [native routes](../../references/platform-providers.md). For MCP launch/discovery use [local MCP systems](../local-mcp-systems/SKILL.md). These supply the actual platform tools and procedures.
