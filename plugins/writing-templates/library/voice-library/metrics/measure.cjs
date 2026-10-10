'use strict';

const { extract, hash, envelope } = require('./markdown.cjs');
const { words, sentences, mattr, balancedWindows, median, CONTRACTIONS, READER } = require('./text.cjs');
const { FEATURE_IDS, UNITS, EXTRACTOR_VERSION, SCHEMA_VERSION, POLICY_VERSION, SENTENCE_VERSION, CONTRACTION_VERSION } = require('./constants.cjs');

async function measure(source, options = {}) {
  if (typeof source !== 'string') throw new TypeError('source must be a UTF-8 string');
  const extracted = await extract(source, options);
  const warnings = [...extracted.warnings];
  const errors = [...extracted.errors];
  const language = extracted.metadata.language || 'en';
  if (!/^en(?:-[A-Za-z]{2,8})*$/u.test(language)) errors.push('unsupported_language');
  if (!extracted.metadata.language) warnings.push('language_assumed_en');
  if (!extracted.metadata.channel) warnings.push('channel_assumed_markdown');
  const tokens = [], sentenceRows = [], paragraphRows = [], emphasisSpans = [];
  let emphasizedWords = 0;
  for (const paragraph of extracted.paragraphs) {
    let text = '', emphasisRanges = [];
    for (const part of paragraph.parts) {
      if (part.emphasized) emphasisRanges.push([text.length, text.length + part.text.length]);
      text += part.text;
    }
    if (/[^\p{Script=Latin}\p{M}\p{N}\p{P}\p{S}\p{Z}\p{C}]/u.test(text)) errors.push('non_latin_prose_requires_language_review');
    const paragraphWords = words(text);
    for (const token of paragraphWords) {
      token.emphasized = emphasisRanges.some(([start, end]) => token.start < end && token.end > start);
      if (token.emphasized) emphasizedWords++;
    }
    tokens.push(...paragraphWords.map(token => token.word));
    const row = { source_start: paragraph.start, source_end: paragraph.end, analysis_text: text, eligible_words: paragraphWords.length };
    paragraphRows.push(row);
    for (const sentence of sentences(text)) sentenceRows.push({ ...sentence, paragraph_index: paragraphRows.length - 1 });
    for (const [start, end] of emphasisRanges) emphasisSpans.push({ paragraph_index: paragraphRows.length - 1, analysis_start: start, analysis_end: end, text: text.slice(start, end) });
  }
  const N = tokens.length, S = sentenceRows.length, P = paragraphRows.length;
  const questionSentences = sentenceRows.filter(row => row.question).length;
  const readerCount = tokens.filter(token => READER.has(token)).length;
  const contractionCount = tokens.filter(token => CONTRACTIONS.has(token)).length;
  const ambiguousApostrophes = tokens.filter(token => /'(?:s|d)$/u.test(token) && token !== "let's");
  if (ambiguousApostrophes.length) warnings.push('ambiguous_s_d_apostrophes_excluded_from_contractions');
  if (N < 50) warnings.push('insufficient_text_for_full_fingerprint');
  if (S < 10) warnings.push('sparse_sentence_statistics');
  if (P < 3) warnings.push('sparse_paragraph_statistics');
  warnings.push('english_rules_do_not_detect_all_mixed_language_or_copied_inline_quotations');
  const mean = S ? sentenceRows.reduce((sum, row) => sum + row.words, 0) / S : null;
  const sd = S ? Math.sqrt(sentenceRows.reduce((sum, row) => sum + (row.words - mean) ** 2, 0) / S) : null;
  const vocabulary = Object.fromEntries([25, 50, 100].map(window => [window, mattr(tokens, window)]));
  const raw = [mean, S >= 10 && mean ? sd / mean : null, vocabulary[50].value, N ? 1000 * readerCount / N : null, N ? 1000 * contractionCount / N : null, S ? 100 * questionSentences / S : null, P >= 3 ? median(paragraphRows.map(row => row.eligible_words)) : null, N ? 100 * emphasizedWords / N : null];
  const reasons = [S ? null : 'no_prose_sentences', S >= 10 ? null : 'requires_10_prose_sentences', vocabulary[50].reason, N ? null : 'no_eligible_words', N ? null : 'no_eligible_words', S ? null : 'no_prose_sentences', P >= 3 ? null : 'requires_3_prose_paragraphs', N ? null : 'no_eligible_words'];
  // Plain text without an explicit authoring-channel declaration cannot establish absent emphasis.
  if (extracted.channel === 'plain_text' && extracted.metadata.emphasis_known !== 'true') { raw[7] = null; reasons[7] = 'plain_text_emphasis_unknown'; }
  const uniqueErrors = [...new Set(errors)];
  const numerators = [sentenceRows.reduce((sum, row) => sum + row.words, 0), sd, null, readerCount, contractionCount, questionSentences, null, emphasizedWords];
  const denominators = [S, mean, null, N, N, S, P, N];
  const sourceHash = hash(source);
  const features = FEATURE_IDS.map((feature_id, index) => ({
    feature_id, raw_value: uniqueErrors.length ? null : raw[index], unit: UNITS[index],
    numerator: numerators[index], denominator: denominators[index],
    status: uniqueErrors.length ? 'unsupported' : raw[index] === null ? 'insufficient_sample' : 'measured',
    reason: uniqueErrors.length ? uniqueErrors.join(';') : reasons[index],
    eligible_word_count: N, eligible_sentence_count: S, eligible_paragraph_count: P,
    extractor_version: EXTRACTOR_VERSION, text_sha256: sourceHash, exclusion_policy: POLICY_VERSION,
    cohort_version: null, display_percentile: null, warnings: [...new Set(warnings)],
    evidence_spans: feature_id === 'F08' ? emphasisSpans : paragraphRows.map(({ source_start, source_end }) => ({ source_start, source_end })),
  }));
  if (uniqueErrors.length) for (const value of Object.values(vocabulary)) { value.value = null; value.reason = uniqueErrors.join(';'); }
  const balanced = balancedWindows(tokens);
  if (uniqueErrors.length) { balanced.value = null; balanced.reason = uniqueErrors.join(';'); }
  return {
    schema_version: SCHEMA_VERSION, extractor_version: EXTRACTOR_VERSION,
    runtime: { node: process.version, icu: process.versions.icu, marked: extracted.parserVersion, parser_resolution: extracted.parserResolution },
    sentence_rules: SENTENCE_VERSION, contraction_lexicon: CONTRACTION_VERSION,
    text_sha256: sourceHash, specimen_sha256: hash(extracted.body),
    source_utf8_bytes: Buffer.byteLength(source, 'utf8'), metadata: extracted.metadata, language, channel: extracted.channel,
    extraction_status: uniqueErrors.length ? 'unsupported' : 'complete', errors: uniqueErrors,
    full_fingerprint_eligible: !uniqueErrors.length && features.every(feature => feature.raw_value !== null) && N >= 50,
    counts: { eligible_words: N, prose_sentences: S, prose_paragraphs: P, reader_address_events: readerCount, contraction_events: contractionCount, ambiguous_apostrophe_events: ambiguousApostrophes.length, question_sentences: questionSentences, emphasized_word_union: emphasizedWords, ...extracted.nodeCounts },
    features, vocabulary_sensitivity: { mattr: vocabulary, balanced_nonoverlap50: balanced },
    diagnostics: { sentence_word_counts: sentenceRows.map(row => row.words), population_sentence_sd: sd, paragraph_word_counts: paragraphRows.map(row => row.eligible_words), lexical_types: new Set(tokens).size },
    evidence: { paragraphs: paragraphRows, sentences: sentenceRows, emphasis: emphasisSpans, ambiguous_apostrophe_forms: [...new Set(ambiguousApostrophes)].sort() },
    exclusions: extracted.exclusions.map(span => ({ ...span, source_characters: span.end - span.start, text_sha256: span.text_sha256 || hash(source.slice(span.start, span.end)) })),
    warnings: [...new Set(warnings)],
    distinctiveness: { status: 'uncalibrated', value: null, sample_count: 0, reason: 'raw_measurement_is_not_a_validated_distinctiveness_or_quality_score' },
    communication_ratings: { status: 'not_rated', reason: 'requires_separate_evidence_based_editorial_review' },
  };
}
function validateMeasurement(result, source) {
  const reasons = [];
  if (result.extractor_version !== EXTRACTOR_VERSION || result.schema_version !== SCHEMA_VERSION || result.sentence_rules !== SENTENCE_VERSION || result.contraction_lexicon !== CONTRACTION_VERSION) reasons.push('stale_measurement_version');
  if (result.text_sha256 !== hash(source) || result.specimen_sha256 !== hash(envelope(source).body)) reasons.push('stale_sample_hash');
  return { status: reasons.length ? 'stale' : 'current', reasons };
}
module.exports = { measure, validateMeasurement };
