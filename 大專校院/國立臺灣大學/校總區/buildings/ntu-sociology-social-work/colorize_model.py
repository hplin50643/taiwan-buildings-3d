"""Independent original front-band and photographed left-grid planes only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
from shapely.geometry import Polygon,box
from shapely.ops import unary_union
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='be0c69744e1fe1881149bf38b4264a790417104f39fe9be738a8b3474cc1cca1';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==3244
t=m.triangles;n=m.face_normals;e=.003;a=np.full(len(t),1,np.int32)
pal=[('Observed front horizontal bands and left outer grid muted stone gray','#B6B8B0'),('UNVERIFIED mixed brick stone window backing gable portal roof neutral','#B8BAB5')]
def plane(k,v):return np.max(abs(t[:,:,k]-v),axis=1)<e
bandshape=unary_union([box(-19,z,19,z+2)for z in [24,38,52]]).buffer(e)
gridshape=unary_union([box(-22,z,36,z+1.3)for z in [18,29,40,51,62]]+[box(y-.6,18,y+.6,63)for y in [-19,-6,7,20,33]]).buffer(e)
bands=[int(i)for i in np.flatnonzero(plane(1,-29.6)&(n[:,1]<-.999)) if bandshape.covers(Polygon(t[i][:,[0,2]]))]
grid=[int(i)for i in np.flatnonzero(plane(0,-69)&(n[:,0]<-.999)) if gridshape.covers(Polygon(t[i][:,[1,2]]))]
a[bands+grid]=0
ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999
cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1);neutralized=[]
for c in cs:
 if len(set(a[c]))>1:neutralized+=c[a[c]!=1].tolist();a[c]=1
D={'central_three_band_fronts':[i for i in bands if a[i]==0],'left_grid_outward':[i for i in grid if a[i]==0]};assert len(D['central_three_band_fronts'])==6 and len(D['left_grid_outward'])==202
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':D,'coplanar_components':len(cs),'coplanar_neutralized_faces':sorted(neutralized),'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'3244 original triangles unchanged','limits':['Three original y-29.6 front rectangles, no adjoining reveals.','Left x-69 grid complete plane union only; not recess/windowbackings.','Entire connected coplanar mixed domains neutral.','Central gable and brick are coplanar and remain fully neutral, no z-cut.','Portal bases, glazing, rear and roof neutral.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':3244,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],{k:len(v)for k,v in D.items()},'neutralized',len(neutralized),'components',len(cs))
