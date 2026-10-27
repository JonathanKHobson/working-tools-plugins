# Human expectations in an implementation handoff

Use when a person-facing software request needs a buildable behavior contract, or when an efficiency-focused implementation risks delivering only a bare happy path. Reuse the existing project brief and source/rendered evidence. A tiny settled edit does not need a new design phase.

UX owns what a person needs to understand, do and recognize at each relevant point in the requested journey. Product/Work Management owns business scope and facts. Development owns implementation choices and technical verification. Prompt Playbook can make the handoff explicit without replacing those decisions.

## Identify the required experience

Start from the named audience, task, context, existing product and requested outcome. Trace a person from entry to completion:

- What must they understand to make the next choice? Preserve meaningful prices, units, qualifications and consequences.
- Which action should they take, and what do they reasonably expect it to do?
- What is available, disabled, pending, empty, successful or failed on this path? Include only states the actual behavior can encounter.
- How do they recognize the authoritative result, correct an error, cancel or recover without losing work?
- What keyboard, focus, accessible-name, contrast, touch, viewport and content-length requirements matter here?
- Which existing components and behavior conventions should carry forward?

Separate observed product/user evidence, established conventions, and assumptions. Reviewer intuition is not user-research evidence. Resolve uncertainties proportionately through current source, the existing design or a focused question/test.

## Keep expected quality distinct from added capability

A field needs a label, usable focus behavior and relevant validation. Autosave is a separate capability. A pricing page needs understandable prices, what each offer includes and a workable next action. A billing-period toggle belongs only if the offering has those periods. A static page does not need artificial loading states. Preserve explicit exclusions and the user's choices.

Do not enumerate every conceivable feature or make attractive extras mandatory. Do not cut essential explanations, error recovery, accessibility or requested behavior to produce fewer elements or less code.

## Hand off and verify

Supply the relevant journey, expected results and states, reusable component/source anchors, exclusions, open facts and acceptance checks in the existing contract. A short interaction may fit in a paragraph. If new visual decisions are needed, use the established design/brand owner; this handoff does not rebrand or redesign the product.

Development Studio's `implement-software` then applies efficient implementation after the contract is ready. Simplicity is judged against the complete experience. Unexpected source behavior or missing dependencies reopen the affected requirement, not the whole design.

On return, use the existing Design Review procedure: inspect rendered changed regions, exercise the important journey and failure/recovery states, check keyboard and relevant viewports, and compare the result to the contract. A compiling implementation or lower line count is not evidence of usability. Record observed checks separately from untested requirements; do not invent participant validation.
