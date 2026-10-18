# Gemini Toolkit

Gemini Toolkit is the provider owner for Gemini and Antigravity guidance. It
is CLI-first: use the authenticated Antigravity CLI for a bounded headless
task, select a live model explicitly, and verify output and permission state.
Use a browser or Antigravity UI only when the task needs screen state or a
surface-specific capability.

The toolkit records task-fit hypotheses and dated model evidence. It does not
claim that Gemini is inherently best at administration, spreadsheets, physics,
or 3D work. Those outcomes depend on tools, input modality, model version, and
task-specific validation.

This source plugin is a candidate for native installation. Installed, signed,
or marketplace status must be verified separately; source presence is not
installation or publication proof.


## Set up your own environment

1. Follow Google’s current [official Antigravity CLI installation](https://www.antigravity.google/docs/getting-started?tab=cli) for your operating system; verify `agy --version`. This plugin supplies instructions, not the runtime or a Google account.
2. Start the official interactive CLI and sign into your own eligible account. Complete any provider-required consent yourself or through authorized host tools. Choose telemetry/privacy settings deliberately. Do not copy another user’s credentials or enable paid API credits as an automatic fallback.
3. Run `agy models`; select an available model and a task-owned empty directory for your first nonprivate test. Follow [CLI operation](skills/gemini-operation/references/cli-operation.md), retain stdout/stderr and require a successful nonempty result. Verify effective permissions before allowing workspace actions.
4. Keep private prompts, provider settings and receipts outside the plugin. A model listing is availability evidence; it does not validate a task or confer access to Google Workspace. If the account/runtime is unavailable, state the gap and retain the bounded assignment.

Computer-use alternatives require the receiving host’s supported browser/app automation and the user’s own session. No browser automation provider, MCP connector, persistent daemon or global permission change is bundled.
