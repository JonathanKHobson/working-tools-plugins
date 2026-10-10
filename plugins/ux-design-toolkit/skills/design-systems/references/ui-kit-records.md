# Editable records for a UI-kit project

Copy only records the current scope needs. These are field contracts, not working APIs or a mandated folder layout. Fill unsupported or unknown fields honestly; do not leave a placeholder that looks production-ready.

## Decision and source intake

| Field | Record |
| --- | --- |
| Decision ID / owner / date | Stable identity and accountable owner |
| Question and adopted rule | Concrete behavior or value, with units |
| Basis | User instruction, adopted project decision, formal criterion, platform guidance, research proposal or observation |
| Source identity | Path/URL, version/date and hash or immutable revision where available |
| Alternatives and rationale | Why this fits the actual task |
| Affected consumers | Components, tokens, content, art and examples |
| Status / recheck trigger | Proposed/adopted/superseded; what would change the decision |
| Validation / limitations | Observed checks and remaining uncertainty |

## Component record

```yaml
id: component-stable-id
name: Human-readable component name
owner: accountable-owner
implementation_status: specified  # proposed / specified / implemented / adopted / deprecated
purpose: task and user need
actual_source: []                # real paths and exports/selectors; empty if not implemented
design_source: null              # real node/version, or unavailable
dependencies: []
anatomy: []
axes: {}                        # intent, emphasis, size, theme, density, orientation
valid_combinations: []
state_precedence: []
measurements: {}                 # units, min/preferred/max, padding/gaps, focus, growth
token_bindings: {}               # actual token to actual consumer/property
content_rules: []
transitions: []                  # trigger, result, authority, focus, cancellation, clearing
input_and_semantics: {}
adaptation: {}
examples: []                     # real usage, difficult state, isolation/multiple instances
verification_refs: []            # no verified claim until applicable evidence passes
acceptance_refs: []              # human decision and exact scope
limitations: []
```

## Asset record

```yaml
id: asset-stable-id
role: illustration              # identity / icon / frame / texture / social / other
status: candidate               # accepted-persisted / rejected-disposable as applicable
path: project-owned-relative-path
width: null
height: null
sha256: null
source_rights: null
source_or_prompt_ref: null
parent_master_sha256: null       # derivatives only
transform: null                  # tool/version, crop, resampling, encoding, color, alpha
bytes: null
protected_regions: []           # normalized coordinates tied to intrinsic source
use_sites: []
acceptance_scope: null
```

## Verification record

```yaml
id: evidence-run-id
disposition: not-run            # current-pass / current-fail / stale / invalid-evidence / not-run
executed_at: null
environment: {}                 # OS, browser/runtime/version, viewport, DPR, input, theme
method: null                    # actual method; distinguish simulation/manual/device
source_dependencies: []         # path + SHA-256
test_dependencies: []           # test/config/fixture path + SHA-256
assertions: []                  # stable ID, component/flow/state, expected, observed, result
execution_errors: []
artifacts: []                   # screenshots/logs, path + hash where persisted
limitations: []
```

An empty record cannot verify anything. The consumer of this schema must apply the freshness and applicability rules in [verification](ui-kit-verification.md); copying fields is not an implemented validator.

## Release and acceptance table

| Item / stable ID | Specified | Implemented | Current scoped verification | Human acceptance | Delivery state | Open gate |
| --- | --- | --- | --- | --- | --- | --- |
| Actual component or composition | Contract/version | Source/version or absent | Named assertions + environment, or untested | Who/what/viewport/date, or pending | Local/packaged/installed/published | Specific next check and owner |

## Stress matrix

| Consumer / scenario | Risk | Source/fixture | Input, width, content, state | Expected result | Method and observation | Status / evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Fill from real workflow | Why it matters | Actual path | Test conditions | Observable behavior | Actual run, not intended check | Pass/fail/untested with reference |
