import { createFigmaConverter } from '@figit/dom-to-figma';
import { encodeFigmaData, composeClipboardHtml } from '@figit/fig-kiwi';

const arrayBuffer = b64 => Uint8Array.from(atob(b64),c=>c.charCodeAt(0)).buffer;
window.htmlToFigmaCapture = async function(settings) {
  const root=document.querySelector(settings.selector||'body');
  if(!root)throw new Error(`Selector not found: ${settings.selector}`);
  const diagnostics={fonts:[],assets:[],omitted:[],risks:[]};
  const fontFaces=[];
  function rules(list,base){for(const rule of list){if(rule.type===CSSRule.FONT_FACE_RULE){
    const s=rule.style;const urls=[...s.getPropertyValue('src').matchAll(/url\(["']?([^"')]+)["']?\)/g)].map(m=>new URL(m[1],base).href);
    fontFaces.push({family:s.getPropertyValue('font-family').replace(/["']/g,'').trim(),weight:(s.getPropertyValue('font-weight')||'400').replace('normal','400').replace('bold','700'),italic:s.getPropertyValue('font-style')==='italic',urls,subset:s.getPropertyValue('unicode-range')});
  }else if(rule.cssRules)rules(rule.cssRules,base);}}
  for(const sheet of document.styleSheets){try{rules(sheet.cssRules,sheet.href||location.href);}catch{diagnostics.risks.push({kind:'unreadable-stylesheet',url:sheet.href});}}
  for(const f of fontFaces)if(fontFaces.filter(x=>x.family===f.family&&x.weight===f.weight&&x.italic===f.italic).length>1)diagnostics.risks.push({kind:'multiple-font-subsets-or-sources',family:f.family,reason:'one file per font request; verify glyph coverage'});
  const loadedFonts=new Map();
  async function fontLoader(req){
    const key=JSON.stringify(req);if(loadedFonts.has(key))return loadedFonts.get(key);
    try{
      const face=fontFaces.find(f=>f.family.toLowerCase()===req.family.toLowerCase()&&f.italic===req.italic&&((f.weight.split(/\s+/).length===2)?req.weight>=+f.weight.split(/\s+/)[0]&&req.weight<=+f.weight.split(/\s+/)[1]:+f.weight===req.weight));
      let file;
      if(face?.urls.length){let last;for(const url of face.urls){try{const r=await fetch(url);if(!r.ok)throw new Error(`HTTP ${r.status}`);file={bytes:await r.arrayBuffer()};diagnostics.fonts.push({...req,url,source:'local-page-font'});break;}catch(e){last=e;}}if(!file)throw last;}
      else{const r=await window.localFigmaFont(req);file={bytes:arrayBuffer(r.base64)};diagnostics.fonts.push({...req,sha256:r.sha256,source:'installed-or-mapped-font'});}
      loadedFonts.set(key,file);return file;
    }catch(e){diagnostics.fonts.push({...req,error:String(e)});throw e;}
  }
  const elements=[root,...root.querySelectorAll('*')];
  for(const el of elements){const s=getComputedStyle(el);if(s.display==='none'||s.visibility==='hidden')continue;
    if([...el.childNodes].some(n=>n.nodeType===Node.TEXT_NODE&&n.textContent.trim())||el.matches('input,textarea,select')){
      // Converter selects the first declared family. Resolve metrics before cache fingerprinting.
      const req={family:s.fontFamily.split(',')[0].replace(/["']/g,'').trim(),weight:+s.fontWeight||400,italic:s.fontStyle==='italic'};
      try{await fontLoader(req);}catch{}
    }
    if(el.matches('canvas,video,iframe')||s.filter!=='none'||s.maskImage!=='none')diagnostics.risks.push({tag:el.tagName,id:el.id,kind:'unsupported-or-approximate',filter:s.filter,mask:s.maskImage});
    if(el.matches('select,input[type=password],input[type=checkbox],input[type=radio],input[type=file],input[type=range]'))diagnostics.risks.push({tag:el.tagName,id:el.id,kind:'native-form-appearance-may-be-omitted'});
  }
  if(settings.phase==='inspect'){
    const styleState=elements.map(el=>{const s=getComputedStyle(el),r=el.getBoundingClientRect();return [el.tagName,el.id,[...s].map(k=>[k,s.getPropertyValue(k)]),[r.x,r.y,r.width,r.height],el.value??null,el.currentSrc??null];});
    return {diagnostics,fingerprint:JSON.stringify({html:root.outerHTML,styleState,fonts:diagnostics.fonts}),size:{width:Math.ceil(Math.max(root.scrollWidth,root.getBoundingClientRect().width)),height:Math.ceil(Math.max(root.scrollHeight,root.getBoundingClientRect().height))}};
  }
  const converter=createFigmaConverter({layout:settings.layout,trace:true,fontLoader,
    imageLoader:async({src})=>{try{const r=await fetch(src);if(!r.ok)throw new Error(`HTTP ${r.status}`);const bytes=await r.arrayBuffer();diagnostics.assets.push({src,bytes:bytes.byteLength});return {bytes,mimeType:r.headers.get('content-type')||'application/octet-stream'};}catch(e){diagnostics.assets.push({src,error:String(e)});throw e;}},
    classify:(el,kind)=>{if(kind==='skip'&&!['SCRIPT','STYLE','LINK','META'].includes(el.tagName))diagnostics.omitted.push({tag:el.tagName,id:el.id,reason:'converter-classification'});return kind;}
  });
  const rect=root.getBoundingClientRect();
  const result=await converter.convert({element:root,width:Math.ceil(Math.max(root.scrollWidth,rect.width)),height:Math.ceil(Math.max(root.scrollHeight,rect.height)),name:settings.name});
  // Upstream's synthetic outer frame is always vertical, even in absolute mode.
  // Disable that wrapper's Auto Layout too; converted absolute children retain geometry.
  let html=result.toClipboardHtml();
  if(settings.layout==='absolute'){
    for(const n of result.document.nodeChanges||[])if(n.type==='FRAME'){
      for(const k of Object.keys(n))if(k.startsWith('stack'))delete n[k];
    }
    const encoded=encodeFigmaData(result.document);html=composeClipboardHtml(encoded.base64);
  }
  const trace=result.trace?.entries||[];
  // Unmapped visible leaves are candidates, not a claim of exhaustive loss detection.
  const paths=new Set(trace.map(e=>e.domPath?.replace(/::text\[\d+\]$/,'')));
  function path(el){if(el===root)return ':scope';const seg=[];while(el&&el!==root){seg.unshift(`${el.tagName.toLowerCase()}:nth-child(${[...el.parentElement.children].indexOf(el)+1})`);el=el.parentElement;}return ':scope > '+seg.join(' > ');}
  for(const el of elements){const s=getComputedStyle(el),r=el.getBoundingClientRect();if(!el.children.length&&r.width&&r.height&&s.display!=='none'&&s.visibility!=='hidden'&&!paths.has(path(el))&&!el.closest('svg'))diagnostics.omitted.push({tag:el.tagName,id:el.id,path:path(el),reason:'visible-leaf-without-trace; review candidate'});}
  converter.clearCache();
  return {html,document:result.document,trace,diagnostics,size:{width:rect.width,height:rect.height}};
};
