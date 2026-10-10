(function(){'use strict';
const drafts=new Map(),receivedPrefills=new Set();
let current=null,host=null,onChange=()=>{},items=[],onChoose=()=>{},fieldNodes=new Map(),picker=null;
const MAX_DRAFTS=60;
const node=(tag,text,className)=>{const e=document.createElement(tag);if(text!==undefined)e.textContent=text;if(className)e.className=className;return e;};
const control=(label,action)=>{const e=node('button',label);e.type='button';e.addEventListener('click',action);return e;};
const text=value=>Array.isArray(value)?value.join('\n'):value===null||value===undefined?'':String(value);
function draft(item){if(!drafts.has(item.id)){if(drafts.size>=MAX_DRAFTS)drafts.delete(drafts.keys().next().value);const values={};for(const field of item.fields||[])if(field.default!==undefined)values[field.key]=field.default;if(values.ctx===undefined)values.ctx='';drafts.set(item.id,{values,checks:[]});}return drafts.get(item.id);}
function valueOf(field){return draft(current).values[field.key];}
function setValue(field,value){draft(current).touched=true;draft(current).values[field.key]=value;const entry=fieldNodes.get(field.key);if(entry){entry.error.hidden=true;entry.input.removeAttribute('aria-invalid');}updateSectionCounts();renderPicker();onChange();}
function hasContent(value){if(Array.isArray(value))return value.some(hasContent);if(value&&typeof value==='object')return Object.values(value).some(hasContent);return typeof value==='boolean'?value:String(value??'').trim().length>0;}
function missing(field){if(!field.required)return false;return !hasContent(valueOf(field));}
function missingCount(fields){return fields.filter(missing).length;}
function options(field){return (field.options||[]).map(o=>typeof o==='object'&&o!==null?{value:String(o.value??o.label??''),label:String(o.label??o.value??'')}:{value:String(o),label:String(o)});}
function makeField(field,index){const wrapper=node('div',undefined,'framework-field');const label=node('label',undefined,'framework-label');const id='framework-field-'+index;label.htmlFor=id;label.append(node('span',field.label||field.key));if(field.required)label.append(node('span',' · Required','framework-required'));wrapper.append(label);if(field.description)wrapper.append(node('p',field.description,'framework-description'));
 let input,kind=field.type||'text';const currentValue=valueOf(field);
 if(kind==='repeater'){
   const list=node('div',undefined,'framework-repeat-list');const grouped=field.itemType==='group'&&Array.isArray(field.fields)&&field.fields.length>0;
   const rows=grouped?(Array.isArray(currentValue)?currentValue:[]):Array.isArray(currentValue)?currentValue.map(text):text(currentValue).split('\n').filter(Boolean);
   if(!grouped&&!rows.length)rows.push('');
   const max=Number.isFinite(Number(field.max))?Number(field.max):20;const min=Math.max(0,Number(field.min)||0);
   function read(){if(grouped){setValue(field,Array.from(list.children).map(row=>{const result={};for(const entry of row.querySelectorAll('[data-subkey]'))result[entry.dataset.subkey]=entry.type==='checkbox'?entry.checked:entry.value;return result;}).filter(hasContent));}else setValue(field,Array.from(list.querySelectorAll('input')).map(e=>e.value).filter(v=>v.trim()).join('\n'));}
   function addRow(value=grouped?{}:''){
     const row=node(grouped?'fieldset':'div',undefined,grouped?'framework-group-row':'framework-repeat-row');
     if(grouped){row.append(node('legend',(field.itemLabel||'Item')+' '+(list.children.length+1)));for(const sub of field.fields){const label=node('label',undefined,'framework-subfield');label.append(node('span',sub.label||sub.key));let entry;if(sub.type==='textarea'){entry=node('textarea');entry.rows=2;}else if(sub.type==='select'){entry=node('select');entry.append(new Option('Select an option',''));for(const option of options(sub))entry.append(new Option(option.label,option.value));}else{entry=node('input');entry.type=sub.type==='checkbox'?'checkbox':'text';}entry.dataset.subkey=sub.key;entry.setAttribute('aria-label',(field.itemLabel||'Item')+' '+(list.children.length+1)+' · '+(sub.label||sub.key));if(entry.type==='checkbox')entry.checked=value?.[sub.key]===true;else entry.value=text(value?.[sub.key]);if(sub.placeholder)entry.placeholder=sub.placeholder;entry.addEventListener(entry.type==='checkbox'||sub.type==='select'?'change':'input',read);label.append(entry);row.append(label);}}
     else {const entry=node('input');entry.type='text';entry.value=value;entry.placeholder=field.placeholder||'';entry.setAttribute('aria-label',(field.itemLabel||field.label||field.key)+' '+(list.children.length+1));entry.addEventListener('input',read);row.append(entry);}
     const remove=control('Remove',()=>{row.remove();read();updateButtons();});remove.setAttribute('aria-label','Remove '+(field.itemLabel||'item'));row.append(remove);list.append(row);updateButtons();
   }
   const add=control('Add '+(field.itemLabel||'item'),()=>{addRow();list.lastElementChild.querySelector('input,textarea,select')?.focus();read();});function updateButtons(){add.disabled=list.children.length>=max;for(const row of list.children)row.querySelector('button').disabled=list.children.length<=min;}
   input=list;input.id=id;rows.slice(0,max).forEach(addRow);while(list.children.length<min)addRow();wrapper.append(list,add);
 }else if(kind==='multiselect'){
   const list=node('div',undefined,'framework-multiselect');const selected=new Set(Array.isArray(currentValue)?currentValue.map(String):text(currentValue).split(/[,\n]/).map(s=>s.trim()).filter(Boolean));for(const o of options(field)){const option=node('label',undefined,'framework-option');const box=node('input');box.type='checkbox';box.value=o.value;box.checked=selected.has(o.value);box.addEventListener('change',()=>setValue(field,Array.from(list.querySelectorAll('input:checked')).map(i=>i.value)));option.append(box,node('span',o.label));list.append(option);}input=list;input.id=id;wrapper.append(list);
 }else if(kind==='checkbox'){
   input=node('input');input.type='checkbox';input.id=id;input.checked=currentValue===true;input.addEventListener('change',()=>setValue(field,input.checked));label.prepend(input);label.htmlFor=id;
 }else if(kind==='select'){
   input=node('select');input.id=id;input.append(new Option('Select an option',''));for(const o of options(field))input.append(new Option(o.label,o.value));input.value=Array.isArray(currentValue)?String(currentValue[0]??''):text(currentValue);input.addEventListener('change',()=>setValue(field,input.value));wrapper.append(input);
 }else{
   input=node(kind==='textarea'?'textarea':'input');input.id=id;if(kind!=='textarea')input.type='text';else input.rows=3;input.value=text(currentValue);input.placeholder=field.placeholder||'';input.addEventListener('input',()=>setValue(field,input.value));wrapper.append(input);
   if(kind==='typeahead'&&options(field).length){const list=node('datalist');list.id=id+'-options';for(const o of options(field)){const option=node('option');option.value=o.value;list.append(option);}input.setAttribute('list',list.id);wrapper.append(list);}
 }
 const error=node('p','Enter '+(field.label||field.key).replace(/\s*\(optional\).*$/i,'')+' before sending.','framework-error');error.id=id+'-error';error.hidden=true;wrapper.append(error);fieldNodes.set(field.key,{wrapper,input,error});return wrapper;}
function updateSectionCounts(){host?.querySelectorAll('[data-framework-section]').forEach(section=>{const start=Number(section.dataset.start),end=Number(section.dataset.end),count=missingCount((current?.fields||[]).slice(start,end));const summary=section.querySelector('summary');summary.textContent=(section.dataset.label||'More fields')+(count?' · '+count+' required to complete':'');});}
function words(value){return Array.from(new Set(text(value).toLowerCase().match(/[a-z0-9]{3,}/g)||[])).filter(t=>!['the','and','for','with','this','that','your','from','into','about','have','will','what','want','need','make'].includes(t)).slice(0,20);}
function tagTerms(value){return Array.from(new Set(text(value).toLowerCase().split(/[,\s]+/).map(s=>s.trim()).filter(Boolean))).slice(0,20);}
function renderPicker(){if(!picker||!current)return;const v=draft(current).values;const terms=words([v.goal,v.stage,v.deliverable,v.constraints].join(' ')),preferred=tagTerms(v.include),excluded=tagTerms(v.exclude);picker.replaceChildren();if(!terms.length&&!preferred.length){picker.append(node('p','Describe your goal to see source metadata matches.','framework-description'));return;}
 const ranked=[];for(const item of items){if(item.id===current.id||item.assemblyStatus==='unavailable')continue;const tagText=(item.tags||[]).join(' ').toLowerCase();if(excluded.some(token=>tagText.includes(token)))continue;const groups=[['name',[item.name]],['use case',item.useCases],['tag',item.tags],['category',item.categories],['definition',[item.definition]]];const matches=[];let score=0;for(const [label,entries] of groups){for(const entry of entries||[]){const matched=terms.filter(t=>String(entry).toLowerCase().includes(t));if(matched.length){score+=matched.length*(label==='use case'?3:label==='name'?2:1);if(matches.length<2)matches.push(label+': '+String(entry).slice(0,110));}}}for(const token of preferred){const tag=(item.tags||[]).find(t=>String(t).toLowerCase().includes(token));if(tag){score+=4;if(matches.length<2)matches.push('preferred tag: '+tag);}}if(score)ranked.push({item,score,matches});}
 ranked.sort((a,b)=>b.score-a.score||a.item.name.localeCompare(b.item.name));if(!ranked.length){picker.append(node('p','No source metadata matches this goal yet. Try a different description or browse the library.','framework-description'));return;}
 picker.append(node('p','Matches use case, tag, category, name, or definition text from the library. These are discovery suggestions, not effectiveness claims.','framework-description'));
 for(const result of ranked.slice(0,3)){const card=node('article',undefined,'framework-match');card.append(node('h4',result.item.name),node('p',result.matches.join(' · ')));card.append(control('Use '+result.item.name,()=>onChoose(result.item)));picker.append(card);}}
function mount({item,host:target,items:all,onChange:changed,onChoose:choose}){current=item;host=target;items=all||[];onChange=changed||(()=>{});onChoose=choose||(()=>{});fieldNodes=new Map();picker=null;const state=draft(item),fragment=document.createDocumentFragment();
 fragment.append(collaborationControls(item));
 if(item.help)fragment.append(node('p',item.help,'framework-help'));
 if(item.notice)fragment.append(node('p',text(item.notice),'framework-assembly-note'));
 if(item.assemblyNote)fragment.append(node('p','Assembly note: '+item.assemblyNote,'framework-assembly-note'));
 const context={key:'ctx',label:'Context',type:'textarea',placeholder:'Add background that should inform this framework.',description:'Optional background for this prompt. Additional instructions remain separate.'};
 const fields=item.fields||[];const split=fields.length>8?Math.min(5,fields.length):fields.length;
 for(let i=0;i<split;i++)fragment.append(makeField(fields[i],i));
 if(split<fields.length){const more=node('details',undefined,'framework-more');more.dataset.frameworkSection='';more.dataset.start=String(split);more.dataset.end=String(fields.length);more.dataset.label='More framework fields';more.append(node('summary','More framework fields'));for(let i=split;i<fields.length;i++)more.append(makeField(fields[i],i));fragment.append(more);}
 const contextMore=node('details',undefined,'framework-more');contextMore.append(node('summary','Context (optional)'),makeField(context,'context'));fragment.append(contextMore);
 const availableChecks=(item.boosters||[]).map((value,index)=>({value,index})).filter(entry=>!(item.id==='pattern-picker'&&entry.value.startsWith('Library tools:')));
 if(availableChecks.length){const checks=node('details',undefined,'framework-more');checks.append(node('summary','Source checks (optional)'));const note=node('p','Add any of these authored checks after the framework prompt.','framework-description');checks.append(note);for(const {value,index} of availableChecks){const label=node('label',undefined,'framework-option');const input=node('input');input.type='checkbox';input.checked=state.checks.includes(index);input.addEventListener('change',()=>{state.touched=true;state.checks=Array.from(checks.querySelectorAll('input:checked')).map(e=>Number(e.value));onChange();});input.value=String(index);label.append(input,node('span',value));checks.append(label);}fragment.append(checks);}
 if(item.id==='pattern-picker'||item.slug==='pattern-picker'){const section=node('section',undefined,'framework-picker');section.append(node('h3','Matching frameworks'));picker=node('div',undefined,'framework-matches');section.append(picker);fragment.append(section);}
 host.replaceChildren(fragment);host.oninput=()=>{state.touched=true;};host.onchange=()=>{state.touched=true;};const brief=document.getElementById('brief');if(brief)brief.oninput=()=>{draft(current).touched=true;};window.FrameworkAdditions?.mount({itemId:item.id,host,onChange});updateSectionCounts();renderPicker();}
function compose(item,additional){const state=draft(item),assembly=window.PromptAssembly;if(!assembly||typeof assembly.assemble!=='function')throw new Error('The source prompt assembly is unavailable.');const assembled=assembly.assemble(item.id,{...state.values});if(typeof assembled!=='string'||!assembled.trim())throw new Error('The source prompt could not be assembled.');const additions=[];for(const index of state.checks){const check=item.boosters?.[index];if(check)additions.push('- '+check);}if(String(additional||'').trim())additions.push(String(additional).trim());const reusable=window.FrameworkAdditions?.compose(item.id)||'';return [assembled,reusable,additions.length?'Additional instructions:\n'+additions.join('\n'):''].filter(Boolean).join('\n\n');}
function hasMissing(){return !!current&&missingCount(current.fields||[])>0;}
function validate(){if(!current)return true;let first=null;for(const field of current.fields||[]){const entry=fieldNodes.get(field.key);if(!entry)continue;const empty=missing(field);entry.error.hidden=!empty;if(empty){entry.input.setAttribute('aria-invalid','true');entry.input.setAttribute('aria-describedby',entry.error.id);if(!first)first=entry;}else{entry.input.removeAttribute('aria-invalid');entry.input.removeAttribute('aria-describedby');}}
 if(first){const section=first.wrapper.closest('details');if(section)section.open=true;const focus=first.input.matches?.('input,select,textarea')?first.input:first.input.querySelector('input,select,textarea');focus?.focus();return false;}return true;}

function applyToolResult(data){
 const p=data?.prefill;
 if(!p||typeof p.id!=='string'||receivedPrefills.has(p.id))return null;
 const item=window.LibraryAdapter?.items.find(i=>i.id===p.frameworkId);
 if(!item||!p.values||typeof p.values!=='object')return null;
 receivedPrefills.add(p.id);
 const state=draft(item);if(state.touched){const status=document.getElementById('framework-collaboration-status');if(status)status.textContent='Your edited draft was kept. Refine it here before preparing another version.';return null;}
 const keys=new Set(['ctx',...(item.fields||[]).map(f=>f.key)]);
 for(const [key,value] of Object.entries(p.values))if(keys.has(key)&&!['__proto__','constructor','prototype'].includes(key))state.values[key]=value;
 state.rationale=typeof p.rationale==='string'?p.rationale:'';
 window.FrameworkAdditions?.seed(item.id,p);
 return {id:item.id,brief:typeof p.additionalInstructions==='string'?p.additionalInstructions:''};
}
function collaborationControls(item){
 const section=node('section',undefined,'framework-collaboration');const state=draft(item);
 if(state.rationale)section.append(node('p',state.rationale,'framework-rationale'));
 const status=node('p','Share these fields with the AI to refine this draft together.','framework-description');status.id='framework-collaboration-status';status.setAttribute('role','status');
 const button=control('Ask AI to refine',async()=>{
  button.disabled=true;button.textContent='Sharing draft…';
  try{
   const brief=document.getElementById('brief')?.value||'';
   const snapshot={frameworkId:item.id,frameworkName:item.name,fields:state.values,sourceChecks:state.checks.map(i=>item.boosters?.[i]).filter(Boolean),additionalInstructions:brief};
   const message='Refinement request — do not execute.\n\nWork through this framework with me in the existing Framework Builder widget. Read its current fields before changing anything so my edits are preserved. Help refine the draft using supplied facts, explain the framework choice, and ask only for material missing information. Do not execute the prepared prompt or create a replacement widget unless asked.\n\nCurrent draft:\n'+JSON.stringify(snapshot,null,2)+'\n\nPrompt preview:\n'+compose(item,brief);
   await window.LibraryBridge.ready();
   if(!window.LibraryBridge.canSend())throw new Error('Copy the prompt preview into chat to refine it together.');
   await window.LibraryBridge.sendMessage(message);
   button.textContent='Ask AI to refine';status.textContent='Draft shared. Continue the conversation here; your fields stay available.';
  }catch(error){button.textContent='Try sharing again';status.textContent=error.message||'Could not share this draft. Try again.';}
  finally{button.disabled=false;}
 });button.id='framework-collaborate';section.append(button,status);return section;
}
window.FrameworkBuilderEditor={mount,compose,hasMissing,validate,applyToolResult};
})();
