"""Complete original front80gon portico vertical facets only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='6c06b4ed10a90a649780285ea55c19c7fd71228265a56f868d780af6babc3bce';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==4064
t=m.triangles;n=m.face_normals;e=.0001;a=np.full(len(t),1,np.int32);D={}
selected=[]
for k in range(40,80):
 p=18*np.array([np.cos(2*np.pi*k/80),np.sin(2*np.pi*k/80)])+np.array([0,-10])
 q=18*np.array([np.cos(2*np.pi*(k+1)/80),np.sin(2*np.pi*(k+1)/80)])+np.array([0,-10])
 tangent=(q-p)/np.linalg.norm(q-p);normal=np.array([tangent[1],-tangent[0]])
 rel=t[:,:,:2]-p;dist=rel@normal;along=rel@tangent
 whole=np.flatnonzero(np.abs(dist).max(1)<e)
 finite=np.flatnonzero((np.abs(dist).max(1)<e)&(along.min(1)>=-e)&(along.max(1)<=np.linalg.norm(q-p)+e)&(t[:,:,2].min(1)>=27-e)&(t[:,:,2].max(1)<=29.8+e)&(t[:,:,1].max(1)<=-11+e))
 assert np.array_equal(whole,finite)
 assert len(whole)==(4 if k in [47,48,53,54,65,66,71,72] else 2)
 D['complete_front_chord_'+str(k)]=whole.tolist();selected.extend(whole.tolist())
assert len(set(selected))==96;a[selected]=0
ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999;cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1);assert all(len(set(a[c]))==1 for c in cs);assert np.bincount(a).tolist()==[96,3968]
pal=[('JUST Design L observed front portico fascia off white','#D5D6D0'),('UNVERIFIED main walls entrance windows roofs neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':D,'coplanar_components':len(cs),'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'4064 original triangles unchanged','limits':['Cap upper skin, underside, rear half and wall backing remain neutral.', 'Columns have foot/base transitions, bands and banner/fixture associations; no full column white.', 'Three true pitched roof pavilion volumes remain originalv3 geometry; gray roof evidence is not extended to unverified rear slopes in this limited review.', 'Low front gable/pediment plates are not roof slopes and are not expanded or recolored by analogy.', 'Main white walls include dark bases, stone lower wings, windows and fixtures without full material boundaries; no blanket white facade.', 'Window/glazing backing contains frames, interior and reflections; no blue/black fill.', 'Roof, steps, base, rear and all unlisted triangles remain neutral.', 'Preserve4064 original faces and allv3 roof/tower geometry; no face splitting, additive details or OBJ generation.', 'Nominal white-family partial only, not full-color or current-condition reconstruction.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':4064,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],'components',len(cs))
