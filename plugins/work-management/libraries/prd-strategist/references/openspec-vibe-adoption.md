# OpenSpec And Vibe Check Adoption Notes

These notes capture the useful patterns harvested from:

- `Fission-AI/OpenSpec` at commit `1b06fdd`, npm `@fission-ai/openspec@1.4.1`
- `TexasBedouin/vibe-check` at commit `f675bbe`, local installed skill `vibe-check`

## Security And Runtime Boundary

- OpenSpec is MIT-licensed and installed only in the local review workspace at
  `work/security-integration-pass/tool-installs/openspec` with
  `npm install --ignore-scripts`.
- OpenSpec CLI usage must set `OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1`.
- Do not run `openspec init`, `openspec update`, workspace setup, shell
  completions, dashboard, or agent-file generation unless the user asks for that
  exact write lane. Those commands can write project/global config or agent
  guidance files.
- Day-to-day PRD work should use the local
  `scripts/create_change_packet.py` scaffold instead of depending on OpenSpec.
- Vibe Check is installed as a static local skill. Do not run its `bump.sh`
  release helper.

## Adopted From OpenSpec

Use a lightweight change packet when chat history is too loose for
implementation:

```text
proposal -> specs -> design -> tasks -> verification -> archive decision
```

Keep the packet fluid, not ceremonial:

- `proposal.md`: why this matters now, what changes, capabilities, scope, impact
- `specs/<capability>/spec.md`: behavior-first requirements and scenarios
- `design.md`: implementation approach, tradeoffs, risks, open questions
- `tasks.md`: ordered checkboxes small enough to verify
- `verification.md`: acceptance checks, evidence log, rollback, archive decision

Use RFC-style words only where they help:

- `SHALL` or `MUST`: required behavior
- `SHOULD`: recommended but contextual
- `MAY`: optional

Specs describe observable behavior, not internal implementation. Put framework,
file, dependency, or migration details in `design.md` and `tasks.md`.

Run this scaffold when useful:

```bash
python3 <work-management-plugin-root>/libraries/prd-strategist/scripts/create_change_packet.py \
  "add calendar availability preview" \
  --output-root ./changes \
  --capability calendar-availability \
  --why "Users need to see conflicts before proposing times." \
  --what "Add a preview that marks unavailable blocks before scheduling." \
  --scenarios "available time selected,conflicting time selected" \
  --tasks "Add availability resolver,Render preview states,Add conflict test"
```

## Adopted From Vibe Check

Use this when product planning starts before requirements are clear, especially
for a beginner, AI-assisted builder, early product idea, or app checkup.

Discovery should separate:

- what the user is trying to accomplish
- what they do today
- the struggling moment that creates demand
- evidence from real users, reviews, forums, or observable behavior
- assumptions that are only hunches

Evidence tags:

- `seen it`: real quote, user input, review, metric, screenshot, or source
- `hunch`: plausible from evidence but not directly proven
- `guess`: agent/user inference; do not overstate

Opportunity scoring:

```text
Opportunity = Pain + max(0, Pain - Served)
```

- `Pain`: how much the need hurts for one specific user group
- `Served`: how well current options already handle it
- high Pain + low Served is the differentiator
- high Pain + high Served is table stakes

V1 scope should include:

- one differentiator: the top underserved need
- only the table stakes required to let someone actually switch
- everything else parked as V2+

For marketplace or multi-sided ideas, discover and score each side separately.
The second side's must-haves are not optional; they hold the whole loop up.

## Beginner Product Artifact Shape

When a nontechnical or AI-assisted builder needs a plan, produce:

- what they are building
- who it helps and in what moment
- the first working version
- V1 versus V2+
- screens, data, integrations, rules, and states
- terms glossary in plain language
- cost/free-tier assumptions
- secret-key and deployment cautions
- growth loop or honest "no loop yet" note
- build phases with checkpoints

## Checkup Mode Pattern

When an AI-built project feels messy or scary to change:

1. Make a safety snapshot first if the repo supports it.
2. Inspect entrypoints and project map.
3. Produce a friendly, visual or card-based report with the few worthwhile
   tidy-ups.
4. Fix one thing at a time.
5. Verify behavior after each tidy-up.
6. Update the project map or decision note so the cleanup sticks.

Use the "microwave principle" from Vibe Check as a plain-language translation
of deep modules: a good component has a simple front door and real work inside.
