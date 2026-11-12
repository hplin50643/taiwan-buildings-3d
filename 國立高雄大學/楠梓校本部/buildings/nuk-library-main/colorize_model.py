"""True elevated screen outer fields and bounded vertical sides of three front piers."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='75adb22859253404b84620cb1960576f44b3b89b9a7bd100809056341755c94a';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==12596
t=m.triangles;n=m.face_normals;lo=t.min(1);hi=t.max(1);e=.003;a=np.full(len(t),1,np.int32)
pal=[('Observed front reverse screen pale fields and front pier vertical sides','#D1C7B3'),('UNVERIFIED mixed walls glazing roof grooves neutral','#B8BAB5')]
def plane(k,v):return np.max(abs(t[:,:,k]-v),axis=1)<e
D={}
for side,count in [(-1,125),(1,127)]:
 mask=plane(1,side*43.75)&(n[:,1]*side>.999)&(lo[:,0]>=-31.75-e)&(hi[:,0]<=5.75+e)&(lo[:,2]>=24-e)&(hi[:,2]<=42.5+e)
 ids=np.flatnonzero(mask).tolist();assert len(ids)==count;D[f'outer_screen_side{side}']=ids;a[ids]=0
for x in [-25,-13,-1]:
 mask=plane(1,-43.3)&(n[:,1]<-.999)&(lo[:,0]>=x-1.1-e)&(hi[:,0]<=x+1.1+e)&(lo[:,2]>=10.7-e)&(hi[:,2]<=25.2+e)
 ids=np.flatnonzero(mask).tolist();assert len(ids)==2;D[f'front_pier_x{x}']=ids;a[ids]=0

# Original pier box vertical boundaries, all vertices finite; no caps.
selected=np.zeros(len(t),bool);eps=2e-5;domains={}
for x in [-25,-13,-1]:
 lower=np.array([x-1.1,-43.3,10.7]);upper=np.array([x+1.1,-40.7,25.2])
 bound=np.all((t>=lower-eps)&(t<=upper+eps),axis=(1,2));side=np.zeros(len(t),bool)
 for k in [0,1]:
  for v in [lower[k],upper[k]]:side|=np.all(abs(t[:,:,k]-v)<eps,axis=1)
 hit=bound&side;assert hit.sum()==14;selected|=hit;domains[str(x)]=np.flatnonzero(hit).tolist()
assert np.sum(selected&(a==1))==36;a[selected]=0;D['front_pier_vertical_sides']=domains

ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999;cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1)
assert all(len(set(a[c]))==1 for c in cs);assert np.bincount(a).tolist()==[294,12302]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':D,'coplanar_components':len(cs),'coplanar_neutralized_faces':[],'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'12596 original triangles unchanged','limits':['Front125/reverse127 true outer screen field triangles, excluding all groove floors and reveals. Three front piers: 42 original vertical side faces, including original 6 front faces. Visible side returns pale; unseen same-pier continuity inferred. Caps and reverse piers remain neutral.','Whole connected coplanar domains uniform.','Main mixed pinkwall/whitebase coplanar all neutral, no z threshold.','All windows crown rails screens roofs steps unknown neutral. Mainblock only, no lowpavilion/longbridge.','Capture dates unverified; suspicious default2002EXIF not evidence,2003opening not capture.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':12596,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],'components',len(cs))
