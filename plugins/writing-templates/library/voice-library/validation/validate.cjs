#!/usr/bin/env node
'use strict';

const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const { TextDecoder } = require('node:util');
const metricsDir = fs.existsSync(path.join(__dirname, 'metrics', 'measure.cjs'))
  ? path.join(__dirname, 'metrics') : path.join(__dirname, '..', 'metrics');
let FEATURE_IDS, UNITS, EXTRACTOR_VERSION, measure;
try {
  ({ FEATURE_IDS, UNITS, EXTRACTOR_VERSION } = require(path.join(metricsDir, 'constants.cjs')));
  ({ measure } = require(path.join(metricsDir, 'measure.cjs')));
} catch (error) {
  if (require.main === module) {
    process.stderr.write(`voice validation: measurement engine unavailable: ${error.message}\n`);
    process.exit(2);
  }
  throw error;
}

const SHA = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const FEATURE_UNIT = Object.fromEntries(FEATURE_IDS.map((id, i) => [id, UNITS[i]]));
const keys = (value, allowed, label) => {
  if (!value || typeof value !== 'object' || Array.isArray(value)) throw new Error(`${label} must be an object`);
  for (const key of Object.keys(value)) if (!allowed.includes(key)) throw new Error(`${label} has unknown field ${key}`);
};
const nonempty = (value, label) => {
  if (typeof value !== 'string' || !value.trim()) throw new Error(`${label} must be a nonempty string`);
};
const finite = (value, label) => {
  if (typeof value !== 'number' || !Number.isFinite(value)) throw new Error(`${label} must be a finite number`);
};
const array = (value, label) => { if (!Array.isArray(value)) throw new Error(`${label} must be an array`); };
const range = (value, label, low = 0, high = Infinity) => {
  if (!Array.isArray(value) || value.length !== 2) throw new Error(`${label} must be [min,max]`);
  value.forEach((n, i) => finite(n, `${label}[${i}]`));
  if (value[0] < low || value[1] > high || value[0] > value[1]) throw new Error(`${label} has invalid bounds`);
};
function featureBound(row, label) {
  keys(row, ['featureId', 'min', 'max', 'source', 'reason'], label);
  if (!FEATURE_IDS.includes(row.featureId)) throw new Error(`${label} has unknown featureId`);
  if (!Object.hasOwn(row, 'min') && !Object.hasOwn(row, 'max')) throw new Error(`${label} needs min or max`);
  if (Object.hasOwn(row, 'min')) finite(row.min, `${label}.min`);
  if (Object.hasOwn(row, 'max')) finite(row.max, `${label}.max`);
  if ((row.min ?? -Infinity) > (row.max ?? Infinity)) throw new Error(`${label} has invalid bounds`);
  if (row.min !== undefined && row.min < 0) throw new Error(`${label}.min cannot be negative`);
  if (row.max !== undefined && row.max < 0) throw new Error(`${label}.max cannot be negative`);
  nonempty(row.source, `${label}.source`);
  nonempty(row.reason, `${label}.reason`);
  const ceiling = { F03: 1, F04: 1000, F05: 1000, F06: 100, F08: 100 }[row.featureId];
  if (ceiling !== undefined && (row.min !== undefined && row.min > ceiling || row.max !== undefined && row.max > ceiling)) throw new Error(`${label} exceeds ${row.featureId} unit bounds`);
}
function uniqueIds(rows, name, key) {
  const seen = new Set();
  for (const row of rows) {
    if (seen.has(row[key])) throw new Error(`${name} contains duplicate ${row[key]}`);
    seen.add(row[key]);
  }
}
function validateProfile(profile) {
  keys(profile, ['schema', 'resourceId', 'name', 'route', 'extractorVersion', 'observedFeatures', 'toneTargets', 'manualChecks', 'hardConstraints', 'incidentOverride', 'observedBasis'], 'profile');
  if (profile.schema !== 'wvl-qa-profile/1') throw new Error('unsupported profile schema');
  ['resourceId', 'name'].forEach(field => nonempty(profile[field], `profile.${field}`));
  if (!/^[VP]\d{2}$/u.test(profile.resourceId)) throw new Error('profile.resourceId must be a Vnn or Pnn ID');
  keys(profile.route, ['selected_resource_id', 'base_profile_id', 'module_ids'], 'profile.route');
  nonempty(profile.route.selected_resource_id, 'profile.route.selected_resource_id');
  nonempty(profile.route.base_profile_id, 'profile.route.base_profile_id');
  if (profile.route.selected_resource_id !== profile.resourceId) throw new Error('profile route selected_resource_id mismatch');
  if (!/^[VP]\d{2}$/u.test(profile.route.base_profile_id)) throw new Error('profile route base_profile_id must be a Vnn or Pnn ID');
  array(profile.route.module_ids, 'profile.route.module_ids');
  profile.route.module_ids.forEach((id, i) => { if (typeof id !== 'string' || !/^P\d{2}$/u.test(id)) throw new Error(`profile.route.module_ids[${i}] must be a Pnn ID`); });
  uniqueIds(profile.route.module_ids.map(id => ({ id })), 'route.module_ids', 'id');
  if (profile.extractorVersion !== EXTRACTOR_VERSION) throw new Error('profile extractorVersion mismatch');
  array(profile.observedFeatures, 'profile.observedFeatures');
  for (const [i, row] of profile.observedFeatures.entries()) {
    const label = `observedFeatures[${i}]`;
    keys(row, ['featureId', 'unit', 'min', 'median', 'max', 'n'], label);
    if (!FEATURE_IDS.includes(row.featureId) || row.unit !== FEATURE_UNIT[row.featureId]) throw new Error(`${label} featureId or unit mismatch`);
    if (!Number.isSafeInteger(row.n) || row.n < 0) throw new Error(`${label}.n must be a nonnegative integer`);
    if (row.n === 0) {
      if (row.min !== null || row.median !== null || row.max !== null) throw new Error(`${label} zero observations require null statistics`);
    } else {
      ['min', 'median', 'max'].forEach(field => finite(row[field], `${label}.${field}`));
      if (row.min < 0 || row.min > row.median || row.median > row.max) throw new Error(`${label} has invalid range`);
      const ceiling = { F03: 1, F04: 1000, F05: 1000, F06: 100, F08: 100 }[row.featureId];
      if (ceiling !== undefined && row.max > ceiling) throw new Error(`${label} exceeds ${row.featureId} unit bounds`);
    }
  }
  uniqueIds(profile.observedFeatures, 'observedFeatures', 'featureId');
  array(profile.toneTargets, 'profile.toneTargets');
  for (const [i, row] of profile.toneTargets.entries()) {
    const label = `toneTargets[${i}]`;
    keys(row, ['dimension', 'range', 'task', 'kind', 'rubric', 'rationale'], label);
    nonempty(row.dimension, `${label}.dimension`);
    range(row.range, `${label}.range`, 1, 5);
    nonempty(row.task, `${label}.task`);
    if (row.kind !== undefined && row.kind !== 'editorial_target') throw new Error(`${label}.kind must be editorial_target`);
    if (row.rubric !== undefined) nonempty(row.rubric, `${label}.rubric`);
    if (row.rationale !== undefined) nonempty(row.rationale, `${label}.rationale`);
  }
  uniqueIds(profile.toneTargets, 'toneTargets', 'dimension');
  array(profile.manualChecks, 'profile.manualChecks');
  for (const [i, row] of profile.manualChecks.entries()) {
    keys(row, ['id', 'label', 'source'], `manualChecks[${i}]`);
    ['id', 'label', 'source'].forEach(field => nonempty(row[field], `manualChecks[${i}].${field}`));
  }
  uniqueIds(profile.manualChecks, 'manualChecks', 'id');
  if (profile.hardConstraints !== undefined) {
    array(profile.hardConstraints, 'profile.hardConstraints');
    profile.hardConstraints.forEach((row, i) => featureBound(row, `hardConstraints[${i}]`));
  }
  if (profile.incidentOverride !== undefined) {
    keys(profile.incidentOverride, ['humor', 'enthusiasm', 'persuasive_intent'], 'incidentOverride');
    for (const [dimension, bounds] of Object.entries(profile.incidentOverride)) range(bounds, `incidentOverride.${dimension}`, 1, 5);
  }
  if (profile.observedBasis !== undefined) {
    const basis = profile.observedBasis;
    keys(basis, ['status', 'sampleIds', 'sourceHashes', 'note'], 'observedBasis');
    if (basis.status !== 'descriptive_only_not_acceptance_limits') throw new Error('observedBasis status mismatch');
    array(basis.sampleIds, 'observedBasis.sampleIds');
    basis.sampleIds.forEach((id, i) => nonempty(id, `observedBasis.sampleIds[${i}]`));
    uniqueIds(basis.sampleIds.map(id => ({ id })), 'observedBasis.sampleIds', 'id');
    keys(basis.sourceHashes, basis.sampleIds, 'observedBasis.sourceHashes');
    for (const id of basis.sampleIds) if (!/^[a-f0-9]{64}$/u.test(basis.sourceHashes[id] || '')) throw new Error(`observedBasis source hash invalid for ${id}`);
    nonempty(basis.note, 'observedBasis.note');
  }
  return profile;
}
function validateConstraints(constraints, resourceId) {
  if (!constraints) return { features: [], requiredSpans: [] };
  keys(constraints, ['schema', 'resourceId', 'features', 'requiredSpans'], 'constraints');
  if (constraints.schema !== 'wvl-task-constraints/1' || constraints.resourceId !== resourceId) throw new Error('constraints schema or resourceId mismatch');
  array(constraints.features, 'constraints.features');
  array(constraints.requiredSpans, 'constraints.requiredSpans');
  constraints.features.forEach((row, i) => featureBound(row, `constraints.features[${i}]`));
  for (const span of constraints.requiredSpans) nonempty(span, 'requiredSpan');
  return constraints;
}
function validateRatings(ratings, resourceId, sourceHash) {
  if (!ratings) return null;
  keys(ratings, ['schema', 'resourceId', 'sourceHash', 'provenance', 'ratings'], 'ratings');
  if (ratings.schema !== 'wvl-editorial-ratings/1' || ratings.resourceId !== resourceId) throw new Error('ratings schema or resourceId mismatch');
  if (ratings.sourceHash !== sourceHash) throw new Error('ratings sourceHash does not match input');
  if (!['model_estimate', 'human_review'].includes(ratings.provenance)) throw new Error('ratings provenance must be model_estimate or human_review');
  array(ratings.ratings, 'ratings.ratings');
  for (const [i, row] of ratings.ratings.entries()) {
    const label = `ratings[${i}]`;
    keys(row, ['dimension', 'value', 'evidence', 'rationale'], label);
    nonempty(row.dimension, `${label}.dimension`);
    if (row.value !== null && (!Number.isInteger(row.value) || row.value < 1 || row.value > 5)) throw new Error(`${label}.value must be 1..5 or null`);
    array(row.evidence, `${label}.evidence`);
    row.evidence.forEach((quote, j) => nonempty(quote, `${label}.evidence[${j}]`));
    if (typeof row.rationale !== 'string') throw new Error(`${label}.rationale must be a string`);
  }
  uniqueIds(ratings.ratings, 'ratings', 'dimension');
  return ratings;
}
function mergeBounds(profile, constraints) {
  const merged = new Map();
  for (const row of [...(profile.hardConstraints || []), ...constraints.features]) {
    const old = merged.get(row.featureId) || { min: -Infinity, max: Infinity, sources: [], reasons: [] };
    const next = { min: Math.max(old.min, row.min ?? -Infinity), max: Math.min(old.max, row.max ?? Infinity),
      sources: [...old.sources, row.source], reasons: [...old.reasons, row.reason] };
    if (next.min > next.max) throw new Error(`constraints conflict for ${row.featureId}`);
    merged.set(row.featureId, next);
  }
  return merged;
}
function evidenceRanges(source, measurement, purpose) {
  const blocked = new Set(['wrapper', 'comment', 'link_destination', 'exclusion_marker', 'boilerplate']);
  if (purpose === 'tone') for (const kind of ['copied_quote', 'blockquote', 'code', 'codespan', 'link_definition', 'bibliography']) blocked.add(kind);
  const ranges = measurement.exclusions.filter(row => blocked.has(row.kind)).map(row => [row.start, row.end]);
  // The plain-text channel has no Markdown parser, so comments need an independent mask.
  for (const match of source.matchAll(/<!--[\s\S]*?-->/gu)) ranges.push([match.index, match.index + match[0].length]);
  return ranges;
}
function supportedOccurrence(source, needle, ranges) {
  let start = source.indexOf(needle);
  while (start !== -1) {
    const end = start + needle.length;
    if (!ranges.some(([excludedStart, excludedEnd]) => start < excludedEnd && end > excludedStart)) return { start, end };
    start = source.indexOf(needle, start + 1);
  }
  return null;
}
const FEATURE_ACTION = {
  F01: 'Review sentence length for clarity.', F02: 'Review sentence length variation where rhythm helps comprehension.',
  F03: 'Review repeated wording without replacing precise terms.', F04: 'Review direct reader address where the audience relationship calls for it.',
  F05: 'Review contractions against the intended level of formality.', F06: 'Review questions where they serve a real rhetorical purpose.',
  F07: 'Review paragraph breaks around distinct ideas.', F08: 'Review emphasis only where it helps scanning.',
};
function assess(measurement, profile, constraints, ratings, source, context, hashes = {}) {
  const bounds = mergeBounds(profile, constraints);
  const byFeature = new Map(measurement.features.map(row => [row.feature_id, row]));
  const numericChecks = [...bounds].map(([featureId, limit]) => {
    const feature = byFeature.get(featureId);
    const value = feature?.raw_value ?? null;
    return { featureId, unit: FEATURE_UNIT[featureId], value, min: Number.isFinite(limit.min) ? limit.min : null, max: Number.isFinite(limit.max) ? limit.max : null,
      status: value === null ? 'unavailable' : value < limit.min || value > limit.max ? 'fail' : 'pass', sources: limit.sources, reasons: limit.reasons };
  });
  const observedComparisons = profile.observedFeatures.map(row => {
    const value = byFeature.get(row.featureId)?.raw_value ?? null;
    const status = value === null || row.n === 0 ? 'unavailable' : value < row.min ? 'below' : value > row.max ? 'above' : 'within';
    const suggestion = status === 'below' || status === 'above'
      ? `Review ${row.featureId} in context; the observed ${status} range is descriptive, so change it only if the task and meaning benefit.`
      : null;
    return { featureId: row.featureId, unit: row.unit, value, observed: { min: row.min, median: row.median, max: row.max, n: row.n }, status, suggestion };
  });
  const requiredRanges = evidenceRanges(source, measurement, 'required');
  const toneRanges = evidenceRanges(source, measurement, 'tone');
  const spanChecks = constraints.requiredSpans.map(span => {
    const occurrence = supportedOccurrence(source, span, requiredRanges);
    return { span, status: occurrence ? 'pass' : 'fail', sourceStart: occurrence?.start ?? null, sourceEnd: occurrence?.end ?? null };
  });
  const ratingMap = new Map((ratings?.ratings || []).map(row => [row.dimension, row]));
  const targetRows = [...profile.toneTargets];
  if (context === 'serious_incident') for (const [dimension, override] of Object.entries(profile.incidentOverride || {})) {
    if (!targetRows.some(row => row.dimension === dimension)) targetRows.push({ dimension, range: override, task: 'Review serious incident suitability' });
  }
  const knownDimensions = new Set([...profile.toneTargets.map(row => row.dimension), ...Object.keys(profile.incidentOverride || {})]);
  for (const row of ratings?.ratings || []) if (!knownDimensions.has(row.dimension)) throw new Error(`ratings unknown dimension ${row.dimension}`);
  const toneChecks = targetRows.map(target => {
    const row = ratingMap.get(target.dimension);
    const targetRange = context === 'serious_incident' && profile.incidentOverride?.[target.dimension] || target.range;
    const evidenceSupported = !!row && row.evidence.length > 0 && row.evidence.every(quote => supportedOccurrence(source, quote, toneRanges));
    const status = !row || row.value === null || !evidenceSupported ? 'unavailable' : row.value < targetRange[0] || row.value > targetRange[1] ? 'outside_target' : 'within_target';
    return { dimension: target.dimension, target: targetRange, task: target.task, value: row?.value ?? null, status,
      evidenceSupported, evidence: row?.evidence || [], rationale: row?.rationale || null, provenance: ratings?.provenance || null };
  });
  const explicitFailure = numericChecks.some(row => row.status === 'fail') || spanChecks.some(row => row.status === 'fail');
  const unavailable = measurement.extraction_status !== 'complete' || measurement.counts.eligible_words === 0;
  const status = unavailable ? 'unavailable' : explicitFailure ? 'fail' : 'review_required';
  const guidance = [];
  if (measurement.extraction_status !== 'complete') guidance.push('Resolve extraction errors and measure the unchanged source again.');
  if (measurement.counts.eligible_words === 0) guidance.push('Add eligible prose paragraphs before relying on numeric measurements.');
  for (const row of numericChecks.filter(item => item.status === 'fail')) {
    const target = row.value < row.min ? `at least ${row.min}` : `at most ${row.max}`;
    guidance.push(`${row.featureId}: measured ${row.value} ${row.unit}; explicit target ${target} (source: ${row.sources.join(', ')}). ${FEATURE_ACTION[row.featureId]} Preserve facts and intended meaning.`);
  }
  for (const row of spanChecks.filter(item => item.status === 'fail')) guidance.push(`Required exact span is absent from the draft body: ${JSON.stringify(row.span)}. Restore it where the authored text belongs; preserve its wording and factual meaning.`);
  if (toneChecks.some(row => row.status === 'unavailable')) guidance.push('An editor still needs to assess tone with exact source evidence.');
  for (const row of toneChecks.filter(item => item.status === 'outside_target')) {
    const quote = row.evidence[0].length > 100 ? `${row.evidence[0].slice(0, 100)}…` : row.evidence[0];
    guidance.push(`${row.dimension}: ${row.provenance} rating ${row.value} is outside editorial target ${row.target[0]}–${row.target[1]}; evidence ${JSON.stringify(quote)}. Review the tone in context and adjust only where appropriate, preserving facts and intent${row.provenance === 'model_estimate' ? '; an editor must confirm this model estimate' : ''}.`);
  }
  guidance.push('Complete the manual checks for factual accuracy, intent, audience fit, and meaning before use.');
  return {
    schema: 'wvl-qa-report/1', status, sourceHash: measurement.text_sha256, profileHash: profile.__hash,
    constraintsHash: hashes.constraintsHash || null, ratingsHash: hashes.ratingsHash || null,
    resourceId: profile.resourceId, profileName: profile.name, route: profile.route, context,
    extractorVersion: measurement.extractor_version, runtime: measurement.runtime, extractionStatus: measurement.extraction_status,
    measured: { features: measurement.features, counts: measurement.counts, warnings: measurement.warnings, errors: measurement.errors,
      fullFingerprintEligible: measurement.full_fingerprint_eligible, evidence: measurement.evidence, exclusions: measurement.exclusions },
    numericChecks, spanChecks, observedComparisons, toneChecks,
    editorialRatings: ratings ? { provenance: ratings.provenance, sourceHash: ratings.sourceHash, suppliedByReviewer: true } : null,
    manualChecks: profile.manualChecks.map(row => ({ ...row, status: 'review_required' })),
    revisionGuidance: guidance,
  };
}
function decode(bytes, label) { try { return new TextDecoder('utf-8', { fatal: true, ignoreBOM: true }).decode(bytes); } catch { throw new Error(`${label} is not valid UTF-8`); } }
function readJson(file, label) {
  let bytes;
  try { bytes = fs.readFileSync(file); } catch (error) { throw new Error(`cannot read ${label}: ${error.message}`); }
  try { return { value: JSON.parse(decode(bytes, label)), hash: SHA(bytes) }; } catch (error) { throw new Error(`invalid ${label}: ${error.message}`); }
}
function parseArgs(argv) {
  const options = {};
  const flags = new Set(['--input', '--profile', '--constraints', '--ratings', '--channel', '--language', '--context', '--emphasis-known', '--output']);
  for (let i = 0; i < argv.length; i += 2) {
    if (!flags.has(argv[i]) || i + 1 >= argv.length || Object.hasOwn(options, argv[i])) throw new Error(`invalid or repeated argument ${argv[i] || ''}`);
    options[argv[i]] = argv[i + 1];
  }
  if (!options['--input']) throw new Error('--input is required');
  if (options['--channel'] && !['markdown', 'plain_text'].includes(options['--channel'])) throw new Error('channel must be markdown or plain_text');
  if (options['--language'] && !/^en(?:-[A-Za-z]{2,8})*$/u.test(options['--language'])) throw new Error('language must be en or an English variant');
  if (options['--context'] && !['ordinary', 'serious_incident'].includes(options['--context'])) throw new Error('context must be ordinary or serious_incident');
  if (options['--emphasis-known'] && options['--emphasis-known'] !== 'true') throw new Error('--emphasis-known accepts only true');
  if (options['--emphasis-known'] && options['--channel'] !== 'plain_text') throw new Error('--emphasis-known requires --channel plain_text');
  if (options['--output'] === '-') throw new Error('--output must be a new file path');
  return options;
}
async function run(argv, stdin = process.stdin) {
  if (Number(process.versions.node.split('.')[0]) < 20) throw new Error('Node 20 or newer is required');
  const args = parseArgs(argv);
  const input = args['--input'];
  let sourceBytes;
  if (input === '-') {
    const chunks = [];
    for await (const chunk of stdin) chunks.push(Buffer.from(chunk));
    sourceBytes = Buffer.concat(chunks);
  } else sourceBytes = fs.readFileSync(input);
  const source = decode(sourceBytes, 'input');
  const defaultProfile = path.resolve(__dirname, '..', 'references', 'qa-profile.json');
  const { value: profile, hash: profileHash } = readJson(args['--profile'] || defaultProfile, 'profile');
  validateProfile(profile);
  Object.defineProperty(profile, '__hash', { value: profileHash });
  const constraintsFile = args['--constraints'] ? readJson(args['--constraints'], 'constraints') : null;
  const validConstraints = validateConstraints(constraintsFile?.value, profile.resourceId);
  // Check contradictory bounds before invoking the extraction runtime.
  mergeBounds(profile, validConstraints);
  const ratingsFile = args['--ratings'] ? readJson(args['--ratings'], 'ratings') : null;
  const validRatings = validateRatings(ratingsFile?.value, profile.resourceId, SHA(sourceBytes));
  const localParser = path.join(__dirname, 'vendor', 'marked');
  if (fs.existsSync(localParser)) process.env.VOICE_LAB_MARKED = localParser;
  const measurement = await measure(source, { metadata: {
    channel: args['--channel'] || 'markdown', language: args['--language'] || 'en',
    ...(args['--emphasis-known'] === 'true' ? { emphasis_known: 'true' } : {}),
  } });
  const report = assess(measurement, profile, validConstraints, validRatings, source, args['--context'] || 'ordinary',
    { constraintsHash: constraintsFile?.hash, ratingsHash: ratingsFile?.hash });
  if (args['--output']) {
    const output = path.resolve(args['--output']);
    if (input !== '-' && output === path.resolve(input)) throw new Error('output cannot overwrite input');
    fs.writeFileSync(output, JSON.stringify(report, null, 2) + '\n', { flag: 'wx', encoding: 'utf8' });
  } else process.stdout.write(JSON.stringify(report, null, 2) + '\n');
  return report.status === 'fail' ? 1 : report.status === 'unavailable' ? 2 : 0;
}
if (require.main === module) run(process.argv.slice(2)).then(code => { process.exitCode = code; }).catch(error => {
  process.stderr.write(`voice validation: ${error.message}\n`);
  process.exitCode = 2;
});
module.exports = { run, parseArgs, validateProfile, validateConstraints, validateRatings, mergeBounds, assess };
