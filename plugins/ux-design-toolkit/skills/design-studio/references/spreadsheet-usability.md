# Human-facing workbook design

This is the complete UX-owned workbook method. Use it for a tracker, calculator, model, operational workbook or spreadsheet decision tool that people must operate. It needs no separate spreadsheet-method plugin. Use the actual spreadsheet runtime for data, formulas, formatting, protection, rendering and export; an unavailable runtime limits execution, not access to this method. Raw machine tables and archives do not need a dashboard by default.

## 1. Establish the task and source

Identify who uses the workbook, the recurring action or decision, frequency, device, locale, required output and consequences of a plausible error. Inspect the actual file and a representative populated range. Read sheet names, formulas, validation, hidden rows/sheets, protections, named ranges, comments and links before changing layout. Record file/version, authoritative sources, last refresh, editable ranges and important calculations. Preserve machine-readable tables, identifiers and existing downstream consumers.

Write a compact contract: “A [role] opens [view], changes [inputs], checks [result], and knows [next action].” Define correct completion and a harmful mistake. If inputs are absent, request only what affects the decision; work with clearly labeled fictional fixtures for structural design. Do not populate real billing or financial assumptions from guesses.

## 2. Choose the smallest useful workbook architecture

Keep inputs and their immediate results near one another. A simple tracker may need only a readable table with filters. A decision model may use a Start/Decision view, Inputs, Calculations and Sources, but create separate sheets only when they clarify a recurring task. Give each sheet an action-oriented name and a visible purpose. Include links back to the entry view and to the relevant assumptions; critical guidance must not live only in hidden cells.

For an operational table, keep one header row with unique labels and one record per row; stable IDs support joins, sorting and traceability. Keep decorative merged headings outside the data range. Preserve sort/filter behavior and totals when adding or deleting rows. Avoid duplicated editable values across views. For a model, show the selected scenario next to outputs and identify which input set drives it. Reset should affect only specified user inputs and have recoverable behavior.

## 3. Make input rules visible and safe

Distinguish editable, calculated and source-backed cells using explicit labels, structure and appropriate protection as well as restrained color. Put units, acceptable ranges, formats and examples at the input. Explain whether blank means unknown, zero, not applicable or incomplete. Use defaults only when defensible and make assumptions recognizable. A stored decimal ratio displayed as a percentage needs an input convention people can follow.

Validate required fields, data types, allowed categories, date ranges and incompatible assumptions. Use native lists or constraints when supported, and inspect behavior for pasted values and expanded ranges rather than assuming validation is enforced. Keep errors close to the input and say what to change. Protect formula ranges against accidental edits where the runtime supports it; sheet protection is an editing guard, not confidentiality or authorization. Preserve a recoverable original before a structural change.

Inputs with exceptional consequences need proportionate checks: currency and time units, monthly versus annual values, net versus gross amounts, time zones, start/end order, mutually exclusive scenarios and sensitivity-driving assumptions. Format is not validation. A number that looks like a date or a percentage can still be wrong.

## 4. Give the decision a legible first view

Lead with the actual question, selected period/scenario, essential result and next action. Label units and denominator near each result; use precision that matches the source. Show incomplete, invalid, stale and unavailable distinctly from a valid zero. Keep comparison baselines visible. Arrange related inputs and results in a consistent reading order; use typography and spacing before dense borders. Freeze useful headers and maintain readable row heights, wrapped labels and practical column widths.

A result card must tell the reader what the result means. For a scenario comparison, expose assumptions that can reverse the ranking, uncertainty/ranges, downside and available buffers. Separate materially different regimes and capital needs. A “best” label requires a stated criterion; a model ranking is not domain advice. Keep assumptions reachable without making every calculation a foreground control. Chart design uses [Dashboard Design](../../dashboard-design/SKILL.md); analytical or regulated judgment needs its domain evidence.

## 5. Design errors, recovery and return visits

Show missing required inputs before an apparently authoritative output. Choose a defined response to impossible dates, negative quantities, missing source data, formula errors and conflicting scenarios; do not mask every error with a zero. Keep users' valid work when another field fails. Give a recovery instruction and a route back to the affected input. Treat external-link refresh and calculation mode as operational dependencies.

For repeated work, include a visible last-updated date, period/scenario and status where meaningful. Provide a simple way to find unfinished records, distinguish planned from completed work and resume after interruption. Test adding a record, deleting a record, filtering and sorting, reopening, and handing the file to another operator. In shared workbooks, make status/ownership conventions explicit and check conflict behavior with the runtime; do not promise collaboration or audit history from a static file.

## 6. Preserve accessibility and practical reading

Use meaningful sheet/table names, unique headers and consistent left-to-right or locale-appropriate structure. Avoid meaning conveyed by color alone, unexplained symbols, cropped instructions and decorative blank grids between related controls. Provide text labels for status and chart meaning. Keep focus/navigation practical with keyboard and the receiving application's supported assistive-technology features. A screenshot cannot establish screen-reader reading order.

