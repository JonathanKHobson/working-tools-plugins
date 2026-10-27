import{createServer}from'node:http';import{readFile,mkdir,lstat,realpath,writeFile,access}from'node:fs/promises';import{dirname,join,resolve,isAbsolute,sep}from'node:path';import{fileURLToPath,pathToFileURL}from'node:url';import{createHash}from'node:crypto';import{spawn,execFileSync}from'node:child_process';import{once}from'node:events';import assert from'node:assert/strict';
import{stateAt}from'./scene.mjs';
const own=dirname(fileURLToPath(import.meta.url)),sha=x=>createHash('sha256').update(x).digest('hex');
const paletteKeys=['ink','teal','coral','yellow','aqua','white','muted'];
const labelKeys=['question','responsePrompt','response','source','sourceMeta','try','compare'];
const requiredAssets=['fredoka','dmRegular','dmBold','shantell','logo','explorer','questioner','maker','underline','coralUnderline','flares'];
const text=(value,name)=>{if(typeof value!=='string'||!value.trim())throw Error('missing text: '+name)};
export function validateProjectShape(project){
 if(!project||typeof project!=='object'||Array.isArray(project))throw Error('project must be an object');
 assert.equal(project.schema,'educational-canvas/1');assert.equal(project.fps,24);assert.equal(project.durationSeconds,12);assert.deepEqual(project.formats,{landscape:[1280,720],portrait:[720,1280]});
 for(const key of ['titleFirst','titleSecond','takeaway'])text(project[key],key);
 if(!Array.isArray(project.takeawayLines)||project.takeawayLines.length!==2)throw Error('two takeaway lines required');project.takeawayLines.forEach((line,i)=>text(line,`takeawayLines[${i}]`));
 if(!Array.isArray(project.steps)||project.steps.length!==3)throw Error('three steps required');project.steps.forEach((step,i)=>{if(!step||typeof step!=='object'||Array.isArray(step))throw Error(`steps[${i}] must be an object`);for(const key of ['action','why','example'])text(step[key],`steps[${i}].${key}`);if(step.note!==undefined)text(step.note,`steps[${i}].note`);if(!['explorer','questioner','maker'].includes(step.character))throw Error(`steps[${i}].character`)});
 if(!project.palette||typeof project.palette!=='object'||Array.isArray(project.palette))throw Error('palette required');for(const key of paletteKeys)if(typeof project.palette[key]!=='string'||!/^#[a-fA-F0-9]{6}$/.test(project.palette[key]))throw Error('palette.'+key);
 if(!project.diagramLabels||typeof project.diagramLabels!=='object'||Array.isArray(project.diagramLabels))throw Error('diagram labels required');for(const key of labelKeys)text(project.diagramLabels[key],'diagramLabels.'+key);
 if(!project.assets||typeof project.assets!=='object'||Array.isArray(project.assets))throw Error('assets required');for(const key of requiredAssets)if(!Object.hasOwn(project.assets,key))throw Error('missing asset: '+key);
}
export function browserProject(project){return{fps:project.fps,durationSeconds:project.durationSeconds,formats:project.formats,titleFirst:project.titleFirst,titleSecond:project.titleSecond,takeawayLines:project.takeawayLines,steps:project.steps.map(({action,why,example,note,character})=>({action,why,example,...(note===undefined?{}:{note}),character})),palette:Object.fromEntries(paletteKeys.map(key=>[key,project.palette[key]])),diagramLabels:Object.fromEntries(labelKeys.map(key=>[key,project.diagramLabels[key]])),assets:Object.fromEntries(Object.entries(project.assets).map(([key,entry])=>[key,{path:entry.path}]))}}
export async function validate(project,projectPath){
 validateProjectShape(project);
 const parent=await realpath(dirname(projectPath)),assetFiles={};for(const[key,entry]of Object.entries(project.assets)){
  if(!/^[a-zA-Z][a-zA-Z0-9]*$/.test(key))throw Error('bad asset key');if(!entry||typeof entry!=='object'||Array.isArray(entry))throw Error('bad asset: '+key);const rel=entry.path;
  if(typeof rel!=='string'||isAbsolute(rel)||rel.split(/[\\/]/).some(x=>!x||x==='.'||x==='..')||rel.includes('\\'))throw Error('asset path denied: '+rel);
  const absolute=resolve(parent,rel);if(!absolute.startsWith(parent+sep))throw Error('asset escapes project');
  let current=parent;for(const part of rel.split('/')){current=join(current,part);if((await lstat(current)).isSymbolicLink())throw Error('symlink denied: '+rel)}
  const actual=await realpath(absolute);if(!actual.startsWith(parent+sep))throw Error('resolved asset escapes project');const bytes=await readFile(actual);
  if(!/^[a-f0-9]{64}$/.test(entry.sha256)||sha(bytes)!==entry.sha256)throw Error('asset hash mismatch: '+key);
  if(!/\.(png|ttf|woff2)$/.test(rel))throw Error('asset type denied');assetFiles[key]={bytes,mime:rel.endsWith('.png')?'image/png':rel.endsWith('.ttf')?'font/ttf':'font/woff2'};
 }
 for(const k of requiredAssets)if(!assetFiles[k])throw Error('missing asset: '+k);
 return assetFiles;
}
export function writeFrameToEncoder(encoder,bytes){
 if(encoder.exitCode!==null||encoder.stdin.destroyed)return Promise.reject(Error('ffmpeg closed before frame write'));
 try{if(encoder.stdin.write(bytes))return Promise.resolve()}catch(error){return Promise.reject(error)}
 return new Promise((resolveWrite,rejectWrite)=>{
  const clear=()=>{encoder.stdin.off('drain',drained);encoder.stdin.off('close',closed);encoder.stdin.off('error',failed);encoder.off('close',closed);encoder.off('error',failed)};
  const drained=()=>{clear();resolveWrite()},closed=()=>{clear();rejectWrite(Error('ffmpeg closed during frame write'))},failed=error=>{clear();rejectWrite(error)};
  encoder.stdin.once('drain',drained);encoder.stdin.once('close',closed);encoder.stdin.once('error',failed);encoder.once('close',closed);encoder.once('error',failed);
  if(encoder.exitCode!==null||encoder.stdin.destroyed)closed();
 });
}
const childResult=child=>new Promise(resolveResult=>{let error;child.once('error',e=>{error=e});child.once('close',(code,signal)=>resolveResult({code,signal,error}))});
export async function render(projectPath,out,env=process.env){
if(!isAbsolute(projectPath)||!isAbsolute(out))throw Error('Usage: render.mjs ABSOLUTE_PROJECT_JSON NEW_ABSOLUTE_OUTPUT_DIR');
const output=resolve(out),projectBytes=await readFile(projectPath),project=JSON.parse(projectBytes.toString('utf8')),assets=await validate(project,projectPath);
try{await access(output);throw Error('output already exists')}catch(e){if(e.code!=='ENOENT')throw e}
const paths={PLAYWRIGHT_MODULE:env.PLAYWRIGHT_MODULE,FFMPEG:env.FFMPEG,FFPROBE:env.FFPROBE};for(const[k,v]of Object.entries(paths))if(!v||!isAbsolute(v))throw Error(k+' requires absolute local path');
const{chromium}=await import(pathToFileURL(paths.PLAYWRIGHT_MODULE).href);
// Catch direct-seek and format boundary errors before encoding.
for(const f of[0,19,20,79,80,139,140,199,200,287,288])assert(stateAt(f,project));
await mkdir(output,{recursive:false});const routes={'/':'preview.html','/preview.html':'preview.html','/scene.mjs':'scene.mjs'},payload=browserProject(project);
const server=createServer(async(req,res)=>{try{const pathname=new URL(req.url,'http://localhost').pathname;if(pathname==='/project.json'){res.setHeader('Content-Type','application/json');res.end(JSON.stringify(payload));return}if(pathname.startsWith('/asset/')){const key=pathname.slice(7),a=assets[key];if(!a){res.writeHead(404);res.end();return}res.setHeader('Content-Type',a.mime);res.end(a.bytes);return}const file=routes[pathname];if(!file){res.writeHead(404);res.end();return}res.setHeader('Content-Type',file.endsWith('.html')?'text/html':'text/javascript');res.end(await readFile(join(own,file)))}catch{res.writeHead(500);res.end()}});
let browser,encoder,encoderDone,failure,result;
try{
 await new Promise((resolveListen,rejectListen)=>{server.once('error',rejectListen);server.listen(0,'127.0.0.1',()=>{server.off('error',rejectListen);resolveListen()})});const base=`http://127.0.0.1:${server.address().port}`;
 browser=await chromium.launch({headless:true});const page=await browser.newPage({viewport:{width:1340,height:1400},deviceScaleFactor:1});await page.route('**/*',route=>route.request().url().startsWith(base+'/')?route.continue():route.abort());await page.goto(base+'/');await page.evaluate(()=>window.ready);
 const png=async(f,format,dirty=false)=>Buffer.from(await page.evaluate(({f,format,dirty})=>{const c=document.querySelector('canvas'),ctx=c.getContext('2d');if(dirty){ctx.beginPath();ctx.rect(0,0,1,1);ctx.clip();ctx.translate(20,30);ctx.globalAlpha=.1;ctx.shadowBlur=20}window.renderFrame(f,format);return c.toDataURL('image/png').split(',')[1]},{f,format,dirty}),'base64');
 const checks={};for(const format of Object.keys(project.formats)){
  const hashes={};for(const f of[287,0,60,120,180,240,287,0,120]){const h=sha(await png(f,format));if(hashes[f])assert.equal(h,hashes[f]);hashes[f]=h}for(const f of[0,120,287])assert.equal(sha(await png(f,format,true)),hashes[f]);
  await page.emulateMedia({reducedMotion:'reduce'});assert.equal(sha(await png(120,format)),hashes[120]);await page.emulateMedia({reducedMotion:'no-preference'});checks[format]=hashes;
  const path=join(output,format+'.mp4');encoder=spawn(paths.FFMPEG,['-hide_banner','-loglevel','error','-n','-f','image2pipe','-framerate','24','-i','pipe:0','-an','-vf',`scale=${project.formats[format].join(':')}:flags=lanczos`,'-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-movflags','+faststart',path],{stdio:['pipe','ignore','pipe']});encoderDone=childResult(encoder);let err='';encoder.stderr.on('data',d=>err+=d);encoder.stdin.on('error',()=>{});
  const keyframes=new Set([0,20,58,80,118,140,178,200,225,287]);for(let f=0;f<288;f++){const b=await png(f,format);if(keyframes.has(f))await writeFile(join(output,`${format}-${String(f).padStart(3,'0')}.png`),b);await writeFrameToEncoder(encoder,b)}
  encoder.stdin.end();const exit=await encoderDone;if(exit.error||exit.code!==0)throw Error('ffmpeg: '+(err||exit.error?.message||`exit ${exit.code??exit.signal}`));encoder=null;encoderDone=null;
  const probe=JSON.parse(execFileSync(paths.FFPROBE,['-v','error','-show_streams','-show_format','-of','json',path],{encoding:'utf8'}));const stream=probe.streams.find(s=>s.codec_type==='video');assert.equal(Number(stream.nb_frames),288);assert.equal(Number(probe.format.duration),12);assert.equal(stream.width,project.formats[format][0]);assert.equal(stream.height,project.formats[format][1]);execFileSync(paths.FFMPEG,['-v','error','-i',path,'-f','null','-']);
  // Sheet uses extracted stills from the encoded file for output-specific review.
  execFileSync(paths.FFMPEG,['-v','error','-i',path,'-vf',`fps=1/2,scale=${format==='portrait'?180:320}:-1,tile=3x2`,'-frames:v','1',join(output,format+'-contact.png')]);
  checks[format]={pixelHashes:hashes,videoSha256:sha(await readFile(path)),probe:{frames:stream.nb_frames,duration:probe.format.duration,width:stream.width,height:stream.height,codec:stream.codec_name},fullDecode:true};
 }
 const record={projectSha256:sha(projectBytes),sceneSha256:sha(await readFile(join(own,'scene.mjs'))),previewSha256:sha(await readFile(join(own,'preview.html'))),browser:browser.version(),assets:Object.fromEntries(Object.entries(project.assets).map(([k,v])=>[k,v.sha256])),formats:checks,checks:['validated local relative assets, SHA-256, no symlinks','out-of-order repeated pixels','inherited clip and transform reset','reduced-motion pixel parity','24fps silent exact 288-frame encode','full MP4 decode'],limitations:'One local Chromium/FFmpeg runtime; lead visual and continuous playback review remain.'};await writeFile(join(output,'checks.json'),JSON.stringify(record,null,2)+'\n');result={output,formats:Object.keys(checks)};
}catch(error){failure=error}finally{const cleanupErrors=[];if(encoder){try{if(encoder.exitCode===null)encoder.kill();await encoderDone}catch(error){cleanupErrors.push(error)}}if(browser)try{await browser.close()}catch(error){cleanupErrors.push(error)}if(server.listening)try{await new Promise((r,j)=>server.close(error=>error?j(error):r()))}catch(error){cleanupErrors.push(error)}if(!failure&&cleanupErrors.length)failure=new AggregateError(cleanupErrors,'renderer cleanup failed')}
if(failure)throw failure;return result;
}
if(process.argv[1]&&resolve(process.argv[1])===fileURLToPath(import.meta.url)){const result=await render(...process.argv.slice(2));console.log(JSON.stringify(result))}
