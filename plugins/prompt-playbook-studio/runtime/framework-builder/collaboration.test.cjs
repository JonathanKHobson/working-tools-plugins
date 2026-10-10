'use strict';
// Rendered HTML in a simulated MCP host. Native Codex acceptance remains separate.
const assert = require('node:assert/strict');
const {execFileSync} = require('node:child_process');
const {chromium} = require(process.env.PROMPT_PLAYWRIGHT_MODULE || 'playwright');
const path = require('node:path');

const root = __dirname;
const html = execFileSync('python3', ['-c',
  `import sys; sys.path.insert(0, ${JSON.stringify(root)}); import server; print(server.render_html())`],
  {encoding:'utf8',maxBuffer:8*1024*1024});
assert(html.includes('FrameworkAdditions'));

const host = `<!doctype html><html><head><style>body{margin:0}iframe{display:block;width:100%;height:100vh;border:0}</style></head><body><iframe id="widget" src="http://mock.local/widget"></iframe>
<script>
window.mock={sent:[],calls:[],saveFailure:false,defaults:{version:1,lensId:'',instructions:'',keepOpen:false}};
window.addEventListener('message',event=>{
  const message=event.data, frame=document.getElementById('widget').contentWindow;
  if(event.source!==frame||message?.jsonrpc!=='2.0'||!message.id)return;
  let result={};
  if(message.method==='ui/initialize')result={protocolVersion:'2026-01-26',hostCapabilities:{serverTools:true,message:{text:true}},hostContext:{displayMode:'inline',availableDisplayModes:['inline','fullscreen'],theme:'light'}};
  else if(message.method==='ui/request-display-mode')result={mode:message.params.mode};
  else if(message.method==='tools/call'){
    const name=message.params.name,args=message.params.arguments;
    window.mock.calls.push({name,args});
    if(name==='read_framework_preferences')result={structuredContent:{preferences:{...window.mock.defaults}}};
    else if(name==='save_framework_preferences'){
      if(window.mock.saveFailure){frame.postMessage({jsonrpc:'2.0',id:message.id,error:{code:-1,message:'Response lost'}},'*');return;}
      window.mock.defaults={version:1,lensId:args.lens_id,instructions:args.instructions,keepOpen:args.keep_open};
      result={structuredContent:{preferences:{...window.mock.defaults}}};
    }
  }else if(message.method==='ui/message')window.mock.sent.push(message.params.content[0].text);
  frame.postMessage({jsonrpc:'2.0',id:message.id,result},'*');
});
window.offer=prefill=>document.getElementById('widget').contentWindow.postMessage({jsonrpc:'2.0',method:'ui/notifications/tool-result',params:{structuredContent:{prefill}}},'*');
<\/script></body></html>`;

