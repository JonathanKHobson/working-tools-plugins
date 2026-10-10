# Master Security Toolkit: choose a workflow

For capabilities, first requests and setup, read [Start here](../README.md). For a known task use the matching skill directly. Read its complete procedure and only the conditional support it calls for. A listed MCP or provider still needs current runtime verification.

| Skill | Outcome and selection trigger |
| --- | --- |
| [agent-artifact-scanning](../skills/agent-artifact-scanning/SKILL.md) | Use to statically scan a local agent skill or plugin package for risky instructions, broad permissions, suspicious downloads, prompt-injection patterns, or secret exposure before installing/admitting it. |
| [application-security-testing](../skills/application-security-testing/SKILL.md) | Review an owned application's source, API or staging environment for authorization, injection and other vulnerabilities; triage findings and verify fixes with explicit coverage. Use for appsec reviews and authorized penetration-test planning, not software installation trust. |
| [indirect-injection-review](../skills/indirect-injection-review/SKILL.md) | Use when an AI system reads externally authored or user-controlled content — retrieved documents, web pages, RAG chunks, emails, tickets, tool output, or images — that could carry hidden or encoded instructions. |
| [instruction-security-review](../skills/instruction-security-review/SKILL.md) | Use to assess direct or indirect prompt-injection risk in an LLM prompt, RAG pipeline, AI agent, or AI product design/code. |
| [mcp-security-review](../skills/mcp-security-review/SKILL.md) | Use before wiring, updating, or trusting any MCP server or Claude/Codex plugin. Trigger on 'is this MCP safe', 'review this MCP before I connect it', or after an MCP's command/tools/permissions change. |
| [permission-and-data-review](../skills/permission-and-data-review/SKILL.md) | Use when an install, script, or agent action requests elevated permissions (Accessibility, Full Disk Access, Keychain, SSH, cloud/wallet access), persistence (LaunchAgents/daemons, login items), or access to private local data. |
| [security-regression-tests](../skills/security-regression-tests/SKILL.md) | Use after a security finding (injection, permission, or provenance issue) has been identified, to turn it into concrete mitigations and repeatable pass/fail regression tests. |
| [software-provenance](../skills/software-provenance/SKILL.md) | Use to verify the provenance, authenticity, and integrity of a specific downloaded artifact, package version, or release — checksums, signatures, notarization, attestations, source-to-build traceability. |
| [software-security-review](../skills/software-security-review/SKILL.md) | Explain Master Security Toolkit capabilities and getting started, or use before installing, running, downloading, or wiring any external app, package, script, installer, or repo. Trigger on 'is this safe to install', 'security check this download', 'audit this package/repo'. |

## Application and API reviews

Use `application-security-testing` for owned codebases, APIs, staging tests and finding remediation. Its complete procedure adapts selected Strix methods; no Strix runtime, paid service or scheduled scan is installed. Installation trust remains `software-security-review`.
