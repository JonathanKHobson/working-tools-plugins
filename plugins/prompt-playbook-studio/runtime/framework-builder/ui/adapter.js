(function(){'use strict';
let data;try{data=JSON.parse(document.getElementById('library-data')?.textContent||'{}');}catch{data={};}
const items=Array.isArray(data.items)?data.items.filter(item=>item&&typeof item.id==='string'&&typeof item.name==='string'):[];
const kinds=Array.from(new Set(items.map(item=>item.kind).filter(Boolean))).sort((a,b)=>a.localeCompare(b));
const simple=value=>Array.isArray(value)?value.join(', '):String(value??'');
const itemSearch=item=>[item.name,item.kind,item.definition,item.help,...item.categories||[],...item.tags||[],...item.useCases||[]].join(' ');
const sourceLabel=item=>item.source?.status&&item.source.status!=='active'?' · '+item.source.status:'';
window.LibraryAdapter={
 title:'Framework Builder',noun:'framework',labels:{plural:'frameworks',search:'Search frameworks',back:'Back to frameworks'},
 items,editor:window.FrameworkBuilderEditor,
 toolbar:{id:'pattern-picker',label:'Find a framework'},
 filters:[{id:'kind',label:'Kind',type:'select',default:'',options:[{label:'All kinds',value:''},...kinds.map(kind=>({label:kind,value:kind}))]}],
 searchText:itemSearch,
 matches(item,filters){return !filters.kind||item.kind===filters.kind;},
 preview(item){return{text:[item.name,item.definition||item.help||''].filter(Boolean).join('\n\n'),meta:[item.kind||'Framework',...(item.categories||[]).slice(0,2)].join(' · ')+sourceLabel(item)};},
 detailType(item){return [item.kind||'Framework',...(item.categories||[]).slice(0,2)].join(' · ')+sourceLabel(item);},
 details(item){const result=[];if(item.definition)result.push({label:'What it is',text:item.definition});if(item.help)result.push({label:'How to use it',text:item.help});if(item.notice)result.push({label:'Source notice',text:simple(item.notice)});if(item.assemblyNote)result.push({label:'Assembly note',text:item.assemblyNote});if(item.useCases?.length)result.push({label:'Use cases',text:item.useCases.map(value=>'- '+value).join('\n')});if(item.fields?.length)result.push({label:'What you can enter',text:item.fields.map(field=>'- '+field.label+(field.required?' (required)':'')).join('\n')});if(item.source?.path)result.push({label:'Source',text:[item.source.path,item.source.status&&item.source.status!=='active'?'Status: '+item.source.status:''].filter(Boolean).join('\n')});return result;},
 localPrompt(item){return 'Use the selected framework: '+item.name+'.';},
 createLabel:'Create framework',createTitle:'Create a framework',
 createPrompt:'Help me create a new framework entry for the Framework Builder. First clarify the goal, audience, expected output, required fields, and a representative example. Inspect the owning source library and its current registration path before editing. Draft a source-compatible entry with a stable ID, definition, use cases, field schema, and prompt assembly. Validate the assembly with distinct sample values, register it through the owning pipeline only when supported, then verify the new framework appears in browse and search. Report which steps were drafted, saved, registered, and verified separately.'
};
})();
