"""2048 original triangles, only existing tower/stone entry faces; partial."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;expected='3cfcf3b3db5c7d78883722a34345081afa66ed8c87b2cdcf1b99c655e307dc14';assert hashlib.sha256((R/'model.stl').read_bytes()).hexdigest()==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==2048
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.full(len(t),1,np.int32)
def span(ax,l,h):return (lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
def box(x0,x1,y0,y1,z0,z1):return span(0,x0,x1)&span(1,y0,y1)&span(2,z0,z1)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
front=plane(1,-29)&box(-33,-15,-29,-29,2.8,104.8)&(m.face_normals[:,1]<-.99)
ret=plane(0,-15)&box(-15,-15,-29,-19,2.8,104.8)&(m.face_normals[:,0]>.99)
reveal=np.zeros(len(t),bool)
for z in [15,37,59,81]:
 radius=np.sqrt((t[:,:,0]+24)**2+(t[:,:,2]-z)**2)
 reveal|=(np.max(abs(radius-4.4),axis=1)<.003)&span(1,-29,-26.7)&(abs(m.face_normals[:,1])<.01)
header=plane(1,-25)&box(-13.5,25.5,-25,-25,22,25)&(m.face_normals[:,1]<-.99)
steps=np.zeros(len(t),bool)
for i in range(5):
 y=-36+i*2;z=3.8+i*1.3;b=box(-3,19,y-1.15,y+1.15,2.8,z)
 steps|=b&((plane(2,z)&(m.face_normals[:,2]>.99))|(plane(1,y-1.15)&(m.face_normals[:,1]<-.99)))
assert front.sum()==202 and reveal.sum()==384 and header.sum()==2
sel=front|ret|reveal|header|steps;a[sel]=0
parent=np.arange(len(a))
def root(i):
 while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
 return i
for i,j in m.face_adjacency:
 if np.dot(m.face_normals[i],m.face_normals[j])>.999999:parent[root(i)]=root(j)
g={}
for i in range(len(a)):g.setdefault(root(i),[]).append(i)
withdrawn=[]
for ids in g.values():
 if len(set(a[ids]))>1:withdrawn.extend(i for i in ids if a[i]==0);a[ids]=1
pal=[('Observed tower front circular reveals and entry stone warmgray','#BDB7A4'),('UNVERIFIED mixed mainwall windowbacks roof rear neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'2048 original triangles unchanged; no new or split faces','domains':{'tower_front':int(front.sum()),'right_return_candidate_faces':int(ret.sum()),'right_return_actual_colored_faces':int((ret&(a==0)).sum()),'circle_reveals':int(reveal.sum()),'header_front':int(header.sum()),'step_tread_risers':int(steps.sum()),'withdrawn_mixed_coplanar_candidates':len(withdrawn)},'limitations':['Towerfront/reveals and entry only; rightreturn candidate2 withdrawn to actual0 due continuous coplanar unknown rear. Circle and ordinary window backing disks neutral.','Mainfront spans stone and lowerbrick/louver; complete mixed wall plane neutral.','Photo dates unknown;2023 form and2025 PDF edition not capture dates.','Two material labels not a verified multi-filament slicing job.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':2048,'original_STL_sha256':expected,'color_mesh_sha256':hashlib.sha256((R/'color-mesh.npz').read_bytes()).hexdigest()},indent=2));print(np.unique(a,return_counts=True));print(int(ret.sum()),int(steps.sum()),len(withdrawn))
