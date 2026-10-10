'use strict';

const normalize = text => text.normalize('NFC').replace(/[\u2018\u2019\u02bc]/gu, "'").toLowerCase();
// Linguistic word forms: Unicode letters/marks, optional internal apostrophes.
// Hyphens separate words; digit strings, emoji and URLs are not word tokens.
function words(text) {
  return [...text.matchAll(/\p{L}[\p{L}\p{M}]*(?:['\u2018\u2019\u02bc][\p{L}\p{M}]+)*/gu)]
    .map(match => ({ word: normalize(match[0]), text: match[0], start: match.index, end: match.index + match[0].length }));
}

const CONTRACTIONS = new Set([
  "ain't", "aren't", "can't", "couldn't", "daren't", "didn't", "doesn't", "don't", "hadn't", "hasn't", "haven't", "isn't", "mayn't", "mightn't", "mustn't", "needn't", "oughtn't", "shan't", "shouldn't", "wasn't", "weren't", "won't", "wouldn't",
  "i'm", "i've", "i'll", "you're", "you've", "you'll", "we're", "we've", "we'll", "they're", "they've", "they'll", "he'll", "she'll", "it'll", "that'll", "there'll", "who'll", "what'll", "where'll", "when'll", "how'll", "who've", "what've", "should've", "could've", "would've", "might've", "must've", "let's",
]);
const READER = new Set(['you', 'your', 'yours', 'yourself', 'yourselves']);

function sentences(text) {
  const protectedPeriods = new Set();
  const protect = regex => {
    for (const match of text.matchAll(regex)) for (let i = 0; i < match[0].length; i++) if (match[0][i] === '.') protectedPeriods.add(match.index + i);
  };
  protect(/\b(?:Mr|Mrs|Ms|Dr|Prof|Sr|Jr|St|vs|etc)\./giu);
  protect(/\b(?:e\.g\.|i\.e\.|a\.m\.|p\.m\.)/giu);
  protect(/\b(?:[A-Za-z]\.){2,}/gu);
  protect(/\b[A-Z]\.(?=\s+[A-Z][a-z])/gu);
  protect(/\d\.\d/gu);
  const result = [];
  let start = 0;
  const push = end => {
    const fragment = text.slice(start, end);
    const tokens = words(fragment);
    if (tokens.length) result.push({ text: fragment.trim(), start, end, words: tokens.length, question: fragment.includes('?') });
    start = end;
  };
  for (let i = 0; i < text.length; i++) {
    if (!/[.!?]/u.test(text[i]) || protectedPeriods.has(i)) continue;
    let end = i + 1;
    while (end < text.length && /[.!?"'\u2019\u201d)\]]/u.test(text[end])) end++;
    if (end === text.length || /\s/u.test(text[end])) { push(end); i = end - 1; }
  }
  push(text.length);
  return result;
}

function mattr(tokens, window) {
  if (tokens.length < window) return { value: null, window, windows: 0, reason: `requires_${window}_words` };
  const counts = new Map();
  let sum = 0;
  for (let i = 0; i < tokens.length; i++) {
    counts.set(tokens[i], (counts.get(tokens[i]) || 0) + 1);
    if (i >= window) {
      const old = tokens[i - window], remaining = counts.get(old) - 1;
      if (remaining) counts.set(old, remaining); else counts.delete(old);
    }
    if (i >= window - 1) sum += counts.size / window;
  }
  return { value: sum / (tokens.length - window + 1), window, windows: tokens.length - window + 1, reason: null };
}

function balancedWindows(tokens, window = 50) {
  // Nonoverlapping full windows from both ends, averaged by direction.
  // This is a sensitivity diagnostic, not another public feature.
  if (tokens.length < window) return { value: null, window, reason: `requires_${window}_words`, windows_per_direction: 0 };
  const sample = offset => {
    const values = [];
    for (let i = offset; i + window <= tokens.length; i += window) values.push(new Set(tokens.slice(i, i + window)).size / window);
    return values.reduce((a, b) => a + b, 0) / values.length;
  };
  return { value: (sample(0) + sample(tokens.length % window)) / 2, window, reason: null, windows_per_direction: Math.floor(tokens.length / window) };
}
const median = values => {
  if (!values.length) return null;
  const sorted = [...values].sort((a, b) => a - b), mid = Math.floor(sorted.length / 2);
  return sorted.length % 2 ? sorted[mid] : (sorted[mid - 1] + sorted[mid]) / 2;
};
module.exports = { normalize, words, sentences, mattr, balancedWindows, median, CONTRACTIONS, READER };
