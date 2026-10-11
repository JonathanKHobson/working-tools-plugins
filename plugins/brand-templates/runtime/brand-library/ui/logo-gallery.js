/* Shared inline logo browsing for the public library and native brand picker. */
(() => {
  'use strict';
  const el=(tag,cls,text)=>{const n=document.createElement(tag);if(cls)n.className=cls;if(text!=null)n.textContent=text;return n;};
  const button=(text,action)=>{const b=el('button','brand-logo-button',text);b.type='button';b.addEventListener('click',action);return b;};
  function mount(brand,resolve=value=>value){
    const data=brand.logoGallery;if(!data?.entries?.length)return null;
    const entries=data.entries,root=el('section','brand-logo-gallery');root.setAttribute('aria-label',data.title||'Logos and illustrations');
    root.append(el('h3','',data.title||'Logos and illustrations'),el('p','brand-logo-description',data.description));
    const controls=el('div','brand-logo-controls'),label=el('label','brand-logo-choice','Choose a logo or illustration'),select=el('select');label.append(select);let group;
    entries.forEach((entry,index)=>{if(!group||group.label!==entry.group){group=el('optgroup');group.label=entry.group;select.append(group);}const option=el('option','',entry.label);option.value=index;group.append(option);});
    let index=0;const previous=button('Previous',()=>show(index-1)),next=button('Next',()=>show(index+1)),count=el('span','brand-logo-count');controls.append(label,previous,count,next);root.append(controls);
    const figure=el('figure','brand-logo-figure'),field=el('div','brand-logo-field'),image=el('img','brand-logo-image'),caption=el('figcaption','brand-logo-caption'),notice=el('p','brand-logo-status');notice.setAttribute('role','status');image.decoding='async';field.append(image);figure.append(field,caption);root.append(figure,notice);
    const sizes=el('div','brand-logo-sizes');root.append(sizes);
    const enlarge=button('Open larger preview',()=>{
      const entry=entries[index],dialog=el('dialog','brand-logo-dialog'),heading=el('h2','',entry.label),close=button('Close preview',()=>dialog.close()),art=el('img','brand-logo-expanded'),description=el('p','',entry.caption);dialog.setAttribute('aria-label',entry.label+' larger preview');art.src=resolve(entry.image);art.alt=entry.alt||entry.label;art.style.background=entry.backing==='navy'?'#03254A':'#FFFFFF';dialog.append(close,heading,art,description);document.body.append(dialog);dialog.addEventListener('click',event=>{if(event.target===dialog)dialog.close();});dialog.addEventListener('close',()=>{dialog.remove();if(enlarge.isConnected)enlarge.focus();},{once:true});dialog.showModal();close.focus();
    });root.append(enlarge);
    image.addEventListener('load',()=>{image.hidden=false;notice.textContent='';});image.addEventListener('error',()=>{image.hidden=true;notice.textContent='This preview could not load. Choose another view or reopen this brand.';});
    function show(value){
      index=Math.max(0,Math.min(entries.length-1,value));const entry=entries[index];select.value=String(index);previous.disabled=index===0;next.disabled=index===entries.length-1;count.textContent=(index+1)+' of '+entries.length;
      field.style.background=entry.backing==='navy'?'#03254A':'#FFFFFF';image.alt=entry.alt||entry.label;image.hidden=false;image.style.maxWidth=entry.displayPx?entry.displayPx+'px':'100%';image.src=resolve(entry.image);caption.replaceChildren(el('strong','',entry.label),el('span','',entry.status),el('span','',entry.caption));sizes.replaceChildren();sizes.hidden=!entry.sizes?.length;
      if(entry.sizes?.length){sizes.append(el('h4','','At the supplied pixel sizes'));const row=el('div','brand-logo-size-row');for(const size of entry.sizes){const item=el('figure','brand-logo-size'),img=el('img');img.src=resolve(size.image);img.alt=entry.label+' at '+size.px+' pixels';img.width=size.px;img.height=size.px;img.style.background=entry.backing==='navy'?'#03254A':'#FFFFFF';item.append(img,el('figcaption','',size.px+'px'));row.append(item);}sizes.append(row);}
    }
    select.addEventListener('change',()=>show(Number(select.value)));show(0);return root;
  }
  window.BrandLogoGallery={mount};
})();
