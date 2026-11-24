"""7136 original triangles; complete complete sloped gable coping component only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='0dae6d42035f5acbb51e19fc4fca8b7d64654c73d9870cd57ae5bdc62d35dd84';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==7136
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.ones(len(t),np.int32)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
def span(ax,l,h):return(lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
whole=np.max(abs(t[:,:,1]+25),1)<1e-5
ids=set(np.where(whole)[0]);adj={i:set()for i in ids}
for i,j in m.face_adjacency:
 if i in ids and j in ids:adj[i].add(j);adj[j].add(i)
cc=[]
while ids:
 seed=ids.pop();comp={seed};stack=[seed]
 while stack:
  for v in adj[stack.pop()]:
   if v in ids:ids.remove(v);comp.add(v);stack.append(v)
 cc.append(sorted(comp))
assert sorted(map(len,cc))==[4,6] and whole.sum()==10
chosen=[c for c in cc if t[c,:,2].min()>30]
assert len(chosen)==1 and len(chosen[0])==4
finite=np.zeros(len(t),bool);finite[chosen[0]]=True
xx=t[finite,:,0];zz=t[finite,:,2];bottom=44.8-abs(xx)*10.5/19.2;top=46.5-abs(xx)*10.5/19.2
assert (abs(xx)<=19.2+1e-5).all() and (zz>=bottom-1e-5).all() and (zz<=top+1e-5).all()
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
pal=[('NTCU Administration Central Section gable coping stone gray','#B5B2A7'),('NTCU Administration Central Section unverified walls windows neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
domains={'whole_sloped_gable_coping_component':int((rail&(a==0)).sum()),'per_rectangle':[int(x.sum())for x in fields],'whole_coplanar_withdrawals':len(removed),'coplanar_domains':len(g)}
assert (a==0).sum()==4
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'7136 original triangles unchanged; no cuts or newgeometry','limitations':['4 complete original sloped gable coping front triangles stone gray.','Whole y-25 plane has10 triangles, BFS6 model support neutral plus4 complete coping approved.','Finite original two-arm profile all3vertices; no rectangular color clipping.','72-face connected arch trim and mixed jambs, lettering, windows and walls remain neutral.','Flat upper and rear cuts are not actual roofs; remain neutral.','Central entrance section only not entire U-shaped building;capture unknown.','Original model.obj verified present and preserved unchanged; not newly generated.','Two labels not verified filament slicing.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':7136,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(np.unique(a,return_counts=True),domains)
