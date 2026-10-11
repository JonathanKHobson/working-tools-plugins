#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
"""Optional UserPromptSubmit / Stop adapters and explicit quality attestations."""
from __future__ import annotations

import argparse
import json
import os
import sys

from quality_rules import detect_obligations, OBLIGATION_ORDER, OBLIGATION_LABELS, ROUTING_HINTS
from scope_state import MAX_BYTES, ScopeStore, StateError, scope_key, pending

CLOSEOUT = (
    'Closeout check for this chat: close finished scripts, dev servers, browser '
    'sessions and temporary helpers you actually started; verify exits with the '
    'owning native tools before claiming cleanup. Preserve ongoing authorized '
    'jobs, other chats\' work, protected services and platform-managed MCP '
    'connections. Age, low CPU, shared cwd and a common Codex parent do not '
    'prove chat ownership. If no task-owned resources remain, no cleanup action '
    'is needed. Check naming only at first substantive work or a scope change; '
    'preserve chosen/correct titles. Do not restart finished work, launch '
    'workers, message chats without authorization or make mandatory memory '
    'captures for closeout. Closeout delivery is a reminder, not proof of '
    'process cleanup. The agent must verify its resource exits; the hook does '
    'not own shared tool-server lifetimes.'
)


def read_payload(stream):
    raw = stream.read(MAX_BYTES + 1)
    if not raw or len(raw) > MAX_BYTES:
        raise ValueError('Missing or oversized input')
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError('Hook payload must be an object')
    return data


def text(value):
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return '\n'.join(filter(None, (text(item) for item in value)))
    if isinstance(value, dict):
        return text(value.get('text') or value.get('content') or value.get('value'))
    return ''


def prompt(payload):
    messages = payload.get('messages')
    if isinstance(messages, list):
        for item in reversed(messages):
            if isinstance(item, dict) and item.get('role') in ('user', 'human'):
                value = text(item.get('content'))
                if value:
                    return value
    for key in ('prompt', 'user_prompt', 'message', 'input', 'text'):
        value = text(payload.get(key))
        if value:
            return value
    return ''


def stop_result(payload, directory):
    if payload.get('stop_hook_active') is True:
        return None
    key = scope_key(payload)
    checks = pending(ScopeStore(directory, key).read()) if key else []
    if checks:
        labels = ', '.join(OBLIGATION_LABELS[name] for name in checks)
        hints = ' '.join(ROUTING_HINTS[name] for name in checks)
        return {'decision': 'block', 'reason':
                f'Codex artifact quality gate: pending {labels}. {hints} '
                'Use the configured codex_host_hooks.py quality mark command after review, '
                'or quality skip with a reason when inapplicable, before final. '
                'These are heuristic obligations; completion records your attestation.'}
    return {'continue': True, 'systemMessage': CLOSEOUT, 'suppressOutput': False}


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--state-dir', required=True,
                        help='Dedicated absolute state directory, private mode 0700; parent must exist')
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('prompt')
    sub.add_parser('stop')
    quality = sub.add_parser('quality')
    scope = quality.add_mutually_exclusive_group()
    scope.add_argument('--session-id', default=None)
    scope.add_argument('--turn-id', default=None)
    scope.add_argument('--scope-key', default=None, help='Opaque hash reported by status')
    actions = quality.add_subparsers(dest='action', required=True)
    actions.add_parser('status')
    actions.add_parser('clear')
    mark = actions.add_parser('mark')
    mark.add_argument('check', choices=OBLIGATION_ORDER)
    mark.add_argument('--reviewer', required=True)
    mark.add_argument('--evidence', required=True)
    skip = actions.add_parser('skip')
    skip.add_argument('check', choices=OBLIGATION_ORDER)
    skip.add_argument('--reason', required=True)
    return parser


def bounded_nonempty(value):
    if not value.strip() or len(value.encode()) > 4096:
        raise StateError('Review details must be nonempty and at most 4096 bytes')


def main(argv=None):
    args = build_parser().parse_args(argv)
    hook = args.command in ('prompt', 'stop')
    try:
        if hook:
            payload = read_payload(sys.stdin.buffer)
            expected = 'UserPromptSubmit' if args.command == 'prompt' else 'Stop'
            if payload.get('hook_event_name') != expected:
                raise ValueError('Unexpected hook event')
            if args.command == 'prompt':
                key, value = scope_key(payload), prompt(payload)
                if key and value:
                    ScopeStore(args.state_dir, key).detect(detect_obligations(value))
            else:
                result = stop_result(payload, args.state_dir)
                if result:
                    print(json.dumps(result, separators=(',', ':')))
            return 0
        key = args.scope_key or scope_key({
            'session_id': args.session_id or (None if args.turn_id else os.getenv('CODEX_SESSION_ID')),
            'turn_id': args.turn_id or os.getenv('CODEX_TURN_ID'),
        })
        store = ScopeStore(args.state_dir, key)
        if args.action == 'mark':
            bounded_nonempty(args.reviewer)
            bounded_nonempty(args.evidence)
            store.update(args.check, 'done')
        elif args.action == 'skip':
            bounded_nonempty(args.reason)
            store.update(args.check, 'skipped')
        elif args.action == 'clear':
            store.clear()
        value = store.read()
        print(json.dumps({'status': 'pending' if pending(value) else 'clear', 'scope_key': key,
                          'pending': pending(value), 'state': value, 'independent_verification': False}))
        return 0
    except (OSError, ValueError, TypeError, RecursionError):
        # Hook failures cannot turn corrupt input/state into an unscoped block.
        # Never echo exception text: it may include IDs, paths or payload values.
        print('Codex host hooks: unavailable input or private scoped state; no blocking decision issued.'
              if hook else 'Quality command failed: invalid scope, state or review details.', file=sys.stderr)
        return 0 if hook else 2


if __name__ == '__main__':
    raise SystemExit(main())