async function main() {
  const browser=await chromium.launch({headless:true});
  try {
    const page=await browser.newPage({viewport:{width:1100,height:850}}),errors=[];
    page.on('pageerror',error=>errors.push(error.message));
    await page.route('http://mock.local/**',route=>route.fulfill({status:200,contentType:'text/html',body:route.request().url().endsWith('/widget')?html:host}));
    await page.goto('http://mock.local/host');
    const frame=page.frameLocator('#widget');
    await frame.locator('#cards .card').first().waitFor();
    const prefill={id:'proposal-1',frameworkId:'clear-prompting-method',values:{clarity:'Explain the course choice',ctx:'Adult learners'},additionalInstructions:'Use one example.',rationale:'CLEAR fits the communication task.',lensId:null,reusableInstructions:null};
    await page.evaluate(p=>window.offer(p),prefill);
    await frame.locator('#framework-field-0').waitFor();
    assert.equal(await frame.locator('#framework-field-0').inputValue(),'Explain the course choice');
    assert.equal(await frame.locator('#framework-field-context').inputValue(),'Adult learners');
    assert.equal(await frame.locator('#brief').inputValue(),'Use one example.');
    assert.match(await frame.locator('.framework-rationale').textContent(),/CLEAR fits/);
    const additions=frame.locator('#prompt-additions');
    assert.equal(await additions.evaluate(el=>el.open),false);
    await frame.locator('#prompt').waitFor({state:'visible'});
    await page.screenshot({path:path.join(root,'qa/collaboration-wide.png')});
    await page.setViewportSize({width:390,height:844});
    await page.screenshot({path:path.join(root,'qa/collaboration-narrow.png')});
    await page.setViewportSize({width:1100,height:850});
    await frame.locator('#framework-field-0').fill('Human revised course choice');
    await page.evaluate(p=>window.offer(p),prefill);
    assert.equal(await frame.locator('#framework-field-0').inputValue(),'Human revised course choice');
    await page.evaluate(p=>window.offer({...p,id:'proposal-2',values:{clarity:'Assistant replacement'}}),prefill);
    await frame.locator('#framework-collaboration-status').getByText(/Your edited draft was kept/).waitFor();
    assert.equal(await frame.locator('#framework-field-0').inputValue(),'Human revised course choice');
    assert.equal(await page.evaluate(()=>window.mock.sent.length),0);

    await additions.locator('summary').focus();
    await additions.locator('summary').press('Enter');
    assert.equal(await additions.evaluate(el=>el.open),true);
    await frame.locator('#additions-lens').selectOption('skeptical-verifier');
    await frame.locator('#additions-instructions').fill('Use the exact audience vocabulary.');
    await page.waitForFunction(()=>document.querySelector('#widget').contentDocument.querySelector('#prompt').value.includes('Use the exact audience vocabulary.'));
    let preview=await frame.locator('#prompt').inputValue();
    assert.match(preview,/Response lens — Verify/);
    assert.match(preview,/Reusable instructions\nUse the exact audience vocabulary\./);
    assert.equal(preview.split('Use the exact audience vocabulary.').length-1,1);
    assert.equal(await page.evaluate(()=>window.mock.calls.filter(c=>c.name==='save_framework_preferences').length),0);

    await frame.locator('#additions-keep-open').check();
    await frame.locator('#additions-save').click();
    await frame.locator('#additions-status').getByText('Defaults saved on this device.').waitFor();
    const saved=await page.evaluate(()=>window.mock.defaults);
    assert.deepEqual(saved,{version:1,lensId:'skeptical-verifier',instructions:'Use the exact audience vocabulary.',keepOpen:true});
    assert.equal(await page.evaluate(()=>window.mock.calls.filter(c=>c.name==='save_framework_preferences').length),1);
    await page.waitForFunction(()=>document.querySelector('#widget').contentDocument.querySelector('#use').textContent==='Send to conversation');
    await additions.scrollIntoViewIfNeeded();
    await page.screenshot({path:path.join(root,'qa/collaboration-additions-wide.png')});
    await page.setViewportSize({width:390,height:844});
    await additions.scrollIntoViewIfNeeded();
    await page.screenshot({path:path.join(root,'qa/collaboration-additions-narrow.png')});
    await page.evaluate(()=>document.querySelector('#widget').contentWindow.postMessage({jsonrpc:'2.0',method:'ui/notifications/host-context-changed',params:{theme:'dark',displayMode:'fullscreen'}},'*'));
    await page.waitForFunction(()=>document.querySelector('#widget').contentDocument.documentElement.dataset.theme==='dark');
    await additions.scrollIntoViewIfNeeded();
    await page.screenshot({path:path.join(root,'qa/collaboration-additions-dark.png')});
    await page.evaluate(()=>document.querySelector('#widget').contentWindow.postMessage({jsonrpc:'2.0',method:'ui/notifications/host-context-changed',params:{theme:'light',displayMode:'fullscreen'}},'*'));
    await page.setViewportSize({width:1100,height:850});

    await frame.locator('#additions-instructions').fill('Unsaved current change.');
    await page.evaluate(()=>window.mock.saveFailure=true);
    await frame.locator('#additions-save').click();
    await frame.locator('#additions-status').getByText(/Save was not confirmed/).waitFor();
    assert.equal(await frame.locator('#additions-instructions').inputValue(),'Unsaved current change.');
    assert.match(await frame.locator('#prompt').inputValue(),/Unsaved current change/);
    assert.deepEqual(await page.evaluate(()=>window.mock.defaults),saved);
    assert(await page.evaluate(()=>window.mock.calls.filter(c=>c.name==='read_framework_preferences').length)>=2);
    await page.evaluate(()=>window.mock.saveFailure=false);

    await frame.locator('#additions-enabled').uncheck();
    await page.waitForFunction(()=>!document.querySelector('#widget').contentDocument.querySelector('#prompt').value.includes('Response lens — Verify'));
    preview=await frame.locator('#prompt').inputValue();
    assert(!preview.includes('Use the exact audience vocabulary.'));
    assert.match(preview,/Human revised course choice/);
    await frame.locator('#additions-restore').click();
    await page.waitForFunction(()=>document.querySelector('#widget').contentDocument.querySelector('#prompt').value.includes('Response lens — Verify'));

    const before=await frame.locator('#prompt').inputValue();
    await frame.locator('#framework-collaborate').click();
    await page.waitForFunction(()=>window.mock.sent.length===1);
    const message=await page.evaluate(()=>window.mock.sent[0]);
    assert.match(message,/Refinement request — do not execute/);
    assert.match(message,/Work through this framework with me/);
    assert.match(message,/Human revised course choice/);
    assert.match(message,/Read its current fields before changing anything/);
    assert.notEqual(message,before);
    assert(message.endsWith(before));
    assert.equal(await frame.locator('#framework-field-0').inputValue(),'Human revised course choice');

    await frame.locator('#handoff-back').click();
    await frame.locator('#search').fill('Tarot Spread Reflection');
    await frame.locator('.card-hit').first().click();
    await frame.locator('#detail-use').click();
    await frame.locator('#additions-lens').waitFor();
    assert.equal(await frame.locator('#additions-lens').inputValue(),'skeptical-verifier');
    assert.equal(await frame.locator('#additions-instructions').inputValue(),'Use the exact audience vocabulary.');
    assert.equal(await frame.locator('#prompt-additions').evaluate(el=>el.open),true);
    await page.waitForFunction(()=>document.querySelector('#widget').contentDocument.querySelector('#prompt').value.includes('Response lens — Verify'));
    assert.deepEqual(errors,[]);
    console.log('simulated-host collaboration: prefill, collision protection, additions, save readback, inherited defaults, and exact-preview refinement message passed');
  } finally {await browser.close();}
}
main().catch(error=>{console.error(error);process.exitCode=1;});
