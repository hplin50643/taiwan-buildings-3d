"""1776 original triangles; three finite frontroofplanes only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='ddd66a9579305c15176149b711ee221a5ee0d6a5dd897e8bc139c1adb2140a8b';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==1776
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.ones(len(t),np.int32)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
def span(ax,l,h):return(lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
roof_fields=[]
for slope,intercept,x0,x1,y0,y1 in [(1/3,38,-62,4,-12,18),(17/31,37.96774193548387,4,62,-20,11),(.25,40,-14.5,8.5,0,24)]:
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
pal=[('Observed three lakefacing roof pitches nominalterracotta','#AD624F'),('UNVERIFIED rearpitches gables whiteeaves mixedwindowscolumns neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
domains={'three_front_roof_pitches':int((rail&(a==0)).sum()),'original_plane_counts':[int(x.sum())for x in roof_fields],'whole_coplanar_withdrawals':len(removed),'coplanar_domains':len(g)}
assert (a==0).sum()==39
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'1776 original triangles unchanged; no cuts or newgeometry','limitations':['Three finite front pitches7/20/12 include allbooleantrimmed triangles.','No normal or centroid shortcuts;rear slopes gables eaves dormercap neutral.','Mixedwindowbacks columns andlowerwalls neutral.','Two lakesidephotos captureunknown;no currentconditionclaim.','Two labels not testedfourfilament.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':1776,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(np.unique(a,return_counts=True),domains)
