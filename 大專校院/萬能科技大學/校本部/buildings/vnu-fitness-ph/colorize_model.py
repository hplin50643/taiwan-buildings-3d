"""Whole original front truncated hip trapezoid only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='daefed1bcc038fb92041ed471265e845f715be141e0f940b5397c153d40fb053';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==340
t=m.triangles;n=m.face_normals;e=.0001;a=np.full(len(t),1,np.int32);D={}
dist=np.abs(13*(t[:,:,1]+56)-43.68*(t[:,:,2]-26))/np.hypot(13,43.68)
ids=np.flatnonzero(dist.max(1)<e)
u=(t[:,:,1]+56)/43.68
halfwidth=42-32.76*u
finite=((u>=-e)&(u<=1+e)&(np.abs(t[:,:,0])<=halfwidth+e)).all(1)
assert np.array_equal(ids,np.flatnonzero((dist.max(1)<e)&finite))
assert len(ids)==2
edges=m.face_adjacency;edges=edges[np.isin(edges[:,0],ids)&np.isin(edges[:,1],ids)]
pcs=trimesh.graph.connected_components(edges,nodes=ids,min_len=1);assert len(pcs)==1;assert all(len(c)==2 for c in pcs)
D['whole_front_hip_skin']=ids.tolist();a[ids]=0
ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999;cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1);assert all(len(set(a[c]))==1 for c in cs);assert np.bincount(a).tolist()==[2,338]
pal=[('VNU PH observed front hip pale gray','#D2D5D1'),('UNVERIFIED main walls entrance windows roofs neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':D,'coplanar_components':len(cs),'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'340 original triangles unchanged','limits':['Left and right diagonal roof slopes and all rear slopes remain neutral, not copied by symmetry.', 'Central flat truncated top, roof underside and thin edge faces remain neutral.', 'Main wall carries dark Chinese/English lettering and windows/frames; no uniform wall coloring.', 'Door, glass backing, side openings, rear wall and ground remain neutral.', 'Preserve340 original faces and octagonal truncated-hip approximation; no changes to slope, geometry, roof partitions or openings.', 'Original190x143 image establishes nominal pale family only; no calibrated finish or2026 condition claim.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':340,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],'components',len(cs))
