# Last30Days Adoption Notes

Source reviewed: `mvanhorn/last30days-skill` v3.6.0, commit `3fa91fc`.

## Adoption Decision

Adopt the research model and recreate safe planner support locally. Do not
install or activate the full Last30Days runtime/MCP by default.

## Why Not Install By Default

The repo is MIT licensed and has a dependency-light Python core, but the full
runtime crosses several sensitive boundaries:

- optional X/Twitter `AUTH_TOKEN` and `CT0` session tokens
- optional API keys for OpenAI, xAI, OpenRouter, Brave, Exa, Serper, Google,
  Apify, ScrapeCreators, Parallel, Bluesky, and related providers
- browser-cookie helpers for Chrome and Safari profiles
- macOS Keychain and `pass(1)` setup scripts
- webhook/Slack delivery for watchlists
- an MCP bundle that shells out to the Python engine and accepts sensitive
  provider configuration
- optional paid or billable provider paths

Those surfaces are legitimate for a user who explicitly wants that runtime, but
they are not safe to wire into Jonathan's local baseline without a narrower
approval for the exact provider, key, cost, storage path, and browser/session
behavior.

## What We Adopted

- recent-window framing, defaulting to 30 days
- source-lane planning before search
- entity-aware query expansion for people, companies, products, and repos
- first-party posts, releases, GitHub activity, hiring, markets, and community
  discussion as separate evidence lanes
- community-language extraction, including memorable comments when useful
- coverage ledger with strong/thin/missing/excluded lanes
- side-by-side comparison framing
- shareable HTML/report handoff requirements that preserve dates, citations,
  uncertainty, and excluded-source notes

## Local Recreated Piece

Use `scripts/current_social_plan.py` to create a safe source plan:

```bash
python3 <plugin-root>/skills/current-social-research/scripts/current_social_plan.py \
  "OpenClaw" \
  --mode product \
  --aliases "Peter Steinberger,steipete" \
  --decision "decide whether this informs a Shareables workflow"
```

The script performs no network calls and reads no credentials. It only emits a
research plan, query variants, source lanes, risk gates, and a coverage ledger
template.

## Future Install Gate

Only revisit a full Last30Days install when the user explicitly asks to run that
runtime and confirms:

- target host: Codex skill, Claude plugin, MCP bundle, or another harness
- exact source/provider lanes to enable
- whether paid APIs may be used
- where keys and outputs may be stored
- whether browser profile/cookie access is allowed
- whether watchlists or outbound webhooks are allowed

Without that approval, use the local planner plus live public browsing.

## Complete-method extension

The original note above records the narrower adoption at its original source pin. For the complete v3.28.1 source and all selected research methods, use [complete recent research](complete-recent-research.md). Its current Studio adapter retains the runtime/access holds and governs new work.
