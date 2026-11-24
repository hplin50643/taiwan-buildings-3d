"""Four complete original projecting-room outward mullion rectangles only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='6fce4a4f62cf190bf0d3cfd4285bf7b983ae074d8d3499ec156414c27cae85c4';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==6662
t=m.triangles;n=m.face_normals;lo=t.min(1);hi=t.max(1);e=.0001;a=np.full(len(t),1,np.int32)
pal=[('Observed projecting room front frame nominal lightgray','#D3D4CE'),('UNVERIFIED brick-gray blocks glass roof neutral','#B8BAB5')];D={}
for x in [36,42,48,54]:
 mask=(np.max(abs(t[:,:,1]+66),axis=1)<e)&(lo[:,0]>=x-.6-e)&(hi[:,0]<=x+.6+e)&(lo[:,2]>=15.5-e)&(hi[:,2]<=23.5+e)
 ids=np.flatnonzero(mask).tolist();assert len(ids)==2;assert abs(m.area_faces[ids].sum()-9.6)<.001;assert np.all(n[ids,1]<-.99999);D[f'front_mullion_x{x}']=ids;a[ids]=0
ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999;cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1)
assert all(len(set(a[c]))==1 for c in cs);assert np.bincount(a).tolist()==[8,6654]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':D,'coplanar_components':len(cs),'coplanar_neutralized_faces':[],'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'6662 original triangles unchanged','limits':['Only four complete projecting-room front mullion rectangles8triangles y-66.','All frame side/top/back, glassproxy and roomskin neutral.','Four mixed brick-gray blocks,balconies,bridges,roofs,stairs,courtyard neutral; no extrapolated repeated colors.','A–D plus connected dormitory stays one originalcomplex/count0; photo capture unknown,not2026survey.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':6662,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],'components',len(cs))
