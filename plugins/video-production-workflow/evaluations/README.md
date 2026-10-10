# Skill Routing and Pressure Scenarios

`scenarios.jsonl` contains positive trigger cases and near-neighbor boundary cases for the sixteen skills. A future Codex pass should run these through the available skill evaluator before and after any description or routing change.

Evaluation dimensions:

1. Correct skill retrieval.
2. No unnecessary neighboring-skill trigger.
3. Skill body is read rather than guessed from description.
4. Required references/scripts are discoverable.
5. Hard rules survive realistic pressure and time-saving temptations.
6. The response creates the correct artifact boundary and routes downstream work.

The current archive provides scenarios but does not claim an external plugin-eval score because the `plugin-eval` executable was not present in the build container.
