"""Output-based acceptance for incorporated methods; never runs an AI model.

Package validation and source_inventory remain the distribution/parity owners.
This gate binds reviewed method/support content, actual trial outputs and host
readbacks. Unchanged relevant content reuses its exact receipt.
"""
from __future__ import annotations
import hashlib
import importlib.util
import json
from pathlib import Path
import re

METHOD_PRODUCTS = {'ux-design-toolkit','writing-quality-studio','career-studio',
                   'research-methodology-local','prompt-playbook-studio',
                   'master-security-toolkit','creative-writing-studio',
                   'marketing-strategy-studio','social-content-studio',
                   'instructional-design-studio','work-management'}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def value_hash(value):
    return digest(json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())


def read_json(path):
    return json.loads(Path(path).read_text())


def safe_path(root, relative):
    if not isinstance(relative,str) or not relative:
        raise ValueError('Unsafe acceptance path: '+str(relative))
    p=Path(relative)
    if p.is_absolute() or '..' in p.parts:
        raise ValueError('Unsafe acceptance path: '+str(relative))
    path=root/p
    if not path.resolve().is_relative_to(root.resolve()) or path.is_symlink():
        raise ValueError('Acceptance path escapes source: '+relative)
    if not path.is_file():
        raise ValueError('Required method/support disappeared: '+relative)
    return path


def load_manifest(root):
    manifest=read_json(root/'catalog/method-acceptance.json')
    if manifest.get('schema_version')!=1:
        raise ValueError('Unsupported method acceptance manifest')
    caps=manifest.get('capabilities',[])
    if not caps or len({x['id'] for x in caps})!=len(caps):
        raise ValueError('Invalid method acceptance capabilities')
    return manifest


def affected_capabilities(manifest, entries):
    selected=[]
    for cap in manifest['capabilities']:
        for entry in entries:
            if entry['id'] not in cap['products']:continue
            changed=entry.get('changed_files')
            # Unknown change scope requires the capability's existing receipt.
            if changed is None:
                selected.append(cap);break
            paths={'plugins/'+entry['id']+'/'+p for p in changed}
            if any(p in cap['sources'] or any(p.startswith(d+'/') for d in cap.get('watched_dirs',[])) for p in paths):
                selected.append(cap);break
    return selected


def _layout(root, cap):
    files=set()
    for relative in cap.get('watched_dirs',[]):
        directory=root/relative
        if not directory.is_dir():raise ValueError('Required method directory disappeared: '+relative)
        for p in directory.rglob('*'):
            if p.is_symlink():raise ValueError('Method support symlink: '+str(p))
            if p.is_file() and not any(s in p.parts for s in ('__pycache__','.git','.pytest_cache')) and p.name!='.DS_Store' and not p.name.startswith('._'):
                files.add(p.relative_to(root).as_posix())
    return sorted(files)


def _references(root, relative):
    path=safe_path(root,relative)
    if path.suffix!='.md':return []
    found=set()
    for target in re.findall(r'\]\(([^)]+)\)',path.read_text()):
        target=target.strip().strip('<>').split(' "')[0].split('#')[0]
        if not target or '://' in target:continue
        resolved=(path.parent/target).resolve()
        if resolved.is_relative_to(root.resolve()):
            found.add(resolved.relative_to(root.resolve()).as_posix())
    return sorted(found)


def _ownership_errors(root, cap):
    # Reuse the established catalog rule rather than another retired-name list.
    spec=importlib.util.spec_from_file_location('method_package_rules',root/'scripts/packages.py')
    rules=importlib.util.module_from_spec(spec);spec.loader.exec_module(rules)
    registry=read_json(root/'catalog/packages.json')['packages']
    rows={r['id']:r for r in registry}
    for product in cap['products']:
        row=rows.get(product)
        if row is None:raise ValueError('Required method owner disappeared: '+product)
        errors=rules.method_requirement_errors(row)
        if errors:raise ValueError('; '.join(errors))
        if row.get('requirements',[])!=cap.get('reviewed_requirements',{}).get(product,[]):
            raise ValueError('Unexpected method/execution requirements require review: '+product)


