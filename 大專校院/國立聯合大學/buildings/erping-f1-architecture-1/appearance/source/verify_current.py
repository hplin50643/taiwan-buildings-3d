from pathlib import Path
import json,hashlib,struct,collections
import numpy as np
from shapely.geometry import box,Polygon
from shapely.ops import unary_union
A=Path(__file__).resolve().parents[1];O=A.parent
raw=(O/'model.stl').read_bytes();n=struct.unpack_from('<I',raw,80)[0];t=np.array([struct.unpack_from('<9f',raw,96+50*i) for i in range(n)]).reshape(n,3,3)
colors=json.loads((A/'face-materials.json').read_text())['face_material_indices']
norm=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);norm/=np.linalg.norm(norm,axis=1)[:,None]
edges=collections.defaultdict(list)
for i,tri in enumerate(t):
 for a,b in [(0,1),(1,2),(2,0)]:edges[tuple(sorted((tuple(tri[a]),tuple(tri[b]))))].append(i)
adj=[set() for _ in t]
for fs in edges.values():
 for i in fs:adj[i].update(set(fs)-{i})
mask=np.all(abs(t[:,:,1]+22.5)<1e-5,axis=1)&(norm[:,1]<-.999999)
seen={1408};stack=[1408]
while stack:
 for j in adj[stack.pop()]:
  if mask[j] and j not in seen:seen.add(j);stack.append(j)
faces=sorted(seen);assert faces==[1408,1409]
support=box(0,19,16,21)
polys=[Polygon(t[i][:,[0,2]]) for i in faces];u=unary_union(polys);outside=sum(q.difference(support).area for q in polys);missing=support.difference(u).area
assert outside<.001 and missing<.001
domains=[{'faces':faces,'count':len(faces),'support_polygon':list(support.exterior.coords),'support_area_mm2':support.area,'actual_area_mm2':sum(q.area for q in polys),'outside_mm2':outside,'reverse_missing_mm2':missing,'current_indices':[colors[i] for i in faces]}]
ids=faces

import zipfile,xml.etree.ElementTree as E,importlib.util
assert ids==[1408, 1409] and n==1524
with zipfile.ZipFile(A/'nuuf1-appearance.3mf') as z:r=E.fromstring(z.read('3D/3dmodel.model'))
ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
vs=np.array([[float(x.get(k)) for k in 'xyz'] for x in r.findall('.//m:vertices/m:vertex',ns)]);ts=r.findall('.//m:triangles/m:triangle',ns);fs=np.array([[int(x.get(k)) for k in ['v1','v2','v3']] for x in ts]);assigned=np.array([int(x.get('p1')) for x in ts]);assert np.array_equal(vs[fs],t) and assigned.tolist()==colors
sp=importlib.util.spec_from_file_location('old',A/'source/build_appearance.py');old=importlib.util.module_from_spec(sp);sp.loader.exec_module(old);before,_=old.classify(t)
assert np.flatnonzero(assigned!=before).tolist()==ids and (assigned[ids]==2).all()
result={'status':'PASS_MATERIAL_ONLY','triangles':n,'changed_faces':ids,'counts':np.bincount(assigned).tolist(),'stl_geometry_order_exact':True,'complete_plane_bfs_domains':domains,'area_tolerance_mm2_per_domain':.001,'source_stl_sha256':hashlib.sha256(raw).hexdigest()}
for k in ['actual_area_mm2','support_area_mm2','outside_mm2','reverse_missing_mm2']:result[k]=sum(d[k] for d in domains)
(A/'qa/current-material-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
