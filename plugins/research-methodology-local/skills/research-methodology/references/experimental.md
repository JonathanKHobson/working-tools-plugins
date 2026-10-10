# Experimental Research: Historical Causal Analysis

The historical experimental label is this plugin's convention, not a definition of all scientific experimentation. Use it for an existing, understood system with an observed change in behavior. Recorded traces can substitute for access to the system. If fundamentals are unclear, first explore them.

## Contents

- When
- Orientation
- Before collecting: hypotheses and grouping characteristics
- Steps (data capture, structure discovery, functioning basis)
- Output template
- Filled mini-example
- Not "random tinkering"
- When data already exists
- Relation to other types

## When

- Need a **causal link** between a past action/change and an observed outcome
- Root-cause analysis: regression after a commit, appliance that stops after an event, symptom change after a medication switch in supplied records, price reaction after an announcement, flaky behavior tied to conditions
- Object is **already well understood**: theory supports interpretation of historical data

Examples: git bisect to find the breaking commit; correlating a metric spike with a deploy; tracing a bug to a config change; a washer that stops mid-cycle after a power outage; a stock move after an earnings release.

## Orientation

Backward-looking and practical: works with **recorded historical data** from an existing system, not hypothetical future behavior.

**Do not** substitute experimental for exploratory or descriptive when the object is poorly understood; conclusions will be wrong at a fundamental level.

Theory is not excluded, but deep object knowledge is assumed.

## Before collecting: hypotheses and grouping characteristics

Write these into the charter **before** the first data point is captured:

- **Candidate causes.** If more than one is plausible, list every candidate and, for each, the observation that would confirm or rule it out. A single candidate may be stated as one hypothesis. Adding a candidate after collection is allowed only if it is marked as post-hoc.
- **Grouping characteristics.** The dimensions along which results will be grouped in Step 2 (for example: commit range, build variant, OS version, payload size, cycle phase, error code, load size, trading window). Groups invented after looking at the data are pattern-fitting, not analysis.

## Steps

### 1. Historical-iterative data capture

- Vary one condition per iteration; record raw results
- **No analysis yet**: collection only
- Log: timestamp, conditions, action taken, outcome for each iteration

If monitoring, tracing, logs, VCS history, symptom notes, or price history already captured the data, this step may be **skipped or shortened**.

Output: tables of (time, conditions, result) per iteration. Each row is also a findings-ledger row with rank 3 evidence (the log, trace, commit, observation, or filing it came from).

Where the user authorizes execution, vary one condition per iteration where feasible and record raw outcomes before interpreting them. Use isolated copies for state-changing diagnostic work. A checkout, bisect, deployment, production experiment, or destructive reset requires the corresponding scope and authority; access to a repository is not permission to discard uncommitted changes.

**Safety and legality.** Unplug or shut off supply before inspecting a household device. Gas, refrigerant, sealed high-voltage parts, and anything under warranty go to a professional. Market analysis uses only lawfully public information (filings, transcripts, published insider-transaction reports, official statistics); do not solicit or use material non-public information. A price move after news is association until a mechanism is shown. Health questions stay on supplied records and published literature; they are not medical advice.

If execution is unavailable, analyze supplied records or deliver an unexecuted protocol. Never claim a bisect, benchmark, or reproduction happened without tool evidence.

### 2. Structure discovery

Analyze collected data:

- Group results by the characteristics defined **before collection**
- Identify patterns linking actions to outcomes
- Produce a classification: table or chart mapping actions → results
- Look for confounders, simultaneous changes, selection effects, measurement changes, and missing observations. A deployment or announcement preceding a spike establishes temporal association, not causation.

For noisy tests, record repetitions and the uncertainty of good/bad classification. A skipped or flaky revision is not good. A first-bad commit narrows the candidate change; it does not by itself establish the mechanism.

Goal: reveal the specific regularity and influencing factors, not "see what happened."

### 3. Derive functioning basis

From the classification:

