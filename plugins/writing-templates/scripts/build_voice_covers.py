#!/usr/bin/env python3
"""Original type-led cover projection; preserves source catalog and measured writing corpus."""
import argparse,json,hashlib,html,re,math
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
P='/System/Library/Fonts/Supplemental/'
FONTS={'black':P+'Arial Black.ttf','hand':P+'Bradley Hand Bold.ttf','essay':P+'Georgia.ttf','scene':P+'BigCaslon.ttf','mono':P+'Andale Mono.ttf','serif':P+'Baskerville.ttc','warm':P+'Arial Rounded Bold.ttf','italic':P+'Georgia Italic.ttf','news':P+'Times New Roman Bold.ttf','narrow':P+'DIN Condensed Bold.ttf','typewriter':P+'AmericanTypewriter.ttc','clean':P+'Arial.ttf','bold':P+'Arial Bold.ttf','chancery':P+'Apple Chancery.ttf','book':P+'Charter.ttc','engraved':P+'Copperplate.ttc'}
# Original editorial demonstrations, newly authored solely for these covers.
COPY={
'V01':'Choose the smaller trial. Keep the larger promise unmade.',
'V02':'Bring the rough version. We’ll find the useful part together.',
'V03':'What if the detour is where the real question begins?',
'V04':'By noon, three empty chairs had become the whole story.',
'V05':'The queue is shorter, but did we count the people who left?',
'V06':'“Available to whom?” she asked, and suddenly the tidy answer needed another question.',
'V07':'The lamp holds a small circle of light while the rest of the room waits.',
'V08':'The system saved us three clicks and introduced a fourth called “contact support.”',
'V09':'Call the desk before Friday; you can borrow a kit without an online account.',
'V10':'A restored draft becomes the current version; the earlier record remains available.',
'V11':'Try one sentence first, then read it aloud before you change the paragraph.',
'V12':'The pilot will record missed appointments; an uncontrolled comparison cannot establish what caused them.',
'V13':'Monday: three unanswered calls, one revised label, and a question I am keeping open.',
'V14':'The shelf holds the tools; the doorway holds the question of who can reach them.',
'V15':'Picture the empty chair, then tell me what would make someone want to sit down.',
'V16':'The door learned to open only after it stopped congratulating itself on being a wall.',
'V17':'The library proposes a six-week lending trial; approval and operating details are still pending.',
'V18':'I support the trial, and I need the borrowing conditions settled before we approve it.',
'V19':'Keep the side door open, count the failed attempts, and make the record answerable.',
'V20':'I kept your pencilled correction because it said what my polished sentence could not.',
'V21':'The ledger records six requests; the margin records the question the tally cannot answer.',
'V22':'The design succeeds where it makes refusal visible, and weakens where it mistakes silence for agreement.',
'V23':'The button worked; the person still needed to know what would happen after pressing it.',
'V24':'Replace “guaranteed results” with “proposed trial,” and the sentence finally tells the truth.',
'P25':'New uploads are unavailable; you can still read existing documents while we investigate the cause.',
'P26':'The queue restarted at noon; exports now work, but the earlier failures remain unexplained.',
'P27':'Count the missed requests before choosing the fix; a tidy total can hide the problem.',
'P28':'Choose the shortcut only if it preserves the record and leaves the exit open.',
'P29':'The wheel advances because each press changes the display; nothing behind the dial moves.',
'P30':'Bring one paragraph back into the light, and give its crowded sentence room to breathe.',
'P31':'Bring a paragraph if this workshop fits; declining the invitation needs no explanation.',
'P32':'Each person brings one draft, so the conversation begins with something everyone can help shape.',
'P33':'Think of revision as a new branch; the earlier path remains on the map.',
'P34':'One open door disproves “every entrance is locked,” but it tells us nothing about the others.',
'P35':'The ledger shows three requests; whether the sign confused anyone is still a question.',
'P36':'I can review the draft today; approving the final release belongs to the editor.',
'P37':'Keep the two notes that explain sign-in, and leave the poster colors for another discussion.',
'P38':'The button resets the display, not the universe; the toy has a modest jurisdiction.',
'P39':'The feature arrives Monday with one clear capability; the bigger claims can wait for evidence.',
'P40':'Her pencilled question remains beside the recipe, a small invitation to try the cake again.',
'P41':'Bring one paragraph on Saturday; if you want a place, register before Friday.',
'P42':'Next time, place the warning beside the action; this record cannot tell us whether that helps.',
'P43':'Plan access is not restore permission; the second rule survives the first promise.',
'P44':'Which version do you need, who may restore it, and what stays outside recovery?',
'P45':'At noon the queue stopped; by one it moved again, with two requests still unresolved.',
'P46':'Included in the plan means no extra charge; it does not mean everyone can approve.',
'P47':'Try the smaller pilot because it answers your question; leave the larger purchase undecided.',
'P48':'“I could not find the side door,” the participant said; the record contains no reason why.'}
# Each art direction has its own composition, typographic relationship and source-specific visual gesture.
DESIGNS=[
('V01','black','#f3ef30','#151811','#3d5543','decision slab',82,85,125,730),
('V02','hand','#fbe2c7','#723b34','#ec815c','handwritten workshop',84,92,130,735),
('V03','essay','#e4e9f2','#222b59','#928fb7','wandering marginal essay',74,118,130,720),
('V04','scene','#112f36','#fff0d1','#d19950','empty-chair stage',76,88,130,738),
('V05','mono','#fbf6ec','#1d2429','#c43e37','evidence brackets',66,114,114,735),
('V06','italic','#272347','#f8e7d2','#db9969','dialogue interruption',72,110,120,730),
('V07','italic','#172b2b','#eaf0b7','#a9b181','light circle lyric',74,96,116,730),
('V08','typewriter','#f2e968','#282620','#c86241','dry mechanical footnote',66,90,114,744),
('V09','bold','#e1f4fa','#12445b','#46a6b5','open public service',76,88,120,736),
('V10','mono','#152625','#d7f4d9','#51a47d','reference ruled specification',66,104,112,730),
('V11','warm','#ede4ff','#3a286d','#9a79d1','patient climbing steps',74,95,118,732),
('V12','book','#f4f0e6','#283c51','#999d97','research conditional frame',70,116,111,722),
('V13','typewriter','#eadfba','#483521','#a57749','notebook indexed scraps',66,114,112,724),
('V14','serif','#efe9dd','#444865','#ba877b','three braided ribbons',74,106,123,730),
('V15','bold','#f85939','#211d1b','#ffd379','spoken stage pulse',78,88,122,738),
('V16','book','#e4d7f2','#453367','#9d68a0','impossible doorway parable',74,98,122,740),
('V17','news','#f9f6e9','#182d38','#be8e61','news masthead architecture',72,87,130,735),
('V18','clean','#e7f1e9','#173a30','#569b78','diplomatic opposing edges',74,104,121,726),
('V19','narrow','#fbdd43','#172329','#c24238','manifesto broadside blocks',88,84,121,735),
('V20','hand','#f4e5ec','#6b374b','#bb748c','private letter folded corner',78,104,118,738),
('V21','typewriter','#e5e6dc','#3f433a','#858979','documentary ledger cut',66,90,117,745),
('V22','serif','#233344','#f5e7d1','#b98264','critical split judgment',76,98,108,740),
('V23','clean','#efedf7','#403050','#a5749b','microessay conversation block',74,106,117,734),
('V24','bold','#f1e9dc','#353728','#b73938','annotated red-pencil repair',72,96,119,734),
('P25','bold','#442b31','#f4e8cf','#d69e50','service consequence break',76,85,113,744),
('P26','typewriter','#d8e3dc','#253d35','#9a6e42','incident chronological spine',66,121,113,705),
('P27','book','#ebede6','#2a4244','#809282','evidence to decision beam',72,99,118,742),
('P28','black','#dfecb7','#30421c','#8aa553','recommendation conditional gate',76,84,118,745),
('P29','mono','#172846','#d5eef8','#579fbe','systems causal circuit',66,92,112,738),
('P30','italic','#f7e3b4','#664428','#d59350','sensory paper and light',76,112,118,715),
('P31','clean','#dff1e8','#276446','#64a88c','consent open threshold',76,100,116,729),
('P32','warm','#9c3739','#fff0d8','#db9360','community converging paths',74,95,117,737),
('P33','book','#e5ebf1','#324661','#98a8c4','comparison branching map',74,99,122,740),
('P34','bold','#ece35d','#353825','#ac6843','counterexample broken repeat',76,88,115,739),
('P35','typewriter','#e9dfcb','#454038','#947955','field record ruled margin',66,114,114,720),
('P36','black','#ede5e0','#593835','#a98373','boundary firm edge',76,109,116,717),
('P37','serif','#b5d8cf','#23433b','#578b7b','curation selected slips',76,102,115,680),
('P38','warm','#f6b5cc','#4b293f','#af587f','playful reset orbit',76,92,116,744),
('P39','bold','#34492e','#f5ecca','#abc283','measured launch horizon',76,89,113,739),
('P40','chancery','#e5d0bd','#5d4137','#ae8068','remembrance recipe trace',80,112,117,718),
('P41','bold','#eef0e9','#365666','#95bac6','compressed correspondence fold',76,92,127,744),
('P42','book','#dedbed','#44415e','#9092b5','after-action return path',74,98,114,739),
('P43','mono','#e9eced','#36464e','#8d6b5a','dry technical annotation tick',66,104,118,738),
('P44','serif','#234946','#f9eed4','#c4ad70','question field-guide compass',76,107,125,725),
('P45','typewriter','#e8dfbb','#453b22','#a38f53','timeline interrupted track',66,113,113,725),
('P46','clean','#e6e2f2','#3c355b','#9483b8','policy separated permissions',74,98,117,738),
('P47','black','#e2a34d','#352c20','#f1d092','earned proof weight',76,83,119,741),
('P48','italic','#e8eee5','#2c4b3c','#88aa8e','participant quote and open record',74,112,113,720)]
FONT_CACHE={}
def font(key):
 if key not in FONT_CACHE:
  f=TTFont(FONTS[key],fontNumber=0);FONT_CACHE[key]=(f,f.getGlyphSet(),f.getBestCmap(),f['head'].unitsPerEm,f['hmtx'].metrics)
 return FONT_CACHE[key]
