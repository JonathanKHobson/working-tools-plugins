# Validation — 2026-09-09

## Verified in this build

- Input archive integrity: all 21 original skill files matched the supplied SHA-256 manifest before adaptation. Original ZIP SHA-256: `6a1216c2707712f601e0b227228d83f5b0e27d956230720e76453477ac9218aa`.
- Codex plugin-creator manifest validator: passed.
- Codex skill-creator quick validator: passed for all four bundled skills.
- Internal Markdown file-link check: passed; targets remain inside the plugin.
- Bundled operator structural checker: passed.
- Original kit packaging/installer regression suite, run against the adapted skill: 22 tests passed with Python 3.10.12. Tests cover copy fidelity, dry-run behavior, non-overwrite and symlink rejection, malformed packages, metadata, and broken internal references. An initial run using the Mac default Python 3.9.6 correctly failed the installer's Python 3.10 minimum; rerunning with the supported interpreter passed.
- Instructions reviewed for existing user authorization, available runtime entry points, focus/selection, clipboard preservation, batching, source/destination evidence, and browser handoff. This is an instruction review, not model execution.

## Not claimed

The 34 behavioral fixtures remain `not_run`. No Figma, Stitch, Claude, or imagegen mutation was performed to test this bundle, and no autonomous success rate is asserted. The September 9 transfer example was a historical human-assisted demonstration reviewed from the authorized source task. Current app access and features must be inspected at execution time.

Visual QA and Design Taste Gate were marked not applicable for this Markdown/configuration package. No screenshots or visual artifact were produced, so no visual anchor observations or scores are invented. Both checks are part of the bundled workflow for actual future visual deliverables.

No browser automation session or additional MCP server was started for this build. A confirmed stale duplicate Codex helper was cleaned up using the configured pressure guard.

## Recheck

```sh
python3 skills/figma-ui-operator/scripts/validate_skill.py --json
```

Run the current host's available skill validator for each `skills/*` directory after edits. The original system plugin-creator path is not a receiving-host prerequisite. Use the authorized disposable-file acceptance protocol before describing a later run as live validated.

## FigJam collaboration guidance — 2026-10-03

Extended the existing operator and visual-QA entrypoints with a conditional FigJam guide. The operator now distinguishes FigJam native objects/tool contracts from Design-only workflows. Added preservation, active-task/evidence hierarchy, recoverable authoring, reveal/locking/role checks, and review/reset handoff. The source ledger records the supplied archive hash and separates handoff claims from independently rechecked documentation.

Validation: all four Figma skills passed the available skill-creator quick validator; the bundled operator structural checker passed. Across the four updated plugins, 35 entrypoints passed, four manifests parsed with existing skill/MCP paths resolving, and 77 relative links in changed guidance resolved, including the new heading targets. The routing audit reported no blocking findings or missing skill references; its pre-existing unindexed-skill warnings were left alone. The older system plugin-creator validator/cachebuster was absent after path discovery, so no result from that validator is claimed; versions were updated in source while preserving unrelated manifest fields.

Independent simulated instruction checks rejected privacy/readiness/screen-reader claims from two API properties and one screenshot, preserved source content in a layout-only cleanup, and bypassed FigJam procedures for an ordinary Design typo. A 40-minute facilitation case retained simultaneous comparison and unknowns; its response assumed the absent sponsor held decision authority, so that assumption must be checked in real use. These were text responses, not live tool execution or participant tests.

Actual-editor reveal, background-only locking, native response editing, links, voting/follow, participant-role/multiplayer, keyboard, screen-reader, and laptop readability were not tested in this maintenance task. No Figma canvas was changed. Package Markdown/metadata is nonvisual; visual QA applies when the guidance produces a real artifact. No template code/assets, external runtime, browser session, or temporary MCP was introduced.

## Live-finding follow-up — 2026-10-03

The later implementation handoff informed only the existing FigJam reference, source ledger, this verification record, and the plugin version. The guide now tests node parenting and section membership alongside background-only locking and reveal; records unlocked staged backgrounds as a disclosed fallback; checks bounds again after revealing a resized section; and rehearses realistic ShapeWithText overflow before replicating its geometry. Native link/reveal separation and authoring-quota recovery are explicit. Separate static-object locking remains untested.

The source ledger distinguishes supplied live observations from independent package checks. Reported 1366×768 operator checks do not establish participant usability, multiplayer behavior, or screen-reader support. No board was operated by this maintenance task; the other three plugin sources did not need another change.

Follow-up package checks: all four skill entrypoints passed quick validation, the operator structural checker passed, and both relative reference links/heading targets in the changed documents resolved. No executable helper behavior changed. Native installation and installed-file parity are checked separately at release.
