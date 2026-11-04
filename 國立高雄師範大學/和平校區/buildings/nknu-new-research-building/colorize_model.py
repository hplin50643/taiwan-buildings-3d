"""8796 original triangles; entrance canopytop andtwo pillarfronts only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='6eec5d4549ee730f13ae66273ea4cbb4ee4d11a942d8dc7686fb931fe534a373';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==8796
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.ones(len(t),np.int32)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
def span(ax,l,h):return(lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
canopy=plane(2,30.2)&span(0,-20,34)&span(1,-66,-48)&(m.face_normals[:,2]>.99)
piers=plane(1,-65.55)&span(2,2.8,28.4)&(span(0,-17.25,-13.75)|span(0,18.75,22.25))&(m.face_normals[:,1]<-.99)
a[canopy]=0;a[piers]=2;p=np.arange(len(a))
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
pal=[('Observed entrance canopy actual top mediumgray','#888C88'),('UNVERIFIED fascia rails windowbacks body neutral','#B8BAB5'),('Observed two entrance pillar frontfaces warmoffwhite','#D7D5CC')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
domains={'canopy_top':int((canopy&(a==0)).sum()),'two_pier_fronts':int((piers&(a==2)).sum()),'whole_coplanar_withdrawals':len(removed)}
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'8796 original triangles unchanged; no cuts or newgeometry','limitations':['Canopy true upperplane only;fascia mixed dark/pale remainsneutral.','Two pillarfronts only;columnside/underside neutral.','Originalsolidparapets not colored black as pretendopenrails.','All windowbacks/mainwalls/roof andotherfaces neutral.','2020article/2026imagepath not capturedate;newbuilding not demolishedold.','Three materiallabels not verified fourfilament slicing.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':8796,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(np.unique(a,return_counts=True),domains)
