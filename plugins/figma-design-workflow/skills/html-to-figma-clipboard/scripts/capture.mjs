#!/usr/bin/env node
import { readFile, writeFile, mkdir, realpath, stat } from 'node:fs/promises';
import { resolve, dirname, join, basename } from 'node:path';
import { homedir } from 'node:os';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';
import { parseArgs } from 'node:util';
import { sha, isLocalURL, allowedResource, staticServer, createFontResolver } from './resources.mjs';
import { acquireLock,validatePayload,pruneCache,cacheRead,cacheWrite,copyPage } from './state.mjs';
import { writeRichClipboard } from './clipboard.mjs';

const here=dirname(fileURLToPath(import.meta.url));
const {values:v,positionals}=parseArgs({allowPositionals:true,options:{width:{type:'string',default:'1280'},height:{type:'string',default:'900'},selector:{type:'string'},layout:{type:'string',default:'auto'},offline:{type:'boolean',default:true},'allow-external':{type:'boolean'},'font-map':{type:'string'},out:{type:'string'},runtime:{type:'string'},'no-copy':{type:'boolean'},'no-cache':{type:'boolean'},strict:{type:'boolean'},timeout:{type:'string',default:'60000'},'settle-ms':{type:'string',default:'300'},'ready-selector':{type:'string'},name:{type:'string'},help:{type:'boolean'}}});
if(v.help||!positionals.length){console.log(`HTML to Figma Clipboard (local @figit/dom-to-figma 0.2.4)
node capture.mjs FILE.html|http://localhost:PORT [--width 1280 --height 900]
  --selector '#design' --layout auto|absolute --font-map fonts.json
  --out /absolute/output --offline --strict --no-copy --no-cache
  --ready-selector '[data-ready]' --settle-ms 300 --timeout 60000
  --allow-external  Permit source assets from HTTP(S); conversion stays local.
node capture.mjs copy /absolute/output  Serve a local Copy for Figma button (5 min).
Setup: node setup.mjs /absolute/mounted/runtime`);process.exit(0);}
let browser,server,release,timeout;let cancelled=false;
async function cleanup(){clearTimeout(timeout);if(browser){const b=browser;browser=null;await b.close().catch(()=>{});}if(server){const s=server;server=null;await s.close();}if(release){await release();release=null;}}
for(const name of ['SIGINT','SIGTERM'])process.once(name,()=>{cancelled=true;cleanup().finally(()=>process.exit(name==='SIGINT'?130:143));});
async function main(){
  if(positionals[0]==='copy'){
    const out=await realpath(positionals[1]||'.');const html=await readFile(join(out,'clipboard.html'),'utf8');validatePayload(html);
    let complete;const completed=new Promise(r=>complete=r);
    server=await staticServer(out,{onCopied:complete});console.log(JSON.stringify({url:server.url+'/copy.html',expiresInSeconds:300}));
    await Promise.race([completed,new Promise(r=>{timeout=setTimeout(r,300000);})]);return;
  }
  const width=+v.width,height=+v.height,limit=+v.timeout,settle=+v['settle-ms'];
  if(![width,height].every(n=>Number.isInteger(n)&&n>=64&&n<=16384)||!Number.isFinite(limit)||limit<1000||limit>300000||!Number.isFinite(settle)||settle<0||settle>30000)throw new Error('Invalid viewport, timeout, or settle interval.');
  if(!['auto','absolute'].includes(v.layout))throw new Error('Layout must be auto or absolute');
  const runtime=await realpath(v.runtime||JSON.parse(await readFile(join(homedir(),'.config/html-to-figma-clipboard/runtime.json'),'utf8')).runtime);
  await mkdir(join(runtime,'tmp'),{recursive:true});process.env.TMPDIR=join(runtime,'tmp');
  process.env.PLAYWRIGHT_BROWSERS_PATH=join(runtime,'browsers');
  const require=createRequire(join(runtime,'package.json'));
  const {chromium}=require('playwright');const esbuild=require('esbuild');
  const converterVersion=JSON.parse(await readFile(join(runtime,'node_modules/@figit/dom-to-figma/package.json'),'utf8')).version;
  if(converterVersion!=='0.2.4')throw new Error('Runtime converter differs from pinned 0.2.4; rerun setup.');
  release=await acquireLock();
  const offline=!v['allow-external'];
  let url=positionals[0],source=url,normalize=x=>x;
  if(!/^https?:/.test(url)){
    source=await realpath(url);const root=dirname(source);server=await staticServer(root);url=server.url+'/'+encodeURIComponent(basename(source));
    normalize=x=>x.replaceAll(server.url,'http://local-file');
  }else if(!isLocalURL(url))throw new Error('Input URL must be localhost, 127.0.0.1, or ::1.');
  const out=resolve(v.out||join(runtime,'outputs','latest'));await mkdir(out,{recursive:true});
  const report={source,provider:'local',converter:{name:'@figit/dom-to-figma',version:converterVersion},viewport:{width,height,deviceScaleFactor:1},settings:{selector:v.selector||'body',layout:v.layout,offline,serviceWorkers:'block',locale:'en-US',timezone:'UTC',colorScheme:'light',settleMs:settle,readySelector:v['ready-selector']||null},statuses:{conversion:'running',clipboard:'not-run',figmaPaste:'unverified',visualFidelity:'unverified',editability:'unverified'},warnings:[],failedRequests:[],blockedRequests:[],responses:[],startedAt:new Date().toISOString()};
  const pending=[];const resources=new Map();
  try{
    browser=await chromium.launch({headless:true,timeout:30000,args:['--disable-background-networking','--disable-component-update','--disable-domain-reliability','--force-webrtc-ip-handling-policy=disable_non_proxied_udp']});
    timeout=setTimeout(()=>{cancelled=true;browser?.close().catch(()=>{});},limit);
    report.browserVersion=browser.version();
    const context=await browser.newContext({viewport:{width,height},deviceScaleFactor:1,serviceWorkers:'block',locale:'en-US',timezoneId:'UTC',colorScheme:'light',reducedMotion:'reduce'});
    await context.route('**/*',async route=>{const u=route.request().url();if(!allowedResource(u,offline)){report.blockedRequests.push({url:u,reason:'offline-external-request-blocked'});await route.abort('blockedbyclient');}else await route.continue();});
    await context.routeWebSocket('**/*',ws=>{if(offline&&!isLocalURL(ws.url().replace(/^ws/,'http'))){report.blockedRequests.push({url:ws.url(),reason:'offline-websocket-blocked'});ws.close();}else ws.connectToServer();});
    const page=await context.newPage();
    page.on('console',msg=>{if(['warning','error'].includes(msg.type()))report.warnings.push({type:msg.type(),text:msg.text()});});
    page.on('pageerror',e=>report.warnings.push({type:'pageerror',text:String(e)}));
    page.on('requestfailed',r=>report.failedRequests.push({url:r.url(),error:r.failure()?.errorText}));
    page.on('response',r=>{pending.push((async()=>{try{const bytes=await r.body();if(bytes.length>32*1024*1024)throw new Error('Response exceeds 32 MiB fingerprint limit');const info={url:normalize(r.url()),status:r.status(),sha256:sha(bytes)};resources.set(info.url,info);if(r.status()>=400)report.failedRequests.push({url:r.url(),error:`HTTP ${r.status()}`});}catch(e){report.warnings.push({type:'resource-hash',url:r.url(),text:String(e)});}})());});
    const fonts=await createFontResolver(require,v['font-map']?resolve(v['font-map']):undefined);
    await page.exposeFunction('localFigmaFont',req=>fonts.load(req));
    await page.goto(url,{waitUntil:'load',timeout:limit});
    if(v['ready-selector'])await page.locator(v['ready-selector']).waitFor({state:'visible',timeout:limit});
    await page.evaluate(async()=>{document.querySelectorAll('img').forEach(i=>i.loading='eager');await document.fonts.ready;await Promise.all([...document.images].map(i=>i.decode().catch(()=>{})));await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));});
    await page.waitForTimeout(settle);
    const readiness=await page.evaluate(()=>({fonts:[...document.fonts].filter(f=>f.status!=='loaded').map(f=>({family:f.family,status:f.status})),images:[...document.images].filter(i=>!i.complete||!i.naturalWidth).map(i=>({src:i.currentSrc||i.src}))}));
    for(const kind of ['fonts','images'])for(const item of readiness[kind])report.warnings.push({type:`unresolved-${kind}`, ...item});
    // Capture selected responsive image, rather than the converter's fallback src.
    await page.evaluate(()=>document.querySelectorAll('img[srcset],picture img').forEach(i=>{const src=i.currentSrc;i.removeAttribute('srcset');i.closest('picture')?.querySelectorAll('source').forEach(s=>s.remove());if(src)i.src=src;}));
    // Upstream 0.2.4 only exports placeholders. Filled text fields need their visible value.
    report.preparations=await page.evaluate(()=>{const changed=[];for(const el of document.querySelectorAll('input,textarea')){if(el.matches('textarea,input:not([type]),input[type=text],input[type=email],input[type=search],input[type=url],input[type=tel],input[type=number]')&&el.value){el.setAttribute('placeholder',el.value);changed.push({kind:'form-visible-value',id:el.id,tag:el.tagName});}}return changed;});
    const entry=await readFile(join(here,'browser-entry.mjs'),'utf8');
    const bundle=await esbuild.build({stdin:{contents:entry,resolveDir:runtime,sourcefile:'browser-entry.mjs'},bundle:true,write:false,format:'iife',platform:'browser',target:'chrome120'});
    await page.addScriptTag({content:bundle.outputFiles[0].text});
    const settings={selector:v.selector,layout:v.layout,name:v.name||basename(source)};
    const inspected=await page.evaluate(s=>window.htmlToFigmaCapture({...s,phase:'inspect'}),settings);
    await Promise.all(pending);
    const wrapper=sha(['capture.mjs','resources.mjs','state.mjs','browser-entry.mjs'].map(f=>require('node:fs').readFileSync(join(here,f),'utf8')).join('\n'));
    const fingerprint=()=>sha(JSON.stringify({source,name:settings.name,settings:report.settings,viewport:report.viewport,browser:report.browserVersion,wrapper,lock:sha(require('node:fs').readFileSync(join(runtime,'package-lock.json'))),fingerprint:normalize(inspected.fingerprint),resources:[...resources.values()].sort((a,b)=>a.url.localeCompare(b.url))}));
    const cacheDir=join(runtime,'cache');await pruneCache(cacheDir);
    const key=fingerprint();let result=!v['no-cache']?await cacheRead(cacheDir,key):null;report.cache={hit:Boolean(result),key};
    if(!result)result=await page.evaluate(s=>window.htmlToFigmaCapture(s),settings);
    await Promise.all(pending);
    const after=await page.evaluate(s=>window.htmlToFigmaCapture({...s,phase:'inspect'}),settings);
    if(after.fingerprint!==inspected.fingerprint)report.warnings.push({type:'unstable-source',text:'DOM or computed geometry changed during conversion; cache disabled. Wait for an application ready selector.'});
    report.payload=validatePayload(result.html);report.diagnostics=result.diagnostics;report.responses=[...resources.values()];
    const nodes=result.document.nodeChanges||[];report.nodeCounts=Object.fromEntries([...new Set(nodes.map(n=>n.type))].map(t=>[t,nodes.filter(n=>n.type===t).length]));
    await page.locator(settings.selector||'body').screenshot({path:join(out,'source.png'),animations:'disabled',timeout:15000});
    const degraded=report.failedRequests.length||report.blockedRequests.length||report.warnings.length||result.diagnostics.fonts.some(f=>f.error)||result.diagnostics.assets.some(f=>f.error)||result.diagnostics.omitted.length||result.diagnostics.risks.length;
    report.statuses.conversion=degraded?'degraded':'passed';
    if(!degraded&&!v['no-cache']&&!report.cache.hit)await cacheWrite(cacheDir,fingerprint(),result);
    await writeFile(join(out,'clipboard.html'),result.html,{mode:0o600});
    await writeFile(join(out,'document.json'),JSON.stringify(result.document,null,2),{mode:0o600});
    await writeFile(join(out,'trace.json'),JSON.stringify(result.trace,null,2),{mode:0o600});
    await writeFile(join(out,'copy.html'),copyPage(result.html,report.payload.sha256),{mode:0o600});
    // Capture browser is closed before native clipboard or any UI handoff.
    await browser.close();browser=null;clearTimeout(timeout);
    if(v.strict&&degraded)throw new Error('Strict capture rejected unresolved resources or conversion warnings. Review report.json; clipboard was not written.');
    if(!v['no-copy']){try{report.clipboard=await writeRichClipboard(result.html);report.statuses.clipboard='passed';}catch(e){report.statuses.clipboard='fallback-required';report.clipboard={error:String(e),command:`node "${join(here,'capture.mjs')}" copy "${out}"`};}}
    report.completedAt=new Date().toISOString();await writeFile(join(out,'report.json'),JSON.stringify(report,null,2),{mode:0o600});
    console.log(JSON.stringify({out,statuses:report.statuses,nodeCounts:report.nodeCounts,cache:report.cache,payload:report.payload,clipboard:report.clipboard},null,2));
  }catch(e){report.statuses.conversion=cancelled?'cancelled-or-timeout':'failed';report.error=String(e);await writeFile(join(out,'report.json'),JSON.stringify(report,null,2),{mode:0o600});throw e;}
}
try{await main();}catch(e){console.error(String(e));process.exitCode=1;}finally{await cleanup();}
