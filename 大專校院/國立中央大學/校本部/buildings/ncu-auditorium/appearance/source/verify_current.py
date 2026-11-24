from pathlib import Path
import json,struct,hashlib,math,collections
import numpy as np
from shapely.geometry import Polygon,box
from shapely.ops import unary_union
A=Path(__file__).resolve().parents[1];R=A.parent;O=R
raw=(O/'model.stl').read_bytes(); n=struct.unpack_from('<I',raw,80)[0]
t=np.array([struct.unpack_from('<9f',raw,96+50*i) for i in range(n)]).reshape(-1,3,3)
norm=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]); norm/=np.linalg.norm(norm,axis=1)[:,None]
colors=json.loads((A/'face-materials.json').read_text())['face_material_indices']
edges=collections.defaultdict(list)
for i,tri in enumerate(t):
 for a,b in ((0,1),(1,2),(2,0)):edges[tuple(sorted((tuple(tri[a]),tuple(tri[b]))))].append(i)
adj=[set() for _ in t]
for fs in edges.values():
 for f in fs:adj[f].update(set(fs)-{f})
domains=[]
for j in range(144):
 p=np.array([61.5*math.cos(j*2*math.pi/144),41.5*math.sin(j*2*math.pi/144)])
 q=np.array([61.5*math.cos((j+1)*2*math.pi/144),41.5*math.sin((j+1)*2*math.pi/144)])
 d=q-p; L=float(np.linalg.norm(d)); u=d/L; outward=np.array([u[1],-u[0],0.])
 # Exact source outer polygon edge clipped by original x<=-20.5 and negative-y side.
 lo,hi=0.,1.
 for k,limit in ((0,-20.5),(1,0.)):
  if abs(d[k])<1e-12:
   if p[k]>limit+1e-10:hi=-1
  elif d[k]>0:hi=min(hi,(limit-p[k])/d[k])
  else:lo=max(lo,(limit-p[k])/d[k])
 if hi-lo<1e-9:continue
 residual=np.abs((t[:,:,:2]-p)@outward[:2]); eligible=np.all(residual<1e-5,axis=1)&(norm@outward>.999999)
 # Seed by full vertex support, then traverse all coplanar eligible triangles (no z cropped BFS).
 seedset=np.where(eligible & np.all(t[:,:,2]>=83-1e-5,axis=1)&np.all(t[:,:,2]<=84.8+1e-5,axis=1))[0]
 assert len(seedset)>0,(j,'no seed')
 seen={int(seedset[0])}; stack=list(seen)
 while stack:
  f=stack.pop()
  for g in adj[f]:
   if eligible[g] and g not in seen:seen.add(g);stack.append(g)
 ids=sorted(seen); coords=[np.column_stack(((t[i,:,:2]-p)@u,t[i,:,2])) for i in ids]
 polys=[Polygon(c) for c in coords]; union=unary_union(polys); support=box(lo*L,83,hi*L,84.8)
 outside=sum(v.difference(support).area for v in polys); missing=support.difference(union).area
 assert outside<.001 and missing<.001,(j,outside,missing)
 domains.append({'facet':j,'seed':ids[0],'faces':ids,'count':len(ids),'original_indices':[colors[i] for i in ids],'plane_normal':outward.tolist(),'plane_origin_xy':p.tolist(),'max_plane_residual_mm':float(residual[ids].max()),'support_segment_xy':[(p+lo*d).tolist(),(p+hi*d).tolist()],'support_z':[83,84.8],'bounds':[t[ids].min(axis=(0,1)).tolist(),t[ids].max(axis=(0,1)).tolist()],'area_mm2':sum(x.area for x in polys),'support_area_mm2':support.area,'outside_mm2':outside,'reverse_missing_mm2':missing,'overlap_mm2':sum(x.area for x in polys)-union.area})
faces=sorted(i for d in domains for i in d['faces'])

import zipfile,xml.etree.ElementTree as E,importlib.util
assert hashlib.sha256(raw).hexdigest()=='50964d7b2b33cb1489a01b8b3198e272d1a1a03c2d537dd9c7fb4030053e9d4b'
assert faces==[9178, 9179, 9181, 9187, 9192, 9195, 9201, 9202, 9204, 9208, 9209, 9215, 9216, 9225, 9226, 9233, 9235, 9240, 9241, 9244, 9245, 9248, 9250, 9253, 9255, 9267, 9270, 9271, 9276, 9278, 9285, 9292, 9293, 9298, 9300, 9304, 9310, 9311, 9322, 9327, 9329, 9334, 9342, 9343, 9348, 9350, 9364, 9365, 9373, 9376, 9382, 9383, 9388, 9390, 9392, 9398, 9403, 9404]
with zipfile.ZipFile(A/'ncu-auditorium-appearance.3mf') as z:r=E.fromstring(z.read('3D/3dmodel.model'))
ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
v=np.array([[float(x.get(k)) for k in 'xyz'] for x in r.findall('.//m:vertices/m:vertex',ns)]);ts=r.findall('.//m:triangles/m:triangle',ns);f=np.array([[int(x.get(k)) for k in ['v1','v2','v3']] for x in ts]);assigned=np.array([int(x.get('p1')) for x in ts]);assert np.array_equal(v[f],t);assert assigned.tolist()==colors
sp=importlib.util.spec_from_file_location('old',A/'source/build_appearance.py');old=importlib.util.module_from_spec(sp);sp.loader.exec_module(old);before,_=old.classify(t)
assert np.flatnonzero(assigned!=before).tolist()==faces and (assigned[faces]==4).all()
assert np.bincount(assigned).tolist()==[2320, 1056, 6028, 152, 58]
result={'status':'PASS_MATERIAL_ONLY','triangles':n,'changed_faces':faces,'counts':np.bincount(assigned).tolist(),'stl_geometry_order_exact':True,'complete_plane_bfs_domains':domains,'actual_area_mm2':sum(d['area_mm2'] for d in domains),'support_area_mm2':sum(d['support_area_mm2'] for d in domains),'outside_mm2':sum(d['outside_mm2'] for d in domains),'reverse_missing_mm2':sum(d['reverse_missing_mm2'] for d in domains),'area_tolerance_mm2_per_facet':.001,'limits':'Original thick polygon rim is not measured panel geometry. Only negative-y outer vertical facets; float32 forward/reverse support differences are nonzero and bounded.','source_stl_sha256':hashlib.sha256(raw).hexdigest()}
(A/'qa/current-material-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
