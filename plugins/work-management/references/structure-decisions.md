# Structure decisions

Before moving files, answer: which current change is hard to make, which responsibilities change independently, and what interface would make the next edit local? If those answers are weak, keep the present structure.

An existing repository's framework and project map control layout. Prefer an adjacent feature folder to a global folder of miscellaneous helpers when a behavior has one owner. Keep shared code shared only after there are real consumers with the same contract. An entrypoint should compose and initialize, while feature logic lives where it can be tested and changed without unrelated edits. Avoid generic wrappers that only forward calls.

For an expandable new project, a few purposeful files are enough. Write the shortest map that points to startup, important data flow, safe run/test command, and the owner of the next likely change. A one-off explicitly single-file artifact stays one file if that is useful.

For a large refactor, note the current workflow and failure risk, preserve a recoverable starting point, then move one boundary at a time. Verify imports and user-visible behavior after each meaningful move. Length alone is a review signal, not a module requirement. A diagram or architecture decision record earns its place only when it resolves a consequential ambiguity.
