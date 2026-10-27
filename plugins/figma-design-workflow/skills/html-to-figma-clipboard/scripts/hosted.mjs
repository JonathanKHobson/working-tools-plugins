#!/usr/bin/env node
// Separate opt-in boundary. This module is never imported by local capture.
import {parseArgs} from 'node:util';
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {join,resolve} from 'node:path';
import {sha} from './resources.mjs';
import {validatePayload,copyPage,pruneCache,cacheRead,cacheWrite} from './state.mjs';
import {writeRichClipboard} from './clipboard.mjs';

const {values:v}=parseArgs({options:{provider:{type:'string'},'confirm-one-credit':{type:'boolean'},input:{type:'string'},out:{type:'string'},width:{type:'string',default:'1280'},height:{type:'string',default:'900'},layout:{type:'string',default:'auto'},'no-copy':{type:'boolean'}}});
if(v.provider!=='hosted'||!v['confirm-one-credit']||!v.input||!v.out)throw new Error('Hosted mode requires --provider hosted --confirm-one-credit --input FILE --out DIR. A new request uses 1 credit and sends HTML to divRIOTS.');
const key=process.env.CODE_TO_DESIGN_API_KEY;if(!key)throw new Error('Set CODE_TO_DESIGN_API_KEY in the local helper environment.');
const input=await readFile(resolve(v.input),'utf8');
if(!/<html\b/i.test(input)||/(?:src|href)\s*=\s*["'](?!data:|#)[^"']+["']|url\(\s*["']?(?!data:|#)[^)]*\)|@import|https?:\/\//i.test(input))throw new Error('Hosted adapter accepts self-contained HTML only: inline/data assets, no relative or remote URLs.');
const width=+v.width,height=+v.height;if(![width,height].every(n=>Number.isInteger(n)&&n>=64&&n<=16384)||!['auto','absolute'].includes(v.layout))throw new Error('Invalid viewport or layout.');
const body={html:input,clip:true,width,height,noAutoLayout:v.layout==='absolute'};
const out=resolve(v.out);await mkdir(out,{recursive:true});const cacheDir=join(out,'hosted-cache');await pruneCache(cacheDir);
const id=sha(JSON.stringify({provider:'divriots-code-to-design-html-v1',body}));let result=await cacheRead(cacheDir,id);
console.log(JSON.stringify({provider:'divriots-code.to.design',expectedCredits:result?0:1,cacheHit:Boolean(result)}));
if(!result){const response=await fetch('https://api.to.design/html',{method:'POST',headers:{Authorization:`Bearer ${key}`,'Content-Type':'application/json'},body:JSON.stringify(body),redirect:'error',signal:AbortSignal.timeout(120000)});if(!response.ok)throw new Error(`Hosted conversion HTTP ${response.status}; no automatic retry.`);const html=await response.text();validatePayload(html);result={html};await cacheWrite(cacheDir,id,result);}
const payload=validatePayload(result.html);await writeFile(join(out,'clipboard.html'),result.html,{mode:0o600});await writeFile(join(out,'copy.html'),copyPage(result.html,payload.sha256),{mode:0o600});
const report={provider:'divriots-code.to.design',payload,figmaPaste:'unverified',visualFidelity:'unverified',editability:'unverified'};
if(!v['no-copy']){try{report.clipboard=await writeRichClipboard(result.html);}catch(e){report.clipboard={error:String(e),fallback:'Use capture.mjs copy OUTPUT'};}}
await writeFile(join(out,'report.json'),JSON.stringify(report,null,2),{mode:0o600});console.log(JSON.stringify({out,payload}));
