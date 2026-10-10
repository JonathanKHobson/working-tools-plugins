"""Exercise real PDF size/text/type checks on temporary fictional data."""
from pathlib import Path
import tempfile,subprocess,sys,json,hashlib
import fitz
ROOT=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='graphic-preflight-') as directory:
    pdf=Path(directory)/'fictional.pdf';doc=fitz.open();page=doc.new_page(width=612,height=792)
    page.insert_text((54,80),'FICTIONAL WORKSHOP',fontsize=22)
    page.insert_text((54,125),'Synthetic check. Not a real event.',fontsize=14)
    doc.save(pdf);doc.close();before=hashlib.sha256(pdf.read_bytes()).hexdigest()
    cli=[sys.executable,str(ROOT/'skills/print-and-export-preflight/scripts/pdf_preflight.py'),str(pdf)]
    good=subprocess.run(cli+['--size-in','8.5','11','--min-type-pt','12','--require-text','FICTIONAL WORKSHOP'],capture_output=True,text=True)
    bad=subprocess.run(cli+['--size-in','11','17','--require-text','Missing required fact'],capture_output=True,text=True)
    assert good.returncode==0 and bad.returncode==1
    assert before==hashlib.sha256(pdf.read_bytes()).hexdigest()
    print(json.dumps({'status':'passed','good':json.loads(good.stdout)['result'],'bad':json.loads(bad.stdout)['result'],'input_unchanged':True,'physical_print_verified':False}))
