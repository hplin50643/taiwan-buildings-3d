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
for step in range(3):
 front=-51+step*1.4-.85;back=front+1.4 if step<2 else -51+step*1.4+.85;top=2.8+.7*(step+1);bottom=3 if step==0 else 2.8+.7*step
 for typ,axis,plane,normal,project,support in [('tread',2,top,[0,0,1],[0,1],box(-50,front,50,back)),('front_riser',1,front,[0,-1,0],[0,2],box(-50,bottom,50,top))]:
  mask=np.all(abs(t[:,:,axis]-plane)<1e-5,axis=1)&(N@normal>.999999)
  # choose seed by full source rectangle containment then traverse all eligible plane neighbors
  seeds=[int(i) for i in np.flatnonzero(mask) if Polygon(t[i][:,project]).difference(support).area<.001]
  assert seeds,(step,typ)
  seen={seeds[0]};stack=list(seen)
  while stack:
   for i in adj[stack.pop()]:
    if mask[i] and i not in seen:seen.add(i);stack.append(i)
  ids=sorted(seen);polys=[Polygon(t[i][:,project]) for i in ids];union=unary_union(polys);outside=sum(p.difference(support).area for p in polys);missing=support.difference(union).area
  assert outside<.001 and missing<.001,(step,typ,outside,missing)
  domains.append({'step_index':step,'type':typ,'faces':ids,'count':len(ids),'seed':ids[0],'plane_axis':axis,'plane_value':plane,'normal':normal,'projection_axes':project,'support_bounds':list(support.bounds),'bounds':[t[ids].min(axis=(0,1)).tolist(),t[ids].max(axis=(0,1)).tolist()],'original_indices':[colors[i] for i in ids],'max_plane_residual_mm':float(abs(t[ids,:,axis]-plane).max()),'area_mm2':sum(p.area for p in polys),'analytic_area_mm2':support.area,'outside_mm2':outside,'reverse_missing_mm2':missing,'overlap_mm2':sum(p.area for p in polys)-union.area})
faces=sorted(i for d in domains for i in d['faces'])
import zipfile,xml.etree.ElementTree as E,importlib.util
assert hashlib.sha256(raw).hexdigest()=='c100700000dfb445be70dab4615a2654875ba3de9ae63e0f0c1c096bec2f6d74' and faces==[6650, 6651, 6652, 6653, 6663, 6664, 6665, 6666, 6678, 6679, 6681, 6683]
with zipfile.ZipFile(A/'ncu-main-library-appearance.3mf') as z:r=E.fromstring(z.read('3D/3dmodel.model'))
ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
v=np.array([[float(x.get(k)) for k in 'xyz'] for x in r.findall('.//m:vertices/m:vertex',ns)]);ts=r.findall('.//m:triangles/m:triangle',ns);f=np.array([[int(x.get(k)) for k in ['v1','v2','v3']] for x in ts]);assigned=np.array([int(x.get('p1')) for x in ts]);assert np.array_equal(v[f],t) and assigned.tolist()==colors
sp=importlib.util.spec_from_file_location('old',A/'source/build_appearance.py');old=importlib.util.module_from_spec(sp);sp.loader.exec_module(old);before,_=old.classify(t)
assert np.flatnonzero(assigned!=before).tolist()==faces and (assigned[faces]==3).all();assert np.bincount(assigned).tolist()==[2273, 506, 2642, 1267]
result={'status':'PASS_MATERIAL_ONLY','triangles':n,'changed_faces':faces,'counts':np.bincount(assigned).tolist(),'stl_geometry_order_exact':True,'complete_plane_bfs_domains':domains,'actual_area_mm2':sum(d['area_mm2'] for d in domains),'support_area_mm2':sum(d['analytic_area_mm2'] for d in domains),'outside_mm2':sum(d['outside_mm2'] for d in domains),'reverse_missing_mm2':sum(d['reverse_missing_mm2'] for d in domains),'area_tolerance_mm2_per_domain':.001,'limits':'First riser clipped at basez3; upper tready=-47.35 retains2.85mm porch gap. Original3steps and omitted fine nosing not measured construction. Nonzero float32 support deviations explicitly retained.','source_stl_sha256':hashlib.sha256(raw).hexdigest()}
(A/'qa/current-material-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
