# Install one package

Choose a package from the README and check its prerequisites. The plugin supplies instructions and any declared local runtime. Provider accounts, apps and host tools are separate.

## Codex desktop and CLI

Use a current Codex version with plugin marketplace support. In a terminal:

```sh
codex plugin marketplace add JonathanKHobson/working-tools-plugins
codex plugin list
codex plugin add stitch-design-studio@working-tools
```

Replace `stitch-design-studio` with the package you chose. Open a fresh chat after installation and ask what that package does. In the desktop app, choose the Working Tools marketplace in Plugins; a restart can be needed after registering a marketplace. The desktop shares the supported local plugin format with Codex CLI, but see the compatibility record for exactly which surface was tested.

The separate `working-tools` marketplace does not update an existing `personal` installation. If you maintain your own edition, choose the intended source and avoid invoking duplicate skill names without a namespace.

## Claude Code

```sh
claude plugin marketplace add JonathanKHobson/working-tools-plugins
claude plugin install stitch-design-studio@working-tools
```

Restart the session after installation. These packages use Claude's plugin/skill format; browser, Figma and local app tools must be supplied by the host. A Claude Code install is not an upload into Claude's web interface.

## Download without a marketplace

Download a versioned ZIP and its checksum from [Releases](https://github.com/JonathanKHobson/working-tools-plugins/releases). Extract into an empty folder. On macOS/Linux, compare `shasum -a 256 PACKAGE.zip` with the release checksum. Review the package README and notices before running it. Each ZIP has its plugin manifest at the archive root. Keeping the entire extracted directory preserves skill references; copying only SKILL.md usually does not.

## A first task

For Stitch, ask: “I have no Stitch session open. Explain what input and access you need to refine a screen, and give me one small first task.” A correct result explains prerequisites without claiming a design was created. With access available, supply one screen, its task, content and source references.

For Artcraft, ask the gateway for `installed_status`. It should return each CLI's availability without launching an app. Then use one installed app on a disposable project. Missing provider software is reported, not silently installed.

Video's package README includes an executable synthetic sample. Resolve and Figma guidance require the actual target app/project for a live operation; a planning response is not evidence of a saved design or timeline.

## Update, disable and remove

For Codex, run `codex plugin marketplace upgrade working-tools`, then reinstall the selected package with `codex plugin add PACKAGE@working-tools` if the installed version has not refreshed. Check `codex plugin list` and the installed manifest. Pin the marketplace to a release ref for repeatable environments: `codex plugin marketplace add JonathanKHobson/working-tools-plugins --ref PACKAGE/vVERSION`.

Disable a Codex package in the Plugins UI or use `enabled = false` in the documented project plugin configuration. Remove it with `codex plugin remove PACKAGE@working-tools`. Remove the marketplace with `codex plugin marketplace remove working-tools` when no longer needed. These operations do not uninstall provider apps or delete your projects.

For Claude, use `claude plugin update PACKAGE@working-tools`, `claude plugin disable PACKAGE@working-tools` and `claude plugin uninstall PACKAGE@working-tools`. Confirm current CLI help when using an older host.

## Troubleshooting

- Marketplace not found: confirm the repository URL, client version and network access; run marketplace list.
- Skill absent: open a fresh session and check the package source and enabled state.
- Missing provider: install/configure the provider separately under its own terms; keep the task pending until access is verified.
- Local MCP cannot start: check Python on PATH and the installed plugin root; run the gateway's documented direct stdio command.
- A package update changes behavior: pin a prior namespaced tag and reinstall; retain your projects separately from the install cache.
- Never paste credentials, personal documents or full machine configuration into an issue. Use a synthetic reproduction and [support guidance](../SUPPORT.md).
