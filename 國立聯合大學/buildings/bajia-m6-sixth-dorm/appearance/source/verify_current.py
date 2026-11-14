from pathlib import Path
import struct,json,collections,hashlib
import numpy as np
from shapely.geometry import Polygon,box
from shapely.ops import unary_union
A=Path(__file__).resolve().parents[1];R=A.parent;O=R;raw=(O/'model.stl').read_bytes();n=struct.unpack_from('<I',raw,80)[0];t=np.array([struct.unpack_from('<9f',raw,96+50*i) for i in range(n)]).reshape(n,3,3)
norm=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);norm/=np.linalg.norm(norm,axis=1)[:,None];colors=json.loads((O/'appearance/face-materials.json').read_text())['face_material_indices'];edges=collections.defaultdict(list)
for i,tri in enumerate(t):
 for a,b in [(0,1),(1,2),(2,0)]:edges[tuple(sorted((tuple(tri[a]),tuple(tri[b]))))].append(i)
adj=[set() for _ in t]
for fs in edges.values():
 for i in fs:adj[i].update(set(fs)-{i})
mask=np.all(abs(t[:,:,1]-56.3)<1e-5,axis=1)&(norm[:,1]<-.999999)
seeds=[int(i) for i in np.flatnonzero(mask) if t[i,:,2].min()>68.6];assert seeds
seen={min(seeds)};stack=list(seen)
while stack:
 for j in adj[stack.pop()]:
  if mask[j] and j not in seen:seen.add(j);stack.append(j)
ids=sorted(seen)
support=box(-41,68.7,41,70.3)
y=56.3;d=58.7-y;top=67.4+d*10.4/14.2
for x in [-53,53]:
 roof=Polygon([(x-14.2,0),(x+14.2,0),(x+14.2,67.4),(x+14.2-d,top),(x-14.2+d,top),(x-14.2,67.4)])
 support=support.difference(roof)
ps=[Polygon(t[j][:,[0,2]]) for j in ids];u=unary_union(ps);outside=sum(p.difference(support).area for p in ps);missing=support.difference(u).area
assert outside<.001 and missing<.001,(outside,missing)
domain={'name':'rear_parapet_inward_vertical_face','seed':ids[0],'faces':ids,'count':len(ids),'plane_axis':1,'plane_value':56.3,'normal_sign':-1,'projection_axes':[0,2],'bounds':[t[ids].min(axis=(0,1)).tolist(),t[ids].max(axis=(0,1)).tolist()],'current_indices':[colors[j] for j in ids],'support_polygon':list(support.exterior.coords),'support_area_mm2':support.area,'actual_area_mm2':sum(p.area for p in ps),'outside_mm2':outside,'reverse_missing_mm2':missing,'max_plane_residual_mm':float(abs(t[ids,:,1]-56.3).max())}

domains=[domain]

import zipfile,xml.etree.ElementTree as E,importlib.util
assert ids==[6965, 6966, 6969, 6970] and n==7000
with zipfile.ZipFile(A/'nuum6-appearance.3mf') as z:r=E.fromstring(z.read('3D/3dmodel.model'))
ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
vs=np.array([[float(x.get(k)) for k in 'xyz'] for x in r.findall('.//m:vertices/m:vertex',ns)]);ts=r.findall('.//m:triangles/m:triangle',ns);fs=np.array([[int(x.get(k)) for k in ['v1','v2','v3']] for x in ts]);assigned=np.array([int(x.get('p1')) for x in ts]);assert np.array_equal(vs[fs],t) and assigned.tolist()==colors
sp=importlib.util.spec_from_file_location('old',A/'source/build_appearance.py');old=importlib.util.module_from_spec(sp);sp.loader.exec_module(old);before,_=old.classify(t)
assert np.flatnonzero(assigned!=before).tolist()==ids and (assigned[ids]==5).all()
result={'status':'PASS_MATERIAL_ONLY','triangles':n,'changed_faces':ids,'counts':np.bincount(assigned).tolist(),'stl_geometry_order_exact':True,'complete_plane_bfs_domains':domains,'area_tolerance_mm2_per_domain':.001,'source_stl_sha256':hashlib.sha256(raw).hexdigest()}
for k in ['actual_area_mm2','support_area_mm2','outside_mm2','reverse_missing_mm2']:result[k]=sum(d[k] for d in domains)
(A/'qa/current-material-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
