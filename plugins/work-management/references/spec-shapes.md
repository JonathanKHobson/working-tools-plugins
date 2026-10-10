# Product artifact shapes

Choose the lightest artifact the receiver can act on.

| Need | Artifact | Minimum contents |
|---|---|---|
| Name a concept | Translation | Precise term, platform context, behavior, common alias if relevant, and one ticket-ready sentence |
| Decide a first slice | MVP brief | User and painful moment, current workaround, one differentiator, required table stakes, in/out scope, validation signal |
| Build one capability | Feature spec | Trigger, flow, inputs/outputs, rules, roles, meaningful states, dependencies, observable acceptance criteria |
| Coordinate a consequential change | Change record | Why now, scope, decision and alternatives, implementation notes, ordered tasks, verification and rollback where relevant |
| Align multiple teams or a release | PRD | Problem, audience, outcomes, scope, requirements, acceptance criteria, risks, metrics, rollout, unresolved decisions |

Avoid a fixed ID scheme for every small request. Use stable IDs and traceability when several requirements or teams need to cross-reference them. Write acceptance criteria as observable outcomes; a Given/When/Then form helps when state and trigger matter. Phase work into vertical slices that can be demonstrated, not UI/backend/database layers that are useful only when assembled. Define a metric's source, denominator, and review window before claiming a target.

Discovery ends with a decision or a stop condition. If the user asks to think bigger, make expansion visible and name the cost; do not silently grow the first release. When evidence is thin, state the riskiest assumption and its cheapest credible check. Do not invent market size, user quotes, prices, delivery dates, or approval.

For a formally packaged document, use the current document skill. For a deep research question, use its research specialist. For UI wording, use the UX-writing owner. For implementation, hand the brief to the owning codebase and verify the actual behavior.
