#!/usr/bin/env python3
"""Preserve UTF-8 prose; optionally apply narrow, reported character cleanup."""
import argparse
import difflib
import json
import sys
from text_review import clean_text, emit, load_lexicon, read_input, stock_matches, validate_output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", default="-", help="UTF-8 file, or - for stdin")
    parser.add_argument("-o", "--out", help="new output file; existing files are never overwritten")
    parser.add_argument("--cleanup", action="store_true", help="opt in to leading BOM and narrow prose SHY/ZWSP removal")
    parser.add_argument("--ascii-quotes", action="store_true", help="opt in to ASCII curly-quote delimiters in unprotected prose")
    parser.add_argument("--json", action="store_true", help="emit before/after, exact changes and report-only lexical candidates")
    parser.add_argument("--report", action="store_true", help="report changes/candidates to stderr")
    parser.add_argument("--diff", action="store_true", help="also show a before/after unified diff on stderr")
    parser.add_argument("--lexicon", help="optional validated inert lexicon JSON")
    args = parser.parse_args()
    try:
        validate_output(args.input, args.out)
        terms = load_lexicon(args.lexicon) if args.lexicon else load_lexicon()
        result = clean_text(read_input(args.input), args.cleanup, args.ascii_quotes)
        result["lexical_candidates"] = stock_matches(result["before"], terms)
        result["limits"] = "No lexical substitutions, authorship judgments or detector guarantees. Review each explicit change before using the output."
        value = json.dumps(result, ensure_ascii=False, indent=2) + "\n" if args.json else result["after"]
        emit(value, args.input, args.out)
        # An applied change is always reported, including without --report.
        if result["changes"] or args.report:
            sys.stderr.write(json.dumps({"changes": result["changes"], "lexical_candidates": result["lexical_candidates"] if args.report else []}, ensure_ascii=False, indent=2) + "\n")
        if args.diff:
            sys.stderr.writelines(difflib.unified_diff(result["before"].splitlines(keepends=True), result["after"].splitlines(keepends=True), fromfile="before", tofile="after"))
    except (OSError, UnicodeError, ValueError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
