#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RELEASE = Path(os.environ.get("VIDEO_WORKFLOW_RELEASE_DIR", ROOT / "release"))
RELEASE.mkdir(parents=True, exist_ok=True)
PLUGIN_VERSION = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text())["version"]


def is_release_file(path: Path) -> bool:
    relative = path.relative_to(ROOT)
    parts = set(relative.parts)
    if parts & {".git", ".venv", ".runtime", ".pytest_cache", "__pycache__", "build", "dist", "release"}:
        return False
    if any(part.endswith(".egg-info") for part in relative.parts):
        return False
    if {"work", "output", "cache"} & parts and "examples" in relative.parts:
        return False
    return path.is_file() and path.suffix not in {".pyc", ".pyo"}


def run_step(name: str, command: list[str]) -> dict[str, Any]:
    started = time.monotonic()
    proc = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
    elapsed = round(time.monotonic() - started, 3)
    return {
        "name": name,
        "command": command,
        "returncode": proc.returncode,
        "duration_s": elapsed,
        "stdout_tail": proc.stdout[-4000:],
        "stderr_tail": proc.stderr[-4000:],
        "passed": proc.returncode == 0,
    }


def main() -> int:
    steps = [
        run_step("plugin-structure", [sys.executable, "scripts/validate_plugin.py"]),
        run_step("python-compile", [sys.executable, "-m", "compileall", "-q", "video_workflow", "skills", "adapters", "scripts"]),
        run_step("vertical-project-audit", [sys.executable, "-m", "video_workflow.cli", "audit-project", "examples/multi-aspect-variants/vertical.json"]),
        run_step("baseline-example-render", ["bash", "scripts/render_example.sh"]),
        run_step("multi-aspect-example-render", ["bash", "scripts/render_variants.sh"]),
        run_step("test-suite", [sys.executable, "-m", "pytest", "-q"]),
    ]

    toolchain_step = run_step("toolchain-report", [sys.executable, "scripts/check_environment.py"])
    steps.append(toolchain_step)
    toolchain: dict[str, Any] | None = None
    if toolchain_step["passed"]:
        try:
            toolchain = json.loads(toolchain_step["stdout_tail"])
        except json.JSONDecodeError:
            # The complete output should normally fit; rerun without tail truncation if it does not.
            proc = subprocess.run([sys.executable, "scripts/check_environment.py"], cwd=ROOT, capture_output=True, text=True, check=False)
            if proc.returncode == 0:
                toolchain = json.loads(proc.stdout)
    if toolchain is not None:
        (RELEASE / "toolchain-report.json").write_text(json.dumps(toolchain, indent=2) + "\n")

    qa_paths = [
        ROOT / "examples/music-slideshow/output/qa-report.json",
        ROOT / "examples/multi-aspect-variants/output/vertical/qa-report.json",
        ROOT / "examples/multi-aspect-variants/output/square/qa-report.json",
    ]
    qa_reports = []
    for path in qa_paths:
        try:
            data = json.loads(path.read_text())
            qa_reports.append({"path": str(path.relative_to(ROOT)), "passed": bool(data.get("passed")), "checks": data.get("checks", [])})
        except Exception as exc:
            qa_reports.append({"path": str(path.relative_to(ROOT)), "passed": False, "error": str(exc)})

    sources = json.loads((ROOT / "research/sources.lock.json").read_text()).get("sources", [])
    scenarios = [line for line in (ROOT / "evaluations/scenarios.jsonl").read_text().splitlines() if line.strip()]
    skills = sorted(path.name for path in (ROOT / "skills").iterdir() if path.is_dir())
    metrics = {
        "skills": len(skills),
        "skill_names": skills,
        "reviewed_sources": len(sources),
        "evaluation_scenarios": len(scenarios),
        "files": sum(1 for p in ROOT.rglob("*") if is_release_file(p)),
        "example_qa_passed": all(report.get("passed") for report in qa_reports),
    }
    passed = all(step["passed"] for step in steps) and metrics["example_qa_passed"]
    report = {
        "version": PLUGIN_VERSION,
        "verified_at": date.today().isoformat(),
        "passed": passed,
        "metrics": metrics,
        "steps": steps,
        "example_qa": qa_reports,
        "limitations": [
            "Packaged routing/pressure scenarios are fixtures, not a measured model-routing benchmark.",
            "Specialized renderer adapters are scaffolds unless their separate runtimes are installed and tested.",
            "Synthetic examples validate mechanics and layout paths; real-world media regression coverage remains a next step.",
        ],
    }
    # Static plugin-eval is advisory: its public-distribution rubric is not the
    # local private-plugin release contract. Never install an evaluator implicitly.
    evaluator = os.environ.get("VIDEO_WORKFLOW_PLUGIN_EVAL") or shutil.which("plugin-eval")
    if evaluator and Path(evaluator).is_file():
        prefix = [evaluator]
        if Path(evaluator).suffix == ".js":
            node = shutil.which("node")
            prefix = [node, evaluator] if node else []
        if prefix:
            static = run_step("static-plugin-eval-advisory", prefix + ["analyze", str(ROOT), "--format", "json", "--output", str(RELEASE / "plugin-eval-static.json")])
            report["static_plugin_eval"] = static
            if not static["passed"]:
                report["limitations"].append("Optional static Plugin Eval did not complete; inspect its command receipt.")
        else:
            report["limitations"].append("Static Plugin Eval JavaScript entrypoint was supplied but Node is unavailable.")
    else:
        report["limitations"].append("Static Plugin Eval not found; set VIDEO_WORKFLOW_PLUGIN_EVAL to an existing CLI or JavaScript entrypoint if needed.")
    (RELEASE / "verification-report.json").write_text(json.dumps(report, indent=2) + "\n")

    md = [
        "# Release Verification",
        "",
        f"- **Version:** {report['version']}",
        f"- **Verified:** {report['verified_at']}",
        f"- **Overall:** {'PASS' if passed else 'FAIL'}",
        f"- **Skills:** {metrics['skills']}",
        f"- **Reviewed sources:** {metrics['reviewed_sources']}",
        f"- **Routing/pressure scenarios:** {metrics['evaluation_scenarios']}",
        "",
        "## Steps",
        "",
        "| Step | Result | Seconds |",
        "|---|---:|---:|",
    ]
    for step in steps:
        md.append(f"| {step['name']} | {'PASS' if step['passed'] else 'FAIL'} | {step['duration_s']} |")
    md += ["", "## Example outputs", ""]
    for qa in qa_reports:
        md.append(f"- `{qa['path']}` — {'PASS' if qa.get('passed') else 'FAIL'}")
    md += ["", "## Limitations", ""] + [f"- {item}" for item in report["limitations"]]
    (RELEASE / "VERIFICATION.md").write_text("\n".join(md) + "\n")

    print(json.dumps({"passed": passed, "metrics": metrics, "report": str(RELEASE / 'verification-report.json')}, indent=2))
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
