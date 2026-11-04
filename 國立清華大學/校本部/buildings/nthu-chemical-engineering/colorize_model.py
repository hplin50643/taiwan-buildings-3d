"""Original independent trim surfaces only; no segmentation or geometry changes."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='41e8564cf83b71f554aa716cfd5ae1992bbc522e7443b0ba5a81aaa0102e952a';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==2924
t=m.triangles;n=m.face_normals;lo=t.min(1);hi=t.max(1);e=.003;a=np.full(len(t),1,np.int32)
pal=[('Observed pre-renovation independent front and right pale trim','#D3D0C5'),('UNVERIFIED mixed pink walls glazing stairs roof neutral','#B8BAB5')]
def plane(k,v):return np.max(abs(t[:,:,k]-v),axis=1)<e
D={}
for z in [15,26,37,48,59,70,81,87]:
 for x0,x1 in [(-56,-24),(24,56)]:
  mask=plane(1,-29.55)&(n[:,1]<-.999)&(lo[:,0]>=x0-e)&(hi[:,0]<=x1+e)&(lo[:,2]>=z-e)&(hi[:,2]<=z+.9+e)
  ids=np.flatnonzero(mask).tolist();assert len(ids)>=2
  assert abs(m.area_faces[ids].sum()-32*.9)<.01
  D[f'front_x{x0}_z{z}']=ids;a[ids]=0
 mask=plane(0,56.55)&(n[:,0]>.999)&(lo[:,1]>=-29-e)&(hi[:,1]<=39+e)&(lo[:,2]>=z-e)&(hi[:,2]<=z+.9+e)
 ids=np.flatnonzero(mask).tolist();assert len(ids)==2;assert abs(m.area_faces[ids].sum()-68*.9)<.01
 D[f'right_z{z}']=ids;a[ids]=0
ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999;cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1)
assert all(len(set(a[c]))==1 for c in cs);assert int((a==0).sum())==50
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':D,'coplanar_components':len(cs),'whole_trim_members':24,'coplanar_neutralized_faces':[],'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'2924 original triangles unchanged','limits':['16 front and8 right whole original trim planes; fronts34 and right16 triangles.','Whole connected coplanar domains uniform.','Mixed pink walls, gable caps, center spine, columns, all glazing, stairs and roof neutral.','Pre-renovation historic public-photo approximation; not2026 renovated condition or completion evidence.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':2924,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],'components',len(cs))
