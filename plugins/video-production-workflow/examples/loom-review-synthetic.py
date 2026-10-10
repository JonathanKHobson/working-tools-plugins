"""Assemble a real review packet from wholly synthetic inputs; no account/network."""
from pathlib import Path
import argparse,csv,json,subprocess,sys,shutil,hashlib
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);parser.add_argument('--capture',action='store_true');args=parser.parse_args()
    output=args.output.expanduser().absolute()
    if output.exists():raise ValueError('Synthetic example output must not already exist')
    output.mkdir(parents=True);source=output/'synthetic-inputs';source.mkdir()
    transcript=source/'transcript.txt';transcript.write_text('0:00 Synthetic draft label.\n0:01 Synthetic saved label; persistence is not demonstrated.\n')
    for index,(label,color) in enumerate([('DRAFT','#fff2cf'),('SAVED','#d9f0e7')]):
        image=Image.new('RGB',(640,360),color);draw=ImageDraw.Draw(image);draw.text((30,30),'FICTIONAL REVIEW FIXTURE',fill='black');draw.text((30,90),label,fill='black');image.save(source/f'scene{index:03d}.png')
    cues=source/'cues.csv'
    with cues.open('w',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=['timestamp','topic','screenshot','observation','question','recommendation']);writer.writeheader()
        for index,label in [(1,'SAVED'),(0,'DRAFT')]:writer.writerow({'timestamp':f'0:0{index}','topic':label.lower(),'screenshot':'' if args.capture else f'scene{index:03d}.png','observation':f'Synthetic frame label is {label}.','question':'Does the real product persist this state?','recommendation':'Verify real save behavior separately.'})
    helper=ROOT/'skills/loom-review-packet/scripts/loom_review_packet.py';cli=[sys.executable,'-B',str(helper)]
    subprocess.run(cli+['extract','--transcript',str(transcript),'--output',str(source/'timestamps.csv')],check=True,capture_output=True,text=True)
    argv=cli+['build','--title','Fictional draft and saved state review','--author','Synthetic reviewer','--source-url','https://example.org/fictional-review','--transcript',str(transcript),'--cues',str(cues),'--output',str(output/'packet')]
    if args.capture:
        ffmpeg=shutil.which('ffmpeg')
        if not ffmpeg:raise ValueError('--capture requires separately installed ffmpeg on PATH')
        video=source/'synthetic.mp4';subprocess.run([ffmpeg,'-hide_banner','-loglevel','error','-framerate','1','-i',str(source/'scene%03d.png'),'-c:v','libx264','-pix_fmt','yuv420p','-y',str(video)],check=True);argv+=['--video',str(video)]
    else:argv+=['--screenshots-dir',str(source)]
    before=hashlib.sha256(transcript.read_bytes()).hexdigest();run=subprocess.run(argv,check=True,capture_output=True,text=True);manifest=json.loads((output/'packet/manifest.json').read_text());assert manifest['status']=='complete' and manifest['cueCount']==manifest['frameCount']==2;assert [x['seconds'] for x in manifest['cues']]==[0,1]
    assert before==hashlib.sha256(transcript.read_bytes()).hexdigest();assert (output/'packet/transcript/raw.txt').read_bytes()==transcript.read_bytes()
    for cue in manifest['cues']:assert hashlib.sha256((output/'packet'/cue['frame']).read_bytes()).hexdigest()==cue['frameSha256']
    print(json.dumps({'status':'passed','packet':str(output/'packet'),'frames':2,'sorted_cues':True,'input_unchanged':True,'frame_mode':'capture' if args.capture else 'copy','real_recording_or_UX_persistence':False,'rendered_packet_or_host_delivery_verified':False}))
if __name__=='__main__':main()
