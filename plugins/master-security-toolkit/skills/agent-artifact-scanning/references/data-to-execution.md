# Trace data that can become execution

Apply only when a reviewed artifact builds command strings, browser content/workspace loaders, or promises a non-mutating inspection mode. Use after the existing static scan; reuse its file/line adjudication and context/trigger checklist instead of repeating the whole review. This adds manual questions, not a new detector or execution permission.

## Generated commands

Follow each untrusted path, label and value into the actual consumer. Structured subprocess argv without a shell has a different boundary from a command displayed/copied for an agent or terminal. HTML escaping a copied command is not shell quoting. Double quotes still permit expansions in POSIX shells; quoting rules differ across POSIX, cmd and PowerShell. Judge each serialization against its declared shell, including embedded quotes, substitutions, separators, percent/bang expansion and newlines. Prefer passing structured argv to an authorized tool. Preserve the source values as data; do not execute a candidate or synthetic payload to inspect quoting.

## Browser data

Separate text/attribute escaping, JSON script-boundary escaping and URL validation. Trace identifiers/classes as well as visible text. An escaped link can still use an active scheme. A workspace script loader executes code even if the files are called data; identify who can create/replace those files and whether it accepts remote origins. Prefer parsed JSON or explicit import over arbitrary script data, allow only the intended schemes and path scope, and retain input/output trust separation. Hardcoded component HTML or a static code string alone is not evidence of external injection; confirm attacker control and reachability before classification. Do not open unreviewed generated HTML to perform static admission.

## Inspection modes

Read the full call path of dry-run, settings-only, help/describe, package/check and update-check modes before invoking one. Importing a module, probing an executable, resolving dependencies, downloading metadata, rendering a page, unpacking archives or running checks is behavior even when the flag sounds passive. Record observed side effects and any branch-dependent promises. For untrusted candidates use trusted text/AST/manifest readers that do not import the target. Candidate evaluation, when specifically authorized, belongs to an isolated runtime phase and must report what actually ran.

## Unexecuted acceptance scenarios

- A path containing quotes or shell metacharacters remains one argv value; a copied shell form uses that shell's safe serializer or is withheld. No test instruction is executed during admission.
- A plan's quote-bearing ID cannot break an attribute, a closing-script token cannot end embedded JSON, and an active URL scheme is rejected. A workspace file claiming to be data cannot silently become executable code.
- A settings-only branch that unpacks an archive and a dry-run branch that imports a checker are classified as side-effectful despite their names. A truly passive read needs no added install approval.
- No regex match plus a reachable unsafe input-to-execution path remains an unresolved/confirmed finding, not a safety pass. A hardcoded empty innerHTML or static component string is not called malicious without a source-to-effect chain.

Record path/line, source control, consumer, classification, severity/confidence and the smallest fix in the existing review. No blanket approval, telemetry, new background trigger or scanner rule is introduced.

Method provenance: original local refinement from the Bloom Studio admission review, 2026-10-02. No candidate source code or prose copied. Existing reviewed scanner contract and current user authorization remain authoritative.
