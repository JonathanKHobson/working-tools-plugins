# Instructional Design For Communication

Use this reference when the user wants to learn, practice, critique, simulate,
or transfer a communication pattern. Keep the output proportionate: not every
message needs a lesson.

## Modes

- `create`: produce or revise the artifact quickly.
- `critique`: evaluate an existing draft against criteria.
- `coach`: guide decisions and tradeoffs before writing.
- `practice`: give a constrained exercise and feedback method.
- `simulate`: respond as the intended reader, reviewer, stakeholder, or client.
- `teach`: explain the pattern, show why it works, then support transfer.

Infer the mode from the prompt when possible. If the mode changes the output
substantially and cannot be inferred, ask one essential question or state the
assumption.

## Rhetorical Situation Analysis

Use for high-stakes, ambiguous, sensitive, or strategic messages:

```yaml
rhetorical_situation:
  speaker:
  audience:
  relationship:
  purpose:
  channel:
  stakes:
  constraints:
  power_dynamics:
  emotional_risk:
  action_needed:
  likely_misread:
  recommended_strategy:
```

## Outcome And Evidence

Before drafting, identify:

- what the reader should understand
- what the reader should do
- what evidence or proof makes the message credible
- what quality criteria define success
- what must remain uncertain or visible

## Cognitive Load Pass

Use when the message is long, complex, or likely to overwhelm:

- intrinsic complexity: what cannot be simplified without losing truth
- extraneous load: jargon, weak sequence, redundant context, hidden ask
- chunking: headings, bullets, example, summary, or table
- optional depth: what can move after the main ask
- next action: the one thing the reader should do

## Worked Example And Faded Scaffold

For teaching or practice:

1. Show a compact strong example.
2. Annotate why it works.
3. Map the pattern to the user's context.
4. Give a partial template.
5. Ask for an independent attempt.
6. Review with a rubric and one next practice variation.

## Reader Simulation

When simulating, answer as the target reader:

- What decision would I make?
- What seems credible?
- What feels vague, risky, or emotionally off?
- What question remains?
- What would increase trust?
- What is the highest-leverage revision?

## Transfer Bridge

End learning-oriented responses with how to adapt the communication for:

- novice vs expert readers
- skeptical readers
- time-constrained readers
- higher or lower power-distance contexts
- written vs spoken delivery

Do not infer sensitive traits or stereotype audiences. Personalize only from
supplied context.
