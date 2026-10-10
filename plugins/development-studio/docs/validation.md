# Source validation receipt

Prepared and verified 2026-10-08. This receipt covers the source package, not native installation or actual-host execution.

- `python3 -B scripts/validate_package.py`: PASS, 11 skills, 175 imported file hashes, complete imported support closure, 137 maintained local links and 42 retained official provider methods. No errors.
- `python3 -B tests/test_package_validation.py`: PASS, 8 tests. Negative cases detect modified upstream and local-MCP files, missing full methods, added unreviewed vendor assets, unexpected runtime declarations, unknown provider routes and escaping references.
- Native Skill Creator quick_validate: all 11 skills passed; exact results in [skill-validation.json](skill-validation.json).
- Staged SkillGuard v0.1.5: 186 eligible text files, 921758 bytes, 0 active / 0 suppressed deterministic findings. Exact report/digest in [staged-scan.json](staged-scan.json). Reports and this receipt are generated after that scan; they contain evidence only. Manual findings and noncoverage are in [admission](admission.md).
- Independent forward review of six realistic prompts found one excessive diagnostic-artifact default; it was corrected to allow bounded inline analysis. See [forward review](forward-review.json). This was judgment of the actual routes, not a measured routing benchmark.
- All 382 captured files of six retained official provider packages still match the preparation inventory. No official source changed in this task.
- A final targeted search found no private username, personal volume label, private fleet profile or private memory path in either package. Concrete host-path and symlink checks also pass.

The release file list hashes every source member except itself after these receipts were written. Parent installation must compare both directions and verify fresh skill discovery. Live MCP/provider behavior and optional helper execution are not claimed.


## Historical 0.2.0 standalone source integration

The added complete standalone methods are source/synthetic verified: 21-head route validator, 252 imported file hashes, 181 local links, 42 provider references; nine behavioral/integrity tests passed. All current discovery heads pass Skill Creator validation in the external verification environment. Synthetic Go retrieval/no-write and actual Apps SDK scaffold generation/refusal passed. Native discovery, runtime providers, compiled projects and publication remain separate lead-owned checks. Earlier 11-head native/source results remain historical receipts.
