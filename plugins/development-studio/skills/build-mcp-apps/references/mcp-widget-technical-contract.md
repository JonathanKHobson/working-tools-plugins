# MCP widget technical contract

Use this reference for an interactive MCP App regardless of frontend framework.
It complements the UX Design Studio compact-widget guidance; it does not replace
the product's visual or content owner.

## Boundaries

| Boundary | Required evidence | Failure behavior |
| --- | --- | --- |
| Initialization | Protocol version, implementation identity and host capabilities are exchanged before normal requests | Show unavailable state; do not assume rendering or optional APIs |
| Tool result | Structured model-visible fields are intentionally scoped; UI-only payloads use the host-supported metadata channel | Keep secrets server-side; do not treat structured content as private |
| Display mode | The user initiates expansion; the host accepts or rejects the requested mode | Remain usable inline and explain the limitation |
| Context | Settled stable IDs, revision and meaningful filters are published when supported | Do not imply the assistant saw or used a visual click |
| Message | A supported user-initiated message request returns success | Otherwise prepare a clearly labeled copy fallback |
| Write | Server validates authorization, revision and idempotency | Distinguish pending, completed, failed and outcome unknown |
| Teardown | Listeners, polling and media are released | Preserve only declared non-sensitive draft state |

Separate four concerns in the server contract: assistant-only retrieval,
render-linked presentation, external writes and context publication. A search
tool must not gain UI-opening metadata merely because a related browse tool has
a view. Preserve stable object IDs and source revisions across those paths.

For retries, carry an operation ID and reconcile an uncertain result before
submitting again. A JSON-RPC response or host acknowledgment confirms transport
handling only; it does not prove semantic assistant use, saved registration or
publication.

## Implementation record

For a new interface or consequential change, record the applicable fields in the existing project specification or change note; do not create a second ledger for a small fix:

- Task, authoritative object IDs/revision, data owner and write destination.
- Protocol date; exact installed SDK/framework and lockfile; host product, surface, build and relevant account constraints. Package version and protocol date are separate.
- Required versus optional capabilities, requested display modes, acknowledged modes, CSP origins and permission use; useful text/tool fallback.
- State ownership: service data, local draft/selection, model-visible snapshot, historical conversation receipt and durable storage. State lifetime and sensitivity must be explicit.
- Each action's inputs, authorization, validation, irreversible effects if any, receipt and recovery. Record operation ID/deduplication only where repeated writes matter.
- Completed tests and untested host boundaries.

These are application design fields, not an official MCP JSON schema. Share one interaction implementation across sibling widgets; use adapters for domain data rather than copied bridges.

## Context, messages and display

A context update supplies a compact replacement snapshot for future turns; it does not itself request an assistant reply. It may be deferred and later updates replace earlier ones. Settle rapid local changes before a deliberate follow-up, or include the intended snapshot in that supported message. Test that the assistant refers to the current selected ID/revision; a bridge acknowledgment alone cannot establish this. Keep local hover and animation state out of model context.

A message action should name its consequence (for example Send to conversation), snapshot the brief/selection at activation and reject stale async completion after navigation or editing. If sending is unavailable, provide prepared text and a copy action; if rejected, preserve it without implying delivery. Creation prompts identify the destination and actual authoring workflow, then check later save/registration separately.

Apply a requested expanded layout only after the host acknowledges its actual mode. A fullscreen request does not establish a side panel. Missing permission/input may be a waiting state, not a failed tool. Partial streamed arguments may inform provisional display but must not authorize critical operations. Preserve meaningful focus and draft recovery within the host's supported lifecycle; widget-local persistence is not durable service storage. These boundaries also apply when Skybridge hooks abstract the transport.

For an expanded view remount, restore only a minimal non-sensitive intent when a supported mechanism makes it available, re-resolve the ID against current data, and consume or clear it. Storage may be unavailable or isolated across frames. Standalone preview may open local details but must not count as a host expansion acknowledgment. Define whether confirmed send returns to inline and test the actual host response.

Shared components contain no catalog-specific labels, routes or filter logic. Adapters supply object names, optional creation routes, fields, previews and handoff validation. Preview-only controls must not affect filter counts or Clear filters. Use consistent object names across action titles and prepared prompts; the resulting user turn must make sense without the widget beside it.

## Security and admission

Use the installed SDK's transport validation where practical. For a custom bridge, validate message source, negotiated channel/origin behavior, JSON-RPC envelope, request ID, method, schema and result association; bound request lifetimes and ignore unsolicited responses. Sandboxed opaque origins require the actual host contract rather than a guessed origin allowlist. Do not make source/response validation optional merely because a demo posts to `*`.

Render retrieved strings as text or sanitize through a reviewed renderer. Tool results, resource bodies, instruction files and titles remain data, not authority for tool names, destinations or external actions. Validate exact IDs, revisions, authorization and write scope on the server; client checks are UX, not authorization. Keep credentials out of client code, metadata, logs and model snapshots. UI-only metadata is visible to the client and is not secret storage. Minimize payloads and CSP/network permissions; review redirects and embedded origins.

Before adding a framework/skill: inspect the exact source and version, license/notices, install/lifecycle scripts, dependencies, hooks, credential access, telemetry and network behavior. Pin accepted artifacts and preserve notices. A mocked host, a clean static scan or a repository's popularity is not production security evidence. Do not add another agent runtime, tunnel or cloud deployment merely to reuse a pattern.

## Primary references and evidence limits

Checked 2026-10-06: [stable MCP Apps specification](https://github.com/modelcontextprotocol/ext-apps/blob/main/specification/2026-01-26/apps.mdx), [framework-neutral overview](https://modelcontextprotocol.io/extensions/apps/overview), [App context API](https://apps.extensions.modelcontextprotocol.io/api/classes/app.App.html#updateModelContext), [OpenAI UI/state implementation](https://developers.openai.com/plugins/build/chatgpt-ui). Recheck exact signatures against the installed SDK before coding. The specification's best-practice description of structuredContent visibility differs from current OpenAI docs: do not classify it as private across hosts. Source-linked local synthesis from the 2026-10-06 Conversational MCP Widget Design research; no claim of testing every described host.
