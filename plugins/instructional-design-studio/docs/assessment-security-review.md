# Assessment-source security review — September 27, 2026

**Verdict:** Proceed with caution for read-only source study and the original local skill update. This is not an approval to install the reviewed repositories, run their scripts or connect their services.

**Confidence:** Medium for the inspected paths and this action scope. No full dependency, binary, supply-chain or runtime audit was performed.

**What was inspected:** Two supplied research texts, selected files in four public repositories, nine primary method sources, four public activity/resource routes, and 31 local File-O-Fun/Atlas records. Exact repository file lists and observed HEADs are in [source records](../skills/assessment-rubric-design/references/source-records.json); links/adoption decisions are in [sources](../skills/assessment-rubric-design/references/sources.md).

**Threats checked:**

| Surface | Finding / handling |
|---|---|
| Source spoofing / mirror | Repository-owner URLs and institution/publisher pages used; NBME original publication read through Rowan's institutional host. |
| Provenance / tampered artifact | HEADs and selected published files inspected; no release binary fetched or verified. Local source hashes record this snapshot, not trust. |
| Install-time scripts | Selected manifests/Python helpers read; none executed. Full dependency trees and nested components remain unaudited. |
| Persistence / services | No external hooks, startup services, MCPs, installers, extensions or auto-updaters added. |
| Sensitive-data access | Local reference reads stayed scoped; no learner data, credentials, browser profiles or private-note upload requested. |
| Prompt injection / tool poisoning | Source docs and skill text treated as untrusted evidence, not authority. No third-party entrypoint loaded as live instructions. |
| Network / tool surface | Public GET/read and Git ref inspection only for research; no hosted MCP enabled. New local helpers have no network or subprocess capability. |
| Reuse rights | Licenses differ; unknown-source material remains local reference. No third-party code/templates/prose files bundled. |

**Risks found:** The quiz-builder template inserts authored strings through `innerHTML` and embeds answers; future renderer reuse would require safe text handling and a practice-only confidentiality boundary. Gareth's repo has a separate hosted MCP/token path; it is outside this update. Its manifest/package version labels differ, so the commit records are more precise. One inspected repo lacked an explicit license. Some advice conflates cognitive level and difficulty, rejects recall too broadly, or overgeneralizes survey response rules; those rules were not adopted.

**Unknowns:** Complete dependency security, runtime behavior and binary provenance of external repos; reuse rights for some original local cards; missing scans behind selected transcriptions; actual learning impact and psychometric performance. No absence-of-malware or validated-assessment claim follows from this review.

**Safer path used:** Original modular references, examples and standard-library helpers in the existing personal plugin. Source facts, proposed adaptations and observed validation remain separate. No external runtime is needed for archive search or bank checks.

**Commands run / not run:** Ran read-only file inventory, hashing, targeted web reads, Git HEAD lookup, local validators and authored helper tests. Did not run reviewed external scripts/installers, package lifecycle hooks, generators or hosted services; did not install scanners. Existing plugin is refreshed only through the already installed Codex CLI after local checks.

**MCP fingerprint:** Not applicable: no MCP is installed, updated, wired or enabled by this change. A future MCP proposal requires its own full capability fingerprint and review.

**Final recommendation:** Use this personal edition for drafting and selecting activities, with review/piloting appropriate to the intended score use. Before copying third-party implementation or distributing source-derived assets, review the exact artifact and its license again.
