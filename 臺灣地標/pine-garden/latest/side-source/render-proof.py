"""Reload exact published scene, remap using exact triangle keys and save current native."""
import bpy,json,struct,hashlib,sys
from pathlib import Path
from mathutils import Vector
q=Path(sys.argv[sys.argv.index('--')+1]); b=(q/'model.stl').read_bytes()
ids=set().union(*json.loads((q/'side-face-proof.json').read_text()).values()); assert len(ids)==56
def key(v):
    t=[tuple(float(x) for x in a) for a in v];return min(tuple(t[i:]+t[:i]) for i in range(3))
lookup={key([p[j:j+3] for j in (3,6,9)]):i for i,p in enumerate(struct.iter_unpack('<12fH',b[84:]))}; assert len(lookup)==5874
s=bpy.context.scene
m=next(o.data for o in s.objects if o.type=='MESH' and len(o.data.polygons)==5874)
seq=[lookup[key([m.vertices[j].co for j in f.vertices])] for f in m.polygons]; assert len(set(seq))==5874
before=[p.material_index for p in m.polygons]
for f,i in zip(m.polygons,seq):
    if i in ids:
        assert f.material_index==0; f.material_index=2
assert len([1 for p,j in zip(m.polygons,before) if p.material_index!=j])==56
assert not any(i.source in ('FILE','MOVIE','SEQUENCE') for i in bpy.data.images)
bpy.context.preferences.filepaths.save_version=0
s.render.filepath='//previews/front.webp'
bpy.ops.wm.save_as_mainfile(filepath=str(q/'current.blend'))

cam=s.camera
views=[('front',(155,-270,150),190,(0,0,27),850),('rear',(-155,270,150),190,(0,0,27),850),('front-elevation',(0,-300,28.7),170,(0,0,28.7),600),('rear-elevation',(0,300,28.7),170,(0,0,28.7),600),('right-end',(300,0,28.7),103,(0,0,28.7),850),('top',(0,0,300),170,(0,0,0),850),('left-end',(-300,0,28.7),103,(0,0,28.7),850)]
for label,loc,scale,target,height in views:
    cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale
    s.render.resolution_y=height;s.render.resolution_x=1200
    s.render.filepath=str(q/(label+'.png'));bpy.ops.render.render(write_still=True)
