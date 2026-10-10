# Writing Voice Library app

Writing Templates owns this read-only MCP app. It reads the retained public, synthetic 48-resource catalog at `library/voice-library/records/catalog.json`. Existing profiles, provisional voice candidates, modules, aliases and merges remain distinct. A selection follows the catalog's actual base and modules; selecting P28, for example, prepares V01 + P28 rather than inventing an independent P28 voice.

## Use and fallback

`browse_writing_voice_library(query="", type="all")` returns compact text and portable metadata with the gallery resource `ui://writing-voice-library/gallery.html`. Valid types are `all`, `legacy_profile`, `voice_candidate`, `module`, `alias` and `merge`.

The gallery shows selectable prose from verified specimen spans, search and type filters, full details, and two or three samples for one shared fictional brief. Feature, workshop and incident briefs are distinct fixtures; their protected facts are available in a disclosure. Six cards appear initially; “Read more voices” reveals the next six. The cream/forest palette and system/Georgia typography require no external fonts, scripts or services.

`prepare_writing_voice_handoff(profile_id, brief, modifier_ids=None)` verifies the selected record, actual base, modules, guide files and examples. Optional modifiers must be registered modules/aliases/merges with the same catalog base; duplicates, unknown IDs, incompatible bases, paths and arbitrary files are rejected. The returned handoff includes the selected classification, versions, catalog and guide SHA-256 values, relative guide references and full verified guide text. It exposes no machine paths. It prepares an instruction package; it does not draft, send, install, generate, deploy or publish.

“Use this voice” calls that tool first, then sends its verified handoff to the host conversation only after a deliberate click and only where the host advertises both server-tool and message capabilities. A source failure sends no message. A rejected/unconfirmed host message leaves a copyable verified handoff and accurately reports its state.

For hosts without MCP Apps, the same HTML is exportable with stdlib Python:

```sh
python3 runtime/writing-voice-library/server.py --export-html /absolute/path/writing-voice-library.html
```

A standalone export can prepare a copyable request to call the validation tool. It cannot claim a current server validation or a sent host message. Public source links target `https://activity-atlas.jkylehobson.chatgpt.site/writing-library/#voice=ID`.

## Runtime and source integrity

The launcher is `scripts/writing_voice_library_mcp.py`. It uses an existing approved MCP-capable Python interpreter when bound locally, or the documented Python fallback with pinned `mcp==1.27.0`; neither path installs dependencies. The private binding stays outside the plugin. MCP mode needs the existing Python SDK/FastMCP; HTML export needs only stdlib. The small JSON-RPC `postMessage` bridge follows the maintained Design Library bridge and checks that incoming messages originate from its iframe parent. It declares no external network capability.

`runtime/writing-voice-library/approved-sources.json` pins the supplied overlay catalog, 48 guides, 144 current example files and shared brief file. The imported source bytes were preserved. File access rejects absolute paths, traversal, symlink components and special files; content is exposed only after matching the approved digest. A changed catalog fails closed pending deliberate source review. Missing/changed guides or samples make a resource unavailable and prevent a handoff. This approved-source manifest is provenance, not a mutable cache; update it only after reviewing an intentional canonical-data change.

Domain checks live in `catalog.py`; MCP/export composition in `server.py`; the self-contained gallery source in `ui/`. Canonical data remains in `library/voice-library`. Plugin discovery/registration stays in the owning manifest and `.mcp.json`.

## Verification on 2026-10-04

Seven unittest checks passed using the existing approved MCP Python. They cover all 48 installed resources, true alias/module routing, compatible and incompatible modifiers, error inputs, portable outputs, traversal/symlinks, stale guides/samples/catalog, actual specimen text, script escaping, and a real SDK stdio session (`initialize`, tool listing/calls, resource listing/read and invalid-ID result).

```sh
PYTHONDONTWRITEBYTECODE=1 /path/to/approved/mcp/python tests/test_writing_voice_library_mcp.py
```

Rendered QA used the exported gallery in the Codex in-app browser at its desktop viewport and a 390 × 844 mobile override. The mobile document measured 375px client and scroll width: no horizontal overflow. Search returned V02 for “warm”; detail showed its actual route, complete selectable prose and public source link. Three incident samples preserved a shared brief while remaining visibly different. The standalone selection produced a copyable request and stated that no host message was sent.

A separate local bridge harness exercised initialization, incoming browse-result filtering, selection validation and message order. A valid P28 selection resulted in one validation call followed by one simulated host message containing `V01 + P28`. A simulated stale-source result produced one call, zero messages and visible failure text. Its mock did not validate message parameters, so it missed the native host incompatibility found later. The reused Python environment emits an existing Pydantic forward-reference warning while protocol checks still pass; no dependency was changed.

The installed native host subsequently rejected the selected handoff with `Invalid MCP message params`. The bridge sent one content object; the installed MCP Apps SDK's `McpUiMessageRequestSchema` requires an array of content blocks. `tests/test_native_bridge_message.mjs` now executes the actual bridge against that installed schema, verifies the former shape is rejected, and checks that an `isError` host result cannot be reported as sent. Source is corrected; installed-host delivery still needs a fresh package and native selection readback.

| Anchor | View and approximate region | Selector | Observed fact and check |
|---|---|---|---|
| W1 | Desktop, top | `header h1` | Serif heading and forest/cream hierarchy are legible; retained design-library visual family. |
| W2 | Desktop/mobile, below heading | `.controls` | Search, type and brief labels remain visible; mobile controls stack without overflow. |
| W3 | Desktop, card area | `[data-id="V02"] .quote` | Real synthetic prose is rendered as selectable text, with exact protected interface wording. |
| W4 | Desktop, selected detail | `#detail` | Actual base/module route and version remain explicit; optional null rhythm is omitted. |
| W5 | Desktop/mobile, compare area | `#compare-grid` | Two/three same-brief columns on desktop; mobile stacks complete incident samples. |
| W6 | Desktop, lower selection panel | `#status`, `#fallback` | Local copyable request, confirmed simulated message and stale-source failure use distinct status text. |
| W7 | Desktop, details source link | `#detail a` | Public URL contains the selected stable ID; no local machine path enters API/UI output. |

## Protocol references

- [Official MCP Apps quickstart](https://apps.extensions.modelcontextprotocol.io/api/documents/Quickstart.html): tool + HTML-resource registration.
- [MCP Apps draft specification](https://github.com/modelcontextprotocol/ext-apps/blob/main/specification/draft/apps.mdx): `ui/initialize`, capabilities, `tools/call`, `ui/message`, tool results and teardown.
- Maintained UX Design Studio `docs/design-library.md` and `runtime/design-library/`: working local FastMCP/export and bridge contract reused conceptually.


Collection-dependent history and commands describe the maintained source-owner collection. Its bodies and private integrity pins are excluded from public distribution. Bind your own authorized collection before running those commands; the fresh public runtime uses its documented fixture or included eligible kits.
