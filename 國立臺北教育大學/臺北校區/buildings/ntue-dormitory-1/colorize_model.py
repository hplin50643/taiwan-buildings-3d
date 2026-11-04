"""Finite original 24gon column facets; original Boolean embedding retained."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='1dbeb4552b226347f0ede3b62f4e1039397ef6aceae33c6af2614069aab3e0e8';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==3170
t=m.triangles;n=m.face_normals;e=.0001;a=np.full(len(t),1,np.int32);D={}
for x in [-10.5,10.5]:
 xy=t[:,:,:2]-np.array([x,-29]);idsall=[];facets={}
 for j in range(24):
  theta=2*np.pi*(j+.5)/24;nn=np.array([np.cos(theta),np.sin(theta)]);tt=np.array([-nn[1],nn[0]])
  if nn[1]>=0:continue
  hit=(abs(xy@nn-1.3*np.cos(np.pi/24)).max(1)<=e)&(abs(xy@tt).max(1)<=1.3*np.sin(np.pi/24)+e)&(t[:,:,2].min(1)>=3-e)&(t[:,:,2].max(1)<=17+e)
  ids=np.flatnonzero(hit)
  if len(ids):facets[str(j)]=ids.tolist();idsall+=ids.tolist()
 assert len(idsall)==len(set(idsall))==10;assert len(facets)==5;a[idsall]=0;D[str(x)]={'indices':idsall,'finite_facets':facets}
ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999;cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1);assert all(len(set(a[c]))==1 for c in cs);assert np.bincount(a).tolist()==[20,3150]
pal=[('Observed entrance twin columns exposed front skin light gray','#CDD0C9'),('UNVERIFIED brick walls caps glass roofs neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':D,'coplanar_components':len(cs),'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'3170 original triangles unchanged','limits':['Only two original24gon column front finite facets, all vertices chord/tangent/z3..17;10+10 surviving triangles.','Boolean embedding within original fan body retained, not standalone reconstructed columns.','Mixed brick ends, caps and window backs neutral; only Dormitory1 evidence, no borrowed Dormitory2 rear.','Photo capture unknown;2023form date not capture.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':3170,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],'components',len(cs))
