## Output Contract

Use this shape for security reviews unless the user asks for something shorter:

```markdown
**Verdict**
Proceed / Proceed with caution / Do not install yet

**Confidence**
Low / Medium / High, with one sentence explaining why.

**What I Inspected**
- Source/repo/download:
- Manifests/scripts/config:
- Permissions/tool surface:
- Dependencies/checks:
- Provenance/signing/attestations:

**Threats Checked**
- Source spoofing / malicious mirror:
- Tampered artifact / missing provenance:
- Install-time script risk:
- Persistence / background service risk:
- Sensitive-data access:
- Prompt-injection / tool-poisoning risk:
- MCP/Codex network or tool-surface risk:

**Risks Found**
- ...

**Unknowns**
- ...

**Safer Path**
- ...

**Commands Run / Not Run**
- Ran:
- Did not run:

**Final Recommendation**
...
```

For quick chat replies, compress the same structure into a short verdict plus
risks and next action.
