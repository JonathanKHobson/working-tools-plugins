(function () {
  'use strict';
  const B = window.LibraryBridge, M = window.StoryboardMedia, $ = id => document.getElementById(id);
  const draft = () => ({ storyboard_id: '', title: 'Untitled storyboard', revision: 0,
    shots: ['Opening', 'Development', 'Resolution'].map(name => ({ id: name.toLowerCase(), visual: '', duration_seconds: 5, narration: '' })),
    state: 'unsaved scaffold; durations are provisional' });
  let board = draft(), dirty = false, busy = false, request = null, handoff = null, editEpoch = 0, initialLoaded = false, pendingReload = null, editHere = false, imports = 0, dragId = null;
  const importTokens = new Map();
  function uid() { return crypto.randomUUID ? crypto.randomUUID().replace(/-/g, '') : 'op_' + Date.now() + '_' + Math.random().toString(36).slice(2); }
  function status(message) { $('status').textContent = message; }
  function snapshot() { return { title: $('title').value.trim(), shots: M.clone(board.shots) }; }
  function updateTotal() { const seconds = board.shots.reduce((sum, shot) => sum + (Number.isFinite(shot.duration_seconds) ? shot.duration_seconds : 0), 0); const label = board.shots.length + (board.shots.length === 1 ? ' shot' : ' shots') + ' · ' + Number(seconds.toFixed(1)) + 's total'; $('total').textContent = label; $('inline-total').textContent = label; }
  function renderInline() {
    $('inline-title').textContent = board.title || 'Untitled storyboard';
    const rows = board.shots.slice(0, 3).map((shot, index) => { const li = document.createElement('li'), number = document.createElement('strong'), summary = document.createElement('span'), duration = document.createElement('em'); number.textContent = String(index + 1).padStart(2, '0'); summary.textContent = shot.visual.trim() || (['opening', 'development', 'resolution'].includes(shot.id) ? shot.id[0].toUpperCase() + shot.id.slice(1) + ' · visual to add' : 'Visual to add'); duration.textContent = (Number.isFinite(shot.duration_seconds) ? shot.duration_seconds : 0) + 's'; li.append(number, summary, duration); return li; });
    if (board.shots.length > 3) { const more = document.createElement('li'); more.className = 'subtle'; more.textContent = '+' + (board.shots.length - 3) + ' more shots in the editor'; rows.push(more); }
    $('inline-shots').replaceChildren(...rows);
  }
  function showMode() { const full = editHere || B.state.context.displayMode === 'fullscreen' || B.state.mode === 'standalone'; $('inline-view').hidden = full; $('editor-view').hidden = !full; }
  function changed() { editEpoch++; dirty = true; handoff = null; $('handoff').hidden = true; $('draw').disabled = true; $('save').disabled = busy || imports > 0; updateAssistant(); $('save').textContent = board.storyboard_id ? 'Save changes' : 'Save storyboard'; $('state').textContent = board.storyboard_id ? 'Unsaved changes · revision ' + board.revision : 'Unsaved scaffold · durations are provisional'; updateTotal(); renderInline(); }
  function updateAssistant() { $('assistant-update').hidden = !B.canSend(); $('assistant-update').disabled = busy || imports > 0 || dirty || !board.storyboard_id; $('check-updates').disabled = busy || !board.storyboard_id; }
  function render() {
    $('title').value = board.title;
    $('state').textContent = board.storyboard_id ? (dirty ? 'Unsaved changes · revision ' : 'Saved · revision ') + board.revision : 'Unsaved scaffold · durations are provisional';
    updateTotal();
    renderInline();
    $('draw').disabled = !board.storyboard_id || dirty;
    $('save').textContent = dirty ? (board.storyboard_id ? 'Save changes' : 'Save storyboard') : 'Saved';
    $('save').disabled = busy || imports > 0 || (!dirty && !!board.storyboard_id); updateAssistant();
    $('shots').replaceChildren(...board.shots.map((shot, index) => {
      const li = document.createElement('li'); li.className = 'shot'; li.dataset.shotId = shot.id;
      const head = document.createElement('div'); head.className = 'shot-head';
      const h = document.createElement('h3'); const stage = ['opening', 'development', 'resolution'].includes(shot.id) ? ' · ' + shot.id[0].toUpperCase() + shot.id.slice(1) : ''; h.textContent = 'Shot ' + (index + 1) + stage; h.tabIndex = -1;
      head.title = 'Drag this shot to reorder';
      head.addEventListener('pointerdown', e => {
        if (e.target.closest('button, input, textarea, select, a')) return;
        beginDrag(e, shot.id, head);
      });
      head.append(h);
      const actions = document.createElement('div'); actions.className = 'shot-actions';
      function action(label, accessible, fn, disabled) { const b = document.createElement('button'); b.type = 'button'; if (label === 'up' || label === 'down') b.innerHTML = '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M10 16V4m0 0-5 5m5-5 5 5"' + (label === 'down' ? ' transform="rotate(180 10 10)"' : '') + '/></svg>'; else b.textContent = label; b.setAttribute('aria-label', accessible); b.disabled = disabled; b.addEventListener('click', fn); actions.append(b); }
      action('up', 'Move shot ' + (index+1) + ' up', () => move(index, -1), index === 0); action('down', 'Move shot ' + (index+1) + ' down', () => move(index, 1), index === board.shots.length - 1);
      action('Remove', 'Remove shot ' + (index+1), () => { if (board.shots.length <= 1) { status('Keep at least one shot.'); return; } board.shots.splice(index, 1); changed(); render(); $('shots').children[Math.min(index, board.shots.length-1)]?.querySelector('h3')?.focus(); });
      head.append(actions); li.append(head);
      function field(label, kind, value, handler) { const wrap = document.createElement('label'); wrap.textContent = label; const input = document.createElement(kind); input.value = value; if (kind === 'textarea') { input.rows = 3; input.maxLength = 2000; } input.addEventListener('input', () => { handler(input.value); changed(); }); wrap.append(input); li.append(wrap); return input; }
      field('Visual action', 'textarea', shot.visual, value => shot.visual = value);
      const duration = field('Duration (seconds)', 'input', shot.duration_seconds, value => shot.duration_seconds = Number(value)); duration.type = 'number'; duration.min = '.5'; duration.max = '600'; duration.step = '.5'; duration.className = 'duration';
      field('Narration', 'textarea', shot.narration, value => shot.narration = value);
      M.mount(li, shot, { changed, status, importReference, removeReference });
      return li;
    }));
  }
  function beginDrag(e, id, handle) {
    if (e.pointerType === 'mouse' && e.button !== 0) return;
    e.preventDefault(); dragId = id; handle.setPointerCapture(e.pointerId);
    let targetId = id;
    const source = handle.closest('.shot'); source.classList.add('dragging');
    function track(event) {
      const target = document.elementFromPoint(event.clientX, event.clientY)?.closest('.shot');
      document.querySelectorAll('.drop-target').forEach(el => el.classList.remove('drop-target'));
      if (target && target.dataset.shotId !== id) { targetId = target.dataset.shotId; target.classList.add('drop-target'); } else targetId = id;
    }
    function finish(event) {
      handle.removeEventListener('pointermove', track); handle.removeEventListener('pointerup', finish); handle.removeEventListener('pointercancel', cancel); handle.removeEventListener('lostpointercapture', cancel);
      document.querySelectorAll('.drop-target,.dragging').forEach(el => el.classList.remove('drop-target', 'dragging')); dragId = null;
      if (event.type === 'pointercancel' || event.type === 'lostpointercapture' || targetId === id) return;
      const from = board.shots.findIndex(s => s.id === id), to = board.shots.findIndex(s => s.id === targetId);
      if (from < 0 || to < 0) return;
      board.shots.splice(to, 0, board.shots.splice(from, 1)[0]); changed(); render(); $('shots').children[to]?.querySelector('h3')?.focus(); status('Moved shot to position ' + (to + 1) + '.');
    }
    function cancel(event) { finish(event); }
    handle.addEventListener('pointermove', track); handle.addEventListener('pointerup', finish); handle.addEventListener('pointercancel', cancel); handle.addEventListener('lostpointercapture', cancel);
  }
  function removeReference(id) { importTokens.delete(id); const shot = board.shots.find(s => s.id === id); if (!shot) return; delete shot.reference; changed(); render(); }
  async function importReference(id, file) {
    const token = uid(); importTokens.set(id, token); imports++; editEpoch++; $('save').disabled = true; updateAssistant(); status('Preparing reference image locally…');
    try {
      const reference = await M.importImage(file), shot = board.shots.find(s => s.id === id);
      if (!shot || importTokens.get(id) !== token) return;
      reference.description = shot.reference?.description || '';
      shot.reference = reference; changed(); render(); status('Reference image attached. Add a description, then save.');
    } catch(e) { status(e.message); }
    finally { if (importTokens.get(id) === token) importTokens.delete(id); imports--; $('save').disabled = busy || imports > 0 || (!dirty && !!board.storyboard_id); updateAssistant(); }
  }
  function move(index, offset) { const other = index + offset; if (other < 0 || other >= board.shots.length) return; [board.shots[index], board.shots[other]] = [board.shots[other], board.shots[index]]; changed(); render(); $('shots').children[other]?.querySelector('h3')?.focus(); }
  function validate(data) { if (!data.title) throw new Error('Add a storyboard title.'); if (new TextEncoder().encode(JSON.stringify(data)).length > 8 * 1024 * 1024 - 4096) throw new Error('This storyboard is too large to save (8 MB limit). Remove some reference images or sketches.'); if (!data.shots.length || data.shots.length > 20) throw new Error('Use 1–20 shots.'); for (const [i,s] of data.shots.entries()) if (!Number.isFinite(s.duration_seconds) || s.duration_seconds < .5 || s.duration_seconds > 600) throw new Error('Shot ' + (i+1) + ' needs a duration from 0.5 to 600 seconds.'); }
  async function save() {
    if (busy || imports > 0 || dragId) { status('Finish the image import or reorder before saving.'); return; }
    const data = snapshot(); try { validate(data); } catch(e) { status(e.message); return; }
    if (!request) request = { data, operation_id: uid(), revision: board.revision, id: board.storyboard_id };
    const newerDraft = JSON.stringify(request.data) !== JSON.stringify(data);
    const epoch = editEpoch;
    busy = true; updateAssistant(); $('reload').hidden = true; $('save').disabled = true; $('save').textContent = 'Saving…'; status(newerDraft ? 'Checking the prior save before saving newer edits.' : 'Saving the ordered shots.');
    try {
      const args = { ...request.data, operation_id: request.operation_id };
      const result = request.id ? await B.callTool('save_video_storyboard', { ...args, storyboard_id: request.id, expected_revision: request.revision }) : await B.callTool('create_video_storyboard', args);
      if (!result?.storyboard_id || !Number.isInteger(result.revision)) throw new Error('Save acknowledgment was incomplete.');
      if (!newerDraft && editEpoch === epoch) { board = result; dirty = false; }
      else { board = { ...result, ...snapshot() }; dirty = true; }
      request = null; pendingReload = null; initialLoaded = true; render(); status(dirty ? 'Saved revision ' + result.revision + '; newer edits still need saving.' : 'Saved revision ' + result.revision + '.');
    } catch (e) { if (String(e.message).includes('revision_conflict') && board.storyboard_id) { request = null; $('reload').hidden = false; status('Saved revision changed. Your edits are preserved. Check for updates; Reload saved version discards this draft.'); } else status(e.message + ' Save was not confirmed. Retry the same request to reconcile it.'); $('save').textContent = 'Retry save'; }
    finally { busy = false; $('save').disabled = imports > 0 || !dirty; updateAssistant(); }
  }
  async function prepare() {
    if (dirty || !board.storyboard_id || busy || imports) { status('Save the storyboard before preparing a Draw and Think handoff.'); return; }
    const epoch = editEpoch, id = board.storyboard_id, revision = board.revision;
    busy = true; updateAssistant(); $('draw').disabled = true; $('draw').textContent = 'Preparing…'; $('send').disabled = false; $('send').textContent = 'Send to conversation';
    try {
      const result = await B.callTool('prepare_video_storyboard_draw_handoff', { storyboard_id: id, expected_revision: revision });
      if (editEpoch !== epoch || dirty || board.storyboard_id !== id || board.revision !== revision) throw new Error('Shots changed while preparing. Save again before handoff.');
      if (!result || result.storyboardId !== id || result.revision !== revision || !result.handoffText) throw new Error('The handoff did not match this saved revision.');
      handoff = result; $('prompt').value = result.handoffText; $('handoff').hidden = false; $('send').hidden = !B.canSend(); status('Draw and Think request prepared from revision ' + board.revision + '. No board has been created.');
    } catch (e) { status(e.message + ' No board was created.'); }
    finally { busy = false; $('draw').textContent = 'Prepare Draw and Think handoff'; $('draw').disabled = dirty || !board.storyboard_id; updateAssistant(); }
  }
  $('title').addEventListener('input', () => { board.title = $('title').value; changed(); });
  $('add').addEventListener('click', () => { if (board.shots.length >= 20) { status('Maximum 20 shots.'); return; } board.shots.push({ id: 'shot_' + uid().slice(0, 12), visual: '', duration_seconds: 5, narration: '' }); changed(); render(); $('shots').lastElementChild?.querySelector('textarea')?.focus(); });
  $('save').addEventListener('click', save); $('draw').addEventListener('click', prepare);
  $('open-editor').addEventListener('click', async () => { try { if (await B.expand()) { showMode(); $('title').focus(); } else { $('edit-here').hidden = false; status('This host cannot expand the storyboard. You can edit it here.'); } } catch (e) { $('edit-here').hidden = false; status(e.message + ' You can edit here.'); } });
  $('edit-here').addEventListener('click', () => { editHere = true; showMode(); $('title').focus(); });
  $('copy').addEventListener('click', async () => { try { await navigator.clipboard.writeText($('prompt').value); status('Prompt copied. Paste it into the conversation to request a Draw and Think board.'); } catch (_) { $('prompt').focus(); $('prompt').select(); status('Copy the selected prompt.'); } });
  $('send').addEventListener('click', async () => { if (!handoff || !$('prompt').value) return; $('send').disabled = true; $('send').textContent = 'Sending…'; try { await B.sendMessage($('prompt').value); status('Request sent to the conversation. Board creation awaits the assistant’s confirmed result.'); $('send').textContent = 'Sent'; } catch(e) { status(e.message + ' Send was not confirmed.'); $('send').textContent = 'Retry send'; $('send').disabled = false; } });
  $('assistant-update').addEventListener('click', async () => {
    if (busy || dirty || imports || !board.storyboard_id) { status('Save all changes before sending an update.'); return; }
    const id = board.storyboard_id, revision = board.revision;
    $('assistant-update').disabled = true;
    try {
      await B.sendMessage('Please review my saved video storyboard ' + id + ', revision ' + revision + '. Read it with read_video_storyboard and confirm the revision matches. Inspect each shot that includes a drawing or reference image with read_video_storyboard_media(storyboard_id="' + id + '", shot_id=<shot ID>, expected_revision=' + revision + '). Use the visuals and descriptions when giving feedback or continuing our collaboration. Do not replace a newer revision; tell me if the saved revision has changed.');
      status('Update sent to the assistant for saved revision ' + revision + '.');
    } catch(e) { status(e.message + ' Update send was not confirmed.'); }
    finally { updateAssistant(); }
  });
  function offerSaved(data) {
    pendingReload = data; $('reload').hidden = false;
    status('Saved revision ' + data.revision + ' is available. Your draft is preserved. Reload saved version explicitly replaces it.');
  }
  $('check-updates').addEventListener('click', async () => {
    if (busy || !board.storyboard_id) return;
    const id = board.storyboard_id; $('check-updates').disabled = true;
    try {
      const data = await B.callTool('read_video_storyboard', { storyboard_id: id, include_media: true });
      if (board.storyboard_id !== id) return;
      if (!data || data.storyboard_id !== id || !Number.isInteger(data.revision) || !Array.isArray(data.shots)) throw new Error('Saved storyboard could not be checked.');
      if (data.revision !== board.revision) offerSaved(data);
      else status('You have saved revision ' + data.revision + (dirty ? '. Your unsaved edits are preserved.' : '. No updates found.'));
    } catch(e) { status(e.message); }
    finally { updateAssistant(); }
  });
  $('reload').addEventListener('click', async () => {
    if (busy || imports || dragId) { status('Finish the current action before reloading.'); return; }
    const epoch = editEpoch, id = board.storyboard_id;
    busy = true; $('reload').disabled = true; $('save').disabled = true; updateAssistant();
    try {
      const data = id ? await B.callTool('read_video_storyboard', { storyboard_id: id, include_media: true }) : pendingReload;
      if (!data || (id && data.storyboard_id !== id) || !Number.isInteger(data.revision) || !Array.isArray(data.shots)) throw new Error('Saved storyboard could not be loaded.');
      if (editEpoch !== epoch || board.storyboard_id !== id || imports > 0) { offerSaved(data); status('You edited while loading. Your draft is preserved; reload again to replace it.'); return; }
      board = data; dirty = !data.storyboard_id; request = null; handoff = null; pendingReload = null; editEpoch++; importTokens.clear(); $('reload').hidden = true; $('handoff').hidden = true; render(); status(data.storyboard_id ? 'Loaded saved revision ' + data.revision + '.' : 'Loaded scaffold.');
    } catch (e) { status(e.message); }
    finally { busy = false; $('reload').disabled = false; $('save').disabled = imports > 0 || !dirty; updateAssistant(); }
  });
  B.onToolResult(result => { const data = result?.structuredContent || result?.result?.structuredContent; if (!data || !Array.isArray(data.shots) || typeof data.title !== 'string' || !Number.isInteger(data.revision) || initialLoaded) return; initialLoaded = true; if (editEpoch > 0) { pendingReload = data; $('reload').hidden = false; status('A storyboard loaded after you began editing. Your draft is preserved; use Reload saved version to replace it.'); return; } board = data; dirty = !data.storyboard_id; request = null; handoff = null; $('handoff').hidden = true; render(); status(data.storyboard_id ? 'Loaded saved revision ' + data.revision + '.' : 'Edit the scaffold, then save to create a storyboard.'); });
  B.onContext(() => { showMode(); updateAssistant(); });
  B.ready().then(() => { showMode(); updateAssistant(); if (!B.canTools()) status('This host cannot save or validate storyboard changes. You can still draft the cards here.'); });
  dirty = true; render(); showMode(); status('Open the editor to edit this scaffold, then save it.');
})();
