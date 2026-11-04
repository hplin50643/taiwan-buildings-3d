"""Whole original upper sunshade fronts and gallery column primitive fronts only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='4cb5bfdbde4b9d544e6944dc1e6a9b72bafb310e6df4bace43f63c6ae0037d42';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==6488
t=m.triangles;n=m.face_normals;lo=t.min(1);hi=t.max(1);e=.003;a=np.full(len(t),2,np.int32)
pal=[('Observed four sunshade front plates muted yellow','#C6AE51'),('Observed gallery column front faces pale warm gray','#CDC9BD'),('UNVERIFIED mixed glazing rails wall roof neutral','#B8BAB5')]
def plane(k,v):return np.max(abs(t[:,:,k]-v),axis=1)<e
D={}
for z in [78,87,96,105]:
 mask=plane(1,15.7)&(n[:,1]<-.999)&(lo[:,0]>=-57.5-e)&(hi[:,0]<=45.5+e)&(lo[:,2]>=z-.2-e)&(hi[:,2]<=z+1.15+e)
 ids=np.flatnonzero(mask).tolist();assert len(ids)==2;assert abs(m.area_faces[ids].sum()-86*1.35)<.02;D[f'yellow_sunshade_z{z}']=ids;a[ids]=0
for z in [16,26,36,46,56,66]:
 for x in [-50,-28,-6,16,38]:
  mask=plane(1,18.9)&(n[:,1]<-.999)&(lo[:,0]>=x-1.7-e)&(hi[:,0]<=x+1.7+e)&(lo[:,2]>=z-.3-e)&(hi[:,2]<=z+8.1+e)
  ids=np.flatnonzero(mask).tolist();assert len(ids)>=2;D[f'gray_column_x{x}_z{z}']=ids;a[ids]=1
ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999;cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1)
assert all(len(set(a[c]))==1 for c in cs);assert np.bincount(a).tolist()==[8,156,6324]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':D,'coplanar_components':len(cs),'coplanar_neutralized_faces':[],'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'6488 original triangles unchanged','limits':['Four complete sunshade fronts8yellow triangles. Thirty genuine column primitive front domains156gray triangles; never blanket y18.9.','Whole connected coplanar domains uniform.','Mixed glazing/rail substitutes/curved wing and unverified walls roofs remain neutral.','2012EXIF without timezone preserved as reported local timestamp; not2026current condition.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':6488,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],'components',len(cs))
