"""Full original-plane BFS and original wedge/cut forward/reverse support."""
from pathlib import Path
import json,struct,hashlib,zipfile,xml.etree.ElementTree as E,importlib.util
from collections import defaultdict
import numpy as np
from shapely.geometry import Polygon,box
from shapely.ops import unary_union
A=Path(__file__).resolve().parents[1];R=A.parent
raw=(R/'model.stl').read_bytes();sha=hashlib.sha256(raw).hexdigest();assert sha=='b2e1d1ba92c36a14e296f1400752af00738c6df3cc83256686be89ae5fd5e676'
n=struct.unpack_from('<I',raw,80)[0];t=np.array([struct.unpack_from('<9f',raw,96+50*i) for i in range(n)]).reshape(n,3,3)
with zipfile.ZipFile(A/'nthuxin-appearance.3mf') as z:r=E.fromstring(z.read('3D/3dmodel.model'))
ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
v=np.array([[float(x.get(k)) for k in 'xyz'] for x in r.findall('.//m:vertices/m:vertex',ns)]);ts=r.findall('.//m:triangles/m:triangle',ns);f=np.array([[int(x.get(k)) for k in ['v1','v2','v3']] for x in ts]);c=np.array([int(x.get('p1')) for x in ts]);assert np.array_equal(v[f],t)
sp=importlib.util.spec_from_file_location('old',A/'source/build_appearance.py');old=importlib.util.module_from_spec(sp);sp.loader.exec_module(old);before,_=old.classify(t)
changed=np.flatnonzero(c!=before).tolist();assert changed==[4247,4248,4249,4250]+list(range(4252,4274));assert (c[changed]==1).all();assert np.bincount(c).tolist()==[4020,586,456,208]
N=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);N/=np.linalg.norm(N,axis=1)[:,None];mask=(abs(t[:,:,1]+2)<1e-5).all(1)&(N[:,1]<-.999999)
_,iv=np.unique(t.reshape(-1,3),axis=0,return_inverse=True);F=iv.reshape(n,3);edges=defaultdict(list)
for i in np.flatnonzero(mask):
 for a,b in [(0,1),(1,2),(2,0)]:edges[tuple(sorted((int(F[i,a]),int(F[i,b]))))].append(int(i))
adj=defaultdict(set)
for group in edges.values():
 for i in group:adj[i].update(group)
seen={changed[0]};stack=[changed[0]]
while stack:
 for i in adj[stack.pop()]-seen:seen.add(i);stack.append(i)
assert sorted(seen)==changed
wedge=Polygon([(5.5,99),(20.5,99),(13,105)]);link=box(7.5,96,18.5,102)
ring=Polygon([(13+2.1*np.cos(2*np.pi*k/48),101.8+2.1*np.sin(2*np.pi*k/48)) for k in range(48)])
cut=wedge.difference(link.union(ring));polys=list(cut.geoms) if hasattr(cut,'geoms') else [cut];support=max(polys,key=lambda p:p.bounds[3])
tris=[Polygon(t[i][:,[0,2]]) for i in changed];u=unary_union(tris);tol=.001
assert all(p.difference(support).area<tol for p in tris) and support.difference(u).area<tol
assert abs(sum(p.area for p in tris)-support.area)<tol
j={'status':'PASS_MATERIAL_ONLY','triangles':n,'changed_faces':changed,'counts':np.bincount(c).tolist(),'stl_geometry_order_exact':True,'complete_plane_bfs':sorted(seen),'fullvertex_plane_residual_mm':float(abs(t[changed,:,1]+2).max()),'support_area_mm2':support.area,'actual_area_mm2':u.area,'outside_mm2':u.difference(support).area,'reverse_missing_mm2':support.difference(u).area,'each_triangle_outside_mm2':[p.difference(support).area for p in tris],'area_tolerance_mm2':tol,'limits':'Original lower gable removed by link cut; circular cut remains an open notch, not a reconstructed complete enclosed oculus.','source_stl_sha256':sha}
(A/'qa/current-material-verification.json').write_text(json.dumps(j,indent=2)+'\n');print(json.dumps(j))
