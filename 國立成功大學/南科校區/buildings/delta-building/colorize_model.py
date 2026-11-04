"""1378 original triangles; roofbox front and independent canopy fascia only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='d8f0539a785192bc10a8c346b59869c6be984a6e95d54d0cfe144a99bfe1ac52';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==1378
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.full(len(t),2,np.int32)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
def span(ax,l,h):return(lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
roofbox=plane(1,1.5)&span(0,-36,-18)&span(2,67.9,75)&(m.face_normals[:,1]<-.99)
fascia=plane(1,-48.5)&span(0,36,60)&span(2,14.5,16)&(m.face_normals[:,1]<-.99)
a[roofbox]=0;a[fascia]=1;p=np.arange(len(a))
def root(i):
 while p[i]!=i:p[i]=p[p[i]];i=p[i]
 return i
for i,j in m.face_adjacency:
 if np.dot(m.face_normals[i],m.face_normals[j])>.999999:p[root(i)]=root(j)
g={}
for i in range(len(a)):g.setdefault(root(i),[]).append(i)
removed=[]
for ids in g.values():
 if len(set(a[ids]))>1:removed.extend(i for i in ids if a[i]!=2);a[ids]=2
pal=[('Observed raisedroof box front offwhite','#D8D4C9'),('Observed canopy front fascia pale stone gray','#C4C0B2'),('UNVERIFIED mixed fullheight walls glazing sides roofs neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');domains={'roofbox_front_offwhite':int((roofbox&(a==0)).sum()),'canopy_frontfascia_gray':int((fascia&(a==1)).sum()),'whole_coplanar_withdrawals':len(removed)}
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'1378 original triangles unchanged; no cuts or addedgeometry','limitations':['Roofbox front only, no roof/back/slit backing.','Whole fullheight white upper/gray stonebase mixed walls neutral, no heightmasked triangles.','Entrybody/posts neutral, canopy front vertical only.','Foundation page dates2015reported not independently authenticated.','Three material labels not tested filament slicing.']},indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':1378,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(np.unique(a,return_counts=True),domains)
