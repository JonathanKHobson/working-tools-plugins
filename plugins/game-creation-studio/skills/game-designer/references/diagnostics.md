# Game Design Diagnostics

Use these checklists to diagnose a design quickly. Pick only the relevant sections. Do not turn every answer into a giant audit unless the user asked for one.

## Fast Diagnostic Sweep

Run this short pass first:

1. What is the fantasy or promise?
2. What verbs define that fantasy?
3. What is the core loop?
4. What resources and constraints create tension?
5. Where are the meaningful decisions?
6. What does the system accidentally reward?
7. What failure mode is most likely active?
8. What is the smallest test that would confirm the diagnosis?

## Fantasy

- Is the intended feeling clear in one sentence?
- Do the available verbs support that feeling?
- Does the reward structure reinforce the fantasy or contradict it?
- Does the fail state still feel on-theme?

Warning signs:
- the pitch sounds exciting but the actions are generic
- the fantasy is broad but the verbs are narrow
- players describe the experience with a different fantasy than the team intended

## Verbs and Core Loop

- Can the player repeat a satisfying cycle within the first few minutes or turns?
- Does each cycle create a new decision or just more maintenance?
- Are rewards immediate enough to teach the loop?
- Does the loop escalate, diversify, or merely repeat?

Warning signs:
- dead turns
- maintenance turns
- repetition without new stakes
- rewards disconnected from the loop

## Decisions

- What are the top three recurring decisions?
- Are those decisions contextual or solved?
- Is there meaningful opportunity cost?
- Can players recover from a suboptimal choice?
- Do players understand why one option is stronger?

Warning signs:
- dominant strategy
- false choice
- obvious best upgrade path
- low decision density
- high complexity with low consequence

## Economy and Progression

- What are the main resources, including time, position, actions, trust, attention, and currency?
- What are the main sources and sinks?
- Which resources gate power, tempo, or access?
- Does progression unlock new play or just inflate stats?
- Where does scarcity create tension?

Warning signs:
- grind without mastery
- resource inflation
- one resource solves every problem
- upgrades erase tradeoffs
- late-game bloat

## Balance and Counterplay

- What strategies are currently strongest?
- Why are they strongest: numbers, tempo, safety, clarity, low execution cost, hidden information?
- What answers exist?
- Are those answers accessible, understandable, and worth using?
- Does early advantage compound too hard?

Warning signs:
- runaway leader
- unbeatable opening lines
- turtling
- kingmaking
- asymmetric factions with no counter-pressure

## Pacing and Readability

- Where does tension rise, release, and rise again?
- How quickly can players parse board state, combat state, or objective state?
- Are important states visible at a glance?
- Does onboarding teach through action, text, or punishment?
- Are downtime and resolution time proportional to the drama created?

Warning signs:
- unreadable state
- excessive downtime
- tutorial overload
- long resolution for low-impact outcomes
- constant intensity with no relief

## Onboarding

- What must a new player understand to take one competent turn or minute of action?
- What can stay hidden until later?
- Does the game teach by doing, by text, or by failure?
- Is the first success achievable quickly?
- Does early play reinforce the right habits?

Warning signs:
- first session feels like homework
- players learn the wrong strategy first
- core systems unlock too late to hook interest

## Replayability

- What creates variation: asymmetry, map state, card flow, roles, social play, build paths, encounter mixes?
- Are repeated plays discovering new patterns or just re-solving the same puzzle?
- Does mastery open new lines or collapse into solved play?

Warning signs:
- novelty mistaken for depth
- too much variance to plan around
- too little variance to sustain discovery

## Common Failure Modes

### Dominant Strategy

- One option is reliably best across most contexts.
- Fix by adding counterplay, increasing opportunity cost, narrowing applicability, or strengthening alternatives in their intended context.

### False Choice

- Options look different but collapse into the same outcome or one is obviously inferior.
- Fix by differentiating context, payoff timing, or interaction with the rest of the system.

### Runaway Leader

- Early advantage compounds faster than the trailing player can respond.
- Fix by reducing positive feedback, adding counter-pressure, or creating new risk for leaders.

### Turtling

- Defensive non-action is safer and stronger than engaging.
- Fix by increasing external pressure, rewarding initiative, or capping stall value.

### Stalemate

- The system produces repeated low-movement equilibrium with no forcing function.
- Fix by adding scarce objectives, escalating pressure, or rules that break parity.

### Analysis Paralysis

- The game offers too many branches or too much hidden computation for the value of the choice.
- Fix by reducing branch count, improving readability, or front-loading defaults.

### Grind

- Repetition increases time cost without increasing mastery, discovery, or tension.
- Fix by compressing repetition, adding meaningful unlocks, or reducing sink pressure.

### Unreadable State

- Players cannot parse what matters, what changed, or what is likely to happen next.
- Fix by improving visual/state clarity, surfacing consequences, or reducing simultaneous demands.

## Playtest Prompt Bank

- What did players try to do that the system discouraged?
- What did players ignore because the game failed to reward it?
- Where did they hesitate, stall, or ask for rule clarification?
- What surprised them in a good way?
- What surprised them in a bad way?
- What did skilled players exploit immediately?
- What did weaker players fail to perceive?
- What single rules or number change would best test the current hypothesis?
