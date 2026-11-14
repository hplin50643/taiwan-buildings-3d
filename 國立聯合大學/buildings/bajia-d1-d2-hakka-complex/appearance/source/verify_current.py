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
domains=[]
# Fresh original stairs(-32,-20.5,-53,-31,3,17,14), overlap .08.
# Subsequent boxes hide overlap at every step; base top z3 hides underside.
for i in range(3):
 y0=-53+22*i/14;y1=-53+22*(i+1)/14;z0=3+i;z1=4+i
 for kind,axis,value,direction,axes,support in [('tread',2,z1,1,[0,1],box(-32,y0,-20.5,y1)),('front_riser',1,y0,-1,[0,2],box(-32,z0,-20.5,z1))]:
  res=abs(t[:,:,axis]-value);mask=np.all(res<1e-5,axis=1)&(norm[:,axis]*direction>.999999)
  centers=t.mean(axis=1);candidates=[j for j in map(int,np.flatnonzero(mask)) if support.buffer(1e-6).contains(__import__('shapely').geometry.Point(centers[j,axes]))];assert candidates
  seen={min(candidates)};stack=list(seen)
  while stack:
   for j in adj[stack.pop()]:
    if mask[j] and j not in seen:seen.add(j);stack.append(j)
  ids=sorted(seen);ps=[Polygon(t[j][:,axes]) for j in ids];u=unary_union(ps);outside=sum(p.difference(support).area for p in ps);missing=support.difference(u).area
  assert outside<.003 and missing<.003,(i,kind,ids,outside,missing)
  domains.append({'name':f'D1_step_{i+1}_{kind}','step_index':i,'seed':ids[0],'faces':ids,'count':len(ids),'plane_axis':axis,'plane_value':value,'normal_sign':direction,'projection_axes':axes,'support_polygon':list(support.exterior.coords),'support_area_mm2':support.area,'actual_area_mm2':sum(p.area for p in ps),'outside_mm2':outside,'reverse_missing_mm2':missing,'max_plane_residual_mm':float(res[ids].max()),'bounds':[t[ids].min(axis=(0,1)).tolist(),t[ids].max(axis=(0,1)).tolist()],'current_indices':[colors[j] for j in ids]})
ids=sorted(j for d in domains for j in d['faces']);assert len(ids)==len(set(ids))

import zipfile,xml.etree.ElementTree as E,importlib.util
assert ids==[523, 526, 533, 534, 538, 539, 551, 552, 555, 556, 557, 558] and n==4476
with zipfile.ZipFile(A/'nuud12-appearance.3mf') as z:r=E.fromstring(z.read('3D/3dmodel.model'))
ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
vs=np.array([[float(x.get(k)) for k in 'xyz'] for x in r.findall('.//m:vertices/m:vertex',ns)]);ts=r.findall('.//m:triangles/m:triangle',ns);fs=np.array([[int(x.get(k)) for k in ['v1','v2','v3']] for x in ts]);assigned=np.array([int(x.get('p1')) for x in ts]);assert np.array_equal(vs[fs],t) and assigned.tolist()==colors
sp=importlib.util.spec_from_file_location('old',A/'source/build_appearance.py');old=importlib.util.module_from_spec(sp);sp.loader.exec_module(old);before,_=old.classify(t)
assert np.flatnonzero(assigned!=before).tolist()==ids and (assigned[ids]==7).all()
result={'status':'PASS_MATERIAL_ONLY','triangles':n,'changed_faces':ids,'counts':np.bincount(assigned).tolist(),'stl_geometry_order_exact':True,'complete_plane_bfs_domains':domains,'area_tolerance_mm2_per_domain':.003,'source_stl_sha256':hashlib.sha256(raw).hexdigest()}
for k in ['actual_area_mm2','support_area_mm2','outside_mm2','reverse_missing_mm2']:result[k]=sum(d[k] for d in domains)
(A/'qa/current-material-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
