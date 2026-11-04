"""Four original 48gon entrance shafts, complete front quarter facets only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='86fd4f37381c68e567d5c836d44dafa5bc2378bb05664480fee790693edd003f';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==11418
t=m.triangles;n=m.face_normals;e=.0001;a=np.full(len(t),1,np.int32);D={}
allids=[]
for cx in [-8,-5.8,5.8,8]:
 for k in range(30,42):
  ang=np.arange(k,k+2)*2*np.pi/48
  ends=np.column_stack((cx+.75*np.cos(ang),-24+.75*np.sin(ang)))*1.75
  tangent=ends[1]-ends[0];L=np.linalg.norm(tangent);tangent/=L;normal=np.array([-tangent[1],tangent[0]])
  delta=t[:,:,:2]-ends[0];dist=delta@normal;u=delta@tangent
  ids=np.flatnonzero((np.abs(dist).max(1)<1e-5)&(u.min(1)>=-1e-5)&(u.max(1)<=L+1e-5)&(t[:,:,2].min(1)>=6.125-1e-5)&(t[:,:,2].max(1)<=16.625+1e-5))
  assert len(ids)==2
  edges=m.face_adjacency;edges=edges[np.isin(edges[:,0],ids)&np.isin(edges[:,1],ids)]
  pcs=trimesh.graph.connected_components(edges,nodes=ids,min_len=1);assert len(pcs)==1
  D[f'column_{cx}_whole_facet_{k}']=ids.tolist();allids.extend(ids.tolist())
ids=np.unique(allids);assert len(ids)==96;a[ids]=0
ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999;cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1);assert all(len(set(a[c]))==1 for c in cs);assert np.bincount(a).tolist()==[96,11322]
pal=[('CTU Library Humanities 2002 observed four shaft front quarters nominal pink stone','#BBA09A'),('UNVERIFIED main walls entrance windows roofs neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':D,'coplanar_components':len(cs),'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'11418 original triangles unchanged','limits':['Remaining column shaft sides/rears, bases and capitals, no copying around cylinder.', 'Arch, entrance lintel and gable have dark trim/pale stone/lettering or emblem boundaries absent from original mesh; retain neutral.', 'Glazing contains frames/reflections; no blanket blue or black.', 'Whole exterior walls, terraces, tower roof, lanterns and central crown not additionally color-mapped here. Unknown rear surfaces remain neutral.', 'Original component/surface false values are retained, not converted to PASS by source review.', 'Four crown feet downward-control length only 1.4874984741mm, not required1.75; actual side connection is distinct evidence.', 'Original83 short first chords and independent215 short first chords remain. Twenty-four0.7424642782mm first chords followed by real0.0048272640mm air gap cannot be recast continuous roots.', '328 cross-layer high-loss samples are section counts, not328 structures. Limited rooted exceptions do not establish global minimum thickness.', 'Flattened corner lantern tips/crown sphere/gable print approximations and no physical print limitations remain.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':11418,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],'components',len(cs))
