#!/usr/bin/env python3
"""Validate an original role palette, export observed Codex JSON format, or preview it."""
import argparse
import html
import json
from pathlib import Path
import re

FIELDS = {'schema_version', 'surface', 'ink', 'accent', 'contrast', 'ui_font', 'code_font', 'opaque_windows', 'semantic_colors', 'variant'}
SEMANTIC = {'diffAdded', 'diffRemoved', 'skill'}
EXAMPLE = {'schema_version': 1, 'surface': '#20242A', 'ink': '#F1F3F5', 'accent': '#76B5FF', 'contrast': 70, 'ui_font': 'Arial', 'code_font': 'monospace', 'opaque_windows': True, 'semantic_colors': {'diffAdded': '#83D5A4', 'diffRemoved': '#F0A0A6', 'skill': '#C1AAFA'}, 'variant': 'dark'}


def hex_color(value, role):
    if not isinstance(value, str) or not re.fullmatch(r'#[0-9a-fA-F]{6}', value):
        raise ValueError(role + ' must use a six-digit hexadecimal color.')
    return value.upper()


def validate(spec):
    if not isinstance(spec, dict) or set(spec) != FIELDS:
        raise ValueError('Role palette must contain exactly the documented schema_version, surface, ink, accent, contrast, ui_font, code_font, opaque_windows, semantic_colors and variant fields.')
    if type(spec['schema_version']) is not int or spec['schema_version'] != 1:
        raise ValueError('Only original role-palette schema version 1 is supported.')
    if spec['variant'] != 'dark':
        raise ValueError('Only dark is supported until another native variant is verified.')
    if type(spec['contrast']) is not int or not 0 <= spec['contrast'] <= 100:
        raise ValueError('Native contrast parameter must be an integer from 0 to 100; it is not a WCAG contrast ratio.')
    if type(spec['opaque_windows']) is not bool:
        raise ValueError('opaque_windows must be boolean.')
    for role in ('surface', 'ink', 'accent'):
        spec[role] = hex_color(spec[role], role)
    for role in ('ui_font', 'code_font'):
        value = spec[role]
        if not isinstance(value, str) or not value.strip() or not re.fullmatch(r'[\w .+\-]{1,120}', value):
            raise ValueError(role + ' must be a single plain font name without controls or CSS/HTML syntax.')
        spec[role] = value.strip()
    semantic = spec['semantic_colors']
    if not isinstance(semantic, dict) or set(semantic) != SEMANTIC:
        raise ValueError('semantic_colors needs exactly diffAdded, diffRemoved and skill.')
    spec['semantic_colors'] = {key: hex_color(semantic[key], key) for key in sorted(SEMANTIC)}
    return spec


def export_line(spec):
    # Independently authored field mapping for the ordinary JSON interchange observed locally.
    payload = {'codeThemeId': 'codex', 'theme': {'surface': spec['surface'], 'ink': spec['ink'], 'accent': spec['accent'], 'contrast': spec['contrast'], 'fonts': {'ui': spec['ui_font'], 'code': spec['code_font']}, 'opaqueWindows': spec['opaque_windows'], 'semanticColors': spec['semantic_colors']}, 'variant': spec['variant']}
    return 'codex-theme-v1:' + json.dumps(payload, ensure_ascii=False, separators=(',', ':'), sort_keys=True)


