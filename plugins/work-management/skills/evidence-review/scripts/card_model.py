"""Manual evidence nomination and bounded claim validation; no IO or inference engine."""
import copy
import hashlib
import json
import re
from datetime import date, datetime

ORIGIN = 'evidence-review-v1'
MAX_BYTES = 512000
KINDS = {'conversation', 'project_file', 'computer_history', 'capture', 'memory'}
CLAIM_KINDS = {'self_report', 'artifact_observation', 'test_report', 'inference', 'measured_outcome'}
RUBRIC = ('contribution', 'meaningful_change', 'decision_quality', 'causal_uncertainty', 'artifact_proof', 'chronology', 'rights', 'reviewer_relevance')


def require(value, message):
    if not value:
        raise ValueError(message)


def object_value(value, name):
    require(isinstance(value, dict), name + ' must be an object')
    return value


def text(value, name, limit=2000):
    require(isinstance(value, str) and bool(value.strip()) and len(value) <= limit, 'Invalid ' + name)
    return value


def identifier(value, name):
    require(isinstance(value, str) and re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.:-]{0,79}', value) is not None, 'Invalid ' + name)
    return value


def timestamp(value, name):
    text(value, name, 80)
    dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
    require(dt.tzinfo is not None, name + ' must include a timezone')


def bounded_list(value, name, maximum):
    require(isinstance(value, list) and len(value) <= maximum, 'Invalid ' + name)
    return value


def strings(value, name, maximum=30):
    for item in bounded_list(value, name, maximum):
        text(item, name)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False)


def digest(value):
    return hashlib.sha256(canonical(value).encode('utf-8')).hexdigest()


def guard(packet, opt_in):
    object_value(packet, 'intake')
    require(len(canonical(packet).encode('utf-8')) <= MAX_BYTES, 'Intake exceeds 512 KB')
    require(opt_in is True and packet.get('opt_in') is True, 'Explicit invocation and intake opt-in required')
    require(type(packet.get('schema_version')) is int and packet['schema_version'] == 1, 'Unsupported schema version')
    require(packet.get('origin') != ORIGIN and packet.get('producer') != ORIGIN and type(packet.get('depth')) is int and packet['depth'] == 0 and packet.get('stop_hook_active') is not True, 'Recursive or hook-continuation intake refused')
    text(packet.get('origin'), 'origin', 80)


def validate_checkpoint(checkpoint):
    object_value(checkpoint, 'checkpoint')
    for key in ('project_id', 'session_id', 'session_revision', 'case_key'):
        identifier(checkpoint.get(key), key)
    for key in ('selected_range', 'purpose', 'authorization_ref', 'retention_owner'):
        text(checkpoint.get(key), key)
    timestamp(checkpoint.get('cutoff_at'), 'cutoff_at')
    date.fromisoformat(text(checkpoint.get('retention_review_on'), 'retention_review_on', 10))


def validate_sources(sources):
    require(bool(bounded_list(sources, 'sources', 40)), 'At least one selected source required')
    ids = set()
    for source in sources:
        object_value(source, 'source')
        sid = identifier(source.get('id'), 'source id')
        require(sid not in ids, 'Duplicate source id')
        ids.add(sid)
        require(source.get('kind') in KINDS, 'Unknown source kind')
        require(source.get('origin') in {'human', 'ai_generated', 'mixed', 'unknown'}, 'Source origin required')
        require(source.get('producer') != ORIGIN, 'Reviewer-generated source refused')
        require(source.get('representation') in {'verbatim', 'paraphrase', 'derived_summary'}, 'Representation required')
        require(source.get('confidentiality') in {'private', 'public', 'redacted'}, 'Excluded confidentiality cannot be retained')
        for field in ('author_or_reporter', 'recorded_by', 'language', 'reference', 'locator', 'version', 'environment'):
            text(source.get(field), 'source ' + field)
        text(source.get('excerpt'), 'excerpt', 12000)
        require(type(source.get('available_for_review')) is bool, 'Availability must be declared')
        date.fromisoformat(text(source.get('date'), 'source date', 10))
        permissions = object_value(source.get('permissions'), 'permissions')
        require(permissions.get('private_review') == 'allowed' and permissions.get('retention') == 'allowed', 'Selected source lacks review or retention permission')
        require(permissions.get('public_sharing') in {'allowed', 'denied', 'unknown'}, 'Sharing permission required')
        text(permissions.get('authorization_ref'), 'source authorization')
        require(source.get('sensitive') is not True, 'Explicitly sensitive input refused; minimize before nomination')
        for ref in bounded_list(source.get('derived_from', []), 'derived_from', 40):
            identifier(ref, 'lineage reference')
    graph = {s['id']: s.get('derived_from', []) for s in sources}
    completed = set()
    def visit(sid, trail):
        require(sid not in trail, 'Cyclic source lineage')
        if sid in completed:
            return
        for parent in graph[sid]:
            require(parent in ids, 'Unknown lineage reference')
            visit(parent, trail | {sid})
        completed.add(sid)
    for sid in ids:
        visit(sid, set())
    return ids


