#!/usr/bin/env python3
"""Report five descriptive text panels; never classify authorship or quality."""
import argparse
import json
from text_review import descriptive_review, emit, load_lexicon, read_input, render_review, validate_output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", default="-", help="UTF-8 file, or - for stdin")
    parser.add_argument("compare", nargs="?", help="optional second file for descriptive before/after")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--language", default="und", help="declared language context; English-specific observations require en")
    parser.add_argument("--lexicon", help="optional validated inert lexicon JSON")
    parser.add_argument("-o", "--out", help="new report file; existing files are never overwritten")
    args = parser.parse_args()
    try:
        if args.input == "-" and args.compare == "-":
            raise ValueError("stdin may be read only once in a comparison")
        validate_output(args.input, args.out)
        if args.compare:
            validate_output(args.compare, args.out)
        terms = load_lexicon(args.lexicon) if args.lexicon else load_lexicon()
        before = descriptive_review(read_input(args.input), terms, args.language)
        before["source"] = args.input
        result = before
        if args.compare:
            after = descriptive_review(read_input(args.compare), terms, args.language)
            after["source"] = args.compare
            result = {"before": before, "after": after, "limits": "Comparisons describe observations; change is not evidence of better writing, authorship or a detector result."}
        if args.json:
            output = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
        elif args.compare:
            output = "BEFORE\n" + render_review(before) + "\nAFTER\n" + render_review(after) + result["limits"] + "\n"
        else:
            output = render_review(before)
        emit(output, args.input, args.out)
    except (OSError, UnicodeError, ValueError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
