#!/usr/bin/env python3
"""Render the single Common Sun guide pilot from an editable page layout.

The logo placements use PNG exports of the original outlined SVG artwork.
Type, rules, cards and page geometry remain editable here.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from PIL import Image
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

SCRIPT_DIR = Path(__file__).resolve().parent
if SCRIPT_DIR.name == 'guide-source':
    BRAND = SCRIPT_DIR.parent
    ROOT = BRAND
    PUBLIC_GUIDES = BRAND
    PUBLIC_MEDIA = SCRIPT_DIR / 'rendered'
else:
    ROOT = SCRIPT_DIR.parent
    BRAND = ROOT / 'brands/community-festival'
    PUBLIC_GUIDES = ROOT / 'public/guides'
    PUBLIC_MEDIA = ROOT / 'public/media'
SRC = BRAND / 'guide-source'
LOGOS = BRAND / 'assets/logos'
MOTIFS = BRAND / 'assets/motifs'
SOURCE_FONTS = BRAND / 'assets/fonts'

W, H = 1200, 1600
PAPER = colors.HexColor('#F6EFD9')
PINE = colors.HexColor('#163C35')
BRASS = colors.HexColor('#BC8C38')
RUST = colors.HexColor('#A4432E')
MUTED = colors.HexColor('#63746D')


def y(top: float) -> float:
    return H-top


def line(c, x1, top1, x2, top2, color=PINE, width=1):
    c.setStrokeColor(color);c.setLineWidth(width);c.line(x1,y(top1),x2,y(top2))


def box(c, x, top, width, height, fill, stroke=None, sw=1):
    c.setFillColor(fill)
    if stroke:
        c.setStrokeColor(stroke);c.setLineWidth(sw)
    c.rect(x,y(top+height),width,height,fill=1,stroke=int(bool(stroke)))


def txt(c, x, top, words, font='Arimo', size=15, fill=PINE):
    c.setFillColor(fill);c.setFont(font,size);c.drawString(x,y(top),words)


def centered(c, x, top, words, font='Arimo', size=15, fill=PINE):
    c.setFillColor(fill);c.setFont(font,size);c.drawCentredString(x,y(top),words)


def fit(c, x, top, words, font, size, width, fill=PINE):
    while size>8 and pdfmetrics.stringWidth(words,font,size)>width:size-=1
    txt(c,x,top,words,font,size,fill)
    return size


def paragraphs(c, x, top, content, width, font='Arimo', size=15, leading=21, fill=PINE):
    c.setFillColor(fill);c.setFont(font,size)
    line_words=[];current=top
    for word in content.split():
        trial=' '.join(line_words+[word])
        if pdfmetrics.stringWidth(trial,font,size)>width and line_words:
            c.drawString(x,y(current),' '.join(line_words));current+=leading;line_words=[word]
        else:line_words.append(word)
    if line_words:c.drawString(x,y(current),' '.join(line_words));current+=leading
    return current


def image(c, path: Path, x, top, width, height):
    if not path.exists():return False
    c.drawImage(ImageReader(str(path)),x,y(top+height),width,height,preserveAspectRatio=True,anchor='c',mask='auto')
    return True


def logo(c, path: Path, x, top, width, height):
    """Place a logo PNG export by its visible alpha bounds, without pixel edits."""
    if not path.exists():return False
    source=Image.open(path)
    if source.mode!='RGBA':source=source.convert('RGBA')
    alpha=source.getchannel('A')
    # The SVG exports use different aspect ratios and transparent margins.
    bounds=alpha.point(lambda p:255 if p>=16 else 0).getbbox() or (0,0,*source.size)
    bw=bounds[2]-bounds[0];bh=bounds[3]-bounds[1]
    scale=min(width/bw,height/bh)
    full_w=source.width*scale;full_h=source.height*scale
    visible_x=x+(width-bw*scale)/2
    visible_top=top+(height-bh*scale)/2
    draw_x=visible_x-bounds[0]*scale
    draw_top=visible_top-bounds[1]*scale
    c.saveState()
    clip=c.beginPath();clip.rect(x,y(top+height),width,height);c.clipPath(clip,stroke=0,fill=0)
    c.drawImage(ImageReader(str(path)),draw_x,y(draw_top+full_h),full_w,full_h,mask='auto')
    c.restoreState()
    return True


def section_header(c, top, title, descriptor=''):
    line(c,70,top,1130,top,PINE,.8)
    txt(c,70,top+30,title,'ArimoBold',15,PINE)
    if descriptor:txt(c,1130-pdfmetrics.stringWidth(descriptor,'Arimo',13),top+30,descriptor,'Arimo',13,MUTED)


def ensure_fonts():
    SRC.mkdir(parents=True,exist_ok=True)
    anton=SOURCE_FONTS/'anton/Anton-Regular.ttf'
    pdfmetrics.registerFont(TTFont('Anton',str(anton)))
    for style in ('Regular','Bold'):
        src=SOURCE_FONTS/f'arimo/Arimo-{style}.woff2'
        out=SRC/f'Arimo-{style}.ttf'
        if not out.exists() or out.stat().st_mtime<src.stat().st_mtime:
            from fontTools.ttLib import TTFont as FontToolsTTFont
            font=FontToolsTTFont(src);font.flavor=None;font.save(out)
        pdfmetrics.registerFont(TTFont('Arimo' if style=='Regular' else 'ArimoBold',str(out)))


def overview(c, primary: Path, stacked: Path, symbol: Path, reverse: Path):
    box(c,0,0,W,H,PAPER)
    # Header and oversized primary lockup. PNG placements come from exact-color
    # production vectors; their SVG originals remain in the brand kit.
    txt(c,70,48,'COMMON SUN  /  VISUAL IDENTITY','ArimoBold',15,PINE)
    txt(c,986,48,'DRAFT 01  ·  2026','Arimo',13,PINE)
    line(c,70,64,1130,64,PINE,1)
    logo(c,primary,68,103,1064,227)
    txt(c,70,377,'A welcoming arts programme with the clarity of a public broadside.','Arimo',22,PINE)

    section_header(c,417,'THE MARK','A small system for large and quiet moments')
    # Primary, stacked and isolated/reverse are distinct uses, with visible room.
    box(c,70,458,330,206,PAPER,PINE,.7)
    logo(c,primary,83,489,302,108)
    txt(c,84,644,'PRIMARY / SYMBOL + NAME','ArimoBold',12,PINE)

    box(c,435,458,330,206,PAPER,PINE,.7)
    logo(c,stacked,495,466,210,167)
    txt(c,449,644,'STACKED / NARROW SPACES','ArimoBold',12,PINE)

    box(c,800,458,330,206,PINE)
    used_reverse=logo(c,reverse,862,484,206,130)
    if not used_reverse: logo(c,symbol,862,484,206,130)
    txt(c,814,644,'ISOLATED / REVERSE USE','ArimoBold',12,PAPER)

    section_header(c,699,'COLOR','Palette')
    swatches=[('FESTIVAL PAPER','#F6EFD9',PAPER),('PINE INK','#163C35',PINE),('BRASS RAYS','#BC8C38',BRASS),('KILN RUST','#A4432E',RUST)]
    for i,(name,hx,color) in enumerate(swatches):
        x=70+i*270
        box(c,x,746,250,78,color,PINE if i==0 else None,.5)
        txt(c,x,848,name,'ArimoBold',13,PINE)
        txt(c,x,869,hx,'Arimo',12,PINE)

    section_header(c,902,'TYPE','A loud invitation, then useful detail')
    txt(c,70,1050,'Aa','Anton',114,PINE)
    txt(c,218,995,'ANTON / DISPLAY','ArimoBold',14,PINE)
    txt(c,218,1022,'ABCDEFGHIJKLMN','Anton',23,PINE)
    txt(c,218,1047,'OPQRSTUVWXYZ  0123456789','Anton',23,PINE)
    txt(c,218,1078,'Tall uppercase headlines and short date labels.','Arimo',14,PINE)
    line(c,596,949,596,1081,BRASS,1)
    txt(c,625,1050,'Aa','ArimoBold',104,PINE)
    txt(c,787,995,'ARIMO / INFORMATION','ArimoBold',14,PINE)
    txt(c,787,1023,'ABCDEFGHIJKLMN','Arimo',17,PINE)
    txt(c,787,1048,'opqrstuvwxyz 0123456789','Arimo',17,PINE)
    txt(c,787,1078,'Session, venue and access information.','Arimo',14,PINE)

    section_header(c,1105,'IN USE','Sample applications')
    # Two different applications, each styled from the identity, not copied
    # from the source site's hero.
    box(c,70,1153,500,330,PAPER,PINE,.7)
    line(c,89,1173,89,1464,BRASS,2)
    logo(c,symbol,377,1164,154,94)
    txt(c,109,1205,'COMMON SUN','Anton',45,PINE)
    txt(c,109,1250,'ARTS WEEKEND','Anton',45,PINE)
    box(c,109,1274,412,3,BRASS)
    txt(c,109,1305,'MAKE · LISTEN · MEET','ArimoBold',17,RUST)
    txt(c,109,1344,'Saturday + Sunday  /  10 AM–5 PM','Anton',21,PINE)
    paragraphs(c,109,1375,'Creative workshops, live music and good company.',409,'Arimo',14,19,PINE)
    txt(c,109,1418,'Town Hall + Market Square','ArimoBold',14,PINE)
    txt(c,109,1440,'Step-free entry at Town Hall','Arimo',13,PINE)
    txt(c,109,1463,'POSTER STUDY','ArimoBold',11,PINE)

    box(c,610,1153,520,330,PINE)
    txt(c,636,1191,'TODAY AT THE FESTIVAL','Anton',27,PAPER)
    line(c,636,1207,1103,1207,BRASS,2)
    for top,time,title,venue in [(1247,'10:00','OPEN STUDIO','Studio'),(1311,'12:30','SOUND & STORIES','Courtyard'),(1375,'15:00','COMMUNITY TABLE','Hall')]:
        txt(c,636,top,time,'Anton',24,PAPER)
        txt(c,748,top,title,'ArimoBold',19,PAPER)
        txt(c,748,top+21,venue,'Arimo',13,PAPER)
        line(c,636,top+32,1103,top+32,colors.HexColor('#56756D'),.7)
    txt(c,636,1455,'PROGRAMME CARD / SAMPLE CONTENT','ArimoBold',11,PAPER)

    line(c,70,1520,1130,1520,PINE,.8)
    txt(c,70,1550,'Come for one session. Stay for the afternoon.','ArimoBold',18,PINE)
    txt(c,70,1573,'Fictional identity  ·  Brand guide  ·  2026','Arimo',12,MUTED)
    c.showPage()


def detail(c, primary: Path, primary_reverse: Path, wordmark: Path, symbol: Path, fan: Path):
    box(c,0,0,W,H,PAPER)
    txt(c,70,55,'COMMON SUN','Anton',42,PINE)
    txt(c,869,50,'SYSTEM IN USE','ArimoBold',14,PINE)
    line(c,70,72,1130,72,PINE,1)

    section_header(c,112,'LOGO USE','Open horizon · generous clear space')
    box(c,70,158,630,304,PAPER,PINE,.7)
    c.setStrokeColor(BRASS);c.setLineWidth(1.2);c.setDash(7,5)
    c.rect(110,y(386),550,182,fill=0,stroke=1);c.setDash()
    logo(c,primary,143,226,484,125)
    line(c,110,371,143,371,BRASS,1.5)
    txt(c,113,397,'x','ArimoBold',17,RUST)
    txt(c,90,444,'CLEAR SPACE / AT LEAST ¼ OF THE CAPITAL HEIGHT','ArimoBold',12,PINE)

    box(c,735,158,395,304,PAPER,PINE,.7)
    txt(c,753,187,'MINIMUM WIDTHS','ArimoBold',15,PINE)
    line(c,753,200,1112,200,BRASS,1)
    logo(c,symbol,754,220,24,16)
    txt(c,826,239,'24 px symbol','Arimo',15,PINE)
    line(c,753,263,1112,263,PINE,.5)
    logo(c,wordmark,754,282,120,33)
    txt(c,951,308,'120 px wordmark','Arimo',14,PINE)
    line(c,753,333,1112,333,PINE,.5)
    logo(c,primary,754,354,160,40)
    txt(c,951,385,'160 px lockup','Arimo',14,PINE)
    txt(c,753,437,'Check legibility in the final output.','Arimo',11,MUTED)

    box(c,70,491,1060,153,PINE)
    logo(c,primary_reverse,238,511,724,92)
    txt(c,88,627,'REVERSE LOCKUP / PINE FIELD','ArimoBold',12,PAPER)

    section_header(c,683,'COLOR PAIRINGS','Read with pine and paper; let accents cue the route')
    box(c,70,735,330,180,PAPER,PINE,.7)
    txt(c,90,782,'THE PROGRAMME','Anton',27,PINE)
    txt(c,90,816,'Pine ink on festival paper','Arimo',15,PINE)
    txt(c,90,888,'TEXT / #163C35  ON  #F6EFD9','ArimoBold',11,PINE)
    box(c,435,735,330,180,PINE)
    txt(c,455,782,'THE PROGRAMME','Anton',27,PAPER)
    txt(c,455,816,'Paper on pine field','Arimo',15,PAPER)
    txt(c,455,888,'TEXT / #F6EFD9  ON  #163C35','ArimoBold',11,PAPER)
    box(c,800,735,330,180,PAPER,PINE,.7)
    txt(c,820,782,'MAKE · LISTEN','Anton',27,RUST)
    txt(c,820,816,'Short accent on paper','Arimo',15,PINE)
    line(c,820,847,1104,847,BRASS,3)
    txt(c,820,888,'BRASS / ORNAMENT ONLY','ArimoBold',11,PINE)

    section_header(c,957,'LAYOUT RHYTHM','Three repeatable moves from the original programme')
    # A: stepped edge and fan, B: date band, C: legible programme fields.
    box(c,70,1010,330,340,PAPER,PINE,.7)
    c.setStrokeColor(BRASS);c.setLineWidth(2)
    path=c.beginPath();path.moveTo(99,y(1034));path.lineTo(99,y(1155));path.lineTo(115,y(1155));path.lineTo(115,y(1207));path.lineTo(99,y(1207));path.lineTo(99,y(1322));c.drawPath(path,stroke=1)
    logo(c,fan,165,1039,158,101)
    txt(c,135,1190,'OPEN THE PAGE','Anton',26,PINE)
    txt(c,135,1228,'WITH ONE CLEAR','Anton',26,PINE)
    txt(c,135,1266,'INVITATION','Anton',26,PINE)
    txt(c,85,1333,'STEPPED EDGE + 17-RAY FAN','ArimoBold',12,PINE)

    box(c,435,1010,330,340,PAPER,PINE,.7)
    txt(c,455,1070,'14—15','Anton',56,PINE)
    txt(c,455,1114,'NOVEMBER','Anton',31,PINE)
    line(c,455,1135,740,1135,BRASS,3)
    txt(c,455,1190,'TOWN HALL','ArimoBold',22,PINE)
    txt(c,455,1221,'MARKET SQUARE','Arimo',20,PINE)
    txt(c,455,1290,'Time and place are','Arimo',15,PINE)
    txt(c,455,1313,'read before ornament.','Arimo',15,PINE)
    txt(c,450,1333,'DATE BAND','ArimoBold',12,PINE)

    box(c,800,1010,330,340,PINE)
    txt(c,821,1065,'TODAY','Anton',35,PAPER)
    line(c,821,1081,1108,1081,BRASS,2)
    for top,tm,title,venue in [(1120,'10:00','OPEN STUDIO','Studio'),(1185,'12:30','SOUND & STORIES','Courtyard'),(1250,'15:00','COMMUNITY TABLE','Hall')]:
        txt(c,821,top,tm,'Anton',22,PAPER)
        txt(c,907,top,title,'ArimoBold',15,PAPER)
        txt(c,907,top+20,venue,'Arimo',12,PAPER)
        line(c,821,top+29,1108,top+29,colors.HexColor('#56756D'),.6)
    txt(c,815,1333,'TIME / TITLE / VENUE','ArimoBold',12,PAPER)

    line(c,70,1401,1130,1401,PINE,.8)
    txt(c,70,1440,'ANTON','Anton',31,PINE)
    txt(c,224,1436,'for invitation and wayfinding','Arimo',17,PINE)
    txt(c,70,1491,'ARIMO','ArimoBold',28,PINE)
    txt(c,224,1487,'for session, venue and access detail','Arimo',17,PINE)
    txt(c,70,1555,'Print every session. On mobile, stack fields before reducing type.','Arimo',15,PINE)
    c.showPage()


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',default=str(PUBLIC_GUIDES/'community-festival.pdf'))
    args=parser.parse_args()
    ensure_fonts()
    primary=LOGOS/'logo-primary.png'
    stacked=LOGOS/'logo-stacked.png'
    symbol=LOGOS/'symbol-primary.png'
    reverse=LOGOS/'symbol-reverse.png'
    fan=MOTIFS/'festival-fan.png'
    if not all(p.exists() for p in (primary,stacked,symbol,reverse,fan)):
        raise SystemExit('Common Sun logo and supporting motif PNG exports are required')
    PUBLIC_GUIDES.mkdir(parents=True,exist_ok=True);PUBLIC_MEDIA.mkdir(parents=True,exist_ok=True)
    path=Path(args.output)
    c=canvas.Canvas(str(path),pagesize=(W,H),pageCompression=1)
    c.setTitle('Common Sun Brand Guide — Pilot')
    overview(c,primary,stacked,symbol,reverse)
    detail(c,primary,LOGOS/'logo-reverse.png',LOGOS/'wordmark.png',symbol,fan)
    c.save()
    subprocess.run(['pdftoppm','-f','1','-l','1','-singlefile','-scale-to','1600','-png',str(path),str(PUBLIC_MEDIA/'community-festival-guide')],check=True)
    board_png=PUBLIC_MEDIA/'community-festival-guide.png'
    im=Image.open(board_png).convert('RGB')
    im.save(PUBLIC_MEDIA/'community-festival-guide.webp',quality=90,method=6)
    board_png.unlink()
    subprocess.run(['pdftoppm','-f','2','-l','2','-singlefile','-scale-to','1600','-png',str(path),str(PUBLIC_MEDIA/'community-festival-rules')],check=True)
    rules_png=PUBLIC_MEDIA/'community-festival-rules.png'
    im2=Image.open(rules_png).convert('RGB')
    im2.save(PUBLIC_MEDIA/'community-festival-rules.webp',quality=90,method=6)
    rules_png.unlink()
    print(path)
    print(PUBLIC_MEDIA/'community-festival-guide.webp')
    print(PUBLIC_MEDIA/'community-festival-rules.webp')
    print('symbol-sha256',hashlib.sha256(symbol.read_bytes()).hexdigest())


if __name__=='__main__':main()
