from pathlib import Path
import struct,json,collections,hashlib
import numpy as np
from shapely.geometry import Polygon,box,Point
from shapely.ops import unary_union
A=Path(__file__).resolve().parents[1];R=A.parent;O=R;raw=(O/'model.stl').read_bytes();n=struct.unpack_from('<I',raw,80)[0];t=np.array([struct.unpack_from('<9f',raw,96+50*i) for i in range(n)]).reshape(n,3,3)
norm=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);norm/=np.linalg.norm(norm,axis=1)[:,None];colors=json.loads((O/'appearance/face-materials.json').read_text())['face_material_indices'];edges=collections.defaultdict(list)
for i,tri in enumerate(t):
 for a,b in [(0,1),(1,2),(2,0)]:edges[tuple(sorted((tuple(tri[a]),tuple(tri[b]))))].append(i)
adj=[set() for _ in t]
for fs in edges.values():
 for i in fs:adj[i].update(set(fs)-{i})
# Tower cut(-8,-13,22.5,19,2.2,34.8), exposed top underside z57.3.
# Host front -13, cut back -11.9, x[-17.5,1.5]; 8 vertical details span z22.4..57.4 and y-13.6..-11.6.
support=box(-17.5,-13,1.5,-11.9)
for x in np.linspace(-16.5,.5,8):support=support.difference(box(float(x)-.375,-13.6,float(x)+.375,-11.6))
parts=sorted(list(support.geoms),key=lambda p:p.bounds[0]);domains=[];mask=np.all(abs(t[:,:,2]-57.3)<1e-5,axis=1)&(norm[:,2]<-.999999);centers=t.mean(axis=1)
for i,p in enumerate(parts):
 seeds=[j for j in map(int,np.flatnonzero(mask)) if p.buffer(1e-6).contains(Point(centers[j,:2]))];assert seeds
 seen={min(seeds)};stack=list(seen)
 while stack:
  for j in adj[stack.pop()]:
   if mask[j] and j not in seen:seen.add(j);stack.append(j)
 ids=sorted(seen);ps=[Polygon(t[j,:,:2]) for j in ids];u=unary_union(ps);outside=sum(q.difference(p).area for q in ps);missing=p.difference(u).area;assert outside<.001 and missing<.001
 domains.append({'name':f'tower_inner_top_strip_{i}','seed':ids[0],'faces':ids,'count':len(ids),'plane_axis':2,'plane_value':57.3,'normal_sign':-1,'projection_axes':[0,1],'support_polygon':list(p.exterior.coords),'support_area_mm2':p.area,'actual_area_mm2':sum(q.area for q in ps),'outside_mm2':outside,'reverse_missing_mm2':missing,'max_plane_residual_mm':float(abs(t[ids,:,2]-57.3).max()),'bounds':[t[ids].min(axis=(0,1)).tolist(),t[ids].max(axis=(0,1)).tolist()],'current_indices':[colors[j] for j in ids]})
ids=sorted(j for d in domains for j in d['faces']);assert len(ids)==len(set(ids))

import zipfile,xml.etree.ElementTree as E,importlib.util
assert ids==[564, 565, 566, 567, 568, 569, 570, 571, 641, 642, 643, 644, 653, 654, 655, 656, 673, 680] and n==4300
with zipfile.ZipFile(A/'nuuq1-appearance.3mf') as z:r=E.fromstring(z.read('3D/3dmodel.model'))
ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
vs=np.array([[float(x.get(k)) for k in 'xyz'] for x in r.findall('.//m:vertices/m:vertex',ns)]);ts=r.findall('.//m:triangles/m:triangle',ns);fs=np.array([[int(x.get(k)) for k in ['v1','v2','v3']] for x in ts]);assigned=np.array([int(x.get('p1')) for x in ts]);assert np.array_equal(vs[fs],t) and assigned.tolist()==colors
sp=importlib.util.spec_from_file_location('old',A/'source/build_appearance.py');old=importlib.util.module_from_spec(sp);sp.loader.exec_module(old);before,_=old.classify(t)
assert np.flatnonzero(assigned!=before).tolist()==ids and (assigned[ids]==2).all()
result={'status':'PASS_MATERIAL_ONLY','triangles':n,'changed_faces':ids,'counts':np.bincount(assigned).tolist(),'stl_geometry_order_exact':True,'complete_plane_bfs_domains':domains,'area_tolerance_mm2_per_domain':.001,'source_stl_sha256':hashlib.sha256(raw).hexdigest()}
for k in ['actual_area_mm2','support_area_mm2','outside_mm2','reverse_missing_mm2']:result[k]=sum(d[k] for d in domains)
(A/'qa/current-material-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
