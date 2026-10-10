# Evaluation — what was run and what was not

## Part 1 — Actually performed in this session

These are document and source checks only. No skill was executed, no prototype was built, and no participants were involved.

| Check | What was done | Result |
|---|---|---|
| Primary-source verification | Rendered and read PDF pages directly: X01 pp. 751–756, X06 pp. 1–3, X07 pp. 39–40, X09 pp. 263–265, X10 PDF pp. 1–4, X11 pp. 87–88 | Claims in `sources.json` are limited to the pages read |
| Summarizer screening | Three WebFetch summaries were rejected: a vague X01 summary, an X06 summary that echoed the request as a "quote", and an X07 summary with an unverifiable quote. The PDFs were read instead. The WCAG 2.5.8 summary was garbled and replaced by X04 | Documented in the `sources.json` ledger notes |
| Sources not fully accessed | X02 (Fitts 1954): 404 and an unrendered PsycNet page. X08: summary page only. X05, X03, X12: summarizer only | Marked `access_extent` accordingly |
| Local coverage audit | Claude read 25 plugin files (L01–L25) and ran targeted term greps; Codex then checked L26–L27, germane-load guidance and UXHC H7 | Term absence did not establish capability absence: L26 states consequences before confirmation; L27 has the risk matrix; L16 supports germane effort; H7 names time pressure. See corrected O4/O6/O7. |
| Edit-anchor check | Every anchor quoted in `proposed/existing-skill-edits.md` was copied from the file as read, and its line number checked | Anchors matched at time of reading; Codex must re-check before applying |
| Atlas audit | Read `shared/atlas-retrieval.json` (queries, UX-relevant entries, quality flags) | Keyword-only, semantic retrieval unavailable, no supporting records (O10) |
| Repository inspection | R01: repository page, `package.json` verbatim, cognitive-walkthrough `SKILL.md` via summarizer. R02: `SKILL.md` via summarizer. Nothing installed or executed | Dispositions recorded in `sources.json` |
| Community lead | One bounded search (C01) | No Reddit threads returned; vendor claims recorded as a counterexample |

**Completion checks:** Codex parsed `sources.json` and `capability-map.csv`, checked packet-local links, and resolved the staged reference links against their proposed installed location. The fenced edit snippets contain links relative to future target files and were not treated as packet links. No skill execution, participant task or live integration was performed.

## Part 2 — Proposed tests (all **not_run**)

Use the same brief and the same inputs for baseline and upgraded runs, following `shared/benchmark-brief.md` and the research contract. The **baseline** is the currently installed skills with no packet material loaded, including L26 consequence copy, L27 confirmation strength, L16 germane effort and UXHC H7 time pressure. The **upgraded** run has the staged reference and edits applied in a scratch copy, never the live plugin. Record the model and configuration. Run each prompt at least three times, because output varies between generations. The graders are Kyle or a reviewer Kyle designates. Model self-grading may be used as a screening pass, but it must be labelled as such.

### T-VAR — Conditional variety versus fixed thresholds (hypothesis H-a, H-c)
- **Input:** the case 1 "before" design description and facts, given verbatim to `design-review`.
- **Measure:**
  - (a) the number of recommendations that apply a fixed threshold outside its conditions — option caps, 44 px misrepresented as a WCAG AA minimum, Fitts' law used for salience, count-based severity;
  - (b) whether a carried-item diagnosis is present;
  - (c) the number of distinct interaction mechanisms recommended, each tied to a stated condition;
  - (d) whether each finding states its evidence type.
- **Pass:** the upgraded run reduces (a) to zero across runs, includes (b), and ties every mechanism in (c) to a condition, with no loss of the baseline's valid findings (unlabeled donut, unprotected delete).
- **Failure condition:** the upgraded run drops valid baseline findings, or its "variety" is mechanisms listed without conditions.

### T-MEM — Carried items
- **Input:** case 1 T2 comparison flow.
- **Pass:** the output lists carried items before and after, and the recommended fix reduces them without hiding frequently used options.
- **Failure:** it recommends collapsing the 12-session list.

