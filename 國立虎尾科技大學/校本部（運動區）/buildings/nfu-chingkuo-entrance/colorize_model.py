"""Seven complete original central short rib end rectangles only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='99578e16887d6d610bd1b7a1f132337bb002a133f816ff6cdce136b34ebc5e3d';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==3438
t=m.triangles;n=m.face_normals;e=.0001;a=np.full(len(t),1,np.int32);D={}
ids=np.flatnonzero(np.abs(t[:,:,1]+10).max(1)<e)
assert len(ids)==18
edges=m.face_adjacency;edges=edges[np.isin(edges[:,0],ids)&np.isin(edges[:,1],ids)]
pcs=trimesh.graph.connected_components(edges,nodes=ids,min_len=1);assert sorted(map(len,pcs))==[2]*9
selected=[]
for c in pcs:
 q=t[c];center=(q[:,:,0].min()+q[:,:,0].max())/2
 if any(abs(center-v)<e for v in [-48,-32,-16,0,16,32,48]):
  assert len(c)==2 and abs(q[:,:,0].max()-q[:,:,0].min()-1.5)<e
  D['complete_central_rib_end_'+str(round(center))]=c.tolist();selected.extend(c)
assert len(selected)==14;a[selected]=0
ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999;cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1);assert all(len(set(a[c]))==1 for c in cs);assert np.bincount(a).tolist()==[14,3424]
pal=[('NFU Chingkuo Entrance observed seven central rib front ends pale cream','#D3D0C0'),('UNVERIFIED main walls entrance windows roofs neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':D,'coplanar_components':len(cs),'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'3438 original triangles unchanged','limits':['Rib side/underside surfaces, outermost2 ribs, all large roof/soffit/fascia surfaces stay neutral.', 'Title canopy underside includes lights and dark ceiling material; shadow does not justify blanket black.', 'Front columns and side buttresses carry event banners, signage or are partly obscured by temporary arch; no all-pale column family.', 'Glass/backings contain pale frames, colored curtains and reflections; no all-blue glass.', 'Stairs, parapet proxies, ground, temporary event objects and all unlisted triangles remain neutral.', 'Preserve3438 original triangles and geometry; no new boundaries/lettering/event geometry or exports.', 'Only front entrance facade section; illustrative20mm cut depth is not surveyed full gym/rear.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':3438,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],'components',len(cs))
