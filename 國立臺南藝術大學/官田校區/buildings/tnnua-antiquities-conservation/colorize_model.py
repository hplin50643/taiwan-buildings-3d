"""1138 original triangles; finite leftminus4deg wall outward only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='ad048144fb69fc167db4e0e1bf1bee1f7d53eae6d8bbccc85007f17de101cb27';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==1138
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.ones(len(t),np.int32)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
def span(ax,l,h):return(lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
theta=np.deg2rad(4);xp=np.cos(theta)*t[:,:,0]-np.sin(theta)*t[:,:,1];yp=np.sin(theta)*t[:,:,0]+np.cos(theta)*t[:,:,1]
rail=(np.max(abs(yp+24.5),axis=1)<.0001)&(xp.min(1)>=-63-.0001)&(xp.max(1)<=-19+.0001)&span(2,3,54)
a[rail]=0;p=np.arange(len(a))
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
pal=[('Observed left rotated wall outward palegraywhite','#D4D5CF'),('UNVERIFIED centralfin mixedbase windows roofsides neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
domains={'left_rotated_full_outward_plane':int((rail&(a==0)).sum()),'whole_coplanar_withdrawals':len(removed),'coplanar_domains':len(g)}
assert (a==0).sum()==48
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'1138 original triangles unchanged; no cuts or newgeometry','limitations':['Only entire leftminus4degree originaloutward plane.','Centralfin acrossdarkbase neutral;no zthreshold white.','Slotsides/back/top roof rightwindows neutral.','Two builtphotos captureunknown;3Dperspective notcolorevidence.','Two labels not testedfourfilament.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':1138,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(np.unique(a,return_counts=True),domains)
