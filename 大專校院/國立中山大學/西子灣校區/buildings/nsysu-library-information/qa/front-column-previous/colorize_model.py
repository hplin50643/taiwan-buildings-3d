"""Complete original v2 south crown outward panel only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='4fde918dd4060a88e5ed64b03e6a233e8e34d176306fd21f16cbd171e14acb35';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==38898
t=m.triangles;n=m.face_normals;e=.0001;a=np.full(len(t),1,np.int32);D={}
ids=np.flatnonzero(np.abs(t[:,:,1]+66.3).max(1)<1e-5);assert len(ids)==179
edges=m.face_adjacency;edges=edges[np.isin(edges[:,0],ids)&np.isin(edges[:,1],ids)]
pcs=trimesh.graph.connected_components(edges,nodes=ids,min_len=1);assert len(pcs)==1
assert ((t[ids,:,0]>=-33.63-1e-5)&(t[ids,:,0]<=33.63+1e-5)&(t[ids,:,2]>=79.61-1e-5)&(t[ids,:,2]<=97.87+1e-5)).all()
D['complete_south_short_crown_outward_panel']=ids.tolist();a[ids]=0
ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999;cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1);assert all(len(set(a[c]))==1 for c in cs);assert np.bincount(a).tolist()==[179,38719]
pal=[('NSYSU Library Information v2 south crown nominal gray brown substrate','#A58F82'),('UNVERIFIED main walls entrance windows roofs neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':D,'coplanar_components':len(cs),'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'38898 original triangles unchanged','limits':['No arc recess interior/underside/top/rear/long elevations/roof machine color inferred.', 'South is original drawing/entry-relative label, not surveyed world orientation.', 'Model bridge connector artificial closure not real facade; remain neutral.', 'Commons2024 original pixels GET403 stopped and not used; 2026 photo only original citation, not read or used as color evidence.', 'Preserve all original v2 geometry/source/printability limits and original previews; no globalQA recertification or current/asbuilt assertion.', 'One existing mainblock; no newbuilding/count increase; still partial.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':38898,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],'components',len(cs))
