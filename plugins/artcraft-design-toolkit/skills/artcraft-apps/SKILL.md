---
name: artcraft-apps
description: Use the installed ArtCraft creative apps for image, vector, video, photo-library, PDF, motion-graphics, or page-layout work, including their CLI or native MCP interfaces when the task needs them.
---

# ArtCraft apps

Choose the one app that fits the current deliverable. PhotoCraft edits images; VectorCraft draws vectors; FilmCraft edits video; LightCraft manages and develops photos; PdfCraft works on PDFs; EffectCraft makes motion graphics; DesignCraft lays out pages. Existing design and video studios still own the creative brief, source fidelity, and rendered review; use ArtCraft as the editing surface when it helps produce their deliverable.

Find the installed desktop app and matching separate CLI on the current host. `ARTCRAFT_HOME` may identify the install root; otherwise use the host's known install location and its installation/verification report, if available. Verify the real path, release version, architecture, checksum/signing record, and `<app>-cli --help` before choosing a command. Never assume a web page's version or a path in this source tree proves installation. Keep source media, libraries, projects, exports, and renders in the owning project on its intended drive. Use an app's documented library, data, root, or config flag where available; an external app bundle alone does not relocate its settings or logs.

Read [app interfaces](references/app-interfaces.md) for **only the selected app**. The plugin's `artcraft-toolkit` gateway exposes `installed_status`, `cli_run`, `open_session`, `native_tools`, `native_call`, and `close_session`. Prefer `cli_run` for a bounded transform. For a persistent session, call `open_session` with one app, `mode` (`headless` or `live`), and an existing writable `project_root`, then inspect real schemas with `native_tools` before `native_call`. The gateway starts only that app's native CLI MCP server; `close_session` ends it. Live mode connects to an already-running app and exposes its window tools where supported. Save work and close a session explicitly before switching apps. Treat a CLI result as operation evidence, and inspect the saved or rendered artifact before calling visual work complete.

Discover command IDs, schemas, and installed-version differences through the CLI (`commands`, `tools`, `describe`, or help as appropriate). Use a small sample or copy before touching valuable source files. The gateway does not assert native autosave outside app-specific flags. Keep task-started desktop control listeners temporary. Respect the current task's authorization for editing and output; publishing a result is a separate action when requested.

For Computer Use, bind the actual installed bundle identity. If first binding times out, inspect the already-running app before restarting it. A blank inactive GPU window is inconclusive: activate its observed title bar and inspect again. Verify the changed document and saved output, not merely the window title. `project_root` supplies working/storage defaults; it is not a universal filesystem sandbox for native tools.
