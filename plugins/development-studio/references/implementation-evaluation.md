# Evaluate implementation efficiency

Use for a reported-impact question or an explicitly requested comparison. Reports do not activate implementation mode or change a repository. The source skill's gain display is retained here as an attributed scoreboard, with a stricter boundary between published evidence and local measurements.

## Published v5 scoreboard

Source: [upstream October 7, 2026 benchmark at the v5.0.0 pin](https://github.com/dietrichgebert/ponytail/blob/b088b2df6e08d4306c6a3c3d575fe38c2d2d2989/benchmarks/results/2026-10-07-agentic.md). These are author-reported results, not independent reproduction or measurements of this adapted studio.

| Metric | Reported v5 result versus no skill |
| --- | --- |
| Delivered lines of code | 53% fewer; reported 95% interval 41–63% fewer |
| Compressed code information | 41% lower |
| Output tokens | 45% fewer |
| Estimated list-price cost | 26% lower; reported interval 16–36% lower |
| Elapsed time | 41% lower; reported interval 32–49% lower |
| Hidden checks | 87/90 passed versus 86/90 |
| Nontrivial tasks leaving a test/check | 98% versus 68% |
| Injected bugs caught where a test exists | 69% versus 77% |

The experiment used one model/host configuration (Opus 5.5, Claude Code), 39 tasks, five runs per task/arm, and geometric means of per-task median ratios. Agents could write but could not run their code. Only 18 tasks had hidden correctness/safety checks; the other 21 primarily measured output size. Estimated token list-price cost is not an account bill.

The reported v5-versus-v4 cost reduction is 10.8%; it is not an 11% overall quality gain. Time versus v4 was 4% lower with an interval crossing zero. The source reports no demonstrated correctness advantage, and its privacy case failed three of five runs in every arm. These observations do not establish formal equivalence or noninferiority.

Raw run directories are not in the pinned repository, and the report says its mutation-test tooling was not yet included. Some shipped scorers only check syntax or delivered files. The source task pool also documents screening open-task candidates for favorable results. Treat selection/tuning bias and generalization as unresolved, not as proof the reported arithmetic is fabricated. An external video's larger test counts require that video's actual methods and outputs; they cannot be verified from this source alone.

Use a table or ASCII bars if requested. Never label these numbers as “your savings.” An implementation that was never built is not a measured baseline.

## A meaningful local comparison

1. Define the same outcome and acceptance checks before looking at generated code. Include exact fixes, a vague product request, a human-facing interaction, a data/security boundary and a larger existing-repository change when those represent actual use. Use held-out cases not used to tune the rules.
2. Compare normal operation, the source efficiency method and the adapted specification/UX handoff where useful. Pin prompts, source revision, model, effort, permissions, dependencies and runtime. Keep task authority equal.
3. Run in isolated disposable workspaces with no credentials or unrelated files. Preserve normal permission controls. Execute generated code only after review in an appropriate sandbox. A process working directory, disabled Bash tool or a temporary folder is not isolation.
4. Check behavior, security, accessibility and completeness before interpreting smaller code. Use hidden tests where suitable, real UI interactions for usability, and independent review of consequential findings. A model judge is advice, not a functional test.
5. Keep all attempts, failures, timeouts, missing outputs and repair effort. Collect actual added/deleted/code/test lines, input/output tokens where reported, elapsed time and provider-reported price estimates separately. Do not turn missing values into zero.
6. Report per-task quality first. For comparable successful pairs, report the prespecified median and ratio aggregation with denominators and exclusions. Report failures alongside conditional efficiency results so excluded failures cannot masquerade as wins. Use repeated trials and uncertainty for broader claims; a one-run acceptance check demonstrates only that case.
7. Inspect the final human experience and maintainability. Fewer lines that move burden to users, skip recovery, or create fragile tests are not an improvement.

Stop once the requested comparison is answered. Do not launch a paid run, provider job, full benchmark suite or recurring measurement merely because this reference is loaded.

## Security boundary of the upstream harness

The pinned upstream harness invokes permission-bypassing agents, imports/executes generated outputs and can send broad workspace contents to a model judge. Even rescoring can execute generated code. Its scripts are retained in the source evidence checkout, not installed as trusted automation. The studio's existing evaluation providers and the procedure above preserve the comparison capability without copying those execution policies.

For a user-requested reproduction, inspect the exact runner and test corpus, provide real isolation and explicit provider/data/cost scope, remove permission bypass and inherited credentials, and verify the result. Do not claim that running a self-test or inspecting the source reproduces the published benchmark.
