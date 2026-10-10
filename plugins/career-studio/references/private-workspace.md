# Private application workspace

This plugin contains reusable procedures and neutral templates. Candidate facts, contact details, work history, preferences, answers, tailored files, evidence and application records belong in an external private workspace, never in a skill, plugin cache, example or release archive.

Resolve the workspace from the current task first. For a returning local user, an optional `~/.config/career-studio/workspace.json` may bind `workspace_root`, `active_campaign`, `portfolio_root` and `secondary_operator_root`. Read this user-owned configuration only for career work. Verify the paths and current campaign; no file or permission is implied merely by its existence. The plugin must remain useful without this optional binding. Keep machine-specific paths out of shared manifests and skills.

Within an existing workspace, preserve its profile, evidence, packet, ledger and dashboard layout. Prefer one authoritative application ledger and a derived dashboard. Another agent's staging folder may supply evidence, but must reconcile into that same ledger by employer and requisition. Read current source records immediately before writes and preserve other operators' updates. Do not create a second tracker on resume.

Keep personal answers with their exact question, role/employer scope, source, review date and any user confirmation. Reuse a fact only when the question means the same thing and no newer evidence contradicts it. Routine wording can be inferred; insurance, legal eligibility, experience, compensation commitments and other missing facts cannot. Sensitive disclosures remain optional unless the form requires a user decision.

For a new user with no tracker, create a small private ledger beside their application material when requested. A dashboard is warranted only by the requested workflow, and its counts derive from receipts. Publishing a portfolio or sharing this plugin never authorizes sharing the application workspace.

Before sharing, inspect the actual staged archive for candidate data, private paths, populated examples, receipts, screenshots, hidden files and credentials. Preserve author attribution and licenses. Export only maintained plugin content; exclude local bindings, backups, caches and generated application artifacts. Run `scripts/check_share_safety.py` as one check, then inspect flagged or ambiguous content manually.

Optional binding keys `voice_profile` and `linkedin_context` may point to the user's existing private writing profile and current LinkedIn brief. Resolve them only for relevant career/social work; missing bindings do not block a supplied-context draft. Treat old metrics, current employment and availability as requiring current evidence. Shared plugins never embed those private paths or facts.
