## Phase Handoff

Use when a workflow spans rounds, stages, or several skills and the next phase
must inherit context without restarting the whole system.

- Phase:
- Decision:
- Artifact(s):
- Verification:
- Next phase:
- Stop condition:
- What not to touch:

Keep handoffs short enough to fit in a status update. They should preserve the
decision, the proof, and the next lane without turning the handoff into a new
planning artifact.

## When execution depends on shutdown or local authentication

Carry forward existing user authorization and finish independent authorized work.
State exactly which action remains, what prerequisite prevents execution, where
the prepared artifact is, and what readback would prove completion. A checked
script is prepared, not executed; a component's removal from an app registry does
not prove its physical files were reclaimed. Keep completed gains separate from
pending work so the next worker does not repeat deletion or promise a finished
migration from a partial redirect.

The owning skill supplies execution-time checks and rollback. For storage work,
use `mac-ops-toolkit:storage-migration`; do not copy machine-specific paths or
destructive commands into general coordination guidance. Resume from current
evidence because mounts, open handles and file contents can change while waiting.
