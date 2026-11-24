"""Color actual original member fronts only, preserving all original triangles."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='f8a4030924c912a3b6e435b7f0b20790b822a290a7ea03b5c6dc87713b726453';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==1200
t=m.triangles;lo=t.min(1);hi=t.max(1);n=m.face_normals;a=np.full(len(t),2,np.int32);e=.003
pal=[('Existing six true horizontal mullion fronts warm offwhite','#D6D2C6'),('Existing entry stair treads and front risers muted stone','#A6A59A'),('UNVERIFIED mixed facade pane backs tile and red eave neutral','#B8BAB5')]
def plane(k,v):return np.max(abs(t[:,:,k]-v),axis=1)<e
def bound(x0,x1,y0,y1,z0,z1):return(lo[:,0]>=x0-e)&(hi[:,0]<=x1+e)&(lo[:,1]>=y0-e)&(hi[:,1]<=y1+e)&(lo[:,2]>=z0-e)&(hi[:,2]<=z1+e)
windows=[]
for x in [-10,0,10]:
 for z in [30,48]:
  mask=plane(1,8.45)&bound(x-3.5,x+3.5,8.45,8.45,z,z+1.1)&(n[:,1]<-.999);assert mask.sum()==2;a[mask]=0;windows.extend(np.flatnonzero(mask).tolist())
stairs=[]
for i in range(4):
 front=2.1+i*1.5;top=3.6+i*.65
 mask=bound(-14,14,front,front+1.8,2.8,top)&((plane(2,top)&(n[:,2]>.999))|(plane(1,front)&(n[:,1]<-.999)))
 a[mask]=1;stairs.extend(np.flatnonzero(mask).tolist())
assert len(windows)==12 and len(stairs)>0
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':{'six_mullion_fronts':windows,'four_step_treads_risers':sorted(set(stairs))},'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'1200 original triangles unchanged','limits':['Only12 actual mullion front triangles, no new fineframe or glass paint.','Step actual treads/front risers only; sidefaces and base neutral.','All mixed wall/columns, window backs, upperroof and redrafter-like thicklip neutral.','Three labels not a verified four-filament job.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':1200,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],q['domain_face_indices'])
