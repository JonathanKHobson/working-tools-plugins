---
name: prompt-playbook
description: Reuse the user's recurring prompt patterns to write, refine, or debug prompts in their usual style without re-deriving the pattern each time.
---

# Prompt Playbook

Use this skill when the user asks to:

- improve a prompt in the user's style
- write a prompt the way the user usually prompts
- analyze what is wrong with a sprawling prompt based on his recurring habits

This skill does three things only:

1. Identify the best matching user pattern.
2. Apply the right template.
3. Trim scope to one concrete deliverable when the prompt is trying to do too much.

## Workflow

1. Read the user request and match it to the closest pattern in `references/patterns.md`.
2. Pull the shortest working scaffold from `references/templates.md`.
3. Enforce the house rules from `references/profile.md`:
   - one deliverable
   - one output contract
   - top three traits only
   - no praise for planning or scaffolding

## Pattern selection guide

- If the user already has a draft prompt, start with `Prompt Refinement First`.
- If the user gives a long messy brief, start with `Intent Dump + Constraint Sweep`.
- If the user asks for a role or expert voice, use `Role Framing as Shortcut`.
- If the user stacks many style words, use `Trait-Stack Output Control`.
- If the user wants results ranked across dimensions, use `Multi-Axis Organizing Prompt`.
- If the user asks for deep self-analysis or synthesis, use `Research/Profile Deep-Dive Prompt`.

## Scope discipline

When the request sprawls, say so plainly and reduce it to the next artifact. Prefer the 80 percent shippable prompt over a bigger system.

## References

- `references/profile.md`
- `references/patterns.md`
- `references/templates.md`
