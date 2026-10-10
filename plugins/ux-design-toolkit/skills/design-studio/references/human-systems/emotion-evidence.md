# Human-systems method: adopted conditional research card

Integrated 2026-09-30. Read this complete card only for its trigger. The original evidence, examples, counterexamples, tradeoffs and proposed tests are retained below; historical pre-integration coverage statements remain provenance. Participant outcomes are not measured. Normative criteria apply at their stated level and with their exceptions, not as universal design formulas. Source IDs resolve in the linked ledger; user/course proposals remain attributed and unvalidated. Locators such as L27 and U09 identify audited sources, not mandatory private-file dependencies.

## HS-07 — Emotion evidence discipline (PCEA, attributed)

- **Owner:** UXHC (H12 evidence), `design-review`, research inputs. Overlaps: `ux-oracle/SKILL.md` line 68 (confidence labels; preserve), critique "emotional journey".
- **Trigger:** any statement about how a person feels ("anxious", "frustrated", "reassured", "delighted"), any emotional-journey graph, or any PCEA worksheet.
- **User task:** varies. The reviewer's task is to separate evidence from interpretation.
- **Evidence:** X08 (systematic review): facial movements aren't reliable, specific indicators of particular emotions across contexts. X06: an established instrument collects frustration by self-report. Kyle's sources: U15 [0007]–[0012] (PCEA proposal), U06 [0027] ("overt emotional reactions… captured through usability testing"), U08 [0015]–[0016] (emotion colors memory), U14 [0027] (anxiety and safety). Community lead C01 is a counterexample.
- **Mechanism:** emotional inference from appearance or pixels is unreliable. False emotion claims then justify design changes no one needed, or persuasive "fixes".
- **Decision rule:** record every emotion claim as exactly one of:
  - **Observed behavior** (e.g., "paused 20 s, reopened filter panel twice, said 'where did it go?'"), with the *interpretation* in a separate field.
  - **Self-report** (a verbatim quote, a rating, a post-task answer).
  - **Reviewer inference**, stated as a hypothesis with at least one alternative explanation and a test.

  A screenshot can support only reviewer inference. Emotion findings become design *questions* ("Is the deletion step anxiety-producing?") unless there is observed or self-reported evidence.
- **When not to use:** don't force emotion rows onto trivial tasks; leave the column empty rather than inventing content.
- **Competing considerations:** Kyle's valid point that usability-only reviews miss affect (U11 [0005]–[0007]); the risk of over-psychologizing; privacy of emotional data.
- **Example:** see `examples/pcea-task-worksheet.md`.
- **Counterexample:** "Users feel overwhelmed by this dashboard (frowning detected in session video)". Emotion is inferred from facial movement, generalized to all users, and presented as a finding.
- **Accessibility and ethics:** don't use emotion inferences to target persuasion. Treat emotional data as sensitive. Cultural and neurodivergent differences in expression make appearance-based inference even less reliable (consistent with X08's context point).
- **Evaluation (not run):** a claim audit over N AI-generated critiques, before and after the rule. Count emotion claims without a stated evidence type, and claims presented as findings from screenshots. Failure condition: emotion content disappears entirely, meaning the rule suppressed useful hypotheses, or unsupported claims persist.
- **Effort:** small.

## Installed support

[Source ledger](../../assets/human-systems/sources.json), [complete evaluation tasks](../../assets/human-systems/evaluation.md), [limits and unresolved terminology](../../assets/human-systems/unresolved.md). [Comparison case](../../assets/human-systems/examples/case-1-dashboard-comparison.md), [interrupted-work case](../../assets/human-systems/examples/case-2-interrupted-work-recovery.md), [neutral-research case](../../assets/human-systems/examples/case-3-neutral-survey-vs-persuasion.md), [optional PCEA worksheet](../../assets/human-systems/examples/pcea-task-worksheet.md).

The existing [consequence-copy method](../ux-writing.md), [risk/recovery matrix](../../../../libraries/frontend-design-premium/skills/frontend-design-premium/references/decision-matrix.md), and [current accessibility checks](../verification.md) remain their respective authorities. Resolve former audit paths through this plugin and its preserved libraries; do not infer participant results from these examples.
