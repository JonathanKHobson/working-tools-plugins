#!/usr/bin/env python3
"""Check an assessment-authoring-1 JSON bank's structure and references.

This read-only check cannot verify source truth, answer correctness, validity,
reliability, fairness, or learner understanding. It prints JSON to stdout.

Format fields:
  single-select: options [{id,text,rationale}], key.correct_option_ids (one),
    scoring.policy="exact-match".
  multiselect: options and key.correct_option_ids; item.select_count is a
    positive integer matching the number of keyed options, or "all". Use
    scoring.policy="exact-match", or "partial-credit" with
    scoring.partial_credit_rule containing finite numeric
    correct_selection_points (>0), incorrect_selection_points (<0),
    omission_points (<=0), and minimum_score (0..points_possible).
    Raw score = selected correct rewards + selected incorrect penalties +
    omitted correct penalties. Final score clamps raw score to
    [minimum_score, points_possible]. The correct-only set's raw score must
    equal points_possible; the all-selected set must score below full credit.
  numeric: key.value (finite number), key.tolerance (finite nonnegative
    absolute tolerance), key.units (nonempty string); scoring.policy is
    "exact-match" for zero tolerance or "numeric-tolerance" otherwise.
  short-response and performance: key.acceptable_alternatives (nonempty
    strings) or scoring.criteria (nonempty [{id,description,points}]);
    scoring.policy is "criterion-based" or "human-review".

All items require objective_ids, claim, evidence, source_refs, stem,
response_directions, scoring.points_possible, feedback.explanation/next_step,
cognitive_demand.label/rationale, difficulty.intended/observed, and review
source_verified/independent_key_check/pilot_status. The checker accepts extra
fields for source conflict notes, accommodations, and review evidence.
"""

import argparse
import json
import math
from pathlib import Path


FORMATS = {'single-select', 'multiselect', 'numeric', 'short-response', 'performance'}


def _filled(value):
    return isinstance(value, str) and bool(value.strip())


def _number(value):
    return type(value) in (int, float) and math.isfinite(value)


