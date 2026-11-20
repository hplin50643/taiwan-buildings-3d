"""Run in Blender with the package scene loaded. Checks exact STL geometry; applies the fixed two-face right end."""
from pathlib import Path
import bpy, hashlib, struct
R=Path(__file__).resolve().parent.parent
RAW=(R/'model.stl').read_bytes()
assert hashlib.sha256(RAW).hexdigest()=='011a653987f0afbe774545d63b572ed4696ef1b56e1a872c24e6c5f9129ceac8'
O='Printable_VNU'
NAME='VNU Yucai L nominal right end brick'
HEX='#AF775D'
IDS=[612,615]
N=2948
assert struct.unpack_from('<I',RAW,80)[0]==N
o=bpy.data.objects[O];mesh=o.data
assert len(mesh.polygons)==N
for i,p in enumerate(mesh.polygons):
    assert len(p.vertices)==3 and struct.pack('<9f',*(c for j in p.vertices for c in mesh.vertices[j].co))==RAW[96+50*i:132+50*i]
sRGB=[int(HEX[i:i+2],16)/255 for i in (1,3,5)]
LIN=tuple(k/12.92 if k<=.04045 else ((k+.055)/1.055)**2.4 for k in sRGB)+(1.0,)
assert mesh.materials[0].name=='Warm stone preview only'
have=[p.material_index for p in mesh.polygons]
want=[int(i in IDS) for i in range(N)]
original_orphan=bpy.data.materials.get('Material')
assert original_orphan and original_orphan.users==int(original_orphan.use_fake_user)
original_orphan.use_fake_user=True
if len(mesh.materials)==1:
    assert set(have)=={0} and NAME not in bpy.data.materials
    m=bpy.data.materials.new(NAME);m.diffuse_color=LIN;mesh.materials.append(m)
    for i in IDS:mesh.polygons[i].material_index=1
else:
    assert len(mesh.materials)==2 and mesh.materials[1].name==NAME and have==want
    assert not mesh.materials[1].use_nodes and all(abs(x-y)<1e-7 for x,y in zip(mesh.materials[1].diffuse_color,LIN))
assert [p.material_index for p in mesh.polygons]==want
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(R/'scene.blend'),compress=True)
