#!/usr/bin/env python3
"""Manual project evidence cards. Previews print to stdout; save requires confirmation."""
import argparse
import json
from pathlib import Path
from card_model import MAX_BYTES, apply_review, nominate, require, validate_card
from record_store import save


def read_input(path, opt_in):
    require(opt_in is True, 'Explicit --opt-in required before reading selected records')
    path = Path(path)
    require(path.is_file() and not path.is_symlink(), 'Input must be a regular selected file, not a symlink')
    require(path.stat().st_size <= MAX_BYTES, 'Input exceeds 512 KB')
    return json.loads(path.read_text())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ('nominate', 'validate', 'review', 'save'):
        cmd = sub.add_parser(name)
        cmd.add_argument('input', type=Path)
        cmd.add_argument('--opt-in', action='store_true')
        if name == 'review':
            cmd.add_argument('--decision', type=Path, required=True)
            cmd.add_argument('--confirm', action='store_true')
        if name == 'save':
            cmd.add_argument('--project-root', type=Path, required=True)
            cmd.add_argument('--store', type=Path, required=True)
            cmd.add_argument('--confirm', action='store_true')
    args = parser.parse_args()
    try:
        value = read_input(args.input, args.opt_in)
        if args.command == 'nominate':
            result = nominate(value, args.opt_in)
        elif args.command == 'validate':
            card = validate_card(value, args.opt_in)
            result = {'valid': True, 'card_id': card['card_id'], 'state': card['lifecycle'], 'holds': card['holds'], 'claim_decisions': card['review']['claim_decisions'], 'accepted_claim_ids': card['accepted_claim_ids'], 'allowed_reviewed_wording': {c['id']: c['allowed_wording'] for c in card['claims'] if c['id'] in card['accepted_claim_ids']}}
        elif args.command == 'review':
            result = apply_review(value, read_input(args.decision, args.opt_in), args.opt_in, args.confirm)
        else:
            result = save(value, args.project_root, args.store, args.opt_in, args.confirm)
    except (ValueError, OSError, TypeError, KeyError, RecursionError):
        # Do not echo private malformed input, filenames or parser fragments.
        parser.exit(2, 'Evidence review refused: check opt-in, confirmation, input schema, permissions, evidence holds and selected project destination.\n')
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
