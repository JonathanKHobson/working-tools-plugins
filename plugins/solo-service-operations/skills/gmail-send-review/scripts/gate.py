#!/usr/bin/env python3
"""Local Gmail pre-send review receipts. No network, daemon, or email storage."""
from __future__ import annotations

import argparse
import base64
import fcntl
import hashlib
from email.header import decode_header, make_header
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
STATE = Path(os.environ.get('GMAIL_SEND_REVIEW_STATE', str(Path.home() / '.local' / 'share' / 'working-tools' / 'gmail-send-review')))
MATCHER = r'^(mcp__codex_apps__gmail[_.](send_email|send_draft|forward_emails)|gmail\.(send_email|send_draft|forward_emails))$'
SEND_RE = re.compile(MATCHER)
REVIEW_TTL = 1800
DRAFT_TTL = 120


class AuthoredHtml(HTMLParser):
    """Collect visible authored text, excluding conventional quoted history."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.text = []

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        attributes = dict(attrs)
        classes = attributes.get('class') or ''
        quoted = tag == 'blockquote' or 'gmail_quote' in classes.split()
        hidden = tag in {'script', 'style', 'head'}
        excluded = (self.stack[-1][1] if self.stack else False) or quoted or hidden
        if not excluded:
            for name in ('alt', 'title', 'aria-label'):
                value = attributes.get(name)
                if value:
                    self.text.append(value)
        if tag not in {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}:
            self.stack.append((tag, excluded))

    def handle_startendtag(self, tag, attrs):
        before = len(self.stack)
        self.handle_starttag(tag, attrs)
        if len(self.stack) > before:
            self.stack.pop()

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag.lower():
                del self.stack[index:]
                break

    def handle_data(self, data):
        if not self.stack or not self.stack[-1][1]:
            self.text.append(data)


def authored_text(value, mime_type):
    if mime_type == 'text/html':
        parser = AuthoredHtml()
        parser.feed(value)
        parser.close()
        return ''.join(parser.text)
    lines = []
    for line in value.splitlines():
        if (re.match(r'^\s*-{2,}\s*Forwarded message\s*-{2,}\s*$', line, re.I)
                or re.match(r'^\s*-{2,}\s*Original Message\s*-{2,}\s*$', line, re.I)
                or re.match(r'^\s*On .+ wrote:\s*$', line)):
            break
        if re.match(r'^\s*>', line):
            continue
        lines.append(line)
    return '\n'.join(lines)


def em_dash_error(tool, args, reviewed_draft=None):
    """Inspect only known authored subject and text MIME leaves."""
    op = operation(tool)
    if op == 'send_draft':
        if reviewed_draft is None:
            return None  # The hook sees only an ID; record_review requires a snapshot.
        source = reviewed_draft
    else:
        source = args
    if not isinstance(source, dict):
        raise ValueError('Reviewed message must be a JSON object.')
    subject = source.get('subject') or ''
    if not isinstance(subject, str):
        raise ValueError('Subject must be text.')
    try:
        decoded_subject = str(make_header(decode_header(subject)))
    except (ValueError, UnicodeError, LookupError) as exc:
        raise ValueError(f'Cannot inspect encoded subject: {exc}') from exc
    if '\u2014' in decoded_subject:
        return 'subject'

    def visit(part, path):
        if not isinstance(part, dict):
            raise ValueError('MIME part must be a JSON object.')
        mime_type = (part.get('mime_type') or '').lower().split(';', 1)[0]
        if mime_type.startswith('multipart/'):
            for index, child in enumerate(part.get('parts') or []):
                found = visit(child, f'{path}.parts[{index}]')
                if found:
                    return found
            return None
        if mime_type not in {'text/plain', 'text/html'} or part.get('content_disposition') == 'attachment' or part.get('filename'):
            return None
        body = part.get('body') or {}
        if not isinstance(body, dict):
            raise ValueError('MIME body must be a JSON object.')
        value = body.get('content')
        if value is not None and body.get('base64_url_content') is not None:
            raise ValueError(f'Cannot inspect ambiguous text body in {path}: both content and base64_url_content are set.')
        if value is None and body.get('base64_url_content') is not None:
            encoded = body['base64_url_content']
            try:
                raw = base64.b64decode(encoded + '=' * (-len(encoded) % 4), altchars=b'-_', validate=True)
                value = raw.decode(part.get('charset') or 'utf-8')
            except (ValueError, UnicodeError, LookupError, TypeError) as exc:
                raise ValueError(f'Cannot inspect text in {path}: {exc}') from exc
        if isinstance(value, str) and '\u2014' in authored_text(value, mime_type):
            return path
        return None

    payload = source.get('payload')
    return visit(payload, 'payload') if payload is not None else None


def reject_em_dash(location):
    return (f'Authored Gmail {location} contains an em dash. Revise the authored wording and review again. '
            'Preserve quoted or forwarded source material and attachments. If the user requested exact text, '
            'report the conflict; do not silently rewrite it or send it unchanged.')


def reply_route_error(tool, args):
    """The reply connector appends history after the reviewed payload."""
    if operation(tool) == 'send_email' and isinstance(args, dict) and args.get('reply_message_id'):
        return (
            'Direct Gmail replies append unreviewed quoted history. Use create_draft with the reply target, '
            'then update_draft with the intended MIME payload, preserving attachments and intentional quotes. '
            'Re-read the saved draft to verify its complete body, recipients and reply headers; review send_draft '
            'with --draft-verified and send only when authorized. This is an automatic agent repair, '
            'not a request for human approval. See ' + str(ROOT / 'SKILL.md') + '.')
    return None


def operation(tool):
    if not isinstance(tool, str) or not SEND_RE.fullmatch(tool):
        return None
    return re.split(r' gmail[_.]', ' ' + tool.replace('mcp__codex_apps__', ''))[-1]


def fingerprint(tool, args):
    if not operation(tool) or not isinstance(args, dict) or not args:
        raise ValueError('Expected a supported Gmail send tool and its exact nonempty arguments.')
    # Response projections do not affect the outgoing message.
    content = {k: v for k, v in args.items() if k != 'response_fields'}
    blob = json.dumps([operation(tool), content], sort_keys=True, separators=(',', ':'), ensure_ascii=False)
    return hashlib.sha256(blob.encode()).hexdigest()


def scoped_path(root, session):
    if not isinstance(session, str) or not session.strip():
        raise ValueError('A session ID is required; receipts cannot cross chats.')
    root.mkdir(mode=0o700, parents=True, exist_ok=True)
    return root / (hashlib.sha256(session.encode()).hexdigest() + '.json')


def write_state(path, data):
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix='.receipt-')
    try:
        with os.fdopen(fd, 'w') as f:
            json.dump(data, f, sort_keys=True)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def mutate(root, session, fn, now):
    path = scoped_path(root, session)
    with open(path.with_suffix('.lock'), 'a') as lock:
        os.chmod(lock.name, 0o600)
        fcntl.flock(lock, fcntl.LOCK_EX)
        try:
            state = json.loads(path.read_text()) if path.exists() else {}
            state = {k: v for k, v in state.items() if isinstance(v, dict) and v.get('expires', 0) > now}
        except (ValueError, TypeError):
            state = {}
        result = fn(state)
        write_state(path, state)
        return result


def record_review(root, session, tool, args, *, voice, audience, authorization,
                  skills_reviewed, draft_verified=False, reviewed_draft=None, now=None):
    if authorization != 'send':
        raise ValueError('Draft-only or approval-pending work cannot receive a send receipt.')
    if not skills_reviewed:
        raise ValueError('Apply the selected recipient voice guidance and prose review before recording a receipt.')
    if voice not in {'matched', 'user-supplied', 'unavailable'}:
        raise ValueError('Record the actual writing-style retrieval outcome.')
    if audience not in {'routine', 'communication-crafter', 'ux-research-follow-up'}:
        raise ValueError('Select the audience review actually completed.')
    route_error = reply_route_error(tool, args)
    if route_error:
        raise ValueError(route_error)
    op = operation(tool)
    if op == 'send_draft':
        if not draft_verified or not isinstance(reviewed_draft, dict):
            raise ValueError('Read the current saved draft in full and provide its reviewed snapshot before recording a receipt.')
        if (not isinstance(args, dict) or not isinstance(args.get('draft_id'), str) or not args['draft_id']
                or reviewed_draft.get('draft_id') != args['draft_id']
                or not isinstance(reviewed_draft.get('subject'), str)
                or not isinstance(reviewed_draft.get('payload'), dict)):
            raise ValueError('Reviewed draft snapshot must match draft_id and include its subject and full MIME payload.')
    location = em_dash_error(tool, args, reviewed_draft)
    if location:
        raise ValueError(reject_em_dash(location))
    key = fingerprint(tool, args)
    now = time.time() if now is None else now
    entry = {'expires': now + (DRAFT_TTL if op == 'send_draft' else REVIEW_TTL),
             'voice': voice, 'audience': audience, 'operation': op}
    mutate(root, session, lambda state: state.update({key: entry}), now)
    return key


def deny(reason):
    return {'hookSpecificOutput': {'hookEventName': 'PreToolUse',
            'permissionDecision': 'deny', 'permissionDecisionReason': reason}}


def before_send(event, root=STATE, now=None):
    tool = event.get('tool_name')
    if not operation(tool):
        return {}
    route_error = reply_route_error(tool, event.get('tool_input'))
    if route_error:
        return deny(route_error)
    now = time.time() if now is None else now
    session = event.get('session_id')
    try:
        location = em_dash_error(tool, event.get('tool_input'))
        if location:
            return deny(reject_em_dash(location))
        key = fingerprint(tool, event.get('tool_input'))
        def consume(state):
            entry = state.get(key)
            if entry and operation(tool) == 'send_draft':
                del state[key]  # A mutable saved draft requires a fresh read for every send attempt.
            return bool(entry)
        if mutate(root, session, consume, now):
            # Do not use permissionDecision=allow: writing review must not override
            # the user's normal tool approval policy.
            return {}
        return deny(
            'Gmail writing review is required before this send. This is an automatic agent review, '
            'not a request for human approval. Read ' + str(ROOT / 'SKILL.md') + '. '
            'Apply or reuse Write Like Me and natural-prose-editor for this exact message; '
            'use the audience specialist only when relevant. Record a review receipt with '
            f'session_id={session!r} and tool_name={tool!r}, then retry the authorized send. '
            'If the user asked for a draft or human approval, preserve that hold. '
            'Do not claim sent until Gmail confirms it.')
    except (OSError, ValueError, TypeError) as exc:
        return deny('Gmail review receipt unavailable: ' + str(exc) + '. Repair the local review check; do not bypass it.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--state-dir', type=Path, default=STATE)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('hook', help='Read the PreToolUse event from stdin.')
    review = sub.add_parser('review', help='Read exact Gmail arguments as JSON; for send_draft use an envelope with tool_input and reviewed_draft.')
    review.add_argument('--session', required=True)
    review.add_argument('--tool', required=True)
    review.add_argument('--voice', required=True, choices=['matched', 'user-supplied', 'unavailable'])
    review.add_argument('--audience', required=True, choices=['routine', 'communication-crafter', 'ux-research-follow-up'])
    review.add_argument('--authorization', required=True, choices=['send', 'hold'])
    review.add_argument('--skills-reviewed', action='store_true')
    review.add_argument('--draft-verified', action='store_true')
    args = parser.parse_args()
    try:
        payload = json.load(sys.stdin)
        if not isinstance(payload, dict):
            raise ValueError('Input must be a JSON object.')
        if args.command == 'hook':
            print(json.dumps(before_send(payload, args.state_dir)))
        else:
            reviewed_draft = None
            if operation(args.tool) == 'send_draft':
                reviewed_draft = payload.get('reviewed_draft')
                payload = payload.get('tool_input')
            key = record_review(args.state_dir, args.session, args.tool, payload,
                voice=args.voice, audience=args.audience, authorization=args.authorization,
                skills_reviewed=args.skills_reviewed, draft_verified=args.draft_verified,
                reviewed_draft=reviewed_draft)
            print(json.dumps({'review_recorded': True, 'fingerprint': key,
                              'next': 'Send the reviewed message if still authorized; verify the Gmail result.'}))
    except Exception as exc:
        if args.command == 'hook':
            print(json.dumps(deny('Gmail review hook could not read its input: ' + str(exc))))
            return 0
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
