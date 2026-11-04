"""Original museum 17290 triangles; front-domain color, no geometric release claim."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
from shapely.geometry import Polygon,box,Point
R=Path(__file__).resolve().parent;EXPECTED_STL='0130b50cd4b44752b86f935dec384faf6326cbacb5270759f5024cdc1614838a';assert hashlib.sha256((R/'model.stl').read_bytes()).hexdigest()==EXPECTED_STL
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==17290
pal=[('Observed front concrete supports soffits and fascia','#BABDB4'),('Observed original front and corner pane recess gray-green','#557974'),('Observed original narrow facade grid dark gray','#364744'),('Observed broad upper roof light gray','#CBCDC4'),('UNVERIFIED courtyard rear supports and model base','#B7B9B3')];a=np.full(len(m.faces),4,np.int32)
ROOF=Polygon([(-28.303,0),(.190,48.248),(28.303,0)]);RIM=Polygon([(-9.656,6.917),(.354,24.062),(10.547,6.495)])
MID=Polygon([(-29.8,8),(1.57,61),(32.17,7.81)]);GROUND=Polygon([(-32,5),(-1.5,57.82),(29,5)])
PIERS=[Polygon([(-25.7,.75),(-19,.75),(-11.2,14.25),(-17.9,14.25)]),Polygon([(19,.75),(25.7,.75),(17.9,14.25),(11.2,14.25)])]
ground=GROUND.buffer(-1.05,join_style=2).intersection(box(-100,-100,100,47.8));mid=MID.buffer(-1.05,join_style=2).intersection(box(-100,14.25,100,100));roof=ROOF.buffer(-.95,join_style=2)
# Regenerate only analytic domains of ORIGINAL cuts, never generate replacement geometry.
edges=[]
for poly,zlo,zhi,rows in [(ground,.28,4.65,5),(mid,5.15,10.70,6),(roof,11.28,16.38,6)]:
 co=list(poly.exterior.coords)[:-1];c=np.array([poly.representative_point().x,poly.representative_point().y])
 for p,q in zip(co,co[1:]+co[:1]):
  p=np.array(p);q=np.array(q);v=q-p;L=np.linalg.norm(v);tv=v/L;iv=np.array([-tv[1],tv[0]])
  if np.dot(c-(p+q)/2,iv)<0:iv=-iv
  front=iv[1]>.9;leftcorner=(iv[0]>.5 and min(p[1],q[1])<15)
  if not front and not leftcorner:continue
  n=max(1,round(L/3.4));dz=(zhi-zlo)/rows;panes=[]
  for j in range(n):
   # Only two near-front left edge bays, not a claim about the long unphotographed back edge.
   if not front:
    near_index=j if p[1]<q[1] else n-1-j
    if near_index>1:continue
   u=p+tv*(j*L/n+.18);w=p+tv*((j+1)*L/n-.18);pp=Polygon([u-iv*.04,w-iv*.04,w+iv*.1,u+iv*.1])
   if zhi<=11:
    pierlist=PIERS
    if zhi<=4.9:
     rp=np.array([-2.,51.8]);rq=np.array([1.6,58.]);vv=rq-rp;nn=np.array([-vv[1],vv[0]])/np.linalg.norm(vv)*.7;pierlist=PIERS+[Polygon([rp+nn,rq+nn,rq-nn,rp-nn])]
    if any(pp.intersects(pi.buffer(.2,join_style=2))for pi in pierlist):continue
   for k in range(rows):panes.append((j*L/n+.18,(j+1)*L/n-.18,zlo+k*dz+.13,zlo+(k+1)*dz-.13))
  edges.append((p,tv,iv,L,zlo,zhi,front,panes))
for i,(tw,norm)in enumerate(zip(m.triangles,m.face_normals)):
 t=tw.copy();t[:,:2]/=2.15;t[:,1]+=29;t[:,2]=(t[:,2]-3)/2.15;lo=t.min(0);hi=t.max(0);xy=t[:,:2];z=t[:,2]
 # Distinct front piers observed all around locally; no northern rear support extrapolation.
 if lo[2]>=-.025 and hi[2]<=11.045:
  for p in PIERS:
   if all(p.buffer(.003).covers(Point(v)) for v in xy):a[i]=0
 # Front outer slab fascia and soffit only; courtyard and unseen rear remain neutral.
 for poly,z0,z1 in [(GROUND,4.45,4.95),(MID,4.42,4.93),(MID,10.52,11.03),(ROOF,10.52,11.03),(ROOF,16.53,17)]:
  co=list(poly.exterior.coords)[:-1]
  for p,q in zip(co,co[1:]+co[:1]):
   p=np.array(p);q=np.array(q);v=q-p;L=np.linalg.norm(v);tv=v/L
   if abs(tv[1])>.02:continue
   iv=np.array([-tv[1],tv[0]]);c=np.array([poly.centroid.x,poly.centroid.y])
   if np.dot(c-(p+q)/2,iv)<0:iv=-iv
   dep=(xy-p)@iv
   if lo[2]>=z0-.003 and hi[2]<=z1+.003 and np.max(abs(dep))<.003:a[i]=0
 # Full exterior upper roof is observed aerially, excluding separate lightwell/rim surfaces.
 if np.max(abs(z-17))<.003 and norm[2]>.9 and Polygon(xy).intersection(RIM).area<1e-7:a[i]=3
 for p,tv,iv,L,zlo,zhi,front,panes in edges:
  along=(xy-p)@tv;dep=(xy-p)@iv
  bodylo,bodyhi=((-0.03,4.9) if zhi<5 else ((4.88,11.0) if zhi<11 else (10.98,16.58)))
  if front and lo[2]>=bodylo-.003 and hi[2]<=bodyhi+.003 and along.min()>=-.003 and along.max()<=L+.003 and dep.min()>=-.005 and dep.max()<=.181:a[i]=1 if dep.min()>=.095 else 2
  for u,v,z0,z1 in panes:
   if along.min()>=u-.003 and along.max()<=v+.003 and lo[2]>=z0-.003 and hi[2]<=z1+.003 and dep.min()>=-.005 and dep.max()<=.181:
    # All original pane cut back surfaces including shallow V incisions stay glass/shadow, not white beams.
    a[i]=1 if dep.min()>=.095 else 2
 # Actual courtyard walls/floor have no source material proof; do not extend roof/glass colors into it.
 if lo[2]>=10.5 and all(RIM.buffer(.005).covers(Point(v))for v in xy):a[i]=4
# Four original V-incision backs cross concrete-pier material domain; no verified glass there.
for fid in [15085,15088,15090,15093]:a[fid]=4
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'geometry_policy':'17290 original triangles and STL bytes unchanged','prior_independent_release_record':'完整原獨立放行紀錄未確認；色審不構成原幾何追認。','limits':['Front three-level facade and first two original near-front left-corner pane bays only.','Original V incisions same pane shadow, never a new white exterior exoskeleton.','Courtyard, rear/northern supports, unknown surfaces neutral.','Five material labels are not a verified multi-filament slicer project.']},ensure_ascii=False,indent=2)+'\n');q={'status':'PASS','original_STL_sha256':EXPECTED_STL,'triangles':len(m.faces),'materials_used':np.unique(a).tolist(),'color_mesh_sha256':hashlib.sha256((R/'color-mesh.npz').read_bytes()).hexdigest()};(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps(q,indent=2));print(q);print(np.unique(a,return_counts=True))
