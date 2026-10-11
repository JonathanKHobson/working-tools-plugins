# Changelog

## 0.1.4

Reduce repeated catalog-server memory while preserving all twelve domain contracts.

Several chats previously loaded separate SDK copies for the same catalog domain. The included transport shares imports per domain, code generation and binding while retaining independent sessions.

Adds an on-demand private Unix-socket backend and bounded stdio proxies. Validates socket ownership, isolates domains and bindings, runs blocking handlers off the shared event loop, drains pending responses and retires an unused backend. Failures are surfaced without replaying writes. Direct SDK transport remains the compatibility and rollback path; existing processes continue their own generation. No schedule or AI monitor is introduced.

Compatibility: Compatible internal transport correction. Existing server IDs, tools, schemas and resources remain unchanged; non-POSIX hosts retain direct SDK transport.

Upgrade: Update Activities Templates using its existing installation method. Keep the configured interpreter and external catalog binding. Existing connections are not hot-reloaded.

Validation: All eight admitted source hashes match the completed14-test runtime/lifecycle/contract-parity receipt. Tests cover all twelve registrations, synthetic retrieval/resources, private socket modes, cancellation, EOF, isolation and recovery. No private corpus is packaged.

## 0.1.3 · 2026-10-10

Align the maintained local source and portable package, preserving complete operative methods and original source history. Refresh recipient setup, registration metadata and file-level provenance.

## 0.1.2

Apply the Compass license model to this new edition of first-party contributions. Preserve all earlier grants and unchanged upstream notices. Add explicit file scopes, attribution and reserved-mark boundaries. Operative method, helper and runtime bodies are unchanged.

