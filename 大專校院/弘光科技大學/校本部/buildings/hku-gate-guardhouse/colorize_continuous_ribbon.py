from pathlib import Path
import numpy as np,json,hashlib,collections
P=Path(__file__).resolve().parent;Q=P/'qa-continuous-walls';Q.mkdir(exist_ok=True);r=json.load(open(P/'ribbon-continuity-domains.json'));H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert H(P/'ribbon-baseline-color-mesh.npz')==r['source_color_mesh_sha256'];assert H(P/'model.stl')==r['source_stl_sha256'];assert H(P/'palette.json')==r['source_palette_sha256'];n=np.load(P/'ribbon-baseline-color-mesh.npz');v=n['vertices'];f=n['faces'];m=n['materials'];t=v[f];rx=np.radians(3);ry=np.radians(-12);RX=np.array([[1,0,0],[0,np.cos(rx),-np.sin(rx)],[0,np.sin(rx),np.cos(rx)]]);RY=np.array([[np.cos(ry),0,np.sin(ry)],[0,1,0],[-np.sin(ry),0,np.cos(ry)]]);scale=np.ptp(t[:,:,0])/110;local=(t/scale-[0,0,43])@(RY@RX);cr=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);norm=cr/np.linalg.norm(cr,axis=1)[:,None];edges=collections.defaultdict(list)
for i,q in enumerate(f):
 for k in range(3):edges[tuple(sorted((q[k],q[(k+1)%3])))].append(i)
adj=collections.defaultdict(set)
for a in edges.values():
 if len(a)==2 and np.dot(norm[a[0]],norm[a[1]])>.999999:adj[a[0]].add(a[1]);adj[a[1]].add(a[0])
cs=[];seen=set()
for i in range(len(f)):
 if i in seen:continue
 c={i};stack=[i];seen.add(i)
 while stack:
  for k in adj[stack.pop()]-seen:seen.add(k);c.add(k);stack.append(k)
 cs.append(c)
groups=[];allids=[]
for k in [14,15,24,43,44,45,46,47]:
 a0=2*np.pi*k/96;a1=2*np.pi*(k+1)/96;p0=np.array([38*np.cos(a0),-2+25*np.sin(a0)]);p1=np.array([38*np.cos(a1),-2+25*np.sin(a1)]);length=np.linalg.norm(p1-p0);tan=(p1-p0)/length;nn=np.array([-tan[1],tan[0]]);vec=local[:,:,:2]-p0;dist=vec@nn;along=vec@tan;plane=(abs(dist)<1e-5).all(1);finite=plane&(along>=-1e-5).all(1)&(along<=length+1e-5).all(1)&(local[:,:,2]>=-1e-5).all(1)&(local[:,:,2]<=19+1e-5).all(1);ids=np.flatnonzero(finite).tolist();assert np.array_equal(plane,finite) and len(ids)==2 and np.all(m[ids]==1);assert any(c==set(ids)for c in cs);uv=np.unique(local[ids].reshape(-1,3),axis=0);assert len(uv)==4
 expected=np.array([[*p,z]for p in[p0,p1]for z in[0.,19.]])
 assert all(min(np.linalg.norm(u-e)for e in expected)<1e-5 for u in uv)
 area=float(np.linalg.norm(cr[ids],axis=1).sum()/2);analytic=float(length*19*scale*scale);assert abs(area-analytic)<3e-5
 groups.append({'facet':k,'faces':ids,'chord_endpoints':[p0.tolist(),p1.tolist()],'local_z':[0,19],'mesh_area_mm2':area,'analytic_area_mm2':analytic,'infinite_plane_equals_complete_finite_domain':True,'four_original_corners_match':True});allids+=ids
assert len(allids)==16;new=m.copy();new[allids]=0;assert np.bincount(m).tolist()==[114,2446] and np.bincount(new).tolist()==[130,2430];assert all(len(set(new[list(c)]))==1 for c in cs)

assert sorted(allids)==r['face_ids'];assert np.array_equal(new[m!=1],m[m!=1]);assert np.flatnonzero(new!=m).tolist()==r['face_ids']
raw=(P/'model.stl').read_bytes();st=np.frombuffer(raw,offset=84,dtype=np.dtype([('n','<f4',3),('v','<f4',(3,3)),('attr','<u2')]))['v'];assert np.array_equal(st,t)
np.savez_compressed(P/'color-mesh.npz',vertices=v,faces=f,materials=new)
(Q/'selection.json').write_text(json.dumps(dict(changed_faces=16,face_ids=sorted(allids),existing_colored_faces_preserved=114,counts=[130,2430],original_triangle_geometry_and_order_exact=True,finite_complete_facets=8,coplanar_components=len(cs),groups=groups),indent=2)+'\n');print('PASS16finiteouterribbonreturns;2560originaltriangles;current114graypreserved')
