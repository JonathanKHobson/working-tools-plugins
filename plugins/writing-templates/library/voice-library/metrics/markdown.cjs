'use strict';

const crypto = require('node:crypto');
const { loadMarked } = require('./parser.cjs');
const { words } = require('./text.cjs');
const hash = text => crypto.createHash('sha256').update(text, 'utf8').digest('hex');

function envelope(source) {
  const metadata = {}, errors = [], exclusions = [];
  let bodyStart = 0, bodyEnd = source.length;
  const frontmatter = source.match(/^\uFEFF?---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/u);
  if (frontmatter) {
    bodyStart = frontmatter[0].length;
    for (const line of frontmatter[1].split(/\r?\n/u)) {
      if (!line.trim() || /^\s*#/u.test(line)) continue;
      const match = line.match(/^([a-z_]+):\s*(.*?)\s*$/u);
      if (!match || Object.hasOwn(metadata, match[1])) { errors.push('unsupported_or_duplicate_frontmatter'); continue; }
      let value = match[2];
      if (/^['"]/u.test(value)) {
        if (value.at(-1) !== value[0]) { errors.push('invalid_frontmatter_quote'); continue; }
        value = value.slice(1, -1);
      } else value = value.replace(/\s+#.*$/u, '');
      if (/[\[\]{}]/u.test(value)) errors.push('frontmatter_requires_scalar_values');
      metadata[match[1]] = value;
    }
  }
  const starts = [...source.matchAll(/<!-- specimen:start -->/gu)], ends = [...source.matchAll(/<!-- specimen:end -->/gu)];
  if (starts.length || ends.length) {
    if (starts.length !== 1 || ends.length !== 1 || starts[0].index < bodyStart || ends[0].index <= starts[0].index) errors.push('invalid_specimen_markers');
    else { bodyStart = starts[0].index + starts[0][0].length; bodyEnd = ends[0].index; }
  }
  if (bodyStart) exclusions.push({ kind: 'wrapper', start: 0, end: bodyStart });
  if (bodyEnd < source.length) exclusions.push({ kind: 'wrapper', start: bodyEnd, end: source.length });
  return { metadata, errors, exclusions, body: source.slice(bodyStart, bodyEnd), bodyStart, hasMarkers: starts.length === 1 && ends.length === 1 };
}

async function extract(source, options = {}) {
  const env = envelope(source), metadata = { ...env.metadata, ...options.metadata };
  const channel = metadata.channel || 'markdown';
  const errors = [...env.errors], warnings = [], exclusions = [...env.exclusions], paragraphs = [];
  const nodeCounts = { headings: 0, list_items: 0, blockquotes: 0, code_blocks: 0, tables: 0 };
  let parserVersion = null, parserResolution = null;
  const exclude = (kind, start, end) => exclusions.push({ kind, start, end, text_sha256: hash(source.slice(start, end)), source_characters: end - start });
  // Marked normalizes CRLF/CR in token.raw; recover the exact original span.
  const locate = (raw, cursor) => {
    const pattern = raw.split('\n').map(line => line.replace(/[.*+?^${}()|[\]\\]/gu, '\\$&')).join('(?:\\r\\n|\\r|\\n)');
    const match = new RegExp(pattern, 'u').exec(source.slice(cursor));
    if (!match) { errors.push('unmapped_source_span'); return [cursor, cursor]; }
    const start = cursor + match.index;
    return [start, start + match[0].length];
  };
  function inline(tokens, origin, emphasized = false) {
    const parts = [];
    let cursor = origin;
    for (const token of tokens || []) {
      const [start, end] = locate(token.raw, cursor);
      cursor = end;
      if (token.type === 'strong' || token.type === 'em') {
        const marker = token.type === 'strong' ? 2 : 1;
        parts.push(...inline(token.tokens, start + marker, true));
      } else if (token.type === 'link') {
        if (/^(?:https?:\/\/|www\.)/iu.test(token.text)) { exclude('url', start, end); parts.push({ text: ' ', emphasized: false }); }
        else {
          parts.push(...inline(token.tokens, start + (token.raw.startsWith('[') ? 1 : 0), emphasized));
          const destination = token.raw.lastIndexOf('](');
          if (destination >= 0) exclude('link_destination', locate(token.raw.slice(0, destination + 2), start)[1], end - 1);
        }
      } else if (token.type === 'text' || token.type === 'escape') {
        if (token.tokens) parts.push(...inline(token.tokens, start, emphasized));
        else parts.push({ text: token.text.replace(/&(?:[a-z][a-z0-9]+|#\d+|#x[0-9a-f]+);/giu, entity => {
          const named = { '&amp;': '&', '&lt;': '<', '&gt;': '>', '&quot;': '"', '&apos;': "'" };
          if (named[entity]) return named[entity];
          if (!entity.startsWith('&#')) { errors.push('unsupported_named_html_entity'); return ' '; }
          const value = /^&#x/iu.test(entity) ? parseInt(entity.slice(3, -1), 16) : parseInt(entity.slice(2, -1), 10);
          return value > 0 && value <= 0x10ffff ? String.fromCodePoint(value) : '\uFFFD';
        }), emphasized, source_start: start, source_end: end });
      } else if (token.type === 'br') parts.push({ text: '\n', emphasized: false });
      else if (['codespan', 'image'].includes(token.type)) { exclude(token.type, start, end); parts.push({ text: ' ', emphasized: false }); }
      else if (token.type === 'html' && /^<!--(?:(?!-->)[\s\S])*-->$/u.test(token.raw)) { exclude('comment', start, end); parts.push({ text: ' ', emphasized: false }); }
      else { errors.push(`unsupported_inline_${token.type}`); exclude('unsupported_markup', start, end); }
    }
    return parts;
  }
  if (!['markdown', 'plain_text'].includes(channel)) errors.push('unsupported_channel');
  if (channel === 'plain_text') {
    let cursor = env.bodyStart;
    for (const raw of env.body.split(/\r?\n\s*\r?\n/u)) {
      const start = source.indexOf(raw, cursor); cursor = start + raw.length;
      if (words(raw).length) paragraphs.push({ start, end: cursor, parts: [{ text: raw, emphasized: false, source_start: start, source_end: cursor }] });
    }
  } else {
    const { marked, version, resolution } = await loadMarked();
    parserVersion = version; parserResolution = resolution;
    const tokens = marked.lexer(env.body, { gfm: true });
    let cursor = env.bodyStart, bibliographyDepth = null, excludedSection = null;
    for (const token of tokens) {
      const [start, end] = locate(token.raw, cursor); cursor = end;
      const exclusionStart = token.type === 'html' && token.raw.trim().match(/^<!-- metrics:exclude:start kind=(boilerplate|copied_quote) -->$/u);
      const exclusionEnd = token.type === 'html' && token.raw.trim() === '<!-- metrics:exclude:end -->';
      if (exclusionStart) {
        if (excludedSection) errors.push('nested_explicit_exclusion');
        excludedSection = exclusionStart[1]; exclude('exclusion_marker', start, end); continue;
      }
      if (exclusionEnd) {
        if (!excludedSection) errors.push('unmatched_explicit_exclusion_end');
        excludedSection = null; exclude('exclusion_marker', start, end); continue;
      }
      if (excludedSection) { exclude(excludedSection, start, end); continue; }
      if (token.type === 'heading') {
        nodeCounts.headings++;
        if (bibliographyDepth !== null && token.depth <= bibliographyDepth) bibliographyDepth = null;
        if (/^(?:references|bibliography|works cited)$/iu.test(token.text.trim())) bibliographyDepth = token.depth;
        exclude('heading', start, end); continue;
      }
      if (bibliographyDepth !== null) { exclude('bibliography', start, end); continue; }
      if (token.type === 'paragraph') {
        const parts = inline(token.tokens, start);
        if (words(parts.map(p => p.text).join('')).length) paragraphs.push({ start, end, parts });
      } else if (token.type === 'space' || token.type === 'hr' || token.type === 'def') {
        if (token.type === 'def') exclude('link_definition', start, end);
      } else if (['blockquote', 'code', 'list', 'table'].includes(token.type)) {
        const key = { blockquote: 'blockquotes', code: 'code_blocks', list: 'list_items', table: 'tables' }[token.type];
        nodeCounts[key] += token.type === 'list' ? token.items.length : 1;
        exclude(token.type, start, end);
      } else if (token.type === 'html' && /^\s*<!--(?:(?!-->)[\s\S])*-->\s*$/u.test(token.raw)) exclude('comment', start, end);
      else { errors.push(`unsupported_block_${token.type}`); exclude('unsupported_markup', start, end); }
    }
    if (excludedSection) errors.push('unclosed_explicit_exclusion');
    if (nodeCounts.headings || nodeCounts.list_items || nodeCounts.tables) warnings.push('layout_nodes_excluded_from_prose');
    if (nodeCounts.blockquotes) warnings.push('blockquotes_assumed_copied_source');
  }
  return { ...env, metadata, channel, errors: [...new Set(errors)], warnings, exclusions, paragraphs, nodeCounts, parserVersion, parserResolution };
}
module.exports = { envelope, extract, hash };
