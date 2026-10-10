# Agent artifact scanning and adjudication

Use this when a local skill/plugin package needs inspection. First enumerate the package's actual files, scripts, manifests, hooks, MCP launch definitions, and declared capabilities. Scan text as data; never execute the candidate merely to scan it. Follow static findings into exact file/line evidence and inspect surrounding context, reachable code, and data flow.

## Risk classes

- Instruction override or authority spoofing: text tries to supersede user/system intent, conceal actions, suppress review, or make external content authoritative.
- Execution and supply chain: remote pipe-to-shell, encoded/eval stages, unpinned runners or VCS refs, lifecycle hooks, destructive commands, broad permissions, persistence, or secondary downloads.
- Data exposure: secret harvesting, credential/session paths, outbound uploads, unexpected logging or telemetry, and overly broad MCP tools.
- Contextual risk: a command shown as a negative example, a scoped cleanup in a tested script, or documentation of an attack may be benign. Judge reachability and intent, not keyword presence alone.

For every candidate finding, record rule/class, exact path and line, relevant excerpt, execution or instruction path, observed versus inferred behavior, severity, confidence, and whether it is active, ambiguous, or false positive. Review the package's tool descriptions, schemas, resources, prompts, and update path even when the deterministic scan is clean.

Suppress a demonstrated false positive only with the exact **finding fingerprint + rule ID + rule version + documented reason**. Re-run the scan after applying a reviewed suppression and report both active and suppressed counts; keep suppressed findings visible in the report. A changed file or rule requires re-review. Test scanner changes against both known-positive and benign near-miss fixtures. Report explicit noncoverage (for example, dynamic behavior, binary payloads, runtime network behavior, or unsupported file types). Scanner exit 0 means its deterministic checks found no active finding, not that the package is safe.

## Bundled read-only scanner

This toolkit vendors [agent-skillguard v0.1.5](https://github.com/SpannDaMan/agent-skillguard/tree/affd36ef237d1fb7ebd830cde630a7b4cc27aaba) at commit `affd36ef237d1fb7ebd830cde630a7b4cc27aaba`, under the upstream [MIT license](../../../vendor/agent-skillguard/LICENSE). The fixed [local wrapper](../../../scripts/skillguard_scan.py) exposes only scans to stdout, with a fixed rule pack and capped file/byte limits. It does not expose upstream `init-suppressions` or `--output` writes, install a package, start an MCP, fetch network resources, or execute target files. Run it with a known local Python 3.10+ interpreter:

```bash
python3 /path/to/master-security-toolkit/scripts/skillguard_scan.py /path/to/candidate --format json
```

Choose `markdown` or `sarif` when helpful. `--suppressions /path/to/reviewed.json` reads an exact-match suppression file; keep the original finding and reason visible. Exit `0` means no active deterministic findings, `1` means findings, `2` means an input or scan error. The local wrapper is a reviewed adaptation of the upstream CLI, not the separately installed `skillguard` command. It uses the upstream [rule corpus](../../../vendor/agent-skillguard/rules/default-rules.json) and [noncoverage registry](../../../vendor/agent-skillguard/rules/non-coverage.json).

Only scan paths within the authorized task. Reports can contain bounded excerpts from scanned files; keep them private when inputs are sensitive. Scan results are not proof of benign behavior or full coverage. If a scan fails or a file is skipped, say so and perform manual review of the gap.

Before trusting a changed scanner module, rule pack, or fixture corpus, run the bundled [upstream rule-corpus verifier](../../../vendor/agent-skillguard/tools/verify_rule_corpus.py) with the SHA-256 of the vendored module as `--product-revision`; require every positive and negative fixture and every rule to pass. The verifier was adapted only for the vendored directory layout and stdout-only output. Record the resulting rule, fixture, and noncoverage hashes in a release review. The scanner excludes symlinks in normal traversal and caps eligible files, but concurrent replacement of a target file during scanning is outside this static review's guarantee; scan a stable copy of an untrusted package.

## Data that can become execution

When the candidate generates copied commands, browser pages/workspace data, or inspection/install modes, read the conditional [data-to-execution checks](../../agent-artifact-scanning/references/data-to-execution.md). Trace the exact input-to-effect path in addition to the normal scan. A clean regex report does not adjudicate these paths. Source/distribution consistency belongs to `work-management:plugin-maintenance` when installed; obtain its release-surface evidence when packaged copies differ. If that owner is absent, report the discrepancy and evidence limits from this review without claiming release reconciliation.
