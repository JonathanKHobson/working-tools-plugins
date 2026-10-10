"""Run the bundled live-card checker on a fictional card and deliberate failure."""
from pathlib import Path
import json,subprocess,sys,tempfile,hashlib
ROOT=Path(__file__).resolve().parents[1]
card=ROOT/'examples/live-run-card.txt';text=card.read_text();before=hashlib.sha256(card.read_bytes()).hexdigest()
with tempfile.TemporaryDirectory(prefix='game-live-card-') as cwd:
    cli=[sys.executable,'-B',str(ROOT/'skills/live-table-director/scripts/check_live_output.py')]
    valid=subprocess.run(cli,input=text,text=True,capture_output=True,cwd=cwd,timeout=5)
    invalid=subprocess.run(cli,input=text.replace('WATCH:',''),text=True,capture_output=True,cwd=cwd,timeout=5)
    assert valid.returncode==0 and invalid.returncode==1
    assert 'missing marker: WATCH:' in invalid.stderr
    assert not list(Path(cwd).iterdir()) and before==hashlib.sha256(card.read_bytes()).hexdigest()
    print(json.dumps({'status':'passed','valid':valid.stdout.strip(),'missing_watch_rejected':True,'input_unchanged':True,'writes':0,'actual_game_or_VTT_operation':False}))
