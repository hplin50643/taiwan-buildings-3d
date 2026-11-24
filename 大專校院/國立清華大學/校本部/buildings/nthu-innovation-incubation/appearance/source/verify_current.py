"""Exact STL/order/material and full central underside rectangle support checks."""
from pathlib import Path
import json,struct,hashlib,zipfile,xml.etree.ElementTree as E
import numpy as np
A=Path(__file__).resolve().parents[1]; R=A.parent
raw=(R/'model.stl').read_bytes();assert hashlib.sha256(raw).hexdigest()=='299656bf3e4e9e65d94a0b4ace96512a289698820cc020f28dca4207076ba5da'
n=struct.unpack_from('<I',raw,80)[0];t=np.array([struct.unpack_from('<9f',raw,96+50*i) for i in range(n)]).reshape(n,3,3)
with zipfile.ZipFile(A/'nthu-innovation-incubation-appearance.3mf') as z:r=E.fromstring(z.read('3D/3dmodel.model'))
ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
v=np.array([[float(x.get(k)) for k in 'xyz'] for x in r.findall('.//m:vertices/m:vertex',ns)])
fs=r.findall('.//m:triangles/m:triangle',ns);f=np.array([[int(x.get(k)) for k in ('v1','v2','v3')] for x in fs]);c=np.array([int(x.get('p1')) for x in fs])
assert np.array_equal(v[f],t);assert np.bincount(c).tolist()==[8650,14,2]
import importlib.util
spec=importlib.util.spec_from_file_location('old',A/'source/build_appearance.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
before,_=old.classify(t); changed=np.flatnonzero(c!=before).tolist();assert changed==[8253,8259]
# Full original-STL analytic plane shared-edge BFS, before the rectangular support test.
normal=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]); normal/=np.linalg.norm(normal,axis=1)[:,None]
plane=(abs(t[:,:,2]-101)<1e-8).all(1)&(normal[:,2]<-.999999)
_,inv=np.unique(t.reshape(-1,3),axis=0,return_inverse=True); original_faces=inv.reshape(-1,3)
from collections import defaultdict
edge_faces=defaultdict(list)
for i in np.flatnonzero(plane):
 for a,b in [(0,1),(1,2),(2,0)]:edge_faces[tuple(sorted((int(original_faces[i,a]),int(original_faces[i,b]))))].append(int(i))
adj=defaultdict(set)
for linked in edge_faces.values():
 for i in linked:adj[i].update(linked)
seen={8253};stack=[8253]
while stack:
 for j in adj[stack.pop()]-seen:seen.add(j);stack.append(j)
assert sorted(seen)==changed
p=t[changed];cross=np.cross(p[:,1]-p[:,0],p[:,2]-p[:,0]);assert (cross[:,2]<0).all()
assert (p[:,:,2]==101).all() and (p[:,:,0]>=-61.75).all() and (p[:,:,0]<=61.75).all() and (p[:,:,1]>=14.5).all() and (p[:,:,1]<=16).all()
# Exact two-triangle rectangular cover: four rectangle vertices and shared diagonal;
# every boundary edge appears once, shared diagonal exactly twice, area equals support.
vv,ii=np.unique(p.reshape(-1,3),axis=0,return_inverse=True);assert len(vv)==4
assert set(map(tuple,vv[:,:2]))=={(-61.75,14.5),(-61.75,16),(61.75,14.5),(61.75,16)}
from collections import Counter
edges=Counter(tuple(sorted((int(row[a]),int(row[b])))) for row in ii.reshape(2,3) for a,b in [(0,1),(1,2),(2,0)])
assert sorted(edges.values())==[1,1,1,1,2]
area=float(np.linalg.norm(cross,axis=1).sum()/2);assert area==185.25
report={'status':'PASS_MATERIAL_ONLY','original_triangles':n,'changed_faces':changed,'counts':np.bincount(c).tolist(),'stl_geometry_order_exact':True,'support_area_mm2':area,'full_stl_plane_shared_edge_bfs':sorted(seen),'per_triangle_containment':True,'reverse_coverage':'rectangle vertices, diagonal pairing and exact area','source_stl_sha256':hashlib.sha256(raw).hexdigest()}
(A/'qa/current-material-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
