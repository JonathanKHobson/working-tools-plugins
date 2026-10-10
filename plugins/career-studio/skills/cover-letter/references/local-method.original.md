# Preserved complete local method

Apply this full method when the current entrypoint selects its local build/audit variant. Its backticked support paths are rooted in the current skill directory (one level above this file), where the complete support files are retained. The current entrypoint and user authorization govern host/provider and writing-review behavior.

---
name: cover-letter-crafter
description: Build, edit, target, audit, and sharpen cover letters with truthful hooks, compact proof arcs, company-fit caution, and evidence-backed voice.
compatibility: Claude Desktop, Claude Code, Codex, ChatGPT, and other hosts that can use Markdown skills
---

# Cover Letter Crafter

Cover Letter Crafter helps a host AI turn real candidate evidence and target-role context into a concise, specific, truthful cover letter. Use it for whole letters, targeted rewrites, opening hooks, proof paragraphs, company-fit checks, voice cleanup, and unsupported-claim review.

This skill is public-facing and generic. It must not rely on a private profile, private source register, local file path, personal career history, or hidden application packet.

## Use This Skill When

- The user wants to build a cover letter from raw notes, a resume, job description, or rough draft.
- The user wants to tailor a cover letter to a role without inventing company research.
- The user asks to rewrite an opening hook, proof paragraph, closing paragraph, or full letter.
- The user wants to check whether a cover letter sounds generic, inflated, or too much like AI.
- The user needs help turning resume evidence into a short persuasive proof story.
- The user asks whether a company-specific claim, metric, or values statement is supported.

## First Move

Identify the task type before writing:

1. Full cover letter build
2. Targeted cover letter rewrite
3. Opening hook rewrite
4. Proof paragraph rewrite
5. Company-fit audit
6. Voice or tone cleanup
7. Unsupported claim or metric review

If the user provided enough material, proceed. If a missing fact would change the output materially, ask for that fact or mark it as `[MISSING INFO: ...]`.

## Core Rules

- Do not invent company research, mission alignment, contacts, referrals, credentials, tools, dates, metrics, responsibilities, scope, seniority, clients, awards, or ownership.
- Do not reuse company-specific praise from an old letter unless the current target is the same company or the user confirms the same context.
- Preserve truth while improving focus, structure, specificity, and voice.
- Use one or two proof stories rather than listing every capability.
- Prefer a role-specific hook over "I am writing to apply."
- Keep unsupported company context visible as `[MISSING INFO: verified company signal]`.
- When a metric is not verified, use conservative non-numeric impact language.
- Do not auto-send, imply obligation, or pressure a referral contact.

## Default Workflow

1. Define the target: role, company, reader, application context, and whether the letter is cold, referral-based, or mission-fit.
2. Inventory evidence: resume facts, projects, skills, artifacts, metrics, work style, constraints, and company signals supplied by the user.
3. Choose the arc: hook, proof paragraph, role/company bridge, and close.
4. Draft or revise: make the letter specific, compact, and defensible.
5. Audit: check truth, company claims, proof strength, metric safety, voice, and generic language.
6. Return next actions: what to verify, what to personalize, and what not to claim.

## Output Shapes

For a full letter, use:

```markdown
Dear [Hiring Team or Contact Name],

[Role-specific hook grounded in the job, company signal, or reader problem.]

[One compact proof paragraph using supplied evidence.]

[Bridge from proof to the role, team, or mission. Use [MISSING INFO: verified company signal] when needed.]

[Confident close with a low-friction next step.]
```

For a hook rewrite, return:

```markdown
## Best Hook
[Opening paragraph]

## Alternatives
1. [Option]
2. [Option]

## Support Check
- Uses supplied facts:
- Needs verification:
- Avoid saying:
```

For an audit, return:

```markdown
## Cover Letter Health Snapshot
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
```

## Reference Navigation

| Need | Read |
| --- | --- |
| Choose the right cover-letter workflow and framework | `references/patterns.md` |
| Audit cover-letter quality | `references/cover-letter-quality-rubric.md` |
| Write or repair openings | `references/hooks-and-openings.md` |
| Build proof paragraphs | `references/proof-paragraphs.md` |
| Check company-fit claims | `references/company-fit-and-research.md` |
| Tune voice and tone | `references/voice-and-tone.md` |
| Handle metrics, evidence, and missing proof | `references/metrics-and-truth.md` |
| Remove generic language | `references/generic-phrase-guardrails.md` |
| Choose a letter template | `templates/template-index.md` |
| Use optional specialist roles | `agents/agent.md` |

## Agent Roles

Use the agent files as prompt-role guidance when a cover-letter task benefits from focused review:

- `agents/cover-letter-strategist.md`: arc, target fit, and template choice
- `agents/hook-writer.md`: opening strategy and hook options
- `agents/proof-editor.md`: proof paragraph and evidence compression
- `agents/company-fit-auditor.md`: company research and values-claim safety
- `agents/evidence-integrity-reviewer.md`: unsupported claim and metric checks

## Stop Conditions

A cover letter is ready for the next human review when:

- The target role and letter context are clear.
- The opening is specific and not generic application boilerplate.
- Every company-specific claim is supplied or visibly marked for verification.
- Each strong candidate claim is supported by supplied evidence.
- Metrics are verified, clearly estimated, or replaced with non-numeric language.
- The letter has one coherent proof arc and a low-pressure close.
