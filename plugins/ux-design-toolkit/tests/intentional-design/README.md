# Paired design and content checks

Maintenance fixtures from the user-supplied Intentional UX pack, 2026-10-02. These are fictional test definitions, not results or a validated quality scale. They do not run automatically and are not loaded for ordinary design work.

`cases.jsonl` contains 30 generator inputs: a failure and legitimate counterpart per pattern plus four cross-cutting cases. `expectations.jsonl` is evaluator-only. `routing-cases.jsonl` contains 12 activation cases with expectations; strip expected_activation and relevant_pattern_ids before passing those prompts to a generator.

1. Select cases for the changed behavior plus their legitimate counterparts. Freeze before/candidate instructions and use the same model, tools, source access and output budget. Preserve completed outputs rather than reconstructing a baseline from memory.
2. Give each fresh generator only the appropriate instruction variant and ordinary task input. Keep expectations, previous answers and suspected failures out of its context. Supply no fabricated live screenshots or measurements for text fixtures.
3. Independently compare outputs against the evaluator criteria. Permit alternative valid solutions. Record pass/partial/fail/unassessed, evidence, missed problems, unwarranted changes and false claims separately. No aggregate score may conceal a consequential fabrication.
4. Add a small held-out task relevant to actual work, using authorized source material. A synthetic ecology note or fictional comparison flow remains synthetic; a real project outcome needs its own source and rendered/reader verification.
5. Report model/settings, input and instruction hashes, loaded files, actual answers, reviewer basis and untested outcomes in the owning project. Repeat only failures or newly affected cases after a correction. An already-passing baseline supports retained capability, not a claimed improvement.

Case groups: P01–P07 cover UX visual/task fit; P08–P12 also concern Writing Quality (contrast, true counts, useful parallelism, attribution and situated voice); P13 covers composition. Ownership stays with existing specialists. Do not export user screenshots or voice samples as reusable fixtures.

For a suspect template, test one task change with brand constant and one brand change with task constant when relevant. The first tests structural responsiveness; the second tests preservation of interaction invariants. Neither proves user performance without appropriate user or task evaluation.
