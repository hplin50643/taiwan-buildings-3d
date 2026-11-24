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
mask=np.all(abs(t[:,:,1]+44.5)<1e-5,axis=1)&(N[:,1]<-.999999);domains=[]
for x in [-22,0,22]:
 # Original column front rectangle minus elevated host startingz38. Base clips bottom at3.
 full=box(x-1.2,3,x+1.2,38.1);host=box(-38,38,38,76.8);support=full.difference(host)
 seeds=[int(i) for i in np.flatnonzero(mask) if Polygon(t[i][:,[0,2]]).difference(support).area<.001]
 assert seeds,x
 seen={seeds[0]};stack=list(seen)
 while stack:
  for i in adj[stack.pop()]:
   if mask[i] and i not in seen:seen.add(i);stack.append(i)
 ids=sorted(seen);polys=[Polygon(t[i][:,[0,2]]) for i in ids];u=unary_union(polys);outside=sum(p.difference(support).area for p in polys);missing=support.difference(u).area
 assert outside<.001 and missing<.001,(x,outside,missing)
 domains.append({'column_center_x':x,'seed':ids[0],'faces':ids,'count':len(ids),'plane_axis':1,'plane_value':-44.5,'normal':[0,-1,0],'full_column_rectangle':list(full.bounds),'subtracted_host_rectangle':list(host.bounds),'support_bounds':list(support.bounds),'bounds':[t[ids].min(axis=(0,1)).tolist(),t[ids].max(axis=(0,1)).tolist()],'original_indices':[colors[i] for i in ids],'max_plane_residual_mm':float(abs(t[ids,:,1]+44.5).max()),'area_mm2':sum(p.area for p in polys),'analytic_area_mm2':support.area,'outside_mm2':outside,'reverse_missing_mm2':missing,'overlap_mm2':sum(p.area for p in polys)-u.area})
faces=sorted(i for d in domains for i in d['faces'])
import zipfile,xml.etree.ElementTree as E,importlib.util
assert hashlib.sha256(raw).hexdigest()=='f8b49387d3e9237da92bb6c3b8d7ed89f931f412ddae9494de118acf6694c287' and faces==[1074, 1079, 1082, 1088, 1090, 1095]
with zipfile.ZipFile(A/'ncu-optoelectronics-appearance.3mf') as z:r=E.fromstring(z.read('3D/3dmodel.model'))
ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
v=np.array([[float(x.get(k)) for k in 'xyz'] for x in r.findall('.//m:vertices/m:vertex',ns)]);ts=r.findall('.//m:triangles/m:triangle',ns);f=np.array([[int(x.get(k)) for k in ['v1','v2','v3']] for x in ts]);assigned=np.array([int(x.get('p1')) for x in ts]);assert np.array_equal(v[f],t) and assigned.tolist()==colors
sp=importlib.util.spec_from_file_location('old',A/'source/build_appearance.py');old=importlib.util.module_from_spec(sp);sp.loader.exec_module(old);before,_=old.classify(t)
assert np.flatnonzero(assigned!=before).tolist()==faces and (assigned[faces]==3).all();assert np.bincount(assigned).tolist()==[2596, 1494, 42, 6]
result={'status':'PASS_MATERIAL_ONLY','triangles':n,'changed_faces':faces,'counts':np.bincount(assigned).tolist(),'stl_geometry_order_exact':True,'complete_plane_bfs_domains':domains,'actual_area_mm2':sum(d['area_mm2'] for d in domains),'support_area_mm2':sum(d['analytic_area_mm2'] for d in domains),'outside_mm2':sum(d['outside_mm2'] for d in domains),'reverse_missing_mm2':sum(d['reverse_missing_mm2'] for d in domains),'area_tolerance_mm2_per_domain':.001,'limits':'Only3 original rectangular front columns y=-44.5/z3..38, original box minus elevated host. Coarse proportions/count and lower railing occlusion not surveyed reality; nonzero float32 outside retained.','source_stl_sha256':hashlib.sha256(raw).hexdigest()}
(A/'qa/current-material-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
