"""Run in Blender: blender -b ORIGINAL_SCENE --python apply_side_color.py -- OUTPUT_SCENE"""
from pathlib import Path
import bpy,json,numpy as np,sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from rebuild_exchange import OBJECT,NAME,HEX,IDS,NPZ,OLD_PALETTE,sha
src=Path(__file__).resolve().parent
target=Path(sys.argv[sys.argv.index('--')+1]).resolve()
assert bpy.data.filepath and target.suffix=='.blend'
meshfile=src/'color-mesh.npz';d=np.load(meshfile)
s=bpy.data.objects[OBJECT];m=s.data
assert np.array_equal(np.array([list(v.co) for v in m.vertices],dtype=np.float32),d['vertices'].astype(np.float32))
assert np.array_equal(np.array([list(p.vertices) for p in m.polygons]),d['faces'])
assert [m.materials[i].name for i in (0,1)]==[x[0] for x in OLD_PALETTE]
target_metadata=sha(meshfile)
old=d['materials'].copy();old[IDS]=1
new=d['materials']
assert np.flatnonzero(new==2).tolist()==IDS
have=[p.material_index for p in m.polygons]
rgb=tuple(int(HEX[i:i+2],16)/255 for i in (1,3,5))
rgba=tuple(x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in rgb)+(1.0,)
if len(m.materials)==2:
    assert have==old.tolist() and s.get('source_mesh_sha256')==NPZ and NAME not in bpy.data.materials
    add=bpy.data.materials.new(NAME);add.diffuse_color=rgba;add.use_nodes=True
    bsdf=add.node_tree.nodes.get('Principled BSDF');bsdf.inputs['Base Color'].default_value=rgba;bsdf.inputs['Roughness'].default_value=.71
    m.materials.append(add)
    for i in IDS:m.polygons[int(i)].material_index=2
else:
    assert len(m.materials)==3 and m.materials[2].name==NAME and have==new.tolist()
    assert np.allclose(m.materials[2].diffuse_color,rgba,atol=1e-7) and s.get('source_mesh_sha256')==target_metadata
s['source_mesh_sha256']=target_metadata
assert [p.material_index for p in m.polygons]==new.tolist()
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(target),compress=True)
