'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const crypto = require('node:crypto');
const { spawnSync } = require('node:child_process');
const { FEATURE_IDS, UNITS } = require('../library/voice-library/metrics/constants.cjs');
const { validateProfile, mergeBounds } = require('../library/voice-library/validation/validate.cjs');

const script = path.resolve(__dirname, '../library/voice-library/validation/validate.cjs');
const sample = [
  'You walk with me today. '.repeat(4).trim(),
  'You walk with me today. '.repeat(3).trim(),
  'You walk with me today. '.repeat(3).trim(),
].join('\n\n');
const digest = value => crypto.createHash('sha256').update(value).digest('hex');
const bound = (featureId, limits) => ({ featureId, ...limits, source: 'user brief', reason: 'Fixture requirement' });
const profile = () => ({
  schema: 'wvl-qa-profile/1', resourceId: 'V01', name: 'Fixture', route: { selected_resource_id: 'V01', base_profile_id: 'V01', module_ids: [] }, extractorVersion: 'wvl-metrics/1.0.0',
  observedFeatures: FEATURE_IDS.map((featureId, i) => ({ featureId, unit: UNITS[i], min: 0, median: featureId === 'F03' ? .5 : 1, max: featureId === 'F03' ? 1 : ['F06', 'F08'].includes(featureId) ? 100 : 1000, n: 4 })),
  toneTargets: [{ dimension: 'humor', range: [2, 4], task: 'Review tone' }, { dimension: 'enthusiasm', range: [2, 4], task: 'Review tone' }],
  incidentOverride: { humor: [1, 1], enthusiasm: [1, 1], persuasive_intent: [1, 1] },
  manualChecks: [{ id: 'facts', label: 'Facts intact', source: 'source' }], hardConstraints: [],
});
function fixture(fn) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'wvl-validation-'));
  try {
    const input = path.join(dir, 'source.txt'), profilePath = path.join(dir, 'profile.json');
    fs.writeFileSync(input, sample); fs.writeFileSync(profilePath, JSON.stringify(profile()));
    return fn({ dir, input, profilePath });
  } finally { fs.rmSync(dir, { recursive: true, force: true }); }
}
function invoke(input, profilePath, extra = []) {
  const channel = extra.includes('--channel') ? [] : ['--channel', 'plain_text'];
  const result = spawnSync(process.execPath, [script, '--input', input, '--profile', profilePath, ...channel, ...extra], { encoding: 'utf8' });
  return { code: result.status, stderr: result.stderr, report: result.stdout ? JSON.parse(result.stdout) : null };
}
test('reports the engine F01-F08 with independently known arithmetic', () => fixture(({ input, profilePath }) => {
  const before = fs.readFileSync(input);
  const { code, report } = invoke(input, profilePath);
  assert.equal(code, 0);
  assert.equal(report.status, 'review_required');
  assert.equal(report.sourceHash, digest(before));
  const values = report.measured.features.map(row => row.raw_value);
  assert.deepEqual(values, [5, 0, .1, 200, 0, 0, 15, null]);
  assert.deepEqual(report.measured.features.map(row => row.feature_id), FEATURE_IDS);
  assert.equal(report.measured.counts.eligible_words, 50);
  assert.equal(report.measured.counts.prose_sentences, 10);
  assert.equal(report.measured.evidence.sentences.length, 10);
  assert.equal(report.measured.fullFingerprintEligible, false);
  assert.deepEqual(fs.readFileSync(input), before);
}));
test('observed ranges never pass or fail; explicit constraints enforce both sides and boundaries', () => fixture(({ dir, input, profilePath }) => {
  const p = profile(); p.observedFeatures[0] = { featureId: 'F01', unit: UNITS[0], min: 8, median: 9, max: 10, n: 4 };
  fs.writeFileSync(profilePath, JSON.stringify(p));
  const c = path.join(dir, 'constraints.json');
  const write = features => fs.writeFileSync(c, JSON.stringify({ schema: 'wvl-task-constraints/1', resourceId: 'V01', features, requiredSpans: [] }));
  let out = invoke(input, profilePath);
  assert.equal(out.code, 0);
  assert.equal(out.report.observedComparisons[0].status, 'below');
  write([bound('F01', { min: 5, max: 5 })]);
  out = invoke(input, profilePath, ['--constraints', c]);
  assert.equal(out.report.numericChecks[0].status, 'pass');
  write([bound('F01', { min: 6 })]);
  out = invoke(input, profilePath, ['--constraints', c]);
  assert.equal(out.code, 1);
  assert.equal(out.report.numericChecks[0].status, 'fail');
  write([bound('F01', { max: 4 })]);
  out = invoke(input, profilePath, ['--constraints', c]);
  assert.equal(out.code, 1);
  assert.equal(out.report.numericChecks[0].status, 'fail');
}));
test('zero stays measured while sparse null is unavailable', () => fixture(({ dir, input, profilePath }) => {
  const c = path.join(dir, 'constraints.json');
  fs.writeFileSync(c, JSON.stringify({ schema: 'wvl-task-constraints/1', resourceId: 'V01', features: [bound('F02', { min: 0, max: 0 }), bound('F03', { min: 0 })], requiredSpans: [] }));
  let out = invoke(input, profilePath, ['--constraints', c]);
  assert.deepEqual(out.report.numericChecks.map(row => row.status), ['pass', 'pass']);
  fs.writeFileSync(input, 'You walk.');
  out = invoke(input, profilePath, ['--constraints', c]);
  assert.equal(out.report.numericChecks[0].status, 'unavailable');
  assert.equal(out.report.numericChecks[1].status, 'unavailable');
  assert.equal(out.report.measured.features[4].raw_value, 0);
}));
test('empty and lists only are not reported as a full style pass', () => fixture(({ input, profilePath }) => {
  fs.writeFileSync(input, '');
  let out = invoke(input, profilePath);
  assert.equal(out.code, 2); assert.equal(out.report.status, 'unavailable');
  fs.writeFileSync(input, '- You walk now.\n- You run now.\n');
  out = invoke(input, profilePath, ['--channel', 'markdown']);
  assert.equal(out.code, 2); assert.equal(out.report.measured.counts.eligible_words, 0);
}));
test('rejects unknown fields, invalid units and malformed ranges', () => {
  const p = profile(); p.surprise = true;
  assert.throws(() => validateProfile(p), /unknown field/);
  delete p.surprise; p.observedFeatures[0].unit = 'words';
  assert.throws(() => validateProfile(p), /unit mismatch/);
  p.observedFeatures[0].unit = UNITS[0]; p.observedFeatures[0].median = -1;
  assert.throws(() => validateProfile(p), /invalid range/);
});
test('accepts sparse observed evidence without treating null statistics as a comparison', () => fixture(({ input, profilePath }) => {
  const p = profile(); p.observedFeatures[1] = { featureId: 'F02', unit: UNITS[1], n: 0, min: null, median: null, max: null };
  fs.writeFileSync(profilePath, JSON.stringify(p));
  const out = invoke(input, profilePath);
  assert.equal(out.code, 0);
  assert.equal(out.report.observedComparisons[1].status, 'unavailable');
  p.observedFeatures[1].max = 1;
  assert.throws(() => validateProfile(p), /zero observations/);
}));
test('task constraints cannot loosen base limits', () => {
  const p = profile(); p.hardConstraints = [bound('F01', { min: 6, max: 8 })];
  const limits = mergeBounds(p, { features: [bound('F01', { min: 1, max: 10 })] });
  assert.equal(limits.get('F01').min, 6); assert.equal(limits.get('F01').max, 8);
  assert.throws(() => mergeBounds(p, { features: [bound('F01', { min: 9 })] }), /conflict/);
});
test('required exact spans fail without rewriting the input', () => fixture(({ dir, input, profilePath }) => {
  const c = path.join(dir, 'constraints.json');
  const before = fs.readFileSync(input);
  fs.writeFileSync(c, JSON.stringify({ schema: 'wvl-task-constraints/1', resourceId: 'V01', features: [], requiredSpans: ['exact factual quotation'] }));
  const out = invoke(input, profilePath, ['--constraints', c]);
  assert.equal(out.code, 1); assert.equal(out.report.spanChecks[0].status, 'fail');
  assert.deepEqual(fs.readFileSync(input), before);
  assert.equal(out.report.constraintsHash, digest(fs.readFileSync(c)));
}));
test('required spans and tone evidence cannot be spoofed by metadata, comments, destinations, or wrappers', () => fixture(({ dir, input, profilePath }) => {
  const phrase = 'Protected sentence';
  const c = path.join(dir, 'constraints.json'), ratingsFile = path.join(dir, 'ratings.json');
  fs.writeFileSync(c, JSON.stringify({ schema: 'wvl-task-constraints/1', resourceId: 'V01', features: [], requiredSpans: [phrase] }));
  for (const source of [
    `---\nnote: ${phrase}\n---\n\n${sample}`,
    `${sample}\n\n<!-- ${phrase} -->`,
    `${sample}\n\n[reference](<${phrase}>)`,
    `<!-- specimen:start -->\n${sample}\n<!-- specimen:end -->\n${phrase}`,
  ]) {
    fs.writeFileSync(input, source);
    fs.writeFileSync(ratingsFile, JSON.stringify({ schema: 'wvl-editorial-ratings/1', resourceId: 'V01', sourceHash: digest(Buffer.from(source)), provenance: 'model_estimate', ratings: [{ dimension: 'humor', value: 3, evidence: [phrase], rationale: 'Fixture' }] }));
    const out = invoke(input, profilePath, ['--channel', 'markdown', '--constraints', c, '--ratings', ratingsFile]);
    assert.equal(out.report.spanChecks[0].status, 'fail', source);
    assert.equal(out.report.toneChecks[0].status, 'unavailable', source);
  }
  const valid = `${sample}\n\n${phrase}.`;
  fs.writeFileSync(input, valid);
  const out = invoke(input, profilePath, ['--channel', 'markdown', '--constraints', c]);
  assert.equal(out.report.spanChecks[0].status, 'pass');
  assert.equal(valid.slice(out.report.spanChecks[0].sourceStart, out.report.spanChecks[0].sourceEnd), phrase);
}));
test('required spans in authored headings, lists, and code remain eligible', () => fixture(({ dir, input, profilePath }) => {
  const c = path.join(dir, 'constraints.json');
  fs.writeFileSync(c, JSON.stringify({ schema: 'wvl-task-constraints/1', resourceId: 'V01', features: [], requiredSpans: ['Protected sentence'] }));
  for (const block of ['# Protected sentence', '- Protected sentence', '```text\nProtected sentence\n```']) {
    fs.writeFileSync(input, `${sample}\n\n${block}`);
    const out = invoke(input, profilePath, ['--channel', 'markdown', '--constraints', c]);
    assert.equal(out.report.spanChecks[0].status, 'pass', block);
  }
}));
test('copied blockquotes and explicit copied-quote blocks cannot support tone evidence', () => fixture(({ dir, input, profilePath }) => {
  const file = path.join(dir, 'ratings.json');
  for (const source of [
    `${sample}\n\n> Protected sentence`,
    `${sample}\n\n<!-- metrics:exclude:start kind=copied_quote -->\n\nProtected sentence\n\n<!-- metrics:exclude:end -->`,
  ]) {
    fs.writeFileSync(input, source);
    fs.writeFileSync(file, JSON.stringify({ schema: 'wvl-editorial-ratings/1', resourceId: 'V01', sourceHash: digest(Buffer.from(source)), provenance: 'human_review', ratings: [{ dimension: 'humor', value: 3, evidence: ['Protected sentence'], rationale: 'Fixture' }] }));
    const out = invoke(input, profilePath, ['--channel', 'markdown', '--ratings', file]);
    assert.equal(out.report.toneChecks[0].status, 'unavailable');
  }
}));
test('stale ratings reject; unsupported quotations remain unavailable', () => fixture(({ dir, input, profilePath }) => {
  const file = path.join(dir, 'ratings.json');
  const ratings = { schema: 'wvl-editorial-ratings/1', resourceId: 'V01', sourceHash: 'stale', provenance: 'model_estimate', ratings: [{ dimension: 'humor', value: 3, evidence: ['You walk'], rationale: 'Dry tone' }] };
  fs.writeFileSync(file, JSON.stringify(ratings));
  let out = invoke(input, profilePath, ['--ratings', file]);
  assert.equal(out.code, 2); assert.match(out.stderr, /sourceHash/);
  ratings.sourceHash = digest(fs.readFileSync(input)); ratings.ratings[0].evidence = ['fabricated quote'];
  fs.writeFileSync(file, JSON.stringify(ratings));
  out = invoke(input, profilePath, ['--ratings', file]);
  assert.equal(out.code, 0); assert.equal(out.report.toneChecks[0].status, 'unavailable');
  assert.equal(out.report.toneChecks[0].evidenceSupported, false);
  assert.equal(out.report.ratingsHash, digest(fs.readFileSync(file)));
  ratings.ratings[0].dimension = 'unrecognized_dimension';
  fs.writeFileSync(file, JSON.stringify(ratings));
  out = invoke(input, profilePath, ['--ratings', file]);
  assert.equal(out.code, 2); assert.match(out.stderr, /unknown dimension/);
}));
test('serious incident overlay changes only editorial target comparison', () => fixture(({ dir, input, profilePath }) => {
  const file = path.join(dir, 'ratings.json');
  const ratings = { schema: 'wvl-editorial-ratings/1', resourceId: 'V01', sourceHash: digest(fs.readFileSync(input)), provenance: 'human_review', ratings: ['humor', 'enthusiasm', 'persuasive_intent'].map(dimension => ({ dimension, value: 2, evidence: ['You walk'], rationale: 'Reviewed source' })) };
  fs.writeFileSync(file, JSON.stringify(ratings));
  const ordinary = invoke(input, profilePath, ['--ratings', file]);
  const incident = invoke(input, profilePath, ['--ratings', file, '--context', 'serious_incident']);
  assert.deepEqual(ordinary.report.toneChecks.map(row => row.status), ['within_target', 'within_target']);
  assert.deepEqual(incident.report.toneChecks.map(row => row.status), ['outside_target', 'outside_target', 'outside_target']);
  assert.equal(incident.report.status, 'review_required');
  assert.equal(incident.report.editorialRatings.provenance, 'human_review');
  assert.match(incident.report.revisionGuidance.join(' '), /humor: human_review rating 2 is outside editorial target 1–1; evidence "You walk"/);
}));
test('rejects unproven and physically impossible feature limits', () => fixture(({ dir, input, profilePath }) => {
  const file = path.join(dir, 'constraints.json');
  const constraints = { schema: 'wvl-task-constraints/1', resourceId: 'V01', features: [{ featureId: 'F03', max: 1 }], requiredSpans: [] };
  fs.writeFileSync(file, JSON.stringify(constraints));
  let out = invoke(input, profilePath, ['--constraints', file]);
  assert.equal(out.code, 2); assert.match(out.stderr, /source/);
  constraints.features = [bound('F03', { max: 1.1 })];
  fs.writeFileSync(file, JSON.stringify(constraints));
  out = invoke(input, profilePath, ['--constraints', file]);
  assert.equal(out.code, 2); assert.match(out.stderr, /unit bounds/);
}));
test('plain text emphasis is unknown until explicit authoring knowledge is supplied', () => fixture(({ input, profilePath }) => {
  const unknown = invoke(input, profilePath);
  const known = invoke(input, profilePath, ['--emphasis-known', 'true']);
  assert.equal(unknown.report.measured.features[7].raw_value, null);
  assert.equal(known.report.measured.features[7].raw_value, 0);
  assert.equal(known.report.measured.fullFingerprintEligible, true);
}));
test('invalid UTF-8 and existing output are rejected without modifying files', () => fixture(({ input, profilePath }) => {
  fs.writeFileSync(input, Buffer.from([0xc3, 0x28]));
  let out = invoke(input, profilePath);
  assert.equal(out.code, 2); assert.match(out.stderr, /valid UTF-8/);
  fs.writeFileSync(input, sample);
  const before = fs.readFileSync(input);
  out = invoke(input, profilePath, ['--output', input]);
  assert.equal(out.code, 2); assert.match(out.stderr, /overwrite input/);
  assert.deepEqual(fs.readFileSync(input), before);
}));
test('all authored external synthetic profiles satisfy the runtime contract', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'writing-qa-fixture-'));
  try {
    const result = spawnSync(process.env.PYTHON_BIN || 'python3', [path.resolve(__dirname, '../scripts/create_sample_collection.py'), '--output', path.join(dir, 'data')], { encoding: 'utf8' });
    assert.equal(result.status, 0, result.stderr);
    const profiles = path.join(dir, 'data/validation/profiles');
    const files = fs.readdirSync(profiles).filter(file => file.endsWith('.json'));
    assert.equal(files.length, 4);
    for (const file of files) assert.doesNotThrow(() => validateProfile(JSON.parse(fs.readFileSync(path.join(profiles, file), 'utf8'))), file);
  } finally { fs.rmSync(dir, { recursive: true, force: true }); }
});
test('portable scripts layout resolves local metrics and pinned marked offline', () => fixture(({ dir, input }) => {
  const scripts = path.join(dir, 'scripts');
  const references = path.join(dir, 'references');
  fs.mkdirSync(scripts); fs.mkdirSync(references);
  fs.copyFileSync(script, path.join(scripts, 'validate.cjs'));
  fs.cpSync(path.resolve(__dirname, '../library/voice-library/metrics'), path.join(scripts, 'metrics'), { recursive: true });
  fs.cpSync(path.resolve(__dirname, '../library/voice-library/validation/vendor/marked'), path.join(scripts, 'vendor/marked'), { recursive: true });
  fs.writeFileSync(path.join(references, 'qa-profile.json'), JSON.stringify(profile()));
  const result = spawnSync(process.execPath, [path.join(scripts, 'validate.cjs'), '--input', input], { encoding: 'utf8' });
  assert.equal(result.status, 0, result.stderr);
  const report = JSON.parse(result.stdout);
  assert.equal(report.runtime.marked, '17.0.5');
  assert.equal(report.runtime.parser_resolution, 'VOICE_LAB_MARKED');
  assert.equal(report.measured.features.length, 8);
  fs.rmSync(path.join(scripts, 'metrics'), { recursive: true });
  const missing = spawnSync(process.execPath, [path.join(scripts, 'validate.cjs'), '--input', input], { encoding: 'utf8' });
  assert.equal(missing.status, 2);
  assert.match(missing.stderr, /measurement engine unavailable/);
}));
