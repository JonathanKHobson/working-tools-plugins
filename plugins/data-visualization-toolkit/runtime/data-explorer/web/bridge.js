import {App} from '@modelcontextprotocol/ext-apps';
export function createBridge(onData,onContext,onClosed){
  const preview=window.DATA_PREVIEW;let app;const state={mode:preview?'preview':'connecting',tools:!!preview,message:false,context:false,host:{}};
  const ready=(async()=>{
    if(preview){if(preview.data)queueMicrotask(()=>onData(preview.data));return state}
    if(window.parent===window){state.mode='offline';return state}
    try{
      app=new App({name:'Data Explorer',version:'0.1.0'},{availableDisplayModes:['inline','fullscreen']});
      app.ontoolresult=result=>{if(result.structuredContent?.dataset_id&&result.structuredContent.rows)onData(result.structuredContent)};
      app.onhostcontextchanged=ctx=>{state.host={...state.host,...ctx};onContext(state.host)};
      app.onteardown=async()=>{state.mode='closed';state.tools=false;onClosed();return {}};
      await app.connect();const caps=app.getHostCapabilities()||{};
      state.mode='host';state.tools=!!caps.serverTools;state.message=!!caps.message?.text;state.context=!!(caps.updateModelContext?.structuredContent||caps.updateModelContext?.text);state.structured=!!caps.updateModelContext?.structuredContent;state.host=app.getHostContext()||{};onContext(state.host);
    }catch(e){state.mode='offline';state.error=e.message}
    return state;
  })();
  return {state,ready,async call(name,args){await ready;if(!state.tools)throw Error('Explorer storage is unavailable.');let result;
    if(preview){const response=await fetch('/api/tool',{method:'POST',headers:{'Content-Type':'application/json','X-Explorer-Token':preview.token},body:JSON.stringify({name,arguments:args})});if(!response.ok)throw Error(`Preview request failed (${response.status})`);result=await response.json()}
    else result=await app.callServerTool({name,arguments:args},{timeout:15000});
    if(result.isError||result.structuredContent?.error){const e=new Error(result.structuredContent?.error?.message||result.content?.find(c=>c.type==='text')?.text||'Explorer operation failed');e.code=result.structuredContent?.error?.code;e.current=result.structuredContent?.current;e.confirmed=true;throw e}return result.structuredContent;
  },async discuss(snapshot,text){await ready;if(!app)return {sent:false,staged:false};let staged=false;
    if(state.context){try{await app.updateModelContext(state.structured?{structuredContent:snapshot}:{content:[{type:'text',text:JSON.stringify(snapshot)}]});staged=true}catch{}}
    if(state.message){try{const result=await app.sendMessage({role:'user',content:[{type:'text',text}]});if(result?.isError)throw Error('Host rejected message');return {sent:true,staged}}catch{}}
    return {sent:false,staged};
  },async expand(){if(!app||!state.host.availableDisplayModes?.includes('fullscreen'))return false;const target=state.host.displayMode==='fullscreen'?'inline':'fullscreen';const result=await app.requestDisplayMode({mode:target});if(result.mode!==target)return false;state.host.displayMode=target;onContext(state.host);return true},close(){app?.close()}};
}
