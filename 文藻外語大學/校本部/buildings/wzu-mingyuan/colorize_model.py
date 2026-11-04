"""Assign existing complete face domains only; original geometry unchanged."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='2aff6817679e3f592f1a7b41bb388d85c61a72f63abca23558dfdcd28ad232cd';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==1488
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.ones(len(m.faces),np.int32);eps=.003
pal=[('Source-supported independent front pale warm gray members','#D4D0C5'),('UNVERIFIED brick tile mixed gables recesses and rear neutral','#B8BAB5')]
def plane(axis,value):return np.max(abs(t[:,:,axis]-value),axis=1)<eps
def bounds(x0,x1,y0,y1,z0,z1):return (lo[:,0]>=x0-eps)&(hi[:,0]<=x1+eps)&(lo[:,1]>=y0-eps)&(hi[:,1]<=y1+eps)&(lo[:,2]>=z0-eps)&(hi[:,2]<=z1+eps)
rails=[]
for x0,x1 in [(-44,-12),(12,44)]:
 mask=plane(1,-34.2)&bounds(x0,x1,-34.2,-34.2,20,22);assert mask.sum()==2;a[mask]=0;rails.extend(np.flatnonzero(mask).tolist())
mask=plane(1,-36)&bounds(-13,13,-36,-36,23,24.6);assert mask.sum()==2;a[mask]=0;band=np.flatnonzero(mask).tolist()
posts=[]
for x in [-41,-28,-15,15,28,41]:
 mask=bounds(x-.9,x+.9,-32.1,-29.9,3,19)
 mask &= plane(0,x-.9)|plane(0,x+.9)|plane(1,-32.1)|plane(1,-29.9)
 a[mask]=0;posts.extend(np.flatnonzero(mask).tolist())
assert len(posts)>0
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
q={'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'1488 original triangles unchanged','domain_face_indices':{'front_rails':rails,'front_band':band,'gallery_posts':posts},'limits':['Brick/tile and mixed gables unfinished; all entire mixed planes neutral.','No black gable triangles or invented white moon-window ring.','Original roof-ridge direction differs approximately from photographed facade; color review does not endorse original geometry.','Two material labels are not a verified four-filament slicer job.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':1488,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q)
