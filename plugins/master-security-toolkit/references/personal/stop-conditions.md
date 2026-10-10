## Stop Conditions

Stop and ask before proceeding if the next step would:

- run an unknown installer, script, package lifecycle hook, MCP server, or
  binary
- grant Accessibility, Full Disk Access, Keychain, browser profile, SSH, cloud,
  wallet, password manager, or vault-level permissions
- wire an unreviewed MCP/plugin into Claude, Codex, or another always-on client
- expose private local data to a remote service
- enable broad network access for Codex or another agent
- require disabling Gatekeeper, SIP, quarantine, or other security controls
- add a persistent background service, LaunchAgent, LaunchDaemon, login item,
  shell profile hook, or auto-updater
- approve an MCP/server update with changed tool descriptions, schemas, launch
  commands, versions, packages, binaries, permissions, or network destinations
