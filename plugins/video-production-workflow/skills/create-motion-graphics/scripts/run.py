#!/usr/bin/env python3
import argparse,json
p=argparse.ArgumentParser(); p.add_argument('--kind',choices=['simple-overlay','ui-motion','explainer','math','3d','react-system'],required=True); a=p.parse_args(); choices={'simple-overlay':'FFmpeg/PIL','ui-motion':'HyperFrames','explainer':'Motion Canvas','math':'Manim','3d':'Blender','react-system':'Remotion (license check required)'}; print(json.dumps({'recommended':choices[a.kind]},indent=2))
