## Login-Item Launch Race

If a desktop app starts too early at login and depends on external-drive MCPs:

1. Remove it from Login Items first.
2. Reboot with the app closed.
3. Mount the external drives.
4. Launch the app manually and confirm the MCPs attach.
5. If the app still fails after manual launch, inspect the MCP logs before
   changing the server config.
