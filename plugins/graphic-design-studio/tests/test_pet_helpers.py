"""Regression checks for deterministic helpers, with no image-provider/native-pet operation."""
from pathlib import Path
import importlib.util,json,subprocess,sys,tempfile,unittest
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/'skills/hatch-pet/scripts'
COUNTS=[6,8,8,4,5,8,6,6,6]

def invoke(name,*args):
    return subprocess.run([sys.executable,'-B',str(SCRIPTS/name),*map(str,args)],capture_output=True,text=True,timeout=30)

class PetHelpers(unittest.TestCase):
    def test_preparation_preserves_generation_hold(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'run'
            result=invoke('prepare_pet_run.py','--pet-name','Geometry Fixture','--description','Test geometry only','--output-dir',out)
            self.assertEqual(result.returncode,0,result.stderr)
            jobs=json.loads((out/'imagegen-jobs.json').read_text())['jobs']
            self.assertEqual(len(jobs),10)
            self.assertTrue(all(job['status']!='complete' for job in jobs))
            self.assertEqual(len(list((out/'references/layout-guides').glob('*.png'))),9)
            before=(out/'imagegen-jobs.json').read_bytes()
            result=invoke('derive_running_left_from_running_right.py','--run-dir',out,'--decision-note','Synthetic test only')
            self.assertNotEqual(result.returncode,0)
            self.assertIn('refusing to mirror',result.stderr)
            self.assertEqual((out/'imagegen-jobs.json').read_bytes(),before)

    def test_mirror_keeps_temporal_order(self):
        spec=importlib.util.spec_from_file_location('mirror_helper',SCRIPTS/'derive_running_left_from_running_right.py')
        mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
        image=Image.new('RGBA',(80,4),(0,0,0,0))
        for index in range(8):
            image.putpixel((index*10+1,1),(index+1,100,200,255))
        result=mod.mirror_strip_preserving_frame_order(image)
        for index in range(8):
            self.assertEqual(result.getpixel((index*10+8,1)),(index+1,100,200,255))
            self.assertEqual(result.getpixel((index*10+1,1)),(0,0,0,0))

    def test_atlas_accepts_layout_and_rejects_unused_pixel_and_empty_used_cell(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp);atlas=Image.new('RGBA',(1536,1872),(0,0,0,0));draw=ImageDraw.Draw(atlas)
            for row,count in enumerate(COUNTS):
                for col in range(count):
                    x=col*192;y=row*208;draw.rectangle((x+40,y+40,x+100,y+100),fill=(30,90,150,255))
            path=out/'valid.png';atlas.save(path)
            result=invoke('validate_atlas.py',path,'--json-out',out/'valid.json')
            self.assertEqual(result.returncode,0,result.stdout+result.stderr)
            self.assertTrue(json.loads((out/'valid.json').read_text())['ok'])
            invalid=atlas.copy();invalid.putpixel((7*192,0),(10,20,30,255));invalid.save(out/'invalid-unused.png')
            result=invoke('validate_atlas.py',out/'invalid-unused.png','--json-out',out/'unused.json')
            self.assertNotEqual(result.returncode,0)
            self.assertIn('unused column',str(json.loads((out/'unused.json').read_text())['errors']))
            invalid=atlas.copy();invalid.paste((0,0,0,0),(0,0,192,208));invalid.save(out/'empty-used.png')
            result=invoke('validate_atlas.py',out/'empty-used.png','--json-out',out/'empty.json')
            self.assertNotEqual(result.returncode,0)
            self.assertIn('empty or too sparse',str(json.loads((out/'empty.json').read_text())['errors']))

    def test_atlas_wrong_dimensions_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'tiny.png';Image.new('RGBA',(192,208),(0,0,0,0)).save(path)
            result=invoke('validate_atlas.py',path,'--json-out',Path(tmp)/'result.json')
            self.assertNotEqual(result.returncode,0)
            self.assertIn('expected 1536x1872',str(json.loads((Path(tmp)/'result.json').read_text())['errors']))

if __name__=='__main__':unittest.main()