def width(text,key,size):
 f,g,c,u,h=font(key);return sum(h[c.get(ord(ch),'.notdef')][0] for ch in text)*size/u

def wrap(text,key,size,w):
 lines=[];line=''
 for word in text.split():
  candidate=(line+' '+word).strip()
  if line and width(candidate,key,size)>w:lines.append(line);line=word
  else:line=candidate
 if line:lines.append(line)
 return lines

def outlined(lines,key,size,x,y,lead,fg,defs,align='left'):
 f,g,c,u,h=font(key);scale=size/u;parts=[];name=f['name'].getDebugName(1) or key
 for index,line in enumerate(lines):
  cursor=x-(width(line,key,size)/2 if align=='center' else 0)
  for char in line:
   glyph=c.get(ord(char),'.notdef');gid=key+'-'+str(ord(char))
   if gid not in defs:
    pen=SVGPathPen(g);g[glyph].draw(pen);defs[gid]='<path id="'+gid+'" d="'+pen.getCommands()+'"/>'
   parts.append(f'<use href="#{gid}" transform="translate({cursor:.3f} {y+index*lead:.3f}) scale({scale:.6f} {-scale:.6f})"/>');cursor+=h[glyph][0]*scale
 return '<g fill="'+fg+'" data-font-px="'+str(size)+'" aria-label="'+html.escape(' '.join(lines),quote=True)+'">'+''.join(parts)+'</g>'

