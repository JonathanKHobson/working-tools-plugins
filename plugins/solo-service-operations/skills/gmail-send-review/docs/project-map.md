# Gmail review module map

- `../SKILL.md`: complete send/reply/schedule workflow and recipient editorial requirements.
- `../scripts/gate.py`: original full offline PreToolUse filter, argument fingerprint, authored-text checks and receipt CLI. POSIX Python3.9+; no network or email storage.
- `../tests/test_gate.py`: original full behavior suite, including encoded MIME, authorization holds, changed content, stale/single-use drafts and session isolation.
- Optional registration: the recipient explicitly adds the helper's `hook` command to their supported host PreToolUse configuration. Installation registers no hooks.
- State: receiving-user `.local/share/working-tools/gmail-send-review`, or explicit `GMAIL_SEND_REVIEW_STATE`/`--state-dir`. Private hash metadata and lock files only.
- Flow: review exact authorized content, record receipt, invoke provider, inspect Sent readback. Draft-only instructions never gain send authority from a receipt.
- Hook limits: only registered connector tool spellings/payload shapes are recognized. ID-only draft sending cannot detect concurrent server edits. Host failures can fail open; this is an editorial guardrail, not a security boundary.
- Run tests from the package root: `python3 -B -m unittest discover -s skills/gmail-send-review/tests -v`.
- Disable by removing only this optional host hook entry and following that host's reload behavior; preserve unrelated hooks.
