# ArtCraft Design Toolkit

Current edition **0.2.3** uses the [Compass licensing model](LICENSING.md): first-party code AGPL-3.0-only; first-party docs, prompts, skills, methods and eligible creative templates CC BY-SA 4.0. Upstream grants and prior release permissions remain valid. Author: Jonathan Kyle Hobson.

Use one on-demand MCP gateway to operate the ArtCraft app that fits an editing task. It exposes installed_status, cli_run, open_session, native_tools, native_call and close_session. The complete first-party gateway, skill, app interface reference and protocol tests are included. ArtCraft applications and CLI binaries are installed separately under their own terms.

## First use

Install through the [Working Tools guide](https://github.com/JonathanKHobson/working-tools-plugins/blob/main/docs/install.md). Python 3.10 or later is required. Obtain matching desktop and CLI versions from the [provider](https://getartcraft.com/apps). Arrange CLI executables as `cli/<app>/<app>-cli` beneath your installation root. Set `ARTCRAFT_HOME` or create `~/.config/artcraft-toolkit/host.json` containing `{ "artcraft_home": "/your/install/root" }`. The example is a placeholder, never a credential.

Ask: “Check which ArtCraft CLI apps are installed. Do not launch any apps.” The gateway returns status without starting a native process. Missing apps are a valid result. For actual work, select one app and an existing project folder, open one session, inspect its real tool schemas, save output, inspect it, and close the session. A project folder is not a universal filesystem sandbox.

The portable root manifest and Codex/Claude compatibility manifests launch the same gateway over stdio. A standalone MCP client can use `python3 /absolute/path/to/scripts/artcraft_gateway.py` with the host environment. This is a local service, not a remotely hosted endpoint.

## Validation

Run `python3 -m unittest discover -s tests -v`. The synthetic fixture tests JSON-RPC framing, native image pass-through and child cleanup; it does not prove all seven provider apps work. The repository compatibility record distinguishes synthetic tests from real installed-provider execution.

[The skill](skills/artcraft-apps/SKILL.md) explains the workflow and links to app-specific documentation. LICENSE covers this original gateway and guidance only. PROVENANCE.json records the exact input and exported file hashes.
