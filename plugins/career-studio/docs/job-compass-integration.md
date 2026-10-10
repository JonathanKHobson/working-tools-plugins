# Job Application Compass integration assessment

Job Application Compass (JAC) is an existing private local stdio packet engine. Career Studio keeps its generic, shareable skills and private workspace boundary. Do not bundle JAC source, personal defaults, application records, or an MCP config with machine-specific paths into the shared plugin.

## Useful private runtime lane

For an operator-owned private application packet when current source authority has been checked, these exact tools add deterministic behavior beyond the Career Studio writing skills:

1. `parse_job_description(job_text=...)` — structure a supplied listing without reading the profile.
2. `validate_evidence_profile(profile_path=..., source_register_path=...)` — check evidence IDs, confidence tags, source tiers and archive-only rules. Pass explicit reviewed files; defaults point to the private JAC project.
3. `map_job_to_evidence(job_text=..., profile_path=..., source_register_path=...)` — distinguish supported requirements from gaps. It reads private evidence, so use only in an authorized private packet workflow.
4. `prepare_application_packet(job_path=..., output_dir=..., profile_path=..., source_register_path=...)` — generate six local packet files from one reviewed role and evidence set. The host still writes and reviews final prose.
5. `validate_application_packet(packet_dir=...)` — verify a prepared packet before handoff.

`prepare_manual_apply_assistant` can help with a pasted employer form after a packet exists, but it creates copy-paste seeds, not a submission or receipt. `prepare_ats_pdf_export` is a separate local render step after final prose. `scan_public_job_sources` plans by default and fetches only with `confirm_fetch=True`; it is outside the core packet path. `get_agent_playbook`, `route_application_task`, and `search_method_index` are mostly method/routing scaffolds already covered by Career Studio skills. Personal profile update, retirement, and job-hunt update tools remain private explicit workflows; their `confirm=True` gates do not justify automatic invocation.

## Local launch and exposure

An operator's private local configuration can launch the existing server with:

```text
command: <private-jac-venv>/bin/python
args:    <private-jac-source>/server.py
env:     PYTHONDONTWRITEBYTECODE=1
```

The reviewed runtime used Python 3.12.13 with MCP SDK 1.27.0 over stdio, with no persistent HTTP listener or OAuth. The server sets `ROOT` to its source directory, and several tools default to private profile, source-register, and portfolio files under that root. Make activation an optional operator-local runtime configuration, with explicit file paths on private calls. Keep it out of distributable Career Studio bundles. Do not copy the 29-tool server into the plugin or launch a second duplicate service.

The current MCP advertises 29 tools; `list_tool_surface(include_write_tools=false)` only changes a returned inventory. It does not remove write tools from MCP `tools/list` or enforce an allowlist. If a host needs a hard five-tool surface, it requires a reviewed server-side wrapper or protocol filter; skill text alone is a routing convention, not an access control. Avoid adding that infrastructure merely for this integration without a concrete packet need.

## Live and synthetic checks

Direct stdio initialize and `tools/list` succeeded with 29 names, 29 inferred output schemas, and structured content on each tested call. Serialized `tools/list` was 23,078 bytes, including 7,093 bytes of descriptions and 10,863 bytes of input schemas. `get_started()` was 38,676 bytes; `list_tool_surface(include_write_tools=false)` was 103,168 bytes and is too large for routine discovery. A supplied fictional UX research job parsed successfully in 6,736 response bytes and routed to `full_application_packet` in 18,129 bytes. An in-memory synthetic evidence fixture passed with two stable IDs; changing an archive-backed claim to `current` blocked it with `archive_promoted_without_review` and `current_without_primary_source`.

The local integration audit holds the probe and aggregate receipts outside this plugin. No real profile, personal answers, application record, employer form, source-candidate index, or portfolio truth bank was read for these checks. No packet, send, submission, publication or personal-data mutation occurred.

JAC source policy requires local stdio only, confirmation before personal-layer writes, source-tier validation, and a privacy scrub before any public package. Its AGPL-3.0-only source and personal defaults reinforce keeping runtime code in its owning private project while Career Studio carries portable methods.
