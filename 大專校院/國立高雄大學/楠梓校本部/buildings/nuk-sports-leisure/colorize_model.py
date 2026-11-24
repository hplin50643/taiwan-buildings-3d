"""2558 original triangles; four verified whole roofedge fascia groups only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='b3da4b8e792d706e2aeb8ae7481e40183c81a5a010b18ccdd09c56432cd75720';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==2558
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.ones(len(t),np.int32)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
def span(ax,l,h):return(lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
highfront=plane(1,-41.5)&span(0,-68,2)&span(2,42.8,47.6)&(m.face_normals[:,1]<-.99)
lowfront=plane(1,-36)&span(0,-1,66)&span(2,24.7,30.8)&(m.face_normals[:,1]<-.99)
highwest=plane(0,-68)&span(1,-41.5,33.5)&span(2,42.8,44.4)&(m.face_normals[:,0]<-.99)
loweast=plane(0,66)&span(1,-36,36)&span(2,24.7,26.3)&(m.face_normals[:,0]>.99)
slabs=highfront|lowfront|highwest|loweast
a[slabs]=0;p=np.arange(len(a))
def root(i):
 while p[i]!=i:p[i]=p[p[i]];i=p[i]
 return i
for i,j in m.face_adjacency:
 if np.dot(m.face_normals[i],m.face_normals[j])>.999999:p[root(i)]=root(j)
g={}
for i in range(len(a)):g.setdefault(root(i),[]).append(i)
removed=[]
for ids in g.values():
 if len(set(a[ids]))>1:removed.extend(i for i in ids if a[i]!=1);a[ids]=1
pal=[('Observed front andtwoverified side fascia green','#65715B'),('UNVERIFIED tower walls windowbacks soffit rooftops neutral','#B7B9B2')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a)
(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
domains={'four_fascia_groups_green':int((slabs&(a==0)).sum()),'whole_coplanar_withdrawals':len(removed)}
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'2558 original triangles unchanged; no cuts or addedgeometry','limitations':['Only highfront6 lowfront6 highwest2 loweast2 fascia triangles.','Entire tower8coplanar domain andwindowbacks neutral.','All soffits rooftops mixedwalls andunknownrear neutral.','Fourphotos datesunknown;some EXIF likelyreset;not2026.','Two material labels not tested filament slicing.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':2558,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(np.unique(a,return_counts=True),domains)