def rect(x,y,w,h,c,**kw):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}" '+ ' '.join(k+'="'+str(v)+'"' for k,v in kw.items())+'/>'
def line(x1,y1,x2,y2,c,w=3,opacity=1):return f'<path d="M{x1} {y1}L{x2} {y2}" fill="none" stroke="{c}" stroke-width="{w}" opacity="{opacity}"/>'
def circle(x,y,r,c,opacity=1):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" opacity="{opacity}"/>'
def path(d,c,w=3,fill='none',opacity=1):return f'<path d="{d}" fill="{fill}" stroke="{c}" stroke-width="{w}" opacity="{opacity}"/>'

def art(ident,bg,fg,a):
 s=''
 # Entire compositions, each with a different rhetorical/visual relation; no generic icon tile.
 if ident=='V01':s=rect(0,0,900,36,fg)+rect(0,524,480,126,fg)+rect(480,524,58,126,a)+line(85,58,815,58,fg,8)
 elif ident=='V02':s=path('M70 65Q260 23 440 73T830 55',a,9)+path('M77 504Q200 480 350 512T510 500',a,9)+circle(822,90,25,a)+rect(0,610,480,40,a)
 elif ident=='V03':s=path('M52 75L86 75L86 492L52 492',a,3)+path('M510 515Q295 598 76 546L210 521',a,6)+line(790,45,840,45,fg,3)+line(840,45,840,94,fg,3)
 elif ident=='V04':s=rect(0,0,900,45,'#0a1f25')+path('M40 570L105 502L280 502L325 570M150 502L150 566M295 570L360 502L510 502',a,12)+rect(0,596,510,54,'#0a1f25')+circle(740,35,95,a,.15)
 elif ident=='V05':s=path('M84 60L52 60L52 486L84 486M840 60L870 60L870 486L840 486',a,7)+line(70,550,475,550,fg,3)+circle(77,550,15,a)
 elif ident=='V06':s=path('M68 65Q15 65 15 116L15 449Q15 499 68 499L94 499L114 520L124 499',a,4)+path('M840 173Q886 190 870 263',a,8)+circle(46,48,16,a)+circle(78,48,16,a)
 elif ident=='V07':s=circle(414,247,267,'#40513f',.35)+path('M22 567Q237 507 490 546',a,3)+circle(860,40,16,a,.9)+circle(776,122,5,a)+circle(829,180,5,a)
 elif ident=='V08':s=rect(0,0,38,650,a)+line(78,527,505,527,fg,4)+rect(78,547,110,36,a)+rect(210,547,65,36,fg)+line(798,24,868,78,fg,7)
 elif ident=='V09':s=rect(0,0,64,650,a)+path('M795 35L862 35L862 470L795 470',a,10)+path('M85 543L400 543L400 585M372 565L400 585L428 565',fg,5)
 elif ident=='V10':
  s=rect(58,45,790,450,'#203b34')+line(59,55,848,55,a,4)
  for yy in [202,316,430]:s+=line(60,yy,848,yy,a,1,.18)
  s+=path('M92 547L92 592L340 592',a,5)+rect(366,581,100,11,a)
 elif ident=='V11':
  for i in range(5):s+=rect(50+i*89,599-i*19,86,51+i*19,a,opacity=.18+i*.12)
  s+=circle(820,76,25,a)+path('M788 106Q810 172 849 185',a,5)
 elif ident=='V12':s=path('M64 49L843 49L843 493L64 493Z',a,2)+line(89,525,482,525,fg,4)+line(89,547,405,547,a,3)+line(89,569,297,569,a,3)
 elif ident=='V13':
  s=line(80,0,80,650,a,3)
  for yy in [50,516,560,604]:s+=line(10,yy,510 if yy>500 else 875,yy,a,2,.3)
  s+=rect(730,0,108,35,a)+circle(41,137,13,'#bba986')+circle(41,379,13,'#bba986')
 elif ident=='V14':s=path('M30 569Q147 502 272 554T503 548',a,11)+path('M10 608Q156 541 307 603T530 602',fg,11,.0 if False else 'none',.3)+path('M0 526Q160 581 290 525T523 536','#7f95a5',9)
 elif ident=='V15':s=rect(0,0,34,650,fg)+path('M58 20L347 20L361 32L642 32',a,15)+path('M61 581L61 513L129 513L129 551L197 551L197 598L265 598L265 561L338 561',fg,15)
 elif ident=='V16':s=path('M44 44L864 44L844 491L64 491Z',a,7)+path('M63 529L133 529L133 644L63 644Z',fg,5)+path('M133 529L199 565L199 648',a,5)+circle(110,586,12,a,.35)
 elif ident=='V17':s=line(40,50,860,50,fg,11)+line(40,77,860,77,fg,2)+line(40,514,506,514,fg,3)+rect(39,545,460,53,a)+line(792,101,858,101,fg,3)
 elif ident=='V18':s=rect(0,0,43,650,a)+rect(854,0,46,503,fg)+path('M98 532L248 532Q302 532 323 558L350 558',a,7)+path('M350 558L406 558L471 529',fg,7)
 elif ident=='V19':s=rect(0,0,900,46,fg)+rect(0,508,485,61,a)+rect(0,595,540,55,fg)+path('M798 82L858 82L858 495',fg,9)+rect(798,475,60,20,a)
 elif ident=='V20':s=path('M800 0L900 92L800 92Z',a,0,fill='#e6c6d5')+path('M82 537Q177 508 270 538T449 527',a,4)+path('M40 31L40 626L496 626',a,2)+circle(74,588,18,a,.4)
 elif ident=='V21':s=rect(0,0,54,650,a)+rect(742,21,132,32,fg)+line(73,518,527,518,fg,3)+line(85,566,513,566,a,3)+line(157,518,157,630,a,2)+line(363,518,363,630,a,2)+rect(742,62,132,20,a)
 elif ident=='V22':s=path('M55 42L847 42L847 494L55 494Z',a,3)+rect(0,539,258,111,a)+rect(258,539,259,111,'#17212b')+line(55,520,517,520,a,5)
 elif ident=='V23':s=circle(16,323,69,a,.45)+path('M92 537Q215 577 346 537L491 537',a,8)+path('M791 23L866 23L866 96',a,8)
 elif ident=='V24':s=path('M43 50L850 39L854 495L53 509Z','#cdbd9e',2)+path('M81 548L475 536',a,8)+path('M86 580L158 612L267 530',a,7)+rect(848,18,24,480,a)
 elif ident=='P25':s=rect(0,0,900,45,a)+rect(0,550,509,100,'#302026')+path('M55 73L55 497',a,8)+circle(815,94,19,a)+line(77,527,498,527,a,4)
 elif ident=='P26':s=line(74,53,74,606,a,5)+circle(74,65,15,a)+circle(74,240,15,a)+circle(74,472,15,a)+path('M74 591L474 591',fg,5)+rect(805,43,41,455,a,opacity=.2)
 elif ident=='P27':s=path('M49 488L49 510L522 510L522 488',a,8)+path('M86 60L86 22L793 22L793 60',fg,4)+rect(82,569,117,42,a)+rect(207,552,117,59,a)+rect(332,535,117,76,fg)
 elif ident=='P28':s=path('M28 25L870 25L870 495L816 495M52 25L52 490',fg,6)+path('M78 562L271 562L317 601L361 562L515 562',a,13)+circle(824,62,16,fg)
 elif ident=='P29':s=path('M38 36L854 36L854 495L38 495Z',a,2)+path('M46 557L156 557L156 613L282 613L282 557L488 557',a,5)+circle(46,557,14,a)+circle(488,557,14,a)+rect(48,64,25,24,a)
 elif ident=='P30':s=path('M0 64L900 0L900 49L0 114Z',a,0,fill=a,opacity=.2)+path('M26 591Q215 514 458 554',a,8)+path('M77 42L816 42',a,2)+circle(779,128,86,a,.07)
 elif ident=='P31':s=path('M26 20L852 20L852 493M65 20L65 495',a,4)+path('M58 579L296 579M356 579L508 579',a,9)+circle(329,579,14,fg)+path('M800 493L850 493',fg,8)
 elif ident=='P32':s=path('M40 650L162 531L277 589L419 527L522 575',a,20)+path('M849 57L830 203M18 107L48 266',a,10)+circle(100,549,15,'#fff0d8')+circle(405,554,15,'#fff0d8')
 elif ident=='P33':s=path('M65 587L220 587L220 535L480 535M220 587L365 616L489 616',a,8)+path('M30 32L860 32L860 495',fg,3)+circle(65,587,12,fg)+circle(480,535,12,fg)+circle(489,616,12,fg)
 elif ident=='P34':
  for i in range(7):s+=rect(42+i*57,538,33,80,fg if i!=3 else a)
  s+=path('M812 25L861 25L861 490L812 490',a,9)+path('M210 535L258 535L258 493L210 493Z',a,5)
 elif ident=='P35':s=line(78,0,78,649,a,2)+path('M795 30L847 30L847 496L795 496',fg,4)+path('M99 525L434 525M99 558L517 558M99 591L278 591',a,3)+circle(37,98,12,'#c5b499')+circle(37,406,12,'#c5b499')
 elif ident=='P36':s=rect(0,0,62,650,fg)+rect(818,0,82,495,a)+path('M102 540L504 540',fg,9)+path('M102 575L367 575',a,7)
 elif ident=='P37':s=path('M33 31L837 17L859 492L62 507Z','#8fc1b3',2,fill='#c7e5da')+path('M73 546L267 523L280 614L86 633Z',a,2,fill=a)+path('M300 555L513 540L519 626L311 637Z',fg,2,fill=fg)+line(806,52,849,93,fg,4)
 elif ident=='P38':s=circle(36,572,119,a,.5)+path('M33 34L837 34L860 490',fg,5)+path('M88 570Q230 478 387 568L468 568',a,11)+circle(464,568,24,fg)
 elif ident=='P39':s=rect(0,0,900,42,a)+path('M25 528L517 528L517 577L25 577Z',a,0,fill=a)+path('M59 615L417 615L497 650',bg,8)+circle(814,79,18,a)
 elif ident=='P40':s=path('M50 41Q64 296 50 503M95 550Q275 536 473 571',a,4)+path('M740 15L860 115L828 148',a,3)+circle(457,590,24,a,.25)+line(61,628,510,628,a,2)
 elif ident=='P41':s=path('M43 41L854 41L854 494L43 494Z',a,2)+path('M66 541L257 625L449 541',a,6)+line(66,541,449,541,fg,5)+rect(742,41,112,29,a)
 elif ident=='P42':s=path('M39 30L858 30L858 493L813 493',a,4)+path('M496 567Q252 658 69 573L147 573M69 573L85 628',a,9)
 elif ident=='P43':s=path('M62 38L848 38L848 493',fg,3)+path('M76 540L503 540M76 577L455 577M76 614L401 614',a,3)+path('M35 80L67 80M35 196L67 196M35 312L67 312M35 428L67 428',a,6)
 elif ident=='P44':s=path('M68 42L825 42L825 500L68 500Z',a,3)+path('M139 626L226 521L320 626M226 521L226 641',a,6)+circle(226,521,12,a)+line(55,25,846,25,a,2)
 elif ident=='P45':s=line(74,41,74,626,a,5)+path('M74 543L179 543L216 569L282 543L499 543',fg,5)+circle(74,41,15,a)+circle(74,271,15,a)+circle(74,492,15,a)+path('M780 33L845 33L845 493',a,3)
 elif ident=='P46':s=rect(0,0,34,650,a)+path('M66 46L850 46L850 494L66 494Z',a,2)+path('M78 552L272 552M335 552L501 552M302 529L302 617',fg,7)+rect(78,584,192,19,a)+rect(337,584,164,19,a)
 elif ident=='P47':s=rect(0,0,900,39,fg)+path('M54 613L132 613L132 576L264 576L264 539L512 539',fg,15)+path('M812 71L859 71L859 493',a,8)
 elif ident=='P48':s=path('M55 35L845 35L845 494L55 494Z',a,3)+path('M91 531L91 612L511 612',fg,4)+path('M320 531L320 612M91 566L511 566',a,2)+circle(490,612,12,a,.3)
 return s

