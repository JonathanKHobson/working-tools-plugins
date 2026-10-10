# Code navigation

Use exact text search for known names, configuration values, filenames and completeness counts. Use a language server for definitions, references and rename boundaries when available; anchor the query to a real source position and read the returned code. Fuzzy or semantic search can locate candidate areas but cannot prove exhaustive absence.

A cold language-server result is not proof of no references. Confirm document symbols from an in-scope file and retry once. If unavailable, enumerate exact text matches, inspect dynamic references, generated code, configurations, tests and examples, and state that semantic completeness was not verified. Before a refactor, identify consumers and invariants and run the affected type/tests after editing.

The complete original local [Code Intelligence method](../skills/code-intelligence/SKILL.md) and pinned Apache-2.0 upstream method/reference closure are now retained. Their exact rights notice and source identities supersede the historical grant hold.
