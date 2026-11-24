"""Reopen delivered scene and rerender saved front camera; compare temporary PNG bytes against its pinned digest."""
import bpy,json,struct,hashlib,tempfile
from pathlib import Path
A=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(A/'scene.blend'))
with tempfile.TemporaryDirectory() as td:
 p=Path(td)/'front.png';bpy.context.scene.render.filepath=str(p);bpy.ops.render.render(write_still=True)
 raw=p.read_bytes();clean=raw[:8];pos=8
 while pos<len(raw):
  n=struct.unpack('>I',raw[pos:pos+4])[0];kind=raw[pos+4:pos+8]
  if kind not in [b'tEXt',b'zTXt',b'iTXt',b'eXIf']:clean+=raw[pos:pos+n+12]
  pos+=n+12
 v=next(r for r in json.loads((A/'qa/render-manifest.json').read_text())['files'] if r['path']=='previews/front-full.webp')
 archived=v['archival_png']
 assert len(clean)==archived['bytes'] and hashlib.sha256(clean).hexdigest()==archived['sha256']
 assert hashlib.sha256((A/v['path']).read_bytes()).hexdigest()==v['sha256']
print(json.dumps(dict(saved_camera_archived_png_bytes_match=True, archived_sha256=archived['sha256'], current_webp_sha256=v['sha256'])))
