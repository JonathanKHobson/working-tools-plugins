import { mkdir, open, readFile, rm, readdir, stat, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import { homedir } from 'node:os';
import { sha } from './resources.mjs';

export async function acquireLock() {
  const dir=join(homedir(),'.cache/html-to-figma-clipboard');await mkdir(dir,{recursive:true});
  const path=join(dir,'capture.lock');const token=`${process.pid}-${Date.now()}`;
  for(let attempt=0;attempt<2;attempt++){
    try{const f=await open(path,'wx',0o600);await f.writeFile(JSON.stringify({pid:process.pid,token}));await f.close();return async()=>{try{if(JSON.parse(await readFile(path,'utf8')).token===token)await rm(path);}catch{}};}
    catch(e){if(e.code!=='EEXIST')throw e;let lock;try{lock=JSON.parse(await readFile(path,'utf8'));}catch{throw new Error('Capture lock is incomplete. Check for an active capture before removing it.');}
      try{process.kill(lock.pid,0);}catch(err){if(err.code==='ESRCH'){await rm(path);continue;}throw err;}
      throw new Error(`Another capture is running (PID ${lock.pid}); only one capture browser is allowed.`);
    }
  }throw new Error('Could not acquire capture lock');
}
export function validatePayload(html) {
  const meta=[...html.matchAll(/<!--\(figmeta\)([A-Za-z0-9+/=]+)\(\/figmeta\)-->/g)];
  const data=[...html.matchAll(/<!--\(figma\)([A-Za-z0-9+/=]+)\(\/figma\)-->/g)];
  if(meta.length!==1||data.length!==1||!html.includes('data-buffer=')||!html.includes('data-metadata='))throw new Error('Invalid rich Figma HTML envelope');
  const metadata=JSON.parse(Buffer.from(meta[0][1],'base64').toString('utf8'));
  const bytes=Buffer.from(data[0][1],'base64');
  if(metadata.dataType!=='scene'||bytes.subarray(0,8).toString()!=='fig-kiwi')throw new Error('Invalid Figma scene metadata or fig-kiwi magic');
  return {valid:true,htmlBytes:Buffer.byteLength(html),binaryBytes:bytes.length,sha256:sha(bytes),metadata};
}
export async function pruneCache(dir,{maxBytes=256*1024*1024,maxEntries=10,maxAge=7*86400000}={}) {
  await mkdir(dir,{recursive:true});const files=[];
  for(const n of await readdir(dir)){if(!/^[a-f0-9]{64}\.json$/.test(n))continue;const p=join(dir,n),s=await stat(p);files.push({p,size:s.size,time:s.mtimeMs});}
  files.sort((a,b)=>b.time-a.time);let bytes=0;
  for(let i=0;i<files.length;i++){const f=files[i];bytes+=f.size;if(i>=maxEntries||bytes>maxBytes||Date.now()-f.time>maxAge)await rm(f.p,{force:true});}
}
export async function cacheRead(dir,key){try{const data=JSON.parse(await readFile(join(dir,key+'.json'),'utf8'));validatePayload(data.html);return data;}catch{return null;}}
export async function cacheWrite(dir,key,data){const bytes=JSON.stringify(data);if(Buffer.byteLength(bytes)>64*1024*1024)return;await writeFile(join(dir,key+'.json'),bytes,{mode:0o600});await pruneCache(dir);}

export function copyPage(html,hash) {
  const safe=JSON.stringify(html).replace(/</g,'\\u003c');
  return `<!doctype html><html lang="en"><meta charset="utf-8"><title>Copy for Figma</title><style>body{font:17px system-ui;max-width:680px;margin:60px auto;padding:24px;color:#18242a;background:#fafafa}button{font:inherit;padding:14px 22px;cursor:pointer}code{overflow-wrap:anywhere}p{line-height:1.5}</style><h1>HTML to Figma Clipboard</h1><p>The local conversion is ready. Copy, switch to Figma, and press Cmd+V.</p><button id="copy">Copy for Figma</button><p id="status" role="status">Paste acceptance and editability are unverified.</p><p>Payload SHA-256: <code>${hash}</code></p><script>const html=${safe};document.querySelector('#copy').onclick=async()=>{const status=document.querySelector('#status');try{try{await navigator.clipboard.write([new ClipboardItem({'text/html':new Blob([html],{type:'text/html'})})]);}catch(first){let wrote=false;const handler=e=>{e.preventDefault();e.clipboardData.setData('text/html',html);e.clipboardData.setData('text/plain','HTML to Figma capture');wrote=true;};document.addEventListener('copy',handler);try{if(!document.execCommand('copy')||!wrote)throw first;}finally{document.removeEventListener('copy',handler);}}status.textContent='Rich clipboard write completed. Switch to Figma and press Cmd+V. Paste acceptance remains unverified.';fetch('/__copied',{method:'POST'}).catch(()=>{});}catch(e){status.textContent='Copy failed: '+e.message;}};</script></html>`;
}
