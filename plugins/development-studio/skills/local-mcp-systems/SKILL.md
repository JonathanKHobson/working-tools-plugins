---
name: local-mcp-systems
description: Build, index, route, and debug local data-backed stdio MCP servers; use for SQLite FTS, compact tool surfaces, multi-client exposure, retrieval contracts, and launcher diagnosis.
---

# Local MCP systems

Use this active route for local data-backed MCPs and client exposure problems. Read the applicable complete preserved method before implementation:

- [Local Data MCP Builder](../../libraries/local-mcp-methods/local-data-mcp-builder/SKILL.md) for indexing, SQLite FTS, stdio servers, tool contracts, routing, validation, retrieval budgets, client configuration, and evals. Follow its linked references and template assets as needed.
- [Local MCP Debugging](../../libraries/local-mcp-methods/local-mcp-debugging/SKILL.md) when a server fails to launch, attach, list tools, route correctly, or return suitable results.

These methods are a portable adaptation of private local material. [Admission and execution boundaries](../../docs/local-mcp-admission.md) govern their support files. In particular, sample configs are examples only; imported scripts are inspect-only until their exact invocation, inputs, process launches, config reads, and write paths are reviewed for the current project. Do not run a fleet smoke or start a real MCP merely because it is linked in the source method. Index/retrieval templates may be copied into an authorized project after adapting paths and validating with synthetic data. The source method's named external skills are routing hints; resolve them from the installed plugin that owns them, never as package-local relative paths.

For an actual MCP App or human-facing widget, use [Build MCP Apps](../build-mcp-apps/SKILL.md) as the owning app method and consult the local data method only for its storage and retrieval lane. Preserve the distinction between direct stdio smoke, client configuration, a live host connection, and model-visible discovery.
