---
name: pattern-picker
description: Framework sommelier that selects the best thinking system, reasoning model, or problem-solving pattern from a framework library before applying one. Use when the user asks for a pattern picker or which framework to use, says they are stuck, brainstorming, or unsure how to tackle something, or needs a way to structure their thinking, for example "what's the best way to think about this?"
---

# Pattern Picker

Route ambiguous problems to the right thinking tool before solving them. Do not apply a framework until you complete intake and choose the best fit from the library.

## Recipient library binding

The original 389/353-record reference corpora are excluded because their redistribution grants are unverified. This package includes eight clearly labelled, original synthetic entries for a harmless sample. They are not a validated framework collection or a replacement for the omitted corpus. The complete selection procedure below is retained.

For real work, the recipient supplies an authorized fast index and matching detailed-entry file in their workspace. Resolve those two exact paths from the user's input before retrieval; references to the two library filenames below then mean those selected recipient paths. Keep source attribution, stable names and redistribution limits alongside the recipient files. Use the bundled sample files only for an explicitly synthetic trial. If no authorized working library is available, request the needed source and do not claim to have searched the omitted corpus.

External Atlas, memory, design and critique tools mentioned below are optional neighboring services. Use the receiving host's equivalent approved tools or report them unavailable. They are not installed by this skill.

## Retrieval Source Priority

- Use the pattern-picker skill itself as the default lightweight workflow.
- Start with the local `references/` files for normal candidate discovery and narrowing.
- Use `knowledge_atlas` only when richer concept or framework context is needed:
  - the user is fuzzy, ambiguous, or highly domain-specific
  - the first pass does not produce strong candidates
  - you need fuller record detail, related concepts, or better recommendation support
- Treat Knowledge Atlas as an escalation layer, not the default first step.

## Coordination and MCP Awareness

- Use this skill before heavier planning skills when the user is stuck on framing, method choice, or which thinking system to use.
- Use `$work-management:focus-work` when the real issue is not framework choice but priorities, sequencing, or "what should I work on right now?"
- Use `$mac-ops-toolkit:mac-environment-conventions` when the user appears blocked by machine/storage/runtime constraints rather than thinking structure.
- Hand off to `$work-management:product-definition` after framework selection when the user needs a scoped product plan, spec, roadmap, or engineering-ready requirements.
- Hand off to `$ux-design-toolkit:ux-heuristic-compass` when the chosen framework leads into bounded interface evaluation, heuristic UX audit, or report-ready UX findings.
- Hand off to `$ux-design-toolkit:design-studio` when the chosen framework leads into frontend implementation planning or code-facing UX review.
- Hand off to `$critical-compass` when the chosen framework is really a
  reasoning audit, claim evaluation, evidence check, or multi-lens decision
  review. Use its Quorum Mode for high-stakes decisions that need independent
  expert lenses and a synthesized recommendation.
- Use `knowledge_atlas` as the richer second-pass library when the local references are not enough.
- Use `kyle_second_brain` memory recall when the best-fit framework should be grounded in prior conversations, saved notes, previous reasoning threads, or durable decisions.

## Core Rules

- Run intake first on every invocation. Do not recommend frameworks before intake is complete.
- Recommend exactly 3 frameworks. Never recommend more or fewer.
- Pick 1 clear winner and say why it beats the other 2.
- Do not default to famous frameworks such as SWOT or 5 Whys without checking the library first.
- Always use the two-pass retrieval flow:
  - Default file flow:
    - Pass 1: scan `references/framework-library.md` to narrow to 5-8 plausible candidates.
    - Pass 2: search `references/framework-library-rich.md` for only the top 3 candidates by exact framework name and read only those entries.
  - Escalation MCP flow:
    - Use `route_atlas_request` or `search_atlas` when the file-based pass is not enough.
    - Use `retrieve_lens_cards` for compact framework or lens-card support.
    - Use `build_context_pack` for only the final top 3 candidates when you need richer record detail.
- Never read the rich library end-to-end.
- Tailor the final prompt to the user's actual problem, phase, deliverable, and constraints. Do not emit a generic template.

