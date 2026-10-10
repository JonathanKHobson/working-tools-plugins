#!/usr/bin/env python3
"""Render the reusable P49 reading guide from its maintained public sources."""
import argparse
import hashlib
import json
import re
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab import rl_config
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    KeepTogether, HRFlowable,
)

ROOT = Path(__file__).resolve().parents[1]
LIB = ROOT / 'library/voice-library'
INK = colors.HexColor('#173a36')
TEAL = colors.HexColor('#216f65')
MUTED = colors.HexColor('#4b6560')
PALE = colors.HexColor('#e8f3ef')
RULE = colors.HexColor('#c9dcd5')
WIDTH, HEIGHT = 612, 792
MARGIN = 54


def inline(text):
    text = escape(text)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', lambda m: (
        '<link href="' + m[2].replace('"', '&quot;') + '" color="#216f65">' + m[1] + '</link>'
        if m[2].startswith(('https://', 'http://')) else m[1]), text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<i>\1</i>', text)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    return text


def render(output, font_root):
    rl_config.invariant = 1
    for name, rel in [('Body', 'dmsans/DMSans-400.ttf'),
                      ('Bold', 'dmsans/DMSans-700.ttf'),
                      ('Display', 'fredoka/Fredoka-700.ttf')]:
        pdfmetrics.registerFont(TTFont(name, str(font_root / rel)))
    pdfmetrics.registerFontFamily('Body', normal='Body', bold='Bold', italic='Body', boldItalic='Bold')
    st = {
        'body': ParagraphStyle('body', fontName='Body', fontSize=10.7, leading=15.8,
                               textColor=INK, spaceAfter=8, allowWidows=0, allowOrphans=0),
        'small': ParagraphStyle('small', fontName='Body', fontSize=9, leading=12.6,
                                textColor=MUTED, spaceAfter=7),
        'h1': ParagraphStyle('h1', fontName='Display', fontSize=30, leading=34,
                             textColor=INK, spaceAfter=18, keepWithNext=True),
        'h2': ParagraphStyle('h2', fontName='Bold', fontSize=15, leading=20,
                             textColor=TEAL, spaceBefore=14, spaceAfter=8, keepWithNext=True),
        'h3': ParagraphStyle('h3', fontName='Bold', fontSize=11.4, leading=16,
                             textColor=INK, spaceBefore=9, spaceAfter=5, keepWithNext=True),
        'cell': ParagraphStyle('cell', fontName='Body', fontSize=9, leading=12.5,
                               textColor=INK, spaceAfter=0),
    }
    story = []
    def p(text, kind='body'):
        return Paragraph(inline(text), st[kind])

    def markdown(raw, skip_title=True):
        raw = re.sub(r'^---\n.*?\n---\n', '', raw, flags=re.S)
        raw = re.sub(r'<!--.*?-->', '', raw, flags=re.S)
        lines = raw.splitlines()
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if not line or line == '---':
                i += 1
                continue
            if line.startswith('|') and i + 1 < len(lines) and re.match(r'^\|?[\s:|\-]+$', lines[i + 1]):
                rows = []
                while i < len(lines) and lines[i].strip().startswith('|'):
                    row = [x.strip() for x in lines[i].strip().strip('|').split('|')]
                    if not all(re.fullmatch(r'[:\- ]+', cell) for cell in row):
                        rows.append(row)
                    i += 1
                count = max(len(row) for row in rows)
                widths = [504 / count] * count
                if count >= 3:
                    widths = [76] + [428 / (count - 1)] * (count - 1)
                data = [[p(('**' + x + '**') if n == 0 else x, 'cell') for x in row]
                        for n, row in enumerate(rows)]
                t = Table(data, colWidths=widths, repeatRows=1, hAlign='LEFT')
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), PALE),
                    ('LINEBELOW', (0, 0), (-1, -1), .35, RULE),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 7),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 7),
                    ('TOPPADDING', (0, 0), (-1, -1), 7),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
                ]))
                story.extend([t, Spacer(1, 10)])
                continue
            heading = re.match(r'^(#{1,6})\s+(.+)', line)
            if heading:
                depth, title = len(heading[1]), heading[2]
                if not (depth == 1 and skip_title):
                    story.append(p(title, 'h2' if depth <= 2 else 'h3'))
                i += 1
                continue
            bullet = re.match(r'^(?:[-*]|\d+[.)])\s+(.*)', line)
            if bullet:
                story.append(Paragraph(inline(bullet[1]), ParagraphStyle(
                    'list', parent=st['body'], leftIndent=13, firstLineIndent=0,
                    bulletIndent=0), bulletText='•'))
                i += 1
                continue
            para = [line.removeprefix('> ')]
            i += 1
            while i < len(lines) and lines[i].strip() and not re.match(r'^(#{1,6}\s|[-*]\s|\d+[.)]\s|\|)', lines[i].strip()):
                para.append(lines[i].strip().removeprefix('> '))
                i += 1
            story.append(p(' '.join(para)))

    record = next(r for r in json.loads((LIB / 'records/catalog.json').read_text())['records'] if r['id'] == 'P49')
    comp = LIB / 'source-edition/companions/P49'
    sources = ['AUTHORITY.md', 'FINGERPRINT.md', 'REQUIREMENTS.md', 'COMPOSITION.md']
    source_hashes = {name: hashlib.sha256((comp / name).read_bytes()).hexdigest() for name in sources}
    story.extend([Spacer(1, 16), p('Fresh Curiosity', 'h1'),
                  p('A reusable writing template', 'h2'),
                  p('Curious, imaginative and encouraging. Give the reader something concrete to examine, then invite a useful next step.'),
                  Spacer(1, 16)])
    axes = [
        ['Voice', 'Curious inventor; optimistic, collaborative and inviting'],
        ['Tone', 'Warm and inquisitive, adapted to the stakes of the task'],
        ['Style', 'Wonder → Meaning → Reflection → Action for suitable long-form work'],
        ['Format', 'The requested artifact determines its container and functional requirements'],
    ]
    table = Table([[p(a, 'h3'), p(b)] for a, b in axes], colWidths=[90, 414])
    table.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'),
                              ('LINEBELOW', (0, 0), (-1, -1), .5, RULE),
                              ('LEFTPADDING', (0, 0), (-1, -1), 0),
                              ('TOPPADDING', (0, 0), (-1, -1), 6),
                              ('BOTTOMPADDING', (0, 0), (-1, -1), 7)]))
    story.extend([table, Spacer(1, 22), p('Choose who is speaking', 'h2'),
                  p('Apply the template to the author, product or team named in the brief. Use first person for a supplied personal perspective; lead product copy with verified behavior; use “we” only for a real team or an explicitly shared exercise.'),
                  p('The style does not supply a biography, credentials, a brand identity or permission to claim someone else’s experience.'),
                  Spacer(1, 12), p('In this guide', 'h2'),
                  p('Complete authority · Fingerprint and measurements · Requirements · Composing with another register · Three demonstrations'),
                  p('P49 · Reusable edition ' + record['version'] + ' · 9 October 2026', 'small'),
                  p('The portable skill adds the complete Markdown references, sample briefs, Humanizer Light and optional offline draft checks.', 'small'),
                  p('https://activity-atlas.jkylehobson.chatgpt.site/writing-library/#voice=P49', 'small')])
    for title, name in [('Complete authority', 'AUTHORITY.md'),
                        ('Fingerprint and measurements', 'FINGERPRINT.md'),
                        ('Requirements', 'REQUIREMENTS.md'),
                        ('Composing with another register', 'COMPOSITION.md')]:
        story.extend([PageBreak(), p(title, 'h1')])
        markdown((comp / name).read_text())
    story.extend([PageBreak(), p('Demonstrations', 'h1')])
    for index, ex in enumerate(record['examples']):
        text = (LIB / ex['path']).read_text()
        specimen = re.search(r'<!-- specimen:start -->(.*?)<!-- specimen:end -->', text, re.S)[1].strip()
        story.append(p(record.get('example_labels', ['Opening invitation', 'Reflective passage', 'Action prompt'])[index], 'h2'))
        markdown(specimen, skip_title=False)
        story.extend([Spacer(1, 16), HRFlowable(width='100%', thickness=.5, color=RULE),
                      Spacer(1, 8), p('AI-authored demonstration · Fictional scenario. The portable skill includes its factual brief and supporting references.', 'small')])
    def page(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(RULE)
        canvas.setLineWidth(.5)
        canvas.line(MARGIN, HEIGHT - 37, WIDTH - MARGIN, HEIGHT - 37)
        canvas.setFillColor(MUTED)
        canvas.setFont('Body', 8)
        canvas.drawString(MARGIN, HEIGHT - 28, 'WRITING LIBRARY  /  FRESH CURIOSITY')
        canvas.line(MARGIN, 38, WIDTH - MARGIN, 38)
        canvas.drawString(MARGIN, 25, 'Reusable writing guide · P49 · ' + record['version'])
        canvas.drawRightString(WIDTH - MARGIN, 25, str(doc.page))
        canvas.restoreState()
    output.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(str(output), pagesize=(WIDTH, HEIGHT), rightMargin=MARGIN,
                            leftMargin=MARGIN, topMargin=58, bottomMargin=54,
                            title='Fresh Curiosity · Reusable Writing Guide', author='Writing Library')
    doc.build(story, onFirstPage=page, onLaterPages=page)
    return {'pdf': str(output), 'bytes': output.stat().st_size,
            'sha256': hashlib.sha256(output.read_bytes()).hexdigest(),
            'sourceVersion': record['version'], 'sourceHashes': source_hashes}


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', required=True, type=Path)
    ap.add_argument('--font-root', required=True, type=Path)
    ap.add_argument('--evidence', required=True, type=Path)
    args = ap.parse_args()
    receipt = render(args.output, args.font_root)
    args.evidence.parent.mkdir(parents=True, exist_ok=True)
    args.evidence.write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt))
