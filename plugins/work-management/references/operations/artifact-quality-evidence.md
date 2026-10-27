# Scoped artifact quality evidence

The existing `scripts/codex_artifact_quality_gate.py` records review obligations. For a visual completion mark, it now validates a structured JSON receipt with file fingerprints, affected regions/states, descendant text contrast and four explicit review categories. A screenshot, link check or outer-container color sample alone does not clear a visual obligation.

## Before declaring completion

1. Identify the current source/delivered version and affected visible regions. Inventory meaningful states, including desktop/narrow and light/dark where the artifact supports them. Exclude only specific irrelevant states with a reason. Include nested content, repeated cards, badges, expanded content and controls affected by inherited styles.
2. Capture the actual rendered states. For web text, enumerate **visible elements with their own nonblank text nodes**, including descendants, rather than sampling only cards/headings. Read computed text color, font size/weight and the effective composited background behind each. Resolve transparent ancestors. Gradients, images, filters or unknown compositing need a suitable measurement method; unsupported measurements remain unresolved. Save the measurement export alongside screenshots. Source inspection can locate the cause but cannot replace rendered checks.
3. Record observed accessibility checks (contrast plus task-relevant keyboard/focus/name/state checks), usability checks (task sequence, comprehension and feedback), QA/auditing (regression tests, errors, affected behavior and artifact closure), and aesthetics (hierarchy, typography, spacing, consistent identity and legibility). Check action gaps, wrapping and separation as well as colors. Keep reviewer inspection separate from participant research; automated contrast alone is not WCAG certification. Include method, observed outcome and limits in each category's evidence.
4. Fix applicable failures and re-run the affected checks. Capture final source/render/measurement file SHA-256 fingerprints. Mark only after all applicable categories pass. Changed source, rendered files or the report invalidate existing marks. If the actual remote artifact changes, refresh the local version capture and recheck it; this local validator cannot monitor a remote deployment.
5. Run `verify --json` under the same native session identity immediately before a completion claim or `update_goal(status="complete")`. Nonzero means unresolved or unassessed. Correctly reasoned nonvisual work can use `skip <check> --reason ...`; a failed or unrun applicable test is never a reason to skip. Marking a review does not authorize sending, deployment or publication.

This engine validates the receipt's structure, recorded coverage, local freshness and opaque sRGB text contrast. The reviewer remains responsible for truthful observations and a complete scoped inventory. It does not execute a browser, establish human approval, certify full accessibility or prove participant usability. Nonvisual/configuration work needs no artificial visual receipt.

## Receipt format (schema version 1)

All paths are absolute receiving-host paths. `files` must include at least one source and one actual rendered capture. Add measurements using role `measurement`. Hash each file's bytes with SHA-256. This illustrative structure omits real paths/hashes and is not passing evidence:

```json
{
  "schema_version": 1,
  "artifact_kind": "interface",
  "files": [
    {"path": "/project/page.html", "sha256": "<actual sha256>", "role": "source"},
    {"path": "/project/desktop.png", "sha256": "<actual sha256>", "role": "render"}
  ],
  "scope": {
    "regions": ["nested-example"],
    "states": ["desktop-light", "narrow-light"],
    "responsive": {"applicable": true, "reason": "Responsive interface", "states": ["desktop-light", "narrow-light"]},
    "themes": {"applicable": false, "reason": "Only a light theme is supported"},
    "exclusions": []
  },
  "coverage": [
    {"region": "nested-example", "state": "desktop-light", "render": "/project/desktop.png", "text_targets": [".example p", ".example .badge"]}
  ],
  "contrast": [
    {"region": "nested-example", "state": "desktop-light", "target": ".example p", "foreground": "#222222", "background": "#ffffff", "font_size_px": 16, "font_weight": 400}
  ],
  "checks": {
    "accessibility": {"status": "pass", "evidence": "<observed contrast and applicable keyboard/focus/name checks>", "limitations": "<untested accessibility dimensions>"},
    "usability": {"status": "pass", "evidence": "<observed task sequence and feedback>", "limitations": "Reviewer inspection, not participant testing"},
    "qa": {"status": "pass", "evidence": "<executed affected regression and audit checks>"},
    "aesthetics": {"status": "pass", "evidence": "<rendered hierarchy/type/spacing/identity/legibility observations>"}
  },
  "blockers": []
}
```

