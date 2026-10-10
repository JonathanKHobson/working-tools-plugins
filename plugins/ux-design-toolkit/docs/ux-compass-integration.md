# UX Heuristic Compass integration

UX Design Studio owns UXHC methods through `skills/ux-heuristic-compass/` and packages a small stdio bridge. The canonical server and its private outputs stay outside the plugin.

## Local launch

Portable `mcp.json` discovers `scripts/compass_mcp.py ux-heuristic-compass`; Codex compatibility retains `.mcp.json`, and the public Claude manifest declares the same server with `${CLAUDE_PLUGIN_ROOT}` so its script resolves inside the installed plugin. The launcher reads `~/.config/studio-tools/compass.json`; configure the `ux-heuristic-compass` entry with absolute `interpreter` and `server` paths. Preserve the virtualenv Python entrypoint, rather than resolving its symlink to a base Python. The bridge does not install or download a backend. Missing mounts or bindings fail with a setup message.

The verified ARM Python 3.12 runtime carries `mcp==1.27.0` and `reportlab==4.5.0`. Keep the virtualenv, private binding, and source/data checkout outside distributable bundles. The server uses stdio; it has no persistent HTTP listener, OAuth, resources, prompts, or sampling route. Reload the host session after installation so its tool catalog refreshes.

## Allowlisted tools

All 18 existing public tools remain exposed: `get_started`, `ux_heuristic_overview`, `list_heuristics`, `prepare_ux_source`, `quick_scan_ux`, `audit_ux_surface`, `validate_ux_report_payload`, `generate_ux_audit_report`, `calibrate_ux_sensitivity`, `calibrate_ux_severity`, `compare_ux_audits`, `draft_project_addon_profile`, `save_preferences`, `update_preferences`, `run_agent_audit`, `get_agent_run`, `run_usability_test`, and `stress_test_heuristic_finding`.

Choose the smallest output: `get_started(topic="brief")` for ordinary startup, default `get_started()` for deeper startup contracts, `get_started(topic="tools")` for all tool contracts, `list_heuristics(detail_level="brief")` for routing, `summary` for descriptions, `full` for checklist IDs/text, and `quick_scan_ux(output_detail="guidance_only")` for unscored direct-fix guidance. `audit_ux_surface` defaults to a status-only response; use saved payload refs and report validation before generation. The MCP Python SDK provides `structuredContent` and inferred `outputSchema` for all tools. Full contracts remain available on demand even though the default startup response omits their repeated prose.

## Measured stdio baseline and result

Measured with the same Python SDK client against `server.py` via initialize, tools/list, and tool calls. Byte counts serialize JSON without whitespace; call counts include the SDK's text block plus structured content. The probe is at `work/design-merge/uxhc_mcp_probe.py` in the Managing My Computer task workspace.

| Response | Before | After |
| --- | ---: | ---: |
| `tools/list`, 18 tools | 30,541 B | 20,033 B |
| Tool descriptions within list | 13,799 B | 3,291 B |
| `get_started()` | 67,642 B | 36,533 B |
| `get_started(topic="tools")` | 98,819 B | 67,710 B |
| `list_heuristics(detail_level="summary")` | 46,786 B | 46,786 B |
| New `list_heuristics(detail_level="brief")` | — | 7,662 B |

Tests: 94 passed with the ARM venv first in `PATH`, because two existing subprocess tests call `python3` and the system shim is blocked by an Xcode license prompt. Direct MCP calls returned 18 tool names, non-error `structuredContent`, and 18 inferred output schemas. Source bundles and installed plugin caches are separate; test the configured Codex host after manifest wiring and reload.

## Capability and data boundary

`prepare_ux_source(capture_urls=true)` can fetch up to 10 explicit URLs and may launch an isolated Chrome capture; URL capture is off by default. It is not a crawler or authenticated browser agent. Other calls can write local run summaries, preferences, checkpoints, or report artifacts, depending on the tool and arguments. Reports, screenshots, private URLs, traces, state, caches, and `.env` files stay out of public bundles. Report generation requires evidence references, heuristic ID, severity, recommendation, confidence, and readiness validation. Synthetic personas/walkthroughs are not participant evidence. The host owns visual interpretation and must cite screenshot regions, DOM/text cues, viewport or observed interactions for findings.

Review the command, 18 names, schemas, descriptions, dependencies, optional URL/network behavior, and local output paths whenever this fingerprint changes. This integration does not request background service, token, browser profile, Keychain, or cloud access.
