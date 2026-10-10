# MCP registry and activation method

This is the recipient-ready registry procedure. Populate it only from the receiving host's current configuration and the user's selected baseline. The author's complete historical inventory is preserved separately in a private binding and is not a recipient default. A listed manifest or old snapshot does not prove a live tool.

## Source of truth

Record the actual host and profile that owns each MCP: Codex active configuration, Codex per-server profile, Claude Desktop profile, or cloud connector. These are distinct surfaces. Store file paths, credentials and account identifiers in the host's private configuration, not in a distributable plugin, chat transcript or public registry. Keep a dated read-only inventory with the configuration hash/revision when it matters for rollback.

| Logical provider | Host/config owner | Server key | Runtime/binding location | Data/corpus owner | Permission scope | Baseline or temporary | Current discovery | Representative harmless check | Rollback/disable route |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [recipient-selected provider] | [actual host] | [actual key] | [private config pointer] | [separate owner] | [read/write scope] | [user-selected role] | [observed state and date] | [safe call] | [reviewed host action] |

## Activation rule

1. Start from the user's chosen small baseline. Verify the selected provider is installed and enabled on the specific host; a plugin declaration, global config block and connector listing may refer to different implementations of the same logical service. Avoid duplicate server registrations when one verified route suffices.
2. Before adding a temporary MCP, identify its task purpose, exact exposed tools/resources, runtime and data location, auth scope, expected side effects and impact on startup. Obtain any task-specific authorization needed for writes or spending. Do not enable a full fleet merely because a package exists.
3. Save the current relevant config state and name the rollback command or UI control. Preserve running sessions and active jobs. A reload or fresh task may be required before discovery changes become visible.
4. Test in order: host configuration readback, process/transport initialization, tool listing, a harmless representative read, then the exact task operation under its own authorization. A successful direct smoke does not prove that an existing chat exposes the tool; check the chat's actual tool surface.
5. After the task, disable only temporary registrations this task enabled unless the user asked to retain them. Verify the intended baseline still appears. Do not remove a permanent provider, another task's session, or a data store based on low CPU, age or a shared parent process.

## Missing or ambiguous states

- **Not configured:** No selected host registration or binding. Ask for the specific missing input only after completing independent work; do not invent a server path or credential.
- **Configured but unavailable:** The entry exists, but transport, permission, executable or data mount fails. Preserve the exact error and test one bounded repair or host-supported alternative.
- **Direct smoke works but chat lacks tools:** Treat native exposure as unresolved. A supported direct fallback may provide task continuity, but report it separately from native discovery.
- **Empty search:** Confirm the tool ran against the intended corpus and scope. Empty results are evidence of this query, not proof that the source or task has no data.
- **Multiple failures:** Check shared runtime/profile health before changing individual repos or indexes. Restore the prior config when an attempted change worsens startup.

## Inventory review

For every provider, keep the logical name, each host-specific key, actual installed source/version, profile membership, data owner, license/rights boundary, read/write/tool scope, startup cost, current health and last verification date. Distinguish daily baseline, optional task pack, temporary diagnostic and retired entries. Retired entries belong in an archive or backup, not an active launch profile. A cloud HTTPS connector and local stdio server are different acquisition routes; do not equate them.

## Test plan and intake

For a new MCP, read the package's own installation and privacy documentation, check source/rights, runtime dependencies, network or subprocess behavior, storage writes, credentials, prompt/tool injection surface and rollback. Use a disposable or read-only first-use call. Verify returned data shape, source lineage and permissions before relying on it. For write tools, prepare the exact intended change, inspect the target state, execute only when authorized, then read back the result. Record installed, discovered, invoked and verified as separate states.

Review the registry after host/plugin upgrades, profile changes or repeated exposure failures. Update only the receiving host's private inventory; this template grants no provider installation, data access or recurring monitor.
