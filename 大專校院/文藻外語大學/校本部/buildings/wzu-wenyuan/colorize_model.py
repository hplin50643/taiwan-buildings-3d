"""1980 original triangles unchanged; partial material on full semantic planes only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;expected='59ed34ba2a8be04e11ce2a292611a47925595039534464100c5edac70ccc1379';assert hashlib.sha256((R/'model.stl').read_bytes()).hexdigest()==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==1980
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.full(len(t),2,np.int32)
def plane(y):return (np.max(abs(t[:,:,1]-y),axis=1)<.003)&(m.face_normals[:,1]<-.99)
def span(ax,l,h):return (lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
frame=plane(-28)&span(0,-22,22)&span(2,27,41);fascia=plane(-24)&span(0,-69,69)&span(2,24,26.2)
roof=(np.max(abs(t[:,:,2]-(44.5+(t[:,:,1]+26.5)*6.5/25.705)),axis=1)<.003)&span(0,-72,72)&span(1,-26.5,-.795)&span(2,44.5,51)&(m.face_normals[:,2]>.8)&(m.face_normals[:,1]<-.1)
assert frame.sum()==20 and fascia.sum()==2 and roof.sum()>0
assert not np.any(roof&(frame|fascia))
a[roof]=0;a[frame|fascia]=1
pal=[('Observed FRONT inclined roof muted graygreen','#606B60'),('Observed central outer frame and front fascia warm gray','#CCC8B9'),('UNVERIFIED mixed columns walls panes rear roof neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'1980 original triangles unchanged; no new or split faces','domains':{'front_roof_upper_slope':int(roof.sum()),'central_outer_frame':int(frame.sum()),'front_floor_fascia':int(fascia.sum())},'limitations':['True inclined front roof plane only; pale rim/ridge, roof side/back slopes neutral.','Mixed-height columns and broad brick/frame/window walls neutral; undated inconsistent nameplate gray-blue neutral.','Photo capture dates unknown;2023 form and2025 PDF edition not capture dates.','Material labels are not a verified multi-filament slicing job.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':1980,'original_STL_sha256':expected,'color_mesh_sha256':hashlib.sha256((R/'color-mesh.npz').read_bytes()).hexdigest()},indent=2));print(np.unique(a,return_counts=True))