Inspect the normal desktop view and any actually requested mobile/tablet/print output. A wide calculation sheet may need a separate compact decision view or export; do not silently claim it fits a phone. Test zoom, long labels, large/negative values and meaning in grayscale. PDF export is a separate output with its own page-break, repeated-header and clipping checks. Record which application and viewport were used.

## 7. Keep trust and traceability inspectable

Link a consequential output to its input, formula/calculation range and source or assumption. Record source date/version and distinguish sourced, estimated and user-entered values. Explain transformations, exclusions and rounding that affect interpretation. Keep uncertainty and missing-data limits visible near the decision. Preserve original source tables; a polished human view is not a substitute for provenance.

Example trace: Decision!B8 → Calculations!D12 → Inputs!B4 (hours, user-entered) and Sources!B3 (rate, dated contract). This chain is a review aid; verify actual references in the real file. Data lineage can be read-only while editable inputs stay on the task view.

## Worked example: monthly capacity tracker

A fictional operator enters committed hours for a 120-hour month. The task view has Period, Capacity hours, Committed hours and Remaining hours; source notes identify the capacity assumption. Capacity 120 and committed 75 produce remaining 45. A blank commitment shows “Enter committed hours,” not 120 remaining. A negative commitment is invalid; capacity zero is an explicit unavailable-period case, not a percentage divide-by-zero. At 135 committed hours, the view reports 15 hours over capacity in words alongside the sign/color. A filter on project rows must not alter the whole-month result unless the view explicitly labels it as filtered.

Changed input cells are labeled Editable; the remaining formula is labeled Calculated. The operator can add a project row without breaking the sum, find the current period after reopening and follow the result to the source rows. The workbook provider checks the actual formula, persisted values and file integrity. UX checks the decision, labels and operating paths.

## Acceptance tasks and deliverable

| Task | Required observation | Failure to fix |
| --- | --- | --- |
| First use | New operator finds the correct period/view, inputs and meaningful result | Hidden starting instructions or unknown editable cells |
| Valid entry | Representative inputs produce the expected, labeled result | Broken references or misleading precision |
| Invalid/pasted entry | Bad date/type/range is rejected or clearly flagged without losing valid work | Invalid value silently accepted or shown as a confident zero |
| Structural edit | Add/delete/sort/filter preserve intended totals and IDs | Fixed formula range drops new rows or totals change without explanation |
| Return visit | Reopen and identify scenario, date, unfinished work and next action | Stale/default values mistaken for current work |
| Traceability | Follow a consequential result to formula, input and source | No source or hidden assumption |
| Accessible reading | Keyboard path, labels and meaning without color work in the tested app | Color-only status, cropped label or inaccessible required control |
| Export, if requested | Rendered output preserves legible labels, page breaks and interpretation | Clipped result or missing repeated header |

Deliver the changed workbook or bounded review, entry sheet/ranges, input rules, source/assumption notes and checks with `pass`, `fail`, `not tested` or `unsupported` plus evidence. Separate formula correctness, rendered appearance and interaction checks. Do not infer a live native validation pass from inspecting XML or rendering an image. Report unresolved application limits and the smallest remaining action.

## Exploratory freedom and decision-model profile

Preserve useful spreadsheet agency. People should be able to inspect relevant assumptions and calculations, adjust a scenario safely and understand the consequences; a polished input surface must not silently remove legitimate exploration or conceal how it works. Add validation/protection in proportion to actual risk. Hidden detail is disclosed and recoverable, and a frozen header region must not consume most of a narrow view. In a quick first-view check, a reader should recognize purpose, active case, principal result, current warning and next action without searching technical tabs.

For budgeting, financing or other consequential decision models, make the following explicit in the user-facing specification. This is UX presentation, not a financial/legal methodology:

- Show estimated ranges, sensitivity or the threshold that reverses a conclusion. Identify which values are sourced, assumed or unresolved and their dates. Do not let a favorable central estimate hide an important unresolved variable.
- Distinguish total resource requirement from timing and available buffer. A positive projected return can coexist with a shortfall during implementation; show available liquidity/contingency and downside near the result.
- Keep alternatives with different upfront and recurring resource profiles separate. Preparation/equipment, operating reserve and working capital may need different timing and sources; a single undifferentiated total can conceal the binding constraint.
- If a domain-verified legal/tax/organization regime changes the analysis materially, show it as a visible scenario rather than a hidden formula choice. Route correctness to actual domain evidence; the UX method cannot select the lawful regime.
- Use a status such as viable/review/decline only when the analytical owner supplies its criterion and supports the classification. Put the unresolved assumption and next verification beside that status.

Illustrative fixture: Option A requires 8,000 units upfront, Option B 4,000 upfront plus 6,000 during delivery, and the available buffer is 7,000. Showing only projected benefit would miss A's immediate shortfall and B's later funding requirement. Keep both timing profiles and remaining buffer visible; no investment recommendation follows from this fictional arithmetic. Acceptance follows each displayed figure to its inputs/source, changes the binding assumption and confirms that scenario/status/period remain recognizable after reopening.
