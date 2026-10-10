# Beginner Build Translation

Use this reference when the user is nontechnical, AI-assisted, or asking whether
an app/site/tool idea or existing project "makes sense."

This distills the adopted Vibe Check patterns without replacing the local
`$vibe-check` skill. Reach for `$vibe-check` when the whole session is app
discovery or beginner coaching. Use this file when the output should stay a
short engineering translation.

## Translate The Idea Into A Buildable Slice

Ask or infer:

- the one user group
- the struggling moment
- what they do today
- what changes after V1 works
- one differentiator
- minimum table stakes
- what is parked for V2+

Do not let "MVP" mean "the differentiator only." A switchable V1 needs the
minimum basics users expect plus the one underserved thing it does better.

## Evidence Tags

Use these labels when the user is mixing research, assumption, and excitement:

- `seen it`: supported by a real quote, interview, review, metric, screenshot,
  support ticket, or user-provided artifact
- `hunch`: plausible based on some evidence, but not directly confirmed
- `guess`: an inference; useful only if labeled and tested later

When turning vague ideas into requirements, do not promote a `guess` into a
requirement unless it is clearly marked as an assumption.

## Plain-Language Glossary

Define a term the first time it matters to the next step. Keep definitions
short and practical:

- `local`: the copy on this computer
- `Git`: version snapshots
- `GitHub`: cloud backup and collaboration copy
- `commit`: a saved snapshot
- `push`: send snapshots to GitHub
- `deploy`: publish the app online
- `production`: the real live app
- `staging` or `preview`: dress rehearsal version before production
- `database`: where the app saves structured information
- `API`: a way for apps/services to talk to each other
- `.env`: protected file for secret keys
- `.gitignore`: list of files Git must not snapshot

## Checkup Translation

When the project already exists and the user says the AI keeps breaking it:

- classify as `project checkup`, not new planning
- inspect entrypoints and project map before recommending a rewrite
- translate problems into plain-language names
- prioritize one tidy-up that makes future AI changes easier
- route folder/code organization to `$project-structure-architect`

Useful plain-language architecture tests:

- "one thing, one place": a decision or calculation should have one home
- "simple front door, real work inside": a module should hide complexity behind
  a small interface
- "middleman check": if deleting a layer makes the app simpler without losing
  real behavior, it may not earn its keep

## Output Add-Ons

For Mode 6 answers, include:

- `WORDS YOU NOW KNOW` only when explaining terms would reduce anxiety or
  prevent a wrong next action
- `EVIDENCE LEVEL` when the plan relies on user research, reviews, or guesses
- `FIRST PROOF` when the next step needs a measurable test of whether the idea
  is real

