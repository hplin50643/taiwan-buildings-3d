"""1694 original triangles; one complete upper roof front fascia rectangle only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='0afbbd065257870eddfee328bb13a17af62567428583b7b1cc389cede2857476';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==1694
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.ones(len(t),np.int32)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
def span(ax,l,h):return(lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
whole=np.max(abs(t[:,:,1]+22),1)<1e-5
finite=whole&(t[:,:,0].min(1)>=-66.5-1e-5)&(t[:,:,0].max(1)<=-19.5+1e-5)&(t[:,:,2].min(1)>=27-1e-5)&(t[:,:,2].max(1)<=28.2+1e-5)
assert np.array_equal(whole,finite)
fields=[finite]
rail=np.logical_or.reduce(fields)
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
pal=[('Observed low hall upper roof front fascia gray','#A5A7A2'),('UNVERIFIED plantedroof supports walls windows neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
domains={'one_complete_upper_front_fascia':int((rail&(a==0)).sum()),'per_rectangle':[int(x.sum())for x in fields],'whole_coplanar_withdrawals':len(removed),'coplanar_domains':len(g)}
assert (a==0).sum()==2
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'1694 original triangles unchanged; no cuts or newgeometry','limitations':['One complete original roofedge vertical front47x1.2 rectangle;2triangles.','All3vertices finiteplane; entire infiniteplane equalsfinite rectangle.','Allroofskins,sides,undersides,plantedroof,Ysupports,windows andwalls neutral.','Singleexterior group,not allcampus sportsbuildings;nointeriors.','Captureunknown;twilight onlystructure notexactcolor.','Two labels not verifiedfilament slicing.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':1694,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(np.unique(a,return_counts=True),domains)
