"""Exercise the full packet CLI with synthetic evidence and deliberate failures."""
from pathlib import Path
import csv,json,subprocess,sys,hashlib
import pytest
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];HELPER=ROOT/'skills/loom-review-packet/scripts/loom_review_packet.py'
def call(*args):return subprocess.run([sys.executable,'-B',str(HELPER),*map(str,args)],capture_output=True,text=True,timeout=10)
def inputs(tmp_path,missing=False):
    source=tmp_path/'source';source.mkdir();transcript=source/'transcript.txt';transcript.write_text('0:00 Draft cue.\n0:01 Saved cue.\n');Image.new('RGB',(32,24),'red').save(source/'draft.png');Image.new('RGB',(32,24),'green').save(source/'saved.png');cues=source/'cues.csv'
    with cues.open('w',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=['timestamp','topic','screenshot','observation','question','recommendation']);writer.writeheader();writer.writerow({'timestamp':'0:01','topic':'saved','screenshot':'' if missing else 'saved.png','observation':'Synthetic saved label','question':'Persistence unverified','recommendation':'Test actual save'});writer.writerow({'timestamp':'0:00','topic':'draft','screenshot':'draft.png','observation':'Synthetic draft label'})
    return source,transcript,cues

def test_timestamp_extraction_preserves_original(tmp_path):
    raw=tmp_path/'raw.txt';text='0:04 First state\n1:02:03 Later state';raw.write_text(text);result=call('extract','--transcript',raw,'--output',tmp_path/'timestamps.csv');assert result.returncode==0
    rows=list(csv.DictReader((tmp_path/'timestamps.csv').open()));assert [int(r['seconds']) for r in rows]==[4,3723];assert raw.read_text()==text

def test_invalid_timestamp_and_no_timestamp_fail_without_derivative(tmp_path):
    for text in ['0:99 invalid','No timed source']:
        raw=tmp_path/'raw.txt';raw.write_text(text);result=call('extract','--transcript',raw,'--output',tmp_path/'out.csv');assert result.returncode==1;assert not (tmp_path/'out.csv').exists()

def test_complete_sorted_copies_hashes_feedback_and_collision(tmp_path):
    source,transcript,cues=inputs(tmp_path);before={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in source.iterdir()};out=tmp_path/'packet';argv=['build','--title','Synthetic review','--transcript',transcript,'--cues',cues,'--screenshots-dir',source,'--output',out];result=call(*argv);assert result.returncode==0,result.stderr
    manifest=json.loads((out/'manifest.json').read_text());assert manifest['status']=='complete';assert manifest['frameCount']==manifest['cueCount']==2;assert [x['seconds'] for x in manifest['cues']]==[0,1]
    for cue in manifest['cues']:
        assert ':' not in cue['frame'];frame=out/cue['frame'];assert hashlib.sha256(frame.read_bytes()).hexdigest()==cue['frameSha256'];assert frame.read_bytes()==Path(cue['frameSource']).read_bytes()
    feedback=(out/'ux-feedback.md').read_text();assert all('**'+s+':**' in feedback for s in ['Observation','Question','Recommendation']);assert (out/'transcript/raw.txt').read_bytes()==transcript.read_bytes();assert before=={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in source.iterdir()};assert call(*argv).returncode==1

def test_missing_frames_require_explicit_partial_staging(tmp_path):
    source,transcript,cues=inputs(tmp_path,missing=True);out=tmp_path/'packet';argv=['build','--title','Synthetic partial','--transcript',transcript,'--cues',cues,'--screenshots-dir',source,'--output',out]
    assert call(*argv).returncode==1;assert not out.exists();result=call(*argv,'--allow-missing');assert result.returncode==2;manifest=json.loads((out/'manifest.json').read_text());assert manifest['status']=='partial' and (manifest['cueCount'],manifest['frameCount'])==(2,1)
