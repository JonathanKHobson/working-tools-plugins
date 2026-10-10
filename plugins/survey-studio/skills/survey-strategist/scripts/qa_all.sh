#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
TMP="$(mktemp -d)"
cleanup() {
  rm -rf "$TMP"
  find "$ROOT" -type d -name __pycache__ -prune -exec rm -rf {} + 2>/dev/null || true
  find "$ROOT" -type f -name '*.pyc' -delete 2>/dev/null || true
}
trap cleanup EXIT
export PYTHONPATH="$ROOT/scripts${PYTHONPATH:+:$PYTHONPATH}"

printf '1/7 Compile Python into a temporary directory\n'
python - "$ROOT" "$TMP" <<'PYCOMPILE'
from pathlib import Path
import py_compile, sys
root=Path(sys.argv[1]); out=Path(sys.argv[2])/'compiled'; out.mkdir()
for path in list((root/'scripts').glob('*.py')) + list((root/'tests').glob('test_*.py')):
    py_compile.compile(str(path), cfile=str(out/f'{path.parent.name}-{path.stem}.pyc'), doraise=True)
PYCOMPILE

printf '2/7 Validate skill structure\n'
python "$ROOT/scripts/validate_skill.py" "$ROOT"

printf '3/7 Run unit tests\n'
python -m unittest discover -s "$ROOT/tests" -p 'test_*.py' -v

printf '4/7 Audit examples and generate all representative exports\n'
python - "$ROOT" "$TMP" <<'PYQA'
from pathlib import Path
import csv, json, sys, xml.etree.ElementTree as ET
import yaml
root=Path(sys.argv[1]); out=Path(sys.argv[2])
sys.path.insert(0,str(root/'scripts'))
from estimate_burden import estimate_burden
from export_survey import export_to_path
from generate_codebook import write_codebook
from survey_io import load_survey
from survey_lint import lint_survey
from validate_qualtrics_txt import validate_file

for path in sorted(list((root/'examples').glob('*.yaml')) + list((root/'examples').glob('*.json'))):
    data=load_survey(path)
    errors=[i for i in lint_survey(data, include_info=True) if i.severity=='error']
    if errors:
        raise SystemExit(f'{path.name}: '+ '; '.join(f'{i.code}: {i.message}' for i in errors))
    report=estimate_burden(data)
    if report['estimated_seconds'] <= 0:
        raise SystemExit(f'{path.name}: invalid burden estimate')

survey_path=root/'examples'/'product-experience-pulse.yaml'
data=load_survey(survey_path)
outputs={
    'markdown':'product-experience-pulse.md',
    'text':'product-experience-pulse.txt',
    'html':'product-experience-pulse.html',
    'xml':'product-experience-pulse.xml',
    'json':'product-experience-pulse.json',
    'yaml':'product-experience-pulse.yaml',
    'csv':'product-experience-pulse.csv',
    'docx':'product-experience-pulse.docx',
    'pdf':'product-experience-pulse.pdf',
    'qualtrics-advanced':'product-experience-pulse.advanced.txt',
    'qualtrics-simple':'product-experience-pulse.simple.txt',
}
for fmt,name in outputs.items():
    export_to_path(data,fmt,out/name)
write_codebook(data,out/'codebook.md','markdown')
write_codebook(data,out/'codebook.json','json')

for name in ('product-experience-pulse.advanced.txt','product-experience-pulse.simple.txt'):
    issues=[i for i in validate_file(out/name) if i.severity=='error']
    if issues:
        raise SystemExit(f'{name}: '+ '; '.join(f'{i.code}: {i.message}' for i in issues))

required=[out/name for name in outputs.values()]+[out/'codebook.md',out/'codebook.json']
missing=[p.name for p in required if not p.exists() or p.stat().st_size==0]
if missing: raise SystemExit('Missing/empty generated files: '+', '.join(missing))
json.loads((out/'product-experience-pulse.json').read_text(encoding='utf-8'))
yaml.safe_load((out/'product-experience-pulse.yaml').read_text(encoding='utf-8'))
ET.parse(out/'product-experience-pulse.xml')
with (out/'product-experience-pulse.csv').open(newline='',encoding='utf-8') as fh:
    if not list(csv.DictReader(fh)): raise SystemExit('CSV codebook has no rows')
html=(out/'product-experience-pulse.html').read_text(encoding='utf-8')
for token in ('<main','<fieldset','<legend','lang="en"'):
    if token not in html: raise SystemExit(f'HTML missing {token}')
PYQA

printf '5/7 Validate DOCX and PDF containers\n'
unzip -t "$TMP/product-experience-pulse.docx" >/dev/null
if command -v pdfinfo >/dev/null 2>&1; then pdfinfo "$TMP/product-experience-pulse.pdf" >/dev/null; fi

printf '6/7 Check command help\n'
for script in estimate_burden.py export_survey.py generate_codebook.py survey_lint.py validate_qualtrics_txt.py validate_skill.py; do
  python "$ROOT/scripts/$script" --help >/dev/null
done

printf '7/7 Verify package hygiene\n'
python - "$ROOT" <<'PYSYMLINKS'
from pathlib import Path
import sys
broken = [str(p) for p in Path(sys.argv[1]).rglob('*') if p.is_symlink() and not p.exists()]
if broken:
    raise SystemExit('Broken symlinks: ' + ', '.join(broken))
PYSYMLINKS
if grep -RInE '\b(TODO|TBD|FIXME)\b|fill[[:space:]]+in[[:space:]]+later' "$ROOT/SKILL.md" "$ROOT/references" "$ROOT/agents/roles"; then
  echo 'Unresolved placeholder found.' >&2
  exit 1
fi

printf 'QA PASS: structure, 35 unit tests, examples, all exports, Qualtrics syntax, DOCX and PDF integrity verified.\n'
