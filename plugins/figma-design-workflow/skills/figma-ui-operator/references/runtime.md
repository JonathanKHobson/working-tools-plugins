# Runtime and capability boundaries

## What this skill supplies

This folder provides Figma-specific operating judgment, not a mouse driver, account connection, model selection, or permission grant. Inspect the tools available in this session. A model name does not establish GUI access. No installation or account changes are required merely to read the skill.

## Codex computer-use entry points

When `mcp__cua_repl.js` is available, its current tool contract owns runtime initialization. On the first call or after reset, execute exactly one documented entry call and read the returned documentation before any additional actions:

- Known desktop app: `let figmaApp = await cua.getApp("Figma");`
- Need a surface inventory or user-mentioned tab: `await cua.getState();`
- Then select a discovered existing tab with `cua.getTab` using the actual tab and browser IDs according to the returned contract.

These are entry points verified against the tool schema on 2026-09-09, not a replacement for that schema. Do not copy raw API examples from old recordings into a new runtime. Subsequent screenshot, accessibility, click, key, drag, and browser methods must come from the returned documentation. Reuse session bindings and reacquire invalidated element references.

A separate Computer Use skill is not a blocker when the runtime already supplies its operating instructions. Conversely, installing this skill does not prove input or screenshot capability. Do not use voice-only screen-capture tools in a text task. Avoid opening or controlling the app just to validate this skill's packaging.

Identify OS, keyboard layout, browser versus desktop, application bounds, UI scaling, canvas zoom, mode, and actual file/page. Scope capture to the relevant app when supported. Another active task or human using the same foreground surface must finish or hand off control before this task sends competing input.

## Choose the route from the request

- Explicit UI/computer-control work: operate the authorized desktop window or existing browser tab. Read-only connector evidence may supplement inspection if the user permits it; do not represent it as UI execution.
- General Figma write where UI was not specified: a purpose-built Figma connector may be preferable. Use the installed `figma-use` guidance before `use_figma`; use design-to-code guidance before design-context implementation tools. This UI skill does not override their prerequisites.
- UI requested but only connector/API tools available: report the missing visual/input capability. Do not silently substitute plugin code.
- Already authorized mixed UI/API work: respect any preference to limit API calls. Reuse scoped node inventories and avoid repeated broad scans. A quota failure is a reason to inspect the exact error and use an already authorized UI route, not loop the API or switch accounts. Follow tool-required account diagnostics when applicable.

For Stitch or HTML clipboard transfer, the destination is the user's authorized Figma editor, which may be an existing browser tab or the desktop app. A clipboard workflow does not require switching to the native app. Resolve model and surface preferences before input, verify that the selected operator can actually access that surface, and keep the destination file/page grounded. A delegated worker's model name does not prove access to the main chat's visible browser tab. If the requested route is unavailable, report the capability gap instead of silently changing model or surface.

## Evidence and access

Use actual screenshots and visible UI state for interaction, plus Layers/properties for structure. A connector's node inventory can corroborate editability, but tool availability alone cannot. Never extract authentication tokens, clipboard payloads, browser storage, or unrelated private files to repair a transfer. Preserve any structured clipboard data by avoiding text-only clipboard replacement.

Pause input for human login/security challenges or required permission decisions. Do not change OS access settings, install automation libraries, or relaunch Chrome with debugging flags to force an unavailable route. Preserve unsynced work and report the exact blocked step.

## Handoff and cleanup

Restore only temporary selections/context and leave the requested result at a useful view. If the user completed part of the work, inspect what landed and continue from the actual state.

When Chrome automation was used on Kyle's Mac, release this task's automation handles and close its automation-owned tabs/windows/session and parent daemon when applicable. Verify process ownership and startup arguments. Finish with either no automation Chrome session or the normal visible Chrome app without headless, temporary-profile, Playwright, or remote-debugging arguments. Do not terminate another active task's session or ordinary user tabs. If ownership prevents cleanup, report that concrete handoff limitation.

If an MCP was enabled specifically for the task, restore its prior setting unless the user asked to leave it enabled. Preserve baseline MCPs. Do not disable connectors that were already available just because this skill used them. Historical recordings supply route clues, not current selection, permissions, or proof of this run.
