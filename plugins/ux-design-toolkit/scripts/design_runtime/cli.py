"""Public entrypoint for explicit detector/context/live calls and quiet hooks."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from .engine import RuntimeErrorWithMessage, invoke, verified_engine
from .config import install_hooks, install_marker_only, remove_hooks
from .hooks import MAX_INPUT, handle
from .scope import disable, enable, explicit_target, loopback_url, project_root

LIVE_VERBS = {"live", "live-target", "live-status", "live-resume", "live-complete",
              "live-inject", "live-wrap", "live-insert", "live-accept", "live-server",
              "live-generate", "live-poll", "live-commit-manual-edits", "live-discard-manual-edits"}
NATIVE_VERBS = {"detect-csp", "palette", "surface-brief", "critique-storage", "embed-prompt",
                "signals", "context-signals", "doctor", "concept-seed", "serve-question",
                "component-review", "comp-spec", "comp-diff", "font-match", "build-phase"}
PRIVATE_FIELD = re.compile(r"token|secret|password|credential|authorization|api[_-]?key", re.I)
PRIVATE_TEXT = re.compile(r"(?i)(token|api[_-]?key|authorization|password|secret)([=:?&\s]+)([^\s&\"']+)")


def _safe_live_output(raw: str) -> str:
    if not raw:
        return ""
    try:
        value = json.loads(raw)
    except ValueError:
        # Prose can include a token without a stable delimiter. Do not relay it.
        return "Native live output is available only in its protected local session."

    def redact(item):
        if isinstance(item, dict):
            return {key: "<redacted>" if PRIVATE_FIELD.search(key) else redact(child) for key, child in item.items()}
        if isinstance(item, list):
            return [redact(child) for child in item]
        if isinstance(item, str):
            return PRIVATE_TEXT.sub(r"\1\2<redacted>", item)[:4000]
        return item

    return json.dumps(redact(value), ensure_ascii=False)[:20000]


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Pinned UX Design Toolkit native design runtime")
    subs = parser.add_subparsers(dest="command", required=True)
    subs.add_parser("verify", help="verify the packaged manifest, architecture, assets, and binary hash")
    detect = subs.add_parser("detect", help="scan only explicitly named frontend files or URLs")
    detect.add_argument("--project", required=True)
    detect.add_argument("--url", action="store_true", help="enable explicit http(s) URL scan in isolated browser profile")
    detect.add_argument("--no-config", action="store_true")
    detect.add_argument("--no-design-system", action="store_true")
    detect.add_argument("--no-inline-ignores", action="store_true")
    detect.add_argument("--no-advisory", action="store_true")
    detect.add_argument("--scope")
    detect.add_argument("--viewport")
    detect.add_argument("targets", nargs="+")
    context = subs.add_parser("context", help="read native design context for an explicit project")
    context.add_argument("--project", required=True)
    native = subs.add_parser("native", help="run one reviewed native design utility")
    native.add_argument("--project", required=True)
    native.add_argument("verb", choices=sorted(NATIVE_VERBS))
    native.add_argument("args", nargs=argparse.REMAINDER)
    live = subs.add_parser("live", help="run an explicitly requested native live/variant verb")
    live.add_argument("--project", required=True)
    live.add_argument("--dev-url", required=True)
    live.add_argument("verb", choices=sorted(LIVE_VERBS))
    live.add_argument("args", nargs=argparse.REMAINDER)
    hook = subs.add_parser("hook", help="quiet advisory PostToolUse/Stop handler")
    hook.add_argument("kind", choices=("post", "stop"))
    hook.add_argument("--project", required=True)
    for name in ("enable-hooks", "disable-hooks"):
        sub = subs.add_parser(name, help="toggle this project's explicit hook marker")
        sub.add_argument("--project", required=True)
    for name in ("install-hooks", "remove-hooks"):
        sub = subs.add_parser(name, help="manage a marker-only plugin opt-in or owned project-local hook entries")
        sub.add_argument("--project", required=True)
        sub.add_argument("--marker-only", action="store_true", help="use plugin-owned host hooks without writing project host configs")
        sub.add_argument("--host", choices=("codex", "claude", "both"), help="legacy project-local fallback; omit with --marker-only")
    return parser


def _write_result(result) -> int:
    if result.stdout:
        sys.stdout.write(result.stdout)
    if result.stderr:
        sys.stderr.write(result.stderr)
    return result.returncode if result.returncode in {0, 1, 2} else 1


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "verify":
            binary, _ = verified_engine()
            print(f"Verified pinned engine: {binary}")
            return 0
        if args.command == "hook":
            raw = sys.stdin.read(MAX_INPUT + 1)
            if len(raw) > MAX_INPUT:
                return 0
            try:
                event = json.loads(raw)
            except ValueError:
                return 0
            try:
                message = handle(args.kind, event, args.project)
            except (OSError, ValueError, RuntimeError, TypeError):
                # Host hooks stay advisory even if local state is corrupt.
                return 0
            if message:
                name = "PostToolUse" if args.kind == "post" else "Stop"
                if name == "Stop" and isinstance(event, dict) and isinstance(event.get("turn_id"), str):
                    # Codex Stop accepts a nonblocking systemMessage; a block
                    # would create another turn and violate advisory behavior.
                    print(json.dumps({"systemMessage": message}))
                else:
                    print(json.dumps({"hookSpecificOutput": {"hookEventName": name, "additionalContext": message}}))
            return 0
        root = project_root(args.project)
        if args.command == "enable-hooks":
            print(f"Enabled project marker: {enable(root)}")
            return 0
        if args.command == "disable-hooks":
            print("Removed owned project marker" if disable(root) else "Owned marker was not enabled")
            return 0
        if args.command == "install-hooks":
            if args.marker_only:
                if args.host:
                    raise ValueError("--marker-only and --host are mutually exclusive")
                print(f"Enabled marker for plugin-owned hooks: {install_marker_only(root)}")
                print("Host plugin installation, trust, and execution require separate verification.")
                return 0
            if not args.host:
                raise ValueError("Project-local installation requires --host codex|claude|both")
            paths = install_hooks(root, args.host)
            print("Prepared project-local hooks: " + ", ".join(str(path) for path in paths))
            print("Host trust and execution still require verification in that project.")
            return 0
        if args.command == "remove-hooks":
            if args.marker_only:
                if args.host:
                    raise ValueError("--marker-only and --host are mutually exclusive")
                print("Removed owned project marker" if disable(root) else "Owned marker was not enabled")
                return 0
            if not args.host:
                raise ValueError("Project-local removal requires --host codex|claude|both")
            paths = remove_hooks(root, args.host)
            print("Removed owned project-local hook entries and marker: " + ", ".join(str(path) for path in paths))
            return 0
        if args.command == "detect":
            targets = [explicit_target(root, item, allow_url=args.url) for item in args.targets]
            if args.url and any(not item.startswith(("http://", "https://")) for item in targets):
                raise ValueError("URL mode accepts only explicit http(s) targets")
            flags = [name for name in ("no_config", "no_design_system", "no_inline_ignores", "no_advisory") if getattr(args, name)]
            cmd = ["detect", "--json", *["--" + flag.replace("_", "-") for flag in flags]]
            for name in ("scope", "viewport"):
                value = getattr(args, name)
                if value:
                    cmd.extend(["--" + name, value])
            return _write_result(invoke([*cmd, *targets], cwd=root, timeout=60 if args.url else 30))
        if args.command == "context":
            return _write_result(invoke(["context", "--target", str(root)], cwd=root, timeout=30))
        if args.command == "native":
            forwarded = args.args[1:] if args.args[:1] == ["--"] else args.args
            for value in forwarded:
                if value.startswith(("http://", "https://")):
                    # A network target must be supplied explicitly by the caller.
                    explicit_target(root, value, allow_url=True)
            return _write_result(invoke([args.verb, *forwarded], cwd=root, timeout=60))
        if args.command == "live":
            dev_url = loopback_url(args.dev_url)
            forwarded = args.args[1:] if args.args[:1] == ["--"] else args.args
            if any(value == "--token" or value.startswith("--token=") or value == "--keep-inject" for value in forwarded):
                raise ValueError("Live tokens and retained injection are unavailable through this adapter")
            for index, value in enumerate(forwarded):
                if value == "--target" and index + 1 < len(forwarded):
                    candidate = Path(forwarded[index + 1]).expanduser().resolve(strict=True)
                    if not candidate.is_relative_to(root):
                        raise ValueError("Live target must stay inside the named project")
                elif value.startswith("--target="):
                    candidate = Path(value.split("=", 1)[1]).expanduser().resolve(strict=True)
                    if not candidate.is_relative_to(root):
                        raise ValueError("Live target must stay inside the named project")
                elif value.startswith("--dev-url="):
                    if loopback_url(value.split("=", 1)[1]) != dev_url:
                        raise ValueError("Live dev URL must match the named loopback URL")
                elif value == "--dev-url" and args.verb != "live" and index + 1 < len(forwarded):
                    if loopback_url(forwarded[index + 1]) != dev_url:
                        raise ValueError("Live dev URL must match the named loopback URL")
            # The native command may accept extra URLs; none may point away from loopback.
            for value in forwarded:
                if "http://" in value or "https://" in value:
                    loopback_url(value.split("=", 1)[-1])
            cmd = [args.verb]
            has_target = "--target" in forwarded or any(item.startswith("--target=") for item in forwarded)
            has_dev_url = "--dev-url" in forwarded or any(item.startswith("--dev-url=") for item in forwarded)
            if args.verb in {"live", "live-generate"} and not has_target:
                cmd.extend(["--target", str(root)])
            if args.verb == "live" and not has_dev_url:
                cmd.append("--dev-url")
            elif args.verb == "live-generate" and not has_dev_url:
                cmd.extend(["--dev-url", dev_url])
            cmd.extend(forwarded)
            result = invoke(cmd, cwd=root, timeout=60, extra_env={"IMPECCABLE_DEV_URL_CANDIDATES": dev_url})
            if result.returncode:
                print(f"Native live command failed (exit {result.returncode}); inspect the local session without sharing its token.", file=sys.stderr)
                return 1
            safe = _safe_live_output(result.stdout)
            if safe:
                print(safe)
            else:
                print(f"Native {args.verb} completed for local dev URL {dev_url}; verify source diff and stop the owned live session when finished.")
            return 0
    except (RuntimeErrorWithMessage, OSError, ValueError) as exc:
        print(f"Design runtime: {exc}", file=sys.stderr)
        return 1
    return 1
