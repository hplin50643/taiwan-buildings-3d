from pathlib import Path
import json,struct,hashlib,collections
import numpy as np
from shapely.geometry import Polygon,box
from shapely.ops import unary_union
A=Path(__file__).resolve().parents[1];R=A.parent;O=R;raw=(O/'model.stl').read_bytes();n=struct.unpack_from('<I',raw,80)[0]
t=np.array([struct.unpack_from('<9f',raw,96+50*i) for i in range(n)]).reshape(n,3,3);N=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);N/=np.linalg.norm(N,axis=1)[:,None]
colors=json.loads((O/'appearance/face-materials.json').read_text())['face_material_indices'];edges=collections.defaultdict(list)
for i,tri in enumerate(t):
 for a,b in [(0,1),(1,2),(2,0)]:edges[tuple(sorted((tuple(tri[a]),tuple(tri[b]))))].append(i)
adj=[set() for _ in t]
for fs in edges.values():
 for i in fs:adj[i].update(set(fs)-{i})
domains=[]
# Original roof add(0,-64,22.2,79,17,2); intersecting side corridor and cap.
for name,plane,normal in [('positive_x_end',39.5,[1,0,0])]:
 full=box(-72.5,22.2,-55.5,24.2)
 support=full.difference(unary_union([box(-61,2.9,67,23.9),box(-62,23.6,68,25)]))
 mask=np.all(abs(t[:,:,0]-plane)<1e-5,axis=1)&(N@normal>.999999)
 seeds=[int(i) for i in np.flatnonzero(mask) if Polygon(t[i][:,[1,2]]).difference(support).area<.001]
 assert seeds,name
 seen={seeds[0]};stack=list(seen)
 while stack:
  for i in adj[stack.pop()]:
   if mask[i] and i not in seen:seen.add(i);stack.append(i)
 ids=sorted(seen);ps=[Polygon(t[i][:,[1,2]]) for i in ids];u=unary_union(ps)
 outside=sum(p.difference(support).area for p in ps);missing=support.difference(u).area
 assert outside<.001 and missing<.001,(name,outside,missing,ids)
 domains.append({'name':name,'plane_axis':0,'plane_value':plane,'normal':normal,'projection_axes':[1,2],'seed':ids[0],'faces':ids,'count':len(ids),'support_polygon_yz':list(support.exterior.coords),'support_area_mm2':support.area,'actual_area_mm2':sum(p.area for p in ps),'outside_mm2':outside,'reverse_missing_mm2':missing,'max_plane_residual_mm':float(abs(t[ids,:,0]-plane).max()),'bounds':[t[ids].min(axis=(0,1)).tolist(),t[ids].max(axis=(0,1)).tolist()],'original_indices':[colors[i] for i in ids]})
faces=sorted(i for d in domains for i in d['faces'])
import zipfile,xml.etree.ElementTree as E,importlib.util
assert faces==[922,923,924,925] and hashlib.sha256(raw).hexdigest()=='d9be3845ba167180ee696df279ba0bb907709bade622a10142d81fc904649ad2'
with zipfile.ZipFile(A/'gechi-appearance.3mf') as z:r=E.fromstring(z.read('3D/3dmodel.model'))
ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
vs=np.array([[float(x.get(k)) for k in 'xyz'] for x in r.findall('.//m:vertices/m:vertex',ns)]);ts=r.findall('.//m:triangles/m:triangle',ns);fs=np.array([[int(x.get(k)) for k in ['v1','v2','v3']] for x in ts]);assigned=np.array([int(x.get('p1')) for x in ts]);assert np.array_equal(vs[fs],t) and assigned.tolist()==colors
sp=importlib.util.spec_from_file_location('old',A/'source/build_appearance.py');old=importlib.util.module_from_spec(sp);sp.loader.exec_module(old);before,_=old.classify(t)
assert np.flatnonzero(assigned!=before).tolist()==faces and (assigned[faces]==2).all()
result={'status':'PASS_MATERIAL_ONLY','triangles':n,'changed_faces':faces,'counts':np.bincount(assigned).tolist(),'stl_geometry_order_exact':True,'complete_plane_bfs_domains':domains,'actual_area_mm2':sum(d['actual_area_mm2'] for d in domains),'support_area_mm2':sum(d['support_area_mm2'] for d in domains),'outside_mm2':sum(d['outside_mm2'] for d in domains),'reverse_missing_mm2':sum(d['reverse_missing_mm2'] for d in domains),'area_tolerance_mm2_per_domain':.001,'source_stl_sha256':hashlib.sha256(raw).hexdigest()}
(A/'qa/current-material-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
