"""Complete analytic plane BFS and bidirectional five-point V-polygon support."""
from pathlib import Path
import struct,json,hashlib,zipfile,xml.etree.ElementTree as E,importlib.util
from collections import defaultdict
import numpy as np
from shapely.geometry import Polygon
from shapely.ops import unary_union
A=Path(__file__).resolve().parents[1];R=A.parent
raw=(R/'model.stl').read_bytes();sha=hashlib.sha256(raw).hexdigest();assert sha=='9e1da09414c48e445598abe41ed5f8027a793f9e455bb69a7fe1dc50fd8e7be6'
n=struct.unpack_from('<I',raw,80)[0];t=np.array([struct.unpack_from('<9f',raw,96+50*i) for i in range(n)]).reshape(n,3,3)
with zipfile.ZipFile(A/'nthuqing-appearance.3mf') as z:r=E.fromstring(z.read('3D/3dmodel.model'))
ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
v=np.array([[float(x.get(k)) for k in 'xyz'] for x in r.findall('.//m:vertices/m:vertex',ns)]);ts=r.findall('.//m:triangles/m:triangle',ns);f=np.array([[int(x.get(k)) for k in ['v1','v2','v3']] for x in ts]);c=np.array([int(x.get('p1')) for x in ts]);assert np.array_equal(v[f],t)
sp=importlib.util.spec_from_file_location('old',A/'source/build_appearance.py');old=importlib.util.module_from_spec(sp);sp.loader.exec_module(old);before,_=old.classify(t)
changed=np.flatnonzero(c!=before).tolist();assert changed==[33143,33153,33155] and (c[changed]==5).all()
assert np.bincount(c).tolist()==[30943,940,138,1032,264,3]
N=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);N/=np.linalg.norm(N,axis=1)[:,None];plane=(abs(t[:,:,1]+21)<1e-5).all(1)&(N[:,1]<-.999999)
_,inv=np.unique(t.reshape(-1,3),axis=0,return_inverse=True);F=inv.reshape(n,3);edges=defaultdict(list)
for i in np.flatnonzero(plane):
 for a,b in [(0,1),(1,2),(2,0)]:edges[tuple(sorted((int(F[i,a]),int(F[i,b]))))].append(int(i))
adj=defaultdict(set)
for group in edges.values():
 for i in group:adj[i].update(group)
seen={33143};stack=[33143]
while stack:
 for i in adj[stack.pop()]-seen:seen.add(i);stack.append(i)
assert sorted(seen)==changed
support=Polygon([(-9,123),(9,123),(9,129),(0,126),(-9,129)])
triangles=[Polygon(t[i][:,[0,2]]) for i in changed];u=unary_union(triangles)
assert all(p.difference(support).area<1e-5 for p in triangles)
assert support.difference(u).area<1e-5 and abs(sum(p.area for p in triangles)-support.area)<1e-5
report={'status':'PASS_MATERIAL_ONLY','original_triangles':n,'changed_faces':changed,'counts':np.bincount(c).tolist(),'stl_geometry_order_exact':True,'complete_plane_bfs':sorted(seen),'plane_y_mm':-21,'full_vertex_residual_mm':float(abs(t[changed,:,1]+21).max()),'support_area_mm2':support.area,'each_triangle_outside_mm2':[p.difference(support).area for p in triangles],'reverse_missing_mm2':support.difference(u).area,'source_stl_sha256':sha}
(A/'qa/current-material-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
