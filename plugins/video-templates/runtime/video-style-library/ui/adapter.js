(function () {
  'use strict';
  let data = {};
  try { data = JSON.parse(document.getElementById('library-data')?.textContent || '{}'); } catch (_) {}
  const items = Array.isArray(data.items) ? data.items : [];
  const text = (item, key) => typeof item?.[key] === 'string' ? item[key] : '';
  const chosen = new Map();
  let currentPreview = null;
  const isFamily = item => item?.kind === 'video-family';
  const familyExample = item => item.examples?.find(example => example.id === chosen.get(item.id)) ||
    item.examples?.find(example => example.id === item.defaultExampleId) || item.examples?.[0];
  const element = (tag, content, className) => {
    const node = document.createElement(tag);
    if (content !== undefined) node.textContent = content;
    if (className) node.className = className;
    return node;
  };
  const button = (label, action) => {
    const node = element('button', label);
    node.type = 'button';
    node.addEventListener('click', action);
    return node;
  };
  const field = (item, key) => Array.isArray(item?.facets?.[key]) ? item.facets[key] : [];
  const optionSet = (key, label) => ({
    id: key, label, type: 'select', default: 'all',
    options: [{ value: 'all', label: 'All ' + label.toLowerCase() }].concat(
      [...new Set(items.filter(isFamily).flatMap(item => field(item, key)))].sort().map(value => ({ value, label: value }))
    )
  });
  function addSection(host, label, content) {
    const section = element('section', undefined, 'detail-section');
    section.append(element('h3', label));
    if (typeof content === 'string') section.append(element('p', content));
    else section.append(content);
    host.append(section);
    return section;
  }
  function link(label, url) {
    const node = element('a', label);
    node.href = url; node.target = '_blank'; node.rel = 'noopener noreferrer';
    node.addEventListener('click', async event => {
      const bridge = window.LibraryBridge;
      if (!bridge?.canOpenLinks?.() || node.dataset.manual === 'true') return;
      event.preventDefault();
      try { await bridge.openLink(url); }
      catch {
        node.dataset.manual = 'true';
        node.textContent = label + ' · host declined; try opening again or copy link address';
      }
    });
    return node;
  }
  function reviewSummary(example) {
    const container = element('div', undefined, 'video-review');
    for (const kind of ['technical', 'creative', 'listening', 'reproduction']) {
      const record = example.review?.[kind];
      const state = typeof record === 'object' && record ? record.state : (record || 'unknown');
      const scope = typeof record === 'object' && record ? record.scope : '';
      const row = element('p');
      row.append(element('strong', kind[0].toUpperCase() + kind.slice(1) + ': '),
        document.createTextNode(String(state || 'unknown') + (scope ? ' · ' + scope : '')));
      container.append(row);
    }
    return container;
  }
  function dismissPreview() {
    if (!currentPreview) return;
    currentPreview.video.pause();
    currentPreview.dialog.close();
  }
  function playPreview(item, { origin, openDetails }) {
    dismissPreview();
    const example = familyExample(item);
    const dialog = element('dialog', undefined, 'video-preview-dialog');
    let restoreFocus = true;
    dialog.setAttribute('aria-label', `${item.name} · ${example.title} playback preview`);
    const header = element('div', undefined, 'video-preview-header');
    const heading = element('div');
    heading.append(element('strong', item.name), element('p', example.title));
    const close = button('Close player', dismissPreview);
    header.append(heading, close);
    const stage = element('div', undefined, 'video-preview-stage');
    const video = element('video');
    video.controls = true; video.playsInline = true; video.preload = 'metadata';
    video.src = example.previewVideo.url;
    if (example.poster?.url) video.poster = example.poster.url;
    video.setAttribute('aria-label', `${example.title} playback preview`);
    video.addEventListener('error', () => {
      video.remove();
      stage.append(element('p', 'This host could not play the preview. Open hosted film details to watch it.'));
    });
    stage.append(video);
    const footer = element('div', undefined, 'video-preview-footer');
    footer.append(element('p', example.previewVideo.label || 'Playback preview · original available in Video only'));
    footer.append(button('View details', () => { restoreFocus = false; dismissPreview(); openDetails(); }));
    if (example.detailUrl || item.detailUrl) footer.append(link('Open hosted film details ↗', example.detailUrl || item.detailUrl));
    dialog.append(header, stage, footer);
    dialog.addEventListener('close', () => {
      video.pause(); video.removeAttribute('src'); video.load();
      dialog.remove();
      if (currentPreview?.dialog === dialog) {
        currentPreview = null;
        if (restoreFocus && origin?.isConnected) origin.focus();
      }
    }, { once: true });
    document.body.append(dialog);
    currentPreview = { dialog, video };
    dialog.showModal();
    video.play().catch(() => {});
    close.focus();
  }
  function renderFamily(item, host) {
    let example = familyExample(item);
    const chooser = element('div', undefined, 'video-variant-selector');
    const label = element('label', 'Film / variant');
    const select = element('select');
    select.setAttribute('aria-label', 'Select film or variant');
    item.examples.forEach(entry => {
      const option = element('option', entry.title);
      option.value = entry.id;
      select.append(option);
    });
    select.value = example.id;
    label.append(select); chooser.append(label);
    chooser.append(element('p', example.relationship || `${item.examples.length} example${item.examples.length === 1 ? '' : 's'} in this family.`));
    host.append(chooser);
    select.addEventListener('change', () => {
      host.querySelectorAll('video').forEach(video => video.pause());
      chosen.set(item.id, select.value);
      host.replaceChildren();
      renderFamily(item, host);
      host.querySelector('select')?.focus();
    });

    example = familyExample(item);
    const media = [];
    const playback = example.previewVideo?.url ? example.previewVideo : example.master;
    if (playback?.url) media.push({ role: example.previewVideo?.url ? 'Playback preview' : 'Original video',
      label: example.previewVideo?.url ? (example.previewVideo.label || `${example.title} preview · original available in Video only`) : example.title,
      url: playback.url, type: 'video', poster: example.poster?.url });
    const galleryRoles = { 'encoded-contact-sheet': 'Final-film overview',
      'encoded-frame': 'Scene frame', 'process-reference': 'Process / reference',
      'planning': 'Process / reference' };
    for (const entry of example.gallery || []) {
      if (entry.url) media.push({ role: galleryRoles[entry.role] || entry.role || 'Scene frame', label: entry.label || 'Scene frame',
        url: entry.url, type: 'image' });
    }
    if (example.poster?.url) media.push({ role: 'Cover frame', label: example.title + ' poster',
      url: example.poster.url, type: 'image' });
    const gallery = element('div', undefined, 'video-gallery');
    const stage = element('div', undefined, 'video-stage');
    const status = element('p', '', 'video-gallery-status');
    let index = 0;
    function showMedia() {
      stage.querySelectorAll('video').forEach(video => video.pause());
      stage.replaceChildren();
      const entry = media[index];
      if (!entry) {
        stage.append(element('p', 'Inline media is unavailable for this example. Open its hosted details to inspect the film.'));
        status.textContent = 'No inline media';
        return;
      }
      if (entry.type === 'video') {
        const video = element('video');
        video.controls = true; video.playsInline = true; video.preload = 'metadata';
        video.src = entry.url;
        if (entry.poster) video.poster = entry.poster;
        video.setAttribute('aria-label', entry.label + ' video');
        video.addEventListener('error', () => {
          video.remove();
          const warning = element('p', 'This host could not play the film inline. Open hosted details to watch it.');
          warning.setAttribute('role', 'status'); stage.append(warning);
        });
        stage.append(video);
      } else {
        const image = element('img');
        image.src = entry.url; image.alt = entry.label;
        image.addEventListener('error', () => {
          image.remove();
          stage.append(element('p', 'This frame is unavailable here. Open hosted details to inspect the film.'));
        });
        image.loading = 'lazy'; stage.append(image);
      }
      status.textContent = `${index + 1} of ${media.length} · ${entry.role}: ${entry.label}`;
    }
    showMedia();
    gallery.append(stage);
    const nav = element('div', undefined, 'video-gallery-nav');
    const previous = button('← Previous media', () => { index = (index + media.length - 1) % media.length; showMedia(); });
    const next = button('Next media →', () => { index = (index + 1) % media.length; showMedia(); });
    previous.disabled = next.disabled = media.length < 2;
    nav.append(previous, status, next); gallery.append(nav);
    gallery.addEventListener('keydown', event => {
      if (event.target.matches('video,select')) return;
      if (event.key === 'ArrowLeft' && !previous.disabled) { event.preventDefault(); previous.click(); }
      if (event.key === 'ArrowRight' && !next.disabled) { event.preventDefault(); next.click(); }
    });
    host.append(gallery);
    const detailUrl = example.detailUrl || item.detailUrl;
    if (detailUrl) {
      const fallback = element('p', undefined, 'video-hosted-fallback');
      fallback.append(link('Open hosted film details ↗', detailUrl));
      host.append(fallback);
    }
    addSection(host, 'Visual direction', item.summary || 'No family summary supplied.');
    const facts = [
      example.producer && `Producer: ${example.producer}`,
      example.format && `Format: ${example.format}`,
      example.master?.duration && `Original duration: ${example.master.duration} seconds`,
      example.master?.encodedFps && `Original encoded frame rate: ${example.master.encodedFps} fps`,
      example.master?.sha256 && `Original SHA-256: ${example.master.sha256}`,
      example.previewVideo?.url && `Playback preview SHA-256: ${example.previewVideo.sha256 || 'unknown'}; derived from the original master`,
    ].filter(Boolean);
    if (item.usageGuidance || example.usageGuidance) addSection(host, 'Make this your own',
      [item.usageGuidance, example.usageGuidance].filter(Boolean).join('\n\n'));
    const prompt = example.starterPrompt || '';
    if (prompt) {
      const wrapper = element('div');
      const textarea = element('textarea');
      textarea.readOnly = true; textarea.value = prompt;
      textarea.setAttribute('aria-label', 'Starter prompt for ' + example.title);
      wrapper.append(textarea, button('Copy starter prompt', async event => {
        try { await navigator.clipboard.writeText(prompt); event.target.textContent = 'Copied'; }
        catch { textarea.focus(); textarea.select(); event.target.textContent = 'Select and copy prompt'; }
      }));
      addSection(host, 'Starter prompt · ' + example.title, wrapper);
    }
    addSection(host, 'Review evidence · ' + example.title, reviewSummary(example));
    const downloads = element('div', undefined, 'video-downloads');
    const labels = { bundle: 'Full style reproduction bundle', video: 'Video only', source: 'Source project', prompt: 'Starter prompt' };
    for (const [kind, name] of Object.entries(labels)) {
      const record = example.downloads?.[kind];
      const row = element(kind === 'bundle' ? 'div' : 'p');
      if (kind === 'bundle' && record?.available && record.url) {
        const contents = element('p');
        contents.append(element('strong', `Selected example: ${example.title}. `),
          document.createTextNode(`Includes ${record.includedFileCount} files: ${(record.includedFiles || []).join(', ')}.`));
        row.append(contents);
        if (record.externalPrerequisites?.length) row.append(element('p',
          `External prerequisites: ${record.externalPrerequisites.join(', ')}.`));
        if (record.license) row.append(element('p', `Rights: ${record.license}`));
        const action = element('p');
        action.append(link('Download full bundle ↗', record.url));
        row.append(action);
      } else if (record?.available && record.url) row.append(link(name + ' ↗', record.url));
      else row.append(element('span', name + ': ' + (record?.reason || 'Unavailable')));
      downloads.append(row);
    }
    addSection(host, 'Downloads · ' + example.title, downloads);
    if (facts.length) {
      const sourceFacts = element('details', undefined, 'detail-section video-source-facts');
      sourceFacts.append(element('summary', 'Media source and technical facts'), element('p', facts.join('\n')));
      host.append(sourceFacts);
    }
    return true;
  }
  window.LibraryAdapter = {
    title: 'Video Library', noun: 'style', labels: { search: 'Search video families and methods', plural: 'styles', back: 'Back to videos' },
    items,
    filters: [{ id: 'kind', label: 'Type', type: 'select', default: 'all',
      options: [{ value: 'all', label: 'All types' }, { value: 'video-family', label: 'Film families' },
        { value: 'staged-method', label: 'Staged reference methods' }] },
      optionSet('producer', 'Producer'), optionSet('format', 'Format'),
      optionSet('motion', 'Motion'), optionSet('material', 'Material'), optionSet('useCase', 'Use case')],
    searchText(item) {
      return [item.id, item.name, item.kind, item.summary, item.bestFor, item.motion,
        ...(item.examples || []).map(entry => [entry.title, entry.relationship, entry.producer].join(' ')),
        ...Object.values(item.facets || {}).flat()].join(' ');
    },
    matches(item, values) {
      return Object.keys(values || {}).every(key => values[key] === 'all' ||
        (key === 'kind' && item.kind === values[key]) ||
        (isFamily(item) ? field(item, key).includes(values[key]) :
          key === 'motion' && text(item, 'motion').toLowerCase().includes(values[key].toLowerCase())));
    },
    detailType(item) {
      return isFamily(item) ? `${item.examples.length} film example${item.examples.length === 1 ? '' : 's'} · Video family` :
        'Staged reference method · Full film and audio unverified';
    },
    preview(item) {
      if (isFamily(item)) {
        const example = familyExample(item), poster = example?.poster || {};
        const portrait = (poster.height || example?.master?.height || 0) > (poster.width || example?.master?.width || 0);
        return { image: poster.url || '', imageFit: portrait ? 'contain' : 'cover', blurFill: portrait,
          text: item.summary || item.name, meta: `${item.examples.length} film example${item.examples.length === 1 ? '' : 's'}` };
      }
      return { image: text(item, 'preview'), meta: 'Staged reference method' };
    },
    canPlayPreview(item) { return isFamily(item) && Boolean(familyExample(item)?.previewVideo?.url); },
    playPreview,
    renderDetail(item, host) { return isFamily(item) ? renderFamily(item, host) : false; },
    onViewChange(view) {
      if (view !== 'detail-view') document.querySelectorAll('#detail-content video').forEach(video => video.pause());
      if (view !== 'chooser') dismissPreview();
    },
    useLabel(item) { return isFamily(item) ? 'Make this your own' : 'Use method'; },
    details(item) {
      const sections = [
        { label: 'Sample frame', image: text(item, 'preview') },
        { label: 'Look', text: text(item, 'summary') },
        { label: 'Best for', text: text(item, 'bestFor') },
        { label: 'Motion', text: text(item, 'motion') },
        { label: 'Adoption state', text: text(item, 'status') },
        { label: 'Source and license', text: [item.sourceProject, item.sourceRevision, item.sourcePath, 'MIT license', 'SHA-256: ' + item.sourceHash].join('\n') }
      ];
      if (item.relatedFamilyIds?.length) sections.splice(1, 0, {
        label: 'Related film family', text: item.relatedFamilyIds.join(', ') + '. This staged method remains a separate reference record.'
      });
      return sections;
    },
    localPrompt(item, brief) {
      if (isFamily(item)) {
        const example = familyExample(item);
        return `Prepare a verified Video Library handoff for ${item.name}, example ${example.title}.\n` +
          `Family ID: ${item.id}\nExample ID: ${example.id}\nMaster SHA-256: ${example.master.sha256 || 'unknown'}\n` +
          `Brief: ${brief || '(not supplied)'}\n` +
          'Call prepare_video_style_handoff with this exact family ID, example ID, hash and brief. ' +
          'Inspect review, rights and source availability before adapting. A storyboard has not been created.';
      }
      return 'Prepare the selected Video Production Studio style and Draw and Think storyboard.\n' +
        'Style ID: ' + item.methodId + '\nSource revision: ' + item.sourceRevision + '\nSource hash: ' + item.sourceHash +
        '\nBrief: ' + (brief || '(not supplied)') + '\n' +
        'Call prepare_video_style_handoff with this exact ID, hash and brief to revalidate the staged source. ' +
        'Use its storyboard payload with draw_create_board and draw_open_board. No board exists yet.';
    },
    handoff: {
      tool: 'prepare_video_style_handoff',
      args(item, brief) {
        if (isFamily(item)) {
          const example = familyExample(item);
          return { style_id: item.id, example_id: example.id, source_hash: example.master.sha256, brief: brief || '' };
        }
        return { style_id: item.methodId, source_hash: item.sourceHash, brief: brief || '' };
      },
      text(payload, item) {
        const example = isFamily(item) ? familyExample(item) : null;
        const expectedId = isFamily(item) ? item.id : item.methodId;
        const expectedHash = example ? example.master.sha256 : item.sourceHash;
        if (!payload || payload.styleId !== expectedId || payload.sourceHash !== expectedHash ||
            payload.sourceRevision !== item.sourceRevision || (example && payload.exampleId !== example.id) ||
            typeof payload.handoffText !== 'string' || !payload.handoffText.trim()) {
          throw new Error('The video selection changed or its handoff was incomplete. Refresh this library.');
        }
        return payload.handoffText;
      }
    }
  };
})();