def snapshot(root, manifest, capabilities):
    root=Path(root); cases=read_json(safe_path(root,manifest['cases']))
    criteria=read_json(safe_path(root,manifest['criteria']))['criteria']
    by_id={x['id']:x for x in cases['cases']}
    source_hashes={};case_hashes={};contracts={};case_ids=[];source_lines={};contract_hashes={}
    for cap in capabilities:
        _ownership_errors(root,cap)
        contract_hashes[cap['id']]=value_hash(cap)
        if _layout(root,cap)!=cap['reviewed_layout']:
            raise ValueError('Added/removed method support requires reviewed closure: '+cap['id'])
        for relative in cap['sources']:
            source_hashes[relative]=digest(safe_path(root,relative).read_bytes())
            if _references(root,relative)!=cap.get('reviewed_references',{}).get(relative,[]):
                raise ValueError('Unexpected method requirements/reference closure: '+relative)
        for primary in cap['procedure_sources']:
            if primary not in cap['sources']:raise ValueError('Primary procedure outside reviewed support: '+primary)
            contracts[primary]=source_hashes[primary]
            source_lines[primary]=safe_path(root,primary).read_text().splitlines()
        for case_id in cap['cases']:
            if case_id not in by_id or case_id not in criteria:raise ValueError('Required functional fixture disappeared: '+case_id)
            case_hashes[case_id]=value_hash({'protocol':cases['protocol'],'case':by_id[case_id],'criteria':criteria[case_id]})
            case_ids.append(case_id)
    return {'source_hashes':source_hashes,'case_hashes':case_hashes,
            'procedure_sources':contracts,'procedure_lines':source_lines,'contract_hashes':contract_hashes,'case_ids':sorted(set(case_ids)),
            'criteria':{key:criteria[key] for key in sorted(set(case_ids))}}


def _bound(expected, supplied, label):
    if not isinstance(supplied,dict):raise ValueError('Missing '+label+' binding')
    for key,value in expected.items():
        if supplied.get(key)!=value:raise ValueError('Stale or missing '+label+': '+key)


def _nonempty_text(value, label):
    if not isinstance(value,str) or not value.strip():raise ValueError('Missing '+label)


def validate_trial(state, receipt):
    if receipt.get('schema_version')!=1 or receipt.get('kind')!='executed-model-trial':
        raise ValueError('An actual executed model-trial receipt is required')
    _bound(state['source_hashes'],receipt.get('source_hashes'),'trial source')
    _bound(state['case_hashes'],receipt.get('case_hashes'),'functional fixture')
    _bound(state['contract_hashes'],receipt.get('contract_hashes'),'reviewed capability contract')
    for field in ('run_id','observed_at','provider','exact_model','invocation_evidence_sha256'):
        _nonempty_text(receipt.get(field),field)
    if receipt['exact_model'].lower() in {'opus','sonnet','haiku','default','auto'}:
        raise ValueError('Resolve the actual model identity; a CLI alias is insufficient')
    if not re.fullmatch(r'[a-f0-9]{64}',receipt['invocation_evidence_sha256']):
        raise ValueError('Invalid actual invocation evidence hash')
    if receipt.get('method_only_providers_invoked') is not False:
        raise ValueError('Trial relied on a retired method prerequisite')
    reviewer=receipt.get('reviewer',{})
    _nonempty_text(reviewer.get('identity'),'output reviewer identity')
    if reviewer.get('method')!='source-and-output-review':
        raise ValueError('Output-based independent review is required')
    _nonempty_text(reviewer.get('limitations'),'review limitations')
    reviews=receipt.get('procedure_reviews',{})
    for path,expected_hash in state['procedure_sources'].items():
        review=reviews.get(path,{})
        if review.get('sha256')!=expected_hash or review.get('kind')!='complete-procedure' or review.get('status')!='pass':
            raise ValueError('Method replaced by routing shell or unreviewed procedure: '+path)
        # Source anchors are evidence, not keyword criteria. A router is not a
        # replacement for its declared full procedural destinations.
        source_lines=receipt.get('procedure_source_evidence',{}).get(path,[])
        if not source_lines:raise ValueError('Missing full-procedure source evidence: '+path)
        anchors={}
        for anchor in source_lines:
            start,end=anchor.get('start'),anchor.get('end')
            lines=state['procedure_lines'][path]
            if not isinstance(start,int) or not isinstance(end,int) or start<1 or end<start or end>len(lines):
                raise ValueError('Invalid procedure source range: '+path)
            if anchor.get('quote')!='\n'.join(lines[start-1:end]):
                raise ValueError('Procedure evidence differs from current full source: '+path)
            if not anchor.get('id') or anchor['id'] in anchors:raise ValueError('Invalid procedure source anchor ID')
            anchors[anchor['id']]=anchor
        for dimension in ('inputs','sequence','edge_cases','output','verification'):
            if not isinstance(review.get(dimension),list) or not review[dimension] or any(a not in anchors for a in review[dimension]):
                raise ValueError('Missing procedure contract/source anchor '+dimension+': '+path)
    outputs=receipt.get('outputs',{});evaluations=receipt.get('evaluations',{})
    for case_id in state['case_ids']:
        output=outputs.get(case_id)
        if output is None or output=='' or output=={}:raise ValueError('Missing real output: '+case_id)
        if receipt.get('output_hashes',{}).get(case_id)!=value_hash(output):
            raise ValueError('Actual output changed after review: '+case_id)
        assessment=evaluations.get(case_id,{})
        if assessment.get('status')!='pass' or 'limitations' not in assessment:
            raise ValueError('Functional case failed or unreviewed: '+case_id)
        results=assessment.get('criteria',{})
        if set(results)!=set(state['criteria'][case_id]):
            raise ValueError('Missing/unexpected functional outcomes: '+case_id)
        flat=json.dumps(output,ensure_ascii=False) if not isinstance(output,str) else output
        for ident,result in results.items():
            if result.get('status')!='pass':raise ValueError('Functional outcome not met: '+case_id+'/'+ident)
            _nonempty_text(result.get('reason'),'functional review reason')
            evidence=result.get('output_evidence')
            if not isinstance(evidence,list) or not evidence:raise ValueError('Missing output evidence: '+case_id+'/'+ident)
            for excerpt in evidence:
                if not isinstance(excerpt,str) or len(excerpt.strip())<12 or excerpt not in flat:
                    raise ValueError('Functional evidence is absent from actual output: '+case_id+'/'+ident)


