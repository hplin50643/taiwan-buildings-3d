"""5330 original triangles; complete original upper curved gate outer fascia only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='bbc2dde32fdf1acff429b99dcac55e937e42ad022e6753595571d6498c4a91c5';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==5330
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.ones(len(t),np.int32)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
def span(ax,l,h):return(lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
ctrl=np.array([(970,500),(990,645),(880,673),(750,710)],float)
u=np.linspace(0,1,33)
px=np.array([(1-v)**3*ctrl[0]+3*(1-v)**2*v*ctrl[1]+3*(1-v)*v*v*ctrl[2]+v**3*ctrl[3]for v in u])
xy=lambda p:np.column_stack(((p[:,0]-1000)*.1375,(800-p[:,1])*.1375))
roof=np.vstack((xy(np.array([(750,710),(860,1070),(1240,820)],float)),xy(px[:-1])))
gate=xy(np.array([(956,510),(971,500),(1002,537),(987,549)],float))
mins=np.min(np.vstack((roof,gate)),axis=0)-2;maxs=np.max(np.vstack((roof,gate)),axis=0)+2
scale=150/max(maxs-mins);curve=xy(px)*scale;fields=[]
for k in range(32):
 A=curve[k];B=curve[k+1];e=B-A;L=np.linalg.norm(e);u=e/L;n=np.array([-u[1],u[0]])
 off=t[:,:,:2]-A;along=off@u;whole=np.max(abs(off@n),axis=1)<1e-5
 wA=.8*np.clip((A[1]/scale-20)/17,0,1);wB=.8*np.clip((B[1]/scale-20)/17,0,1)
 low=(40.4+1.2+wA+(wB-wA)*along/L)*scale;high=low+1.8*scale
 finite=whole&np.all((along>=-1e-5)&(along<=L+1e-5)&(t[:,:,2]>=low-1e-5)&(t[:,:,2]<=high+1e-5),axis=1)
 assert whole.sum()==(0 if k<2 else 2) and np.array_equal(whole,finite),(k,whole.sum(),finite.sum())
 fields.append(finite)
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
pal=[('STUST Living Services Gate 2016 upper curved gate outer fascia pale gray','#CBCBC5'),('STUST Living Services Gate 2016 unverified walls windows neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
domains={'complete_curved_gate_outer_fascia':int((rail&(a==0)).sum()),'per_rectangle':[int(x.sum())for x in fields],'whole_coplanar_withdrawals':len(removed),'coplanar_domains':len(g)}
assert (a==0).sum()==60
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'5330 original triangles unchanged; no cuts or newgeometry','limitations':['60 complete original curved-gate outer fascia triangles palegray;5270 neutral.','Original3material preview and designated homepage representative retained unchanged,not monochrome discovery.','Original6posts150corner-loss samples,max2.893369991percent and1163globalshortchords/v1HOLD/v2limitedexceptions retained without global printability endorsement.','Original homepage36.87deg/23.43deg image remains primary;newtenviews are additional material QA only.','Architect2016/project andURL2021/12 not independently authenticated capture or2026 survey;photos nearly same direction not opposing proof.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':5330,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(np.unique(a,return_counts=True),domains)
