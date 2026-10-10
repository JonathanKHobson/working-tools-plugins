#!/usr/bin/env python3
"""Render source-grounded two-page brand guides from profiles, logo and font plans.

The driver writes per-brand portable data, fonts and a copy of this renderer.
Only brands with complete, real logo and font assets can render.
"""
from __future__ import annotations
import argparse, json, math, re, shutil, subprocess, sys
from pathlib import Path
from PIL import Image
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

HERE=Path(__file__).resolve().parent
PORTABLE=HERE.name=='guide-source'
ROOT=HERE.parent if not PORTABLE else HERE.parent
W,H=1200,1600
PILOTS=['creative-practice-zine','cost-scenario-planner','annual-community-review','concept-comparison-readout','creative-workshop-offering','evaluation-log-notebook','creative-business-model','photocopied-assembly-public-graphics']
MOVE_CAPTIONS={
 'creative-practice-zine':[('MASTHEAD','Build the WORK masthead from blue rectangular letter segments.'),('READING PAGE','Give a large serif proposition room; keep chapter indexing compact.'),('CHAPTER THREAD','Use red rules to connect evidence and commentary.')],
 'cost-scenario-planner':[('WORKBOOK','Keep assumptions left and selected-case calculations right.'),('INPUT CELL','Blue text on pale yellow means editable input.'),('RESULT ROW','Use stronger umber rules as a subtotal becomes a result.')],
 'annual-community-review':[('MASTHEAD','Use a full Georgia masthead with two unequal rules.'),('STORY PAGE','Keep narrow narrative columns beside the workbench image.'),('SECTION ROUTE','Large numbers guide reading; burgundy marks editorial emphasis.')],
 'concept-comparison-readout':[('TITLE','Set Futura titles with plain supporting text on warm paper.'),('COMPARISON','Give alternatives equal fields and the same question order.'),('FINDING','Use red for one focused observation or decision marker.')],
 'creative-workshop-offering':[('INVITATION','Lead with the workshop serif, then practical sans-serif detail.'),('ACTION','Reserve rust for the primary action on a cream field.'),('STAGES','Number each stage and pair it with a short title.')],
 'evaluation-log-notebook':[('SIDE RAIL','Keep the filter rail stable against the dark reading ground.'),('RECORD ID','Set record IDs and states in mono to ease scanning.'),('EVIDENCE','Show evidence and uncertainty as separate fields.')],
 'creative-business-model':[('ORBIT','Let a reel-like orbit connect the model; avoid a funnel.'),('QUESTION','Keep What must be true at the center of the page.'),('MODEL LINK','Tie offer, time, cost and delivery back to the question.')],
 'photocopied-assembly-public-graphics':[('MASTHEAD','Set OPEN PRESS in bold lettering against a vertical spine.'),('TITLE STRIP','Use one contrasting strip to establish the page title.'),('ASSEMBLY','On the reverse, number the paper-like making steps.')],
}
PAIR_LABELS={'creative-practice-zine':'THE WORK','cost-scenario-planner':'THE CASE','annual-community-review':'THE YEAR','concept-comparison-readout':'TWO IDEAS','creative-workshop-offering':'MAKE TOGETHER','evaluation-log-notebook':'RECORD / 004','creative-business-model':'THE MODEL','photocopied-assembly-public-graphics':'MAKE ONE THING'}

def move_label(observation,index):
 s=observation.lower()
 for words,label in (
  (('date','venue','access','booking'),'ATTENDANCE'),
  (('source','citation','provenance','evidence'),'EVIDENCE'),
  (('color','colour','cream','accent','palette','teal'),'COLOR'),
  (('masthead','typograph','display face','lettering','headline'),'TYPE'),
  (('column','byline','issue','caption'),'EDITORIAL'),
  (('cell','denominator','count','percentage','calculated'),'DATA'),
  (('route','navigation','rail','link'),'NAVIGATION'),
  (('sequence','stage','step','numbered','chronology'),'SEQUENCE'),
  (('frame','margin','grid','layout','outline'),'LAYOUT'),
 ):
  if any(word in s for word in words):return label
 return f'RULE 0{index+1}'


def C(h): return colors.HexColor(h)
def yy(t): return H-t
def rect(c,x,t,w,h,fill,stroke=None,sw=1):
 c.setFillColor(fill)
 if stroke: c.setStrokeColor(stroke);c.setLineWidth(sw)
 c.rect(x,yy(t+h),w,h,fill=1,stroke=int(bool(stroke)))
def rule(c,x1,t1,x2,t2,col,sw=1):
 c.setStrokeColor(col);c.setLineWidth(sw);c.line(x1,yy(t1),x2,yy(t2))
def text(c,x,t,s,font,size,col):
 c.setFillColor(col);c.setFont(font,size);c.drawString(x,yy(t),str(s))
def fit(c,x,t,s,font,size,col,maxw,minsize=10):
 while size>minsize and pdfmetrics.stringWidth(str(s),font,size)>maxw:size-=1
 text(c,x,t,s,font,size,col);return size
def wrap(c,x,t,s,font,size,col,maxw,lead=None,maxlines=4):
 words=str(s).split()
 while True:
  lines=[];row=''
  for word in words:
   test=(row+' '+word).strip()
   if row and pdfmetrics.stringWidth(test,font,size)>maxw:lines.append(row);row=word
   else:row=test
  if row:lines.append(row)
  if len(lines)<=maxlines or size<=9:break
  size-=.5
 if len(lines)>maxlines:raise ValueError(f'Text requires {len(lines)} lines at minimum size: {str(s)[:70]}')
 lead=lead or size*1.35
 for i,line in enumerate(lines):text(c,x,t+i*lead,line,font,size,col)
 return len(lines)*lead

def logo(c,path,x,t,w,h):
 p=Path(path)
 if not p.exists():raise FileNotFoundError(p)
 im=Image.open(p).convert('RGBA');box=im.getchannel('A').getbbox() or (0,0,*im.size)
 bw,bh=box[2]-box[0],box[3]-box[1];scale=min(w/bw,h/bh)
 vx=x+(w-bw*scale)/2;vt=t+(h-bh*scale)/2
 dx=vx-box[0]*scale;dt=vt-box[1]*scale
 c.saveState();clip=c.beginPath();clip.rect(x,yy(t+h),w,h);c.clipPath(clip,stroke=0,fill=0)
 c.drawImage(ImageReader(str(p)),dx,yy(dt+im.height*scale),im.width*scale,im.height*scale,mask='auto');c.restoreState()

def lum(h):
 r,g,b=[int(h[i:i+2],16)/255 for i in (1,3,5)]
 def v(x):return x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4
 return .2126*v(r)+.7152*v(g)+.0722*v(b)
def contrast(a,b):
 x,y=sorted([lum(a),lum(b)],reverse=True);return (x+.05)/(y+.05)
def kind_asset(d,kind):
 for a in d['logos']:
  if a['kind']==kind:return Path(d['brandDir'])/a['png']
 raise ValueError(f"{d['id']}: missing {kind} logo")
def register_fonts(d):
 fonts=[]
 for i,f in enumerate(d['fonts']):
  role=f['role'];r=Path(d['brandDir'])/f['regular'];b=Path(d['brandDir'])/f['bold']
  for suff,path in [('',r),('B',b)]:
   name=f'{d["id"].replace("-","_")}_{i}{suff}';pdfmetrics.registerFont(TTFont(name,str(path)))
  prefix=f'{d["id"].replace("-","_")}_{i}'
  fonts.append({'role':role,'source':f['sourceFamily'],'render':f['renderFamily'],'exact':f['exactOrSubstitute'],'regular':prefix,'bold':prefix+'B'})
 return fonts

def roles(fonts):
 display=next((f for f in fonts if f['role'] in ('display','heading','title')),fonts[0])
 body=next((f for f in fonts if f['role'] in ('body','text','information')),fonts[-1])
 return display,body

def palette(d):
 return [{**p,'c':C(p['hex'])} for p in d['palette']]
def theme(d):
 pal=palette(d);bg=next((p for p in pal if p['role']=='background'),pal[0]);ink=next((p for p in pal if p['role']=='text'),pal[min(1,len(pal)-1)])
 accent=next((p for p in pal if p['role']=='primary'),next((p for p in pal if p['role']=='accent'),ink))
 return bg,ink,accent

def header(c,d,ink,bg,body,page):
 label=d['name'].upper()+('  /  VISUAL IDENTITY' if page==1 else '  /  SYSTEM IN USE')
 fit(c,70,48,label,body['bold'],14,ink['c'],880,10)
 text(c,1030,48,f'{page:02d} / 02',body['regular'],13,ink['c']);rule(c,70,65,1130,65,ink['c'],1)
def hero_decor(c,d,bg,ink,acc):
 """Give the identity a source-shaped stage without altering its logo asset."""
 bid=d['id'];area=(70,93,1060,238)
 if bid=='creative-practice-zine':
  for j,h in enumerate((64,40,64,40)):
   rect(c,70+j*20,264-h,13,h,acc['c'])
  area=(150,93,980,238)
 elif bid=='cost-scenario-planner':
  surface=next((p['hex'] for p in d['palette'] if p['role']=='surface'),bg['hex'])
  rect(c,70,92,1060,241,C(surface));rule(c,90,320,1110,320,acc['c'],3);area=(90,100,1020,207)
 elif bid=='annual-community-review':
  rule(c,70,94,1130,94,ink['c'],3);rule(c,70,102,1130,102,ink['c'],.8)
  rule(c,70,324,1130,324,ink['c'],.8);area=(70,113,1060,204)
 elif bid=='concept-comparison-readout':
  rule(c,70,324,582,324,ink['c'],.8);rule(c,618,324,1130,324,ink['c'],.8)
  area=(70,93,1060,223)
 elif bid=='creative-workshop-offering':
  rect(c,70,105,7,208,acc['c']);area=(95,95,1035,223)
 elif bid=='evaluation-log-notebook':
  surface=next((p['hex'] for p in d['palette'] if p['role']=='surface'),bg['hex'])
  rect(c,70,93,1060,239,C(surface));rect(c,70,93,42,239,acc['c']);area=(126,101,985,220)
 elif bid=='creative-business-model':
  area=(70,93,1060,238)
 elif bid=='photocopied-assembly-public-graphics':
  rect(c,70,93,46,239,acc['c']);rect(c,128,305,1002,18,ink['c']);area=(132,93,997,202)
 return area
def section(c,y,title,desc,ink,body):
 rule(c,70,y,1130,y,ink['c'],.8);text(c,70,y+28,title,body['bold'],15,ink['c'])
 if desc:fit(c,1130-pdfmetrics.stringWidth(desc,body['regular'],13),y+28,desc,body['regular'],13,ink['c'],500)

