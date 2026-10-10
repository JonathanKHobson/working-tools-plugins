# Verification record

Reviewed September 8, 2026. This records observed checks for version 0.1.0. Instruction quality remains something to improve through actual use; these checks do not establish learner outcomes.

## Package and helper checks

- Both plugin manifests passed plugin-creator validation.
- All 19 skill folders across the two packages passed skill-creator validation.
- All 63 relative Markdown links across the source packages resolved after the verification reports were added.
- Every skill has discovery metadata in `agents/openai.yaml`.
- The alignment and agenda examples passed their actual command-line checkers.
- Eighteen helper checks passed: two valid examples and sixteen malformed or inconsistent cases. Coverage includes dangling outcome IDs, missing practice, duplicate IDs, missing outcome coverage, score-total mismatch, unknown assessment references, invalid types, overlapping/gapped agenda segments, wrong duration, missing closeout/fallback, and nonfinite or boolean numbers.
- No connector, account, additional MCP server, background process, or API key is required for ordinary text skill use.
- Existing global skills and external evidence archives were preserved.

The JSON checkers test structure, coverage, and arithmetic. They cannot establish appropriate difficulty, assessment validity, facilitator competence, accessibility conformance, or learning effectiveness.

## Independent behavioral review

A separate agent used the actual package skill instructions to produce four complete responses:

| Request | Observed result | Limit |
|---|---|---|
| Offline 25-minute AI draft verification lesson | Complete materials, worked example, guided practice, different independent task, answer key, feedback, rubric, and retry; unknown price was distinguished from a known free price | The original scenario also appeared in a package reference, so this was primarily a completion test |
| Unfamiliar 18-minute observation-versus-inference lesson for six adults | Completed examples, paired practice, individual assessment, answer guidance, feedback, retry, and a changed-setting task; all timing sums to 18 minutes; no AI or prompt-writing diversion | Text lesson reviewed; live pacing and learner performance unpiloted |
| Immediate help after repeated interruptions in a discovery workshop | 123-word response with speakable intervention, participation alternatives, and no unauthorized shift to a vote | Simulated response, not a facilitated event |
| Faithful organization of three notes, including an exact repeat | All three source IDs and original strings retained separately; no invented themes, contributors, or prevalence | Text input only; handwriting/OCR was not tested |

The review identified overlapping score anchors in the illustrative factual-support rubric. They were rewritten to distinguish correcting some original unsupported claims, correcting all, and introducing new unsupported claims. AI prompt-writing and tool-choice exercises were also made conditional on the requested learning outcome. The independent follow-up review confirmed both fixes and found no material issue in the unfamiliar non-AI lesson.

## Research and personal-source review

Primary research, professional guidance, and standards are linked in the relevant research reference, with applicability and access limits. Empirical findings, design frameworks, standards, curated patterns, and personal preferences are distinguished. No unsupported universal learning-style prescription, learning-pyramid percentage, or fixed attention-span rule was adopted.

Academic Writing Toolkit performed four targeted author-year/reference consistency audits after reference formatting was corrected: Ryan and Deci (2000), Freeman et al. (2014), Pashler et al. (2008), and Pashler et al. (2007). All four returned zero citation issues. This was a narrow citation-format check, not independent verification of every claim or full-text review of every source.

| Source requested | Actual coverage |
|---|---|
| Coursera | Read the supplied project dashboard and the linked course overview; observed the separate draft project and the actual launched course |
| Google Drive | Read the guided-project proposal, development workbook, and an older draft; retained source/version distinctions |
| Gmail | Read the October 2024 course-production correspondence for historical context; no messages sent and no raw email bundled |
| GitHub | Fetched the portfolio teaching-AI case at a specific branch/blob; treated it as secondary framing |
| Past conversations | Inspected relevant original user messages about workshop transcription, concise questions, and teaching process/context |
| Local files | Read portfolio source notes and existing teaching/GM skills; located course archives without claiming a full review of the original media |
| File-O-Fun | Read selected method cards and archive documentation; all nine adapted method examples were identified as later draft expansions |
| Knowledge Atlas | Read the NVC needs-based-dialogue pattern; treated it as curated practice rather than empirical or clinical authority |
| Deep Research | Applied the research workflow to primary studies, official practice guides, accessibility standards, and facilitation methods |
| Academic Writing Toolkit | Ran the four citation consistency audits described above |

No raw private transcript, email, workbook, learner record, original course media, or card scan is bundled. The historical personal source retained locators at that time. This public export excludes them and unknown-rights source summaries; current scope is recorded in PROVENANCE.json.

## Coursera visual source anchors

Course overview at `https://www.coursera.org/teach/chatgpt-beginners/course/overview`; observed viewport 2094 × 1151. Coordinates below are approximate normalized regions.

| Anchor | Region / UI hint | Observed fact | Action and closeout |
|---|---|---|---|
| C1 | x .12–.34, y .12; course heading | The linked teaching course was open | Match it to the development evidence; confirmed |
| C2 | x .35–.39, y .12; status badge | “Launched” displayed | Record actual launch state separately from old workbook checkboxes; confirmed |
| C3 | x .31–.69, y .42; public-version card | Original version marked live from October 8, 2024 | Use only as observed delivery state; no claim of educational effectiveness |

The user’s tab was returned to its original project dashboard. Process inspection showed normal Chrome without automation-only profile/headless arguments. No automation-owned Chrome was left running.

## Limits and release boundaries

This deliverable is a source plugin package, not a rendered learner-facing document, website, or classroom deployment. Visual layout/design-taste QA is not applicable to the package itself; the Coursera source screen was inspected using the anchors above. Future visual artifacts generated with these skills still require their own visual QA.

No real learner pilot, workshop, role-play runtime, SCORM export, LMS import, accessibility certification, publication, or learning-gain measurement was performed. Historical role-play runtime verification remains labeled with its original date. Current tool interfaces and platform requirements must be rechecked when a future task depends on them.

## Collaborative-board guidance — 2026-10-03

Updated the existing workshop-design agenda/evidence references and decision-making patterns. Guidance now carries one active task through evidence, candidates, common-criteria comparison, decision/deferral, and accepted action while preserving original records. It distinguishes live reveal from review mode, presentation hiding from privacy, and a proposed owner from an accepted commitment. Counts, timing, and template choices remain adaptable recommendations.

All eight entrypoints passed skill-creator quick validation. Local links in the changed files passed, and the existing manifest parsed with its skills/MCP paths resolving. No helper code changed. The old system plugin-creator validator was unavailable; no new pass from it is claimed.

A separate agent produced a simulated 40-minute sequence with typed-chat access, simultaneous comparison, explicit Unknowns, recommendation/deferral, and honest action ownership. It assumed the absent sponsor held final authority; actual delegation remains an input to verify, not a general rule that sponsor absence prevents a decision. No facilitated session, participant pilot, or FigJam runtime check was performed. Source scope is recorded in the existing facilitation-evidence reference.
