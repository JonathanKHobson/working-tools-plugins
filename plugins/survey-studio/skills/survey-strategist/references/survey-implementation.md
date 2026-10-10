# Survey implementation

Use only when the user wants a working collection flow or platform integration. A draft, export or review remains at that requested stage. Identify the owning project and reuse its existing persistence, authentication and survey facilities before adding infrastructure.

## Definition and context

Render each authorized entry path from one canonical instrument. Preserve stable question IDs, codes and instrument versions; retain the definition associated with historical responses. Store minimal interpretation context separately from answers: experience or transaction ID when relevant, collection source, instrument version and timestamp. Do not confuse an account ID with an anonymous response ID.

Use trusted context lookup or validated public identifiers; raw URL parameters cannot authorize private access. Where context is absent, ask or use an explicit selection rather than silently assigning a population. Shared instruments support comparison only when constructs, wording and populations make that interpretation defensible.

## Collection and privacy

Implement presentation, validation, persistence, truthful acknowledgement and authorized retrieval. Show success only after storage confirms. Handle double-clicks and network retries without accidental duplicate responses, preserve answers after failure where appropriate, and document the limits of anonymous duplicate prevention without defaulting to fingerprinting.

Verify account linkage, cookies, IP/server logs, small-cohort combinations and identifying free text before describing privacy. If unknown, state the uncertainty and handle responses conservatively. Confirm response access and retention; separate voluntary follow-up contact where appropriate. Public collection access must not grant access to raw responses or administration.

Keep feedback voluntary and dismissible; do not silently make it a condition of access or completion. Other form types can have required fields when justified by their stated purpose. Build additional administration, dashboards or automation only when the requested outcome needs them. Current authorization governs publication and invitations; historical activity does not supply it.

## Verify the requested end state

Exercise each relevant entry path with tagged synthetic responses and read back stored values, context and version. Check missing/invalid context, skip/branch behavior, validation failure, save failure, retry and duplicate handling. Test participant versus owner access. Inspect exported columns/codes and keep skipped, not-applicable and low scores distinct. Exclude synthetic responses from analysis and clean them up where authorized.

For a visible form, map 3–8 source/viewport anchors before changes and recheck affected labels, controls, focus, validation and completion states on relevant desktop/mobile views. A static export or source inspection does not verify collection, accessibility or platform behavior. Use platform-specific import and preview checks; never treat descriptive programming notes as implemented logic.

Technical validation does not replace respondent comprehension testing or an operational pilot. Report the actual state—drafted, exported, configured, locally tested, deployed, response persisted or distributed—and outstanding checks. Stop when the requested slice is verified.