## Workflow

### 1. Intake

Ask this structured intake first:

1. What's the problem or goal?
Describe what you're trying to figure out, decide, create, or solve. Be as specific or fuzzy as you want , we'll sharpen it together.

2. What phase of work are you in?
Choose one:
- Explore
- Define
- Ideate
- Plan
- Compose
- Analyze
- Compare / Decide
- Prioritize
- Evaluate / Review
- Troubleshoot
- Other

3. What's your desired deliverable?
Examples: checklist, one-pager, structured prompt, decision, plan, draft, conversation guide, prototype spec.

4. Are there constraints?
Examples: time pressure, audience, tone, topics to exclude, tools available.

If the problem remains ambiguous after these answers, ask up to 3 additional clarifying questions. Ask only questions that materially change framework selection or the final prompt.

### 2. Retrieval and Recommendation

After intake:

1. Start with the fast index in `references/framework-library.md`.
2. Narrow to 5-8 candidates before choosing the final 3.
3. Search the rich reference file for only those top 3 candidates and read their entries.
4. If that pass still feels weak, incomplete, or too fuzzy:
   - Use `route_atlas_request` or `search_atlas` with the user's goal, stage, constraints, and any obvious topic filters.
   - Use `retrieve_lens_cards` when compact operational lens cards are enough.
   - Use `build_context_pack` for only the final top 3 candidates when you need richer record detail or neighboring ideas.
5. Recommend exactly 3 frameworks.

When using the MCP, prefer framework records over glossary-only terms. Use glossary records only to clarify concepts, vocabulary, or neighboring ideas around the shortlisted frameworks.

For each framework, provide:

- Framework name
- One-sentence rationale for why it fits this specific situation
- One line on why each of the other 2 is a runner-up instead of the winner

Then:

- Pick 1 winner and state clearly why it edges out the others.
- Produce a ready-to-use prompt tailored to the user's situation.

Use this output shape:

```markdown
## Best-Fit Frameworks

### 1. [Framework Name]
Why it fits: [one sentence tied to the user's actual problem]
Why not the winner vs. [Runner-up A]: [one line]
Why not the winner vs. [Runner-up B]: [one line]

### 2. [Framework Name]
Why it fits: ...
Why not the winner vs. ...
Why not the winner vs. ...

### 3. [Framework Name]
Why it fits: ...
Why not the winner vs. ...
Why not the winner vs. ...

## Winner
[Framework Name] is the best fit because [specific edge over the other two].

## Ready-to-Use Prompt
[Copy-paste-ready prompt customized to the user's goal, phase, deliverable, and constraints]
```

## Prompt-Writing Requirements

- Reference the user's real context, not placeholders.
- Preserve any relevant constraints, audience, or tone.
- Tell the framework exactly what to produce.
- If the framework benefits from a sequence, encode the sequence in the prompt.
- Keep it copy-paste ready.

## Anti-Patterns

- Do not skip intake even if the answer feels obvious.
- Do not rely only on familiar frameworks already in your head.
- Do not recommend a framework you did not verify in the library.
- Do not jump to the MCP before the lightweight skill workflow has had a fair first pass.
- Do not produce a vague final prompt.
- Do not apply the winning framework until the user chooses to continue.

## Apply or Iterate

After delivering the recommendation, end with:

`Want to go with this, swap to one of the runners-up, or explore a different angle?`

If the user proceeds, apply the chosen framework in full. If the chosen framework turns out to be a poor fit, explain what was missing and suggest the closest alternative from the library.

## Reference Files

- Default local files:
  - `references/framework-library.md`: fast index for candidate discovery and narrowing
  - `references/framework-library-rich.md`: detailed entries for the final top 3 only
- Escalation MCP tools:
  - `route_atlas_request`: choose the next Knowledge Atlas read-only retrieval route
  - `search_atlas`: keyword, semantic, hybrid, or fallback retrieval when the shortlist still feels weak
  - `retrieve_lens_cards`: compact operational framework, lens, or concept cards
  - `build_context_pack`: optional supporting context when the user needs neighboring ideas or glossary concepts
