"""21356 original triangles; actual independent outward fin/column planes only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='23c39f3022dbfe62fd0731e22b4974995073c15e8040179acf5d4ebfe0f61f1c';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==21356
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.ones(len(t),np.int32)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
def span(ax,l,h):return(lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
fin=np.zeros(len(a),bool);col=fin.copy()
for side in [-1,1]:
 for i in range(41):
  x=-71+i*3.55;zmask=(span(2,2.4,10.3)|span(2,18.3,28.9))if abs(x)<43 else span(2,2.4,28.9)
  fin|=plane(1,side*10.35)&span(0,x-.5,x+.5)&zmask&(m.face_normals[:,1]*side>.99)
 for x in [-40,-30,-20,-10,10,20,30,40]:col|=plane(1,side*9.6)&span(0,x-.7,x+.7)&span(2,10,18.7)&(m.face_normals[:,1]*side>.99)
a[fin|col]=0;p=np.arange(len(a))
def root(i):
 while p[i]!=i:p[i]=p[p[i]];i=p[i]
 return i
for i,j in m.face_adjacency:
 if np.dot(m.face_normals[i],m.face_normals[j])>.999999:p[root(i)]=root(j)
g={}
for i in range(len(a)):g.setdefault(root(i),[]).append(i)
removed=[]
for ids in g.values():
 if len(set(a[ids]))>1:removed.extend(i for i in ids if a[i]==0);a[ids]=1
pal=[('Observed true outward concrete fin and terrace column planes','#C4C0B2'),('UNVERIFIED mixed horizontal bands windowbacks walls roof ends neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');domains={'fin_candidates':int(fin.sum()),'fin_actual_gray':int((fin&(a==0)).sum()),'column_candidates':int(col.sum()),'column_actual_gray':int((col&(a==0)).sum()),'whole_coplanar_withdrawals':len(removed)}
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'21356 original triangles unchanged; no cuts or added geometry','limitations':['Actual outward fin yplusminus10.35 andcolumn yplusminus9.6 planes independently matched, not raw review face indices.','All continuous horizontal mixed rail/slab bands,windowbacks,ends,roof and conference block neutral.','Low library pavilion excluded.','Photographer page visit years not image capture proof.','Two material labels not tested filament slicing.']},indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':21356,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(np.unique(a,return_counts=True),domains)
