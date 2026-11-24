#!/usr/bin/env python3
"""Verify native delivery checksums and the chapel's six full-size WebP previews."""
import hashlib,json
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def verify():
 proof=json.loads((R/'display-proof.json').read_text(encoding='utf-8'))
 rows=proof['current_preview_pixels']; expect={f'previews/{s}-current.webp' for s in ('front','rear','elevation','top','left','right')}
 if len(rows)!=6 or {x['path'] for x in rows}!=expect:raise ValueError('Unexpected preview list.')
 native={'model.stl','model-colored.3mf','scene.blend'}
 if set(proof['current_native_sha256'])!=native:raise ValueError('Unexpected native-model list.')
 for p,want in proof['current_native_sha256'].items():
  if sha((R/p).read_bytes())!=want:raise ValueError(f'{p}: native model SHA-256 differs')
 for x in rows:
  p=R/x['path']; b=p.read_bytes()
  if len(b)!=x['bytes'] or sha(b)!=x['webp_sha256']:raise ValueError(f'{p.name}: WebP file size or SHA-256 differs')
  with Image.open(p) as im:
   if im.format!='WEBP' or list(im.size)!=x['dimensions']:raise ValueError(f'{p.name}: image format or dimensions differ')
   if sha(im.convert('RGBA').tobytes())!=x['rgba_sha256']:raise ValueError(f'{p.name}: decoded RGBA SHA-256 differs')
 print('Verified six WebP file/pixel hashes and three native-model hashes.')
if __name__=='__main__':verify()
