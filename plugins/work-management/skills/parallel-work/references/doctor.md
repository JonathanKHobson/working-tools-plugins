# Compatibility check

Doctor is a manual, read-only compatibility check. It is not a repair agent, project scanner, scheduler, model review, findings writer, or second task authority.

Run the installed script from Work Management:

```text
/opt/homebrew/bin/python3.12 <work-management-plugin>/scripts/codex_coordinator_doctor.py --check
```

It verifies only the packaged manifest, contract-28 capability file, skill frontmatter and links, state-helper syntax, project-lifecycle syntax, exact SessionStart/Stop registration, and hook syntax. It does not run a hook, inspect projects, read Codex databases or transcripts, scan rollouts, write diagrams, compare private paths, or modify installed files.

Results are `healthy` or `broken`. On `broken`, report:

> Parallel Work is broken or outdated. Update or reinstall the plugin from its configured marketplace or source.

Do not copy files, repair targets, roll back an installation, create a task, start an optional observer, or schedule a follow-up. The plugin manager owns update and reinstall.

Legacy `--apply` requests are rejected without writing and return the same update-or-reinstall action.
