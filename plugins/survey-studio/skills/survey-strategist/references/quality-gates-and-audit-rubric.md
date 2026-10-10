# Quality Gates and Audit Rubric

## Verdicts

- **Field-ready:** no release blockers; required evidence and validation complete.
- **Ready after fixes:** design is viable, but named errors must be resolved and retested.
- **Not ready:** objective/method/audience, ethics, logic, or analysis is fundamentally unresolved.

A numeric score supports prioritization; it never overrides a release blocker.

## Severity

| Severity | Meaning | Action |
|---|---|---|
| Critical | likely harm, invalid consent, major privacy/security risk, wrong population/method, or unusable instrument | stop fielding |
| Error | likely invalid measurement, broken path/export, inaccessible required task, or analysis-blocking defect | fix and retest |
| Warning | plausible bias, burden, ambiguity, or maintainability risk | fix or document acceptance |
| Info | enhancement or observation | consider |

## 100-point rubric

| Domain | Points | Evidence |
|---|---:|---|
| Decision alignment | 15 | objective, owner, decision rules, item-purpose map |
| Audience and sampling | 10 | population/frame, eligibility, recruitment, claim limits |
| Measurement and wording | 20 | construct fit, neutral/answerable items, recall, pretest |
| Response options and scales | 15 | exhaustive/exclusive choices, anchors, codes, scoring |
| Flow, logic, and burden | 10 | journey, path tests, duration, relevance, mobile |
| Accessibility and inclusion | 10 | semantic/interaction tests, inclusive categories, accommodations |
| Privacy, ethics, and governance | 10 | data inventory, notice/consent, minimization, retention, review |
| Analysis and export readiness | 10 | analysis plan, codebook, test response, validated files |

### Scoring

For each domain assign:

- 0%: absent or fundamentally wrong;
- 25%: major gaps;
- 50%: partially specified/unverified;
- 75%: mostly sound with minor gaps;
- 100%: complete, evidenced, and tested.

Report score, evidence, and defects. Do not award full points based on a written claim without artifacts or test results.

## Release blockers

- no clear decision/objective or survey is the wrong method;
- wrong/undefined target population;
- required sensitive data without necessity and appropriate handling;
- privacy/consent language contradicts actual collection;
- high-risk study lacks required ethics/legal/security review;
- primary item is leading, double-barreled, or not answerable;
- choices overlap or omit common valid responses;
- broken/circular/forward logic or unreachable required item;
- validated scale altered while claiming original validity/benchmark;
- required interaction inaccessible without alternative;
- no cognitive pretest for a new/materially changed instrument;
- no test responses or codebook for a programmed survey;
- duplicate IDs/codes, malformed export, or unsupported feature silently lost.

## Audit procedure

1. Load canonical instrument and brief.
2. Run `survey_lint.py` and `estimate_burden.py`.
3. Trace every item to objective and analysis.
4. Review wording/options/scales independently.
5. Test all logic paths and exported values.
6. Review accessibility, inclusion, privacy, ethics, and localization.
7. Inspect pretest/pilot evidence and change log.
8. Validate final exports and version alignment.
9. Record findings with severity, evidence, owner, fix, and retest status.
10. Issue verdict.

## QA report structure

- instrument/version/date/reviewer;
- scope and evidence reviewed;
- verdict and score;
- release blockers;
- findings table;
- burden estimate and hotspots;
- path/export test results;
- pretest/pilot status;
- accepted risks and owners;
- final sign-off conditions.

Use `assets/qa-report-template.md`.