Supply coverage for every region/state pair and a measured contrast sample for every inventoried `text_targets` entry. Distinguish repeated nodes with stable IDs or indexed selectors. An exclusion such as `{"scope":"region@state","reason":"Component absent in this state"}` removes only that pair. Regions without text use `no_text_reason` instead of text targets. For interfaces, `responsive` and `themes` require applicability and a reason; applicable dimensions list at least two states from the inventory. This is an explicit scope decision, not automatic detection of all possible states.

The supported kinds are `interface`, `document` and `graphic`. For a document/graphic an inapplicable non-aesthetic category may use `{"status":"not_applicable","reason":"..."}`. Interface categories must all pass. Unknown/pending/failed/not-run statuses do not pass. Text thresholds are 4.5:1 normally or 3:1 for large text at least 24 CSS px, or at least 18.667 CSS px with weight at least 700. These limited checks do not cover every accessibility criterion.

```sh
python3 scripts/codex_artifact_quality_gate.py mark visual_qa --reviewer '<actual reviewer>' --evidence /project/review.json
python3 scripts/codex_artifact_quality_gate.py mark design_taste --reviewer '<actual reviewer>' --evidence /project/review.json
python3 scripts/codex_artifact_quality_gate.py verify --json
```

`detect` retains unresolved scoped obligations through follow-up prompts. `status` revalidates recorded evidence and exposes reasons; `verify` additionally returns nonzero for no scoped assessment. Historical visual marks without structured receipts must be reviewed again, or explicitly ruled inapplicable to the current scope.

For outgoing communication, save the **exact final local text** (for example, the final email body in a UTF-8 `.txt` file) and run `writing-quality-studio:natural-prose-editor` on those bytes. After the review, mark with its absolute path and concise, specific review evidence. The mark records a SHA-256 fingerprint and becomes pending if the file changes or disappears. Re-review after any personalization or composer edit, save the revised final text and mark again. A legacy free-text-only `done` mark is retained in history but remains unverified.

```sh
python3 scripts/codex_artifact_quality_gate.py mark communication_review \
  --artifact /project/final-email.txt \
  --reviewer writing-quality-studio:natural-prose-editor \
  --evidence 'Reviewed final wording, tone and requested action; no changes after review'
python3 scripts/codex_artifact_quality_gate.py verify --json
```

Successful new communication attestations optionally call the configured usage recorder with `kind=editorial_review`, `plugin=writing-quality-studio`, `operation=natural-prose-editor`, `status=success`, and an event ID derived from scope, artifact hash and review-evidence hash. The callback carries no draft text, evidence text or artifact path. An unchanged repeated mark emits no new callback; disabled or unavailable tracking does not affect the gate result. The local mark proves which bytes were reviewed, while the reviewer remains responsible for the accuracy of the review evidence.

## Portable project receipts

The same recorder works outside Codex. Resolve this plugin’s installed folder and pass `--state-path` to keep review evidence with the project. Use the same working directory for marking and verification when the host supplies no session identity. No private hook, account configuration or usage service is required. Optional host tracking remains a separate integration.

```sh
python3 /installed/work-management/scripts/codex_artifact_quality_gate.py mark communication_review \
  --state-path /project/review-state.json \
  --artifact /project/final-copy.html \
  --reviewer writing-quality-studio:natural-prose-editor \
  --evidence 'Reviewed final visible copy against the brief; removed redundant explanations'
python3 /installed/work-management/scripts/codex_artifact_quality_gate.py verify \
  --state-path /project/review-state.json --json
```

Replace the example paths and evidence with the actual artifact and observed review. Verification checks receipt freshness; it does not perform the wording review. A host with no command execution can still apply the Humanizer but must report that recording was unavailable.

## Host boundary and maintenance

The generic closeout adapter delegates only to an explicitly configured host helper. Where a host's existing Stop helper reads this engine and blocks `pending`, failed/stale receipts use that existing behavior. Confirm its actual import path and run a scoped synthetic negative/positive integration before claiming enforcement. Stop re-entry handling may permit a blocked turn to end, so this is not an absolute completion lock. Neither this engine nor the shipped hook declaration intercepts native `update_goal`; the check-before-goal rule above is an agent lifecycle requirement. Do not claim native runtime enforcement without a supported, verified host interceptor.

Do not edit a plugin cache directly. Validate canonical source, install using the host plugin manager, compare changed canonical/cache bytes and verify discovery/trust plus the actual hook import target. A host shim may already resolve canonical source independently of cached skill files. Preserve host registrations and other chats' state. Run `python3 -B -m unittest discover -s tests -p 'test_artifact_quality_gate.py' -v` and the engine's `--self-test`.