def main():
 p=argparse.ArgumentParser();p.add_argument('--public-root',type=Path,required=True);p.add_argument('--evidence',type=Path,required=True);a=p.parse_args();root=a.public_root;cat=json.loads((root/'catalog.json').read_text());by={r['id']:r for r in cat['records']};records=[];manifest=[]
 for ident,key,bg,fg,accent,layout,size,x,y,w in DESIGNS:
  quote=COPY[ident];words=len(re.findall(r"[A-Za-z]+(?:[’'-][A-Za-z]+)*",quote));assert (9 if ident in ['V01','V02','V03','V04'] else 10)<=words<=18,(ident,words)
  lines=wrap(quote,key,size,w);lead=round(size*1.12)
  if y+(len(lines)-1)*lead>487:
   size=66;lead=74;lines=wrap(quote,key,size,w);y=112
  assert y+(len(lines)-1)*lead<=487,(ident,lines,size)
  assert max(width(s,key,size) for s in lines)<=w
  defs={};
  if ident in ['V07','V14','P32','P44']:
   outlined_text=outlined(lines,key,size,450,y,lead,fg,defs,align='center')
  elif ident in ['V13','V21']:
   outlined_text=''.join(outlined([chunk],key,size,x+[0,44,0,26,0,30][i],y+i*lead,lead,fg,defs) for i,chunk in enumerate(lines))
  else:outlined_text=outlined(lines,key,size,x,y,lead,fg,defs)
  if ident in ['V02','P37']:outlined_text='<g transform="rotate('+('1.5' if ident=='V02' else '-1.5')+' 450 280)">'+outlined_text+'</g>'
  svg='<svg xmlns="http://www.w3.org/2000/svg" width="900" height="650" viewBox="0 0 900 650" role="img" aria-labelledby="title desc"><title id="title">'+html.escape(by[ident]['name']+' — '+quote)+'</title><desc id="desc">Original synthetic cover example, newly authored for the graphic; not part of the measured library corpus.</desc><defs>'+''.join(defs.values())+'</defs>'+rect(0,0,900,650,bg)+art(ident,bg,fg,accent)+outlined_text+'</svg>'
  output=root/'previews'/f'{ident}.svg';output.parent.mkdir(exist_ok=True);output.write_text(svg);sha=hashlib.sha256(svg.encode()).hexdigest();record={'id':ident,'name':by[ident]['name'],'preview':f'previews/{ident}.svg','width':900,'height':650,'aspectRatio':'18/13','palette':{'background':bg,'ink':fg,'accent':accent},'font':{'family':font(key)[0]['name'].getDebugName(1),'rendering':'outlined glyph shapes; no external font dependency','quoteSourcePixels':size},'layout':layout,'visualIntent':layout+' uses a distinct reading field and meaningful graphic gesture for '+by[ident]['name']+'. The typography carries the demonstration; no measured result is implied.','coverQuote':{'text':quote,'authorship':'AI-authored original synthetic editorial cover demonstration','status':'new_cover_example_not_measured_not_reviewed_as_source_corpus','sourceSampleId':None,'sourceBriefId':None,'inheritedMeasuredValues':False},'quoteLines':lines,'quoteBaselineBottom':y+(len(lines)-1)*lead,'controlSafeRegion':{'x':540,'y':520,'width':360,'height':130},'sha256':sha}
  if ident in ['V01','V02','V03','V04']:
   raster=root/'artwork/personality-covers-01.jpg'
   if raster.exists():record['rasterArt']={'path':'artwork/personality-covers-01.jpg','kind':'AI-generated bespoke four-poster sheet','spritePosition':{'V01':'0% 0%','V02':'100% 0%','V03':'0% 100%','V04':'100% 100%'}[ident],'sheetWidth':1476,'sheetHeight':1066,'sha256':hashlib.sha256(raster.read_bytes()).hexdigest(),'quoteText':quote,'fallback':record['preview']}
  if ident in ['V07','V20']:
   raster=root/'artwork'/f'{ident}-image-led.jpg'
   if raster.exists():
    record['rasterArt']={'path':f'artwork/{ident}-image-led.jpg','kind':'AI-generated bespoke single cover','width':900,'height':651 if ident=='V07' else 650,'sha256':hashlib.sha256(raster.read_bytes()).hexdigest(),'quoteText':quote,'fallback':record['preview']}
  records.append(record);manifest.append({'path':str(output),'bytes':len(svg.encode()),'sha256':sha})
 payload={'schemaVersion':'wvl-cover-designs/1','status':'created_for_render_review_not_published','records':records,'provenance':'All cover examples are newly authored synthetic editorial demonstrations. They are not extracts, real outcomes, real participant quotations, measurements, or private personal source. Canonical guides, samples and benchmark hashes unchanged.','selfContained':True};(root/'data/cover-designs.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n');notes='# Writing personalities: original cover examples\n\nThese 48 short lines were newly authored for the cover graphics. They are fictional editorial demonstrations, including imagined dialogue and memory; none is a real quotation, outcome, private author sample or benchmark measurement. Source-corpus examples, reviews, feature values and hashes remain separate. Six have companion AI-generated artwork; all 48 have a self-contained typographic SVG fallback.\n\nThe 900×650 compositions use outlined lettering, distinct palettes, layouts and motifs. Visible quote text is at least 66 source pixels (22 pixels at 300px image width); no miniature metadata is drawn. The voice title belongs below the cover. A quiet bottom-right region remains for the existing View details control.\n\n'+'\n'.join('## '+rec['id']+' · '+rec['name']+'\n\n> '+rec['coverQuote']['text']+'\n\nVisual intent: '+rec['visualIntent']+'\n\nStatus: original synthetic cover example; not measured. Preview: ['+rec['id']+'](../'+rec['preview']+').\n' for rec in records)
 (root/'data/cover-notes.md').write_text(notes)
 a.evidence.parent.mkdir(parents=True,exist_ok=True);a.evidence.write_text(json.dumps({'schema':'wvl-cover-build/1','status':'created_not_yet_visual_acceptance','covers':48,'minimumQuoteFontPixels':min(r['font']['quoteSourcePixels'] for r in records),'files':manifest,'totalSvgBytes':sum(f['bytes'] for f in manifest),'canonicalEdits':False,'nativeRefresh':False},indent=2)+'\n');print(json.dumps({'covers':48,'bytes':sum(f['bytes'] for f in manifest),'minimumFont':min(r['font']['quoteSourcePixels'] for r in records)}))
if __name__=='__main__':main()