def validate(data):
    """Return (errors, warnings) without mutating the authoring bank."""
    errors, warnings = [], []
    if not isinstance(data, dict):
        return ['bank: JSON object required'], warnings

    if data.get('schema_version') != 'assessment-authoring-1':
        errors.append('schema_version: expected assessment-authoring-1')
    for field in ('id', 'status', 'purpose', 'intended_use'):
        if not _filled(data.get(field)):
            errors.append(f'{field}: nonempty string required')
    if not isinstance(data.get('conditions'), dict):
        errors.append('conditions: object required')
    if data.get('status') == 'draft':
        warnings.append('bank: draft status; review and pilot evidence are still needed')

    indexed = {}
    for group in ('outcomes', 'sources', 'items'):
        rows = data.get(group)
        if not isinstance(rows, list) or not rows:
            errors.append(f'{group}: nonempty list required')
            indexed[group] = {}
            continue
        found = {}
        for index, row in enumerate(rows):
            location = f'{group}[{index}]'
            if not isinstance(row, dict):
                errors.append(f'{location}: object required')
                continue
            key = row.get('id')
            if not _filled(key):
                errors.append(f'{location}.id: nonempty string required')
                continue
            if key in found:
                errors.append(f'{group}: duplicate id {key}')
                continue
            found[key] = row
        indexed[group] = found

    outcomes, sources, items = (indexed[group] for group in ('outcomes', 'sources', 'items'))
    for oid, outcome in outcomes.items():
        for field in ('claim', 'evidence', 'decision_use'):
            if not _filled(outcome.get(field)):
                errors.append(f'outcomes/{oid}.{field}: nonempty string required')
    for sid, source in sources.items():
        for field in ('title', 'version', 'kind'):
            if not _filled(source.get(field)):
                errors.append(f'sources/{sid}.{field}: nonempty string required')
        if not (_filled(source.get('content')) or _filled(source.get('locator'))):
            errors.append(f'sources/{sid}: content or locator required')

    covered = set()
    for iid, item in items.items():
        where = f'items/{iid}'
        for field in ('claim', 'evidence', 'stem', 'response_directions'):
            if not _filled(item.get(field)):
                errors.append(f'{where}.{field}: nonempty string required')

        objective_ids = item.get('objective_ids')
        if not isinstance(objective_ids, list) or not objective_ids or not all(_filled(x) for x in objective_ids):
            errors.append(f'{where}.objective_ids: nonempty list of IDs required')
        else:
            if len(objective_ids) != len(set(objective_ids)):
                errors.append(f'{where}.objective_ids: duplicate ID')
            unknown = set(objective_ids) - set(outcomes)
            if unknown:
                errors.append(f'{where}.objective_ids: unknown outcomes {sorted(unknown)}')
            covered.update(set(objective_ids) & set(outcomes))

        refs = item.get('source_refs')
        if not isinstance(refs, list) or not refs:
            errors.append(f'{where}.source_refs: nonempty list required')
        else:
            for index, ref in enumerate(refs):
                loc = f'{where}.source_refs[{index}]'
                if not isinstance(ref, dict):
                    errors.append(f'{loc}: object required')
                    continue
                if not _filled(ref.get('source_id')) or ref['source_id'] not in sources:
                    errors.append(f'{loc}.source_id: unknown or missing source')
                for field in ('locator', 'supports'):
                    if not _filled(ref.get(field)):
                        errors.append(f'{loc}.{field}: nonempty string required')

        demand = item.get('cognitive_demand')
        if not isinstance(demand, dict) or not all(_filled(demand.get(f)) for f in ('label', 'rationale')):
            errors.append(f'{where}.cognitive_demand: label and rationale required')
        difficulty = item.get('difficulty')
        if not isinstance(difficulty, dict) or not _filled(difficulty.get('intended')) or 'observed' not in difficulty:
            errors.append(f'{where}.difficulty: intended and explicit observed field required')
        elif difficulty['observed'] is not None:
            if not isinstance(difficulty['observed'], dict):
                errors.append(f'{where}.difficulty.observed: null or evidence object required')
            elif not difficulty['observed']:
                warnings.append(f'{where}: observed difficulty has no evidence; treat as unverified')

        review = item.get('review')
        if not isinstance(review, dict):
            errors.append(f'{where}.review: object required')
        else:
            for field in ('source_verified', 'independent_key_check'):
                if type(review.get(field)) is not bool:
                    errors.append(f'{where}.review.{field}: boolean required')
                elif not review[field]:
                    warnings.append(f'{where}: {field} remains false')
            if not _filled(review.get('pilot_status')):
                errors.append(f'{where}.review.pilot_status: nonempty string required')
            elif review['pilot_status'] == 'not-piloted':
                warnings.append(f'{where}: not piloted')
            if any(review.get(field) is True for field in ('source_verified', 'independent_key_check')):
                if not all(_filled(review.get(field)) for field in ('reviewer', 'reviewed_at', 'evidence')):
                    warnings.append(f'{where}: positive review flags need reviewer, reviewed_at, and evidence')

        feedback = item.get('feedback')
        if not isinstance(feedback, dict) or not all(_filled(feedback.get(f)) for f in ('explanation', 'next_step')):
            errors.append(f'{where}.feedback: explanation and next_step required')
        scoring = item.get('scoring')
        if not isinstance(scoring, dict):
            errors.append(f'{where}.scoring: object required')
            scoring = {}
        points = scoring.get('points_possible')
        if not _number(points) or points <= 0:
            errors.append(f'{where}.scoring.points_possible: positive finite number required')
            points = None
        if not _filled(scoring.get('policy')):
            errors.append(f'{where}.scoring.policy: nonempty string required')
        key = item.get('key')
        if not isinstance(key, dict):
            errors.append(f'{where}.key: object required')
            key = {}

        response_format = item.get('format')
        if not isinstance(response_format, str) or response_format not in FORMATS:
            errors.append(f'{where}.format: unsupported format {response_format!r}; manual review required')
            continue

        if response_format in ('single-select', 'multiselect'):
            options = item.get('options')
            option_ids = set()
            if not isinstance(options, list) or len(options) < 2:
                errors.append(f'{where}.options: at least two option objects required')
            else:
                for index, option in enumerate(options):
                    loc = f'{where}.options[{index}]'
                    if not isinstance(option, dict):
                        errors.append(f'{loc}: object required')
                        continue
                    for field in ('id', 'text', 'rationale'):
                        if not _filled(option.get(field)):
                            errors.append(f'{loc}.{field}: nonempty string required')
                    option_id = option.get('id')
                    if _filled(option_id):
                        if option_id in option_ids:
                            errors.append(f'{where}.options: duplicate id {option_id}')
                        option_ids.add(option_id)
            correct = key.get('correct_option_ids')
            if not isinstance(correct, list) or not correct or not all(_filled(x) for x in correct):
                errors.append(f'{where}.key.correct_option_ids: nonempty list of IDs required')
                correct = []
            else:
                if len(correct) != len(set(correct)):
                    errors.append(f'{where}.key.correct_option_ids: duplicate ID')
                unknown = set(correct) - option_ids
                if unknown:
                    errors.append(f'{where}.key.correct_option_ids: unknown options {sorted(unknown)}')
            if response_format == 'single-select':
                if len(correct) != 1:
                    errors.append(f'{where}: single-select needs exactly one keyed option')
                if scoring.get('policy') != 'exact-match':
                    errors.append(f'{where}.scoring.policy: single-select requires exact-match')
            else:
                count = item.get('select_count')
                if count != 'all' and (type(count) is not int or count <= 0):
                    errors.append(f'{where}.select_count: positive integer or "all" required')
                elif type(count) is int and count != len(correct):
                    errors.append(f'{where}.select_count: must match keyed option count')
                if scoring.get('policy') not in ('exact-match', 'partial-credit'):
                    errors.append(f'{where}.scoring.policy: multiselect requires exact-match or partial-credit')
                if scoring.get('policy') == 'partial-credit':
                    rule = scoring.get('partial_credit_rule')
                    fields = ('correct_selection_points', 'incorrect_selection_points', 'omission_points', 'minimum_score')
                    if not isinstance(rule, dict) or not all(_number(rule.get(f)) for f in fields):
                        errors.append(f'{where}.scoring.partial_credit_rule: finite numeric {fields} required')
                    elif rule['correct_selection_points'] <= 0 or rule['incorrect_selection_points'] >= 0 or rule['omission_points'] > 0 or rule['minimum_score'] < 0 or (points is not None and rule['minimum_score'] > points):
                        errors.append(f'{where}.scoring.partial_credit_rule: invalid reward, penalty, or floor')
                    elif points is not None and correct and option_ids:
                        full_key_raw = len(correct) * rule['correct_selection_points']
                        if not math.isclose(full_key_raw, points, rel_tol=1e-9, abs_tol=1e-9):
                            errors.append(f'{where}.scoring.partial_credit_rule: correct-only raw score {full_key_raw} differs from points_possible {points}')
                        all_selected_raw = (len(correct) * rule['correct_selection_points']
                                            + (len(option_ids) - len(set(correct)))
                                            * rule['incorrect_selection_points'])
                        all_selected = min(points, max(rule['minimum_score'], all_selected_raw))
                        if all_selected >= points:
                            errors.append(f'{where}.scoring.partial_credit_rule: selecting every option earns full credit')
        elif response_format == 'numeric':
            value, tolerance, units = (key.get(f) for f in ('value', 'tolerance', 'units'))
            if not _number(value):
                errors.append(f'{where}.key.value: finite number required')
            if not _number(tolerance) or tolerance < 0:
                errors.append(f'{where}.key.tolerance: nonnegative finite number required')
            if not _filled(units):
                errors.append(f'{where}.key.units: nonempty string required')
            if _number(tolerance):
                expected = 'exact-match' if tolerance == 0 else 'numeric-tolerance'
                if scoring.get('policy') != expected:
                    errors.append(f'{where}.scoring.policy: numeric tolerance requires {expected}')
        else:
            alternatives = key.get('acceptable_alternatives')
            if alternatives is not None and (not isinstance(alternatives, list) or not alternatives or not all(_filled(x) for x in alternatives)):
                errors.append(f'{where}.key.acceptable_alternatives: nonempty strings required when present')
                alternatives = None
            criteria = scoring.get('criteria')
            if criteria is not None:
                if not isinstance(criteria, list) or not criteria:
                    errors.append(f'{where}.scoring.criteria: nonempty list required when present')
                    criteria = None
                else:
                    seen, total = set(), 0
                    for index, criterion in enumerate(criteria):
                        loc = f'{where}.scoring.criteria[{index}]'
                        if not isinstance(criterion, dict):
                            errors.append(f'{loc}: object required')
                            continue
                        for field in ('id', 'description'):
                            if not _filled(criterion.get(field)):
                                errors.append(f'{loc}.{field}: nonempty string required')
                        cid = criterion.get('id')
                        if _filled(cid):
                            if cid in seen:
                                errors.append(f'{where}.scoring.criteria: duplicate id {cid}')
                            seen.add(cid)
                        weight = criterion.get('points')
                        if not _number(weight) or weight <= 0:
                            errors.append(f'{loc}.points: positive finite number required')
                        else:
                            total += weight
                    if points is not None and all(_number(c.get('points')) and c['points'] > 0 for c in criteria if isinstance(c, dict)) and not math.isclose(total, points):
                        errors.append(f'{where}.scoring.criteria: total {total} differs from points_possible {points}')
            if not alternatives and not criteria:
                errors.append(f'{where}: accepted alternatives or scoring criteria required')
            if scoring.get('policy') not in ('criterion-based', 'human-review'):
                errors.append(f'{where}.scoring.policy: criterion-based or human-review required')

    uncovered = set(outcomes) - covered
    if uncovered:
        errors.append(f'outcomes: uncovered IDs {sorted(uncovered)}')
    return errors, warnings


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('path', type=Path, help='JSON assessment bank to inspect (never modified)')
    args = parser.parse_args(argv)
    try:
        data = json.loads(args.path.read_text(encoding='utf-8'))
        errors, warnings = validate(data)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        errors, warnings = [f'input: {exc}'], []
    print(json.dumps({'ok': not errors, 'errors': errors, 'warnings': warnings,
                      'limit': 'Structural check only; human source, key, accessibility, and pilot review remain required.'}, indent=2))
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
