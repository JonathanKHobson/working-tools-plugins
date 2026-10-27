"""Portable stdlib CLI for explicit efficient implementation state and reports."""

import argparse
import json
import sys

# Read-only invocations must not create plugin-side bytecode caches.
sys.dont_write_bytecode = True

from hooks import EVENTS, handle, read_payload
from scan import debt_ledger, reuse_map
from state import MODES, Session, config_dir, default_mode, project_root, set_default


def parser():
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--state-dir", help="private state location; defaults to recipient config directory")
    commands = result.add_subparsers(dest="command", required=True)
    session = commands.add_parser("session", help="explicit state for one project and session ID")
    session.add_argument("action", choices=("status", "set", "off", "reopen"))
    session.add_argument("mode", nargs="?", choices=MODES)
    session.add_argument("--root", required=True)
    session.add_argument("--session", required=True)
    session.add_argument("--ready", action="store_true", help="contract ambiguity was resolved by the caller")
    session.add_argument("--scope", help="bounded task identifier, revalidated by caller on rescope")
    accepted = session.add_mutually_exclusive_group()
    accepted.add_argument("--contract", help="existing bounded project-relative contract file")
    accepted.add_argument("--acceptance", help="short private acceptance for a conversational contract")
    default = commands.add_parser("default", help="read preference; only an explicit mode writes it")
    default.add_argument("mode", nargs="?", choices=MODES)
    for name in ("map", "debt"):
        report = commands.add_parser(name, help="on-demand read-only regex report")
        report.add_argument("--root", required=True)
        report.add_argument("--max-files", type=int, default=4000)
        report.add_argument("--max-entries", type=int, default=20000)
        report.add_argument("--max-depth", type=int, default=6)
        report.add_argument("--max-bytes", type=int, default=8388608)
        report.add_argument("--max-chars", type=int, default=6000 if name == "map" else 12000)
        if name == "debt":
            report.add_argument("--marker", default="shortcut")
            report.add_argument("--import-upstream-marker", action="store_true", help="also report legacy ponytail: comments")
    hook = commands.add_parser("hook", help="optional bounded stdin adapter; never registers global hooks")
    hook.add_argument("event", choices=EVENTS)
    hook.add_argument("--root")
    hook.add_argument("--session")
    hook.add_argument("--host", choices=("generic", "codex"), default="generic",
                      help="explicit host input contract; Codex subagent session_id identifies its parent")
    return result


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        directory = config_dir(args.state_dir)
        if args.command == "hook":
            try:
                value = handle(args.event, read_payload(), directory, root=args.root,
                               session_id=args.session, host=args.host)
                if value:
                    print(json.dumps(value, ensure_ascii=True))
            except Exception:
                # Lifecycle integration is optional: malformed/unavailable state must not block the host.
                pass
            return 0
        if args.command == "default":
            value = {"default_mode": set_default(directory, args.mode) if args.mode else default_mode(directory),
                     "activates_session": False}
        elif args.command == "session":
            session = Session(directory, args.root, args.session)
            if args.action == "set":
                value = session.set(args.mode, ready=args.ready, scope=args.scope,
                                    contract=args.contract, acceptance=args.acceptance)
            elif args.action in {"off", "reopen"}:
                value = session.off(args.action)
            else:
                value = session.status(args.scope)
        else:
            bounds = {"max_files": args.max_files, "max_entries": args.max_entries,
                      "max_depth": args.max_depth, "max_bytes": args.max_bytes, "max_chars": args.max_chars}
            root = project_root(args.root)
            value = (reuse_map(root, **bounds) if args.command == "map" else
                     debt_ledger(root, marker=args.marker, import_upstream=args.import_upstream_marker, **bounds))
        print(json.dumps(value, ensure_ascii=True, indent=2))
        return 0
    except (OSError, ValueError) as error:
        print("efficient-implementation: " + str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
