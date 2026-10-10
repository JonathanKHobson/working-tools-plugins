"""Private immutable datasets and revisioned views for the data explorer."""
from __future__ import annotations
import hashlib
from functools import cmp_to_key
from contextlib import contextmanager
import json
import math
import re
import sqlite3
import uuid
from pathlib import Path

KEY = re.compile(r"^[A-Za-z][A-Za-z0-9_]{0,39}$")
ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:-]{0,79}$")

class ExplorerError(ValueError):
    def __init__(self, code, message, current=None):
        super().__init__(message)
        self.code, self.current = code, current

def bad(message): raise ExplorerError('invalid_input', message)
def txt(value, label, limit=160, required=True):
    if not isinstance(value, str) or len(value) > limit or (required and not value.strip()): bad(f'{label} must be nonempty text at most {limit} characters')
    return value.strip()
def canonical(value): return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))

def validate_dataset(title, source_revision, synthetic, columns, rows):
    title, source_revision = txt(title, 'title'), txt(source_revision, 'source_revision', 100)
    if type(synthetic) is not bool: bad('synthetic must be true or false')
    if not isinstance(columns, list) or not 1 <= len(columns) <= 12: bad('columns must contain 1–12 definitions')
    clean_cols=[]; keys=set(); numeric=[]
    for col in columns:
        if not isinstance(col, dict) or set(col)-{'key','label','type','unit'}: bad('invalid column definition')
        key=col.get('key'); label=txt(col.get('label'), 'column label', 80)
        if not isinstance(key,str) or not KEY.fullmatch(key) or key in keys or key=='id': bad('column keys must be unique safe identifiers other than id')
        kind=col.get('type')
        if kind not in ('number','category','text'): bad('column type must be number, category or text')
        unit=col.get('unit')
        if unit is not None and (kind!='number' or not isinstance(unit,str) or len(unit)>30): bad('unit is only available on numeric columns, at most 30 characters')
        keys.add(key); clean_cols.append({'key':key,'label':label,'type':kind,'unit':unit.strip() if unit else None})
        if kind=='number': numeric.append(key)
    if not numeric: bad('at least one numeric column is required')
    if not isinstance(rows,list) or len(rows)>500: bad('rows must contain at most 500 records')
    clean_rows=[]; ids=set()
    for row in rows:
        if not isinstance(row,dict) or set(row)!={'id','values'}: bad('each row needs id and values only')
        rid=row['id']; vals=row['values']
        if not isinstance(rid,str) or not ID.fullmatch(rid) or rid in ids: bad('row ids must be unique, stable identifiers')
        if not isinstance(vals,dict) or set(vals)!=keys: bad('every row must define exactly the declared columns')
        clean={}
        for col in clean_cols:
            key=col['key']; value=vals[key]
            if value is None: clean[key]=None
            elif col['type']=='number':
                if type(value) not in (int,float) or not math.isfinite(value): bad(f'{key} needs a finite number or null')
                clean[key]=value
            elif not isinstance(value,str) or len(value)>120: bad(f'{key} needs text at most 120 characters or null')
            else: clean[key]=value
        ids.add(rid); clean_rows.append({'id':rid,'values':clean})
    dataset={'title':title,'source_revision':source_revision,'synthetic':synthetic,'columns':clean_cols,'rows':clean_rows}
    if len(canonical(dataset).encode())>512_000: bad('dataset exceeds 512 KB')
    return dataset

def default_view(dataset):
    return {'category_column':None,'category_value':None,'numeric_filter':None,'measure':next(c['key'] for c in dataset['columns'] if c['type']=='number'),'sort':{'column':'id','direction':'asc'},'selected_ids':[]}

def validate_view(dataset, view):
    try: return _validate_view(dataset, view)
    except (TypeError, ValueError, KeyError) as exc: bad(f'malformed view: {exc}')

