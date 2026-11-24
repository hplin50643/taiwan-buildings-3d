"""Original 3926 triangles unchanged; source-supported exact exposed planes only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;expected='de7f24a7c25d7f5c5344f0f0887718080a7b0201a07b42d2bea4d1100d2508b2';assert hashlib.sha256((R/'model.stl').read_bytes()).hexdigest()==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==3926
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.full(len(t),2,np.int32)
def plane(axis,value):return (np.max(abs(t[:,:,axis]-value),axis=1)<.003)&(m.face_normals[:,axis]<-.99)
def span(axis,low,high):return (lo[:,axis]>=low-.003)&(hi[:,axis]<=high+.003)
bands=np.zeros(len(t),bool);edges=bands.copy();counts=[]
for z in [15,25,35,45,55,65,75,85]:
 b=plane(1,-20.95)&span(0,-65.5,65.5)&span(2,z-2,z-.6);bands|=b;counts.append(int(b.sum()))
 edges|=plane(0,-67)&span(1,-19.5,29.5)&span(2,z-2,z-.8)
bar=plane(1,-26.4)&span(0,55.4,56.6)&span(2,4,94)
assert counts==[6,4,4,4,4,4,4,4] and bar.sum()==18
assert edges.sum()==16
assert not np.any((bands|edges)&bar)
a[bands|edges]=0;a[bar]=1
pal=[('Observed exposed floorband edges gray','#BCBFBB'),('Observed central front stair mullion dark gray','#48504D'),('UNVERIFIED brick mixed panes rear roof neutral','#B8BAB5')]
original=a.copy()
added=plane(1,-22)&span(0,45.5,62.5)&span(2,109,110.5)
assert np.flatnonzero(added).tolist()==[3866,3868]
assert (original[added]==2).all()
a[added]=0
assert np.array_equal(a[~added],original[~added])
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'3926 original triangles unchanged; no new or split faces','domains':{'front_bands':int(bands.sum()),'left_slab_edges':int(edges.sum()),'tower_central_front_bar':int(bar.sum()),'service_tower_cap_front':int(added.sum())},'limitations':['Exact exposed planes only; mixed panes and continuous brick/gray walls neutral.','Photo capture dates unknown;2023 form and2025 PDF edition are not capture dates.','Material labels are not a verified multi-filament slicing job.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':3926,'original_STL_sha256':expected,'color_mesh_sha256':hashlib.sha256((R/'color-mesh.npz').read_bytes()).hexdigest()},indent=2));print(np.unique(a,return_counts=True))
