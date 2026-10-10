// Protocol and state checks against a generated widget. This is a simulated host,
// not native ChatGPT delivery evidence. No browser automation is used here.
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {mkdtempSync,readFileSync,rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {execFileSync} from 'node:child_process';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const folder=mkdtempSync(path.join(tmpdir(),'starter-bridge-'));
try {
 execFileSync(process.execPath,[path.join(root,'skills/chatgpt-apps/scripts/scaffold_node_ext_apps.mjs'),folder]);
 const html=readFileSync(path.join(folder,'public/widget.html'),'utf8');
 const script=html.match(/<script type="module">([\s\S]*?)<\/script>/)[1];
 const flush=async()=>{for(let i=0;i<6;i++)await Promise.resolve();};
 function fixture({standalone=false,capabilities={serverTools:{},message:{text:{}}},hang=false}={}) {
  const elements=new Map(),sent=[],timers=new Map();let receive;
  const element=(id)=>{if(!elements.has(id))elements.set(id,{textContent:'',disabled:id.includes('button'),addEventListener(t,fn){this[t]=fn;}});return elements.get(id);};
  const parent={postMessage(m){sent.push(m);if(m.method==='ui/initialize'&&!hang)queueMicrotask(()=>receive({source:parent,data:{jsonrpc:'2.0',id:m.id,result:{hostCapabilities:capabilities}}}));}};
  const win={parent,addEventListener(t,fn){receive=fn;}};if(standalone)win.parent=win;
  const context={window:win,document:{querySelector:element},setTimeout(fn){let id=timers.size+1;timers.set(id,fn);return id;},clearTimeout(id){timers.delete(id);},console,Map,Error};
  vm.runInNewContext(script,context);
  return {element,sent,timers,reply(result,error){let request=sent.filter(x=>x.id).at(-1);receive({source:parent,data:{jsonrpc:'2.0',id:request.id,...(error?{error}:{result})}});}};
 }
 let f=fixture({standalone:true});await flush();assert.match(f.element('#status').textContent,/Standalone preview/);assert.equal(f.sent.length,0);assert.equal(f.element('#tool-button').disabled,true);
 f=fixture({capabilities:{serverTools:{}}});await flush();assert.equal(f.element('#follow-up-button').disabled,true);assert.match(f.element('#status').textContent,/copy-ready/);
 f=fixture({hang:true});await flush();for(const fn of [...f.timers.values()])fn();await flush();assert.match(f.element('#status').textContent,/did not respond/);assert.equal(f.element('#tool-button').disabled,true);
 f=fixture();await flush();let action=f.element('#tool-button').click();assert.equal(f.element('#tool-button').disabled,true);await f.element('#tool-button').click();assert.equal(f.sent.filter(x=>x.method==='tools/call').length,1);f.reply({structuredContent:{headline:'Fictional result',message:'Read-only result'}});await action;assert.equal(f.element('#headline').textContent,'Fictional result');assert.equal(f.element('#tool-button').disabled,false);
 action=f.element('#tool-button').click();f.reply({isError:true});await action;assert.equal(f.element('#headline').textContent,'Fictional result');assert.match(f.element('#status').textContent,/previous result/);
 action=f.element('#tool-button').click();f.reply({});await action;assert.match(f.element('#status').textContent,/no display data/);
 action=f.element('#follow-up-button').click();assert.equal(typeof f.sent.at(-1).id,'number');assert.equal(f.sent.at(-1).method,'ui/message');f.reply({});await action;assert.match(f.element('#status').textContent,/acknowledged/);assert.match(f.element('#status').textContent,/Check the chat/);
 action=f.element('#follow-up-button').click();f.reply({isError:true});await action;assert.match(f.element('#status').textContent,/rejected/);
 action=f.element('#follow-up-button').click();for(const fn of [...f.timers.values()])fn();await action;assert.match(f.element('#status').textContent,/check the chat before retrying/i);
 console.log('PASS: standalone, unsupported capability, initialization timeout, duplicate click, tool success/error/empty, message request/ack/error/timeout. Native host untested.');
} finally {rmSync(folder,{recursive:true,force:true});}
