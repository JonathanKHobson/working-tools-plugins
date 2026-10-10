# Resolve routes and edition boundaries

Record host-specific observations in your current project. This package contains no personal setup record.

## What Free 21.1.1 supports

Blackmagic's current Studio product page says Resolve Studio includes Python and Lua scripting, developer APIs, remote scripting API and workflow integration plugins. A versioned API reference describing internal launch does not establish Free-edition availability. The community MCP maintainer reports that 21.1 moved Python scripting to Studio and limits its Free bridge to 21.0.x; Free 21.1 Console Python remains unconfirmed. Do not present internal Python as supported on an unverified installation. Lua/Fusion behavior also needs a same-build check before use.

Do not infer that any third-party MCP works because it is installed, appears in a marketplace, or returns a tools list. Check its maintained source and license, configure only the scope needed, then make a live read-only request against the actual Resolve process and inspect the returned project identity. Before mutations, exercise one disposable project and verify save/reopen/render behavior.

## Free-edition fallback

Use Computer Use for direct interaction in the active Resolve window. Internal scripting is conditional on verified edition/build/language support; it is not a proven fallback on Free 21.1.1. For long reviewed assemblies, use the separately installed Video Production Workflow package's timeline interchange export and manually import it in Resolve. Its EDL/OTIO exporters omit audio tracks. Confirm the format on a small disposable or copied project before a large import.

Studio-gated features include external scripting/workflow integration, the official assistant integration/MCP route, Voice Isolation, Magic Mask, Smart Reframe, and other features identified by the current vendor documentation as Studio-only. Verify each effect in the installed UI rather than relying on this list after an app update.

## Sources

- Blackmagic Design, [DaVinci Resolve Studio](https://www.blackmagicdesign.com/products/davinciresolve/studio), current Studio feature listing, accessed 2026-10-10.
- Blackmagic Design support site, [DaVinci Resolve support](https://www.blackmagicdesign.com/support), current support/download landing page, accessed 2026-10-10.
- Resolve scripting reference for 21.1.1, [versioned reference mirror](https://wheheohu.github.io/bmd_doc/ResolveAPI/intro), consulted for distinction between internal and external scripting. Vendor installation is still the authority for exact behavior.
- Verify the installed app bundle documentation on your own host.

- [Community MCP maintainer](https://github.com/samuelgursky/davinci-resolve-mcp#free-edition-in-app-bridge), accessed 2026-10-10: Free bridge limited to 21.0.x; Free 21.1 Python Console unconfirmed. No upstream code installed.