def draw_suite(c,d,y0,bg,ink,acc,body):
 cards=[('primary','PRIMARY / FIRST CONTACT'),('secondary','SECONDARY / COMPACT'),('reverse','REVERSE / CONTRAST FIELD')]
 for i,(kind,label) in enumerate(cards):
  x=70+i*365;field=ink['c'] if kind=='reverse' else bg['c'];foreground=bg['c'] if kind=='reverse' else ink['c']
  rect(c,x,y0,330,205,field,None if kind=='reverse' else ink['c'],.6)
  logo(c,kind_asset(d,kind),x+22,y0+19,286,133)
  text(c,x+14,y0+185,label,body['bold'],11,foreground)

def draw_palette(c,d,y0,bg,ink,body):
 pal=palette(d);n=len(pal);cols=5 if n>8 else 4 if n>5 else min(n,5);rows=math.ceil(n/cols);gap=16;cw=(1060-(cols-1)*gap)/cols;step=100 if n>5 else 115
 for i,p in enumerate(pal):
  x=70+(i%cols)*(cw+gap);top=y0+(i//cols)*step
  rect(c,x,top,cw,51 if n>5 else 62,p['c'],ink['c'] if p['hex'].upper()==bg['hex'].upper() else None,.5)
  fit(c,x,top+(70 if n>5 else 82),p['name'].upper(),body['bold'],12,ink['c'],cw)
  text(c,x,top+(88 if n>5 else 101),p['hex'].upper(),body['regular'],11,ink['c'])
 return rows*step

def draw_type(c,d,y0,bg,ink,acc,fonts,body):
 show=fonts[:3];gap=20;cw=(1060-gap*(len(show)-1))/len(show)
 for i,f in enumerate(show):
  x=70+i*(cw+gap)
  if i:rule(c,x-10,y0,x-10,y0+128,acc['c'],.7)
  text(c,x,y0+83,'Aa',f['bold'],77,ink['c'])
  fit(c,x+110,y0+30,(f['role']+' / '+f['render']).upper(),body['bold'],13,ink['c'],cw-115)
  fit(c,x+110,y0+59,'ABCDEFGHIJKL',f['regular'],16,ink['c'],cw-116,11)
  fit(c,x+110,y0+80,'MNOPQRST 012345',f['regular'],15,ink['c'],cw-116,11)
  if f['exact']=='exact':label='Source face · bundled'
  else:label='Source '+f['source']+' · kit '+f['render']
  wrap(c,x,y0+118,label,body['regular'],12,ink['c'],cw-4,15,2)
 return 164

def app_zine(c,x,t,w,h,d,bg,ink,acc,display,body):
 rect(c,x,t,w,h,bg['c'],ink['c'],.6);rect(c,x+18,t+18,12,56,acc['c'])
 text(c,x+48,t+48,'01 / QUESTION',body['bold'],14,acc['c'])
 wrap(c,x+48,t+103,'What can the work make visible?',display['regular'],30,ink['c'],w-85,39,2)
 rule(c,x+48,t+154,x+w-25,t+154,acc['c'],2)
 wrap(c,x+48,t+190,'A chapter begins with one inspectable question.',body['regular'],17,ink['c'],w-80,22,2)
 text(c,x+48,t+h-22,'WORK IN VIEW  /  01',body['bold'],11,ink['c'])
def app_ledger(c,x,t,w,h,d,bg,ink,acc,display,body):
 rect(c,x,t,w,h,bg['c'],ink['c'],.7);rect(c,x,t,w,44,acc['c']);text(c,x+20,t+29,'CASE & COST   /   ONE PERIOD',body['bold'],15,C('#FFFFFF'))
 for i,(label,value) in enumerate([('Selected case','Workshop'),('Capacity','24 seats'),('Unit cost','$18'),('Estimated total','$432')]):
  top=t+82+i*47;rect(c,x+18,top-28,w-36,38,C('#FFF2CC') if i in (0,1) else C('#F4EBE6'))
  text(c,x+28,top,label,body['regular'],15,ink['c']);fit(c,x+w-150,top,value,body['bold'],15,C('#0000CC') if i in (0,1) else ink['c'],125)
  if i==3:rule(c,x+18,top+10,x+w-18,top+10,acc['c'],2)
def app_newspaper(c,x,t,w,h,d,bg,ink,acc,display,body):
 rect(c,x,t,w,h,bg['c'],ink['c'],.6);text(c,x+22,t+42,'THE COMMON THREAD',display['bold'],29,ink['c'])
 rule(c,x+22,t+50,x+w-22,t+50,ink['c'],3);rule(c,x+22,t+58,x+w-22,t+58,ink['c'],.8)
 text(c,x+22,t+82,'ISSUE 01  /  SHARED MAKING',body['bold'],11,acc['c'])
 wrap(c,x+22,t+127,'A year of small repairs',display['regular'],27,ink['c'],w-44,33,2)
 rule(c,x+w/2,t+161,x+w/2,t+h-25,ink['c'],.5)
 wrap(c,x+22,t+191,'A careful record of the sessions and the questions still open.',body['regular'],13,ink['c'],w/2-35,18,4)
 wrap(c,x+w/2+15,t+191,'Participation is counted. Lasting outcomes need more evidence.',body['regular'],13,ink['c'],w/2-38,18,4)
def app_comparison(c,x,t,w,h,d,bg,ink,acc,display,body):
 rect(c,x,t,w,h,bg['c'],ink['c'],.6);text(c,x+20,t+36,'TWO IDEAS  /  ONE QUESTION',display['bold'],23,ink['c'])
 for i,title in enumerate(('CONCEPT A','CONCEPT B')):
  bx=x+20+i*(w/2-3);bw=w/2-23
  rect(c,bx,t+58,bw,178,bg['c'],ink['c'],.8);text(c,bx+12,t+85,title,display['bold'],17,ink['c'])
  rule(c,bx+12,t+97,bx+bw-12,t+97,acc['c'],2)
  text(c,bx+12,t+129,'Same task',body['regular'],14,ink['c']);text(c,bx+12,t+154,'Same evidence',body['regular'],14,ink['c'])
  text(c,bx+12,t+211,'What differs?',body['bold'],13,ink['c'])
def app_workshop(c,x,t,w,h,d,bg,ink,acc,display,body):
 rect(c,x,t,w,h,bg['c'],ink['c'],.6);text(c,x+22,t+39,'HANDS AT WORK',display['bold'],30,ink['c'])
 wrap(c,x+22,t+84,'Begin with one simple material.',display['regular'],24,ink['c'],w-44,29,2)
 rect(c,x+22,t+115,w-44,38,acc['c']);text(c,x+38,t+140,'JOIN A WORKSHOP',body['bold'],14,bg['c'])
 for i,(n,s) in enumerate([('01','Make'),('02','Share'),('03','Take home')]):
  top=t+182+i*32;text(c,x+22,top,n,body['bold'],15,acc['c']);text(c,x+66,top,s,body['regular'],16,ink['c'])
def app_log(c,x,t,w,h,d,bg,ink,acc,display,body):
 rect(c,x,t,w,h,bg['c']);rect(c,x,t,112,h,C('#19392C'))
 text(c,x+18,t+39,'LOGS',display['bold'],18,ink['c']);text(c,x+132,t+39,'TRIAL / 004',display['bold'],21,acc['c'])
 rule(c,x+132,t+52,x+w-22,t+52,C('#66806C'),1)
 for i,(k,v) in enumerate([('STATE','In review'),('EVIDENCE','3 observations'),('UNCERTAINTY','Access still unknown')]):
  top=t+92+i*(52 if h<260 else 61);text(c,x+132,top,k,display['bold'],13,acc['c']);text(c,x+132,top+25,v,body['regular'],16,ink['c'])
def app_orbit(c,x,t,w,h,d,bg,ink,acc,display,body):
 rect(c,x,t,w,h,bg['c'],ink['c'],.6);text(c,x+22,t+37,'WHAT MUST BE TRUE?',display['bold'],24,ink['c'])
 cx=x+w/2;cy=t+160
 c.setStrokeColor(acc['c']);c.setLineWidth(1.5);c.circle(cx,yy(cy),50,stroke=1,fill=0)
 for a,word in [(0,'OFFER'),(math.pi/2,'TIME'),(math.pi,'COST'),(3*math.pi/2,'DELIVERY')]:
  px=cx+80*math.cos(a);py=cy+80*math.sin(a);c.circle(px,yy(py),23,stroke=1,fill=0)
  fit(c,px-20,py+4,word,body['bold'],10,ink['c'],40,8)
 text(c,cx-29,cy+6,'MODEL',display['bold'],15,ink['c'])
def app_press(c,x,t,w,h,d,bg,ink,acc,display,body):
 rect(c,x,t,w,h,bg['c'],ink['c'],.5);rect(c,x+20,t+20,52,h-40,acc['c'])
 c.saveState();c.translate(x+58,yy(t+h-32));c.rotate(90);c.setFillColor(bg['c']);c.setFont(display['bold'],24);c.drawString(0,0,'OPEN PRESS');c.restoreState()
 rect(c,x+93,t+27,w-118,63,ink['c']);fit(c,x+108,t+72,'MAKE ONE THING',display['bold'],27,bg['c'],w-148)
 text(c,x+109,t+131,'01  CUT',display['bold'],24,ink['c']);text(c,x+109,t+172,'02  ARRANGE',display['bold'],24,ink['c']);text(c,x+109,t+213,'03  PRINT',display['bold'],24,ink['c'])
 rule(c,x+108,t+227,x+w-25,t+227,acc['c'],3)

def application_family(d):
 bid=d['id'];fmt=d.get('format','presentation')
 if bid in ('creative-practice-calendar','festival-schedule-planner','team-time-planner'):return 'calendar'
 if fmt=='spreadsheet':return 'ledger'
 if bid in ('community-newspaper','culture-journal','evidence-brief-for-print','research-digest-and-follow-through','portfolio-reading-edition','printmaking-mini-zine'):return 'editorial'
 if any(q in bid for q in ('programme','program','invitation','festival','wall-poster','social-campaign')):return 'event'
 if any(q in bid for q in ('workbook','lesson-activity','learning-trail','practice-and-debrief','teaching-demonstration','workshop-game')):return 'workbook'
 if any(q in bid for q in ('storyboard','story-treatment','five-frame','project-evidence-story','product-launch-narrative')):return 'story'
 if any(q in bid for q in ('portfolio','recruiter-evidence-map','career-bridge')):return 'portfolio'
 if any(q in bid for q in ('catalogue','recipe-collection','exhibition-visitor-guide','material-sample')):return 'catalogue'
 if fmt=='site':return 'site'
 if any(q in bid for q in ('letter','proposal','scope','memorandum','decision-brief','grant-project')):return 'proposal'
 if any(q in bid for q in ('evidence','research','audit','readout','case-report','retrospective','discovery')):return 'evidence'
 if fmt=='presentation':return 'deck'
 return 'dossier'

def native_application(c,x,t,w,h,d,bg,ink,acc,display,body):
 """Small original artifact samples arranged in the identity's source format."""
 fam=application_family(d);name=d['name'];sample=d['voice']['sample'];other=d['voice'].get('secondaryExample','')
 rect(c,x,t,w,h,bg['c'],ink['c'],.6)
 source_tables={
  'collaboration-scope':(('INCLUDED','OUTSIDE'),(('Workshop plan','Extra sessions'),('One review','New deliverables'))),
  'decision-memorandum':(('CONDITION','OWNER','EVIDENCE'),(('Ready','Project lead','Source note'),('Open','Review team','Next check'))),
  'ux-research-decision-brief-edition':(('OPTION','EVIDENCE'),(('Keep the step','Task observations'),('Test a label','Follow-up study'))),
  'grant-project-summary':(('DELIVERY','COST','EVIDENCE'),(('Workshop','$120','Attendance'),('Review','$80','Notes'))),
  'material-sample-catalogue':(('SPECIMEN','DIMENSION','EVIDENCE'),(('Paper 01','A4','Source record'),('Ink 02','30 ml','Test print'))),
  'evidence-brief-for-print':(('SESSION','FILLED','AVAILABLE'),(('01','12 seats','16 seats'),('02','10 seats','16 seats'))),
  'community-program-a4-edition':(('TIME','SESSION'),(('10:00','Open workshop'),('11:30','Shared reading'))),
  'facilitation-field-guide':(('STEP','PROMPT'),(('Notice','What changed?'),('Compare','What differs?'))),
 }
 if d['id'] in source_tables:
  headers,rows=source_tables[d['id']];roles={item['role']:item['hex'] for item in d['palette']}
  header=C(roles.get('header',roles.get('primary',ink['hex'])));surface=C(roles.get('surface',bg['hex']))
  fit(c,x+20,t+39,name.upper(),display['bold'],23,ink['c'],w-40,13)
  widths=[(w-40)/len(headers)]*len(headers);top=t+61
  for j,label in enumerate(headers):
   xx=x+20+sum(widths[:j]);rect(c,xx,top,widths[j],41,header)
   fit(c,xx+9,top+27,label,body['bold'],11,bg['c'],widths[j]-18,8)
  for i,row in enumerate(rows):
   yy0=top+41+i*55
   for j,value in enumerate(row):
    xx=x+20+sum(widths[:j]);rect(c,xx,yy0,widths[j],55,surface,ink['c'],.3)
    fit(c,xx+9,yy0+32,value,body['regular'],12,ink['c'],widths[j]-18,9)
  text(c,x+20,t+h-17,'SAMPLE TABLE',body['regular'],10,ink['c'])
  return
 if d['id']=='cross-study-synthesis-atlas':
  nav=d['_fontsByRole']['navigation'];purple=C('#563B75');lavender=C('#F0EBF5');rust=C('#B4643D');charcoal=C('#2D3235')
  fit(c,x+20,t+38,'Where studies meet',display['bold'],26,ink['c'],w-40,17)
  text(c,x+20,t+61,'SYNTHESIS / STUDIES 01–03',nav['bold'],11,ink['c'])
  widths=(107,165,181);starts=(x+20,x+127,x+292)
  for j,label in enumerate(('STUDY','CONVERGENCE','DIFFERENCE')):
   rect(c,starts[j],t+78,widths[j],36,purple)
   fit(c,starts[j]+8,t+102,label,nav['bold'],11,bg['c'],widths[j]-16,9)
  for row,values in enumerate((('01','Shared task','Different setting'),('02','Same friction','New audience'))):
   top=t+114+row*39
   for j,value in enumerate(values):
    rect(c,starts[j],top,widths[j],39,lavender,ink['c'],.25)
    fit(c,starts[j]+8,top+25,value,body['regular'],12,ink['c'],widths[j]-16,10)
  for j,col in enumerate((purple,rust,charcoal)):
   rect(c,x+114+j*118,t+h-38,18,27,col)
  for j in range(5):
   rule(c,x+20,t+h-35+j*5,x+w-24,t+h-35+j*5,C('#E3DCEF'),3)
  return
 if d['id']=='research-wall-poster':
  cyan=C('#72C4CA');plum=C('#8B355A');mint=C('#CDEBE5');dark=C('#24232B')
  fit(c,x+20,t+35,'What can the evidence show?',display['bold'],24,ink['c'],w-40,15)
  rect(c,x+20,t+51,w-40,111,cyan)
  for j,(label,col) in enumerate((('QUESTION',plum),('METHOD',dark),('EVIDENCE',mint))):
   xx=x+32+j*150
   if j==0:
    c.setFillColor(col);c.circle(xx+50,yy(t+103),29,stroke=0,fill=1)
   elif j==1:
    c.setFillColor(col);p=c.beginPath();p.moveTo(xx+16,yy(t+132));p.lineTo(xx+87,yy(t+132));p.lineTo(xx+52,yy(t+72));p.close();c.drawPath(p,stroke=0,fill=1)
   else:rect(c,xx+22,t+71,62,62,col)
   text(c,xx+3,t+151,label,body['bold'],10,dark)
  text(c,x+20,t+192,'01  FINDING',body['bold'],12,ink['c']);text(c,x+173,t+192,'A specific observation',body['regular'],13,ink['c'])
  text(c,x+20,t+219,'SOURCE',body['bold'],12,ink['c']);text(c,x+173,t+219,'Linked to the record',body['regular'],13,ink['c'])
  return
 if d['id']=='design-sprint-wall-kit':
  burgundy=C('#562C30');paper=C('#F5F2EC');sage=C('#A9C4B9');amber=C('#F2C467')
  fit(c,x+20,t+36,'Move evidence into a test',display['bold'],22,ink['c'],w-40,14)
  for j,(label,fill) in enumerate((('FRAME',paper),('COMPARE',sage),('TEST',amber))):
   xx=x+20+j*152;rect(c,xx,t+56,137,148,fill,burgundy,.8)
   if j==0:
    c.setStrokeColor(burgundy);c.setLineWidth(2);c.circle(xx+68,yy(t+109),26,stroke=1,fill=0)
   elif j==1:rect(c,xx+41,t+80,56,56,fill,burgundy,2)
   else:rect(c,xx+34,t+101,69,14,burgundy)
   text(c,xx+12,t+186,label,body['bold'],11,burgundy)
  text(c,x+20,t+228,'PROMPT  /  EVIDENCE  /  NEXT DECISION',body['bold'],11,burgundy)
  return
 if d['id']=='museum-learning-trail':
  blue=C('#183C52');paper=C('#FFF8E6');gold=C('#E6B944')
  fit(c,x+20,t+35,'Choose one thing to notice',display['bold'],22,ink['c'],w-40,14)
  for j,label in enumerate(('CUP','PATTERN','TIMER')):
   xx=x+20+j*152;rect(c,xx,t+52,137,132,paper,blue,.8)
   if j==0:
    rule(c,xx+35,t+93,xx+99,t+93,blue,2);rule(c,xx+35,t+93,xx+45,t+148,blue,2);rule(c,xx+99,t+93,xx+89,t+148,blue,2);rule(c,xx+45,t+148,xx+89,t+148,blue,2)
   elif j==1:
    for row in range(3):
     for col in range(3):
      c.setFillColor(blue);c.circle(xx+45+col*23,yy(t+91+row*21),4,stroke=0,fill=1)
   else:
    c.setStrokeColor(blue);c.setLineWidth(2);c.circle(xx+68,yy(t+117),31,stroke=1,fill=0);rule(c,xx+68,t+117,xx+68,t+96,gold,3);rule(c,xx+68,t+117,xx+86,t+125,gold,3)
   text(c,xx+11,t+173,label,body['bold'],10,blue)
  text(c,x+20,t+214,'I NOTICED',body['bold'],11,blue);rule(c,x+113,t+215,x+w-20,t+215,blue,.7)
  return
 if d['id']=='lesson-activity-cards':
  rect(c,x+20,t+18,5,h-36,acc['c'])
  text(c,x+42,t+43,'CARD 04 / PATTERN',display['bold'],25,ink['c'])
  text(c,x+42,t+73,'MATERIALS',body['bold'],12,acc['c'])
  text(c,x+164,t+73,'Paper strips and two colors',body['regular'],13,ink['c'])
  rule(c,x+42,t+86,x+w-28,t+86,acc['c'],1.2)
  wrap(c,x+42,t+115,'Find the rule. Try it another way.',body['regular'],18,ink['c'],w-73,24,2)
  for j in range(4):rect(c,x+42+j*76,t+146,56,30,acc['c'] if j%2==0 else bg['c'],acc['c'],1)
  text(c,x+42,t+208,'YOUR TURN  /  CONTINUE THE PATTERN',body['bold'],12,acc['c'])
  return
 if d['id']=='project-reflection-journal':
  label=d['_fontsByRole']['labels'];rule_color=C('#A99E8D')
  fit(c,x+23,t+44,'An observation worth keeping',display['bold'],24,ink['c'],w-46,16)
  text(c,x+23,t+69,'FIELD NOTE  /  07 OCTOBER',label['bold'],11,acc['c'])
  rule(c,x+23,t+80,x+w-23,t+80,rule_color,1)
  wrap(c,x+23,t+112,'The same edge catches the light each afternoon.',body['regular'],16,ink['c'],w-46,21,2)
  rect(c,x+23,t+139,143,75,bg['c'],rule_color,.8)
  text(c,x+34,t+184,'IMAGE / SKETCH',label['regular'],10,ink['c'])
  text(c,x+183,t+161,'ATTEMPTED CHANGE',label['bold'],11,acc['c'])
  wrap(c,x+183,t+184,'Move the material and compare the result.',body['regular'],13,ink['c'],w-210,17,2)
  return
 if d['id']=='ux-research-case-report':
  label=d['_fontsByRole']['labels'];surface=C('#F2F5F7');header=C('#303E3B')
  fit(c,x+20,t+38,'A task before an opinion',display['bold'],25,ink['c'],w-40,16)
  text(c,x+20,t+63,'STUDY 01  /  FORMATIVE RESEARCH',label['bold'],11,ink['c'])
  wrap(c,x+20,t+96,'Understand the task before judging the interface.',body['regular'],15,ink['c'],w-40,20,2)
  for j,col in enumerate(('SOURCE ID','OBSERVATION','NEXT QUESTION')):
   bx=x+20+(0 if j==0 else 108 if j==1 else 295);bw=108 if j==0 else 187 if j==1 else 164
   rect(c,bx,t+121,bw,34,header);fit(c,bx+7,t+143,col,label['bold'],10,bg['c'],bw-14,8)
  for j,values in enumerate((('P01','Task paused','Check label'),('P02','Step retried','Test prompt'))):
   top=t+155+j*33
   for k,value in enumerate(values):
    bx=x+20+(0 if k==0 else 108 if k==1 else 295);bw=108 if k==0 else 187 if k==1 else 164
    rect(c,bx,top,bw,33,surface,ink['c'],.25);fit(c,bx+7,top+22,value,label['regular'],11,ink['c'],bw-14,9)
  return
 if d['id']=='open-studio-invitation':
  red=C('#AD351F');black=C('#161616')
  fit(c,x+21,t+62,'OPEN',display['bold'],53,black,w-43,35)
  fit(c,x+21,t+116,'STUDIO',display['bold'],53,red,w-43,35)
  text(c,x+24,t+143,'COME IN  /  SEE THE WORK',body['bold'],12,black)
  for j,col in enumerate((black,red,black,red)):
   xx=x+22+j*57;top=t+162+(j%2)*7
   rule(c,xx,top,xx+39,top,col,2.3);rule(c,xx,top,xx,top+30,col,2.3)
   rule(c,xx+39,top+5,xx+39,top+30,col,2.3);rule(c,xx+5,top+30,xx+39,top+30,col,2.3)
  text(c,x+285,t+173,'SATURDAY / 10 AM',body['bold'],12,black)
  text(c,x+285,t+197,'COMMUNITY HALL',body['regular'],12,black)
  text(c,x+285,t+221,'STEP-FREE ENTRY',body['regular'],11,black)
  return
 if d['id']=='festival-schedule-planner':
  navy=C('#152B3A');blue=C('#DBE9F1');green=C('#E4EBDD');tan=C('#EEE2DB');pink=C('#FADBDD');red=C('#A4262C')
  fit(c,x+20,t+37,'PROGRAMME DESK',display['bold'],22,ink['c'],w-40,14)
  widths=(75,125,125,135);labels=('TIME','HALL','STUDIO','COURTYARD');left=x+20;top=t+53
  for j,label in enumerate(labels):
   xx=left+sum(widths[:j]);rect(c,xx,top,widths[j],33,navy)
   text(c,xx+8,top+23,label,body['bold'],10,bg['c'])
  rows=(('10:00','Workshop','Reading','Open table'),('11:00','Talk','! Conflict','Break'))
  for i,values in enumerate(rows):
   yy0=top+33+i*62
   for j,value in enumerate(values):
    xx=left+sum(widths[:j]);fill=(bg['c'],blue,green if i==0 else pink,tan)[j]
    rect(c,xx,yy0,widths[j],62,fill,navy,.3)
    fit(c,xx+8,yy0+36,value,body['bold'] if j==0 else body['regular'],12,red if i==1 and j==2 else navy,widths[j]-15,9)
  text(c,x+20,t+226,'BOOKINGS BY TIME AND VENUE',body['bold'],10,navy)
  return
 if fam=='calendar':
  title='OCTOBER / SMALL EXPERIMENTS' if d['id']=='creative-practice-calendar' else name.upper()
  fit(c,x+20,t+37,title,display['bold'],23,ink['c'],w-40,13)
  practice=d['id']=='creative-practice-calendar'
  days=('PERSON','WEEK 1','WEEK 2','WEEK 3','WEEK 4') if d['id']=='team-time-planner' else ('MON','TUE','WED','THU','FRI','SAT','SUN') if practice else ('MON','TUE','WED','THU','FRI');cw=(w-40)/len(days)
  for j,day in enumerate(days):
   xx=x+20+j*cw
   if practice:
    rect(c,xx,t+53,cw-3,30,C(('#FAD3C3','#C6E5D7','#DCD0EF')[j%3]),C('#787878'),.45)
    text(c,xx+7,t+74,day,body['bold'],10,ink['c'])
   else:rect(c,xx,t+53,cw-4,30,ink['c']);text(c,xx+9,t+74,day,body['bold'],11,bg['c'])
  for row in range(2):
   for col in range(len(days)):
    xx=x+20+col*cw;yy0=t+88+row*65;field=next((p['hex'] for p in d['palette'] if p['role']=='input-surface'),bg['hex']) if (row,col) in ((0,1),(1,3)) else bg['hex']
    rect(c,xx,yy0,cw-(3 if practice else 4),59,C(field),C('#787878') if practice else ink['c'],.4)
    if d['id']=='team-time-planner' and col==0:text(c,xx+8,yy0+36,'A' if row==0 else 'B',body['bold'],15,ink['c'])
    else:text(c,xx+8,yy0+17,str(1+row*len(days)+col).zfill(2),body['bold'],11,ink['c'])
    if (row,col) in ((0,1),(1,3)):rule(c,xx+8,yy0+36,xx+cw-14,yy0+36,acc['c'],2)
  text(c,x+20,t+h-17,'People × weeks  /  amber entries' if d['id']=='team-time-planner' else 'Prompt  /  Space to try  /  Review',body['regular'],11,ink['c'])
 elif fam=='ledger':
  rect(c,x+18,t+18,w-36,41,ink['c']);fit(c,x+32,t+46,name.upper(),body['bold'],17,bg['c'],w-64,11)
  input_color=next((p['hex'] for p in d['palette'] if p['role']=='input-surface'),next((p['hex'] for p in d['palette'] if p['role']=='attention-surface'),bg['hex']))
  surface=next((p['hex'] for p in d['palette'] if p['role'] in ('surface','calculated-surface')),bg['hex'])
  for j,(label,value) in enumerate((('INPUT / 01','Edit a value'),('COMPARISON','Hold criteria'),('RESULT','Review the effect'))):
   yy0=t+72+j*49;rect(c,x+18,yy0,w-36,43,C(input_color if j==0 else surface),ink['c'],.3)
   text(c,x+31,yy0+28,label,body['bold'],13,ink['c']);fit(c,x+225,yy0+28,value,body['regular'],14,ink['c'],w-260,10)
  text(c,x+20,t+h-16,'Editable input stays distinct from a calculated reading.',body['regular'],10,ink['c'])
 elif fam=='editorial':
  fit(c,x+20,t+38,name,display['bold'],27,ink['c'],w-40,15);rule(c,x+20,t+48,x+w-20,t+48,ink['c'],2)
  text(c,x+20,t+69,'ISSUE 01  /  SAMPLE EDITION',body['bold'],10,acc['c'])
  wrap(c,x+20,t+106,sample,display['regular'],18,ink['c'],w-40,23,2)
  text(c,x+20,t+153,'BY THE EDITORIAL TEAM',body['bold'],10,ink['c'])
  rule(c,x+w/2,t+140,x+w/2,t+h-20,ink['c'],.6)
  wrap(c,x+20,t+166,other or sample,body['regular'],12,ink['c'],w/2-36,16,4)
  wrap(c,x+w/2+15,t+166,'A second column keeps the account and its context together.',body['regular'],12,ink['c'],w/2-34,16,4)
 elif fam=='event':
  rule(c,x+25,t+28,x+w-25,t+28,acc['c'],2);fit(c,x+25,t+77,name.upper(),display['bold'],30,ink['c'],w-50,16)
  wrap(c,x+25,t+116,sample,body['regular'],18,ink['c'],w-50,23,2)
  rule(c,x+25,t+144,x+w-25,t+144,acc['c'],1)
  text(c,x+25,t+174,'DATE  /  SATURDAY',body['bold'],12,ink['c'])
  text(c,x+25,t+197,'PLACE  /  COMMUNITY HALL',body['bold'],12,ink['c'])
  text(c,x+25,t+220,'ACCESS  /  STEP-FREE ENTRY',body['bold'],12,ink['c'])
 elif fam=='workbook':
  rect(c,x+20,t+20,5,h-40,acc['c']);fit(c,x+41,t+50,name.upper(),display['bold'],25,ink['c'],w-66,14)
  text(c,x+41,t+82,'01  WORKED EXAMPLE',body['bold'],12,ink['c'])
  wrap(c,x+41,t+107,sample,body['regular'],15,ink['c'],w-78,19,2)
  text(c,x+41,t+164,'02  YOUR TURN',body['bold'],12,ink['c'])
  for j in range(3):rule(c,x+41,t+188+j*21,x+w-30,t+188+j*21,ink['c'],.5)
 elif fam=='story':
  labels=(('01','REQUEST'),('02','HOLD'),('03','DECISION')) if d['id']=='product-launch-narrative' else (('01','SETUP'),('02','TURN'),('03','NEXT'))
  fit(c,x+20,t+39,name.upper(),display['bold'],25,ink['c'],w-40,14)
  for j,(n,label) in enumerate(labels):
   xx=x+18+j*160;rect(c,xx,t+64,146,142,bg['c'],ink['c'],.7);rect(c,xx+11,t+75,124,68,bg['c'],acc['c'],1)
   text(c,xx+11,t+164,n,display['bold'],22,acc['c']);text(c,xx+54,t+164,label,body['bold'],11,ink['c'])
  text(c,x+20,t+h-18,'SAMPLE STORYBOARD',body['bold'],10,ink['c'])
 elif fam=='portfolio':
  fit(c,x+20,t+39,name,display['bold'],26,ink['c'],w-40,15);rule(c,x+20,t+52,x+w-20,t+52,acc['c'],2)
  for j,(label,detail) in enumerate((('PROJECT','One clear contribution'),('EVIDENCE','A visible sample'),('REFLECTION','What changed or remains'))):
   yy0=t+92+j*52;text(c,x+24,yy0,label,body['bold'],12,ink['c']);text(c,x+166,yy0,detail,body['regular'],13,ink['c']);rule(c,x+24,yy0+14,x+w-25,yy0+14,ink['c'],.4)
 elif fam=='catalogue':
  fit(c,x+20,t+38,name.upper(),display['bold'],24,ink['c'],w-40,14)
  for j,(label,detail) in enumerate((('01','Object / material'),('02','Origin / process'),('03','Use / observation'))):
   yy0=t+62+j*58;rect(c,x+20,yy0,67,45,bg['c'],ink['c'],.6);text(c,x+34,yy0+30,label,display['bold'],18,acc['c']);text(c,x+104,yy0+28,detail,body['regular'],15,ink['c'])
 elif fam=='site':
  rect(c,x+18,t+18,w-36,38,ink['c']);fit(c,x+32,t+44,name.upper(),display['bold'],16,bg['c'],w-66,10)
  wrap(c,x+24,t+104,sample,display['regular'],20,ink['c'],w-48,25,2)
  for j,(label) in enumerate(('EXPLORE','DETAILS','NEXT STEP')):
   xx=x+22+j*156;rect(c,xx,t+143,143,75,bg['c'],acc['c'],.8);text(c,xx+10,t+178,label,body['bold'],11,ink['c'])
 elif fam=='proposal':
  fit(c,x+22,t+42,name,display['bold'],26,ink['c'],w-44,14);rule(c,x+22,t+54,x+w-22,t+54,acc['c'],1.5)
  text(c,x+22,t+78,'PURPOSE  /  SAMPLE PROPOSAL',body['bold'],11,ink['c'])
  wrap(c,x+22,t+111,sample,body['regular'],16,ink['c'],w-44,21,2)
  for j,s in enumerate(('01  Scope','02  Responsibilities','03  Decision')):text(c,x+22,t+174+j*24,s,body['bold'],12,ink['c'])
 elif fam=='evidence':
  fit(c,x+22,t+43,name.upper(),display['bold'],24,ink['c'],w-44,14);rule(c,x+22,t+56,x+w-22,t+56,acc['c'],1.5)
  rows=(('DATE / 01','What was believed'),('CHANGE / 02','What the record changed'),('REASON / 03','What remains open')) if d['id']=='research-retrospective' else (('OBSERVATION','What the record shows'),('INTERPRETATION','What it might mean'),('LIMIT / NEXT','What remains open'))
  for j,(label,detail) in enumerate(rows):
   yy0=t+92+j*48;text(c,x+23,yy0,label,body['bold'],12,ink['c']);text(c,x+206,yy0,detail,body['regular'],12,ink['c']);rule(c,x+23,yy0+12,x+w-23,yy0+12,ink['c'],.4)
 elif fam=='deck':
  text(c,x+22,t+39,'01  /  KEY MESSAGE',body['bold'],12,acc['c']);rule(c,x+22,t+51,x+w-22,t+51,acc['c'],2)
  wrap(c,x+22,t+110,sample,display['regular'],25,ink['c'],w-44,31,3)
  text(c,x+22,t+h-24,'CONTEXT    /    EVIDENCE    /    NEXT QUESTION',body['bold'],11,ink['c'])
 else:
  fit(c,x+22,t+42,name.upper(),display['bold'],25,ink['c'],w-44,14);rule(c,x+22,t+55,x+w-22,t+55,acc['c'],1.5)
  wrap(c,x+22,t+110,sample,body['regular'],18,ink['c'],w-44,23,2)
  for j,s in enumerate(('01  Context','02  Detail','03  Next step')):text(c,x+22,t+171+j*24,s,body['bold'],11,ink['c'])

def application(c,x,t,w,h,d,bg,ink,acc,display,body):
 funcs={'creative-practice-zine':app_zine,'cost-scenario-planner':app_ledger,'annual-community-review':app_newspaper,'concept-comparison-readout':app_comparison,'creative-workshop-offering':app_workshop,'evaluation-log-notebook':app_log,'creative-business-model':app_orbit,'photocopied-assembly-public-graphics':app_press}
 if d['id'] in funcs:return funcs[d['id']](c,x,t,w,h,d,bg,ink,acc,display,body)
 bid=d['id']
 if bid in ('applied-ai-workflow-case','architecture-concept-review','art-deco-workshop-poster','artist-exhibition','artist-residency-proposal','async-research-reading-deck','audience-routed-portfolio','beginner-practice-workbook','broadside-portfolio-pitch','capability-proof-sheet','capacity-ledger','career-bridge'):
  rect(c,x,t,w,h,bg['c'],ink['c'],.6)
  if bid=='applied-ai-workflow-case':
   text(c,x+20,t+34,'TRACE / 01',display['bold'],21,ink['c']);rule(c,x+20,t+47,x+w-20,t+47,acc['c'],2)
   for j,(head,detail) in enumerate((('INSTRUCTION','What was asked'),('BASELINE','What happened before'),('CHANGE','What shifted'),('LIMIT','What remains unknown'))):
    y=t+77+j*43;text(c,x+22,y,f'0{j+1}',display['bold'],18,acc['c']);text(c,x+66,y,head,body['bold'],14,ink['c']);text(c,x+227,y,detail,body['regular'],13,ink['c'])
  elif bid=='architecture-concept-review':
   text(c,x+20,t+35,'ROOM STUDY / TWO ARRANGEMENTS',display['bold'],18,ink['c'])
   for j,label in enumerate(('CONCEPT A','CONCEPT B')):
    bx=x+20+j*238;rect(c,bx,t+53,218,166,bg['c'],ink['c'],1)
    rect(c,bx+16,t+70,186,110,bg['c'],acc['c'],1.2)
    rect(c,bx+30+(j*30),t+87,57,39,bg['c'],ink['c'],.8)
    rect(c,bx+109-(j*20),t+135,51,24,bg['c'],ink['c'],.8)
    text(c,bx+13,t+208,label,body['bold'],11,ink['c'])
  elif bid=='art-deco-workshop-poster':
   brass=C(next((p['hex'] for p in d['palette'] if p['role']=='ornament'),acc['hex']))
   rule(c,x+27,t+28,x+w-27,t+28,brass,2);rule(c,x+45,t+37,x+w-45,t+37,brass,.8)
   fit(c,x+31,t+82,'CEDAR HOUSE',display['bold'],36,ink['c'],w-62,20)
   text(c,x+31,t+113,'WORKSHOPS',body['bold'],22,ink['c']);rule(c,x+31,t+127,x+w-31,t+127,brass,2)
   text(c,x+31,t+157,'PAPER / INK / FOLD',body['bold'],17,ink['c'])
   text(c,x+31,t+186,'SATURDAY  ·  10 AM–NOON',body['regular'],14,ink['c'])
   text(c,x+31,t+207,'Town Hall  ·  Step-free entry',body['regular'],13,ink['c'])
  elif bid=='artist-exhibition':
   text(c,x+18,t+34,'OBJECTS IN SEQUENCE',display['bold'],23,ink['c'])
   for j,(date,label) in enumerate((('01','Opening study'),('02','Objects in place'),('03','Return visit'))):
    y=t+68+j*59;rect(c,x+22,y,85,41,bg['c'],ink['c'],.7);text(c,x+35,y+27,date,display['bold'],19,acc['c'])
    text(c,x+126,y+16,label,body['bold'],15,ink['c']);rule(c,x+126,y+28,x+w-27,y+28,acc['c'],.8)
  elif bid=='artist-residency-proposal':
   text(c,x+23,t+49,'Common Material',display['bold'],29,ink['c']);rule(c,x+23,t+61,x+w-23,t+61,acc['c'],1.4)
   wrap(c,x+23,t+102,d['voice']['sample'],body['regular'],18,ink['c'],w-47,23,2)
   for j,s in enumerate(('01  CREATIVE PREMISE','02  PARTICIPANT EXPERIENCE','03  PRODUCTION NEEDS')):text(c,x+23,t+169+j*27,s,body['bold'],13,ink['c'])
  elif bid=='async-research-reading-deck':
   text(c,x+23,t+48,'ATLAS READING ROOM',display['bold'],30,ink['c']);rule(c,x+23,t+60,x+w-23,t+60,acc['c'],1.4)
   wrap(c,x+23,t+116,d['voice']['sample'],display['regular'],19,ink['c'],w-48,25,3)
   text(c,x+23,t+h-42,'READER MAP    /    EVIDENCE LINKS    /    NEXT LOOK',body['bold'],12,ink['c'])
  elif bid=='audience-routed-portfolio':
   rect(c,x+16,t+17,111,h-34,bg['c'],acc['c'],1.3);text(c,x+28,t+48,'ROUTES',body['bold'],14,ink['c'])
   for j,s in enumerate(('Design','Research','Teaching')):text(c,x+28,t+86+j*36,s,body['regular'],12,ink['c'])
   text(c,x+151,t+51,'SELECTED WORK',display['bold'],25,ink['c']);rule(c,x+151,t+64,x+w-23,t+64,acc['c'],2)
   for j,s in enumerate(('01  Practice case','02  Learning offer','03  Public writing')):text(c,x+151,t+105+j*41,s,body['bold'],13,ink['c'])
  elif bid=='beginner-practice-workbook':
   rect(c,x+20,t+18,5,h-36,acc['c']);text(c,x+42,t+48,'TRY ONE VERSION',display['bold'],26,ink['c'])
   text(c,x+42,t+87,'WORKED EXAMPLE',body['bold'],13,ink['c']);text(c,x+42,t+114,'Compare it with the criterion.',body['regular'],17,ink['c'])
   text(c,x+42,t+158,'YOUR ATTEMPT',body['bold'],13,ink['c'])
   for j in range(3):rule(c,x+42,t+182+j*22,x+w-30,t+182+j*22,ink['c'],.5)
  elif bid=='broadside-portfolio-pitch':
   fit(c,x+22,t+70,'LET STORIES',display['bold'],49,ink['c'],w-44,28)
   fit(c,x+22,t+126,'TRAVEL',display['bold'],52,ink['c'],w-44,28)
   for j,s in enumerate(('WORDS','PATHS','MOMENTS')):
    xx=x+22+j*154;rule(c,xx,t+154,xx+132,t+154,acc['c'],3);text(c,xx,t+182,s,body['bold'],14,ink['c'])
  elif bid=='capability-proof-sheet':
   text(c,x+24,t+49,'USEFUL PROOF',display['bold'],31,ink['c']);rule(c,x+24,t+63,x+w-24,t+63,acc['c'],2)
   for j,(head,detail) in enumerate((('CAPABILITY','A clear statement'),('EVIDENCE','One inspectable sample'),('NEXT','A useful conversation'))):
    yy0=t+105+j*48;text(c,x+24,yy0,head,body['bold'],13,ink['c']);text(c,x+174,yy0,detail,body['regular'],14,ink['c'])
  elif bid=='capacity-ledger':
   rect(c,x+17,t+19,w-34,45,ink['c']);text(c,x+33,t+48,'ROOM TO GATHER / CAPACITY',body['bold'],17,bg['c'])
   input_color=next((p['hex'] for p in d['palette'] if p['role']=='input-surface'),'#FFF2CC')
   result_color=next((p['hex'] for p in d['palette'] if p['role']=='surface'),bg['hex'])
   for j,(name,a,b) in enumerate((('Recorded','18 / 24','75%'),('Scenario input','20 / 24','editable'),('Comparison','+2 places','review'))):
    yy0=t+76+j*49;rect(c,x+20,yy0,w-40,43,C(input_color if j==1 else result_color),ink['c'],.35)
    text(c,x+30,yy0+28,name,body['regular'],14,ink['c']);text(c,x+275,yy0+28,a,body['bold'],15,ink['c']);fit(c,x+403,yy0+28,b,body['bold'],13,ink['c'],76,10)
  elif bid=='career-bridge':
   text(c,x+23,t+48,'Across Practice',display['bold'],30,ink['c']);text(c,x+23,t+77,'RESEARCH  /  DESIGN  /  TEACHING',body['bold'],13,ink['c']);rule(c,x+23,t+91,x+w-23,t+91,acc['c'],1.7)
   for j,s in enumerate(('FOCUS  Transferable work, clearly named','EVIDENCE  Relevant projects with dates','NEXT  The role this experience serves')):text(c,x+23,t+128+j*36,s,body['regular'],13,ink['c'])
  return
 return native_application(c,x,t,w,h,d,bg,ink,acc,display,body)

def rule_glyph(c,d,i,x,t,bg,ink,acc,display,body):
 """Small source-specific constructions above the three recognition rules."""
 bid=d['id'];fg=bg['c'] if i==2 else ink['c'];accent=acc['c']
 if bid=='creative-practice-zine':
  if i==0:
   for bx,ht in ((0,43),(29,30),(58,43),(87,30)):
    rect(c,x+bx,t+60-ht,18,ht,accent)
   text(c,x+127,t+53,'WORK',display['bold'],31,accent)
  elif i==1:
   text(c,x,t+48,'Aa',display['regular'],42,fg);text(c,x+106,t+48,'01 / CHAPTER',body['bold'],16,fg)
  else:rule(c,x,t+42,x+288,t+42,C('#C14137'),4)
 elif bid=='cost-scenario-planner':
  if i==0:
   rect(c,x,t+8,126,54,C('#FFF2CC'));rect(c,x+162,t+8,126,54,C('#F4EBE6'))
   text(c,x+12,t+42,'INPUT',body['bold'],15,C('#0000CC'));text(c,x+173,t+42,'RESULT',body['bold'],15,ink['c'])
  elif i==1:
   rect(c,x,t+11,288,48,C('#FFF2CC'));text(c,x+15,t+44,'CASE  01',body['bold'],20,C('#0000CC'))
  else:
   text(c,x,t+42,'$432',body['bold'],31,fg);rule(c,x,t+55,x+288,t+55,accent,3)
 elif bid=='annual-community-review':
  if i==0:
   text(c,x,t+38,'THREAD',display['bold'],27,fg);rule(c,x,t+47,x+288,t+47,fg,3);rule(c,x,t+56,x+288,t+56,fg,.8)
  elif i==1:
   rect(c,x,t+8,125,50,fg);rule(c,x+145,t+8,x+145,t+59,fg,.6);text(c,x+163,t+38,'STORY',body['bold'],18,fg)
  else:text(c,x,t+54,'01',display['bold'],50,accent)
 elif bid=='concept-comparison-readout':
  if i==0:text(c,x,t+44,'Aa',display['bold'],42,fg)
  elif i==1:
   rect(c,x,t+8,131,52,bg['c'],fg,1);rect(c,x+157,t+8,131,52,bg['c'],fg,1)
   text(c,x+12,t+41,'A',display['bold'],25,fg);text(c,x+169,t+41,'B',display['bold'],25,fg)
  else:rect(c,x,t+28,288,13,accent)
 elif bid=='creative-workshop-offering':
  if i==0:text(c,x,t+52,'Aa',display['regular'],47,fg)
  elif i==1:
   rect(c,x,t+12,260,48,accent);text(c,x+13,t+45,'JOIN THE WORKSHOP',body['bold'],16,bg['c'])
  else:
   for j in range(3):text(c,x+j*89,t+46,f'0{j+1}',display['bold'],29,fg)
 elif bid=='evaluation-log-notebook':
  if i==0:rect(c,x,t+6,38,57,C('#19392C'));rule(c,x+51,t+17,x+281,t+17,fg,.8)
  elif i==1:text(c,x,t+48,'TRIAL / 004',display['bold'],26,fg)
  else:
   text(c,x,t+27,'EVIDENCE',display['bold'],13,fg);rule(c,x,t+35,x+265,t+35,accent,1.5);text(c,x,t+55,'UNCERTAINTY',display['bold'],13,fg)
 elif bid=='creative-business-model':
  if i==0:
   c.setStrokeColor(accent);c.setLineWidth(3);c.circle(x+42,yy(t+35),28,stroke=1,fill=0);c.circle(x+42,yy(t+35),12,stroke=1,fill=0)
  elif i==1:
   rect(c,x,t+13,260,44,ink['c']);text(c,x+12,t+43,'WHAT MUST BE TRUE?',display['bold'],17,bg['c'])
  else:
   c.setStrokeColor(fg);c.setLineWidth(1);c.circle(x+134,yy(t+35),24,stroke=1,fill=0)
   for dx in (-92,92):c.circle(x+134+dx,yy(t+35),16,stroke=1,fill=0)
 elif bid=='photocopied-assembly-public-graphics':
  if i==0:text(c,x,t+49,'OPEN PRESS',display['bold'],33,fg)
  elif i==1:rect(c,x,t+7,38,55,accent);rect(c,x+50,t+20,220,30,fg)
  else:
   for j in range(3):text(c,x+j*88,t+50,str(j+1),display['bold'],45,fg)
 elif bid=='art-deco-workshop-poster' and i==2:
  accent=C(next((p['hex'] for p in d['palette'] if p['role']=='ornament'),acc['hex']))
  for j,label in enumerate(('DATE','VENUE','ACCESS')):
   xx=x+j*98;text(c,xx,t+27,label,body['bold'],12,fg);rule(c,xx,t+39,xx+82,t+39,accent,1.5)
 elif bid=='local-festival-sponsorship' and i==2:
  for j,label in enumerate(('SPONSOR','ORGANIZER','ASSUMPTION')):
   xx=x+j*98;fit(c,xx,t+26,label,body['bold'],11,fg,88,9);rule(c,xx,t+39,xx+83,t+39,accent,1.4)
 elif bid=='science-in-pictures-lecture' and i==1:
  rect(c,x,t+5,95,51,bg['c'],fg,.7);text(c,x+12,t+39,'01',display['bold'],26,fg)
  text(c,x+108,t+25,'SOURCE',body['bold'],11,fg);rule(c,x+108,t+31,x+282,t+31,accent,1)
  text(c,x+108,t+53,'Useful caption',body['regular'],12,fg)
 elif bid=='team-time-planner':
  lavender=C(next((p['hex'] for p in d['palette'] if p['role']=='surface'),bg['hex']))
  amber=C(next((p['hex'] for p in d['palette'] if p['role']=='input-surface'),bg['hex']))
  if i==0:
   rect(c,x,t+6,288,18,ink['c']);rect(c,x,t+26,288,35,lavender)
   text(c,x+10,t+19,'PLAN',body['bold'],10,bg['c']);text(c,x+10,t+49,'Working area',body['regular'],13,fg)
  elif i==1:
   rect(c,x,t+8,130,48,amber,fg,.7);rect(c,x+157,t+8,130,48,lavender,fg,.7)
   text(c,x+9,t+39,'EDITABLE',body['bold'],11,fg);text(c,x+166,t+39,'CALCULATED',body['bold'],11,fg)
  else:
   for row in range(3):
    for col in range(4):
     xx=x+col*72;yy0=t+7+row*18;field=amber if (row,col) in ((1,1),(2,2)) else lavender
     rect(c,xx,yy0,68,16,field,fg,.35)
   text(c,x+4,t+19,'P',body['bold'],9,ink['c']);text(c,x+75,t+19,'W1',body['bold'],9,ink['c']);text(c,x+147,t+19,'W2',body['bold'],9,ink['c'])
 elif bid=='capacity-ledger':
  amber=C(next((p['hex'] for p in d['palette'] if p['role']=='input-surface'),bg['hex']))
  pale=C(next((p['hex'] for p in d['palette'] if p['role']=='surface'),bg['hex']))
  if i==0:
   rect(c,x,t+5,288,18,ink['c']);rect(c,x,t+27,130,35,amber);rect(c,x+158,t+27,130,35,pale)
   text(c,x+10,t+19,'CAPACITY',body['bold'],9,bg['c']);text(c,x+9,t+49,'INPUT',body['bold'],11,fg);text(c,x+169,t+49,'RESULT',body['bold'],11,fg)
  elif i==1:
   for j,s in enumerate(('OVERVIEW','SESSIONS','DEFINITIONS')):
    xx=x+j*97;rect(c,xx,t+13,91,38,pale,fg,.5);fit(c,xx+7,t+38,s,body['bold'],10,fg,77,8)
  else:
   text(c,x,t+47,'18 / 24',display['bold'],32,fg);rule(c,x+158,t+33,x+275,t+33,accent,1.5);text(c,x+177,t+47,'75%',body['bold'],24,fg)
 else:
  # Draw the mechanism named by this identity's own source observation.
  # These are schematic guide diagrams, never substitutes for the production logo.
  observation=d['recognitionRules'][i].lower()
  if any(s in observation for s in ('chronology','timeline','sequence','numbered','stages','steps')):
   rule(c,x+15,t+31,x+273,t+31,fg,1)
   for j in range(3):
    cx=x+26+j*123;c.setFillColor(accent);c.circle(cx,yy(t+31),7,stroke=0,fill=1)
    text(c,cx-10,t+61,f'0{j+1}',body['bold'],13,fg)
  elif any(s in observation for s in ('column','side by side','alternatives','comparison','paired','two paths')):
   for j in range(2):
    bx=x+j*151;rect(c,bx,t+7,137,52,C(d['palette'][0]['hex']) if i!=2 else ink['c'],fg,.8)
    rule(c,bx+12,t+21,bx+125,t+21,accent,2)
    text(c,bx+12,t+45,'A' if j==0 else 'B',display['bold'],20,fg)
  elif any(s in observation for s in ('rail','margin','spine','sidebar')):
   rect(c,x,t+6,45,57,accent);rule(c,x+59,t+14,x+281,t+14,fg,1)
   rule(c,x+59,t+29,x+255,t+29,fg,.6);rule(c,x+59,t+44,x+271,t+44,fg,.6)
  elif any(s in observation for s in ('table','grid','cell','ledger','count','percentage','denominator')):
   for j in range(3):
    rect(c,x+j*98,t+8,89,48,C(d['palette'][0]['hex']) if i!=2 else ink['c'],fg,.7)
    text(c,x+j*98+12,t+39,str(j+1).zfill(2),body['bold'],17,fg)
  elif any(s in observation for s in ('caption','image','thumbnail','illustration','photograph')):
   rect(c,x,t+7,130,43,C(d['palette'][0]['hex']) if i!=2 else ink['c'],fg,.7)
   rule(c,x+12,t+43,x+59,t+18,accent,1.2);rule(c,x+59,t+18,x+104,t+43,accent,1.2)
   rule(c,x+146,t+15,x+279,t+15,fg,1);rule(c,x+146,t+29,x+263,t+29,fg,.7);rule(c,x+146,t+43,x+273,t+43,fg,.7)
  elif any(s in observation for s in ('type','typograph','font','letter','masthead','title','heading','name')):
   fit(c,x,t+48,d['name'],display['bold'],31,fg,278,14);rule(c,x,t+57,x+288,t+57,accent,2)
  elif any(s in observation for s in ('color','colour','accent','teal','blue','burgundy','rust','yellow','pink','cream','paper')):
   for j,p in enumerate(d['palette'][:4]):
    rect(c,x+j*74,t+12,61,42,C(p['hex']),fg if p['hex'].upper()==bg['hex'].upper() else None,.6)
  elif any(s in observation for s in ('frame','outline','border','rule','divider','line')):
   rect(c,x,t+10,288,46,C(d['palette'][0]['hex']) if i!=2 else ink['c'],fg,.8)
   rule(c,x+14,t+24,x+274,t+24,accent,2);rule(c,x+14,t+44,x+219,t+44,fg,.6)
  else:
   fit(c,x,t+38,d['name'].upper(),display['bold'],23,fg,280,13)
   rule(c,x,t+55,x+288,t+55,accent,2)

def second_app(c,x,t,w,h,d,bg,ink,acc,display,body):
 # Distinct second state: short-form information card, not a duplicate cover.
 rect(c,x,t,w,h,ink['c']);foreground=bg['c']
 if d.get('conditionalColors'):
  states=d['conditionalColors'][:8]
  text(c,x+22,t+35,'FUNCTIONAL STATES',body['bold'],13,foreground)
  rule(c,x+22,t+46,x+w-22,t+46,acc['c'],2)
  def state_label(state):
   named={
    'festival-schedule-planner':{'#DBE9F1':'HALL BOOKING','#152B3A':'VENUE TEXT','#FADBDD':'CONFLICT','#A4262C':'CONFLICT TEXT','#E4EBDD':'STUDIO BOOKING','#EEE2DB':'COURTYARD','#FDE4D5':'VALIDATION','#F6CF3E':'OUTSIDE HOURS'},
    'evidence-audit-scorecard':{'#E0EEE7':'SCORABLE','#18563B':'SCORABLE TEXT','#FFF1D1':'UNAVAILABLE','#704000':'UNAVAILABLE TEXT','#A4D8E2':'TIE','#101B24':'TIE TEXT','#FFC7CE':'INVALID WEIGHTS','#9C0006':'INVALID TEXT'},
   }
   explicit=named.get(d['id'],{}).get(state['hex'].upper())
   if explicit:return explicit
   rule=(state.get('sourceRules') or [{}])[0]
   condition=rule.get('condition','')
   if condition=='!':label='CONFLICT'
   elif condition=='0' and rule.get('operator')=='greaterThan':label='COUNT > 0'
   elif condition and len(condition)<=16 and not any(ch in condition for ch in ('(',')','=', '$')):
    label=condition.upper()
   else:
    source_range=rule.get('range','')
    sheet,_,cell=source_range.partition('!')
    label=(sheet+' '+''.join(ch for ch in cell.split(':')[0] if ch.isalpha())).upper() or 'WORKBOOK'
   return label+' / '+('TEXT' if state.get('role')=='conditional-text' else 'FILL')
  for i,state in enumerate(states):
   col=i%2;row=i//2;xx=x+22+col*247;yy0=t+62+row*42
   rect(c,xx,yy0,38,28,C(state['hex']),foreground,.45)
   fit(c,xx+46,yy0+13,state_label(state),body['bold'],11,foreground,174,8)
   text(c,xx+46,yy0+27,state['hex'].upper(),body['regular'],10,foreground)
  text(c,x+22,t+h-16,'Shown only when the workbook condition is met.',body['regular'],10,foreground)
  return
 text(c,x+22,t+38,'IN PRACTICE',body['bold'],13,foreground);rule(c,x+22,t+50,x+w-22,t+50,acc['c'],2)
 if d['id']=='cost-scenario-planner':
  lines=[('SELECTED CASE','Workshop'),('ASSUMPTION','24 seats'),('CONSEQUENCE','$432 estimate')]
 elif d['id']=='evaluation-log-notebook':
  lines=[('RECORD','004'),('RESULT','Provisional'),('NEXT TEST','Check access')]
 elif d['id']=='concept-comparison-readout':
  lines=[('ASK','Same task'),('COMPARE','Equal fields'),('DECIDE','Next test')]
 elif d['id']=='creative-workshop-offering':
  lines=[('MATERIAL','Paper + ink'),('DURATION','90 minutes'),('ACCESS','Ask ahead')]
 elif d['id']=='creative-practice-zine':
  lines=[('01 / QUESTION','What is visible?'),('02 / WORK','Show the making'),('03 / REFLECTION','What to test next')]
 elif d['id']=='annual-community-review':
  lines=[('REPORTED','12 sessions'),('COUNT','Participation only'),('LIMIT','No outcome claim')]
 elif d['id']=='creative-business-model':
  lines=[('OFFER','What is made?'),('TIME','What can fit?'),('DELIVERY','What must hold?')]
 elif d['id']=='photocopied-assembly-public-graphics':
  lines=[('MAKE','Start with shape'),('KEEP','Take a copy'),('SHARE','Show a step')]
 elif d['id']=='product-launch-narrative':
  lines=[('REQUEST','A workshop is proposed'),('ROOM HOLD','A place is reserved'),('DECISION','Review before confirming')]
 elif d['id']=='cross-study-synthesis-atlas':
  lines=[('STUDY ID','Keep each source visible'),('OVERLAP','Name shared evidence'),('DIFFERENCE','Retain disagreement')]
 elif d['id']=='research-wall-poster':
  lines=[('QUESTION','What is being tested?'),('FINDING','One bounded statement'),('SOURCE','A traceable evidence link')]
 elif d['id']=='design-sprint-wall-kit':
  lines=[('PROMPT','Frame the decision'),('EVIDENCE','Move the source card'),('TEST','Record the next step')]
 elif d['id']=='museum-learning-trail':
  lines=[('OBJECT','Look for one detail'),('RESPONSE','Record what you notice'),('ROUTE','Choose what to inspect next')]
 else:
  fam=application_family(d)
  examples={
   'calendar':[('PROMPT','One small experiment'),('SPACE','Leave room to write'),('REVIEW','Return after the attempt')],
   'ledger':[('INPUT','An editable value'),('RESULT','A calculated reading'),('CHECK','Definition and denominator')],
   'editorial':[('ISSUE','01 / Sample edition'),('STORY','Keep a byline with the account'),('CAPTION','Attach it to the image')],
   'event':[('DATE','Saturday, 10 AM'),('VENUE','Community Hall'),('ACCESS','Step-free entry')],
   'workbook':[('EXAMPLE','Show one worked attempt'),('TRY','Leave room to respond'),('REFLECT','Ask what changed')],
   'story':[('FRAME 01','Set the scene'),('FRAME 02','Show the turn'),('FRAME 03','Name the next beat')],
   'portfolio':[('ROLE','Name the contribution'),('PROOF','Link one visible sample'),('LEARNING','State the limit')],
   'catalogue':[('OBJECT','What is shown'),('SOURCE','Where it came from'),('NOTE','What remains uncertain')],
   'site':[('ROUTE','Choose an entry'),('DETAIL','Read one clear record'),('NEXT','Follow a useful link')],
   'proposal':[('SCOPE','Name the work'),('TERMS','State responsibilities'),('DECISION','Mark the next approval')],
   'evidence':[('OBSERVED','What the record shows'),('INFERRED','What it may suggest'),('OPEN','What to test next')],
   'deck':[('FRAME 01','One claim per slide'),('SUPPORT','Show the relevant evidence'),('NEXT','A bounded question')],
   'dossier':[('PURPOSE','Name the use'),('DETAIL','Keep the record clear'),('NEXT','Show the follow-through')],
  }
  lines=examples[fam]
 for i,(a,b) in enumerate(lines):
  top=t+94+i*(48 if h<260 else 55);text(c,x+23,top,a,body['bold'],13,foreground)
  wrap(c,x+184,top,b,body['regular'],13,foreground,w-209,16,2)
  rule(c,x+22,top+23,x+w-22,top+23,foreground,.35)
 text(c,x+22,t+h-23,'SAMPLE CONTENT',body['bold'],10,foreground)

def page_one(c,d,fonts):
 bg,ink,acc=theme(d);display,body=roles(fonts);rect(c,0,0,W,H,bg['c']);header(c,d,ink,bg,body,1)
 # Source-shaped stages vary, while the actual production lockup stays intact.
 logo(c,kind_asset(d,'primary'),*hero_decor(c,d,bg,ink,acc))
 wrap(c,70,378,d['summary'],body['regular'],20,ink['c'],1050,27,2)
 section(c,429,'THE MARK','A flexible identity with a clear first use',ink,body);draw_suite(c,d,470,bg,ink,acc,body)
 section(c,700,'COLOR','Roles from the source system',ink,body)
 pal_h=draw_palette(c,d,746,bg,ink,body)
 compact=pal_h>115
 ty=746+pal_h+(15 if compact else 24);section(c,ty,'TYPE','Portable rendering shown below',ink,body)
 draw_type(c,d,ty+43,bg,ink,acc,fonts,body)
 ay=ty+43+(141 if compact else 180);section(c,ay,'IN USE','Original sample applications',ink,body)
 app_h=245 if compact else 270
 application(c,70,ay+48,500,app_h,d,bg,ink,acc,display,body)
 second_app(c,610,ay+48,520,app_h,d,bg,ink,acc,display,body)
 foot=ay+48+app_h+28;rule(c,70,foot,1130,foot,ink['c'],.8)
 wrap(c,70,foot+32,d['voice'].get('secondaryExample',d['voice']['sample']),body['bold'],17,ink['c'],1000,21,2)
 text(c,70,min(1570,foot+64),'Fictional identity · Brand guide · 2026',body['regular'],11,ink['c'])
 if foot+64>1580:raise ValueError(f"{d['id']}: page one overflows: footer {foot+64}")
 c.showPage()

def page_two(c,d,fonts):
 bg,ink,acc=theme(d);display,body=roles(fonts);rect(c,0,0,W,H,bg['c']);header(c,d,ink,bg,body,2)
 section(c,112,'LOGO USE','Keep room around the identity',ink,body)
 rect(c,70,158,630,302,bg['c'],ink['c'],.6)
 c.setStrokeColor(acc['c']);c.setLineWidth(1.1);c.setDash(7,5);c.rect(110,yy(385),550,180,stroke=1,fill=0);c.setDash()
 logo(c,kind_asset(d,'primary'),145,224,480,126)
 rule(c,110,218,145,218,acc['c'],1);rule(c,110,212,110,224,acc['c'],1);rule(c,145,212,145,224,acc['c'],1)
 text(c,117,206,'x',body['bold'],12,acc['c'])
 wrap(c,91,437,'CLEAR SPACE / '+d.get('clearSpaceRule','Keep other content outside the frame.'),body['bold'],11,ink['c'],580,14,2)
 rect(c,735,158,395,302,bg['c'],ink['c'],.6);text(c,753,187,'MINIMUM WIDTHS',body['bold'],15,ink['c'])
 rule(c,753,200,1112,200,acc['c'],.7)
 mins=d.get('minimumSize',{});primary_width=int(mins.get('primaryWidthPx',220));secondary_width=int(mins.get('secondaryWidthPx',180))
 logo(c,kind_asset(d,'primary'),753+(359-primary_width)/2,219,primary_width,166)
 text(c,753,405,f'PRIMARY  /  {primary_width} px recommended width',body['bold'],12,ink['c'])
 detail=f'Secondary {secondary_width} px'
 if mins.get('symbolWidthPx'):detail+=f'  ·  symbol {mins["symbolWidthPx"]} px'
 text(c,753,430,detail,body['regular'],12,ink['c'])
 text(c,753,447,'Check legibility in each final output.',body['regular'],10,ink['c'])
 rect(c,70,491,1060,150,ink['c']);logo(c,kind_asset(d,'reverse'),210,509,780,95);text(c,88,625,'REVERSE LOCKUP / CONTRAST FIELD',body['bold'],11,bg['c'])
 section(c,682,'COLOR PAIRINGS','Reading colors first; accents carry emphasis',ink,body)
 pairs=[(bg['hex'],ink['hex'],'READING GROUND'),(ink['hex'],bg['hex'],'REVERSE GROUND')]
 if contrast(bg['hex'],acc['hex'])>=4.5:pairs.append((bg['hex'],acc['hex'],'FOCUSED ACCENT'))
 else:pairs.append((bg['hex'],ink['hex'],'ACCENT AS A RULE'))
 for i,(ground,fg,label) in enumerate(pairs):
  x=70+i*365;rect(c,x,735,330,180,C(ground),ink['c'] if ground==bg['hex'] else None,.5)
  fit(c,x+19,779,PAIR_LABELS.get(d['id'],d['name'].upper()),display['bold'],28,C(fg),292)
  text(c,x+19,815,label,body['regular'],15,C(fg))
  if i==2:
   accent_line=C(next((p['hex'] for p in d['palette'] if p['role']=='ornament'),acc['hex'])) if d['id']=='art-deco-workshop-poster' else acc['c']
   rule(c,x+19,850,x+307,850,accent_line,5 if d['id']=='art-deco-workshop-poster' else 3)
   if d['id']=='art-deco-workshop-poster':
    rule(c,x+93,844,x+93,850,accent_line,5);rule(c,x+222,844,x+222,850,accent_line,5)
  text(c,x+19,891,f'{fg.upper()} ON {ground.upper()}',body['bold'],11,C(fg))
 section(c,957,'RECOGNITION MOVES','Three source-grounded rules in use',ink,body)
 # The three cards are short visual rules with different abstract source forms.
 moves=MOVE_CAPTIONS.get(d['id'],[(move_label(v,i),v) for i,v in enumerate(d['recognitionRules'][:3])])
 for i,(label,move) in enumerate(moves[:3]):
  x=70+i*365;field=ink['c'] if i==2 else bg['c'];txtcol=bg['c'] if i==2 else ink['c']
  rect(c,x,1010,330,338,field,None if i==2 else ink['c'],.6)
  rule_glyph(c,d,i,x+18,1043,bg,ink,acc,display,body)
  rule(c,x+18,1125,x+310,1125,acc['c'] if i!=2 else txtcol,.8)
  wrap(c,x+18,1162,move,body['regular'],16,txtcol,289,23,5)
  text(c,x+18,1329,label,body['bold'],11,txtcol)
 rule(c,70,1402,1130,1402,ink['c'],.8)
 text(c,70,1437,'ADAPTATION',body['bold'],15,ink['c'])
 wrap(c,70,1470,d['adaptations'][0],body['regular'],17,ink['c'],1040,24,2)
 text(c,70,1556,d['name']+'  ·  Brand guide  ·  2026',body['regular'],11,ink['c'])
 c.showPage()

def render(d,out,media):
 fonts=register_fonts(d);d['_fontsByRole']={f['role']:f for f in fonts};out.parent.mkdir(parents=True,exist_ok=True);media.mkdir(parents=True,exist_ok=True)
 c=canvas.Canvas(str(out),pagesize=(W,H),pageCompression=1);c.setTitle(d['name']+' — Brand Guide')
 page_one(c,d,fonts);page_two(c,d,fonts);c.save()
 for i,suffix in ((1,'guide'),(2,'rules')):
  png=media/f"{d['id']}-{suffix}.png";stem=png.with_suffix('')
  subprocess.run(['pdftoppm','-f',str(i),'-l',str(i),'-singlefile','-scale-to','1600','-png',str(out),str(stem)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
  Image.open(png).convert('RGB').save(media/f"{d['id']}-{suffix}.webp",quality=90,method=6);png.unlink()
 return out

def prepare(root,id,profiles,logos,allow_produced=False):
 p=profiles[id];lp=logos[id]
 status=lp.get('status','')
 if status not in ('ready','approved','complete') and not (allow_produced and status.startswith('produced')):raise ValueError(f'{id}: logos status {status}')
 required={'primary','secondary','reverse','mono'};assets=lp.get('assets',[])
 missing=required-{a['kind'] for a in assets}
 if missing:raise ValueError(f'{id}: missing logo kinds {sorted(missing)}')
 brand=root/'brands'/id;src=brand/'guide-source';src.mkdir(parents=True,exist_ok=True)
 brand_record_path=brand/'brand.json'
 if not brand_record_path.exists():raise FileNotFoundError(f'{id}: kit prep has not created brand.json')
 brand_record=json.loads(brand_record_path.read_text())
 font_records=[]
 for f in brand_record['portableTypography']:
  if 'regular' not in f['files']:raise ValueError(f'{id}: missing regular font for {f["role"]}')
  paths={style:f['files'].get(style,f['files']['regular'])['path'] for style in ('regular','bold')}
  for path in (*paths.values(),f['licenseFile']):
   if not (brand/path).exists():raise FileNotFoundError(brand/path)
  font_records.append({'role':f['role'],'sourceFamily':f['sourceFamily'],'renderFamily':f['renderFamily'],'exactOrSubstitute':f['exactOrSubstitute'],'regular':paths['regular'],'bold':paths['bold'],'license':f['licenseFile'],'sourceFontDependency':f.get('sourceFontDependency')})
 public_profile={k:p[k] for k in ('id','name','summary','category','palette','conditionalColors','typography','recognitionRules','voice','logoDirection','invariants','adaptations') if k in p}
 data={**public_profile,'format':p['source']['format'],'logos':[{'kind':a['kind'],'png':a['png']} for a in assets], 'fonts':font_records,'brandDir':str(brand),'clearSpaceRule':lp.get('clearSpace',{}).get('rule','Keep other content outside the frame.'),'minimumSize':lp.get('minimumSize',{})}
 # Logo plan paths may be task-root-relative. Convert to brand-relative.
 for a in data['logos']:
  source=root/a['png'];a['png']=str(source.relative_to(brand))
 portable={**data,'brandDir':'..'}
 (src/'guide-data.json').write_text(json.dumps(portable,ensure_ascii=False,indent=2)+'\n')
 shutil.copy2(Path(__file__),src/'render_guide.py')
 (src/'README.md').write_text('Run `python3 render_guide.py` from any directory. Requires ReportLab, Pillow and `pdftoppm`.\nProduction logo PNG/SVG files are in `../assets/logos/`; selected font files and licenses are in `../assets/fonts/`.\nThe source typeface and any portable substitute are named in `guide-data.json`. Examples are fictional.\n')
 return data

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--ids',nargs='*');ap.add_argument('--all',action='store_true');ap.add_argument('--output');ap.add_argument('--draft',action='store_true',help='Render produced logo sets to staging for joint visual review');ap.add_argument('--publish-reviewed',action='store_true',help='Write lead-reviewed produced logo sets to public guide paths');args=ap.parse_args()
 if args.draft and args.publish_reviewed:ap.error('--draft and --publish-reviewed are mutually exclusive')
 if PORTABLE:
  d=json.loads((HERE/'guide-data.json').read_text());d['brandDir']=str(HERE.parent)
  render(d,Path(args.output) if args.output else HERE.parent/f"{d['id']}.pdf",HERE/'rendered');return
 root=ROOT
 profiles={p['id']:p for p in json.loads((root/'brand-profiles.json').read_text())['brands']}
 logos={p['brandId']:p for p in json.loads((root/'logo-plan.json').read_text())['brands']}
 ids=[id for id in profiles if id!='community-festival'] if args.all else args.ids or PILOTS
 failures=[]
 for id in ids:
  try:
   d=prepare(root,id,profiles,logos,allow_produced=args.draft or args.publish_reviewed)
   if args.draft:
    out=root/'staging/guide-previews'/f'{id}.pdf';media=root/'staging/guide-previews/media'
   else:
    out=root/'public/guides'/f'{id}.pdf';media=root/'public/media'
   render(d,out,media)
   print('draft' if args.draft else 'rendered',id,out)
  except Exception as e:
   print('FAILED',id,e,file=sys.stderr)
   if not args.draft:raise
   failures.append(id)
 if failures:raise SystemExit(f'{len(failures)} draft guide(s) failed: {", ".join(failures)}')
if __name__=='__main__':main()
