'use strict';

const { EXTRACTOR_VERSION, SCHEMA_VERSION, FEATURE_IDS } = require('./constants.cjs');
const { median } = require('./text.cjs');
const { hash } = require('./markdown.cjs');
const COHORT_METHOD = 'frozen-raw-percentile-robust-distance/1.0.0';
const quantile = (values, p) => {
  const sorted = [...values].sort((a, b) => a - b), position = (sorted.length - 1) * p;
  const lo = Math.floor(position), hi = Math.ceil(position);
  return sorted[lo] + (sorted[hi] - sorted[lo]) * (position - lo);
};
function featureMap(result) { return Object.fromEntries(result.features.map(feature => [feature.feature_id, feature.raw_value])); }
function validateGroupConfig(groups, floors) {
  if (!Array.isArray(groups) || !groups.length || Math.abs(groups.reduce((sum, group) => sum + group.weight, 0) - 1) > 1e-10) throw new Error('group weights must sum to one');
  const seen = new Set();
  for (const group of groups) {
    if (!Number.isFinite(group.weight) || group.weight < 0 || !group.features?.length) throw new Error('invalid group');
    for (const id of group.features) {
      if (!FEATURE_IDS.includes(id) || seen.has(id) || !Number.isFinite(floors[id]) || floors[id] <= 0) throw new Error('feature IDs must be unique with explicit positive scale floors');
      seen.add(id);
    }
  }
}
function freezeCohort(samples, config) {
  const { version, genre, length_band, generation_conditions, language, channel, groups, floors } = config;
  for (const value of [version, genre, length_band, generation_conditions, language, channel]) if (typeof value !== 'string' || !value.trim()) throw new Error('cohort version and comparison conditions required');
  validateGroupConfig(groups, floors);
  if (!samples.length) throw new Error('empty calibration cohort');
  const ids = new Set(), hashes = new Set();
  for (const sample of samples) {
    if (!sample.metadata.sample_id || sample.metadata.split !== 'calibration') throw new Error('calibration samples require unique sample_id and split=calibration');
    if (ids.has(sample.metadata.sample_id) || hashes.has(sample.specimen_sha256)) throw new Error('duplicate calibration sample or specimen');
    if (sample.extractor_version !== EXTRACTOR_VERSION || sample.schema_version !== SCHEMA_VERSION || sample.extraction_status !== 'complete' || sample.language !== language || sample.channel !== channel) throw new Error('incompatible calibration sample');
    for (const key of ['genre', 'length_band', 'generation_conditions']) if (sample.metadata[key] !== config[key]) throw new Error(`calibration condition mismatch: ${key}`);
    ids.add(sample.metadata.sample_id); hashes.add(sample.specimen_sha256);
  }
  const reference = {};
  for (const id of FEATURE_IDS) {
    const values = samples.map(sample => featureMap(sample)[id]);
    const eligible = values.filter(Number.isFinite).sort((a, b) => a - b);
    reference[id] = {
      values: eligible, sample_count: eligible.length, missing_count: values.length - eligible.length,
      median: eligible.length ? median(eligible) : null,
      iqr: eligible.length ? quantile(eligible, 0.75) - quantile(eligible, 0.25) : null,
      scale_floor: floors[id] ?? null,
    };
  }
  const cohort = {
    version, method_version: COHORT_METHOD, extractor_version: EXTRACTOR_VERSION, schema_version: SCHEMA_VERSION,
    genre, length_band, generation_conditions, language, channel, groups, reference,
    calibration_sample_ids: [...ids], calibration_specimen_hashes: [...hashes],
    calibration_prompt_ids: [...new Set(samples.map(sample => sample.metadata.prompt_id).filter(Boolean))],
  };
  return { ...cohort, cohort_sha256: hash(JSON.stringify(cohort)) };
}
function compatibility(result, cohort) {
  const reasons = [];
  if (cohort.method_version !== COHORT_METHOD || cohort.extractor_version !== result.extractor_version || cohort.schema_version !== result.schema_version) reasons.push('incompatible_versions');
  if (cohort.language !== result.language || cohort.channel !== result.channel) reasons.push('incompatible_language_or_channel');
  if (result.extraction_status !== 'complete') reasons.push('unsupported_extraction');
  // Condition metadata is explicit, never inferred from filename or profile label.
  for (const key of ['genre', 'length_band', 'generation_conditions']) if (result.metadata[key] !== cohort[key]) reasons.push(`incompatible_${key}`);
  if (result.metadata.split === 'evaluation' && (cohort.calibration_sample_ids.includes(result.metadata.sample_id) || cohort.calibration_specimen_hashes.includes(result.specimen_sha256) || (result.metadata.prompt_id && cohort.calibration_prompt_ids.includes(result.metadata.prompt_id)))) reasons.push('calibration_evaluation_leakage');
  const { cohort_sha256, ...payload } = cohort;
  if (hash(JSON.stringify(payload)) !== cohort_sha256) reasons.push('cohort_hash_mismatch');
  return [...new Set(reasons)];
}
function percentiles(result, cohort) {
  const reasons = compatibility(result, cohort), values = featureMap(result);
  return FEATURE_IDS.map(id => {
    const x = values[id], ref = cohort.reference[id]?.values || [];
    const reason = reasons.length ? reasons.join(';') : !Number.isFinite(x) ? 'missing_raw_feature' : !ref.length ? 'no_eligible_reference_values' : null;
    return {
      feature_id: id, raw_value: x, display_percentile: reason ? null : 100 * (ref.filter(v => v < x).length + 0.5 * ref.filter(v => v === x).length) / ref.length,
      cohort_version: cohort.version, cohort_sha256: cohort.cohort_sha256, method_version: COHORT_METHOD,
      eligible_reference_count: ref.length, reason,
    };
  });
}
function distance(a, b, cohort) {
  const reasons = [...compatibility(a, cohort), ...compatibility(b, cohort)];
  const A = featureMap(a), B = featureMap(b);
  let squared = 0;
  const components = [];
  for (const group of cohort.groups) {
    let groupSum = 0;
    for (const id of group.features) {
      const ref = cohort.reference[id];
      if (!Number.isFinite(A[id]) || !Number.isFinite(B[id]) || !Number.isFinite(ref?.median) || !Number.isFinite(ref?.iqr) || !Number.isFinite(ref?.scale_floor) || ref.scale_floor <= 0) { reasons.push(`missing_required_${id}`); continue; }
      const scale = Math.max(ref.iqr, ref.scale_floor), delta = (A[id] - B[id]) / scale;
      groupSum += delta ** 2;
      components.push({ feature_id: id, scale, standardized_delta: delta });
    }
    squared += group.weight * groupSum / group.features.length;
  }
  return { value: reasons.length ? null : Math.sqrt(squared), reason: reasons.length ? [...new Set(reasons)].join(';') : null, cohort_version: cohort.version, cohort_sha256: cohort.cohort_sha256, method_version: COHORT_METHOD, label: cohort.groups.some(g => g.features.some(id => ['F07', 'F08'].includes(id))) ? 'layout_inclusive_recipe_distance' : 'language_only_distance', components };
}
// Each matched task contributes one center, regardless of its word count or variant count.
function equalTaskSummary(samples, taskIds) {
  if (!taskIds?.length || new Set(taskIds).size !== taskIds.length) throw new Error('declare unique matched task IDs');
  if (samples.some(sample => !taskIds.includes(sample.metadata.brief_id))) throw new Error('unexpected task');
  return FEATURE_IDS.map(id => {
    const tasks = taskIds.map(task => {
      const rows = samples.filter(sample => sample.metadata.brief_id === task);
      const values = rows.map(sample => featureMap(sample)[id]);
      return { brief_id: task, sample_count: rows.length, raw_value: !rows.length || values.some(v => !Number.isFinite(v)) ? null : median(values) };
    });
    return { feature_id: id, raw_value: tasks.some(task => task.raw_value === null) ? null : tasks.reduce((sum, task) => sum + task.raw_value, 0) / tasks.length, reason: tasks.some(task => task.raw_value === null) ? 'missing_matched_task_feature' : null, method_version: 'equal-task-median-centers/1.0.0', tasks };
  });
}
module.exports = { freezeCohort, percentiles, distance, equalTaskSummary, COHORT_METHOD };
