"""Whole original upper beam and two jamb front planes."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='a14fa14bae7f2462d442f7f226862135b32781f7f6f032724ff31bb256a8c7cf';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==2992
t=m.triangles;n=m.face_normals;e=.0001;a=np.full(len(t),1,np.int32);D={}
for name,yy,count,ncomp in [('upper_beam_front',-24.2,6,3),('side_jamb_fronts',-24.5,4,2)]:
 ids=np.flatnonzero(np.abs(t[:,:,1]-yy).max(1)<e);assert len(ids)==count
 edges=m.face_adjacency;edges=edges[np.isin(edges[:,0],ids)&np.isin(edges[:,1],ids)]
 planecomponents=trimesh.graph.connected_components(edges,nodes=ids,min_len=1)
 assert len(planecomponents)==ncomp and all(len(c)==2 for c in planecomponents)
 D[name]=ids.tolist();a[ids]=0
ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999;cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1);assert all(len(set(a[c]))==1 for c in cs);assert np.bincount(a).tolist()==[10,2982]
pal=[('Observed glazed-bay frame fronts off-white','#D3D6D3'),('UNVERIFIED main walls entrance windows roofs neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':D,'coplanar_components':len(cs),'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'2992 original triangles unchanged','limits':['Whole three major roof slopes have real skylights/roof interruptions absent in original plane geometry; no blanket gray roof.', 'Bay glazing, mullions, lower filled support mass and frame side/top/undersides remain neutral.', 'Main full-height walls mix white structure, yellow/green inset panels and dark glazing without reliable original boundaries.', 'Other gallery/front piers and canopy, stairs, all rear surfaces and base remain neutral.', 'Association composite bottom teachers-college view is not color evidence for this model; alternate titled engineering entrance does not transfer its colors to this elevation.', 'Only principal connected science/engineering facade group, not entire college.', '10-face partial recommendation, not full color completion and not formalGO.', 'No geometry corrections, roof openings, panel splits or texture added.', 'Source modification/publication dates are not verified capture; no2026 current-state claim.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':2992,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],'components',len(cs))
