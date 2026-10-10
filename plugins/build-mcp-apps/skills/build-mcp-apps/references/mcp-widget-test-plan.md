# MCP widget technical test plan

This is a focused contract checklist, not a universal usability scale. Record
host, surface, build, viewport, SDK/framework version and capability flags.

- Initialize with the real protocol version and assert the initialized
  notification; test version mismatch and unavailable host behavior.
- Exercise a view with complete, empty, partial and error tool results without
  treating partial input as safe for critical writes.
- Deny fullscreen, message, context, file and tool capabilities one at a time;
  verify each honest fallback and that no unsupported request is emitted.
- Confirm AI-only search returns structured data without view metadata, while a
  deliberate browse/presentation tool opens the view.
- Change selection/filter state, publish a settled context snapshot where
  supported, then verify the next supported turn receives stable IDs and current
  revision. Test remount as best-effort recovery, not a guarantee.
- Test duplicate activation, timeout after backend commit, stale revision,
  authorization expiry and partial batch writes. Verify idempotency and
  outcome-unknown reconciliation before retry.
- Test keyboard, touch, narrow layout, enlarged text, theme change, reduced
  motion, teardown and non-hover equivalents. Browser or VM evidence does not
  substitute for the claimed real host.
- Verify message content shape and rejection. Label prepared, copied, sent,
  pending and failed states accurately; never claim that a prompt changed an
  artifact without authoritative evidence.

Record the tested path and the untested host boundaries in the release note.

## Admission regressions from external examples

Before adapting a downloaded “production-ready” template, check these concrete failure cases against the installed SDK:

- The App initiates `ui/initialize`, validates the reply and then sends the initialized notification. A view that merely waits for the host to initialize it is not proof of a working lifecycle.
- Validate request versus notification forms and typed content blocks for messages/context. Register response handling before dispatch; reject unknown IDs and bound pending requests. A fire-and-forget message cannot support a “sent” receipt.
- Return a tool `isError`, an application-level rejection, a missing required confirmation ID and an ambiguous timeout. None may become “Confirmed” through a default string or transport success.
- Render quote-containing and markup-like record fields as text. Do not interpolate API data into `innerHTML` or inline event handlers.
- Validate resource CSP metadata against the protocol schema. Raw browser directive names such as `scriptSrc` are not substitutes for the MCP Apps origin fields `connectDomains`, `resourceDomains`, `frameDomains` and `baseUriDomains`. Verify enforcement in the claimed host.
- Treat custom CSS token names as adapters, not standard host variables. Verify theme changes, fallback contrast, enlarged text and content sizing without clipping or an unbounded resize loop. A border preference is a hint, not evidence that the host supplied one.

These cases were identified in a supplied October 2026 research supplement; its code was withheld from installation. A static scanner reported no actionable findings while manual review found injection and false-confirmation paths. Both results belong in an admission record.

## Reference fidelity and host acceptance

- Compare 3–8 named rendered anchors with the accepted reference at the same viewport/theme. Check loading, empty, error and open overlays for unexpected frame growth, clipping and hidden controls; permit necessary accessible reflow rather than requiring constant height at all text sizes.
- Exercise denied expansion, same-instance expansion and a fresh expanded instance when the host supports it. Confirm selection and return behavior; record unavailable persistence honestly.
- Trace visible badges, previews, counts, filters and actions to real fields or supported routes. Check sibling adapters preserve shared topology without hard-coded domain strings.
- Test separate primary/secondary card targets, Escape and dismissal appropriate to the overlay pattern, sibling overlay behavior, and focus returning to a still-present control. Do not impose menu semantics on every disclosure.
- Mark source/harness/render completion as a locally verified candidate. Claim acceptance only for the host/build and paths actually exercised. A screenshot approval does not prove delivery, remount or persistence.

For asynchronous handoffs, change selection/brief or navigate back while the message response is delayed. The old response must not overwrite the new view, clear its intent or collapse it; a stale button cleanup must not disable the new action. Return keyboard focus to a visible control after a successful handoff. Teardown must reject outstanding requests, release observers/listeners, reject later requests and ignore late replies; test request ID zero as well as positive IDs. Protocol-version mismatch and malformed response envelopes must not produce success.

## Live release freshness

After changing a server, view resource or tool metadata, verify three distinct layers: canonical source, installed package and the existing host connection. A fresh subprocess smoke test can pass while a long-lived server still holds an older renderer or tool schema.

1. Read the view resource through the actual connected server. Check for errors and identify the expected revision using a release identifier or distinctive changed markup. Do not interpret a truncated tool response as full resource size or hash parity.
2. Inspect the live tool contract: AI-only search must remain free of view metadata and the intended browse tool must expose the current resource. A source declaration alone is insufficient.
3. If live behavior disagrees with installed bytes, inspect process/connection freshness and cached resource identity before redesigning or deleting implementation files. Use a supported reconnect/reload; if the host requires a user restart, explain the concrete stale-connection evidence. Do not kill unrelated services or bypass restricted host controls.
4. After refresh, repeat the live resource check, invoke a fresh browse instance, and inspect its rendered anchors against the accepted design. Historical chat cards may retain old snapshots; distinguish them from the newly invoked instance. Never claim old chat records were replaced or deleted without a supported operation and readback.
5. Record resource loading, visible design approval and exercised interactions separately. A successful browse call is not proof that the host rendered the widget, and appearance approval does not prove send, copy, expansion or persistence.

For a text-only skill update, verify changed guidance and installed parity; do not restart healthy MCP connections or rerun unrelated visual tests solely because the text discusses widgets.

## Default dark theme regression

For Kyle-owned widgets, verify neutral black/white/gray dark chrome unless another design is explicitly requested; preserve user content colors. Test explicit host dark and light, omitted theme with system fallback, and live theme changes. Measure rendered foreground/background contrast for title, metadata, enabled/disabled buttons, inputs/placeholders, tables and SVG labels; inspect nested editor chrome separately. Set paired background and foreground tokens so a transparent host surface cannot leave dark text on dark. Use the UX conversational-widget theme guidance as the design owner.
