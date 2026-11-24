"""Four complete original uppermost window-head front rectangles only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='f8941efc458ff2df0707ebf20bcae8845c91ed056212a38845e6b00696cd9ade';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==3606
t=m.triangles;n=m.face_normals;e=.0001;a=np.full(len(t),1,np.int32);D={}
ids=np.flatnonzero(np.abs(t[:,:,1]+7.45).max(1)<e)
assert len(ids)==32
edges=m.face_adjacency;edges=edges[np.isin(edges[:,0],ids)&np.isin(edges[:,1],ids)]
pcs=trimesh.graph.connected_components(edges,nodes=ids,min_len=1);assert sorted(map(len,pcs))==[2]*16
selected=[]
for c in pcs:
 lo=t[c].reshape(-1,3).min(0);hi=t[c].reshape(-1,3).max(0)
 if any(abs(lo[2]-z)<e and abs(hi[2]-(z+1.1))<e for z in [90,105]):
  assert abs(hi[0]-lo[0]-30)<e;selected.extend(c.tolist())
assert len(selected)==8
D['four_complete_upper_window_head_fronts']=selected;a[selected]=0
ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999;cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1);assert all(len(set(a[c]))==1 for c in cs);assert np.bincount(a).tolist()==[8,3598]
pal=[('MCUT Innovation Facade Segment observed upper window heads muted gray','#929894'),('UNVERIFIED main walls entrance windows roofs neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':D,'coplanar_components':len(cs),'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'3606 original triangles unchanged','limits':['Other12 window heads remain neutral in this conservative review; right lower heads obscured by adjoining building and left lower vegetation are not mirrored or extrapolated.', 'Brick wall includes pale horizontal bands without matching original boundaries; no full red wall.', 'Central glazing mixes bright frames, dark spandrels and reflections; no full blue backing.', 'Gallery rail/slab proxy and deep backs not blanket black.', 'Round entry columns contain brick/gray transitions and obscured lower areas; no full-column color.', 'Window-head top/underside/returns, all rear cut surfaces, roof, support and unlisted triangles remain neutral.', 'Preserve3606 original faces; no geometry edits, new boundaries or OBJ creation.', 'Shallow front facade segment only; back is an arbitrary cut, not the actual rear elevation.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':3606,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],'components',len(cs))
