"""One complete original front roof fascia with Boolean interruptions preserved."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='b58ec49d9ac34394b02ed4c57ed4e67e6150877b32339a4d14d4fc80c497a1e9';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==4726
t=m.triangles;n=m.face_normals;e=.0001;a=np.full(len(t),1,np.int32);D={}
ids=np.flatnonzero(np.abs(t[:,:,1]+41).max(1)<e)
assert len(ids)==62
edges=m.face_adjacency;edges=edges[np.isin(edges[:,0],ids)&np.isin(edges[:,1],ids)]
pcs=trimesh.graph.connected_components(edges,nodes=ids,min_len=1);assert len(pcs)==1
D['complete_front_roof_fascia']=ids.tolist();a[ids]=0
original=a.copy()
v=np.array([[-36.5,45.5],[-42,60.7],[-35,59.]])
M=np.column_stack((v[1]-v[0],v[2]-v[0]));uv=(t[:,:,1:]-v[0])@np.linalg.inv(M).T
inside=(uv.min((1,2))>=-1e-5)&(uv.sum(2).max(1)<=1.00001)
candidate=np.zeros(len(t),bool);by={}
for x in [-60,-36,-12,12,36,60]:
 q=(np.abs(t[:,:,0]-(x+.95)).max(1)<.0001)&inside&(n[:,0]>.99999);by[str(x)]=np.flatnonzero(q).tolist();candidate|=q
ad=m.face_adjacency;cs=trimesh.graph.connected_components(ad[(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999],nodes=np.arange(len(t)),min_len=1)
assert candidate.sum()==42 and np.all(original[candidate]==1) and all(not candidate[c].any() or candidate[c].all() for c in cs)
a[candidate]=0;assert np.bincount(a).tolist()==[104,4622] and all(len(set(a[c]))==1 for c in cs)
pal=[('Observed front fascia and bounded visible gusset plate sides lightgray','#C7CECC'),('Unverified other original geometry neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'original_domain_face_indices':D,'new_plate_domains':by,'new_face_indices':np.flatnonzero(candidate).tolist(),'original_colored_faces':62,'added_colored_faces':42,'colored_faces':104,'neutral_faces':4622,'coplanar_components':len(cs),'mixed_coplanar_domains':0,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'4726 original triangles and STL/build bytes unchanged','limits':['Only +X planar visible side of six original triangular gusset proxies. Reverse sides/thickness edges/rods stay neutral.','Original solid triangle is simplified detailed tapered/flanged steelwork, not surveyed joints. Mapping covers the original bounded proxy, not measured per-vertex evidence.','Reuse nominal pale lightgray family, not calibrated HEX; shadows not dark material.','No whole roof underside, brick-gray mixed walls, glazing, unknown rear, base or other surfaces newly colored.','Only five-diamond ball hall volume, not swimming pool/connecting hall or entire sports complex.','Original geometry has no later solar panels; not2026 condition. Reference dates unknown; photos private.']}
(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':4726,'original':62,'added':42,'colored':104,'neutral':4622,'mixed_coplanar_domains':0,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2)+'\n');print(q)
