# Task-specific AI workflow evaluation

Use when a decision depends on whether a changed prompt, model, skill, provider or workflow improves the user's actual work. Work Management owns worker routing and typed advisory gates; this method owns a comparison protocol. A supplied vendor benchmark informs candidate selection but does not establish local benefit.

## Define the comparison

Write the decision, current workflow, proposed change, intended users, output and unacceptable failure. Change one factor where possible; otherwise compare named workflow bundles and avoid attributing the difference to a model alone. Preserve the current working baseline. Define the smallest representative task set that can inform this decision, explaining what it leaves out. Do not invent a universal required sample count.

For each task keep an ID, authorized input location, expected usable outcome, source/version, scoring criteria and important boundary case. Use synthetic or redacted inputs where private material is unnecessary. Include routine work, known failures and cases where the right action is to abstain, ask for missing evidence or avoid a tool. Separate development examples from unseen acceptance tasks; do not tune against the acceptance answers.

Choose observable scoring bands before comparing outputs. Record accepted alternatives and critical failures separately from partial credit. Source fabrication, unauthorized external action or missing required work cannot be hidden by a good average. For subjective craft, define anchors using strong, partial and flawed examples, then calibrate raters on the same evidence. Blind candidate names and vary presentation order when feasible. Keep model judges advisory until checked against human judgments.

## Run and retain evidence

Use authorized providers and an agreed cost/resource limit; writing the protocol does not authorize spending or uploading client files. Fix the task inputs and record model/version, prompt, skill revision, tools, permissions, relevant settings and run date. Reset task state between trials and prevent access to prior answers. Repeat where variable behavior matters; report the number of tasks and trials rather than treating retries as new tasks.

Retain the actual output and state/artifact receipt needed to score it. Distinguish a failed output, a missing observation, an unavailable provider and an environment failure. Inspect disputed failures before changing the rubric; version any correction and rescore both candidates consistently.

## Decide without overstating

Compare task-level quality first, then human repair effort, elapsed time, observed token/cost usage and local resource pressure where measured. Unknown cost is unknown, not free. Separate setup effort from repeated-use cost. Show failures and abstentions as well as successes; do not report only the best retry. A small pilot supports a bounded trial decision, not a general superiority or safety claim.

Deliver one compact table: task ID; baseline/candidate versions; trial count; score and critical failures; evidence path; repair effort; measured cost/time; uncertainty. Add the decision (retain baseline, revise, bounded adoption or insufficient evidence), its rationale and when changed inputs or versions require rechecking. Keep task data and results in the owning project, not in this shared skill.

Example: compare two evidence-brief workflows on the same authorized sources. Score factual support, required coverage and usefulness separately. An elegant brief with an invented source fails the factual gate; a provider outage is recorded separately. No example scores here are actual results.

## Provenance

Original local synthesis of existing Research evidence controls and Work Management's advisory-decision validation. The supplied [Feedough article](https://feedough.co/p/how-to-create-your-own-ai-benchmarks) motivated making user-task evaluation explicit; no article text or prompt was imported. Technical cross-check: [Anthropic's agent evaluation guidance](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents), accessed 2026-10-02, supports checking outcomes, stable trial environments, grader calibration and inspecting failures. No external evaluation package, telemetry, grader service or execution hook is installed.
