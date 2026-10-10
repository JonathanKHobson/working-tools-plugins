# Human-systems method: adopted conditional research card

Integrated 2026-09-30. Read this complete card only for its trigger. The original evidence, examples, counterexamples, tradeoffs and proposed tests are retained below; historical pre-integration coverage statements remain provenance. Participant outcomes are not measured. Normative criteria apply at their stated level and with their exceptions, not as universal design formulas. Source IDs resolve in the linked ledger; user/course proposals remain attributed and unvalidated. Locators such as L27 and U09 identify audited sources, not mandatory private-file dependencies.

## Kyle Hobson's three proposed heuristics — operational observations

**Attribution:** proposed by Kyle Hobson in the HSE 521 heuristic-evaluation reflection (U14 [0022]–[0033]), "inspired by Jakob Nielsen's seminal work". They aren't official Nielsen heuristics (X12 lists ten) and haven't been independently validated. They already exist in UXHC as optional profiles H11–H13 (L05 lines 46–48), and their checklist item text lives in the UXHC MCP, which wasn't inspected. The proposal below adds *observation prompts* to that installed structure. It doesn't add new heuristics or scores.

### H11 — Accessibility & Ease of Access (Kyle's proposal)
- **Kyle's definition:** accommodating all users including those with disabilities; adopting universal design principles "like those articulated in the WCAG" (U14 [0025]).
- **Observable prompts:** Can every core action be completed by keyboard, with focus visible and not obscured (2.4.11)? Do pointer targets meet 2.5.8 or its spacing exception? Does dragging have an alternative (2.5.7)? Is meaning carried by more than color (1.4.1)? Are status changes announced (4.1.3)? Does content reflow at 320 CSS px (see L13 line 17)? Does authentication avoid cognitive tests without alternatives (3.3.8)? "Ease of access" also covers **situational** constraints: one-handed use, glare, low bandwidth, interruption (HS-04).
- **What doesn't count:** "looks accessible" from a screenshot; an automated scan alone. Severity 3–4 findings hand off to a real accessibility review, as L05 line 46 already says.
- **Test:** T-HEUR in `evaluation.md`.

### H12 — Empathetic Engagement and Inclusion (Kyle's proposal)
- **Kyle's definition:** nurturing an emotional connection; designs "that mitigate anxiety and convey a sense of safety"; welcoming users "from all walks of life" (U14 [0027], [0031]).
- **Observable prompts:** At high-stakes steps (payment, deletion, submission, personal data), does the interface say what will happen, what won't happen, and how to undo or get help (HS-03, HS-05)? Are error messages blame-free and specific (H9)? Do forms assume a particular identity, family structure, name format, locale or resource level? Is tone steady across normal and error states? Are there anxiety *points*, located by consequence and uncertainty rather than by guessing feelings (HS-07)?
- **What doesn't count:** decorative warmth (illustrations, exclamation marks) without consequence clarity; emotional claims without an evidence type; engagement mechanics that exploit emotion. Kyle's own ethics passages (U07 [0011]) rule this out.
- **Test:** T-HEUR, T-EMO.

### H13 — Customer Journey and Satisfaction (Kyle's proposal)
- **Kyle's definition:** the whole span "from initial engagement through to long-term satisfaction", including consistency of brand values, navigation, personalized content and support (U14 [0029]).
- **Observable prompts:** Does the screen tell people where they came from and what comes next? Do handoffs (email → app, app → support, device → device) preserve context (HS-04)? Is the end state explicit — done, pending or failed — with a receipt? Do small frictions *compound* across repeated or multi-step use (already in L08's calibration)? Is there a path back after completion (edit, cancel, get help)?
- **What doesn't count:** "satisfaction" asserted without self-report or behavioral evidence; journey claims from a single screen. L07 already requires multi-page scope for H13.
- **Test:** T-HEUR.

## Installed support

[Source ledger](../../assets/human-systems/sources.json), [complete evaluation tasks](../../assets/human-systems/evaluation.md), [limits and unresolved terminology](../../assets/human-systems/unresolved.md). [Comparison case](../../assets/human-systems/examples/case-1-dashboard-comparison.md), [interrupted-work case](../../assets/human-systems/examples/case-2-interrupted-work-recovery.md), [neutral-research case](../../assets/human-systems/examples/case-3-neutral-survey-vs-persuasion.md), [optional PCEA worksheet](../../assets/human-systems/examples/pcea-task-worksheet.md).

The existing [consequence-copy method](../ux-writing.md), [risk/recovery matrix](../../../../libraries/frontend-design-premium/skills/frontend-design-premium/references/decision-matrix.md), and [current accessibility checks](../verification.md) remain their respective authorities. Resolve former audit paths through this plugin and its preserved libraries; do not infer participant results from these examples.
