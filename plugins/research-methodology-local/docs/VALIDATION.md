# Package validation and release gates

Run `python3 scripts/check.py` for local links, manifests, PNG paths, skill heads and remote endpoint shape; run `python3 -m unittest discover -s tests -v` for the document compiler. The package repository validator and marketplace builder belong to the owning Working Tools repository. A static pass does not prove recipient installation or publication. File-level source rights are recorded in `SOURCE-RIGHTS.md` and `LICENSE-SCOPE.json`.

## Synthetic sample checks

- Research method: ask for a fictional appointment-booking usability protocol. The expected result has eligibility/sampling rationale, consent, neutral tasks, pilot, record and analysis plan. No participant data or external retrieval is needed.
- Academic writing: supply an invented abstract claiming generality from a six-person pilot in which four succeeded. The expected revision narrows the claim, preserves 4/6 and invents no citation.
- Missing Research Compass: run the launcher with `RESEARCH_COMPASS_BINDING` pointing to a nonexistent temporary path. It must exit nonzero with a diagnostic and no download.
- Missing publisher plugin: bundled manuscript or study methods remain available; a provider-specific pass is explicitly unrun.

## Native acceptance

Install the reviewed exact revision through each supported host's native flow. For Codex, verify skill discovery, optional tool exposure, a bundled-method sample and a configured Research Compass routing call if the backend is intentionally supplied. For Claude, verify the same bundled skill and separately installed publisher dependencies; do not infer Claude availability from a Codex cache. Mobile/cloud behavior requires a real host test. Save exact revision, installed path, output and result in release evidence. These checks have not been represented as completed by the staged candidate.
