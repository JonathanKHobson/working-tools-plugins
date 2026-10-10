# Preserved complete local method

Apply this full method when the current entrypoint selects its local build/audit variant. Its backticked support paths are rooted in the current skill directory (one level above this file), where the complete support files are retained. The current entrypoint and user authorization govern host/provider and writing-review behavior.

---
name: resume-crafter
description: Build, edit, target, audit, and sharpen resumes with evidence-backed claims, ATS-safe structure, recruiter-readable positioning, and strong bullet writing.
compatibility: Claude Desktop, Claude Code, Codex, ChatGPT, and other hosts that can use Markdown skills
---

# Resume Crafter

Resume Crafter helps a host AI turn real career material into a clear, truthful, targeted resume. Use it for whole resumes, targeted rewrites, single-bullet edits, resume audits, ATS cleanup, design guidance, and metric-safe impact language.

This skill is public-facing and generic. It must not rely on a private profile, private source register, local file path, personal career history, or hidden application packet.

## Use This Skill When

- The user wants to build a resume from raw work history, notes, LinkedIn text, a portfolio, or an existing draft.
- The user wants to tailor a resume to a job description.
- The user asks to rewrite one resume statement or create stronger bullet options.
- The user wants an audit for ATS readability, recruiter clarity, evidence integrity, or generic language.
- The user asks how to phrase impact when metrics are missing, uncertain, or sensitive.
- The user wants design or layout guidance that keeps the resume usable by both parsers and humans.
- The user is targeting marketing, growth, content, SEO, lifecycle, campaign,
  go-to-market, or product-marketing roles and needs supported evidence
  translated into that role family without inventing campaign results.

## First Move

Identify the task type before writing:

1. Full resume build
2. Targeted resume rewrite
3. Single bullet rewrite
4. Resume audit
5. ATS cleanup
6. Design or layout guidance
7. Metric reconstruction or impact phrasing

If the user provided enough material, proceed. If a missing fact would change the output materially, ask for that fact or mark it as `[MISSING INFO: ...]`.

## Core Rules

- Do not invent jobs, employers, credentials, tools, dates, metrics, responsibilities, scope, seniority, clients, awards, or ownership.
- Preserve truth while improving emphasis, clarity, ordering, and language.
- Use role-specific keywords only when the user's evidence supports them.
- For marketing/growth roles, separate supported evidence from scaffold
  language: audience, offer, campaign, funnel, SEO/content, lifecycle,
  experiment, analytics, and GTM language must map to real supplied work.
- Prefer concrete proof over generic polish.
- Make unsupported claims visible instead of smoothing them away.
- When a metric is not verified, use conservative non-numeric impact language.
- Do not optimize for ATS in a way that makes the resume unreadable to humans.
- Do not create fake precision, inflated titles, or implied ownership.
- Do not undo prior truth corrections. If an earlier pass softened, removed, or corrected a claim for accuracy, preserve that correction unless the user supplies new supporting evidence.
- Use a recruiter-readable vocabulary baseline, especially in summaries,
  skills, project bullets, and hybrid AI/UX/product positioning.
- Avoid unexplained abbreviations or insider shorthand such as `IA`, `UI`,
  `UX`, `viz`, `ATS`, `MCP`, `LLM`, and role-specific labels unless the job
  description clearly expects them.
- If a technical or industry term is necessary, define it in plain language on
  first use. For example: "information architecture (how content is organized)."
- Prefer reader-facing outcomes over craft labels. For example, write
  "made the dashboard easier to scan" before "improved visual hierarchy."
- Replace low-signal technical phrasing with proof. For example, rewrite
  "AI summary, real data viz, five IA buckets" as
  "automatic summary, clear charts, five screen sections."
- Ask before finalizing: "Would a recruiter or hiring manager understand this
  without a design glossary?"

## Default Workflow

1. Define the target: role, industry, seniority, job description, or reader.
2. Inventory evidence: work history, projects, skills, education, credentials, artifacts, metrics, and constraints.
3. Choose positioning: one center of gravity that explains why this candidate fits this role.
4. Draft or revise: use ATS-safe structure and recruiter-readable proof.
5. Audit: check truth, specificity, keywords, formatting, metrics, generic language, unexplained abbreviations, recruiter readability, and whether any prior truth correction was accidentally undone.
6. Return next actions: what to submit, what to verify, and what evidence is still missing.

## Output Shapes

For a full resume, use:

```markdown
# [Candidate Name]
[Location] | [Email] | [Phone] | [LinkedIn/Portfolio]

## Summary

## Skills

## Experience

## Selected Projects

## Education
```

For a bullet rewrite, return:

```markdown
## Best Option
- [Strongest bullet]

## Alternatives
- [Option 2]
- [Option 3]

## Why This Works
- Truth preserved:
- Stronger because:
- Verify before use:
```

For an audit, return:

```markdown
## Resume Health Snapshot
- Target:
- Overall read:
- Top priority:
- Biggest risk:

## Findings
1. Issue:
   - Why it matters:
   - Fix:

## Strongest Existing Material

## Next Revision Pass

## Truth Regression Check
- Prior corrections checked:
- Claims strengthened in this pass:
- Evidence for each upgrade:
- Corrections preserved:
```

## Reference Navigation

| Need | Read |
| --- | --- |
| Choose the right resume workflow and framework | `references/patterns.md` |
| Audit a resume's quality | `references/resume-quality-rubric.md` |
| Rewrite bullets | `references/bullet-rewriting.md` |
| Make the resume ATS-safe | `references/ats-and-formatting.md` |
| Pick positioning by role family | `references/role-positioning.md` |
| Handle metrics, evidence, and missing proof | `references/metrics-and-truth.md` |
| Remove generic language | `references/generic-phrase-guardrails.md` |
| Choose a layout direction | `design/design.md` |
| Use optional specialist roles | `agents/agent.md` |

## Agent Roles

Use the agent files as prompt-role guidance when a resume task benefits from focused review:

- `agents/resume-strategist.md`: positioning, ordering, and role targeting
- `agents/bullet-editor.md`: single bullet and experience-section rewrites
- `agents/ats-auditor.md`: parser safety and formatting cleanup
- `agents/evidence-integrity-reviewer.md`: unsupported claim and metric checks
- `agents/resume-design-advisor.md`: layout and design choices

## Stop Conditions

A resume is ready for the next human review when:

- The target role is clear.
- Each strong claim is supported by supplied evidence.
- Metrics are verified, clearly estimated, or replaced with non-numeric language.
- Prior softenings, cuts, corrected titles, and scope corrections have not been restored without new evidence.
- The structure is ATS-safe.
- A recruiter can identify fit within 10 seconds.
- Generic filler has been replaced with proof, decisions, outcomes, or scope.
- Unexplained shorthand has been removed, expanded, or justified by the target
  job description.
