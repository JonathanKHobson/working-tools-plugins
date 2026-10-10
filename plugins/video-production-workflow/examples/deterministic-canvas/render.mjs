// Explicit local dependencies only. Does not install software or run upstream kits.
import {createServer} from 'node:http';
import {readFile,mkdir,writeFile,access} from 'node:fs/promises';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {resolve,dirname,join,isAbsolute} from 'node:path';
import {createHash} from 'node:crypto';
import {spawn,execFileSync} from 'node:child_process';
import {once} from 'node:events';
import assert from 'node:assert/strict';
import {sceneAt,DURATION,BEATS} from './scene.mjs';
const root=dirname(fileURLToPath(import.meta.url));
const dest=process.argv[2];
if(!dest||!isAbsolute(dest))throw new Error('Supply a NEW absolute output directory');
const output=resolve(dest);
try {await access(output);throw new Error('Output already exists; use a new directory');}catch(e){if(e.code!=='ENOENT')throw e;}
for(const key of ['PLAYWRIGHT_MODULE','FFMPEG','FFPROBE'])if(!process.env[key]||!isAbsolute(process.env[key]))throw new Error(key+' must be an absolute reviewed local path');
const {chromium}=await import(pathToFileURL(process.env.PLAYWRIGHT_MODULE).href);
const sha=b=>createHash('sha256').update(b).digest('hex');
for(const fps of [24,25,30,60]){assert.equal(sceneAt(4*fps,fps).beat,'storyboard');assert.equal(sceneAt(8*fps,fps).beat,'render');assert.equal(sceneAt(12*fps,fps).phase,'hold');}
for(const pair of [[-1,24],[1.2,24],[0,0],[0,NaN]])assert.throws(()=>sceneAt(...pair),RangeError);
await mkdir(output,{recursive:true});
const routes={'/':'preview.html','/preview.html':'preview.html','/scene.mjs':'scene.mjs'};
const server=createServer(async(req,res)=>{const file=routes[req.url];if(!file){res.writeHead(404);res.end();return;}try{res.setHeader('Content-Type',file.endsWith('.html')?'text/html':'text/javascript');res.end(await readFile(join(root,file)));}catch{res.writeHead(500);res.end();}});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const url=`http://127.0.0.1:${server.address().port}/`;
let browser,encoder;
try{
 browser=await chromium.launch({headless:true});
 const page=await browser.newPage({viewport:{width:1024,height:800},deviceScaleFactor:1});
 await page.route('**/*',route=>route.request().url().startsWith(url)?route.continue():route.abort());
 await page.goto(url);await page.evaluate(()=>window.ready);
 const pixels=async(frame,dirty=false)=>page.evaluate(({frame,dirty})=>{const c=document.querySelector('canvas'),ctx=c.getContext('2d');if(dirty){ctx.rect(0,0,2,2);ctx.clip();ctx.translate(20,20);ctx.globalAlpha=.1;ctx.shadowBlur=24;}window.renderFrame(frame);return c.toDataURL('image/png').split(',')[1];},{frame,dirty});
 const seen={};
 for(const f of [287,0,143,287,96,0]){const h=sha(Buffer.from(await pixels(f),'base64'));if(seen[f])assert.equal(h,seen[f]);seen[f]=h;}
 for(const f of [0,96,143,287])assert.equal(sha(Buffer.from(await pixels(f,true),'base64')),seen[f]);
 await page.emulateMedia({reducedMotion:'reduce'});assert.equal(sha(Buffer.from(await pixels(143),'base64')),seen[143]);
 await page.emulateMedia({reducedMotion:'no-preference'});
 const bounds=await page.evaluate(()=>{const c=document.querySelector('canvas'),ctx=c.getContext('2d');ctx.font='22px MotionExample';return window.sceneBeats.map(b=>({beat:b.name,width:ctx.measureText(b.caption).width}));});
 assert(bounds.every(b=>b.width<=840));
 encoder=spawn(process.env.FFMPEG,['-hide_banner','-loglevel','error','-n','-f','image2pipe','-framerate','24','-i','pipe:0','-an','-c:v','libx264','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-movflags','+faststart',join(output,'preview.mp4')],{stdio:['pipe','ignore','pipe']});
 let err='';encoder.stderr.on('data',d=>err+=d);const complete=once(encoder,'close');encoder.stdin.on('error',()=>{});
 const anchors=new Set([0,48,90,96,144,186,192,264,287]);
 for(let f=0;f<DURATION*24;f++){const png=Buffer.from(await pixels(f),'base64');if(anchors.has(f))await writeFile(join(output,`frame-${f}.png`),png);if(!encoder.stdin.write(png))await once(encoder.stdin,'drain');}
 encoder.stdin.end();const [code]=await complete;if(code!==0)throw new Error(err);
 const probe=JSON.parse(execFileSync(process.env.FFPROBE,['-v','error','-show_streams','-show_format','-of','json',join(output,'preview.mp4')],{encoding:'utf8'}));
 assert.equal(Number(probe.streams[0].nb_frames),288);assert.equal(Number(probe.format.duration),12);
 execFileSync(process.env.FFMPEG,['-v','error','-i',join(output,'preview.mp4'),'-f','null','-']);
 const record={browser:browser.version(),fps:24,frames:288,duration:12,checks:['boundary rates 24/25/30/60','out-of-order pixel equality','dirty clip reset','reduced-motion export parity','text width','probe and full decode'],pixelHashes:seen,textWidths:bounds,sceneSha256:sha(await readFile(join(root,'scene.mjs'))),videoSha256:sha(await readFile(join(output,'preview.mp4'))),font:'MotionExample explicitly loaded from local Arial',audio:'silent; not tested',limits:'One browser/environment. No cross-platform pixel guarantee. Visual/playback review separate.'};
 await writeFile(join(output,'checks.json'),JSON.stringify(record,null,2)+'\n');console.log(JSON.stringify(record));
}finally{if(encoder&&encoder.exitCode===null)encoder.kill();if(browser)await browser.close();await new Promise(r=>server.close(r));}
