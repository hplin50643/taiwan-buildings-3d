"""Only two original long foreground solar-table top fields, not rear tables."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='f1abdfe63fc2154e42a209a786d7226b483d45f09af70ad14d283f9acb803210';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==11156
t=m.triangles;n=m.face_normals;lo=t.min(1);hi=t.max(1);e=.003;a=np.full(len(t),1,np.int32)
pal=[('Observed long foreground photovoltaic table top fields','#5D6C78'),('UNVERIFIED roofs rear tables walls glazing neutral','#B8BAB5')]
D={}
for x in [-61,61]:
 mask=(np.max(abs(t[:,:,2]-37.2),axis=1)<e)&(n[:,2]>.999)&(lo[:,0]>=x-6.1-e)&(hi[:,0]<=x+6.1+e)&(lo[:,1]>=-51.5-e)&(hi[:,1]<=1.5+e)
 ids=np.flatnonzero(mask).tolist();assert len(ids)==62;D[f'front_long_solar_top_x{x}']=ids;a[ids]=0
ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999;cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1)
assert all(len(set(a[c]))==1 for c in cs);assert np.bincount(a).tolist()==[124,11032]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':D,'coplanar_components':len(cs),'coplanar_neutralized_faces':[],'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'11156 original triangles unchanged','limits':['Two foreground long-table true top fields62+62, excluding grooves floors and sides.','Both short rear tables neutral; actual leftrear redroof/equipment cannot be cloned blue.','Whole connected coplanar domains uniform.','All walls/glazing/equipment/parapets/bridges/steps neutral. No extra solar cells or geometry.','Capture dates unknown;2014album date not necessarily capture; not2026condition.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':11156,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],'components',len(cs))
