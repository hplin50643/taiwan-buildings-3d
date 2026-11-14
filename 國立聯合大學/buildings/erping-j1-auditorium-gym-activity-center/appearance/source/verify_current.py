from pathlib import Path
import struct,json,collections,hashlib
import numpy as np
A=Path(__file__).resolve().parents[1];R=A.parent;O=R;raw=(O/'model.stl').read_bytes();n=struct.unpack_from('<I',raw,80)[0];t=np.array([struct.unpack_from('<9f',raw,96+50*i) for i in range(n)]).reshape(n,3,3)
v=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);area=np.linalg.norm(v,axis=1)/2;norm=v/(2*area[:,None]);colors=json.loads((O/'appearance/face-materials.json').read_text())['face_material_indices'];edges=collections.defaultdict(list)
for i,tri in enumerate(t):
 for a,b in [(0,1),(1,2),(2,0)]:edges[tuple(sorted((tuple(tri[a]),tuple(tri[b]))))].append(i)
adj=[set() for _ in t]
for fs in edges.values():
 for i in fs:adj[i].update(set(fs)-{i})
domains=[];visited=set()
for seed in range(n):
 if seed in visited:continue
 normal=norm[seed];offset=float(normal@t[seed,0]);mask=(np.max(abs(t@normal-offset),axis=1)<1e-5)&(norm@normal>1-1e-8)
 seen={seed};stack=[seed]
 while stack:
  for j in adj[stack.pop()]:
   if mask[j] and j not in seen:seen.add(j);stack.append(j)
 visited.update(seen);ids=sorted(seen)
 domains.append({'seed':seed,'faces':ids,'count':len(ids),'normal':normal.tolist(),'plane_offset':offset,'max_plane_residual_mm':float(np.max(abs(t[ids]@normal-offset))),'bounds':[t[ids].min(axis=(0,1)).tolist(),t[ids].max(axis=(0,1)).tolist()],'area_mm2':float(area[ids].sum()),'material_counts':dict(collections.Counter(colors[i] for i in ids)),'current_indices':[colors[i] for i in ids]})

import math
from shapely.geometry import Polygon,LineString,Point
from shapely.ops import unary_union
ds=domains; points=np.array([(165*math.sin(math.radians(a)),120-165*math.cos(math.radians(a))) for a in np.linspace(-17.6,17.6,65)])
candidates=[d for d in ds if d['bounds'][0][2]>=2.39 and d['bounds'][1][2]<=2.951 and d['normal'][1]<-.8 and abs(d['normal'][2])<.01];assert len(candidates)==64
out=[]
for a,b in zip(points[:-1],points[1:]):
 v=b-a; length=np.linalg.norm(v); u=v/length
 normal=np.array([u[1],-u[0],0]); offset=normal[:2]@a
 matches=[d for d in candidates if np.max(abs(t[d['faces']]@normal-offset))<1e-5 and np.dot(d['normal'],normal)>1-1e-8];assert len(matches)==1
 d=matches[0].copy(); ids=d['faces']; p=t[ids]; polygons=[Polygon(np.column_stack(((tri[:,:2]-a)@u,tri[:,2]))) for tri in p]; actual=unary_union(polygons); expected=Polygon([(0,2.4),(length,2.4),(length,2.95),(0,2.95)])
 extra=actual.difference(expected).area;missing=expected.difference(actual).area;assert extra<1e-5 and missing<1e-5
 tower_dist=LineString([a,b]).distance(Point(-58,-24));assert tower_dist>13.3
 d['analytic_support']={'original_step_i':0,'radius':165,'CY':120,'endpoints':[a.tolist(),b.tolist()],'z':[2.4,2.95],'base_clips_original_bottom_2_3':True,'area':expected.area,'outside_area':extra,'missing_area':missing,'tower_center_distance':tower_dist,'tower_radius':13.3,'tower_does_not_intersect':True,'right_terrace_min_x':50.5,'right_terrace_does_not_intersect':bool(max(a[0],b[0])<50.5)};out.append(d)

ids=sorted(i for d in out for i in d["faces"])

import zipfile,xml.etree.ElementTree as E,importlib.util
assert ids==[167, 169, 170, 171, 175, 176, 177, 182, 184, 185, 188, 189, 190, 192, 193, 194, 203, 204, 206, 209, 210, 211, 215, 216, 218, 221, 222, 224, 227, 228, 229, 230, 231, 232, 233, 234, 236, 238, 239, 241, 251, 252, 254, 257, 258, 259, 263, 264, 265, 267, 268, 269, 273, 274, 275, 277, 278, 279, 284, 286, 288, 291, 294, 296, 300, 302, 303, 307, 310, 312, 314, 317, 319, 322, 323, 324, 328, 329, 330, 333, 334, 335, 338, 339, 341, 343, 345, 347, 348, 351, 352, 354, 356, 357, 358, 360, 361, 362, 363, 364, 372, 374, 375, 378, 381, 382, 383, 385, 386, 390, 392, 394, 397, 400, 401, 403, 404, 405, 409, 411, 413, 415, 417, 419, 421, 422, 425, 428] and n==16168
with zipfile.ZipFile(A/'nuuj1-appearance.3mf') as z:r=E.fromstring(z.read('3D/3dmodel.model'))
ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
vs=np.array([[float(x.get(k)) for k in 'xyz'] for x in r.findall('.//m:vertices/m:vertex',ns)]);ts=r.findall('.//m:triangles/m:triangle',ns);fs=np.array([[int(x.get(k)) for k in ['v1','v2','v3']] for x in ts]);assigned=np.array([int(x.get('p1')) for x in ts]);assert np.array_equal(vs[fs],t) and assigned.tolist()==colors
sp=importlib.util.spec_from_file_location('old',A/'source/build_appearance.py');old=importlib.util.module_from_spec(sp);sp.loader.exec_module(old);before,_=old.classify(t)
assert np.flatnonzero(assigned!=before).tolist()==ids and (assigned[ids]==7).all()
result={'status':'PASS_MATERIAL_ONLY','triangles':n,'changed_faces':ids,'counts':np.bincount(assigned).tolist(),'stl_geometry_order_exact':True,'complete_plane_bfs_domains':out,'area_tolerance_mm2_per_domain':1e-5,'source_stl_sha256':hashlib.sha256(raw).hexdigest()}
result.update(actual_area_mm2=sum(d['area_mm2'] for d in out),support_area_mm2=sum(d['analytic_support']['area'] for d in out),outside_mm2=sum(d['analytic_support']['outside_area'] for d in out),reverse_missing_mm2=sum(d['analytic_support']['missing_area'] for d in out))
(A/'qa/current-material-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
