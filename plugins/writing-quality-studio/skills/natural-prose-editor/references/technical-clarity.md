# Technical clarity

Use for instructions or technical explanations where wording affects what the reader does. Keep this mode separate from fiction, dialogue and deliberate personal voice.

- Preserve executable content exactly: commands, flags, identifiers, file paths, UI labels, quoted errors and literal values. Edit surrounding explanation; flag a suspected technical error separately.
- Identify the actor, prerequisite, action and observable result. Put a condition before the action when a reader must evaluate it before proceeding. Separate independent actions into steps; distinguish instructions from explanatory notes.
- Use stable names for concepts and keep pronoun references clear. Explain necessary technical terms instead of replacing them with less accurate everyday words.
- Preserve modality. A requirement, recommendation, capability, permission and uncertain result are different claims. Do not turn “might fail” into “fails,” or advice into a mandatory step, just to simplify the sentence.
- Keep words needed for grammar and interpretation. Choose length for comprehension; do not impose sentence quotas, vocabulary bans or forced contractions.
- For a broad or translated audience, clarify dates, units and references to controls. Use the control's label rather than relying on position or color.

## Choose the reader's path

For skill, plugin and agent instructions, edit for economical action. Prefer
short, complete sentences, concrete verbs and one clear job per paragraph.
Remove repeated explanations, inflated role claims and context the intended
reader can reliably infer. Preserve facts and instructions needed to act.

Reveal detail as the reader commits to a task:

1. **Startup description:** state the intended job and when to choose it.
2. **Orientation:** explain the purpose, useful input, expected result and
   the next relevant reading route.
3. **Procedure:** give the actions and checks needed for this task.
4. **Conditional depth:** link examples, variants, tools and exceptions with
   a clear reason to open each reference.

Each layer should add information. Cut paraphrases of the previous layer,
duplicate global guidance and unrelated historical decisions. Keep one
authoritative rule and link to it from other owners. Combine tiny references
when they answer the same decision; split a long procedure when its branches
serve distinct tasks. File count alone is not a quality measure.

Review negative instructions individually. Keep one when it prevents a
plausible wrong action, preserves authorization or a factual distinction, or
corrects an observed recurring failure. Otherwise state the desired action
directly or remove the line. Avoid explaining rejected alternatives to a fresh
reader who has no reason to consider them.

After shortening, compare the jobs, triggers, conditions, action order, source
claims and acceptance checks with the original. Test a realistic request and
a nearby request that belongs elsewhere. The shorter version must still lead
to the right method and complete result. Moving words into a reference reduces
initial reading only if its route is clear and the agent loads it when needed.

For a how-to, state the goal and prerequisites, then actions in use order, an observable result and only the troubleshooting that helps this task. Keep explanatory notes outside the action line. A note explains a reason or consequence; it does not hide a required command. For a concept explanation, name the concept, its behavior and one accurate example before discussing exceptions. For release notes, say what changed, who is affected and whether the reader must act; put a breaking change before optional improvements.

Put a warning before the action that creates the risk. Name the actual consequence and scope, especially for destructive flags, irreversible migrations, credential exposure or production settings. Do not upgrade a possible risk into a certain result. Example: “Before you run `--force` against production, confirm the target. The flag may delete rows that do not match the source.” The literal flag and uncertainty remain intact; the sentence does not claim deletion was observed.

For an error message, report what happened and the known cause, then one next check or action. If the cause is unknown, label it unknown rather than inventing diagnosis. For a technical audit instead of a rewrite, report the exact location, ambiguous actor/condition/action/result, likely reader error and a proposed correction. Keep suspected defects in commands or product behavior separate from prose fixes.

Verify against the original: literal spans, action order, conditions, negation, numbers and obligation remain correct. Then read once as someone carrying out the steps. Report missing instructions rather than inventing operational behavior. Editing a command's explanation is not a command-execution test.

This is a practical clarity pass. If the user requests ASD-STE100 compliance, consult the applicable official standard and dictionary; this reference does not establish compliance.

Informed by the inspected [Plain English](https://github.com/b1rdmania/claude-plain-english-skill) and [Natural Writing](https://github.com/anotb/natural-writing) marketplace skills (2026-09-28). Original local synthesis; no source scripts or rule catalogs imported.
