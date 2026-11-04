"""Whole original open front gable fascia plane only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='d89f40d9b54331b72d9f6c1b4c0e2ad364c8fb3c10decedbb60cea4783437093';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==816
t=m.triangles;n=m.face_normals;e=.0001;a=np.full(len(t),1,np.int32);D={}
ids=np.flatnonzero(np.abs(t[:,:,1]+15.5).max(1)<e)
assert len(ids)==7
edges=m.face_adjacency;edges=edges[np.isin(edges[:,0],ids)&np.isin(edges[:,1],ids)]
pcs=trimesh.graph.connected_components(edges,nodes=ids,min_len=1);assert len(pcs)==1
D['whole_front_open_gable_fascia']=ids.tolist();a[ids]=0
ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999;cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1);assert all(len(set(a[c]))==1 for c in cs);assert np.bincount(a).tolist()==[7,809]
pal=[('Observed complete front open gable fascia offwhite','#D3D6D3'),('UNVERIFIED main walls entrance windows roofs neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':D,'coplanar_components':len(cs),'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'816 original triangles unchanged','limits':['Roof upper skins, inner underside, rear gable and depthwise edges remain neutral; white front trim is not transferred to whole shell.', 'Piers include gray stone, yellow stripes and notices not independently bounded; no blanket gray.', 'Horizontal sign band contains wording; whole original plane neutral.', 'Actual green approach has differently bounded pavement/curbs; original ramp and solid parapets neutral.', 'Blue-green truss, wall/window backs, exterior vegetation/AC fixtures, hidden rear and section cuts neutral.', 'Central entrance pavilion and one window bay per side only, not whole tennis/multiuse hall; one existing building group.', 'Capture date unknown; PV plans or multiuse naming do not prove current installations/2026 appearance.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':816,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],'components',len(cs))
