# UXHC Report Payload Field Guide

Use this guide when preparing a payload for `validate_ux_report_payload` or `generate_ux_audit_report`.

The safest path is simple: use the `report_ready_payload`, `report_payload_ref.path`, or scored audit payload returned by `quick_scan_ux` or `audit_ux_surface`. Do not build report payloads from scratch unless you are debugging.

The HTML artifact is owned by the UXHC report design harness. If validation
blocks, repair the named payload fields and retry the renderer. Do not create a
standalone handmade HTML or PDF report as a workaround.

## Core Rule

Always use `checklist_ratings` from the audit scorecard or returned report-ready payload.

Do not pass:

- the `report_readiness_contract` object by itself
- `canonical_payload_template`
- a manually invented checklist table
- ratings that use `item_id` instead of `checklist_item_id`
- ratings that use `severity` instead of `rating`

## Required Top-Level Fields

A minimal report-ready payload needs:

| Field | Notes |
| --- | --- |
| `source` | must include `source_id` and non-blocked `status` |
| `platform` | `desktop` or `mobile` |
| `ux_health_snapshot` | must include `display_state: "scored"` |
| `scorecard` | must include scored status, percentages, descriptors, and grades |
| `heuristic_scores` | usually returned by the audit tool |
| `checklist_ratings` | use returned ratings, not hand-built rows |
| `plain_language_read` | 1-2 nontechnical sentences |
| `before_using_this_interface` | must start with `Before using this interface,` |
| `top_finding` | top issue object or no-scored-findings state |
| `one_recommendation` | one concrete fix or validation action |
| `report_readiness_contract` | must be present and have `status: "ready"` |

## Required Checklist Rating Fields

The validator uses these field names:

| Field | Required | Valid example |
| --- | --- | --- |
| `checklist_item_id` | yes | `h01_d_01` |
| `heuristic_id` | yes | `h01` |
| `platform` | yes | `desktop` |
| `rating` | yes | `2` |
| `evidence_refs` | yes unless `evidence_limits` explains the gap | `["screenshot:hero"]` |
| `rationale` | yes | `The primary status after clicking is not visible in the screenshot.` |
| `confidence` | yes | `medium` |

The validator allows missing `evidence_refs` only when the rating includes `evidence_limits`.

## Minimal Valid Test Payload Shape

This is a compact validator smoke shape. Real reports should prefer the payload returned by UXHC audit tools.

```json
{
  "source": {
    "source_id": "sample-source",
    "status": "ready"
  },
  "platform": "desktop",
  "ux_health_snapshot": {
    "display_state": "scored",
    "overall_label": "Sample scored audit"
  },
  "scorecard": {
    "score_status": "scored",
    "core_quality_percentage": 75,
    "core_grade": "B+",
    "core_descriptor": "Good - a few notable issues",
    "overall_quality_percentage": 75,
    "overall_grade": "B+",
    "overall_descriptor": "Good - a few notable issues"
  },
  "heuristic_scores": [
    {
      "heuristic_id": "h01",
      "platform": "desktop",
      "active_item_count": 1,
      "sum_item_scores": 1,
      "average_item_severity": 1,
      "quality_percentage": 75,
      "letter_grade": "B+",
      "descriptor": "Good - a few notable issues"
    }
  ],
  "checklist_ratings": [
    {
      "checklist_item_id": "h01_d_01",
      "heuristic_id": "h01",
      "platform": "desktop",
      "rating": 1,
      "evidence_refs": ["sample-screenshot"],
      "rationale": "The page title is visible, but the current task state could be clearer.",
      "confidence": "medium"
    }
  ],
  "evidence_limits": [],
  "plain_language_read": "The interface is mostly understandable, with one visible status issue to clarify.",
  "before_using_this_interface": "Before using this interface, confirm whether users need status feedback after the primary action.",
  "top_finding": {
    "status": "finding",
    "heuristic_id": "h01",
    "title": "Status feedback could be clearer"
  },
  "one_recommendation": "Add a clearer status confirmation after the primary action.",
  "report_readiness_contract": {
    "status": "ready"
  }
}
```

## Common Blockers And Fixes

| Blocker | Meaning | Fix |
| --- | --- | --- |
| `source.source_id` | no source identifier | use `prepare_ux_source` or carry over the audit source |
| `source.status` | source is missing or blocked | submit a ready source manifest |
| `ux_health_snapshot.display_state` | not scored | run `audit_ux_surface` or `quick_scan_ux` with complete ratings |
| `scorecard.score_status` | scorecard not scored | use the scored audit output |
| `checklist_ratings` | no checklist rows | use returned `scorecard.checklist_ratings` |
| `checklist_ratings[n].checklist_item_id` | wrong field name or missing ID | use `checklist_item_id`, not `item_id` |
| `checklist_ratings[n].rating` | wrong field name or out of range | use `rating` from 0 to 4, not `severity` |
| `checklist_ratings[n].evidence_refs` | no evidence refs | add evidence refs or explicit `evidence_limits` |
| `plain_language_read.max_2_sentences` | too long | shorten to one or two sentences |
| `before_using_this_interface.prefix` | wrong prefix | start exactly with `Before using this interface,` |
| `report_readiness_contract.status` | not ready | use the report-ready payload after validation passes |
| `content_slot_too_long` | a required narrative slot exceeds the report design limit | shorten only that slot and retry validation |
| `placeholder_text` | report copy still contains TODO/TBD/placeholder text | replace with evidence-bound copy or omit the optional section |
| `human_panel_language_without_data` | blended/human-panel wording appears without human-panel data | switch to AI-only audit language |

## Payload Assembly Checklist

1. Start from returned audit payload, `report_ready_payload`, or `payload_path`.
2. Keep `checklist_ratings` intact.
3. Do not rename fields.
4. Do not pass `canonical_payload_template`.
5. Run `validate_ux_report_payload`.
6. Only call `generate_ux_audit_report` after validation returns ready.

If validation blocks, fix the smallest missing-field set and rerun validation before generating artifacts.

If the HTML renderer blocks on static output validation, use
`repair_instructions` from the tool result. The standard HTML must remain one
page, static, linkless, scriptless, and free of external assets.
