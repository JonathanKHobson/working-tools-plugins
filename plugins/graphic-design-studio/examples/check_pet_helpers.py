"""Exercise deterministic pet helpers with mechanical fixtures, not generated pet art."""
from pathlib import Path
import argparse,json,subprocess,sys,hashlib
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];SCRIPTS=ROOT/'skills/hatch-pet/scripts'
COUNTS={'idle':6,'running-right':8,'running-left':8,'waving':4,'jumping':5,'failed':8,'waiting':6,'running':6,'review':6}
def invoke(script,*args):
    r=subprocess.run([sys.executable,'-B',str(SCRIPTS/script),*map(str,args)],capture_output=True,text=True,timeout=30)
    if r.returncode:raise RuntimeError(r.stderr+r.stdout)
    return r

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);a=parser.parse_args();out=a.output.expanduser().absolute()
    if out.exists():raise ValueError('Output must not already exist')
    invoke('prepare_pet_run.py','--pet-name','Mechanical Fixture','--description','Synthetic geometry test, not pet art','--chroma-key','#FF00FF','--output-dir',out)
    jobs=json.loads((out/'imagegen-jobs.json').read_text());assert len(jobs['jobs'])==10;assert all(j['status']!='complete' for j in jobs['jobs']);before=hashlib.sha256((out/'imagegen-jobs.json').read_bytes()).hexdigest()
    decoded=out/'decoded';decoded.mkdir(exist_ok=True)
    for state,count in COUNTS.items():
        strip=Image.new('RGB',(192*count,208),'#FF00FF');draw=ImageDraw.Draw(strip)
        for i in range(count):
            x=i*192;draw.rectangle((x+48,54,x+144,154),fill=(40,95,150));draw.rectangle((x+54+i*8,100,x+62+i*8,108),fill=(245,190,40))
        strip.save(decoded/(state+'.png'))
    invoke('extract_strip_frames.py','--decoded-dir',decoded,'--output-dir',out/'frames','--states','all','--chroma-key','#FF00FF','--method','components')
    invoke('inspect_frames.py','--frames-root',out/'frames','--json-out',out/'inspection.json','--require-components')
    invoke('compose_atlas.py','--frames-root',out/'frames','--output',out/'atlas.png','--webp-output',out/'atlas.webp')
    invoke('validate_atlas.py',out/'atlas.webp','--json-out',out/'validation.json')
    invoke('make_contact_sheet.py',out/'atlas.webp','--output',out/'contact-sheet.png')
    invoke('render_animation_previews.py','--frames-root',out/'frames','--output-dir',out/'previews')
    valid=json.loads((out/'validation.json').read_text());inspection=json.loads((out/'inspection.json').read_text());assert valid['ok'] and inspection['ok'];assert (valid['width'],valid['height'])==(1536,1872);assert valid['transparent_rgb_residue_pixels']==0
    assert before==hashlib.sha256((out/'imagegen-jobs.json').read_bytes()).hexdigest();assert len(list((out/'previews').glob('*.gif')))==9
    result={'status':'passed','output':str(out),'states':9,'frames':sum(COUNTS.values()),'atlas':[1536,1872],'unused_cells_transparent':True,'transparent_RGB_residue':0,'source_generation_jobs_unchanged':True,'generation_jobs_complete':False,'imagegen_or_native_pet_operation':False,'scope':'Mechanical fixture helpers only; no production pet identity/state/motion acceptance'}
    (out/'sample-receipt.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
