import bpy,json,struct,hashlib
from pathlib import Path
P=Path(__file__).resolve().parent.parent
bpy.ops.wm.open_mainfile(filepath=str(P/'scene.blend'));bpy.context.preferences.filepaths.save_version=0
o=bpy.data.objects['Printable_Meiho'];assert len(o.data.polygons)==3546
raw=b''.join(struct.pack('<9f',*(v for i in p.vertices for v in o.data.vertices[i].co))for p in o.data.polygons)
assert hashlib.sha256(raw).hexdigest()=='4d67614c82b5d8796787c4a9cc4b95656dfc8026554453a27febf6b40f90f4ad'
ids=json.loads((P/'side-color-domain.json').read_text())['check'][0]['faces'];assert len(ids)==40
name='Nominal salmon spandrel - 40 side faces';assert o.data.materials[0].name=='Warm stone preview only';assert len(o.data.materials)in [1,2]
if len(o.data.materials)==1:
 assert all(p.material_index==0 for p in o.data.polygons)
 m=bpy.data.materials.new(name);m.diffuse_color=(.57,.32,.23,1);o.data.materials.append(m)
else:
 assert o.data.materials[1].name==name;assert all(abs(x-y)<1e-7 for x,y in zip(o.data.materials[1].diffuse_color,(.57,.32,.23,1)))
 assert all(p.material_index==(1 if p.index in ids else 0)for p in o.data.polygons)
for m in bpy.data.materials:
 if m.users==0:m.use_fake_user=True
for i in ids:o.data.polygons[i].material_index=1
bpy.ops.wm.save_as_mainfile(filepath=str(P/'scene.blend'))