- State how the object behaves under observed conditions
- Rank factors: significant vs negligible
- Produce an **actionable instruction** to achieve or avoid the target outcome
- Confirm the mechanism against a rank 1–2 source when the subject involves a third-party product, study, device, or market (changelog, service manual, filing, documented behavior). A correlation in your own logs or prices is rank 3 until then.

A supported cause needs evidence that distinguishes it from material alternatives, ideally reproduction plus reversal or another appropriate control. Do not force certainty when historical records cannot support it. Market conclusions are scenarios with stated assumptions and uncertainty, not investment advice.

Output: root-cause statement + fix/prevention steps with evidence. Keep observed results distinct from proposed actions.

## Output template

```markdown
# [Issue / Question] — Experimental Research

## Charter
[Goal as a causal question, scope/object/subject, type, questions, sources]

## Candidate causes
| # | Hypothesis | Discriminating observation |
|---|------------|----------------------------|

## Grouping characteristics (defined before collection)
- …

## Data sources
- Git range: …
- Metrics/logs: …
- Manual iterations: …

## Raw iteration log
| # | Time | Conditions | Action | Outcome | Notes |
|---|------|------------|--------|---------|-------|

## Classification
| Group | Characteristic | Count | Pattern |
|-------|----------------|-------|---------|

## Findings ledger
| # | Claim | Evidence | Rank | Answers |
|---|-------|----------|------|---------|

## Scope filter
…

## Object filter
…

## Conclusions
- **Cause:** … (F…)
- **Mechanism:** … (F…)
- **Significant factors:** …
- **Negligible factors:** …

## Action
1. …
```

## Filled mini-example

### Task A: Android build fails with "Duplicate class kotlin.collections.jdk8..." after a dependency bump

```markdown
## Charter
- Goal: name the change that introduced the duplicate class and the minimal fix
- Scope / Object / Subject: Kotlin/Gradle build system / dependency resolution in this Android project / `kotlin-stdlib` vs `kotlin-stdlib-jdk8` on module `:app`
- Type: experimental — build worked at tag v1.4.0, fails at HEAD; both states are recorded
- Questions: Q1 which commit first fails; Q2 which module pulls jdk8; Q3 is this a documented Kotlin behavior
- Sources: git history (3), `gradle :app:dependencies` output (3), kotlinlang.org "What's new in 1.8" (2), AGP release notes (1)

## Candidate causes
| # | Hypothesis | Discriminating observation |
|---|------------|----------------------------|
| H1 | Kotlin plugin bump to 1.8+ merged jdk7/jdk8 into stdlib | failing commit touches kotlin_version |
| H2 | A Cordova plugin pins old kotlin-stdlib-jdk8 | jdk8 appears only under capacitor-cordova-android-plugins |

## Grouping characteristics (defined before collection)
- Commit (bisect range v1.4.0..HEAD); module that declares the dependency

## Raw iteration log
| # | Time | Conditions | Action | Outcome | Notes |
|---|------|------------|--------|---------|-------|
| 1 | 10:02 | v1.4.0 | ./gradlew :app:assembleDebug | OK | |
| 2 | 10:05 | 3f9c1d2 | same | FAIL duplicate class | bumps kotlin_version 1.7.21 → 1.9.0 |
| 3 | 10:09 | 3f9c1d2 | gradle :app:dependencies | jdk8:1.6.21 via cordova plugins module | |

## Classification
| Group | Characteristic | Count | Pattern |
|-------|----------------|-------|---------|
| commit < 3f9c1d2 | kotlin 1.7.x | 1 | builds |
| commit >= 3f9c1d2 | kotlin >= 1.8 | 1 | duplicate class |

## Findings ledger
| # | Claim | Evidence | Rank | Answers |
|---|-------|----------|------|---------|
| F1 | First failing commit is 3f9c1d2 | iteration 2 | 3 | Q1 |
| F2 | jdk8 artifact comes from the Cordova plugins module | iteration 3 | 3 | Q2 |
| F3 | Since Kotlin 1.8, stdlib-jdk7/jdk8 are merged into stdlib | kotlinlang.org/docs/whatsnew18.html#updated-jvm-compilation-target | 2 | Q3 |

## Scope filter
Nothing discarded — F3 is a platform-wide rule, F1–F2 are its instance here.

## Object filter
Nothing discarded — the failing module is the one under study.

## Conclusions
- Cause: kotlin_version bump (F1) combined with a transitive jdk8 pin (F2).
- Mechanism: merged stdlib duplicates classes still shipped by jdk8 (F3). H1 and H2 are both required; neither alone reproduces.

## Action
1. Force `kotlin-stdlib-jdk7/jdk8` to the same version as `kotlin-stdlib` in the root Gradle file.
```

