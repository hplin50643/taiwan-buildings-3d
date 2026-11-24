"""Whole original entrance cap front and right edge planes only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='0cb4d2834e6d59d34eb79a55f763518bcf2e19a9c447912f74a6cf1168fed25d';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==6028
t=m.triangles;n=m.face_normals;e=.0001;a=np.full(len(t),1,np.int32);D={}
for label,axis,plane in [('cap_front',1,-40),('cap_right',0,64.5)]:
 ids=np.flatnonzero(np.abs(t[:,:,axis]-plane).max(1)<e)
 assert len(ids)==2
 edges=m.face_adjacency;edges=edges[np.isin(edges[:,0],ids)&np.isin(edges[:,1],ids)]
 pcs=trimesh.graph.connected_components(edges,nodes=ids,min_len=1);assert len(pcs)==1;assert all(len(c)==2 for c in pcs)
 D[label]=ids.tolist();a[ids]=0
ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999;cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1);assert all(len(set(a[c]))==1 for c in cs);assert np.bincount(a).tolist()==[4,6024]
pal=[('TNUA Kuandu observed entry cap silver gray','#AAB0B2'),('UNVERIFIED main walls entrance windows roofs neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':D,'coplanar_components':len(cs),'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'6028 original triangles unchanged','limits':['Cap roof upper skin, soffit, rear/left returns remain neutral.', 'Glass backing contains blinds, reflections and inner doors; do not paint solid blue.', 'Front and side frame domains remain neutral in this narrow review; no inferred metallic color through base/skirt transitions.', 'Left curved wall lower areas obscured by vegetation; brick inset partly covered by exhibition banners. No whole-wall white/red.', 'Low curved wall contains dark museum plaque; not uniformly white.', 'Stair treads, risers, terrace, skylight, rear curves, roof boundaries and all remaining faces remain neutral.', 'Only the existing upper fourth-floor entry/curved roof segment, not the whole museum/downhill storeys or neighboring research buildings.', 'Architect-source project evidence does not assign all historic exterior design authorship to that firm.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':6028,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],'components',len(cs))
