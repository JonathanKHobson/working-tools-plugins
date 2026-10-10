# Skill Review Mini-Rubric

Use this lightweight rubric when reviewing an existing Codex skill, MCP-facing
skill package, or proposed skill change. It is for fast human/agent judgment,
not a full eval harness.

## Review Rules

1. Read the skill's frontmatter `name` and `description` first.
2. Read only the core `SKILL.md` body before opening references.
3. Judge whether the skill helps the agent make a better decision or take a
   better action than it would without the skill.
4. Fix only critical and major issues by default. For minor issues, first ask:
   would changing this materially improve behavior, or just make the skill
   prettier?
5. Do not add eval JSON, scripts, or validators unless the skill performs a
   repeatable transformation, routes behavior, writes files, or has a known
   trigger regression.

## Severity

- Critical: The skill can trigger unsafe behavior, encourage installing or
  running unreviewed external code, violate a privacy/write boundary, or route
  the agent to the wrong high-risk tool.
- Major: The skill often triggers when it should not, fails to trigger when it
  should, lacks a needed verification step, hides important scope boundaries,
  or gives equal-weight menus where a default is needed.
- Minor: The skill is wordy, has weak examples, buries useful instructions, or
  repeats things the model already knows, but behavior is still basically safe.
- Defer: The issue is real but not worth changing until the skill is used in a
  concrete task or shows a repeated failure pattern.

## Checks

### Trigger Clarity

- The description says "Use when..." or otherwise names the user intent that
  should activate the skill.
- The description includes common phrases the user might actually type.
- The skill has an implied or explicit "do not use when" boundary if another
  local skill owns a nearby lane.
- Strong review signal: write two should-trigger prompts and two
  should-not-trigger prompts from memory. If that is hard, the description is
  probably blurry.

### Action Boundary

- The skill tells the agent what to do, not just what the topic is.
- The first workflow step starts from real local context or user intent.
- The skill names what it must not mutate, install, enable, or assume.
- The skill gives one default path before listing alternatives.

### Source And Provenance

- The skill distinguishes local rules from external inspiration.
- Any external framework, repo, document, or spec is named as a source or
  reference, not smuggled in as local policy.
- If the skill was extracted from a shipped local workflow, it says what
  durable behavior was learned.

### Verification

- The skill has a clear success check for its normal output.
- Risky or user-visible work includes a validation loop, smoke test, visual QA,
  source check, or manual review gate.
- The final answer should report what was verified and what was not.

### Safety And Install Boundary

- External repos, packages, scripts, MCPs, plugins, and apps stay inspect-only
  unless the user explicitly approves execution.
- Copying, installing, running, wiring, or adapting external code routes through
  `personal-security-check`.
- The skill does not widen Codex MCP baselines or client configs as a side
  effect of review.

### Context Cost

- The core `SKILL.md` stays focused on instructions needed every time.
- Detailed references are loaded only when their trigger is met.
- The skill cuts generic advice the model already knows.
- High-value gotchas appear before the agent is likely to make the mistake.

## Output Shape

Use this compact format for reviews:

```markdown
Verdict: keep / revise / split / defer

Findings:
- [Severity] Area - concrete issue and why it changes behavior.

Recommended change:
- The smallest patch that would improve the skill.

Verification:
- How to confirm the skill is better after the change.
```
