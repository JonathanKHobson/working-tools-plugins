import { readFile, readdir, stat, realpath } from 'node:fs/promises';
import { join, extname, resolve, sep } from 'node:path';
import { homedir } from 'node:os';
import { createServer } from 'node:http';
import { createHash } from 'node:crypto';

export const sha = value => createHash('sha256').update(value).digest('hex');
export function isLocalURL(value) {
  try {const u=new URL(value);return ['http:','https:'].includes(u.protocol)&&['localhost','127.0.0.1','[::1]'].includes(u.hostname);}catch{return false;}
}
export function allowedResource(value,offline) {
  return /^(data:|blob:|about:)/.test(value)||isLocalURL(value)||(!offline&&/^https?:/.test(value));
}
export async function staticServer(root,{onCopied}={}) {
  root=await realpath(root);
  const types={'.html':'text/html','.css':'text/css','.js':'text/javascript','.mjs':'text/javascript','.svg':'image/svg+xml','.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg','.woff2':'font/woff2','.woff':'font/woff','.ttf':'font/ttf','.otf':'font/otf','.json':'application/json'};
  const server=createServer(async(req,res)=>{
    try{
      const url=new URL(req.url,'http://localhost');
      if(onCopied&&url.pathname==='/__copied'&&req.method==='POST'){res.writeHead(204);res.end();onCopied();return;}
      let p=await realpath(resolve(root,'.'+decodeURIComponent(url.pathname)));
      if(p!==root&&!p.startsWith(root+sep))throw new Error('outside root');
      if((await stat(p)).isDirectory())p=await realpath(join(p,'index.html'));
      if(!p.startsWith(root+sep))throw new Error('outside root');
      res.writeHead(200,{'Content-Type':types[extname(p)]||'application/octet-stream','Cache-Control':'no-store','Access-Control-Allow-Origin':'*'});res.end(await readFile(p));
    }catch{res.writeHead(404);res.end('Not found');}
  });
  await new Promise((r,j)=>{server.once('error',j);server.listen(0,'127.0.0.1',r);});
  return {url:`http://127.0.0.1:${server.address().port}`,close:()=>new Promise(r=>{server.closeAllConnections();server.close(r);})};
}

// Only explicit maps and installed single-file fonts. No remote catalog or metric substitution.
export async function createFontResolver(require,fontMapPath) {
  const fontkit=require('fontkit');
  const explicit=fontMapPath?JSON.parse(await readFile(fontMapPath,'utf8')):[];
  if(!Array.isArray(explicit))throw new Error('Font map must be an array of {family,weight,italic,path}.');
  const candidates=[];
  for(const dir of [join(homedir(),'Library/Fonts'),'/Library/Fonts','/System/Library/Fonts/Supplemental','/System/Library/Fonts']) {
    for(const f of await readdir(dir).catch(()=>[]))if(/\.(ttf|otf|woff2?)$/i.test(f))candidates.push(join(dir,f));
  }
  let catalog;
  const used=new Map();
  return {
    used,
    async load(req){
      const key=JSON.stringify(req);
      if(used.has(key))return used.get(key);
      let entry=explicit.find(f=>f.family.toLowerCase()===req.family.toLowerCase()&&Number(f.weight??400)===req.weight&&Boolean(f.italic)===req.italic);
      if(!entry){
        if(!catalog){catalog=[];for(const path of candidates){try{const f=fontkit.openSync(path);if(f.fonts||!f.familyName)continue;const style=f.subfamilyName||'';catalog.push({path,family:f.familyName,weight:f['OS/2']?.usWeightClass||(/bold/i.test(style)?700:400),italic:/italic|oblique/i.test(style)});}catch{}}}
        entry=catalog.find(f=>f.family.toLowerCase()===req.family.toLowerCase()&&f.weight===req.weight&&f.italic===req.italic);
      }
      if(!entry)throw new Error(`No exact local font: ${req.family} ${req.weight} ${req.italic?'italic':'normal'}. Supply --font-map.`);
      const bytes=await readFile(resolve(fontMapPath?resolve(fontMapPath,'..'):'.',entry.path));
      const result={base64:bytes.toString('base64'),sha256:sha(bytes),path:entry.path};used.set(key,result);return result;
    }
  };
}
