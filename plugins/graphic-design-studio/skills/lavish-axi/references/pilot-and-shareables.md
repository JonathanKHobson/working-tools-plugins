# Lavish Pilot And Shareables Integration

## Source Verdict

The useful part of Lavish AXI is the loop shape:

- the agent writes a local HTML artifact;
- the local browser reports layout faults before human review;
- the human annotates rendered elements or text;
- the agent polls for feedback, fixes the artifact, and replies;
- the final artifact remains clean and portable.

Do not treat the external runtime as part of the deliverable. The deliverable is
either a safer local workflow or a measured sandbox result.

Reviewed version: `lavish-axi@0.1.31`, MIT. The package was installed in an
isolated review prefix with lifecycle scripts disabled and verified with
`--help` and `playbook plan` only.

Key runtime surfaces:

- local Express server and browser-open flow;
- file watcher for the selected HTML artifact and optionally sibling assets;
- local state under `.lavish-axi/` or `LAVISH_AXI_STATE_DIR`;
- optional SessionStart hook installer for Claude Code, Codex, and OpenCode;
- optional telemetry path, disabled locally with `LAVISH_AXI_TELEMETRY=off`;
- non-loopback binding support that can expose an unauthenticated local-file
  server if misconfigured.

Keep the reviewed isolated binary as the preferred inspection path for future
trials:

```bash
LAVISH_AXI_TELEMETRY=off \
  "${LAVISH_AXI_BIN:?Set LAVISH_AXI_BIN to your reviewed installed executable}" \
  playbook plan
```

## Pilot Shape

Use this only after the user approves a runtime trial.

1. Create or use `_Sandbox/lavish-axi-pilot/`.
2. Copy one real HTML frame into the sandbox.
3. Inline or reference the local project tokens/style source. Do not use the
   `lavish-axi design` CDN fallback when a local style source exists.
4. Run the smallest approved command sequence from the sandbox.
   Use `LAVISH_AXI_TELEMETRY=off`, keep the default loopback host, and avoid
   `setup hooks` unless hook installation is the explicit test.
5. Capture whether the layout gate caught real issues and whether annotation
   feedback saved turns versus screenshots.
6. End/stop the session and confirm no background browser/server remains.
7. Test the exported HTML directly, outside Lavish, including mobile width and
   cold-open portability.

Exit criteria:

- at least one real annotation feedback loop completed;
- layout warnings, if any, were fixed before human review;
- exported file has no Lavish SDK, CDN fallback, `localhost`, private paths, or
  unexpected external URLs;
- the user decides whether to keep Lavish as a side tool, rebuild native, or
  stop the experiment.

## Shareables Option

For Shareables MCP/workflow work, add Lavish-derived behavior as a build-time
or dev-time review option:

- render QA can surface layout warnings before public staging;
- a future authoring overlay may queue element notes for the agent, but must be
  stripped from exports;
- style-source resolution should follow local registry/tokens first, detected
  project config second, and bundled fallback last;
- published Shareables stay static/public-safe and cannot depend on a local
  server, browser session, or unreviewed CDN runtime.

This belongs beside existing Shareables validation and visual QA, not in place
of them.
