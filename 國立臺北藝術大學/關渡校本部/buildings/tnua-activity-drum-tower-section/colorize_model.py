"""Whole original projecting gable plane x1.9, three complete components only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='af435a570f06d52a5ea5a0462ba8e2520301b62a6bd9ffeae061de230dceca9c';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==3422
t=m.triangles;n=m.face_normals;e=.0001;a=np.full(len(t),1,np.int32);D={}
ids=np.flatnonzero(np.abs(t[:,:,0]-1.9).max(1)<e)
assert len(ids)==33
edges=m.face_adjacency;edges=edges[np.isin(edges[:,0],ids)&np.isin(edges[:,1],ids)]
pcs=trimesh.graph.connected_components(edges,nodes=ids,min_len=1);assert sorted(map(len,pcs))==[7,7,19]
D['whole_projecting_gable']=ids.tolist();a[ids]=0
ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999;cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1);assert all(len(set(a[c]))==1 for c in cs);assert np.bincount(a).tolist()==[33,3389]
pal=[('TNUA Drum Tower observed projecting gable stone gray','#AAA69B'),('UNVERIFIED main walls entrance windows roofs neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':D,'coplanar_components':len(cs),'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'3422 original triangles unchanged','limits':['Sloping roof upper skin, underside, curved eave rolls and crest ornaments remain neutral; code roof descriptions are not photographic color proof.', 'Full-height front y-27 plane crosses lower brick and upper gray with no original material boundary; no whole gray or red.', 'Curved adjoining wall crosses concealed base and material changes, so neutral.', 'Stair/retaining wall signage and people obscure part of extent; neutral.', 'Glass, window frames, gallery rails, x2 projecting columns, opposite gable, rear/cut ends, support and all unlisted triangles remain neutral.', 'Only activity-centre drum-tower local segment, not bell tower, whole activity building, pond or plaza.', 'Correct slug retained; intake alias/copy is not a second model or independent source.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':3422,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],'components',len(cs))