def validate_claims(claims, sources):
    require(bool(bounded_list(claims, 'claims', 20)), 'Manual nomination needs at least one claim')
    by_id = {s['id']: s for s in sources}
    ids = set()
    for claim in claims:
        object_value(claim, 'claim')
        cid = identifier(claim.get('id'), 'claim id')
        require(cid not in ids, 'Duplicate claim id')
        ids.add(cid)
        require(claim.get('kind') in CLAIM_KINDS, 'Unknown claim kind')
        require(claim.get('polarity') in {'asserted', 'negated', 'uncertain'}, 'Explicit claim polarity required')
        for field in ('statement', 'scope', 'allowed_wording'):
            text(claim.get(field), 'claim ' + field)
        for field in ('prohibited_wording', 'missing_proof'):
            strings(claim.get(field, []), field)
        for field in ('supporting_sources', 'contradicting_sources'):
            refs = bounded_list(claim.get(field), field, 40)
            require(len(refs) == len(set(refs)), 'Duplicate claim source links')
            for ref in refs:
                require(ref in by_id, 'Unknown claim source reference')
        require(bool(claim['supporting_sources']), 'Each claim requires a supporting source')
        require(not set(claim['supporting_sources']) & set(claim['contradicting_sources']), 'Same source cannot support and contradict one claim')
        for event in bounded_list(claim.get('verification_events', []), 'verification_events', 20):
            object_value(event, 'verification event')
            for field in ('reviewer', 'method', 'scope', 'receipt_ref', 'result'):
                text(event.get(field), 'verification ' + field)
            timestamp(event.get('checked_at'), 'checked_at')
            require(type(event.get('independently_rerun')) is bool, 'Rerun status required')
            require(event.get('kind') in {'source_read', 'pixels_inspected', 'technical_check', 'participant_observation', 'outcome_measurement'}, 'Unknown verification kind')
    return ids


def content_key(packet):
    # Case identity survives review-date changes; source/claim changes make new content.
    checkpoint = {k: packet['checkpoint'][k] for k in ('project_id', 'session_id', 'session_revision', 'case_key', 'selected_range', 'cutoff_at', 'purpose')}
    return digest({'checkpoint': checkpoint, 'sources': packet['sources'], 'claims': packet['claims']})


def validate_intake(packet, opt_in=False):
    guard(packet, opt_in)
    require(packet.get('record_type') == 'manual-checkpoint', 'Manual checkpoint input required')
    validate_checkpoint(packet.get('checkpoint'))
    validate_sources(packet.get('sources'))
    validate_claims(packet.get('claims'), packet['sources'])
    return packet


def root_sources(sid, sources):
    by_id = {s['id']: s for s in sources}
    visited = set()
    roots = set()
    def visit(current):
        if current in visited:
            return
        visited.add(current)
        parents = by_id[current].get('derived_from', [])
        if not parents:
            roots.add(current)
        for parent in parents:
            visit(parent)
    visit(sid)
    return roots


def lineage_groups(claims, sources):
    return {c['id']: {sid: sorted(root_sources(sid, sources)) for sid in c['supporting_sources']} for c in claims}


def claim_holds(claim, sources):
    selected = {s['id']: s for s in sources}
    holds = list(claim.get('missing_proof', []))
    if claim['contradicting_sources']:
        holds.append('Unresolved contrary sources: narrow or hold this claim')
    if claim['polarity'] == 'uncertain':
        holds.append('Uncertain claim requires qualified wording')
    if any(not selected[s]['available_for_review'] for s in claim['supporting_sources']):
        holds.append('An essential source is unavailable for review')
    roots = set().union(*(root_sources(s, sources) for s in claim['supporting_sources']))
    if all(selected[s]['kind'] == 'memory' for s in roots):
        holds.append('Memory is a recall pointer, not active independent evidence')
    if claim['kind'] == 'measured_outcome' and not any(e['kind'] in {'participant_observation', 'outcome_measurement'} for e in claim.get('verification_events', [])):
        holds.append('Outcome claim has no recorded participant or outcome verification')
    return holds


def nominate(packet, opt_in=False):
    validate_intake(packet, opt_in)
    card = copy.deepcopy(packet)
    card['record_type'] = 'evidence-card'
    card['producer'] = ORIGIN
    ck = card['checkpoint']
    card['card_id'] = 'card-' + digest({k: ck[k] for k in ('project_id', 'session_id', 'case_key')})[:24]
    card['content_key'] = content_key(packet)
    for source in card['sources']:
        source['excerpt_sha256'] = hashlib.sha256(source['excerpt'].encode()).hexdigest()
    card['review'] = {
        'decision': 'held', 'human_confirmed': False, 'human_reviewer': None, 'reviewed_at': None,
        'reason': 'Human review required; manual nomination does not establish credibility.',
        'contribution': '[MISSING INFO: source-backed contribution statement]',
        'rubric': {key: {'status': 'incomplete', 'reason': 'Needs human assessment'} for key in RUBRIC},
        'claim_decisions': {c['id']: 'held' for c in card['claims']},
    }
    card['lifecycle'] = {'state': 'candidate', 'disposition': 'held', 'public_ready': False, 'published': False}
    card['routing_proposals'] = [{'owner': 'project evidence', 'action': 'Review privately before downstream use'}]
    card['holds'] = {c['id']: claim_holds(c, card['sources']) for c in card['claims']}
    card['support_lineage'] = lineage_groups(card['claims'], card['sources'])
    card['accepted_claim_ids'] = [cid for cid, decision in card['review']['claim_decisions'].items() if decision == 'accepted']
    return card


