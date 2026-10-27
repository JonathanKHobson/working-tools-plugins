// Pure frame-index drawing. Project text, palette and art are supplied by project.json.
export const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
const ease=x=>{x=clamp(x);return x*x*(3-2*x)};
export function stateAt(frame,project){
 if(!Number.isInteger(frame)||frame<0)throw new RangeError('frame');
 const t=Math.min(frame/project.fps,project.durationSeconds);
 const boundaries=[0,.8,3.3,5.8,8.3,12];let phase=boundaries.findIndex((v,i)=>i<4&&t>=v&&t<boundaries[i+1]);
 if(phase<0)phase=4;
 const start=boundaries[phase],local=t-start;
 return {frame,t,phase,local,arrive:ease(local/.45),reveal:ease((local-.2)/.5),hold:phase===4?t>=8.85:local>=.75};
}
function text(ctx,s,x,y,size,color,font='DM',align='left'){
 ctx.fillStyle=color;ctx.font=`${size}px ${font}`;ctx.textAlign=align;ctx.textBaseline='alphabetic';ctx.fillText(s,x,y);
}
function round(ctx,x,y,w,h,r,c){ctx.fillStyle=c;ctx.beginPath();ctx.roundRect(x,y,w,h,r);ctx.fill()}
function line(ctx,x1,y1,x2,y2,color,width=3){ctx.strokeStyle=color;ctx.lineWidth=width;ctx.lineCap='round';ctx.beginPath();ctx.moveTo(x1,y1);ctx.lineTo(x2,y2);ctx.stroke()}
function fit(ctx,img,x,y,w,h){if(!img)return;let k=Math.min(w/img.width,h/img.height),dw=img.width*k,dh=img.height*k;ctx.drawImage(img,x+(w-dw)/2,y+(h-dh)/2,dw,dh)}
function pop(ctx,img,x,y,w,h,a){if(!img)return;ctx.save();ctx.globalAlpha=clamp(a);fit(ctx,img,x,y,w,h);ctx.restore()}
function label(ctx,s,x,y,c,size=22){text(ctx,s,x,y,size,c,'DMBold')}
function drawDiagram(ctx,s,project,L,p){
 const C=project.palette;let x=L.diagramX,y=L.diagramY,w=L.diagramW,h=L.diagramH;
 ctx.save();ctx.globalAlpha=s.reveal;
 if(p===0){
  round(ctx,x,y,w*.61,h*.42,22,C.aqua);text(ctx,project.diagramLabels.question,x+26,y+36,L.small,C.muted,'DMBold');text(ctx,project.steps[0].example,x+26,y+77,L.diagram,C.ink,'DMBold');
  line(ctx,x+w*.64,y+h*.21,x+w*.76,y+h*.21,C.teal,7);round(ctx,x+w*.77,y+h*.04,w*.23,h*.34,20,C.yellow);text(ctx,project.diagramLabels.responsePrompt,x+w*.80,y+h*.13,L.small,C.ink,'DMBold');text(ctx,project.diagramLabels.response,x+w*.80,y+h*.25,L.diagram,C.ink,'DMBold');
 } else if(p===1){
  round(ctx,x,y,w*.62,h*.86,14,C.aqua);round(ctx,x+24,y+22,w*.42,12,6,C.teal);round(ctx,x+24,y+62,w*.52,8,4,'#A5CED0');round(ctx,x+24,y+87,w*.46,8,4,'#A5CED0');
  label(ctx,project.diagramLabels.source,x+30,y+h*.64,C.ink,L.diagram);text(ctx,project.diagramLabels.sourceMeta,x+30,y+h*.75,L.small,C.muted);
  line(ctx,x+w*.68,y+h*.23,x+w*.84,y+h*.23,C.coral,6);line(ctx,x+w*.84,y+h*.23,x+w*.79,y+h*.16,C.coral,6);line(ctx,x+w*.84,y+h*.23,x+w*.79,y+h*.30,C.coral,6);
 } else {
  round(ctx,x,y,w*.34,h*.67,18,C.aqua);round(ctx,x+w*.62,y,w*.34,h*.67,18,C.aqua);label(ctx,project.diagramLabels.try,x+30,y+55,C.ink,L.diagram);label(ctx,project.diagramLabels.compare,x+w*.65,y+55,C.ink,L.diagram);
  line(ctx,x+w*.38,y+h*.3,x+w*.58,y+h*.3,C.teal,7);line(ctx,x+w*.58,y+h*.3,x+w*.53,y+h*.22,C.teal,7);line(ctx,x+w*.58,y+h*.3,x+w*.53,y+h*.38,C.teal,7);
  round(ctx,x+33,y+86,w*.18,11,5,C.yellow);round(ctx,x+w*.65,y+86,w*.18,11,5,C.coral);
 }
 ctx.restore();
}
export function drawFrame(ctx,frame,project,images,format){
 const dims=project.formats[format];if(!dims)throw new Error('unknown format');const [W,H]=dims,C=project.palette,s=stateAt(frame,project),portrait=format==='portrait';
 if(ctx.canvas.width!==W||ctx.canvas.height!==H)throw new Error('canvas dimensions');
 // reset() discards an inherited clip, transforms, shadows, paths and drawing state.
 if(typeof ctx.reset!=='function')throw new Error('Canvas 2D reset() required');ctx.reset();ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle=C.white;ctx.fillRect(0,0,W,H);
 let L=portrait?{left:58,top:90,head:61,body:29,small:22,diagram:29,diagramX:70,diagramY:570,diagramW:570,diagramH:230,artX:422,artY:832,artW:196,artH:212}: {left:72,top:75,head:68,body:31,small:23,diagram:28,diagramX:80,diagramY:384,diagramW:700,diagramH:220,artX:872,artY:265,artW:325,artH:355};
 // Open white reading field, small painted cues beyond it.
 round(ctx,portrait?450:945,portrait?85:50,portrait?220:280,portrait?180:190,120,C.aqua);
 pop(ctx,images.flares,portrait?560:1090,portrait?111:73,portrait?90:95,portrait?70:80,1);
 text(ctx,'A SMALL CHECK',L.left,L.top,L.small,C.muted,'DMBold');
 if(portrait){text(ctx,project.titleFirst,L.left,186,L.head,C.ink,'Fredoka');text(ctx,project.titleSecond,L.left,259,L.head,C.coral,'Fredoka');pop(ctx,images.underline,L.left,263,260,58,1)}
 else {text(ctx,project.titleFirst,L.left,174,L.head,C.ink,'Fredoka');text(ctx,project.titleSecond,L.left+ctx.measureText(project.titleFirst).width+16,174,L.head,C.coral,'Fredoka');pop(ctx,images.underline,L.left+335,184,300,64,1)}
 if(s.phase===4){
  const yy=portrait?380:286,lh=portrait?79:72;
  project.steps.forEach((step,i)=>{const y=yy+i*lh;round(ctx,L.left,y-32,42,42,21,[C.teal,C.coral,C.yellow][i]);text(ctx,String(i+1),L.left+21,y-2,24,C.ink,'DMBold','center');text(ctx,step.action,L.left+60,y,L.body,C.ink,'DMBold')});
  if(portrait){line(ctx,L.left,670,W-L.left,670,C.teal,4);text(ctx,project.takeawayLines[0],L.left,736,39,C.ink,'Fredoka');text(ctx,project.takeawayLines[1],L.left,787,39,C.ink,'Fredoka');pop(ctx,images.coralUnderline,L.left,797,365,56,1);pop(ctx,images.questioner,368,849,230,240,1);pop(ctx,images.logo,572,1134,87,95,1);}
  else {line(ctx,L.left,535,820,535,C.teal,4);text(ctx,project.takeawayLines[0],L.left,600,44,C.ink,'Fredoka');ctx.font='44px Fredoka';const endX=L.left+ctx.measureText(project.takeawayLines[0]).width+17;text(ctx,project.takeawayLines[1],endX,600,44,C.ink,'Fredoka');pop(ctx,images.coralUnderline,endX,609,385,56,1);pop(ctx,images.questioner,928,300,260,270,1);pop(ctx,images.logo,1160,590,75,82,1);}
  return s;
 }
 if(s.phase===0){
  text(ctx,'An answer can sound certain.',L.left,portrait?412:302,L.body,C.ink,'DMBold');text(ctx,'Make its claim easy to inspect.',L.left,portrait?458:345,L.body,C.muted);
  pop(ctx,images.explorer,L.artX,L.artY,L.artW,L.artH,s.arrive);pop(ctx,images.logo,portrait?572:1160,portrait?1134:590,portrait?87:75,portrait?95:82,1);return s;
 }
 const step=project.steps[s.phase-1],num=s.phase;let actionY=portrait?391:294;
 round(ctx,L.left,actionY-30,44,44,22,[C.teal,C.coral,C.yellow][num-1]);text(ctx,String(num),L.left+22,actionY+1,25,C.ink,'DMBold','center');
 text(ctx,step.action,L.left+58,actionY,L.body,C.ink,'DMBold');
 if(portrait){const words=step.why.split(' ');let row='',yy=actionY+58;ctx.font='25px DM';for(const word of words){const next=row?row+' '+word:word;if(ctx.measureText(next).width>600&&row){text(ctx,row,L.left,yy,25,C.muted);yy+=34;row=word}else row=next}if(row)text(ctx,row,L.left,yy,25,C.muted)}else text(ctx,step.why,L.left,actionY+55,27,C.muted);
 drawDiagram(ctx,s,project,L,num-1);
 pop(ctx,images[step.character],L.artX,L.artY,L.artW,L.artH,s.arrive);
 if(portrait){text(ctx,step.note||step.example,L.left,1080,25,C.ink,'Shantell');pop(ctx,images.coralUnderline,L.left,1090,355,56,1)}
 else {text(ctx,step.note||step.example,L.left,660,23,C.ink,'Shantell');pop(ctx,images.coralUnderline,L.left,661,400,44,1)}
 pop(ctx,images.logo,portrait?572:1160,portrait?1134:590,portrait?87:75,portrait?95:82,1);
 return s;
}
