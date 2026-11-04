"""Nine complete original outward louver rectangles only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='853c057591a890c9923fe3fb219f345fedaff79a3a1d27eabac799b7ff83fee4';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==3416
t=m.triangles;n=m.face_normals;lo=t.min(1);hi=t.max(1);e=.0001;a=np.full(len(t),1,np.int32)
pal=[('Observed original front louvers nominal charcoal','#4D5252'),('UNVERIFIED mixed walls wood proxies courtyard roof neutral','#B8BAB5')];D={}
for k in range(9):
 z=24+k*2.8
 mask=(np.max(abs(t[:,:,1]+63),axis=1)<e)&(lo[:,0]>=21.5-e)&(hi[:,0]<=52.5+e)&(lo[:,2]>=z-e)&(hi[:,2]<=z+1.2+e)
 ids=np.flatnonzero(mask).tolist();assert len(ids)==2;assert abs(m.area_faces[ids].sum()-37.2)<.001;assert np.all(n[ids,1]<-.99999);D[f'front_louver_z{z}']=ids;a[ids]=0
ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999;cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1)
assert all(len(set(a[c]))==1 for c in cs);assert np.bincount(a).tolist()==[18,3398]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':D,'coplanar_components':len(cs),'coplanar_neutralized_faces':[],'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'3416 original triangles unchanged','limits':['Only nine complete original louverfront rectangles18triangles y-63.','Louver top/bottom/end/back and recessed backing neutral, no filled black gaps.','Wood folded-panel proxies, simplified courtyard bowl, all mixed walls roofs stairs columns neutral.','One original connected complex/count0; photo capture unknown,not2026survey.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':3416,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],'components',len(cs))