### Task B: front-load washer stops mid-cycle after a power outage

```markdown
## Charter
- Goal: name the most supported cause of the stop and the next safe diagnostic action
- Scope / Object / Subject: household appliances / this front-load washer that stops mid-cycle after a power outage / error code, door lock, and drain pump
- Type: experimental — the machine worked before the outage; symptoms are recorded
- Questions: Q1 which error code appears; Q2 whether the door lock or drain pump matches the manual; Q3 whether the control board is a remaining candidate
- Sources: service manual error table for this model (1), user observations with timestamps (3), manufacturer support notice if any (1)

## Candidate causes
| # | Hypothesis | Discriminating observation |
|---|------------|----------------------------|
| H1 | Door lock did not re-engage after the outage | error code for door/lid lock; door will not latch |
| H2 | Drain pump blocked or not running | error code for drain; water remains in drum |
| H3 | Control board failed after the surge | other codes ruled out; no lock or drain fault |

## Grouping characteristics (defined before collection)
- Cycle phase (fill, wash, drain, spin); error code; load size

## Raw iteration log
| # | Time | Conditions | Action | Outcome | Notes |
|---|------|------------|--------|---------|-------|
| 1 | 18:10 | after outage, small load | start normal cycle | stops at drain; code E21 | power off before opening |
| 2 | 18:22 | same | inspect door latch (unplugged) | latch moves freely; no lock code | H1 less likely |
| 3 | 18:35 | same | check drum for standing water | water remains; pump silent | H2 supported |

## Classification
| Group | Characteristic | Count | Pattern |
|-------|----------------|-------|---------|
| drain phase | E21 | 1 | stop with water left |
| other phases | no code | 0 | not observed |

## Findings ledger
| # | Claim | Evidence | Rank | Answers |
|---|-------|----------|------|---------|
| F1 | E21 is listed as a drain fault for this model | service manual error table, model W, p. 14 | 1 | Q1, Q2 |
| F2 | Cycle stops at drain with water remaining and a silent pump | iterations 1 and 3 | 3 | Q2 |
| F3 | Door latch is free and no lock code was shown | iteration 2 | 3 | Q2 |

## Scope filter
Nothing discarded — rows concern this model's drain path, not other brands.

## Object filter
Revised F3: latch observation is visual only; does not prove the lock solenoid works under power.

## Conclusions
- Cause: drain path (F1, F2); H1 not supported by the observed code (F3). H3 remains open until drain is cleared or the pump is tested by a professional.
- Mechanism: after the outage the machine reaches drain and cannot empty (F1, F2). Association with the outage is temporal; surge damage to the board is not established.
- Next action: keep the machine unplugged; clear accessible lint trap only if the manual allows; otherwise a technician. Gas, refrigerant, and sealed high-voltage parts are out of scope.

## Action
1. Do not run further powered tests. Hand to a professional if the trap is not user-serviceable.
```

## Not "random tinkering"

Experimental research is a structured process over data from a **working object**. Each iteration is recorded; analysis follows collection; conclusions are evidence-backed.

## When data already exists

Production monitoring, distributed tracing, structured logs, VCS history, symptom notes, and price series often eliminate Step 1. Proceed directly to structure discovery on existing artifacts, but still write candidate causes and grouping characteristics first.

## Relation to other types

| Type | Time direction | Requires working system |
|------|----------------|-------------------------|
| Exploratory | Future | No |
| Descriptive | Future | No |
| Experimental | Past | Yes (or recorded traces thereof) |
