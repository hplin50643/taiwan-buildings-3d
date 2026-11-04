"""6092 original triangles; two finite outer roof-edge fascia rectangles only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='7fa290233db6e22474ef2c8af0bee8d881b4dc5f8e7c01f8d6904afe947135b2';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==6092
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.ones(len(t),np.int32)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
def span(ax,l,h):return(lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
fields=[]
for y in [-65.8,65.8]:
 fields.append((np.max(abs(t[:,:,1]-y),1)<.0001)&(lo[:,0]>=-65.5-.0001)&(hi[:,0]<=65.5+.0001)&(lo[:,2]>=71.2-.0001)&(hi[:,2]<=72.7+.0001))
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
pal=[('Observed two outward roof edge vertical fascia mediumgray','#858985'),('UNVERIFIED mixedbrickwalls entryframes glazing roofplanes neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
domains={'outer_roof_edge_fascia':int((rail&(a==0)).sum()),'per_rectangle':[int(x.sum())for x in fields],'whole_coplanar_withdrawals':len(removed),'coplanar_domains':len(g)}
assert (a==0).sum()==4
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'6092 original triangles unchanged; no cuts or newgeometry','limitations':['All vertices on complete y+-65.8 finitefascia planes,x+-65.5,z71.2..72.7.','4faces2perrectangle;twonamedbuildingsONEgroup.','No normal or centroid shortcuts;horizontal roofs side returns neutral.','Entry lettering mixedbase mainbrickwalls andwindowbacks neutral.','2023formdate notphotocapture;captureunknown.','Two labels not testedfourfilament.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':6092,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(np.unique(a,return_counts=True),domains)
