# Install one package

Choose a package from the README and check its prerequisites. The plugin supplies instructions and any declared local runtime. Provider accounts, apps and host tools are separate.

## Codex desktop and CLI

Use a current Codex version with plugin marketplace support. In a terminal:

```sh
codex plugin marketplace add JonathanKHobson/working-tools-plugins
codex plugin list
codex plugin add stitch-design-studio@working-tools
```

Replace `stitch-design-studio` with the package you chose. If the full checkout is slow, use the [selected-package checkout](#slow-marketplace-refreshes) below. Open a fresh chat after installation and ask what that package does. In the desktop app, choose the Working Tools marketplace in Plugins; a restart can be needed after registering a marketplace. The desktop shares the supported local plugin format with Codex CLI, but see the compatibility record for exactly which surface was tested.

The separate `working-tools` marketplace does not update an existing `personal` installation. If you maintain your own edition, choose the intended source and avoid invoking duplicate skill names without a namespace.

The marketplace identifies the installation source. A skill uses its package namespace: for example, `figma-design-workflow:figma-ui-operator`, not `working-tools:figma-ui-operator`. A fresh chat should list the selected skill and its installed package path. If several editions are installed, verify the path before running it.

## Claude Code

```sh
claude plugin marketplace add https://github.com/JonathanKHobson/working-tools-plugins.git
claude plugin install stitch-design-studio@working-tools
```

The explicit HTTPS URL avoids relying on GitHub SSH-key access. If an earlier shorthand add failed with `Permission denied (publickey)`, retry with this URL and inspect `claude plugin marketplace list` before installing. No global Git URL rewrite is required. A [selected-package checkout](#slow-marketplace-refreshes) can avoid downloading unrelated source packs.

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

For Claude, use `claude plugin update PACKAGE@working-tools`, `claude plugin disable PACKAGE@working-tools` and `claude plugin uninstall PACKAGE@working-tools`. Keep the original installation scope, such as `--scope local` for a local install. Repeating `install` can leave the installed version unchanged even after the marketplace offers an update. Read the command result and verify the installed version. Confirm current CLI help when using an older host.

## Slow marketplace refreshes

The repository includes complete methods and source packs, so its full Git checkout can take several minutes. Full refreshes have timed out on the maintainer Mac. A timeout is not an installed update; inspect the installed version before retrying.

For a new marketplace registration, fetch the marketplace manifest and only the package you want. These commands acquired Research Toolkit through both native managers with all 103 package files intact:

```sh
codex plugin marketplace add JonathanKHobson/working-tools-plugins --ref main --sparse .agents/plugins/marketplace.json --sparse plugins/research-methodology-local
codex plugin add research-methodology-local@working-tools
```

```sh
claude plugin marketplace add https://github.com/JonathanKHobson/working-tools-plugins.git --sparse .claude-plugin plugins/research-methodology-local
claude plugin install research-methodology-local@working-tools
```

Replace `research-methodology-local` in both the path and install command to choose another package. Add each additional package path with another `--sparse` in Codex, or after the existing `--sparse` in Claude. The checkout contains only those named paths; listing a package in the marketplace does not prove its source was fetched. Use an intended release ref instead of `main` for a pinned Codex snapshot.

An existing marketplace may reject registration with different sparse paths. Record its source, ref, paths, installed versions and scopes before changing it. Re-register only the `working-tools` marketplace when those settings can be preserved; do not remove another source or project files. Check the installed manifest and open a fresh session afterward.

Claude also supports a longer fetch timeout with `CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS=300000 claude plugin marketplace update working-tools`. It has succeeded on earlier snapshots, but a longer timeout does not guarantee a full checkout will finish. Keep the original scope when updating an installed package. A versioned ZIP remains available when native acquisition is unavailable.

## Troubleshooting

- Marketplace not found: confirm the repository URL, client version and network access; run marketplace list.
- Skill absent: open a fresh session and check the package source and enabled state.
- Missing provider: install/configure the provider separately under its own terms; keep the task pending until access is verified.
- Local MCP cannot start: check Python on PATH and the installed plugin root; run the gateway's documented direct stdio command.
- A package update changes behavior: pin a prior namespaced tag and reinstall; retain your projects separately from the install cache.
- Never paste credentials, personal documents or full machine configuration into an issue. Use a synthetic reproduction and [support guidance](../SUPPORT.md).
