---
name: application-security-testing
description: "Review an owned application's source, API or staging environment for authorization, injection and other vulnerabilities; triage findings and verify fixes with explicit coverage. Use for appsec reviews and authorized penetration-test planning, not software installation trust."
---

# Application security testing

When orientation helps, briefly name this skill’s outcome, needed input and expected result, then proceed. Broader help uses the [plugin introduction](../../README.md); skip maintainer notes unless needed.


Read the complete [scoped application testing procedure](../../references/application-security-testing.md) before reviewing a codebase, API, running application, or supplied penetration-test report. It adapts the useful Strix source/API/web assessment and remediation methods to this host's existing tools; the Strix runtime is not installed.

Start from the requested target and existing authorization. Source review can proceed within that scope. Live exploitation requires a defined authorized target, isolated test environment, allowed actions and credentials. Do not expand a repository-install review into attacks on its publisher or hosted service. Do not silently install Strix, upload source to its cloud, add CI jobs or purchase scan credits.

Deliver reproducible evidence, root cause, proposed or applied mitigation, exercised regression result and untested coverage. Source suspicion, an automated claim and a confirmed exploit are different states. Use the existing security-regression-tests skill for a demonstrated finding. External tool installation uses software-security-review; instruction packages use agent-artifact-scanning.

## Conditional coverage-led source audit

For an explicitly requested multi-surface codebase security audit whose results need complete coverage accounting and independently checked finding records, read [coverage-led audit adaptation](../../references/coverage-led-security-audit.md). It routes to the preserved Cloudflare method and its schema/validators. The existing scoped procedure remains the default for focused source/API reviews and fixes. The full Cloudflare workflow's dynamic phase requires a verified OS-enforced sandbox; without it, record held validation and do not claim a completed full audit.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports Security Reviewer, Security Specialist. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