def validate_hosts(state, receipts, required_hosts):
    if not isinstance(receipts,list):raise ValueError('Actual source/package/host agreement receipts are required')
    by_host={x.get('host'):x for x in receipts}
    for host in required_hosts:
        item=by_host.get(host,{})
        if item.get('kind')!='verified-host-method-readback' or item.get('status')!='pass':
            raise ValueError('Missing verified host method agreement: '+host)
        _bound(state['source_hashes'],item.get('source_hashes'),'host method source')
        _bound(state['contract_hashes'],item.get('contract_hashes'),'host capability contract')
        for field in ('observed_at','evidence_sha256'):_nonempty_text(item.get(field),'host '+field)
        for condition in ('package_source_agreement','loaded_method_agreement','retired_prerequisites_absent'):
            if item.get('checks',{}).get(condition) is not True:
                raise ValueError('Source/package/host disagreement: '+host+'/'+condition)
        if not isinstance(item.get('limitations'),list):raise ValueError('Host limitations must be explicit: '+host)


def validate_release(root, config, entries):
    root=Path(root)
    if not any(x['id'] in METHOD_PRODUCTS for x in entries):return {'status':'unaffected','cases':[]}
    manifest=load_manifest(root)
    selected_products={entry['id'] for entry in entries}
    for cap in manifest['capabilities']:
        if selected_products & set(cap['products']):_ownership_errors(root,cap)
    caps=affected_capabilities(manifest,entries)
    if not caps:return {'status':'unaffected-method-content','cases':[]}
    state=snapshot(root,manifest,caps)
    trial_path=config.get('method_acceptance_receipt')
    if not trial_path:raise ValueError('Changed incorporated methods require method_acceptance_receipt; unchanged receipts may be reused')
    validate_trial(state,read_json(trial_path))
    host_path=config.get('method_acceptance_host_receipts')
    if not host_path:raise ValueError('Changed incorporated methods require method_acceptance_host_receipts')
    validate_hosts(state,read_json(host_path),manifest['required_hosts'])
    return {'status':'accepted','cases':state['case_ids'],'source_files':len(state['source_hashes'])}


def prepare_trial(root, products=None):
    """Read-only full source bundle and reviewer snapshot; no model execution."""
    root=Path(root);manifest=load_manifest(root)
    caps=[c for c in manifest['capabilities'] if products is None or set(products)&set(c['products'])]
    state=snapshot(root,manifest,caps)
    cases=read_json(safe_path(root,manifest['cases']))
    bundle={'protocol':cases['protocol'],
            'sources':{p:safe_path(root,p).read_text() for p in sorted(state['source_hashes'])},
            'cases':[case for case in cases['cases'] if case['id'] in state['case_ids']]}
    # Reviewer-only criteria and source anchors are deliberately absent from
    # the generation bundle. Source hashes travel in the separate snapshot.
    return state,bundle


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode',choices=('snapshot','input-bundle'))
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[2])
    parser.add_argument('--product',action='append')
    args=parser.parse_args();state,bundle=prepare_trial(args.root,args.product)
    print(json.dumps(state if args.mode=='snapshot' else bundle,indent=2,ensure_ascii=False))
