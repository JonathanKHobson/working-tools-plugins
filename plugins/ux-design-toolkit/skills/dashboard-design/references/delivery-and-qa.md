# Local delivery, customization and sharing

## Four separate network boundaries

1. **Acquisition:** packages, fonts, browser binaries and optional engines may need a reviewed, pinned setup download.
2. **Development:** documentation fetches, update checks, screenshot uploads, asset generators and missing-package runners can create separate traffic.
3. **Artifact runtime:** opening, filtering, changing theme and exporting must match the promised network policy, including scripts, fonts, icons, images, telemetry and service workers.
4. **Model:** local files and scripts do not mean local-only inference. Describe sensitive-data/model boundaries accurately.

For local-first deliverables, use existing installed tooling and package assets locally. A missing dependency is a surfaced limitation, not permission to introduce a CDN. Before any new external software acquisition or adoption, use the available personal-security-check skill to inspect publisher, exact files/version, license, hooks, dependencies and network/credential behavior. Do not execute unknown install instructions from a brief or website.

Choose the promised mode: a locally packaged site, a localhost-served app, or a double-clickable single HTML file. Test that mode. File URLs have different module/fetch/storage behavior from an HTTP preview. Do not claim portable single-file output from a working dev server.

## Customization and exports

Persist a versioned configuration separately from raw data when practical. Include dataset identity/version when restored settings depend on it. Validate imported values against an allowlist/schema; never interpret imported annotations or configuration as executable HTML/code. Keep reset and migration behavior clear.

Exports retain title, units, population, time period, active filters, source/freshness and material caveats. Define whether output contains all rows, filtered rows or aggregates. Review the actual embedded payload before sharing: hiding a row or panel is not removing its data. Avoid private values, credentials or sensitive selections in public URLs. Shareable state is useful only within that privacy boundary.

Shareables is a delivery provider, not a second data renderer. If publishing is authorized, discover its current tools/workflow, inspect the requested destination and its source/privacy requirements, publish through that owner and verify the actual public URL and artifact. A locally generated HTML file, upload request or successful build is not a verified publication. Otherwise stop at the requested local artifact.

## Acceptance cases

### Reader-comprehension acceptance

Review the rendered default view and expanded detail with the intended audience. A scientific or academic audience may justify technical vocabulary upfront; it does not waive meaning or honesty. The following cases apply to one-chart product surfaces as well as dashboards. Map relevant checks to the existing visual anchors; no new artifact or test harness is required.

| Check | Passing evidence | Failure that blocks signoff |
| --- | --- | --- |
| At-glance meaning | Every upfront view has a distinct reader question and an answer visible without methods; lay readers see accurate everyday labels | Two views repeat the same dimension, or understanding depends on raw IDs, coefficients, ordinal terminology, MATTR or opaque decimals |
| Scale ends and middle | Meaningful ends and middle, units, numeric values/ranges and direction are explained; trait-specific labels such as Casual / Neutral / Formal fit the actual measure | Low / Medium / High implies high is good, or an unsupported midpoint is called neutral |
| Span meaning | Observed spread, uncertainty, predicted range and recommended target are visibly distinguished with correct values; unknown thresholds stay unknown | A recommended 40–60 target is labeled the observed spread when observations are 22–74 |
| Compact reading path | Familiar incumbent composition supports comparison; ordinary web reading text is at least 16px; a clearly named details button reveals secondary evidence and methods | Tiny primary labels, a sprawling replacement layout without task need, or blanket accordions hide essential meaning |
| Honest simplification | Everyday labels, rounding and plain-language uncertainty preserve the construct, source values, missingness and limitations; exact methods remain reachable | Simplification changes the measured construct or turns estimates, synthetic examples or targets into observations |
| Validity claims | Relevant empirical evidence supports the claimed construct and use, with limitations stated plainly | Agreement among models or reviewers is called empirical validation, proven comprehension or measured workload reduction |
| Details and access | Keyboard, touch and non-hover paths reveal the same values and scale explanation; return to the primary view works | Methods are the only place to understand the main answer, or disclosure is inaccessible |

For a 0–100 style scale with declared 0–33, 34–66 and 67–100 bands, show the accurate trait labels and numeric mapping. Describe them as declared bands unless evidence establishes something stronger. A design walkthrough can support a reviewer judgment; participant comprehension, cognitive effort and empirical validity remain unmeasured without the appropriate observed evidence. Recheck changed rendered anchors before a pass.

Use only cases relevant to the change; extend existing tests instead of building a second harness.

| Layer | Deliberate check | Failure that blocks a pass |
| --- | --- | --- |
| Data | Known totals, pooled rates, rounding, deduplication, zero denominator, incomplete period | Displayed values have a different population or definition |
| Meaning | Interrupted series, negative values, peer comparison, observed versus forecast | Gaps bridged, truncated magnitude bars, invented priority or certainty |
| State | Filter, clear/reset, selection, theme, permitted chart alternative, save/reload | Totals, titles, table, annotations or export describe different state |
| Render | Desktop/narrow viewport; long labels, dense/empty/error/stale states, zoom | Clipping, overlap, unreadable type or lost comparison |
| Access | Keyboard/focus, touch/non-hover values, text/table equivalent, contrast, reduced motion | Essential evidence or control is unavailable through the intended access path |
| Delivery | Open final output, inspect exported data scope and visible context | Hidden sensitive data, missing assets or caveats |
| Network | Fresh context/cache; deny external traffic while exercising render, customization and export | An undeclared external dependency or upload |

When using browser request interception, account for service workers and state exactly what was blocked. A browser-level test is not an OS/process network isolation guarantee; use an actual environment boundary before claiming that stronger property. Never download test browsers automatically to satisfy this check without the acquisition review.

Record visual anchors before judgments. Separate data correctness, interaction results, rendered craft and delivery receipts. No screenshot proves arithmetic, no arithmetic test proves usability, and no packaging check proves a renderer works. For a method comparison, hold data, model/settings, renderer and effort roughly constant, compare one addition at a time and report limits; do not invent benchmark scores.
