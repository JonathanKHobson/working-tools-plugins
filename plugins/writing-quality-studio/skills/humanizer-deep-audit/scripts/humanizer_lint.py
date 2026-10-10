#!/usr/bin/env python3
"""Flag common machine-like writing, formatting, and interface residue.

The rules are editorial cues. They do not determine authorship.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Rule:
    category: str
    severity: str
    pattern: str
    message: str
    suggestion: str
    flags: int = re.IGNORECASE


RULES = (
    Rule("em_dash", "info", r"—", "Em dash found.", "Check density, function, spacing, cadence, and house style."),
    Rule("spaced_em_dash", "low", r"\s—\s", "Spaced em dash found.", "Confirm the destination style and whether a period, colon, comma, or parentheses fits better."),
    Rule("ai_vocabulary", "low", r"\b(?:additionally|bolstered|crucial|delve|emphasizing|enduring|enhance|fostering|garner|interplay|intricate|intricacies|meticulous(?:ly)?|pivotal|showcas(?:e|es|ing)|tapestry|testament|underscor(?:e|es|ing)|vibrant)\b", "A vocabulary watch-list item appears.", "Judge density and context; replace the underlying abstraction, not merely the word."),
    Rule("unsupported_significance", "medium", r"\b(?:stands?|serves?) as (?:a |an )?(?:testament|reminder|symbol)|\b(?:pivotal|vital|crucial|significant|key) (?:role|moment|turning point|milestone)|\b(?:enduring|lasting) legacy\b|\b(?:evolving|broader) landscape\b|\bindelible mark\b|\bsetting the stage\b", "Importance or legacy language may outrun the evidence.", "Name the concrete consequence and source, or cut the claim."),
    Rule("generic_analysis", "medium", r"(?:,|—|--)\s*(?:highlighting|underscoring|emphasizing|reflecting|symbolizing|ensuring|cultivating|fostering|encompassing|enhancing|contributing to|aligning with|resonating with)\b", "A fact is followed by a broad interpretation.", "Stop at the fact, add sourced evidence, or attribute the interpretation."),
    Rule("puffery", "low", r"\b(?:boasts?|vibrant|renowned|groundbreaking|seamless|world[- ]class|breathtaking|nestled|rich (?:heritage|history|culture)|diverse array|natural beauty|unwavering commitment|powerful emotional presence)\b", "Promotional or brochure language found.", "Replace praise with an observable feature, action, condition, or result."),
    Rule("vague_attribution", "medium", r"\b(?:experts|observers|critics|researchers|scholars|industry reports|some commentators|several sources|many believe) (?:say|argue|note|have cited|suggest|believe|contend)\b", "Unnamed authority found.", "Name the source, count sources accurately, qualify the claim, or remove it."),
    Rule("inflated_consensus", "medium", r"\bwidely (?:regarded|recognized|considered|interpreted|believed|viewed)\b|\bbroad consensus\b|\bnumerous (?:sources|outlets|publications|experts)\b", "Consensus or quantity may be overstated.", "Verify how many independent sources support the exact claim."),
    Rule("coverage_performance", "low", r"\b(?:independent coverage|prominent media outlets|national and regional media|trade publications|profiled in|featured in numerous|high-quality independent sources)\b", "The prose may perform notability instead of reporting source content.", "State what the source establishes and why it matters here."),
    Rule("social_presence", "low", r"\bmaintains? (?:an? )?(?:active|strong|robust) (?:social media|digital|online) presence\b", "Digital-presence boilerplate found.", "Name the relevant use of the account or delete the sentence."),
    Rule("formulaic_outlook", "medium", r"\b(?:challenges and (?:legacy|future (?:directions|prospects|outlook))|despite (?:these|its) challenges|future outlook|well[- ]positioned to thrive|remain relevant for generations)\b", "Formulaic challenge/future framing found.", "Replace with the real constraint, decision, date, test, or unresolved question."),
    Rule("conclusion_restatement", "low", r"^(?:#{1,6}\s*)?(?:in )?(?:summary|conclusion|overall)(?::|\b)", "Summary or conclusion template found.", "Check whether it adds a consequence, decision, limit, or merely repeats the body.", re.IGNORECASE | re.MULTILINE),
    Rule("copula_evasion", "low", r"\b(?:serves?|stands?|functions?|operates?|marks?) as (?:a|an|the)\b|\b(?:boasts?|features?|maintains?|offers?) (?:a|an|the)\b|\brefers to (?:a|an|the)\b", "A plain is/are/has construction may have been inflated.", "Test the simpler copula; keep the richer verb only when it adds meaning."),
    Rule("negative_parallelism", "low", r"\bnot (?:only|just|merely)\b.{0,100}\bbut (?:also )?\b|\bthis (?:isn't|is not)\b.{0,80}\b(?:it's|it is)\b|\bno [^,.]{1,35}, no [^,.]{1,35}, (?:just|only)\b", "Formulaic negative parallelism found.", "State the concrete distinction directly unless correcting a real misconception."),
    Rule("reversed_contrast", "info", r"\b(?:prioritizing|emphasizing|favoring|focusing on)\b.{0,100}\brather than\b", "A reversed contrast template appears.", "Confirm that both sides are real alternatives supported by the source."),
    Rule("rule_of_three", "info", r"\b[^,.;:\n]{1,40},\s+[^,.;:\n]{1,40},\s+and\s+[^,.;:\n]{1,40}(?:[.;]|$)", "A three-part sequence appears.", "Check whether the material naturally has three parts or the list is decorative."),
    Rule("transition_opener", "info", r"^(?:Additionally|Moreover|Furthermore|Consequently|Notably|Importantly),", "A stock transition opens the sentence.", "Keep it only if it names a real relationship and is not part of a repeated pattern.", re.IGNORECASE | re.MULTILINE),
    Rule("filler_verb", "low", r"\b(?:serves? to|is in the process of|puts? (?:an )?emphasis on|provides? (?:a |an )?means of|facilitates? the (?:process of )?)\b", "Potential filler verb phrase found.", "Use the direct verb if it preserves meaning."),
    Rule("nominalization_stack", "low", r"\b(?:implementation|facilitation|enhancement|optimization|utilization|operationalization) of (?:the )?\w+(?:\s+\w+){0,3}", "A nominalization may hide the actor and action.", "Restore who did what, under which condition, with what result."),
    Rule("overhedging", "low", r"\b(?:I would like to suggest|it seems to me that|may possibly|might perhaps|could potentially perhaps|it may be possible that)\b", "Stacked or ceremonial hedge found.", "Keep only the uncertainty the evidence requires."),
    Rule("title_case_heading", "low", r"^#{1,6}\s+(?:[A-Z][^\s]*\s+){2,}[A-Z][^\s]*\s*$", "Possible title-case Markdown heading found.", "Match destination heading style; many systems prefer sentence case.", re.MULTILINE),
    Rule("markdown_bold", "info", r"\*\*[^*\n]+\*\*", "Bold Markdown found.", "Confirm the destination supports Markdown and that the emphasis aids scanning."),
    Rule("inline_header_list", "low", r"^\s*(?:[-*+•]|\d+[.)])\s+\*\*[^*\n]+(?::\*\*|\*\*\s*:)[ \t]+", "Label-colon list item found.", "Use this only for a genuine mapping; otherwise restore prose or a real table.", re.MULTILINE),
    Rule("emoji_formatting", "low", r"^(?:#{1,6}\s*)?[\U0001F300-\U0001FAFF\u2600-\u27BF]\ufe0f?\s*", "Emoji appears to format a heading or line.", "Keep only when the destination and function justify it.", re.MULTILINE),
    Rule("thematic_break", "info", r"^(?:---+|\*\*\*+|___+)\s*$", "Thematic break found.", "Check whether it marks a real division or mechanically precedes a heading.", re.MULTILINE),
    Rule("curly_quotes", "info", r"[“”‘’]", "Curly quotation or apostrophe found.", "Check consistency and destination syntax; curly quotes are normal in typeset prose."),
    Rule("collaborative_residue", "medium", r"\b(?:I hope this helps|Of course!|Certainly!|You're absolutely right|Would you like (?:me )?to|Is there anything else|Let me know if|Here is a (?:detailed|comprehensive) (?:overview|breakdown))\b", "Prompt-recipient or canned-helpfulness residue found.", "Remove the conversation and deliver the actual content."),
    Rule("cutoff_disclaimer", "high", r"\b(?:as of my last (?:knowledge|training) update|up to my last training update|my knowledge cutoff|I (?:do not|don't) have access to current|based on (?:the )?(?:provided|available) search results)\b", "Model limitation residue found.", "State the real evidence boundary and date instead."),
    Rule("unsupported_absence", "medium", r"\b(?:not widely (?:available|documented|disclosed)|details (?:are|remain) (?:limited|scarce)|specific (?:details|information) (?:are|is) limited|maintains? a low profile|keeps? (?:their|his|her) personal (?:life|details) private)\b", "Absence or privacy may be inferred from failed retrieval.", "Say only what the supplied sources do not cover; do not infer motive or nonexistence."),
    Rule("placeholder", "high", r"\[(?:Your Name|Company|Email Address|insert [^\]]+|link)\]|\b(?:20\d{2}-[Xx]{2}-[Xx]{2}|YYYY-MM-DD|INSERT_[A-Z0-9_]+|PASTE_[A-Z0-9_]+_HERE|SOURCE_PUBLISHER|TBD|TK)\b", "Unfilled placeholder found.", "Block release until the real value is supplied or remove the dependent claim."),
    Rule("ai_markup", "high", r"(?:contentReference|oaicite|oai_citation|turn\d+(?:search|image|news|file)\d+|attributableIndex|\[cite:\s*\d|\[span_\d+\]|grok[_-](?:card|render_citation_card_json)|【\d+†L\d|\[(?:attached_file|web):\d+\]|ppl-ai-file-upload|:::?writing\{)", "Internal model or interface artifact found.", "Recover and verify the intended source or object before removing the artifact."),
    Rule("tracking_parameter", "medium", r"(?:utm_source=(?:chatgpt\.com|openai|copilot\.com)|referrer=grok\.com)", "Model-associated tracking parameter found.", "Verify the clean source URL, then remove unnecessary tracking."),
    Rule("prompt_refusal", "high", r"\b(?:as an AI language model|as a large language model|I (?:can't|cannot) directly|I'm sorry, but I cannot)\b", "Prompt-refusal residue found.", "Remove the model conversation and complete or appropriately scope the deliverable."),
    Rule("didactic_disclaimer", "low", r"\b(?:it is|it's) (?:important|critical|crucial) to (?:note|remember|consider)\b|\bit is worth noting\b", "Didactic disclaimer found.", "State the relevant condition or exception directly."),
    Rule("policy_assurance", "medium", r"\b(?:ensure[ds]?|revised|improved).{0,80}\b(?:adheres? to|complies? with|in compliance with|neutral(?:ity| tone)|encyclopedic tone|verifiability)\b", "Canned compliance assurance found.", "Name the exact change and the exact rule or reader benefit."),
    Rule("preservation_assurance", "low", r"\b(?:while )?(?:preserv(?:e|ed|ing)|retain(?:ed|ing)) (?:the )?(?:original|existing|all|key)\b", "Prompt-constraint language about unchanged material found.", "Mention preservation only when reviewers need that information."),
)

SEVERITY_ORDER = {"info": 0, "low": 1, "medium": 2, "high": 3}
COMPOUND = re.compile(r"(?<![\w-])[A-Za-z]{2,}(?:-[A-Za-z]{2,})+(?![\w-])")
COMPOUND_WINDOW = 220
COMPOUND_COUNT = 4


def read_text(path: str) -> tuple[str, str]:
    if path == "-":
        return sys.stdin.read(), "stdin"
    source = Path(path)
    return source.read_text(encoding="utf-8"), str(source)


def location(text: str, index: int) -> tuple[int, int]:
    before = text[:index]
    return before.count("\n") + 1, index - before.rfind("\n")


def findings(text: str, rules: Iterable[Rule], *, include_compound: bool = True) -> list[dict[str, object]]:
    lines = text.splitlines()
    results: list[dict[str, object]] = []
    for rule in rules:
        for match in re.finditer(rule.pattern, text, flags=rule.flags):
            line, column = location(text, match.start())
            context = lines[line - 1].strip() if lines and line <= len(lines) else ""
            results.append({
                "category": rule.category,
                "severity": rule.severity,
                "line": line,
                "column": column,
                "match": match.group(0),
                "message": rule.message,
                "suggestion": rule.suggestion,
                "context": context,
            })
    if include_compound:
        results.extend(compound_stack_findings(text, lines))
    return sorted(results, key=lambda item: (int(item["line"]), int(item["column"]), str(item["category"])))


def compound_stack_findings(text: str, lines: list[str]) -> list[dict[str, object]]:
    """Find four prose compounds that fit together in a sliding sentence window.

    Periods, question/exclamation marks, and line breaks delimit this heuristic's
    sentences. It does not parse abbreviations or protected Markdown/code spans.
    """
    results: list[dict[str, object]] = []
    for sentence in re.finditer(r"[^.!?\n]+", text):
        compounds = list(COMPOUND.finditer(sentence.group()))
        for first, last in zip(compounds, compounds[COMPOUND_COUNT - 1:]):
            if last.end() - first.start() > COMPOUND_WINDOW:
                continue
            offset = sentence.start() + first.start()
            line, column = location(text, offset)
            results.append({
                "category": "compound_stack",
                "severity": "low",
                "line": line,
                "column": column,
                "match": sentence.group()[first.start():last.end()],
                "message": "Four hyphenated prose compounds appear close together.",
                "suggestion": "Check whether the modifiers clarify the point; keep useful terms and ordinary hyphens.",
                "context": lines[line - 1].strip() if lines and line <= len(lines) else "",
            })
            break
    return results


def render_markdown(source: str, results: list[dict[str, object]]) -> str:
    lines = [f"# Humanizer lint: `{source}`", "", "Flags are revision cues, not proof of authorship.", ""]
    if not results:
        return "\n".join(lines + ["No configured cues found."])
    counts: dict[str, int] = {}
    for item in results:
        counts[str(item["category"])] = counts.get(str(item["category"]), 0) + 1
    lines.append("Summary: " + ", ".join(f"`{key}` {value}" for key, value in sorted(counts.items())))
    lines.extend(["", "| Location | Severity | Category | Cue | Suggested check |", "| --- | --- | --- | --- | --- |"])
    for item in results:
        cue = str(item["match"]).replace("|", "\\|").replace("\n", " ")
        suggestion = str(item["suggestion"]).replace("|", "\\|")
        lines.append(f"| {item['line']}:{item['column']} | {item['severity']} | {item['category']} | {cue} | {suggestion} |")
    return "\n".join(lines)


def render_text(source: str, results: list[dict[str, object]]) -> str:
    if not results:
        return f"{source}: no configured cues found (not an authorship verdict)."
    lines = [f"{source}: {len(results)} revision cue(s); not an authorship verdict."]
    for item in results:
        lines.append(f"{item['line']}:{item['column']} [{item['severity']}] {item['category']}: {item['message']} Matched: {item['match']!r}. {item['suggestion']}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Flag writing and interface residue without scoring authorship.")
    parser.add_argument("path", nargs="?", help="UTF-8 text file, or - for stdin")
    parser.add_argument("--format", choices=("text", "markdown", "json"), default="text")
    parser.add_argument("--only", help="Comma-separated categories to include")
    parser.add_argument("--ignore", help="Comma-separated categories to exclude")
    parser.add_argument("--fail-on", choices=tuple(SEVERITY_ORDER), help="Exit 1 if a cue meets this severity")
    parser.add_argument("--list-rules", action="store_true", help="List configured categories and exit")
    args = parser.parse_args()
    if args.list_rules:
        for rule in RULES:
            print(f"{rule.category}\t{rule.severity}\t{rule.message}")
        print("compound_stack\tlow\tFour hyphenated prose compounds appear close together.")
        return 0
    if not args.path:
        parser.error("path is required unless --list-rules is used")
    text_value, source = read_text(args.path)
    only = {item.strip() for item in args.only.split(",")} if args.only else None
    ignore = {item.strip() for item in args.ignore.split(",")} if args.ignore else set()
    rules = [rule for rule in RULES if (only is None or rule.category in only) and rule.category not in ignore]
    results = findings(text_value, rules, include_compound=(only is None or "compound_stack" in only) and "compound_stack" not in ignore)
    if args.format == "json":
        print(json.dumps({"source": source, "disclaimer": "Revision cues only; not an authorship verdict.", "findings": results}, indent=2))
    elif args.format == "markdown":
        print(render_markdown(source, results))
    else:
        print(render_text(source, results))
    return 1 if args.fail_on and any(SEVERITY_ORDER[str(item["severity"])] >= SEVERITY_ORDER[args.fail_on] for item in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
