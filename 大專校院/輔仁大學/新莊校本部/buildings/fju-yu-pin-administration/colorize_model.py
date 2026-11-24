"""Same 3836 original triangles, only exact source-supported front planes."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;expected='ebbae24bcf6e89c97151832a96f159524b5015534a164532d7aa503bba5b2c21';assert hashlib.sha256((R/'model.stl').read_bytes()).hexdigest()==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==3836
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.full(len(t),2,np.int32)
def plane(y):return (np.max(abs(t[:,:,1]-y),axis=1)<.003)&(m.face_normals[:,1]<-.99)
def box(x0,x1,z0,z1):return (lo[:,0]>=x0-.003)&(hi[:,0]<=x1+.003)&(lo[:,2]>=z0-.003)&(hi[:,2]<=z1+.003)
grid=plane(-22.85)&box(-12,12,20,45);back=plane(-19.5)&box(-12,12,20,44.5);canopy=plane(-31.5)&box(-16,16,16.2,18.4)
slots=plane(-14.3)&(box(-19.7,-16.3,6,43)|box(16.3,19.7,6,43))
assert [grid.sum(),back.sum(),canopy.sum(),slots.sum()]==[402,2,2,4]
a[grid|canopy]=0;a[back|slots]=1
pal=[('Observed screen and canopy FRONT warm off-white','#DADBD2'),('Actual screen backing and nearest slots muted shadow','#414B47'),('UNVERIFIED upper windows walls rear roof underside neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'3836 original triangles unchanged; no new or split faces','domains':{'screen_front':int(grid.sum()),'screen_back':int(back.sum()),'near_slot_backs':int(slots.sum()),'canopy_front':int(canopy.sum())},'limitations':['Only exact existing front coplanar domains; upper long window band, canopy underside and unknown large walls neutral.','2019 publication photo capture unknown plus 2023 entrance event, not code2025/current color survey.','Three material labels are not a verified multi-filament slicing job.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':3836,'original_STL_sha256':expected,'color_mesh_sha256':hashlib.sha256((R/'color-mesh.npz').read_bytes()).hexdigest()},indent=2));print(np.unique(a,return_counts=True))
