"""Entire original lake-facing plane, one component."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='2b79321536cdecd979ecae1d67a6b656992089400802ab55cc502cd19eec9aa3';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==3662
t=m.triangles;n=m.face_normals;e=.0001;a=np.full(len(t),1,np.int32);D={}
ids=np.flatnonzero(np.abs(t[:,:,1]+25).max(1)<e)
assert len(ids)==203
edges=m.face_adjacency;edges=edges[np.isin(edges[:,0],ids)&np.isin(edges[:,1],ids)]
planecomponents=trimesh.graph.connected_components(edges,nodes=ids,min_len=1)
assert len(planecomponents)==1 and len(planecomponents[0])==203
D['entire_lake_wall_y_minus25']=ids.tolist();a[ids]=0
ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999;cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1);assert all(len(set(a[c]))==1 for c in cs);assert np.bincount(a).tolist()==[203,3459]
pal=[('Observed whole lake-facing wall nominal pale gray','#D3D6D3'),('UNVERIFIED main walls entrance windows roofs neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':D,'coplanar_components':len(cs),'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'3662 original triangles unchanged','limits':['Central glazed recess, its original thickened mullions and scattered window backs/returns; no uniformly cyan glass.', 'InnerV faces: lower entry/glazing/vent details are not all cut into this simplified original surface; keep complete planes neutral rather than extrapolate stone over omitted doors.', 'Grass roof slopes with mixed paths/retaining strips/railings lacking original boundaries; no solidgreen blanket.', 'Low information wing contains pale, gray, green vertical strips and glass not completely separated in original geometry; whole low wing remains neutral.', 'Roof/top/copings outside selected frontplane, side walls, entrance wedge, ground/base and steps remain neutral.', 'Mountain main library plus low information wing is one model group, not separate new deliveries.', 'OriginalV/notch and scattered-window rhythm remain approximate; no new geometry, texture, paths, window schedules or interiors.', '203-face partial recommendation only, not full-color completion or formalGO.', 'EXIF306 modification dates not capture dates; no2026 current-state claim.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':3662,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],'components',len(cs))
