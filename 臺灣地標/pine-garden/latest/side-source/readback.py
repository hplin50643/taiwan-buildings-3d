import bpy,sys,struct,json
from pathlib import Path
q=Path(sys.argv[sys.argv.index('--')+1])
b=(q/'model.stl').read_bytes()
a=json.loads((q/'face-material-map.json').read_text())
ids=set().union(*json.loads((q/'side-face-proof.json').read_text()).values())
def key(v):
 t=[tuple(float(x) for x in a) for a in v];return min(tuple(t[i:]+t[:i]) for i in range(3))
ks={key([p[j:j+3] for j in (3,6,9)]):i for i,p in enumerate(struct.iter_unpack('<12fH',b[84:]))}
m=next(o.data for o in bpy.context.scene.objects if o.type=='MESH' and len(o.data.polygons)==5874)
seq=[ks[key([m.vertices[j].co for j in f.vertices])] for f in m.polygons]; assert len(set(seq))==5874
two=set(a['front_masonry'])|ids
one=set(a['roof'])
assert all(f.material_index==(2 if i in two else 1 if i in one else 0) for f,i in zip(m.polygons,seq))
assert not any(i.source in ('FILE','MOVIE','SEQUENCE') for i in bpy.data.images)
print('PASS exact all original oriented triangles, 56 bounded selections and remaining appearances')
