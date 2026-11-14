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
# Original portal boxes: vertical x=-48/-19,width1.6,y=-15.2,depth8,z13.2..23.8;
# top z23..24.4 and bottom z13.1..14.1 x=-48.8..-18.2. Main host front y=-12.
# Interior free rectangle x=-47.2..-19.8,z14.1..23, exposed depth y=-19.2..-12.
for name,axis,plane,normal,proj,full in [('left_cheek',0,-47.2,[1,0,0],[1,2],box(-19.2,14.1,-12,23)),('right_cheek',0,-19.8,[-1,0,0],[1,2],box(-19.2,14.1,-12,23)),('top_return',2,23,[0,0,-1],[0,1],box(-47.2,-19.2,-19.8,-12))]:
 cuts=[]
 # Re-derive all original regular window cuts, project only when actual cut box crosses domain plane.
 for z in [4.8,14.9,25.0]:
  for x in np.arange(-66,67,4.4):
   if z==4.8 and (-50<x<-18 or 39<x<53):continue
   for dz in [0,2.7,5.4]:
    bounds=[(float(x)-1.75,float(x)+1.75),(-12.9,-11.3),(z+dz,z+dz+2.1)]
    if bounds[axis][0]<plane<bounds[axis][1]:
     a,b=proj;cuts.append(box(bounds[a][0],bounds[b][0],bounds[a][1],bounds[b][1]))
 # Original solid sloping parapets intersect bottom return: YZ polygon [(-35,3),(-13,14),(-13,15.2),(-35,4.2)] extruded1 at x=-48.2/-33.5/-18.8.
 if axis==2 and 3<plane<15.2:
  ylo=max(-35,2*(plane-21.7));yhi=min(-13,2*(plane-20.5))
  if ylo<yhi:
   for rail_x in [-48.2,-33.5,-18.8]:cuts.append(box(rail_x-.5,ylo,rail_x+.5,yhi))
 support=full.difference(unary_union(cuts));mask=np.all(abs(t[:,:,axis]-plane)<1e-5,axis=1)&(N@normal>.999999)
 seeds=[int(i) for i in np.flatnonzero(mask) if Polygon(t[i][:,proj]).difference(support).area<.001]
 assert seeds,name
 seen={seeds[0]};stack=list(seen)
 while stack:
  for i in adj[stack.pop()]:
   if mask[i] and i not in seen:seen.add(i);stack.append(i)
 ids=sorted(seen);ps=[Polygon(t[i][:,proj]) for i in ids];u=unary_union(ps);outside=sum(p.difference(support).area for p in ps);missing=support.difference(u).area
 assert outside<.001 and missing<.001,(name,outside,missing,ids)
 domains.append({'name':name,'plane_axis':axis,'plane_value':plane,'normal':normal,'projection_axes':proj,'seed':ids[0],'faces':ids,'count':len(ids),'support_bounds':list(support.bounds),'support_area_mm2':support.area,'area_mm2':sum(p.area for p in ps),'analytic_area_mm2':support.area,'outside_mm2':outside,'reverse_missing_mm2':missing,'max_plane_residual_mm':float(abs(t[ids,:,axis]-plane).max()),'bounds':[t[ids].min(axis=(0,1)).tolist(),t[ids].max(axis=(0,1)).tolist()],'original_indices':[colors[i] for i in ids]})
faces=sorted(i for d in domains for i in d['faces'])
import zipfile,xml.etree.ElementTree as E,importlib.util
assert hashlib.sha256(raw).hexdigest()=='65c69b86b4e2a05a45a0e4fa53f8b5b5c405a6b2015488ad2e41f870bfb3bc1d' and faces==[4101, 4102, 4104, 4106, 4112, 4114, 4116, 4117, 4122, 4123, 4126, 4127, 4128, 4129, 4137, 4138, 4154, 4158]
with zipfile.ZipFile(A/'ncku-future-venue-front-appearance.3mf') as z:r=E.fromstring(z.read('3D/3dmodel.model'))
ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
v=np.array([[float(x.get(k)) for k in 'xyz'] for x in r.findall('.//m:vertices/m:vertex',ns)]);ts=r.findall('.//m:triangles/m:triangle',ns);f=np.array([[int(x.get(k)) for k in ['v1','v2','v3']] for x in ts]);assigned=np.array([int(x.get('p1')) for x in ts]);assert np.array_equal(v[f],t) and assigned.tolist()==colors
sp=importlib.util.spec_from_file_location('old',A/'source/build_appearance.py');old=importlib.util.module_from_spec(sp);sp.loader.exec_module(old);q=A/'qa/material-boundaries.json';saved=q.read_bytes() if q.exists() else None
try:before,_=old.classify(t)
finally:
 if saved is not None:q.write_bytes(saved)
 elif q.exists():q.unlink()
assert np.flatnonzero(assigned!=before).tolist()==faces and (assigned[faces]==3).all();assert np.bincount(assigned).tolist()==[4515, 372, 120, 35, 2]
result={'status':'PASS_MATERIAL_ONLY','triangles':n,'changed_faces':faces,'counts':np.bincount(assigned).tolist(),'stl_geometry_order_exact':True,'complete_plane_bfs_domains':domains,'actual_area_mm2':sum(d['area_mm2'] for d in domains),'support_area_mm2':sum(d['analytic_area_mm2'] for d in domains),'outside_mm2':sum(d['outside_mm2'] for d in domains),'reverse_missing_mm2':sum(d['reverse_missing_mm2'] for d in domains),'area_tolerance_mm2_per_domain':.001,'limits':'Only left14 right2 and top underside2 portal returns, original7.2 exposed depth/window-cut notches retained. Bottom floor/stairs excluded; original5 shaders unchanged. Coarse proxies not surveyed depth or fine-detail restoration.','source_stl_sha256':hashlib.sha256(raw).hexdigest()}
(A/'qa/current-material-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
