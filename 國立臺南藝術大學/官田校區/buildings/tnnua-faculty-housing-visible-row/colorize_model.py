"""1650 original triangles; five finite frontroofplanes only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='78d0dc70d98162529015604406d4c615fe144ee7ebe6bc1868ba8ed3e91ba8b0';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==1650
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.ones(len(t),np.int32)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
def span(ax,l,h):return(lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
roof_fields=[]
for slope,intercept,x0,x1,y0,y1 in [(5/18,43.5,-65.5,-38.5,-9,9),(5/18,44.083333333333336,-39.5,-12.5,-7.5,10.5),(5/18,43.5,-13.5,13.5,-9,9),(5/18,45.916666666666664,12.5,39.5,-10.5,7.5),(5/18,44.5,38.5,65.5,-9,9)]:
 roof_fields.append((np.max(abs(t[:,:,2]-slope*t[:,:,1]-intercept),1)<.0001)&span(0,x0,x1)&span(1,y0,y1))
rail=np.logical_or.reduce(roof_fields)
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
pal=[('Observed five visible row front roof pitches nominalterracotta','#AD624F'),('UNVERIFIED rearpitches gables whiteeaves mixedwindowscolumns neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
domains={'five_front_roof_module_pitches':int((rail&(a==0)).sum()),'original_plane_counts':[int(x.sum())for x in roof_fields],'whole_coplanar_withdrawals':len(removed),'coplanar_domains':len(g)}
assert (a==0).sum()==20
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'1650 original triangles unchanged; no cuts or newgeometry','limitations':['Five finite front pitches4/2/10/2/2 include allbooleantrimmed triangles.','No normal or centroid shortcuts;rear slopes gables eaves raisedprojections neutral.','Mixedwindowbacks columns andlowerwalls neutral.','Two visible rowphotos captureunknown;no currentconditionclaim.','Two labels not testedfourfilament.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':1650,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(np.unique(a,return_counts=True),domains)
