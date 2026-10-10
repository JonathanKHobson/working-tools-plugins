# Mac Operations Toolkit

Current edition **0.3.3** uses the [Compass licensing model](LICENSING.md): first-party code AGPL-3.0-only; first-party docs, prompts, skills, methods and eligible creative templates CC BY-SA 4.0. Upstream grants and prior release permissions remain valid. Author: Jonathan Kyle Hobson.

Diagnose Mac app and storage problems, recover usable windows, and make verified installations or file moves while preserving user state.

## What you can do

- Recover an app that runs without a usable window.
- Find the cause of stuck processes, disk pressure or updater failures.
- Install an authorized application or move selected storage with integrity checks and rollback.

## How to start

1. Select this plugin in a supported host, or name the workflow in your request. Describe the result you want and provide the inputs listed below.
2. Start with one useful task. The assistant should explain the relevant capability, required input/access and expected result briefly when that helps; an explicit task can begin immediately.
3. Check the result and its reported state. A draft, local file, sent message and published result are different outcomes. Ask “what else can this plugin do?” or “help me get started” whenever you need the wider menu.

## Try a first task

| Ask | Bring | Expect |
| --- | --- | --- |
| “This app is running but I cannot see its window.” | App name and the observed symptom. | A focused diagnosis and verified recovery, preserving profiles and sessions. |
| “Help me move this project to the external drive.” | Exact source and intended mounted volume. | A checked move with copy integrity, consumer verification and rollback. |

## Choose a skill

The table is a selection guide. Once a task matches, read that complete skill; follow only its applicable support-file routes.

| Skill | Use it for |
| --- | --- |
| [app-window-recovery](skills/app-window-recovery/SKILL.md) | Recover an app that is running without a usable window while preserving user state. |
| [application-installation](skills/application-installation/SKILL.md) | Choose placement and verify an authorized Mac application installation, including external-runtime and login-item dependencies. |
| [mac-environment-conventions](skills/mac-environment-conventions/SKILL.md) | Choose the established Mac storage or runtime placement convention before a change. |
| [local-storage-mcp](skills/local-storage-mcp/SKILL.md) | Inspect recipient-authorized local storage through an available provider. |
| [storage-memory-manager](skills/storage-memory-manager/SKILL.md) | Inspect storage and memory pressure with read-only helpers before a recovery decision. |
| [mac-troubleshooter](skills/mac-troubleshooter/SKILL.md) | Triage an unexplained Mac application failure and select the smallest recovery workflow. |
| [process-diagnosis](skills/process-diagnosis/SKILL.md) | Diagnose a blocked quit, stale helper or resource-pressure symptom using exact process ownership. |
| [storage-migration](skills/storage-migration/SKILL.md) | Find what is taking Mac disk space, clean up authorized caches or unused runtimes, and move large files externally with verified volume identity, copy integrity and rollback. |
| [symlink-audit](skills/symlink-audit/SKILL.md) | Inspect a broken or confusing filesystem redirect and distinguish storage policy from runtime locks or sockets. |
| [updater-recovery](skills/updater-recovery/SKILL.md) | Diagnose Codex desktop update or disk-capacity failures and verify a bounded recovery. |

## Tools, setup and access

No MCP is bundled. Skills use currently available shell/native-app tools; references to local-storage or other providers are conditional dependencies, not connections supplied by this package. If a provider is absent, inspect the permitted filesystem/native state directly where supported and name the missing evidence.

Storage rules are specific to the current Mac and must be checked against live volumes. This package is not blanket authorization to delete caches, terminate unrelated processes or grant OS permissions.

## Reading routes for the assistant

- For a concrete task, go directly to the selected `SKILL.md`; this README is not required reading for every run.
- For a capability/help question, use the introduction, first-task examples, skill table and relevant setup section, then recommend one first request. Skip maintainer notes unless the question concerns an update. On first relevant use, give a brief task-specific orientation; do not replay a tour on every invocation or claim the user has been permanently onboarded.
- Load the full selected procedure and its required support. References explain methods; scripts execute only the authorized operation; templates/assets are output material. Preserved libraries are conditional depth, not a bulk context load.
- Check actual callable tools and action/resource scope before promising access or completion.

## Maintainer and existing integration notes

The canonical owner and the Working Tools package share the same distributable implementation. Edit the canonical source, mirror reviewed files to the public package, validate both, then install the selected version through the host's plugin manager. Start a fresh chat for refreshed discovery. Preserve recipient configuration outside the package.

Historical standalone entrypoints are compatibility routes. The current skill table and package project map define this implementation; private marketplace and cache paths are not installation requirements.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional agents

[Studio roles and assignments](references/professional-agents/README.md) connect these skills to named jobs. Work Management maintains cross-studio coverage and handoffs; native registrations are installed separately for each host.
<!-- END PROFESSIONAL-AGENTS -->

## Prerequisites and receiving-host storage roles

Ten complete skill heads, both historical original procedures, all recovery references and both shell helpers remain. Private machine bindings remain in the author archive; no operative method or helper is omitted. The literal placeholders `$ARCHIVE_VOLUME`, `$RUNTIME_VOLUME` and `<user>` stand for independently verified recipient volume names/user paths; never execute them literally or create a mountpoint. Establish a receiving-host role map with actual UUID, mounted path, filesystem, free space, archive/runtime/backup purpose, approved install roots and existing symlink patterns before any placement decision. Historical placement examples are conditional patterns, not facts about your Mac. Recheck the selected daily Claude profile rather than adopting the old private profile.

macOS is required for actual AppleScript/window inspection and Time Machine operations. Shell helpers use bash, standard system commands and `rg`; check local command availability and OS permissions. Other named skills/MCPs are optional receiving-host capabilities, not bundled services. The support-state backup helper preserves its timestamped copy behavior and does not establish a successful restore. Do not run recovery changes merely to test this package.

For “move this app to my external SSD” without a mounted, identified volume, return “the destination volume and its role are not verified” and complete a read-only inventory or request actual volume evidence. Preserve the full copy/hash/metadata/reopen/rollback procedure until those prerequisites are met. No installation, process termination, live restore or storage migration was performed by the synthetic validation.

`RUNTIME_VOLUME`, `ARCHIVE_VOLUME` and `SYSTEM_DATA_ROOT` are recipient-selected, verified mounted paths, not predefined environment values. Establish them from current volume identity and role evidence before translating any example command. macOS Data-volume inspection must use the actual current system data mount.

## Complete standalone storage methods

10 complete skill heads are retained. The added methods are `local-storage-mcp`, `storage-memory-manager`. Complete references and operative helpers are included; only originating private binding/input records are projected to recipient templates. No automatic installation of providers, hooks or global configuration occurs.

For a first task, use a disposable scan folder and explicit volume roles. Run the disk helper against that scope; it performs no deletion or move. An absent `local_storage` provider must yield an honest missing-provider state, not invented catalog contents. The Mac memory helper diagnoses only; it never terminates an application.