def _validate_view(dataset, view):
    if not isinstance(view,dict) or set(view)!={'category_column','category_value','numeric_filter','measure','sort','selected_ids'}: bad('view must have exactly the declared fields')
    cols={c['key']:c for c in dataset['columns']}; cat=view['category_column']; value=view['category_value']
    if cat is None:
        if value is not None: bad('category_value requires category_column')
    elif not isinstance(cat,str) or cat not in cols or cols[cat]['type']!='category' or (value is not None and (not isinstance(value,str) or len(value)>120)): bad('invalid category filter')
    nf=view['numeric_filter']
    if nf is not None:
        if not isinstance(nf,dict) or set(nf)!={'column','min','max','include_missing'}: bad('invalid numeric filter')
        if not isinstance(nf['column'],str) or nf['column'] not in cols or cols[nf['column']]['type']!='number' or type(nf['include_missing']) is not bool: bad('invalid numeric filter column or missing policy')
        for bound in ('min','max'):
            v=nf[bound]
            if v is not None and (type(v) not in (int,float) or not math.isfinite(v)): bad(f'{bound} must be a finite number or null')
        if nf['min'] is not None and nf['max'] is not None and nf['min']>nf['max']: bad('minimum exceeds maximum')
    measure=view['measure']
    if not isinstance(measure,str) or measure not in cols or cols[measure]['type']!='number': bad('measure must be a numeric column')
    sort=view['sort']
    if not isinstance(sort,dict) or set(sort)!={'column','direction'} or not isinstance(sort['column'],str) or sort['column'] not in {'id',*cols} or sort['direction'] not in ('asc','desc'): bad('invalid sort')
    ids=view['selected_ids']
    if not isinstance(ids,list) or len(ids)>500 or any(not isinstance(i,str) for i in ids) or len(ids)!=len(set(ids)): bad('selected_ids must be unique ids')
    present={row['id'] for row in dataset['rows']}
    if any(i not in present for i in ids): bad('selected_ids contains an unknown row')
    return view

def compute(dataset, view):
    validate_view(dataset,view)
    filtered=[]; nf=view['numeric_filter']; cat=view['category_column']
    for row in dataset['rows']:
        vals=row['values']
        if cat is not None and vals[cat]!=view['category_value']: continue
        if nf:
            n=vals[nf['column']]
            if n is None:
                if not nf['include_missing']: continue
            elif (nf['min'] is not None and n<nf['min']) or (nf['max'] is not None and n>nf['max']): continue
        filtered.append(row)
    sort=view['sort']; key=sort['column']
    def compare(a,b):
        av=a['id'] if key=='id' else a['values'][key]
        bv=b['id'] if key=='id' else b['values'][key]
        if av is None or bv is None:
            primary=0 if av is bv else (1 if av is None else -1)
        else:
            primary=(av>bv)-(av<bv)
            if sort['direction']=='desc': primary=-primary
        return primary or (a['id']>b['id'])-(a['id']<b['id'])
    filtered.sort(key=cmp_to_key(compare))
    numbers=[r['values'][view['measure']] for r in filtered if r['values'][view['measure']] is not None]
    mean=None
    if numbers:
        mean=0.0
        for index,n in enumerate(numbers,1): mean+=n/index-mean/index
        if not math.isfinite(mean): bad('computed mean is not finite')
    count=len(filtered); known=len(numbers); selected=set(view['selected_ids']); visible_ids={r['id'] for r in filtered}
    return {'row_count':count,'known_count':known,'missing_count':count-known,'min':min(numbers) if numbers else None,'max':max(numbers) if numbers else None,'mean':mean,'denominator':known,'selected_ids':view['selected_ids'],'selected_visible_ids':[r['id'] for r in filtered if r['id'] in selected],'selected_hidden_ids':[i for i in view['selected_ids'] if i not in visible_ids]}

