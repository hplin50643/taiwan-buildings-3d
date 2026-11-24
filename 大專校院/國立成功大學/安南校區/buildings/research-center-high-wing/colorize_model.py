"""Only original projecting frame front planes; no glazing inference or geometry edits."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
from shapely.geometry import Polygon,box
from shapely.ops import unary_union
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='099ed50f802897d56c62391375035da51dc66b10de6bfbed3ae64c1de0ebdb63';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==2340
t=m.triangles;n=m.face_normals;e=.003;a=np.full(len(t),1,np.int32)
pal=[('Observed projecting horizontal bands and vertical fins muted warm gray','#B7B2A9'),('UNVERIFIED glazing backings other walls roof rear neutral','#B8BAB5')]
def plane(k,v):return np.max(abs(t[:,:,k]-v),axis=1)<e
bandshape=unary_union([box(-65,z-1.2,59,z)for z in [17,27,37,47,57,67]]).buffer(e)
finshape=unary_union([box(x-1.1,3,x+1.1,69)for x in [-61,-25,17,56]]).buffer(e)
bands=[int(i)for i in np.flatnonzero(plane(1,-23.2)&(n[:,1]<-.999)) if bandshape.covers(Polygon(t[i][:,[0,2]]))]
fins=[int(i)for i in np.flatnonzero(plane(1,-22.5)&(n[:,1]<-.999)) if finshape.covers(Polygon(t[i][:,[0,2]]))]
a[bands+fins]=0
ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999
cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1);neutralized=[]
for c in cs:
 if len(set(a[c]))>1:neutralized+=c[a[c]!=1].tolist();a[c]=1
D={'six_band_front_planes':[i for i in bands if a[i]==0],'four_fin_front_planes':[i for i in fins if a[i]==0]};assert [len(v)for v in D.values()]==[12,56]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':D,'coplanar_components':len(cs),'coplanar_neutralized_faces':sorted(neutralized),'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'2340 original triangles unchanged','limits':['Exact original front planes and complete box union material domains, not stored face IDs.','Six band fronts y-23.2 and four fin fronts y-22.5 only.','All connected coplanar domains uniform.','Windows mix frames rails glass opaque inserts and reflections, remain neutral.','Higher wing only; no low wing, bridges or shared curved canopy.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':2340,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],{k:len(v)for k,v in D.items()},'neutralized',len(neutralized),'components',len(cs))
