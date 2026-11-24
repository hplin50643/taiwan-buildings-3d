"""Original complete entry front fascia rectangle only; geometry untouched."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='b097b43c754db67ab0281e4e660de2084042903d89c3deed954b3f9cf88fea42';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==2756
t=m.triangles;n=m.face_normals;lo=t.min(1);hi=t.max(1);e=.0001;a=np.full(len(t),1,np.int32)
pal=[('Observed entry front fascia nominal cobalt','#26466F'),('UNVERIFIED mixed facade rear roof neutral','#B8BAB5')];D={}
for name,y,x0,x1,z0,z1,mat in [('entry_front_fascia',-31,-4,68,27.4,29.1,0)]:
 mask=(np.max(abs(t[:,:,1]-y),axis=1)<e)&(n[:,1]<-.999999)&(lo[:,0]>=x0-e)&(hi[:,0]<=x1+e)&(lo[:,2]>=z0-e)&(hi[:,2]<=z1+e)
 ids=np.flatnonzero(mask).tolist();assert len(ids)==2;assert abs(m.area_faces[ids].sum()-(x1-x0)*(z1-z0))<.001
 assert np.allclose(lo[ids].min(0),[x0,y,z0],atol=e) and np.allclose(hi[ids].max(0),[x1,y,z1],atol=e)
 D[name]=ids;a[ids]=mat
ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999;cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1)
assert all(len(set(a[c]))==1 for c in cs);assert np.bincount(a).tolist()==[2,2754]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':D,'coplanar_components':len(cs),'coplanar_neutralized_faces':[],'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'2756 original triangles unchanged','limits':['Only one whole finite original entry fascia rectangle2triangles, allvertices and exactarea checked.','Red balcony frame mixes floor/parapet solids; diagonal blade mixes grayfoot without boundary, allneutral.','Entire fullwidth cap neutral because it fuses photographed pinkleft and redright without boundary. Canopy top and bottom, glass/window/rail proxies, mixed mainfacade, rear and plaza neutral.','First Campus West identity retained, notYanchao; unknown capture;2025–26 improvement not verified complete.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':2756,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],'components',len(cs))
