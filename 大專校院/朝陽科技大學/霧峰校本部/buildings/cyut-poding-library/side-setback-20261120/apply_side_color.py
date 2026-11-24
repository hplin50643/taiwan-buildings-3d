"""Apply this finite side-wall material to a copy of the existing appearance scene.

blender -b appearance/scene.blend --python side-setback-20261120/apply_side_color.py -- model.stl appearance/face-materials.json side-setback-20261120/scene.blend
"""
from pathlib import Path
import bpy, json, hashlib, struct, sys
d=Path(__file__).resolve().parent
stl,fmap,output=map(Path,sys.argv[sys.argv.index('--')+1:])
raw=stl.read_bytes()
assert hashlib.sha256(raw).hexdigest()=='caac8ffd529735147d3004e1477b9f5da4ffb8b5d3dd3481242b3ec78b9e16c9'
base=json.loads(fmap.read_text())['face_material_indices']
assert (len(base),base.count(0),base.count(1),base.count(2))==(7254,6816,316,122)
obj=bpy.data.objects['CYUT Poding Library limited-scope limited appearance']; m=obj.data
assert len(m.polygons)==struct.unpack_from('<I',raw,80)[0]==7254
assert all(struct.pack('<9f',*(c for k in p.vertices for c in m.vertices[k].co))==raw[96+50*i:132+50*i] for i,p in enumerate(m.polygons))
ids=json.loads((d/'domain-core.json').read_text())[0]['faces']; assert len(ids)==45 and all(base[i]==0 for i in ids)
ids_calc=[p.index for p in m.polygons if all(abs(m.vertices[k].co.y+8*150/166)<1e-5 for k in p.vertices)]
assert ids==ids_calc
new=base.copy()
for i in ids:new[i]=3
prior=['neutral_unconfirmed_structure','opaque_muted_window_proxy','opaque_pale_long_window_band_proxy']
assert [x.name for x in m.materials][:3]==prior
name='CYUT setback wall cool gray stone-like proxy'; rgb=[int('B5BABB'[i:i+2],16)/255 for i in (0,2,4)];rgba=tuple(v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in rgb)+(1.,)
evidence='CYUT official oblique campus photo and public ground panoramas; retain 438 existing window backs, add 45 original south setback wall faces. Source pictures private, none embedded.'
limits='Nominal uncalibrated cool-gray setback wall only; preserve all earlier window materials and original approximate geometry. No extension to mixed curved wall, glazing, roofs or base. No physical print test.'
if len(m.materials)==3:
    assert [p.material_index for p in m.polygons]==base
    mat=bpy.data.materials.new(name);mat.diffuse_color=rgba;mat.use_nodes=True
    bs=mat.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=rgba;bs.inputs['Roughness'].default_value=.86
    m.materials.append(mat)
    for i in ids:m.polygons[i].material_index=3
    obj['evidence']=evidence;obj['limitations']=limits
else:
    assert len(m.materials)==4 and m.materials[3].name==name and obj['evidence']==evidence and obj['limitations']==limits
assert [p.material_index for p in m.polygons]==new
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(output.resolve()),compress=True)