### T-TGT — Target-size authority
- **Input:** "Review these row icons: 16 px icons, 4 px apart, edit next to delete" through both `responsive-design` and `design-review`.
- **Pass:** cites the WCAG 2.2 AA floor with the spacing exception, presents 44 as an enhanced option chosen for the audience, and separates delete from edit.
- **Failure:** states "44 px is the WCAG AA minimum". A deliberate 44px design target may be appropriate.

### T-FITTS — Scope
- **Input:** two prompts: a landing-page CTA, and a repeated table-row stepper.
- **Pass:** Fitts' law is used only for the stepper, and the output asks for time and errors to be measured separately.

### T-FF — Existing consequence guidance routed into the task
- **Input:** the case 1 scenario slider.
- **Pass:** the recommendation includes a consequence preview, a scenario marker, restore, and announced status, with no confirmation modal.

### T-INT — Resumption
- **Input:** case 2 facts through `interaction-resilience`.
- **Pass:** includes a resumption cue with continue, review and discard; separates scenario from source; addresses timeout warning and re-authentication return; and names the shared-device exception.
- **Failure:** "preserve state" alone.

### T-ERR — Existing matrix applied to the task
- **Input:** an inventory of six actions: filter change, archive row, delete shared dataset, apply scenario to source, export, send report.
- **Pass:** each action is mapped to prevent, confirm or undo consistently with L27's confirmation-strength matrix, and no frequent reversible action gets a modal.

### T-WL — Workload
- **Input:** "Simplify this monitoring dashboard" with its scope and last-updated line present.
- **Pass:** keeps ambient scope and freshness, names the workload dimension, and labels any workload statement as a hypothesis.

### T-EMO — Emotion claim audit (hypothesis H-b)
- **Input:** three screenshot-only review prompts (tool-dependent; use descriptions if images aren't available).
- **Measure:** emotion claims without an evidence type; emotion claims presented as findings.
- **Pass:** zero unsupported claims presented as findings, while inferred emotional hypotheses are still raised as questions.
- **Failure:** emotion content disappears entirely (over-suppression) or unsupported claims persist.

### T-PCEA — Worksheet usefulness (Kyle review)
- **Input:** Kyle fills the worksheet for one real task he knows well.
- **Measure:** Kyle's judgment of whether the split emotion columns preserve his intent and whether any column is noise.
- **Output:** a keep/revise decision on the column set. Expert review is not user validation.

### T-HEUR — H11–H13 attribution and prompts
- **Input:** a UXHC standalone expanded-profile audit of the case 1 description.
- **Pass:** the report names H11–H13 as optional profiles originating from Kyle's proposed extensions; H12 findings use consequence and uncertainty evidence, not emotional guesses; checklist counts are unchanged (still 204 at full coverage).

### T-SURV — Neutral boundary
- **Input:** the case 3 merged instrument.
- **Pass:** routes it to Survey Studio, flags leading, double-barrelled and presupposing items, and removes the promotion from the instrument.
- **Failure:** optimizes completion or share rate.

### T-DASH — Contract uptake (joint with lane01)
- **Input:** lane01's prototypes.
- **Pass:** each of the ten contract requirements is checked, with its actual evidence or "not run".

### Regression checks (must stay unchanged)
- `design-review` still delivers findings without editing on review-only requests (L02 workflow step 3).
- The `interaction-resilience` example boundary still contains "retain an unsent form after a retryable failure".
- `verification.md` stays unchanged and remains the target-size authority.
- UXHC checklist counts, severity scale and MCP contract are unchanged.
- Impeccable runtime files are byte-identical; compare with `plugin-file-hashes.json`.

## Part 3 — Honest limits

- No claim in this packet says users will perform better. The cards are decision rules with cited evidence and stated inferences.
- The worked cases are synthetic. The "baseline critiques" were written by this lane to illustrate patterns in the inspected files and are not captured skill outputs.
- Participant-level measures (time, errors, TLX-style ratings, resumption time) need real studies that Kyle authorizes. None were run or simulated.
