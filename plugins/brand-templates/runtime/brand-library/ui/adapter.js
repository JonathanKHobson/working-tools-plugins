(function () {
  'use strict';
  const data = JSON.parse(document.getElementById('library-data').textContent);
  const items = data.items || [];
  const lines = values => (values || []).map(v => '• ' + v).join('\n');
  window.LibraryAdapter = {
    title: 'Brand Templates', noun: 'brand', items,
    createLabel: 'Create brand', createTitle: 'Create a reusable brand',
    createDescription: 'Describe the identity and its intended uses.',
    createPrompt: 'Help me create a reusable Brand Templates entry using Graphic Design brand-guide production and the installed Brand Templates workflow. First inspect the current package schema and a neighboring kit. Identify the audience, purpose, source references and rights. Build a complete editable identity with DESIGN.md, color/type/layout/logo rules, source assets and notices, writing guidance, an asset manifest with real hashes, and rendered previews. Keep fictional examples distinct from facts; do not invent permissions or trademark clearance. Review the candidate before registration, then verify its exact ID, preview, source closure and Use handoff. If registration is unavailable, provide the complete candidate and exact remaining steps. Prepared, registered and verified are separate states.',
    detailType: item => item.category,
    filters: [{id:'category',label:'Type',type:'select',default:'all',options:[{value:'all',label:'All types'}, ...[...new Set(items.map(i=>i.category))].sort().map(v=>({value:v,label:v}))]}],
    searchText: item => [item.id,item.name,item.summary,item.category,...item.tags,...item.sourceTemplateIds].join(' '),
    matches: (item,selected) => !selected || !selected.category || selected.category==='all' || selected.category===item.category,
    preview: item => ({image:item.preview,text:item.summary}),
    afterDetail: (item,host) => { if(item.logoGallery) { const gallery=window.BrandLogoGallery.mount(item); if(gallery)host.prepend(gallery); } },
    details: item => [
      {label:'Brand guide',image:item.preview},
      {label:'Purpose',text:item.summary},
      {label:'Recognition rules',text:lines(item.recognitionRules)},
      {label:'Colors',text:lines(item.colors.map(c=>c.name+': '+c.hex))},
      {label:'Typography',text:lines(item.typography.map(t=>t.role+': '+t.family+' · '+t.usage))},
      {label:'Source templates',text:lines(item.sourceTemplateIds)},
      {label:'Rights and substitutions',text:item.rightsSummary+' Read the selected kit typography and asset notices before adapting.'}
    ],
    localPrompt: (item,brief) => 'Prepare a verified Brand Templates handoff for '+item.name+' (ID: '+item.id+'). Call prepare_brand_handoff with brand_id="'+item.id+'" and brief="'+(brief||'')+'". Read the selected SKILL.md and DESIGN.md and preserve its source facts, recognition rules and font notices. Source validation was unavailable in this standalone chooser.',
    handoff: {
      tool:'prepare_brand_handoff',
      args:(item,brief)=>({brand_id:item.id,brief:brief||''}),
      text:(payload,item)=>{
        if (!payload || payload.brandId!==item.id || payload.sourceHash!==item.sourceHash || typeof payload.closureHash!=='string' || !payload.handoffText) throw new Error('Brand handoff did not match the selected source.');
        return payload.handoffText;
      }
    }
  };
})();
