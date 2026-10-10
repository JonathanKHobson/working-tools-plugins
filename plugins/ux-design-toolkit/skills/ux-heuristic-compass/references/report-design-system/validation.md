# Report Validation

The report harness validates four layers.

## Payload Validation

Checks source status, scored snapshot, scorecard fields, heuristic scores,
checklist ratings, required narrative fields, and content slot lengths.

## Copy Hygiene

Blocks placeholders, overlong required slots, missing required prefixes, and
human-panel language without human-panel data.

## Static HTML Validation

Generated HTML must not include links, scripts, external assets, `@import`, or
CSS asset URLs.

## Visual QA

Optional browser QA can open the generated HTML at desktop and mobile sizes,
check for blank output, obvious overflow, section order, and awkward wrapping.
Any automation-owned browser must be closed and handed back before signoff.
