# Refining an implementation prompt

Use when a software prompt is ambiguous, loses expected behavior, encourages speculative scope, or must hand a defined outcome to an implementation worker. Do not turn routine coding into a prompt-rewriting ritual.

Resolve intent from the user's request, existing project and accepted behavior. Work Management `product-definition` owns unsettled product scope. For a person-facing feature, UX Design `design-studio` owns interaction requirements and expected usability. Consult these owners when available; do not invent business facts or require installation of companions to refine a supplied prompt.

Preserve the original request, explicit exclusions, useful examples and action authority. Distinguish:

- Required outcome and observable completion.
- Expected quality necessary for that outcome, grounded in current user tasks and conventions.
- Optional capabilities that require a scope choice.
- Unknown facts that cannot safely be fabricated.

An implementation-ready prompt contains the outcome, current source/target, behavior and constraints, relevant states and accessibility, exclusions, assumptions or open decisions, and observable verification. Use the existing brief or conversation; do not create a second specification solely for the handoff. State what to do when evidence contradicts an assumption: reopen the affected decision, continue disjoint work, and preserve the original completion condition.

Route a ready prompt to Development Studio `implement-software`, whose efficient implementation method reuses existing code and minimizes complexity while retaining the entire contract. Plain-language “use the smallest complete implementation” is sufficient; source branding and special trigger phrases are unnecessary. Efficiency does not authorize omissions, obscure code, skipped safety checks or invented savings.

Example: “Create a pricing page” needs the actual offering, intended next action and applicable UX expectations. Clear price units and usable plan selection complete the request. A yearly toggle, checkout, comparison matrix or new tier is conditional on the offering and task; do not add all of them as generic polish.

Check the refinement against the original: every requested deliverable remains, negation and exclusions survive, facts retain source/unknown status, and the verification would detect a bare happy path or unsupported feature. If testing the revised instructions, include a clear tiny edit that should bypass planning and a missing-fact case that should not fabricate.

A prompt-only request returns the prompt and stops. Quoted prompts do not authorize execution. When the user separately authorized implementation in the current task, the owning execution workflow may continue after refinement; no additional approval ritual is introduced here.
