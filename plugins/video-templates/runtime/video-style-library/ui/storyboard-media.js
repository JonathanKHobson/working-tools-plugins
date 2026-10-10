(function () {
  'use strict';
  const LIMIT = 1024 * 1024;
  function clone(value) { return JSON.parse(JSON.stringify(value)); }
  function decodedBytes(url) { return Math.floor((url.split(',')[1] || '').length * 3 / 4) - (url.endsWith('==') ? 2 : url.endsWith('=') ? 1 : 0); }
  async function importImage(file) {
    if (!['image/png', 'image/jpeg', 'image/webp'].includes(file.type)) throw new Error('Choose a PNG, JPEG or WebP image.');
    if (file.size > 20 * LIMIT) throw new Error('Choose an image smaller than 20 MB.');
    const url = URL.createObjectURL(file), img = new Image();
    try {
      await new Promise((resolve, reject) => { img.onload = resolve; img.onerror = () => reject(new Error('This image could not be read.')); img.src = url; });
      if (!img.naturalWidth || !img.naturalHeight || img.naturalWidth * img.naturalHeight > 80000000) throw new Error('Choose an image with fewer than 80 million pixels.');
      let scale = Math.min(1, 1600 / Math.max(img.naturalWidth, img.naturalHeight));
      const canvas = document.createElement('canvas');
      for (let attempt = 0; attempt < 7; attempt++) {
        canvas.width = Math.max(1, Math.round(img.naturalWidth * scale)); canvas.height = Math.max(1, Math.round(img.naturalHeight * scale));
        const ctx = canvas.getContext('2d'); ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, canvas.width, canvas.height); ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        const data_url = canvas.toDataURL('image/jpeg', .82);
        if (decodedBytes(data_url) <= LIMIT) return { data_url, name: file.name.slice(0, 120), description: '' };
        scale *= .72;
      }
      throw new Error('This image could not be reduced below 1 MB.');
    } finally { URL.revokeObjectURL(url); }
  }
  function mount(container, shot, options) {
    const section = document.createElement('details'); section.className = 'shot-media'; section.open = !!(shot.sketch?.strokes?.length || shot.reference);
    const summary = document.createElement('summary'); summary.textContent = 'Sketch & reference'; section.append(summary);
    const hint = document.createElement('p'); hint.className = 'subtle'; hint.textContent = 'Sketch the framing. Describe the idea in Visual action so it is accessible.'; section.append(hint);
    const canvas = document.createElement('canvas'); canvas.width = 640; canvas.height = 360; canvas.className = 'sketch-pad'; canvas.setAttribute('aria-label', 'Shot sketch pad. Use Visual action to describe the sketch.'); section.append(canvas);
    const controls = document.createElement('div'); controls.className = 'media-actions';
    function button(label, fn) { const b = document.createElement('button'); b.type = 'button'; b.textContent = label; b.addEventListener('click', fn); controls.append(b); return b; }
    const ctx = canvas.getContext('2d'); let active = null, pointerId = null;
    function strokes() { return shot.sketch?.strokes || []; }
    function paint() { ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, 640, 360); ctx.strokeStyle = '#252525'; ctx.fillStyle = '#252525'; ctx.lineWidth = 3; ctx.lineCap = 'round'; ctx.lineJoin = 'round'; for (const stroke of strokes()) { const p = stroke.points; if (!p.length) continue; ctx.beginPath(); ctx.moveTo(p[0][0] * 640, p[0][1] * 360); if (p.length === 1) { ctx.arc(p[0][0] * 640, p[0][1] * 360, 1.5, 0, Math.PI * 2); ctx.fill(); } else { for (const [x,y] of p.slice(1)) ctx.lineTo(x * 640, y * 360); ctx.stroke(); } } undo.disabled = clear.disabled = !strokes().length; }
    const undo = button('Undo stroke', () => { if (active) return; strokes().pop(); options.changed(); paint(); });
    const clear = button('Clear sketch', () => { if (active) return; delete shot.sketch; options.changed(); paint(); });
    section.append(controls);
    function point(e) { const r = canvas.getBoundingClientRect(); return [Math.max(0, Math.min(1, (e.clientX-r.left)/r.width)), Math.max(0, Math.min(1, (e.clientY-r.top)/r.height))]; }
    canvas.addEventListener('pointerdown', e => { if (active || (e.pointerType === 'mouse' && e.button !== 0)) return; if (strokes().length >= 64) { options.status('Sketch limit reached (64 strokes). Undo or clear to continue.'); return; } e.preventDefault(); shot.sketch ||= { strokes: [] }; active = { points: [point(e)] }; shot.sketch.strokes.push(active); pointerId = e.pointerId; canvas.setPointerCapture(pointerId); options.changed(); paint(); });
    canvas.addEventListener('pointermove', e => { if (!active || e.pointerId !== pointerId) return; const p = point(e), last = active.points[active.points.length-1]; if (Math.hypot(p[0]-last[0], p[1]-last[1]) < .002) return; if (active.points.length < 512) active.points.push(p); else active.points[511] = p; options.changed(); paint(); });
    function end(e) { if (e.pointerId !== pointerId) return; active = null; pointerId = null; }
    canvas.addEventListener('pointerup', end); canvas.addEventListener('pointercancel', end); canvas.addEventListener('lostpointercapture', end);
    paint();
    const reference = document.createElement('div'); reference.className = 'reference';
    if (shot.reference) {
      const img = document.createElement('img'); img.src = shot.reference.data_url; img.alt = shot.reference.description || 'Reference image for this shot'; reference.append(img);
      const name = document.createElement('p'); name.className = 'subtle reference-name'; name.textContent = shot.reference.name || 'Reference image'; reference.append(name);
      const label = document.createElement('label'); label.textContent = 'Reference description'; const text = document.createElement('textarea'); text.rows = 2; text.maxLength = 2000; text.value = shot.reference.description || ''; text.addEventListener('input', () => { shot.reference.description = text.value; img.alt = text.value || 'Reference image for this shot'; options.changed(); }); label.append(text); reference.append(label);
      const remove = document.createElement('button'); remove.type = 'button'; remove.textContent = 'Remove image'; remove.addEventListener('click', () => options.removeReference(shot.id)); reference.append(remove);
    }
    const label = document.createElement('label'); label.className = 'image-upload'; label.textContent = shot.reference ? 'Replace reference image' : 'Attach reference image'; const file = document.createElement('input'); file.type = 'file'; file.accept = 'image/png,image/jpeg,image/webp'; file.addEventListener('change', () => { if (file.files[0]) options.importReference(shot.id, file.files[0]); }); label.append(file); reference.append(label);
    const note = document.createElement('p'); note.className = 'subtle'; note.textContent = 'One reference preview per shot · resized locally as JPEG on white to fit 1 MB. Your original file stays unchanged.'; reference.append(note); section.append(reference); container.append(section);
  }
  window.StoryboardMedia = { mount, importImage, clone, decodedBytes };
})();
