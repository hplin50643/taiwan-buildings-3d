from pathlib import Path
import json,struct,hashlib,collections
import numpy as np
from shapely.geometry import Polygon,box
from shapely.ops import unary_union
A=Path(__file__).resolve().parents[1];R=A.parent;O=R;raw=(O/'model.stl').read_bytes();n=struct.unpack_from('<I',raw,80)[0]
t=np.array([struct.unpack_from('<9f',raw,96+50*i) for i in range(n)]).reshape(n,3,3);normals=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);normals/=np.linalg.norm(normals,axis=1)[:,None]
colors=json.loads((O/'appearance/face-materials.json').read_text())['face_material_indices'];edges=collections.defaultdict(list)
for i,tri in enumerate(t):
 for a,b in [(0,1),(1,2),(2,0)]:edges[tuple(sorted((tuple(tri[a]),tuple(tri[b]))))].append(i)
adj=[set() for _ in t]
for fs in edges.values():
 for i in fs:adj[i].update(set(fs)-{i})
# Original hip(0,0,30,145,41,9): ridge x +/- (72.5-41*.38), z39.
# Front slope z=39+(9/20.5)*y; original eaves add(0,0,28.6,144,40,1.8).
k=9/20.5;normal=np.array([0,-k,1]);normal/=np.linalg.norm(normal);res=abs(t[:,:,2]-39-k*t[:,:,1])/np.sqrt(1+k*k)
mask=np.all(res<1e-5,axis=1)&(normals@normal>.999999)
remaining=set(map(int,np.flatnonzero(mask)));components=[]
while remaining:
 seen={min(remaining)};stack=list(seen)
 while stack:
  for i in adj[stack.pop()]:
   if mask[i] and i not in seen:seen.add(i);stack.append(i)
 remaining-=seen;ids=sorted(seen);ps=[Polygon(t[i][:,:2]) for i in ids];components.append((ids,ps,unary_union(ps)))
components.sort(key=lambda c:c[2].area,reverse=True)
full=Polygon([(-72.5,-20.5),(72.5,-20.5),(56.92,0),(-56.92,0)])
ycut=(30.4-39)/k
support_all=full.difference(box(-72,-20,72,ycut));support_parts=list(support_all.geoms) if hasattr(support_all,'geoms') else [support_all];support=max(support_parts,key=lambda q:q.area)
ids,ps,u=components[0];outside=sum(p.difference(support).area for p in ps);missing=support.difference(u).area
assert outside<.002 and missing<.002,(outside,missing,ids)
scale=np.sqrt(1+k*k)
d={'name':'front_main_hip_slope','seed':ids[0],'faces':ids,'count':len(ids),'plane_equation':'z - (9/20.5)*y - 39 = 0','normal':normal.tolist(),'projection_axes':[0,1],'support_polygon_xy':list(support.exterior.coords),'support_projected_area_mm2':support.area,'actual_projected_area_mm2':sum(p.area for p in ps),'support_area_mm2':support.area*scale,'actual_area_mm2':sum(p.area for p in ps)*scale,'outside_mm2':outside*scale,'reverse_missing_mm2':missing*scale,'max_plane_residual_mm':float(res[ids].max()),'bounds':[t[ids].min(axis=(0,1)).tolist(),t[ids].max(axis=(0,1)).tolist()],'current_indices':[colors[i] for i in ids]}
import zipfile,xml.etree.ElementTree as E,importlib.util
assert ids==[943,953] and hashlib.sha256(raw).hexdigest()=='9863599d487c595e276ad781dd44943b86451ff5c20ef3a8c7871788b90d944f'
with zipfile.ZipFile(A/'physics-appearance.3mf') as z:r=E.fromstring(z.read('3D/3dmodel.model'))
ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
vs=np.array([[float(x.get(k)) for k in 'xyz'] for x in r.findall('.//m:vertices/m:vertex',ns)]);ts=r.findall('.//m:triangles/m:triangle',ns);fs=np.array([[int(x.get(k)) for k in ['v1','v2','v3']] for x in ts]);assigned=np.array([int(x.get('p1')) for x in ts]);assert np.array_equal(vs[fs],t) and assigned.tolist()==colors
sp=importlib.util.spec_from_file_location('old',A/'source/build_appearance.py');old=importlib.util.module_from_spec(sp);sp.loader.exec_module(old);before,_=old.classify(t)
assert np.flatnonzero(assigned!=before).tolist()==ids and (assigned[ids]==8).all()
result={'status':'PASS_MATERIAL_ONLY','triangles':n,'changed_faces':ids,'counts':np.bincount(assigned).tolist(),'stl_geometry_order_exact':True,'complete_plane_bfs_domains':[d],'actual_area_mm2':d['actual_area_mm2'],'support_area_mm2':d['support_area_mm2'],'outside_mm2':d['outside_mm2'],'reverse_missing_mm2':d['reverse_missing_mm2'],'area_tolerance_mm2_per_domain':.003,'source_stl_sha256':hashlib.sha256(raw).hexdigest()}
(A/'qa/current-material-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
