"""Original triangle material assignment only. Source-supported front domains; no geometry edits."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib,math
R=Path(__file__).resolve().parent;expected='774d6599a3b721d55dd10b76ada762ed953373568b3fc389680c9356881b2955';assert hashlib.sha256((R/'model.stl').read_bytes()).hexdigest()==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==20662
t=m.triangles;lo=t.min(1);hi=t.max(1);norm=m.face_normals
pal=[('Photographed front shell and cap warm light gray','#B9B5A9'),('Three original front door backing surfaces muted red','#A62C32'),('Actual front stair treads and risers gray','#A6A7A2'),('UNVERIFIED rear shell walls lattice and base neutral','#B8BAB5')];a=np.full(len(m.faces),3,np.int32)
# Reproduce only original upper roof reference surface (not a new model or remesh).
N=560;radii=[.01,19,25,35,45,55,65];v=[]
for r in radii:
 for j in range(N):
  ang=2*math.pi*j/N;u=max(0,(r-19)/46);z=41-13*(u**.8)+2*abs(math.sin(35*ang))*u;v.append((r*math.cos(ang),6+r*math.sin(ang),z))
f=[]
for k in range(len(radii)-1):
 for j in range(280,560):
  q=(j+1)%N;b=k*N+j;c=k*N+q;d=(k+1)*N+j;e=(k+1)*N+q;f.extend([(b,d,e),(b,e,c)])
ref=trimesh.Trimesh(np.array(v),np.array(f),process=False)
def match(ref):
 good=np.zeros(len(m.vertices),bool);ids=np.flatnonzero((m.vertices[:,1]<=6.005)&(m.vertices[:,2]>=27.995))
 for k in range(0,len(ids),1000):
  ix=ids[k:k+1000];_,di,_=trimesh.proximity.closest_point(ref,m.vertices[ix]);good[ix]=di<.006
 ix=np.flatnonzero(good[m.faces].all(1)&(hi[:,1]<=6.005));ans=[]
 for k in range(0,len(ix),1000):
  ii=ix[k:k+1000];_,di,fi=trimesh.proximity.closest_point(ref,m.triangles_center[ii]);keep=(di<.006)&((norm[ii]*ref.face_normals[fi]).sum(1)>.99);ans.extend(ii[keep])
 return np.array(ans,dtype=int)
roof=match(ref);a[roof]=0
# Original cone surface from exact sampled ring vertices; front half only.
v=[]
for rad,z in [(21.6,45),(.5,48.5)]:
 for j in range(140):v.append((rad*math.cos(2*math.pi*j/140),6+rad*math.sin(2*math.pi*j/140),z))
f=[]
for j in range(70,140):
 q=(j+1)%140;f.extend([(j,q,140+q),(j,140+q,140+j)])
ref=trimesh.Trimesh(v,f,process=False);ref.invert() if ref.face_normals[:,2].mean()<0 else None
cap=match(ref);a[cap]=0
# Only the actual backed planes, not red jambs, soffits or fabricated trim.
for x in [-18,0,18]:
 mask=(np.max(abs(t[:,:,1]+49.6),axis=1)<.003)&(lo[:,0]>=x-4.503)&(hi[:,0]<=x+4.503)&(lo[:,2]>=11.997)&(hi[:,2]<=22.503)&(norm[:,1]<-.99);assert mask.sum()==25,(x,mask.sum());a[mask]=1
# Whole original top/riser planes on ten stair boxes. Side faces remain neutral.
for i in range(10):
 top=3.7+i*.85;front=-73.35+i*2.3
 mask=(lo[:,0]>=-41.503)&(hi[:,0]<=41.503)&(lo[:,1]>=front-.003)&(hi[:,1]<=front+2.703)&(lo[:,2]>=2.797)&(hi[:,2]<=top+.003)
 mask &= ((np.max(abs(t[:,:,2]-top),axis=1)<.003)&(norm[:,2]>.99))|((np.max(abs(t[:,:,1]-front),axis=1)<.003)&(norm[:,1]<-.99))
 a[mask]=2
assert (a==1).sum()==75
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
q={'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'20662 original triangles unchanged','roof_reference_faces_matched':len(roof),'cap_reference_faces_matched':len(cap),'limits':['Only photographed front shell hemisphere/cap gray, unknown rear neutral; coverage boundary is not a real material seam.','Door red limited to 75 original backing triangles. Original middle arch differs from photographed rectangle, geometry not changed.','No dark paint in unseen lattice or black valley stripes.','Four material labels are not a verified four-filament slicer job.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':20662,'color_mesh_sha256':hashlib.sha256((R/'color-mesh.npz').read_bytes()).hexdigest()},indent=2));print(q,flush=True)
