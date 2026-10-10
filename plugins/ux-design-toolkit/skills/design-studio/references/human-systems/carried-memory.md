# Human-systems method: adopted conditional research card

Integrated 2026-09-30. Read this complete card only for its trigger. The original evidence, examples, counterexamples, tradeoffs and proposed tests are retained below; historical pre-integration coverage statements remain provenance. Participant outcomes are not measured. Normative criteria apply at their stated level and with their exceptions, not as universal design formulas. Source IDs resolve in the linked ledger; user/course proposals remain attributed and unvalidated. Locators such as L27 and U09 identify audited sources, not mandatory private-file dependencies.

## HS-02 — Memory carried across a gap (recognition over recall; put it back in the world)

- **Owner:** `design-review` (local override of the Impeccable working-memory rule), `dashboard-design` via the lane01 contract. Overlaps: UXHC H6, critique.md's "Memory Bridge" and "Context Switch" violations, which are good and should be preserved.
- **Trigger:** someone must remember a value, selection, rule or location from a different screen, scroll position, tab, earlier step, or from before an interruption, in order to act or compare. Typical signs: comparing two items shown on separate pages, re-typing a code seen earlier, filter state visible only inside a closed panel, a legend far from the chart.
- **User task:** decide or compare while keeping several pieces of information available.
- **Evidence:** X05 (empirical review): roughly 3–5 chunks can be held in mind when rehearsal and grouping are prevented; this is about information *held*, not information *visible*. X12 #6 (practitioner): make options visible to minimize memory load. X11 p. 88 (theory with experiments): representation choice changes cognitive behavior. X07 p. 40: pending goals need cues. Kyle's sources: U08 [0012]–[0013] (attention), U09 [0021] (clear labels, less clutter) and [0023]–[0024] (mental models).
- **Mechanism:** visible information can reduce the need to retain items across a gap, but reading, integrating and choosing still demand attention and memory. Information that must be carried creates additional retention demands. Grouping ("chunking") only helps once the grouping is meaningful to the person.
- **Decision rule:**
  1. Count **carried items**: what must be remembered across a gap to finish the task. Don't count visible options.
  2. Reduce carried items by co-locating the things compared, echoing the current selection and scope next to results, using direct labels instead of distant legends, and keeping units and scale identical across compared items.
  3. Group visible options by the person's task vocabulary, not by system structure. Long visible lists are acceptable when they are scannable, ordered meaningfully and searchable.
  4. Hide options (progressive disclosure) only when they are genuinely rare. Hiding a frequent option turns recognition into recall.
- **When not to use:** high-frequency expert workflows, where a memorized keyboard command beats a visible menu. Offer both, as Nielsen #7 suggests via UXHC H7.
- **Competing considerations:** co-location costs space; direct labels can clutter small charts; echoing state adds text. Balance these with HS-06.
- **Example:** to compare sessions S04 and S09, the "before" design has the user open each detail page in turn. The "after" design pins both to a side-by-side comparison tray with the same axes, the units shown, and the active week range echoed above the tray. Carried items drop from about four (two values, two denominators) to zero.
- **Counterexample:** "No more than four options at any decision point" applied to a 12-session list. The list is collapsed behind a "More" menu, and the coordinator must now recall which sessions exist. That is the opposite of the intended effect.
- **Accessibility and ethics:** carried memory is a larger barrier for people with some cognitive disabilities, for people under stress, and for people who get interrupted. Visible state also helps screen-reader users when it is exposed programmatically (WCAG 4.1.3 for status changes, X03).
- **Evaluation (not run):** a carried-item count before and after, done by walkthrough (inspection evidence). Then a comparison task with real participants measuring accuracy of the comparison and the number of back-and-forth navigations. Failure condition: accuracy doesn't improve, or the comparison tray hides information needed elsewhere.
- **Effort:** small (review rule); medium (design pattern).

## Installed support

[Source ledger](../../assets/human-systems/sources.json), [complete evaluation tasks](../../assets/human-systems/evaluation.md), [limits and unresolved terminology](../../assets/human-systems/unresolved.md). [Comparison case](../../assets/human-systems/examples/case-1-dashboard-comparison.md), [interrupted-work case](../../assets/human-systems/examples/case-2-interrupted-work-recovery.md), [neutral-research case](../../assets/human-systems/examples/case-3-neutral-survey-vs-persuasion.md), [optional PCEA worksheet](../../assets/human-systems/examples/pcea-task-worksheet.md).

The existing [consequence-copy method](../ux-writing.md), [risk/recovery matrix](../../../../libraries/frontend-design-premium/skills/frontend-design-premium/references/decision-matrix.md), and [current accessibility checks](../verification.md) remain their respective authorities. Resolve former audit paths through this plugin and its preserved libraries; do not infer participant results from these examples.
