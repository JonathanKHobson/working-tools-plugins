#!/usr/bin/env python3
"""Bounded, read-only CSS var contract check; never executes source code.

Checks CSS files and HTML style blocks/attributes. Directory inputs collect these
files in sorted order, not runtime load order. Exact selectors and unconditional
:root/html declarations are understood; unresolved DOM/cascade cases are limits.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from html.parser import HTMLParser
import json
from pathlib import Path
import re

NAME = re.compile(r'--[A-Za-z_][A-Za-z0-9_-]*\Z')
LIMITATIONS = [
    'Static scan does not prove cascade, computed styles, DOM inheritance, or rendering.',
    'Only CSS and HTML style blocks/attributes are scanned; JS-generated styles beyond fixed-name style.setProperty hints, imports, external stylesheets, escaped/non-ASCII token names, and CSS nesting need separate review.',
    'Directory stylesheets are a collected source set; their runtime loading order is not inferred.',
]


def masked(text):
    """Blank comments and strings while preserving character/line offsets."""
    out = list(text)
    i = 0
    while i < len(text):
        if text.startswith('/*', i):
            end = text.find('*/', i + 2)
            end = len(text) if end < 0 else end + 2
        elif text[i] in '\"\'':
            quote = text[i]
            end = i + 1
            while end < len(text):
                if text[end] == '\\':
                    end += 2
                elif text[end] == quote:
                    end += 1
                    break
                else:
                    end += 1
        else:
            i += 1
            continue
        for j in range(i, min(end, len(text))):
            if text[j] != '\n':
                out[j] = ' '
        i = end
    return ''.join(out)


@dataclass(frozen=True)
class Declaration:
    file: str
    line: int
    selector: str
    context: tuple
    name: str
    value: str


@dataclass(frozen=True)
class Var:
    name: str
    fallback: str | None
    offset: int


def vars_in(value):
    """Return top-level var calls; fallback calls are parsed recursively."""
    clean = masked(value)
    found = []
    pos = 0
    while match := re.search(r'(?<![\w-])var\s*\(', clean[pos:], re.I):
        start = pos + match.start()
        opening = pos + match.end() - 1
        level, comma, end = 1, None, opening + 1
        while end < len(clean) and level:
            char = clean[end]
            if char == '(':
                level += 1
            elif char == ')':
                level -= 1
            elif char == ',' and level == 1 and comma is None:
                comma = end
            end += 1
        if level:
            found.append(Var('', None, start))
            break
        boundary = comma if comma is not None else end - 1
        name = clean[opening + 1:boundary].strip()
        fallback = value[comma + 1:end - 1] if comma is not None else None
        found.append(Var(name, fallback, start))
        pos = end
    return found


def all_vars(value):
    for call in vars_in(value):
        yield call
        if call.fallback is not None:
            yield from all_vars(call.fallback)


def scan_css(text, file, line=1, inline=False):
    clean = masked(text)
    stack = []
    start, depth = 0, 0
    declarations = []
    limits = []
    def emit(stop):
        chunk = clean[start:stop]
        if ':' not in chunk or not stack or stack[-1][0].startswith('@'):
            return
        name, value = chunk.split(':', 1)
        name = name.strip()
        if not re.fullmatch(r'(?:--)?[A-Za-z_][A-Za-z0-9_-]*', name):
            return
        offset = start + len(chunk) - len(chunk.lstrip())
        selector = stack[-1][0]
        selectors = selector.split(',') if '(' not in selector and '[' not in selector else [selector]
        for part in selectors:
            declarations.append(Declaration(file, line + text[:offset].count('\n'),
                                            part.strip(), tuple(x[0] for x in stack[:-1]),
                                            name, text[start + chunk.index(':') + 1:stop].strip()))
    if inline:
        stack.append(('<inline-style>', 0))
    for i, char in enumerate(clean):
        if char == '(' or char == '[':
            depth += 1
        elif char == ')' or char == ']':
            depth = max(0, depth - 1)
        elif depth == 0 and char == '{':
            header = clean[start:i].strip()
            if stack and not stack[-1][0].startswith('@'):
                limits.append({'code': 'nested_css', 'file': file, 'line': line + text[:i].count('\n')})
            stack.append((header, i))
            start = i + 1
        elif depth == 0 and char == ';':
            emit(i)
            start = i + 1
        elif depth == 0 and char == '}':
            emit(i)
            if stack:
                stack.pop()
            start = i + 1
    if inline:
        emit(len(text))
    if depth or (stack and not inline):
        limits.append({'code': 'unbalanced_css', 'file': file, 'line': line})
    return declarations, limits


class StyleHTML(HTMLParser):
    def __init__(self, file):
        super().__init__(convert_charrefs=True)
        self.file, self.declarations, self.limits = file, [], []
        self.in_style = False
        self.style_parts, self.style_line = [], 1
    def handle_starttag(self, tag, attrs):
        if tag == 'style':
            self.in_style = True
            self.style_parts, self.style_line = [], self.getpos()[0]
        for key, value in attrs:
            if key == 'style' and value:
                decl, limits = scan_css(value, self.file, self.getpos()[0], True)
                self.declarations.extend(decl)
                self.limits.extend(limits)
            if tag == 'link' and key == 'rel' and value == 'stylesheet':
                self.limits.append({'code': 'stylesheet_loading_not_verified', 'file': self.file, 'line': self.getpos()[0]})
    def handle_data(self, data):
        if self.in_style:
            self.style_parts.append(data)
    def handle_endtag(self, tag):
        if tag == 'style' and self.in_style:
            decl, limits = scan_css(''.join(self.style_parts), self.file, self.style_line)
            self.declarations.extend(decl)
            self.limits.extend(limits)
            self.in_style = False


def safe_path(path):
    path = Path(path).absolute()
    if path.is_symlink() and not path.is_dir():
        raise ValueError(f'Symlink traversal rejected: {path}')
    if not path.exists():
        raise ValueError(f'Source does not exist: {path}')
    return path.resolve()


def runtime_tokens(text):
    """Recognize fixed-name style.setProperty calls as runtime providers only."""
    clean = masked(text)
    # JS template strings and line comments are opaque; no JS is executed.
    for match in re.finditer(r"`(?:\\.|[^`])*`|//[^\n]*", clean):
        clean = clean[:match.start()] + re.sub(r"[^\n]", " ", match.group()) + clean[match.end():]
    for match in re.finditer(r"\.style\.setProperty\s*\(", clean):
        token = re.match(r"[\"\'](--[A-Za-z_][A-Za-z0-9_-]*)[\"\']\s*,", text[match.end():].lstrip())
        if token:
            yield token.group(1), text[:match.start()].count("\n") + 1


def load_source(path):
    path = safe_path(path)
    files = [path] if path.is_file() else sorted(path.rglob('*'))
    declarations, limits, scanned, runtime = [], [], [], []
    for file in files:
        if file.is_symlink():
            raise ValueError(f'Symlink traversal rejected: {file}')
        if not file.is_file() or file.suffix.lower() not in {'.css', '.html', '.htm', '.js', '.mjs'}:
            continue
        file = safe_path(file)
        label = file.name if path.is_file() else str(file.relative_to(path))
        text = file.read_text(encoding='utf-8')
        if file.suffix.lower() in {'.js', '.mjs'}:
            runtime.extend({'token': token, 'file': label, 'line': line} for token, line in runtime_tokens(text))
            continue
        if file.suffix.lower() == '.css':
            decl, extra = scan_css(text, label)
        else:
            html = StyleHTML(label)
            html.feed(text)
            decl, extra = html.declarations, html.limits
        declarations.extend(decl)
        limits.extend(extra)
        scanned.append(label)
    return declarations, limits, scanned, runtime


def check_source(source, reference=None):
    declarations, limits, files, runtime = load_source(source)
    definitions = [d for d in declarations if d.name.startswith('--')]
    declared = sorted({d.name for d in definitions})
    used = sorted({v.name for d in declarations for v in all_vars(d.value) if NAME.fullmatch(v.name)})
    errors = []
    if not files:
        limits.append({'code': 'no_styles_scanned', 'file': str(Path(source).absolute()), 'line': 1})
    def diagnostic(code, d, **extra):
        return {'code': code, 'file': d.file, 'line': d.line, 'selector': d.selector, **extra}
    runtime_names = {d['token'] for d in runtime}
    def candidates(name, at):
        defs = [d for d in definitions if d.name == name]
        # Exact selector within the same conditional context can override globals.
        local = [d for d in defs if d.selector == at.selector and d.context == at.context]
        base = [d for d in defs if d.selector in {':root', 'html'} and not d.context]
        chosen = local or base
        # Equal selector/context in one file has known source order. Across
        # files, order is unknown. Preserve the last !important declaration.
        groups = {}
        for d in chosen:
            key = (d.file, d.selector, d.context)
            previous = groups.get(key)
            if previous is None or '!important' not in previous.value.lower() or '!important' in d.value.lower():
                groups[key] = d
        return list(groups.values()), bool(defs) or name in runtime_names
    def resolve(call, at, trail):
        if not NAME.fullmatch(call.name):
            return 'invalid_var', [call.name]
        choices, exists = candidates(call.name, at)
        if not choices:
            status, names = ('scope_unresolved', [call.name]) if exists else ('undefined_token', [call.name])
        else:
            results = []
            for d in choices:
                if d in trail:
                    results.append(('alias_cycle', [x.name for x in (*trail, d)]))
                elif d.value.strip().lower() in {'initial', 'inherit', 'unset', 'revert', 'revert-layer'}:
                    results.append(('scope_unresolved', [call.name]))
                else:
                    results.append(resolve_value(d.value, d, (*trail, d)))
            status, names = results[0]
            if len(set(x[0] for x in results)) > 1 or len({d.value for d in choices}) > 1:
                status, names = 'cascade_unresolved', [call.name]
        if status in {'undefined_token', 'alias_cycle'} and call.fallback is not None:
            return resolve_value(call.fallback, at, trail)
        return status, names
    def resolve_value(value, at, trail=()):
        for call in vars_in(value):
            status, names = resolve(call, at, trail)
            if status != 'valid':
                return status, names
        return 'valid', []
    # Cycle graph includes references in fallbacks, as CSS cycles invalidate a
    # custom property's value even when a fallback branch would be inactive.
    def cycle(d, trail):
        for call in all_vars(d.value):
            choices, _ = candidates(call.name, d)
            for nxt in choices:
                if nxt in trail:
                    return [x.name for x in (*trail, nxt)]
                found = cycle(nxt, (*trail, nxt))
                if found:
                    return found
        return None
    for d in definitions:
        found = cycle(d, (d,))
        if found:
            errors.append(diagnostic('alias_cycle', d, tokens=found))
    for d in declarations:
        for call in vars_in(d.value):
            status, names = resolve(call, d, (d,) if d in definitions else ())
            if status == 'valid':
                continue
            entry = diagnostic(status, d, token=call.name, tokens=names)
            (limits if status.endswith('_unresolved') else errors).append(entry)
    baseline = None
    if reference is not None:
        original, _, _, _ = load_source(reference)
        baseline = sorted({v.name for d in original for v in all_vars(d.value) if NAME.fullmatch(v.name)})
        for token in sorted(set(baseline) - set(used)):
            loc = next(d for d in original if token in {v.name for v in all_vars(d.value)})
            errors.append({'code': 'baseline_token_removed', 'file': loc.file, 'line': loc.line,
                           'token': token, 'location': 'reference', 'source': str(Path(reference).absolute())})
    def unique(items):
        return [json.loads(s) for s in sorted({json.dumps(x, sort_keys=True) for x in items})]
    errors, limits = unique(errors), unique(limits)
    return {'ok': not errors, 'status': 'error' if errors else 'limited' if limits else 'pass',
            'source': str(Path(source).absolute()), 'files': files,
            'tokens': {'declared': declared, 'used': used, 'baseline_used': baseline, 'runtime_set': sorted(runtime_names)},
            'errors': errors, 'limits': limits, 'runtime_providers': runtime, 'limitations': LIMITATIONS}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', help='CSS/HTML file or source directory (no symlinks inside source)')
    parser.add_argument('--reference', help='Original source to preserve its consumed token names')
    args = parser.parse_args()
    try:
        result = check_source(args.source, args.reference)
    except (OSError, ValueError, RecursionError) as exc:
        result = {'ok': False, 'status': 'error', 'errors': [{'code': 'source_error', 'file': args.source, 'line': 1, 'message': str(exc)}]}
    print(json.dumps(result, sort_keys=True, separators=(',', ':')))
    return int(not result['ok'])


if __name__ == '__main__':
    raise SystemExit(main())
