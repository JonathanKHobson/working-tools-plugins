#!/usr/bin/env python3
"""Regenerate MIT synthetic fixture media without remote assets or providers."""
from pathlib import Path
import math
import struct
import wave
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]

def main() -> None:
    assets = ROOT / 'examples/music-slideshow/assets'
    assets.mkdir(parents=True, exist_ok=True)
    fixtures = [('01-wide.png', (960,540), '#193745', '#62D5C8', 'WIDE'),
                ('02-portrait.png', (540,960), '#49263C', '#F1B567', 'PORTRAIT'),
                ('03-square.png', (720,720), '#2B2B56', '#ADABFF', 'SQUARE')]
    for name, size, background, accent, label in fixtures:
        image=Image.new('RGB',size,background);draw=ImageDraw.Draw(image)
        width,height=size; margin=int(min(size)*.12)
        draw.rounded_rectangle((margin,margin,width-margin,height-margin),radius=24,outline=accent,width=8)
        radius=int(min(size)*.19);x,y=width/2,height*.45
        draw.ellipse((x-radius,y-radius,x+radius,y+radius),fill=accent)
        font=ImageFont.load_default(size=round(min(size)*.055))
        draw.text((width/2,height*.77),label,font=font,fill='white',anchor='mm')
        image.save(assets/name)
    rate=48000; duration=8
    with wave.open(str(assets/'music.wav'),'wb') as out:
        out.setnchannels(1);out.setsampwidth(2);out.setframerate(rate)
        samples=[]
        for index in range(rate*duration):
            t=index/rate; edge=min(1,t/.02,(duration-t)/.05)
            pulse=math.exp(-(t%.5)*17)
            value=edge*(.18*math.sin(2*math.pi*220*t)+.10*math.sin(2*math.pi*330*t)+.08*pulse*math.sin(2*math.pi*80*t))
            samples.append(struct.pack('<h',round(32767*value)))
        out.writeframes(b''.join(samples))
    print('Generated three original geometric images and an eight-second synthesized waveform.')

if __name__ == '__main__':
    main()
