"""Local descriptive text review; no network, classifier or automatic lexical edits.

Adapted from Jakeschincariol/linkedin-agent-skill's MIT li-human toolkit.
The original's authorship scores, format-character deletion and lexical rewriting
are deliberately not used. Source provenance/license is maintained by the Studio.
"""
from collections import Counter
import json
from pathlib import Path
import re
import statistics
import sys
import unicodedata

MAX_INPUT_BYTES = 2 * 1024 * 1024
DEFAULT_LEXICON = Path(__file__).with_name("stock_terms.json")
WORD = re.compile(r"\b[^\W\d_]+(?:['’][^\W\d_]+)*\b", re.UNICODE)
PROTECTED = re.compile(
    r"https?://[^\s<>\"`]+|www\.[^\s<>\"`]+"
    r"|[\w.+-]+@[\w.-]+\.[\w-]+"
    r"|\{\{[^\n]*?\}\}|\$\{[^\n]*?\}|\[[^\n\]]*\]|<[^\n>]*>",
    re.IGNORECASE,
)
QUOTES = {"‘": "'", "’": "'", "“": '"', "”": '"'}


def load_lexicon(path=DEFAULT_LEXICON):
    """Validate inert term data. Never compile regex supplied by a lexicon."""
    with Path(path).open("rb") as handle:
        raw = handle.read(256 * 1024 + 1)
    if len(raw) > 256 * 1024:
        raise ValueError("lexicon exceeds 256 KiB")
    data = json.loads(raw.decode("utf-8"))
    if not isinstance(data, dict) or type(data.get("version")) is not int or data.get("version") != 1:
        raise ValueError("lexicon requires version 1 and a terms array")
    terms = data.get("terms")
    if not isinstance(terms, list) or len(terms) > 500:
        raise ValueError("lexicon terms must be an array of at most 500 entries")
    seen = set()
    for entry in terms:
        if not isinstance(entry, dict):
            raise ValueError("each lexicon entry must be an object")
        for key in ("find", "suggestion", "family"):
            value = entry.get(key)
            if not isinstance(value, str) or len(value) > 200 or any(
                unicodedata.category(c).startswith("C") for c in value
            ):
                raise ValueError("lexicon fields must be short strings without controls")
        if not entry["find"].strip() or entry["find"].casefold() in seen:
            raise ValueError("lexicon find terms must be nonempty and unique")
        seen.add(entry["find"].casefold())
    return terms


def read_input(source):
    if source == "-":
        data = sys.stdin.buffer.read(MAX_INPUT_BYTES + 1)
    else:
        with Path(source).open("rb") as handle:
            data = handle.read(MAX_INPUT_BYTES + 1)
    if len(data) > MAX_INPUT_BYTES:
        raise ValueError("input exceeds 2 MiB")
    text = data.decode("utf-8")  # strict; preserves BOM and CRLF
    if "\x00" in text:
        raise ValueError("input contains NUL; use a UTF-8 prose file")
    return text


def validate_output(source, output):
    if output is None:
        return
    destination = Path(output)
    if source != "-":
        original = Path(source)
        if destination.resolve() == original.resolve() or (
            destination.exists() and original.samefile(destination)
        ):
            raise ValueError("output must not refer to the input path or inode")
    if destination.exists() or destination.is_symlink():
        raise ValueError("output already exists; choose a new path")


def emit(value, source="-", output=None):
    validate_output(source, output)
    encoded = value.encode("utf-8")
    if output:
        # Exclusive creation also prevents a race from overwriting another file.
        with Path(output).open("xb") as handle:
            handle.write(encoded)
    else:
        sys.stdout.buffer.write(encoded)


def protected_spans(text):
    """Conservative Markdown protection, including unfinished fenced code.

    This is not a full Markdown parser. It deliberately preserves complete
    bracketed spans (including link labels) and unmatched code fences.
    """
    spans = []
    fence = None
    start = 0
    offset = 0
    for line in text.splitlines(keepends=True):
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if fence is not None:
            if marker and marker.group(1)[0] == fence[0] and len(marker.group(1)) >= len(fence):
                # Closing fences contain no info string.
                if not line[marker.end():].strip():
                    spans.append((start, offset + len(line)))
                    fence = None
        elif marker:
            fence, start = marker.group(1), offset
        elif line.startswith("    ") or line.startswith("\t"):
            spans.append((offset, offset + len(line)))
        offset += len(line)
    if fence is not None:
        spans.append((start, len(text)))
    # Backtick runs must close with the same run length; do not consume a
    # longer closing run's first characters as a short inline-code delimiter.
    for match in re.finditer(r"(?<!`)(`+)(?!`)([\s\S]*?)(?<!`)\1(?!`)", text):
        spans.append(match.span())
    spans.extend(match.span() for match in PROTECTED.finditer(text))
    merged = []
    for start, end in sorted(spans):
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(end, merged[-1][1]))
        else:
            merged.append((start, end))
    return merged


def prose_mask(text):
    chars = list(text)
    for start, end in protected_spans(text):
        for position in range(start, end):
            if chars[position] not in "\r\n":
                chars[position] = " "
    return "".join(chars)


def location(text, position):
    return {
        "offset": position,
        "line": text.count("\n", 0, position) + 1,
        "column": position - text.rfind("\n", 0, position),
    }