class ExplorerStore:
    def __init__(self, data_dir):
        candidate=Path(data_dir).expanduser()
        if candidate.is_symlink(): raise ExplorerError('storage_error','Data directory cannot be a symlink')
        existed=candidate.exists()
        candidate.mkdir(parents=True,exist_ok=True,mode=0o700)
        if not candidate.is_dir() or (candidate.stat().st_mode & 0o077): raise ExplorerError('storage_error','Data directory must be private (mode 0700)')
        self.path=candidate.resolve()
        self.db=self.path/'explorer.sqlite3'
        if self.db.is_symlink(): raise ExplorerError('storage_error','Database path cannot be a symlink')
        with self.connect() as db:
            db.execute('CREATE TABLE IF NOT EXISTS datasets (id TEXT PRIMARY KEY, data TEXT NOT NULL, view TEXT NOT NULL, revision INTEGER NOT NULL)')
            db.execute('CREATE TABLE IF NOT EXISTS operations (dataset_id TEXT NOT NULL, operation_id TEXT NOT NULL, fingerprint TEXT NOT NULL, result TEXT NOT NULL, PRIMARY KEY(dataset_id,operation_id))')
    @contextmanager
    def connect(self):
        if self.db.is_symlink(): raise ExplorerError('storage_error','Database path cannot be a symlink')
        db=sqlite3.connect(self.db,timeout=5); self.db.chmod(0o600); db.row_factory=sqlite3.Row
        try:
            with db: yield db
        finally: db.close()
    def create(self, title, source_revision, synthetic, columns, rows):
        data=validate_dataset(title,source_revision,synthetic,columns,rows); did=str(uuid.uuid4()); view=default_view(data)
        with self.connect() as db: db.execute('INSERT INTO datasets VALUES (?,?,?,?)',(did,canonical(data),canonical(view),1))
        return self._package(did,data,view,1,include_rows=False)
    def _load(self,db,did):
        if not isinstance(did,str) or not ID.fullmatch(did): bad('invalid dataset_id')
        record=db.execute('SELECT * FROM datasets WHERE id=?',(did,)).fetchone()
        if not record: raise ExplorerError('not_found','Dataset not found')
        return json.loads(record['data']),json.loads(record['view']),record['revision']
    def _package(self,did,data,view,revision,include_rows):
        output={'dataset_id':did,'title':data['title'],'source_revision':data['source_revision'],'synthetic':data['synthetic'],'columns':data['columns'],'revision':revision,'view':view,'aggregate':compute(data,view)}
        if include_rows: output['rows']=data['rows']
        return output
    def read(self,did,include_rows=False):
        with self.connect() as db: data,view,rev=self._load(db,did)
        return self._package(did,data,view,rev,include_rows)
    def save(self,did,expected_revision,operation_id,view):
        if type(expected_revision) is not int or expected_revision<1: bad('expected_revision must be a positive integer')
        if not isinstance(operation_id,str) or not ID.fullmatch(operation_id): bad('operation_id must be a stable unique identifier')
        fp=hashlib.sha256(canonical({'expected_revision':expected_revision,'view':view}).encode()).hexdigest()
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            prior=db.execute('SELECT * FROM operations WHERE dataset_id=? AND operation_id=?',(did,operation_id)).fetchone()
            if prior:
                if prior['fingerprint']!=fp: raise ExplorerError('operation_reused','operation_id was used with different content')
                return json.loads(prior['result'])
            data,current,rev=self._load(db,did)
            validate_view(data,view)
            if rev!=expected_revision: raise ExplorerError('conflict','Saved view changed; preserve your draft and refresh explicitly',self._package(did,data,current,rev,True))
            result=self._package(did,data,view,rev+1,True)
            db.execute('UPDATE datasets SET view=?,revision=? WHERE id=?',(canonical(view),rev+1,did))
            db.execute('INSERT INTO operations VALUES (?,?,?,?)',(did,operation_id,fp,canonical(result)))
            return result
