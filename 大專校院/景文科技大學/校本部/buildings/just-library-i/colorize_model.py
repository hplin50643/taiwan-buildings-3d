"""Whole original upper setback cap front edge only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='13af7f41db8f2e61ba1542b8e36f4514217f01ed838e2c22997a980f5963b31a';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==1582
t=m.triangles;n=m.face_normals;e=.0001;a=np.full(len(t),1,np.int32);D={}
ids=np.flatnonzero(np.abs(t[:,:,1]+5.5).max(1)<e)
assert len(ids)==2
edges=m.face_adjacency;edges=edges[np.isin(edges[:,0],ids)&np.isin(edges[:,1],ids)]
pcs=trimesh.graph.connected_components(edges,nodes=ids,min_len=1);assert sorted(map(len,pcs))==[2]
D['whole_upper_setback_cap_front']=ids.tolist();a[ids]=0
ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999;cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1);assert all(len(set(a[c]))==1 for c in cs);assert np.bincount(a).tolist()==[2,1580]
pal=[('JUST Library I observed upper setback cap pale warm gray','#CECBC2'),('UNVERIFIED main walls entrance windows roofs neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':D,'coplanar_components':len(cs),'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'1582 original triangles unchanged','limits':['Entire upper slab top, underside, left/right returns and rear remain neutral; no material-family extrapolation from its front edge.', 'Main three-rank screen mixes pale panels, darker windows and frames without complete original material boundaries; no blanket pale facade or black window backing.', 'Right tower contains multicolor banners and sign elements absent from modeled surface; no all-gray tower.', 'Ground-floor piers, entrance canopy and lower walls partly vegetation-obscured or not fully matched; remain neutral.', 'Roof room, lower roof terrace, stairs, base and unlisted faces remain neutral.', 'Rear was deliberately modeled blank for lack of clear rear photograph; not inferred from front.', 'Preserve1582 original faces and existing geometry; no face splitting, new material boundaries or OBJ generation.', 'Nominal pale gray family only, not calibrated stone texture or complete building coloring.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':1582,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],'components',len(cs))
