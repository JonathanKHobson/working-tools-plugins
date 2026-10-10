# UXHC Evidence Collection Guide

UXHC ratings should be tied to observable evidence or an explicit evidence limit. Use this guide when preparing screenshots, URL captures, Playwright observations, or code-aware notes for an audit.

## Evidence First Rule

For every material finding, capture:

- what was observed
- where it was observed
- which heuristic it affects
- what state was visible
- what state was not visible
- whether the issue is direct evidence or host inference

Do not treat a guessed interaction state as observed evidence.

## Screenshot States By Heuristic Group

| Heuristic group | Helpful states to collect |
| --- | --- |
| H1 Status | loading, progress, success, save confirmation, refresh, submitted, delayed response |
| H2 Real-world match | labels, page headings, domain terms, form examples, category names, help text |
| H3 Control and freedom | back, cancel, close, undo, edit, delete confirmation, exit paths |
| H4 Consistency | repeated components, navigation variants, button styles, form patterns, desktop/mobile equivalents |
| H5 Error prevention | required fields, destructive actions, disabled states, validation hints, confirmation steps |
| H6 Recognition | menus, breadcrumbs, filters, visited states, selected states, visible choices |
| H7 Efficiency | shortcuts, defaults, repeated task flows, saved preferences, keyboard paths, mobile effort |
| H8 Minimalism | above-the-fold priority, competing calls to action, clutter, visual hierarchy |
| H9 Error recovery | inline errors, error summaries, invalid input, recovery copy, retry states |
| H10 Help | help links, tooltips, onboarding, examples, documentation, support paths |
| H11 Accessibility | focus, keyboard path, contrast risk, labels, target size, captions, alternatives |
| H12 Inclusion | representation, tone, consequences and uncertainty at high-stakes steps; assumptions about resources, identity, language, safety. Separate observed behavior, participant self-report and reviewer inference; pixels or facial expression alone do not establish emotion. |
| H13 Journey | entry point, next step, handoff, confirmation, completion, dead ends |
| H14 UX writing | button labels, headings, instructions, errors, empty states, plain-language clarity |

## SPA And Client-Side Routing

Single-page apps can mislead quick captures. Watch for:

- page title still showing a generic title
- visible "loading" or skeleton states
- delayed text after hydration
- buttons that appear before handlers are ready
- route changes that do not reload the page
- data that appears after a delay

Use a bounded wait before judging the final state. If the host has Playwright or browser capture support, capture after the page settles and note the wait. If the state still cannot be observed, record an evidence limit.

## Settled Responsive and Prototype Evidence

Before measuring or comparing renders, wait for fonts, relevant images, hydration,
and stable layout. Wait again after text resizing, orientation, or viewport changes;
record the viewport and state. At narrow widths and 200% text size, verify each
required navigation destination is visible or accessible through the intended menu.
Hidden DOM links and a no-overflow result do not prove usable wayfinding.

A screenshot, Stitch screen, or Claude preview establishes only the states actually
shown or exercised. Label static, simulated, and implemented behavior separately.
For forms and handoffs, distinguish a visible success state, service acknowledgement,
and verified external receipt. Prefer mocked failures for QA; use real sends only
within the user's authorization. Do not silently pass untested recovery paths.

## Playwright Observations

Playwright observations can count as evidence when they directly observe rendered behavior, such as:

- a visible label, heading, button, link, or error message
- an element not appearing after a bounded wait
- keyboard tab order or focus visibility
- a submitted form showing an error or success state
- a responsive layout at a named viewport
- a click changing or failing to change a visible state

Playwright observations should not be treated as evidence when they are only:

- inferred from code without rendering
- based on a selector name that users cannot see
- based on hidden DOM content
- based on network logs without user-visible consequence
- from an authenticated or out-of-scope page

## Code-Aware Evidence

Code can support an audit, but it does not replace visible evidence.

Use code observations to say:

- "This may affect H11 because no label is visible in the markup supplied."
- "This suggests H1 risk because loading state handling was not found."
- "This should be confirmed in the rendered UI before final scoring."

Do not say:

- "Users failed this task" unless user evidence exists.
- "This violates WCAG" unless a real accessibility review supports it.
- "The rating is high confidence" when rendered behavior was not observed.

## Evidence Limit Contract

When a state cannot be observed, write the limit explicitly:

```json
{
  "checklist_item_id": "h01_d_04",
  "reason": "Loading and delayed response states were not captured.",
  "confidence_impact": "Rating may understate severity if users often wait on this screen.",
  "evaluatable": false
}
```

Use low confidence when evidence is partial. Use "not evaluatable" when the missing state is central to the checklist item.

## Single-Screen Vs Multi-Page Scope

Use a single-screen audit when:

- the user asks for one visible screen
- the target decision is above the fold
- the task can be judged from one state
- the goal is quick triage or coaching

Use multi-page or task-flow coverage when:

- the finding depends on entry and exit points
- H3, H7, H9, H10, or H13 are important
- the user asks whether a task can be completed
- errors, confirmation, recovery, or handoff states matter
- desktop/mobile comparison is requested

If the user asks for a launch-readiness judgment from one screenshot, call that a limited snapshot review and recommend follow-up capture.

## Minimum Evidence For Report-Ready Audits

Before report generation, confirm:

- source status is ready
- platform is named
- user goal is named
- active heuristics are clear
- every checklist rating has evidence refs or evidence limits
- confidence is set honestly
- missing states are not silently treated as passes

For emotion or workload claims, read the complete [emotion evidence](../../design-studio/references/human-systems/emotion-evidence.md) or [workload tradeoff](../../design-studio/references/human-systems/workload-tradeoffs.md) method; a reviewer hypothesis is not a participant measurement.
