# Flow-bound accessibility evidence

Use when the review identifies an access barrier or the user requests accessibility verification of a particular flow. This is an evidence protocol for the existing full audit methods, not a replacement WCAG guide.

## Select the method and scope

Read the complete selected [design-review procedure](../../../docs/procedures/design-review.md) and its [host adapter](../../../docs/full-design-host-adapter.md). For web keyboard, semantics, widgets and assistive technology checks, also read the complete preserved [frontend accessibility reference](../../../libraries/frontend-ux/references/accessibility.md). Use the native audit/platform method for native apps; do not equate CSS pixels, points and dp. Existing source scores summarize review health, not proven WCAG conformance. Resolve criterion numbers, thresholds and exceptions against current W3C guidance before reporting a violation; the maintained [verification reference](../../design-studio/references/verification.md#current-web-accessibility-checks) already distinguishes target-size and focus/reflow requirements.

Define the actual entry link, flow end state, user role, revision/build, browser/OS, viewport in CSS pixels, zoom/text scale, theme and starting data/session. Record exclusions. Use existing 3–8 visual anchors; add selector, accessible name/role or native node ID where available. A screenshot, source warning or automatic scan is evidence of that check only. W3C recommends combining tools with human evaluation. [WAI evaluation](https://www.w3.org/WAI/test-evaluate/)

## Bind each finding to a reproducible check

Keep one row per barrier or material check, in the owning task record:

| Finding / anchor | Exact path and state | Node / region | Criterion + level | Method and action sequence | Expected / observed | Evidence | Status / retest |
| --- | --- | --- | --- | --- | --- | --- | --- |
| F1 / A2 | route, role, build, viewport, zoom, starting state | selector or name/role and approximate region | verified criterion or suspected risk | keys/actions, tool/version or AT/OS/browser combination | task outcome and focus/announcement actually observed | capture/log/time | failed, passed scoped check, unverified, or not applicable with reason; fixed build and rerun evidence |

For a keyboard check, start at the real entry and operate the affected task without pointer assistance: record traversal, activation, focus visibility, exit/return and the resulting state. Use the selected widget/platform method for appropriate keys. Test the function, including a keyboard equivalent for dragging where applicable; a list of focusable nodes does not prove operability. [W3C Keyboard, Level A](https://www.w3.org/WAI/WCAG22/Understanding/keyboard.html)

For screen-reader checks, name the actual assistive technology and version, inspect exposed name/role/state, and record the spoken result or a bounded transcript for the changed labels, errors or status updates. Do not claim an announcement from ARIA markup alone. If AT is unavailable, record that gap and retain a reproducible manual test for the receiver. For contrast, reflow or target checks, bind the measurement to the same rendered state, element and dimensions rather than a global palette value. Automated findings retain tool/version, tested page/state and exact node; manually adjudicate each relevant match.

## Fix and rerun the same path

When fixes are authorized, retain the original row, implement the smallest correction, then rerun the original entry, role, viewport/zoom, data state, action sequence and method on the fixed revision. Record any necessary changed precondition. Recheck the changed node plus its immediate predecessor/successor or close/return path when focus or state management changed. Preserve before/after evidence; a fresh scan on a different page or a mouse click does not close a keyboard finding.

Close a finding only when the failed outcome has been deliberately rerun and observed to pass. Report unresolved barriers and untested combinations separately. The handoff states exactly which flow, states, criteria and environments were checked; partial checks do not establish whole-product WCAG conformance.
