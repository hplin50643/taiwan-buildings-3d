"""2150 original triangles; one whole finite short end vertical roof fascia only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='968dfdd9cbbe8b96268f737ae5cda3cc66ff890f8eeccb83d54a3723cd5fa8b8';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==2150
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.ones(len(t),np.int32)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
def span(ax,l,h):return(lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
fields=[(np.max(abs(t[:,:,0]+71),1)<.0001)&(lo[:,1]>=-16-.0001)&(hi[:,1]<=16+.0001)&(lo[:,2]>=34-.0001)&(hi[:,2]<=35.6+.0001)]
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
pal=[('Observed short end roof fascia mediumgray','#858983'),('UNVERIFIED mixedbrickwalls entryframes glazing roofplanes neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
domains={'short_end_roof_fascia':int((rail&(a==0)).sum()),'per_rectangle':[int(x.sum())for x in fields],'whole_coplanar_withdrawals':len(removed),'coplanar_domains':len(g)}
assert (a==0).sum()==2
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'2150 original triangles unchanged; no cuts or newgeometry','limitations':['All vertices on complete shortend fascia x-71,y+-16,z34..35.6.','2faces oneoriginal shortend vertical fascia rectangle.','No normal or centroid shortcuts;horizontal roofs side returns neutral.','Mixedbasewalls longobscuredelevations windows bands neutral.','Captureunknown;2022waterproofingnote not roofcolor orcaptureproof.','Two labels not testedfourfilament.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':2150,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(np.unique(a,return_counts=True),domains)
