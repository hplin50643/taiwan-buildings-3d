"""Color-only original 3518-triangle geometry; no new surfaces or textures."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;EXPECTED='80ff9dc2d73fa0f4ad340dc49eaa53a8e223a1a6559a98b8cd29c8536b935bf4'
assert hashlib.sha256((R/'model.stl').read_bytes()).hexdigest()==EXPECTED
m=trimesh.load(R/'model.stl',process=True,force='mesh');assert len(m.faces)==3518 and m.is_watertight
pal=[('Approximate light structural frame','#DDDCD2'),('Approximate warm tan brick','#A88D70'),('Approximate balcony gray','#B3B7B1'),('Approximate light rail metal','#9BABA6'),('Open corridor shadow NOT glazing','#626861'),('UNVERIFIED rear side roof neutral','#A7ABA5'),('Authored display base neutral','#AAA8A0')]
t=m.triangles;c=m.triangles_center;mat=np.full(len(c),5,np.int32)
for i,(x,y,z) in enumerate(c):
 if z<=3.001:mat[i]=6;continue
 # Original front wall and recess reveal planes: light-frame fallback where brick bands lack facets.
 if -18.201<=y<=-13.999 and abs(x)<=68.001 and z<58.001:mat[i]=0
 # Back of each actual shallow corridor recess is shadow, not glass.
 if abs(y+14)<.002 and any(a-.001<z<a+7.001 for a in [6,17,28,39,50]):mat[i]=4
 # Broad projecting stair/brick zones, using all vertices to avoid diagonal partial-plane paints.
 if any(np.all(abs(t[i,:,0]-a)<=5.751) for a in [-36,36]) and t[i,:,1].min()>=-20.601 and t[i,:,1].max()<=-15.399 and t[i,:,2].max()<=58.001:mat[i]=1
 # Existing narrow rail relief; not arbitrary bands on underlying broad triangles.
 if -17.701<=y<=-16.299 and any(t[i,:,2].min()>=a+2.199 and t[i,:,2].max()<=a+3.201 for a in [15,26,37,48]):mat[i]=3
 # Central landing and actual parapet faces, plus original entry platform and short steps.
 if t[i,:,1].max()<-18.201 and np.all(abs(t[i,:,0])<=10.001) and t[i,:,2].max()<=42:mat[i]=2
 if y<-25 and abs(x)<=15.001 and z<=5.601:mat[i]=2
 # Top actual louvers: light gray relief with recess shade retained behind.
 if -18.201<=y<=-13.799 and any(t[i,:,2].min()>=a-.001 and t[i,:,2].max()<=a+.901 for a in [53,55]):mat[i]=3
 # Entire unverified horizontal roof slab and plain rear/end planes are neutral.
 if z>=58.001 or y>=23.999 or abs(x)>=67.999:mat[i]=5
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=mat)
(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');assert len(np.unique(mat))==7
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':a,'hex':b,'faces':int(np.sum(mat==i))}for i,(a,b)in enumerate(pal)],'geometry_policy':'3518 original triangles unchanged.','corridor_semantics':'Recess shadow not glazing or black paint.','four_color_printing':'Seven appearance labels are not a tested four-filament slicer project.','limits':'Photographic narrow horizontal brick bands lack independent mesh domains and remain simplified light-frame fallback; rear sides roof neutral.'},indent=2)+'\n')
q={'status':'PASS','original_STL_sha256':EXPECTED,'triangles':len(m.faces),'materials_used':np.unique(mat).tolist(),'bounds_mm':m.bounds.tolist(),'color_mesh_sha256':hashlib.sha256((R/'color-mesh.npz').read_bytes()).hexdigest()};(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps(q,indent=2)+'\n');print(q)
