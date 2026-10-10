(function(){'use strict';
const drafts=new Map();
const RATIOS=['Auto','1:1','4:5','3:2','2:3','16:9','9:16'];
const DETAILS=['Concise','Balanced','Detailed'];
const BACKGROUNDS=['Scene','Transparent'];
let current=null,host=null,onChange=()=>{},nodes={};
const el=(tag,text,cls)=>{const n=document.createElement(tag);if(text!==undefined)n.textContent=text;if(cls)n.className=cls;return n;};
function draft(item){if(!drafts.has(item.id)){
  if(drafts.size>=100)drafts.delete(drafts.keys().next().value);
  drafts.set(item.id,{subject:'',ratio:RATIOS.includes(item.ratio)?item.ratio:'Auto',detail:DETAILS.includes(item.detail)?item.detail:'Balanced',background:'Scene',referenceNotes:'',prompt:item.prompt,checks:(item.checks||[]).map((_,i)=>i)});
}return drafts.get(item.id);}
function field(labelText,key,options,required=false){const wrap=el('div',undefined,'image-field'),label=el('label',labelText+(required?' · Required':''));const id='image-'+key;label.htmlFor=id;wrap.append(label);
 const input=options?el('select'):el(key==='subject'?'input':'textarea');input.id=id;
 if(options){options.forEach(v=>input.append(new Option(v,v)));input.value=draft(current)[key];}
 else {if(key==='subject'){input.type='text';input.placeholder='For example: '+current.exampleSubject;}else input.rows=key==='prompt'?9:3;input.value=draft(current)[key];input.maxLength=key==='subject'?1000:key==='prompt'?10000:2000;}
 input.addEventListener(options?'change':'input',()=>{draft(current)[key]=input.value;input.removeAttribute('aria-invalid');nodes[key]?.error?.setAttribute('hidden','');onChange();});wrap.append(input);
 const error=el('p','Enter '+labelText.toLowerCase()+' before sending.','image-error');error.id=id+'-error';error.hidden=true;wrap.append(error);nodes[key]={input,error};return wrap;}
function mount({item,host:target,onChange:changed}){current=item;host=target;onChange=changed||(()=>{});nodes={};const state=draft(item),frag=document.createDocumentFragment();
 frag.append(el('p','Try this template: edit the prompt, then send it to request an image.','image-note'));
 const grid=el('div',undefined,'image-grid');grid.append(field('Subject','subject',null,true),field('Aspect ratio','ratio',RATIOS),field('Detail','detail',DETAILS),field('Background','background',BACKGROUNDS));frag.append(grid);
 if(item.reference==='required')frag.append(el('p','This workflow needs an actual source image. Attach it in the conversation; notes below do not upload an image.','image-required-reference'));
 else if(item.reference==='optional')frag.append(el('p','A source image is optional. If you use one, attach it in the conversation.','image-note'));
 frag.append(field('Reference notes (optional)','referenceNotes'));
 frag.append(field('Image prompt','prompt',null,true));
 const reset=el('button','Restore recipe prompt','image-reset');reset.type='button';reset.addEventListener('click',()=>{state.prompt=item.prompt;nodes.prompt.input.value=item.prompt;nodes.prompt.error.hidden=true;nodes.prompt.input.removeAttribute('aria-invalid');onChange();});frag.append(reset);
 if(Array.isArray(item.checks)&&item.checks.length){const checks=el('fieldset',undefined,'image-checks');checks.append(el('legend','Review checks'));item.checks.forEach((check,index)=>{const label=el('label');const input=el('input');input.type='checkbox';input.checked=state.checks.includes(index);input.addEventListener('change',()=>{state.checks=Array.from(checks.querySelectorAll('input:checked')).map(n=>Number(n.value));onChange();});input.value=String(index);label.append(input,el('span',check));checks.append(label);});frag.append(checks);}
 host.replaceChildren(frag);}
function hasMissing(){if(!current)return false;const s=draft(current);return !s.subject.trim()||!s.prompt.trim();}
function validate(){if(!current)return true;const s=draft(current),missing=['subject','prompt'].filter(k=>!s[k].trim());for(const key of ['subject','prompt']){const n=nodes[key];if(!n)continue;n.error.hidden=!missing.includes(key);if(missing.includes(key)){n.input.setAttribute('aria-invalid','true');n.input.setAttribute('aria-describedby',n.error.id);}else{n.input.removeAttribute('aria-invalid');n.input.removeAttribute('aria-describedby');}}if(missing.length){nodes[missing[0]]?.input.focus();return false;}return true;}
function compose(item,additional){const s=draft(item);if(!RATIOS.includes(s.ratio)||!DETAILS.includes(s.detail)||!BACKGROUNDS.includes(s.background))throw new Error('Invalid image controls.');
 if(s.subject.length>1000||s.prompt.length>10000||s.referenceNotes.length>2000||String(additional||'').length>2000)throw new Error('One of the image request fields is too long.');
 const lines=['Generate one image using the official imagegen tool. This is a prepared request, not a generated image.',
  'Selected template: '+item.name+' (ID: '+item.id+'; catalog revision: '+item.revision+')',
  'Subject: '+(s.subject.trim()||'[Subject required before sending]'),
  'Aspect ratio guidance: '+s.ratio+'. Compose for this ratio where supported and inspect returned dimensions before claiming it was met.',
  'Detail guidance: '+s.detail+'. This is prompt guidance, not an imagegen tool parameter.',
  'Background: '+s.background+'.'+(s.background==='Transparent'?' Set imagegen transparent_background=true and inspect the returned image alpha channel.':' Set imagegen transparent_background=false.'),
  'Image direction:\n'+(s.prompt.trim()||'[Image prompt required before sending]')];
 if(s.referenceNotes.trim())lines.push('Reference notes (description only; no image is uploaded by this field):\n'+s.referenceNotes.trim());
 if(item.reference==='required')lines.push('A source image is required. Verify it is actually available in this conversation before generation. If missing, ask the user to attach it and stop; do not invent a reference.');
 else if(item.reference==='optional')lines.push('If a real source image is supplied, use it. Reference notes alone are not an upload.');
 lines.push('For actual image references, inspect any local file with view_image before editing. Use referenced_image_paths if every target has a local path; otherwise use the smallest recent conversation image window that includes all targets (up to five). Never use both mechanisms. If targets cannot all be included, ask the user to attach them again.');
 const checks=s.checks.map(i=>item.checks?.[i]).filter(Boolean);if(checks.length)lines.push('Review the returned image against:\n'+checks.map(c=>'- '+c).join('\n'));
 if(String(additional||'').trim())lines.push('Additional instructions:\n'+String(additional).trim());
 lines.push('Show the generated image and report only verified properties. Sending this request alone does not mean generation succeeded.');
 return lines.join('\n\n');}
window.ImageWorkflowEditor={mount,compose,hasMissing,validate};
})();
