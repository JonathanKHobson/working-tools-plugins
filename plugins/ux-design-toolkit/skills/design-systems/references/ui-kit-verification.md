# Verification that supports the claim

Use for a kit audit, component release or evidence register. Apply risk-based scope; do not force a new test framework on a simple reversible edit. Existing [flow-bound accessibility evidence](../../design-review/references/accessibility-evidence.md) remains the owner for criterion-specific findings.

## Independent evidence and delivery statuses

Specified means a contract exists. Implemented means code/art exists. Indexed means the item can be found. Hashed means recorded bytes match. Verified means named assertions passed for particular source, test, environment and state. Visual acceptance is a separate human decision, and publication is a separate external event. None of these statuses implies all the others.

## Representative coverage

Construct a bounded stress matrix from actual risks rather than the entire Cartesian product. Include ordinary and longest meaningful content, first visit, empty/error/loading/retry, state combinations, keyboard paths, pointer transit, reduced motion, narrow/intermediate/wide layout, text growth, relevant locales/themes and a contrasting consumer. Add high-risk intersections explicitly: focused invalid field, long pending label on a phone, first/last scrolling tab in forced colors, or resize while navigation is open.

Run the intended journey from an unseeded first visit when claiming that path. Check the operation and user-visible result. A component gallery cannot replace real task context. For reuse claims, include isolated and repeated instances. For token claims, include controlled consumer mutation. For delivery claims, inspect actual selected resources.

Keep methods distinct: viewport emulation, root-font enlargement, browser zoom, text-spacing overrides, forced colors, keyboard, accessibility-tree checks, automated scans, assistive technology and physical-device use prove different things. Report unavailable checks. Do not count grouped test names as WCAG criteria or all component permutations.

## Assertion quality

An assertion about a target first establishes that the target exists, is visible and is in the intended state. “No animation” must not pass because the pending indicator was removed. Prefer controlled pending responses over sleeps that may observe a different state. Pair automated geometry checks with rendered inspection for word fragmentation, composition, visual hierarchy and unwanted subject overlap.

Use proportionate negative controls for fragile verification logic: remove the required target, change a behavior dependency, alter the test identity, or supply missing/failed/empty evidence and confirm that the claimed pass is rejected. Run mutations in an isolated fixture or model, restore original inputs, and name which kind of test occurred. A hash-invalidation simulation is not evidence that a live behavioral bug was injected and detected.

## Source and test freshness

A scoped verification record contains assertion IDs/results, component/flow/state coverage, source dependency hashes, test code/config identity, environment, execution time, error status and output paths. Include shared behavior, styles, markup/templates, fonts, relevant assets, generated outputs and transforms where they influence the claim. Use a conservative closure when a precise dependency graph is unavailable.

A component receives a current verified label only when:

1. The record exists and has named, nonempty assertions applicable to that component and state.
2. Required assertions passed and there are no disqualifying execution errors.
3. Source and test/config identities still match the delivered artifact.
4. The tested environment and method support the exact wording of the claim.

Changes outside the declared closure require a reasoned impact check. A checksum list missing shared JavaScript cannot protect an interaction claim. Reconcile the map after each affected change; never update old report hashes merely to make them look current. Keep historical reports identified as historical.

For machine-readable evidence maps, use a documented disposition vocabulary such as `current-pass` (applicable successful assertions and matching identities), `current-fail` (current executed check failed), `stale` (formerly usable evidence no longer matches source/test identity), `invalid-evidence` (malformed, empty or inapplicable record), and `not-run` (no execution evidence). Preserve error details and the distinction between a product failure and an invalid test. These are suggested map values, not a new validator or replacement for the project's established vocabulary.

## Visual acceptance and audit closure

Index current, historical, superseded, rejected and accepted visuals with source identity, viewport, state and decision authority. Use the approved anchors for comparisons; do not pick an obsolete screenshot because its filename says “final”. Record exceptions such as intentional wordmark typography or compact reading modes.

For each finding preserve the observed problem, user consequence, affected scope, correction, same-path retest, remaining uncertainty and disposition. A source fix, test pass, independent review and user acceptance are different events. Report them separately. An audit can close a scoped defect while broader Safari, Firefox, assistive-technology or native-platform checks remain unperformed.