def clean_text(text, cleanup=False, ascii_quotes=False):
    """Preserve by default; narrow explicit character changes with source offsets."""
    mask = prose_mask(text)
    changes, output = [], []
    for position, char in enumerate(text):
        replacement, reason = char, None
        if cleanup and position == 0 and char == "\ufeff":
            replacement, reason = "", "remove leading BOM (explicit cleanup)"
        elif mask[position] == char:
            if cleanup and char in {"\u00ad", "\u200b"}:
                before = text[position - 1] if position else ""
                after = text[position + 1] if position + 1 < len(text) else ""
                # No broad Cf deletion. Script/emoji/RTL controls are untouched.
                # The optional operation is confined to Latin letters or an
                # existing adjacent ASCII whitespace boundary.
                if (before.isascii() and before.isalpha() and after.isascii() and after.isalpha()) or (
                    before in " \t\r\n" and bool(before)
                ) or (after in " \t\r\n" and bool(after)):
                    replacement, reason = "", "remove optional prose separator (explicit cleanup)"
            if ascii_quotes and char in QUOTES:
                replacement, reason = QUOTES[char], "ASCII quote preference (explicit option)"
        output.append(replacement)
        if reason:
            changes.append({**location(text, position), "before": char, "after": replacement, "reason": reason})
    return {"before": text, "after": "".join(output), "changes": changes}


def stock_matches(text, terms):
    prose = prose_mask(text)
    matches = []
    for entry in terms:
        # Escape literal data, allow ordinary spaces only, and bound words
        # without losing a phrase's terminal question mark.
        pattern = r"(?<!\w)" + re.escape(entry["find"]).replace(r"\ ", r"[ \t]+") + r"(?!\w)"
        for match in re.finditer(pattern, prose, re.IGNORECASE):
            matches.append({**location(text, match.start()), "text": match.group(),
                            "candidate": entry["find"], "suggestion": entry["suggestion"],
                            "family": entry["family"]})
    return sorted(matches, key=lambda item: (item["offset"], -len(item["text"])))


def descriptive_review(text, terms, language="und"):
    prose = prose_mask(text)
    tokens = WORD.findall(prose)
    english = language.lower().split("-")[0] == "en"
    # Requiring a declared English context avoids pretending that a Latin
    # alphabet is a language identification method.
    sufficient = english and len(tokens) >= 25
    lengths = [len(WORD.findall(s)) for s in re.split(r"[.!?]+(?:\s+|$)|[\r\n]+", prose) if WORD.search(s)]
    sentence = {"status": "observed" if sufficient and len(lengths) >= 4 else "unknown",
                "approximate_sentence_count": len(lengths),
                "note": "English punctuation heuristic; no preferred variation or quality threshold. Short or undeclared/non-English samples are unknown."}
    if sentence["status"] == "observed":
        sentence.update({"approximate_word_lengths": lengths, "mean": round(statistics.mean(lengths), 3),
                         "population_stddev": round(statistics.pstdev(lengths), 3)})
    numbers = [{**location(text, m.start()), "text": m.group()} for m in re.finditer(r"(?<!\w)\d+(?:[.,]\d+)*(?:%)?(?!\w)", prose)]
    names = [{**location(text, m.start()), "text": m.group()} for m in re.finditer(r"\b[A-Z][a-z]{2,}\b", prose)] if english else []
    specificity = {"status": "observed" if sufficient else "unknown", "number_candidates": numbers,
                   "capitalized_word_candidates": names,
                   "note": "These are surface candidates, not verified facts or names. Absence does not imply vagueness. Never add numbers, names or experience to satisfy a panel."}
    counts = Counter(c for c in text if unicodedata.category(c) == "Cf" or c in "—–‘’“”…\u00a0\u202f\u2009\u2007")
    typography = {"status": "observed", "characters": [
        {"codepoint": f"U+{ord(c):04X}", "name": unicodedata.name(c, "UNNAMED"), "count": count}
        for c, count in sorted(counts.items())],
        "note": "Typography and Unicode may carry meaning, script shaping, directionality or emoji composition. Their presence says nothing about origin; preservation is the default."}
    voice = {"status": "observed" if sufficient else "unknown",
             "note": "English surface cues, not an authentic voice baseline. Formality, purposeful repetition and contractions can all fit a writer; no target density applies."}
    if sufficient:
        voice.update({"contractions": len(re.findall(r"\b\w+['’](?:s|t|re|ve|ll|d|m)\b", prose, re.IGNORECASE)),
                      "personal_pronouns": len(re.findall(r"\b(?:i|me|my|mine|we|us|our|you|your)\b", prose, re.IGNORECASE)),
                      "bullet_line_word_lengths": [len(WORD.findall(m)) for m in re.findall(r"(?m)^\s*[-*•]\s+(.+)$", prose)],
                      "repeated_frame_candidates": [{**location(text, m.start()), "text": m.group()} for m in re.finditer(
                          r"\bnot only\b[^.!?\n]{2,80}\bbut also\b|\b(?:here['’]s what (?:i|we) learned)\b", prose, re.IGNORECASE)]})
    return {"language_context": language, "approximate_word_count": len(tokens),
            "protected_span_count": len(protected_spans(text)),
            "panels": {"sentence_variation": sentence, "specificity_candidates": specificity,
                       "stock_terms": {"status": "observed", "matches": stock_matches(text, terms),
                                       "note": "Literal English lexicon candidates only; suggestions may change meaning or register. Review in context, keep when accurate, and never substitute automatically."},
                       "typography_unicode": typography, "voice_cues": voice},
            "limits": "Descriptive local observations only. No authorship inference, detector verdict, writing-quality score, performance forecast or release approval."}


def render_review(review):
    lines = ["LOCAL TEXT OBSERVATIONS", review["limits"], f"Language context: {review['language_context']}"]
    for name, panel in review["panels"].items():
        lines.append(f"\n{name.replace('_', ' ').upper()}: {panel['status']}")
        lines.append(json.dumps({k: v for k, v in panel.items() if k not in {"status", "note"}}, ensure_ascii=False))
        lines.append(panel["note"])
    return "\n".join(lines) + "\n"
