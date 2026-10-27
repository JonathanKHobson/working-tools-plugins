# Activities Templates

Current edition **0.1.3** uses the [Compass licensing model](LICENSING.md): first-party code AGPL-3.0-only; first-party docs, prompts, skills, methods and eligible creative templates CC BY-SA 4.0. Upstream grants and prior release permissions remain valid. Author: Jonathan Kyle Hobson.

Find an activity or reusable method, inspect its source and review status, and adapt it through the relevant studio. This package owns the catalog runtime and human chooser. Workshop Facilitation owns running a session; UX, Instructional Design, Career and other studios own their production workflows.

Try “Find a remote activity for eight people in fifteen minutes” or “Find a research synthesis method for this evidence.” Supply the purpose, audience, time and delivery mode when they affect selection. The result is a small set of inspectable candidates or a selected guide with an adaptation rationale. Search alone does not establish effectiveness.

The single discovery entrypoint is [activity-library](skills/activity-library/SKILL.md). [Catalog use](references/catalog-use.md) gives the complete retrieval/adaptation and private-feedback contract. [Setup](references/setup.md) explains required external data and Python dependencies, their absent state, and harmless verification.

## Data and rights

This public edition includes the complete first-party runtime and chooser. The private Atlas vault and SQLite catalog are external dependencies. Neither is included. The public editorial edition is a separate 461-guide projection; [its source register](library/public-edition.json) records the inspected edition and redistribution hold. Public availability is not a blanket license. The register contains no guide bodies or private paths. No network request, automatic download, rebuild, publication, watcher or telemetry runs at startup.

## Runtime ownership

Twelve existing `atlas-*` server IDs and their search/browse/read tools and resource URIs are preserved in [.mcp.json](.mcp.json). Each server launches a fixed view; tools cannot change its domain. A record can legitimately belong to several views. `domains.json` retains the existing visualization definition without adding a thirteenth registration. Whole-Atlas `knowledge_atlas` remains separately owned and configured.

[Source provenance](SOURCE-NOTES.md) identifies the code migration and unchanged/adapted files. [Project map](docs/project-map.md) locates the launcher, runtime, UI, bindings and tests. Installation and source preparation are separate states; serialized cutover must remove each predecessor registration only after this owner is installed and checked.

## Public first use

Install through the Working Tools repository guide. Use a Python 3.10+ environment and install requirements.txt. To exercise the actual runtime without private data, run that interpreter with `scripts/create_sample_catalog.py --output <empty-external-folder>`, then set ACTIVITIES_ATLAS_CONFIG to the emitted binding file. The generated notes are explicitly authored synthetic fixtures, not the private guide collection or evidence of method effectiveness. Enable the plugin only after configuring the selected interpreter and data binding. The stock host python3 bootstrap executes that selected environment before loading the MCP server.

Run the selected interpreter with `-B -m unittest discover -s tests -v`. The tests execute all twelve fixed-domain stdio registrations, verify tools and real resources, retrieve complete synthetic source bodies, reject foreign-domain IDs and preserve the catalog bytes. Set ACTIVITIES_BOOTSTRAP_PYTHON to the stock host Python to test that bootstrap route. Source preparation, native installation and live-host widget acceptance remain separate states.

## Local transport efficiency patch

On supported Unix hosts, the launcher automatically connects to a private backend for its fixed domain, code generation and external bindings. Several chats can share SDK imports while retaining separate MCP sessions and exactly the same tools and chooser resources. No user toggling is required. Catalog reads remain read-only; feedback still writes only when explicitly requested. Blocking work runs off the shared event loop. Each proxy uses bounded queues and only accepts an owned private socket; no network listener is opened.

Backends start when needed and retire after all client connections close and 60 idle seconds pass. Low CPU and process age never trigger termination. A backend failure affects connections for that domain/generation; other domains use separate processes. Failed requests are surfaced, never silently replayed. A later new connection can start a replacement. Existing processes are not hot-reloaded. Keep their code/resource files available until their owners finish.

The first connection pays for both the small proxy and the backend. Savings grow when several sessions use the same domain, as in the measured replicated-server workload. Process count alone is therefore not the acceptance metric. Measure aggregate footprint, preserved contracts and responsive behavior. `ACTIVITIES_TRANSPORT=direct` retains the original SDK path for operator rollback and unsupported platforms retain that path; ordinary use needs neither switch. Tests may override `ACTIVITIES_BACKEND_SOCKET_DIR` and `ACTIVITIES_BACKEND_IDLE_SECONDS` to isolate short-lived fixtures. Production defaults require no LaunchAgent, scheduler or AI monitor.

## Optional private usage measurement

When a recipient enables `~/.config/studio-tools/usage-tracking.json`, registered MCP tool handlers can emit one metadata-only completion event through its configured recorder. Missing/disabled tracking does nothing; recording failure never changes tool output. No arguments, results, accounts, catalog content or raw session IDs are logged. The observer runs in the existing tool process with no model call, polling or extra service. Fresh connections load code updates; preserve active shared connections until a normal reload. Internal helper reuse is not counted twice. The private recorder owns aggregation and any exclusion needed to avoid overlapping native-hook counts.
