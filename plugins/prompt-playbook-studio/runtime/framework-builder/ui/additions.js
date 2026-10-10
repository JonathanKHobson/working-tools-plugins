(function () {
  'use strict';
  // Per-framework drafts stay in this view; only explicit defaults use the local MCP store.
  const lenses = [
    {id:'analytical-algorithmic', label:'Logic', hint:'Organize the answer and check key steps.', prompt:'Preserve the requested format. Choose a clear approach, state material assumptions briefly, and check key calculations or prerequisites. Keep detailed working private; explain the result and useful steps concisely. Skip extra ceremony for simple tasks.'},
    {id:'divergent-inventive', label:'Creative', hint:'Explore distinct possibilities and choose a useful direction.', prompt:'Preserve the requested format. Consider distinct approaches, then recommend the strongest using clear criteria. When useful, include up to three genuinely different options and their trade-offs. Favor originality that fits the task; keep raw brainstorming private.'},
    {id:'skeptical-verifier', label:'Verify', hint:'Check claims, assumptions, and uncertainty.', prompt:'Preserve the requested format. Check the claims or calculations that matter, consider a credible counterexample, and revise unsupported conclusions. Cite sources when available and relevant; otherwise clearly identify what needs verification. Do not fabricate evidence. Keep uncertainty specific and concise.'},
    {id:'systems-integrator', label:'Systems', hint:'Consider connections, consequences, and trade-offs.', prompt:'Preserve the requested format. Define the scope, identify important dependencies and feedback loops, and explain likely downstream effects and trade-offs. Keep the analysis proportional to the task and avoid expanding its scope.'},
    {id:'human-centered-mediator', label:'Empathy', hint:'Make the answer considerate and easy to understand.', prompt:'Preserve the requested format and factual accuracy. Use clear, respectful language suited to the audience. Acknowledge relevant concerns without guessing feelings or facts. Avoid blame, platitudes, and unnecessary jargon; offer practical next steps when useful.'}
  ];
  const empty = () => ({version:1,lensId:'',instructions:'',keepOpen:false});
  const drafts = new Map();
  let saved = empty(), loaded = false, loading = null, active = null;
  const el = (tag,text,cls) => {const n=document.createElement(tag);if(text!==undefined)n.textContent=text;if(cls)n.className=cls;return n;};
  const equal = (a,b) => a.lensId===b.lensId && a.instructions===b.instructions && a.keepOpen===b.keepOpen;
  const values = s => ({version:1,lensId:s.lensId,instructions:s.instructions,keepOpen:s.keepOpen});
  function normalize(p) {
    if (!p || p.version!==1 || typeof p.instructions!=='string' || p.instructions.length>8000 || typeof p.keepOpen!=='boolean' || (p.lensId!==''&&!lenses.some(l=>l.id===p.lensId))) throw new Error('Saved defaults could not be read.');
    return {...p};
  }
  async function call(name,args={}) {
    const bridge=window.LibraryBridge;
    await bridge.ready();
    if(!bridge.canTools())throw new Error('This host cannot save defaults. You can still use additions in this prompt.');
    return normalize((await bridge.callTool(name,args)).preferences);
  }
  function stateFor(id) {
    if(!drafts.has(id)){if(drafts.size>=60)drafts.delete(drafts.keys().next().value);drafts.set(id,{...saved,enabled:true,touched:false});}
    return drafts.get(id);
  }
  function mount({itemId,host,onChange}) {
    const s=stateFor(itemId),section=el('details',undefined,'framework-additions');section.id='prompt-additions';section.open=s.keepOpen;
    const summary=el('summary','Prompt additions');section.append(summary);
    const body=el('div',undefined,'framework-additions-body');section.append(body);
    const intro=el('p','Choose a lens or add instructions. Your choices appear in the prompt preview.','framework-additions-help');body.append(intro);
    const includeLabel=el('label',undefined,'framework-additions-toggle');const include=el('input');include.type='checkbox';include.id='additions-enabled';include.checked=s.enabled;includeLabel.append(include,el('span','Include in this prompt'));body.append(includeLabel);
    const lensLabel=el('label','Response lens');lensLabel.htmlFor='additions-lens';
    const select=el('select');select.id='additions-lens';select.append(new Option('No lens',''));lenses.forEach(l=>select.append(new Option(l.label,l.id)));select.value=s.lensId;
    const hint=el('p','', 'framework-additions-help');hint.id='additions-lens-hint';select.setAttribute('aria-describedby',hint.id);body.append(lensLabel,select,hint);
    const label=el('label','Reusable instructions');label.htmlFor='additions-instructions';const instructions=el('textarea');instructions.id='additions-instructions';instructions.rows=3;instructions.maxLength=8000;instructions.value=s.instructions;instructions.placeholder='For example: Use plain language and end with one practical next step.';body.append(label,instructions);
    const defaults=el('div',undefined,'framework-additions-defaults');const openLabel=el('label',undefined,'framework-additions-toggle');const keepOpen=el('input');keepOpen.type='checkbox';keepOpen.id='additions-keep-open';keepOpen.checked=s.keepOpen;openLabel.append(keepOpen,el('span','Keep this panel expanded'));defaults.append(openLabel);
    const actions=el('div',undefined,'framework-additions-actions');const save=el('button','Save as my defaults');save.id='additions-save';save.type='button';const restore=el('button','Use saved defaults');restore.id='additions-restore';restore.type='button';actions.append(save,restore);defaults.append(actions);
    defaults.append(el('p','Defaults are saved on this device for new framework drafts. Fields and one-time instructions are not saved.','framework-additions-help'));
    const status=el('p','Loading saved defaults…','framework-additions-status');status.id='additions-status';status.setAttribute('role','status');defaults.append(status);body.append(defaults);host.append(section);
    let pending=false;
    const view={s,section,refresh,changed:onChange};active=view;
    function refresh() {
      const lens=lenses.find(l=>l.id===s.lensId);const has=!!(lens||s.instructions.trim());
      summary.textContent='Prompt additions'+(has?' · '+(!s.enabled?'Off':[lens?.label,s.instructions.trim()?'Instructions':null].filter(Boolean).join(' + ')):' (optional)');
      hint.textContent=lens?.hint||'Lenses add a short instruction to the prompt.';
      includeLabel.hidden=!has;include.checked=s.enabled;select.value=s.lensId;instructions.value=s.instructions;keepOpen.checked=s.keepOpen;
      save.disabled=pending||(loaded&&equal(s,saved));save.textContent=pending?'Saving…':loaded&&equal(s,saved)?'Defaults saved':'Save as my defaults';
      restore.disabled=pending||!loaded||equal(s,saved);
    }
    function edit() {s.touched=true;status.textContent='Changes apply to this prompt. Save to reuse them.';refresh();onChange();}
    select.addEventListener('change',()=>{s.lensId=select.value;edit();});
    instructions.addEventListener('input',()=>{s.instructions=instructions.value;edit();});
    include.addEventListener('change',()=>{s.enabled=include.checked;s.touched=true;refresh();onChange();});
    keepOpen.addEventListener('change',()=>{s.keepOpen=keepOpen.checked;edit();});
    restore.addEventListener('click',()=>{Object.assign(s,saved,{enabled:true,touched:true});section.open=true;status.textContent='Saved defaults applied to this prompt.';refresh();onChange();});
    save.addEventListener('click',async()=>{
      if(pending)return;const snapshot=values(s);pending=true;refresh();status.textContent='Saving defaults on this device…';
      try {saved=await call('save_framework_preferences',{lens_id:snapshot.lensId,instructions:snapshot.instructions,keep_open:snapshot.keepOpen});loaded=true;status.textContent='Defaults saved on this device.';}
      catch(error) {
        // The write may have committed before a lost response. Read back before offering another save.
        try {const actual=await call('read_framework_preferences');saved=actual;loaded=true;status.textContent=equal(actual,snapshot)?'Defaults saved on this device.':'Save was not confirmed. Your current prompt is unchanged; try saving again.';}
        catch {status.textContent='Save could not be confirmed. Your additions still work in this prompt. Try again when the connection is available.';}
      } finally {pending=false;refresh();}
    });
    refresh();
    if(loaded){status.textContent='Saved defaults are ready. Changes stay in this prompt until you save.';return;}
    if(!loading)loading=call('read_framework_preferences').then(p=>{saved=p;loaded=true;return p;}).finally(()=>{loading=null;});
    loading.then(p=>{if(active!==view)return;if(!s.touched){Object.assign(s,p);section.open=p.keepOpen;refresh();onChange();}status.textContent='Defaults loaded from this device.';}).catch(error=>{if(active!==view)return;status.textContent=error.message;refresh();});
  }
  function compose(id) {const s=stateFor(id);if(!s.enabled)return '';const lens=lenses.find(l=>l.id===s.lensId);return [lens?'Response lens — '+lens.label+'\n'+lens.prompt:'',s.instructions.trim()?'Reusable instructions\n'+s.instructions.trim():''].filter(Boolean).join('\n\n');}
  function seed(id,p) {
    const s=stateFor(id);
    if(p.lensId!==null&&p.lensId!==undefined){s.lensId=p.lensId;s.touched=true;}
    if(p.reusableInstructions!==null&&p.reusableInstructions!==undefined){s.instructions=p.reusableInstructions;s.touched=true;}
  }
  window.FrameworkAdditions={mount,compose,seed};
})();
