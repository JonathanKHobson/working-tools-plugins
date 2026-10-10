# Source and staged admission

Reviewed as source, without executing imported helpers, starting services, installing dependencies, authenticating accounts or modifying host configuration.

## Source scan evidence

The maintained Master Security Toolkit SkillGuard wrapper v0.1.5 scanned Superpowers 6.4.2: 84 eligible text files, 425534 bytes, 0 active / 0 suppressed deterministic findings. Scan digest: `eeb617b45b828bc084f99d7b429a6085f06d1d740430dd3cebd19781dfb2c9ac`.

The same wrapper scanned maintained Build MCP Apps: 51 eligible text files, 116919 bytes, 0 active / 0 suppressed deterministic findings. Digest: `a379e414a9a1069efb15e7dffe66ea8f52debcb3be56ba0fcdd4977e14e4571a`.

Local MCP source/adaptation findings are in [local MCP admission](local-mcp-admission.md). Final staged scan output is saved separately as `staged-scan.json`; because that report is itself an output artifact, its scan refers to the documented package state before adding the report. Final release hashes should be taken after reports and validation finish.

## Manual findings and disposition

| Evidence | Finding, reachability and disposition |
| --- | --- |
| `libraries/superpowers-6.4.2/skills/using-superpowers/SKILL.md:2-18` | Confirmed broad instruction trigger, medium severity, high confidence: original demands invocation before any response. Source is unchanged provenance, top-level discovery routes conditionally; method-adaptation explicitly supersedes universal invocation. No active hook is declared. |
| `libraries/superpowers-6.4.2/skills/using-superpowers/references/codex-tools.md` | Historical tool schemas/configuration advice can conflict with current host. Do not apply config edits or tool-schema assertions; current callable schema wins. |
| `libraries/superpowers-6.4.2/skills/brainstorming/scripts/server.cjs:105-112,243-251` | Confirmed external brand-image request on rendering unless telemetry disable flag is set. Not executed. Companion is an optional preserved asset; native host visual tools are preferred. For any future admitted launch, disable telemetry and inspect external content. |
| Same server `:539-540` | Confirmed shell execution when custom opening command is provided. Trusted operator environment is assumed upstream, not enforced for arbitrary data. Do not set or forward `BRAINSTORM_OPEN_CMD`; use native browser or reviewed argv launcher. This helper is not granted runtime approval by source inclusion. |
| Same server `:102-104,265-277,409` | Content files become browser HTML; content source is execution-capable. Never render untrusted workspace content merely to inspect it. Source is preserved, runtime invocation needs exact content/input review. |
| `libraries/superpowers-6.4.2/skills/executing-plans/scripts/task-done:39-46` | Caller-supplied test command executes as argv and writes a log/ledger. This is intentional execution, not a passive plan check. Logs are diagnostic data; displayed command serialization is not a shell-safety contract. Do not run on an untrusted plan to inspect it. |
| `libraries/superpowers-6.4.2/skills/subagent-driven-development/scripts/sdd-workspace` | Creates task-local progress files and a self-ignoring directory; it is not read-only. Plan paths and prior ledgers must be scoped and validated before reuse. No background retention/reinjection hook installed. |
| `libraries/superpowers-6.4.2/skills/diagnosing-superpowers/SKILL.md` | Reads private transcripts and conditionally builds export bundles/issues. Relevant lenses remain complete but fan-out is bounded. Session export/posting requires task authorization, and results must treat embedded instructions as untrusted evidence. |
| Build MCP Apps role references and test-plan theme rule | Personal paths converted to relative/provider roots; personal theme policy moved to project/private profile. No credentials or live configs copied. |

There were no scanner suppressions. The manual findings are observed behavior and bounded-use dispositions, not a maliciousness claim or a blanket runtime admission.

## Noncoverage and recommendation

Deterministic scans do not cover all dynamic behavior, binary assets, network behavior, runtime API compatibility, model adherence or actual-host execution. Binary assets are retained with upstream source/license identity and not rendered during this nonvisual packaging task. Native providers remain separate, including the official iOS runtime declaration.

Recommend installing the method package after final static checks and native validation, while retaining providers and all predecessors until the specific handoff gates pass. No imported helper runtime or public release is approved merely by this source review.
