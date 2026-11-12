"""Bounded original face domains; no new geometry or arbitrary wall color cuts."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
from shapely.geometry import Polygon,LineString,Point
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='1401a0086b52e77230373c2d3372ef387d91c6ffe3c556a834ac6c744d3bf90e';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==13806
t=m.triangles;n=m.face_normals;lo=t.min(1);hi=t.max(1);e=.003;a=np.full(len(t),2,np.int32)
pal=[('Observed enclosed court cells muted green','#538369'),('Observed separate rim belts and stairs pale gray','#B8BBB3'),('UNVERIFIED curved walls windows equipment and rear neutral','#B8BAB5')]
ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999
cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1)
def plane(k,v):return np.max(abs(t[:,:,k]-v),axis=1)<e
court=[];cellrecords=[]
for c in cs:
 if plane(2,68.8)[c].all() and (n[c,2]>.999).all():
  pts=t[c].reshape(-1,3);mn=pts.min(0);mx=pts.max(0)
  if mn[0]>=-33.65-e and mx[0]<=28.65+e and mn[1]>=-23.65-e and mx[1]<=23.65+e:
   edges=m.edges_sorted.reshape(-1,3,2)[c].reshape(-1,2);u,cnt=np.unique(edges,axis=0,return_counts=True);boundary=u[cnt==1];vv,degree=np.unique(boundary,return_counts=True);assert (degree==2).all()
   court.extend(c.tolist());cellrecords.append({'faces':c.tolist(),'bounds':[mn.tolist(),mx.tolist()],'boundary_closed':True,'area':float(m.area_faces[c].sum())})
a[court]=0;assert len(cellrecords)>1
ang=np.arange(144)*2*np.pi/144
def ring(rx,ry,ix,iy,z,h,front=False):
 outer=np.column_stack((rx*np.cos(ang),ry*np.sin(ang)));inner=np.column_stack((ix*np.cos(ang),iy*np.sin(ang)));ann=Polygon(outer,[inner[::-1]]).buffer(.002)
 ids=[]
 for i in np.flatnonzero((lo[:,2]>=z-e)&(hi[:,2]<=z+h+e)):
  if front and hi[i,1]>e:continue
  q=t[i,:,:2];ok=False
  if abs(n[i,2])>.999 and (plane(2,z)[i] or plane(2,z+h)[i]):ok=ann.covers(Polygon(q))
  elif abs(n[i,2])<.001:
   for poly in [outer,inner]:
    for k in range(144):
     p0=poly[k];p1=poly[(k+1)%144];d=p1-p0;L=np.linalg.norm(d);cross=np.abs(np.cross(d,q-p0))/L;proj=(q-p0)@d/(L*L)
     if max(cross)<e and min(proj)>-e and max(proj)<1+e:ok=True;break
    if ok:break
  if ok:ids.append(int(i))
 return ids
rim=ring(65,39,61.8,35.8,80,2);a[rim]=1
belts=[]
for z in [19,40,63]:belts+=ring(65.8,39.8,63,37,z,1.7,True)
a[belts]=1
stairs=[]
for j in range(5):
 y=-49+1.8*j;top=3.6+.8*j
 ids=np.flatnonzero((lo[:,0]>=-13.5-e)&(hi[:,0]<=13.5+e)&(lo[:,1]>=y-1.05-e)&(hi[:,1]<=y+1.05+e)&(lo[:,2]>=2.8-e)&(hi[:,2]<=top+e)&((plane(2,top)&(n[:,2]>.999))|(plane(1,y-1.05)&(n[:,1]<-.999))))
 stairs+=ids.tolist()
a[stairs]=1
# Continuous coplanar source domains must never acquire arbitrary half-face color boundaries.
neutralized=[]
for c in cs:
 if len(set(a[c]))>1:neutralized+=c[a[c]!=2].tolist();a[c]=2
D={'closed_court_cells':[i for i in court if a[i]==0],'upper_rim':[i for i in rim if a[i]==1],'front_belts':[i for i in belts if a[i]==1],'stair_tread_riser':[i for i in stairs if a[i]==1]}
assert all(len(v)>0 for v in D.values())
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':D,'court_components':cellrecords,'coplanar_components':len(cs),'coplanar_neutralized_faces':sorted(neutralized),'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'13806 original triangles unchanged','limits':['Court only original enclosed top cells; groove sides and floors not painted white.','Rim/belts matched actual 144-segment annulus surface, not boxes or height ranges.','Entire connected coplanar mixed-coverage regions neutral; front scope is evidence coverage, not actual finish boundary.','Curved main walls, windows, supports and equipment remain neutral.']}
(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':13806,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],{k:len(v)for k,v in D.items()},'cells',len(cellrecords),'neutralized',len(neutralized))
