# Tool authority and finding calibration

This Toolkit method reviews an AI action path using source evidence and enforcement checks. It complements the existing injection-path, MCP and permission procedures; it does not invoke a live target merely to illustrate a concern.

## Review the action boundary

1. Inventory each relevant tool's accessible resources, authenticated identity, input fields, destinations, side effects, data returned and logging/update behavior. Read the actual schema, handler, policy and configuration where available. A friendly description is not proof of scope.
2. Identify which fields external content can affect: tool choice, resource ID, recipient, query, uploaded body, path or call sequence. Follow the value from source through retrieval/summary/model output to the parser and action handler. Keep transformation/provenance evidence instead of replacing it with an invented attack story.
3. Find the enforcement point for identity, tenant/user binding, destination/resource authorization, field types/bounds and permitted operation. Check whether the server validates those independently of model judgment. A broad token plus a refusal instruction leaves the server-side question unresolved.
4. Examine outputs as another possible input boundary. Minimize secrets and cross-user data; preserve source identity for content returned into later model turns. Tool-produced text cannot authorize a new action or a change to persistent memory.
5. Check duplicate calls, retry behavior and event order where those affect impact. Verify feasible idempotency, compensation or rollback, and redacted logs that retain useful denial/success evidence. A read-only display can still disclose sensitive information.
6. Propose controls at the failing boundary. Distinguish a proposed policy from deployed code and a deployed control from one exercised successfully. Apply the regression method to both an unauthorized attempt and the legitimate use that must remain possible.

## Findings and severity

Use an actual source locator and the path's preconditions. Distinguish an observed exploit outcome, a plausible reachable path, an ambiguous lead and absent evidence. Content mentioning an attack is not itself a vulnerability. A finding should explain the deviation, sensitive data or action at risk, who can supply the input and how the boundary fails.

Calibrate priority from reachable impact and preconditions. A cross-user private-data disclosure or unauthorized privileged action warrants greater urgency than a cosmetic response defect. Reduced likelihood from a narrow permission or unavailable capability must be documented, not assumed. Keep severity and confidence separate: a potentially severe path with missing handler evidence can have low confidence. Do not invent measured probability or detection percentages.

Each finding records: local ID, component/source, controlling actor, relevant evidence, preconditions, deviation/impact, severity rationale, confidence/evidence status, correction, enforcement point, harmless verification and residual gap. Avoid copying secret values into the report; identify the source location/type and route any confirmed exposure to its remediation owner.

## Exercise synthetic cases

Only run within the task's bounded authority and an isolated fixture where side effects are safe. Cover the hostile input, a benign quoted near miss, the legitimate request and a relevant identity/resource mismatch. For a forbidden email destination, assert that the send handler was not called, or that authorization denied it before transmission. For the authorized destination, check the intended operation succeeds in the fixture. A refusal sentence alone proves neither result.

For example, a retrieved invoice note proposes changing a payee and sending a copy externally. Review whether the note can change destination arguments, whether the handler binds the action to the authenticated user's allowed recipient, and what an actual denial logs. Keep the legitimate invoice lookup working. Do not run a real transfer or send a private invoice to demonstrate the path.

Return a finding-to-control-to-test record with pass/fail/untested results and the evidence actually observed. Static review, a successful synthetic fixture and live deployment are distinct states. No small corpus certifies an injection-free model or a complete security audit.