def luminance(color):
    values = [int(color[index:index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [value / 12.92 if value <= .04045 else ((value + .055) / 1.055) ** 2.4 for value in values]
    return sum(weight * value for weight, value in zip((.2126, .7152, .0722), linear))


def ratio(a, b):
    x, y = sorted((luminance(a), luminance(b)))
    return (y + .05) / (x + .05)


def preview(spec):
    ui = html.escape('font-family: "' + spec['ui_font'] + '", sans-serif;', quote=True)
    code = html.escape('font-family: "' + spec['code_font'] + '", monospace;', quote=True)
    colors = spec['semantic_colors']
    style = f"--surface:{spec['surface']};--ink:{spec['ink']};--accent:{spec['accent']};--added:{colors['diffAdded']};--removed:{colors['diffRemoved']};--skill:{colors['skill']};"
    color_rows = ''.join('<tr><th scope="row">' + html.escape(role) + '</th><td><span class="swatch" style="background:' + color + '"></span>' + color + '</td></tr>' for role, color in [('Surface', spec['surface']), ('Text', spec['ink']), ('Accent', spec['accent']), *colors.items()])
    return '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Original application palette preview</title>
<style>
*{box-sizing:border-box}body{margin:0;background:var(--surface);color:var(--ink);font-size:16px;line-height:1.55}main{max-width:1100px;margin:auto;padding:32px 24px}h1,h2,p{margin:0 0 16px}h1{font-size:clamp(1.8rem,4vw,2.5rem);line-height:1.2}h2{font-size:1.25rem}.intro{max-width:70ch}.grid{display:grid;grid-template-columns:minmax(0,2fr) minmax(240px,1fr);gap:28px;margin-top:28px}.panel{border:1px solid currentColor;border-radius:12px;padding:24px;min-width:0}.meta{font-size:.95rem}button,a{color:var(--accent)}button{font:inherit;background:none;border:1px solid var(--accent);padding:10px 16px;border-radius:6px;cursor:pointer}button[aria-pressed="true"]{background:var(--accent);color:var(--surface)}a{text-decoration-thickness:2px;text-underline-offset:3px}button:focus-visible,a:focus-visible,input:focus-visible{outline:3px solid var(--accent);outline-offset:4px}label{display:block;margin:20px 0 8px}input{background:var(--surface);color:var(--ink);border:1px solid currentColor;font:inherit;padding:10px;width:100%;border-radius:4px}pre{white-space:pre-wrap;overflow-wrap:anywhere;border-left:3px solid var(--accent);padding:16px 0 16px 20px;margin:20px 0}.added{color:var(--added)}.removed{color:var(--removed)}.skill{color:var(--skill)}table{width:100%;border-collapse:collapse;text-align:left}th,td{padding:8px 0;vertical-align:middle}.swatch{display:inline-block;width:18px;height:18px;border:1px solid currentColor;vertical-align:middle;margin-right:8px}.actions{display:flex;gap:12px;flex-wrap:wrap}#selection{margin-top:16px;min-height:1.6em}@media(max-width:720px){main{padding:24px 16px}.grid{grid-template-columns:1fr}.panel{padding:20px}}
</style></head><body style="''' + style + ui + '''"><main><h1>Original application palette</h1><p class="intro">Review your text, action and code color roles. This is a local role preview, not a screenshot of the receiving application's rendering. Font names use available local fallbacks.</p><div class="grid"><section class="panel" aria-labelledby="sample"><h2 id="sample">A focused work sample</h2><p>A clear heading and readable paragraph should remain comfortable at your normal viewing size. <a href="#palette">Inspect the palette</a> before choosing it.</p><div class="actions"><button type="button" id="primary" aria-pressed="false">Select this palette</button><button type="button" id="reset">Reset selection</button></div><p id="selection" role="status">No selection made in this preview.</p><label for="sample-field">Example input</label><input id="sample-field" value="Review the saved draft" autocomplete="off"><pre style="''' + code + '''"><span class="removed">- Previous wording</span>
<span class="added">+ Clear next action</span>
<span class="skill">Method: inspect the source</span></pre><p class="meta">Text on surface contrast: ''' + f"{ratio(spec['surface'],spec['ink']):.2f}:1" + '''. The native contrast parameter is separate from this measured color pair.</p></section><section class="panel" aria-labelledby="palette"><h2 id="palette">Color roles</h2><table><thead><tr><th scope="col">Role</th><th scope="col">Color</th></tr></thead><tbody>''' + color_rows + '''</tbody></table><p class="meta">Preview controls affect this page only. Native import and actual application appearance need separate verification.</p></section></div></main><script>
const primary=document.getElementById('primary'), status=document.getElementById('selection');primary.addEventListener('click',()=>{primary.setAttribute('aria-pressed','true');primary.textContent='Palette selected here';status.textContent='Selected in this preview. No application setting changed.'});document.getElementById('reset').addEventListener('click',()=>{primary.setAttribute('aria-pressed','false');primary.textContent='Select this palette';status.textContent='Selection reset in this preview.'});
</script></body></html>'''


def main():
    command = argparse.ArgumentParser(description=__doc__)
    command.add_argument('operation', choices=('example', 'validate', 'export', 'preview'))
    command.add_argument('--spec', type=Path)
    command.add_argument('--output', type=Path)
    command.add_argument('--replace', action='store_true')
    args = command.parse_args()
    if args.operation == 'example':
        result = json.dumps(EXAMPLE, indent=2) + '\n'
    else:
        if args.spec is None:
            raise ValueError('--spec is required for this operation.')
        if args.spec.stat().st_size > 100_000:
            raise ValueError('Role palette input exceeds 100 KB.')
        spec = validate(json.loads(args.spec.read_text(encoding='utf-8')))
        if args.operation == 'validate':
            result = json.dumps({'status': 'valid', 'supported_variant': 'dark', 'text_surface_ratio': round(ratio(spec['surface'], spec['ink']), 3), 'native_import_verified': False}) + '\n'
        elif args.operation == 'export':
            result = export_line(spec) + '\n'
        else:
            result = preview(spec) + '\n'
    if args.output is None:
        print(result, end='')
    else:
        if args.output.is_symlink():
            raise ValueError('Output may not be a symlink.')
        with args.output.open('w' if args.replace else 'x', encoding='utf-8') as output:
            output.write(result)
        print(json.dumps({'status': 'saved', 'operation': args.operation, 'output': str(args.output.resolve()), 'native_import_verified': False}))


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({'status': 'error', 'detail': str(exc)}))
        raise SystemExit(1)