def validate_card(card, opt_in=False):
    object_value(card, 'card')
    packet = copy.deepcopy(card)
    packet['record_type'] = 'manual-checkpoint'
    packet.pop('producer', None)
    validate_intake(packet, opt_in)
    expected = nominate(packet, opt_in)
    require(card.get('record_type') == 'evidence-card' and card.get('producer') == ORIGIN, 'Not an evidence card')
    require(card.get('card_id') == expected['card_id'], 'Card identity mismatch')
    # Stored excerpt hashes are generated data, excluded from source-content identity.
    key_packet = copy.deepcopy(packet)
    for source in key_packet['sources']:
        stored = source.pop('excerpt_sha256', None)
        require(stored == hashlib.sha256(source['excerpt'].encode()).hexdigest(), 'Excerpt integrity mismatch')
    require(card.get('content_key') == content_key(key_packet), 'Content identity mismatch; renominate changed sources/claims')
    review = object_value(card.get('review'), 'review')
    require(review.get('decision') in {'held', 'accepted', 'rejected', 'superseded'}, 'Invalid human decision')
    text(review.get('reason'), 'review reason')
    require(isinstance(review.get('contribution'), str), 'Contribution statement required')
    rubric = object_value(review.get('rubric'), 'rubric')
    for name in RUBRIC:
        dimension = object_value(rubric.get(name), 'rubric ' + name)
        require(dimension.get('status') in {'supported', 'incomplete', 'contradicted', 'not_applicable'}, 'Invalid rubric status')
        text(dimension.get('reason'), 'rubric reason')
    decisions = object_value(review.get('claim_decisions'), 'claim decisions')
    require(set(decisions) == {c['id'] for c in card['claims']}, 'All claims need a disposition')
    require(all(d in {'held', 'accepted', 'rejected'} for d in decisions.values()), 'Invalid claim disposition')
    if review['decision'] != 'held':
        require(review.get('human_confirmed') is True, 'Human confirmation must remain recorded')
        text(review.get('human_reviewer'), 'human reviewer')
        timestamp(review.get('reviewed_at'), 'reviewed_at')
    if review['decision'] == 'accepted':
        text(review['contribution'], 'contribution')
        require('[MISSING INFO' not in review['contribution'], 'Contribution remains missing')
        require(all(d['status'] in {'supported', 'not_applicable'} for d in rubric.values()), 'Unresolved rubric hold')
        require('accepted' in decisions.values(), 'At least one bounded claim must be accepted')
    for claim in card['claims']:
        if decisions[claim['id']] == 'accepted':
            require(review['decision'] == 'accepted', 'Accepted claim needs an accepted human review')
            require(not claim_holds(claim, card['sources']), 'Accepted claim has unresolved evidence holds')
            require(bool(claim.get('verification_events')), 'Accepted claim needs a scoped verification event')
    lifecycle = card.get('lifecycle')
    required_state = 'reviewed' if review['decision'] == 'accepted' else 'candidate'
    require(lifecycle == {'state': required_state, 'disposition': review['decision'], 'public_ready': False, 'published': False}, 'Lifecycle mismatch; publication is a separate workflow')
    # Holds and hashes are recomputed; caller metadata cannot waive policy.
    card = copy.deepcopy(card)
    card['holds'] = {c['id']: claim_holds(c, card['sources']) for c in card['claims']}
    card['support_lineage'] = lineage_groups(card['claims'], card['sources'])
    card['accepted_claim_ids'] = [cid for cid, decision in card['review']['claim_decisions'].items() if decision == 'accepted']
    return card


def apply_review(card, decision, opt_in=False, confirm=False):
    require(confirm is True, 'Human review mutation requires confirmation')
    current = validate_card(card, opt_in)
    object_value(decision, 'human review')
    require(decision.get('human_confirmed') is True, 'Explicit human confirmation required')
    current['review'] = {k: decision.get(k) for k in ('decision', 'human_confirmed', 'human_reviewer', 'reviewed_at', 'reason', 'contribution', 'rubric', 'claim_decisions')}
    current['lifecycle'] = {'state': 'reviewed' if decision.get('decision') == 'accepted' else 'candidate', 'disposition': decision.get('decision'), 'public_ready': False, 'published': False}
    return validate_card(current, opt_in)
