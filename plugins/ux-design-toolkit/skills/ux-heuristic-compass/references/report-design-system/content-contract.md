# Report Content Contract

Use the scored audit payload or `report_ready_payload` as source of truth. Do
not reconstruct checklist rows manually.

## Required Content Slots

| Slot | Limit | Rule |
| --- | ---: | --- |
| `plain_language_read` | 520 chars | One or two nontechnical sentences. |
| `before_using_this_interface` | 420 chars | Must start with `Before using this interface,`. |
| `one_recommendation` | 380 chars | One fix or validation action. |
| `top_finding.title` | 120 chars | Short user-visible problem title. |

## Flexible Counts

- Heuristic cards render for any active count, including 9, 10, 11, or 14.
- Optional profile omissions must appear in the audit scope section.
- Checklist rows remain visible even when there are many items.
- Empty optional sections render as a short absence note, not as placeholders.

## Repair Policy

Missing required audit content blocks report generation. Minor optional omissions
may render with warnings. Overlong required content returns repair instructions
instead of letting the host AI improvise HTML.

## Forbidden Copy

Do not use `TBD`, `TODO`, `Lorem ipsum`, bracket placeholders, or human-panel
language unless the payload explicitly supports it.
