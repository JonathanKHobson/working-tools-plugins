(function(){'use strict';
let data={};try{data=JSON.parse(document.getElementById('library-data')?.textContent||'{}');}catch(_){}
const items=(Array.isArray(data.items)?data.items:[]).map(item=>({...item,revision:data.revision}));
const categories=[...new Set(items.map(i=>i.category).filter(Boolean))];
const domainOptions=[{value:'all',label:'All domains'},...['graphic','ux','creative','video'].map(value=>({value,label:value[0].toUpperCase()+value.slice(1)}))];
const categoryOptions=[{value:'all',label:'All categories'},...categories.map(value=>({value,label:value}))];
window.LibraryAdapter={
 title:'Image Gen Templates',noun:'template',labels:{search:'Search image templates',plural:'templates',back:'Back to templates'},items,
 filters:[{id:'domain',label:'Domain',type:'select',default:'all',options:domainOptions},{id:'category',label:'Category',type:'select',default:'all',options:categoryOptions}],
 searchText(item){return [item.id,item.name,item.category,item.useCase,item.summary].join(' ');},
 matches(item,values){return (values.domain==='all'||item.domains?.includes(values.domain))&&(values.category==='all'||item.category===values.category);},
 detailType(item){return item.category+' · '+item.domains.join(', ');},
 preview(item){return item.preview?{image:item.preview,meta:'Example output · '+item.category}:{text:item.summary+'\n\nExample: '+item.exampleSubject,meta:'Prompt recipe · '+item.category};},
 details(item){return [
  ...(item.preview?[{label:'Example output',text:'Generated example from this template. Your result will vary with your subject, references and instructions.',image:item.preview}]:[]),
  {label:'Purpose',text:item.summary},
  {label:'Best use',text:item.useCase.replaceAll('-',' ')},
  {label:'Example subject',text:item.exampleSubject},
  {label:'Source image',text:item.reference==='required'?'Required; attach an actual image in the conversation.':item.reference==='optional'?'Optional; attach an actual image if using one.':'No source image required.'},
  {label:'Starting direction',text:item.prompt},
  {label:'Review checks',text:(item.checks||[]).map(c=>'- '+c).join('\n')}
 ];},
 editor:window.ImageWorkflowEditor,
 localPrompt(item,brief){return window.ImageWorkflowEditor.compose(item,brief);}
};
window.LibraryBridge?.onToolResult(result=>{const payload=result?.structuredContent||result?.result?.structuredContent;
 if(!payload||payload.schemaVersion!==1||typeof payload.domain!=='string')return;
 const select=document.getElementById('filter-domain');
 if(select&&domainOptions.some(o=>o.value===payload.domain)){select.value=payload.domain;select.dispatchEvent(new Event('change',{bubbles:true}));}
});
})();
