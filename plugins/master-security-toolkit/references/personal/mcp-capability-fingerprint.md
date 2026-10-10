## MCP Capability Fingerprint

For every MCP under review, produce this capability fingerprint:

```text
name:
source/repo:
transport: stdio / streamable HTTP / SSE / other
launch command:
package/version/binary/hash:
env vars requested:
working directory:
tools:
resources:
prompts:
sampling support:
filesystem scope:
network scope:
write/destructive actions:
auth/OAuth/token behavior:
logs/output destinations:
update mechanism:
```

Any change to the command, package, version, binary, hash, tool list, tool
descriptions, schemas, resources, permissions, OAuth/token behavior, filesystem
scope, network scope, write actions, or update mechanism triggers re-review.
