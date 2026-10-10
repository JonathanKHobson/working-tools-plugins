# Stitch Export Handoff

Use [Workbench](workbench.md) for draft and selection preservation. Read [the handoff template](brief-and-handoff.md) when packaging several outputs.

1. Identify the exact project and screen/component/selection being exported. Capture source and version/date privately. Confirm selection through visible UI; selecting a screen may also attach it to the draft context.
2. Open Export and inspect the current options. No selection may mean disabled export. Choose the least broad destination that satisfies the task. ZIP, clipboard, Figma, project brief, and hosted partners are possibilities, not guaranteed capabilities.
3. Follow the selected UI path. Exporting locally, copying code, transferring to another service, and publishing are different actions. Use the destination already authorized by the user; otherwise finish the local reviewable package before requesting any necessary external approval.
4. Verify the result: saved local path and contents; clipboard text captured into the intended file; or the actual receiving project/artifact. Clicking Export, seeing a toast, or opening a partner tab is not completion evidence. Restore only the temporary selection/context afterward.
5. For an **export-only request**, stop after verifying the saved file/contents and its visual usability, restoring temporary selection, and reporting the actual path. Do not edit a repo, install dependencies, or broaden to implementation. Inspect archive paths before extraction; if the export contains code, identify it as unexecuted unless execution was requested.
6. Continue the remaining steps only when integration or implementation is part of the task. Inspect downloaded archives and code before execution. Review file paths, scripts, dependencies, remote resources, trackers, credentials, placeholders, license notices, fonts, icon libraries, and framework assumptions. Never blindly run an exported installer or overwrite an existing project.
7. Reconcile with the receiving repo: verify its root and local changes, use the project’s existing structure and components, map tokens, replace sample content with supported facts, and separate shared shell from page content. If another agent owns that checkout, use a separate scratch directory/worktree and merge selected changes deliberately.
8. Replace fake links and simulated behavior with the requested real behavior, or clearly label unresolved prototype behavior. Keep forms and external services testable without sending unsolicited messages.
9. Run relevant build/functional checks and render the implementation. Compare it to the selected reference using 3–8 anchors, including a small viewport, font/image settling, focus, and meaningful interaction states. Apply [Design review](design-review.md).

## Closeout

Record export format, actual output path, accepted source design, code/assets integrated, checks performed, and remaining gaps. Distinguish exported, implemented, built, deployed, live-served, and externally delivered states. Do not claim pixel-perfect fidelity or full accessibility from a single screenshot.

Keep raw exports and QA material outside the public bundle unless needed. Mark disposable review artifacts for cleanup after the user’s applicable review/cleanup approval; preserve original source evidence.
