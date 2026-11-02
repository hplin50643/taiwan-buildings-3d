"""Material-only update of the original 3142-face mesh; no displacement, subdivision or textures."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;EXPECTED='15f50381efbbf8980a172a7fe4a0a78132118206175ce463b826e497ecdf0394'
assert hashlib.sha256((R/'model.stl').read_bytes()).hexdigest()==EXPECTED
m=trimesh.load(R/'model.stl',process=True,force='mesh');assert len(m.faces)==3142 and m.is_watertight
pal=[('Approximate dark gray main tile roof','#555A59'),('Approximate observed red-orange brick','#A9573B'),('Approximate pale gray entrance and bay balustrade','#C7C8B8'),('Opaque corridor recess shadow illustration NOT glazing','#55534D'),('UNVERIFIED ends rear roofs and authored base neutral','#B3B1A7')]
t=m.triangles;c=m.triangles_center;n=m.face_normals;mat=np.full(len(c),4,np.int32);bays=[-63,-55,-47,-19,-11,-3,5,13,21,47,55,63]
for i,((x,y,z),(nx,ny,nz)) in enumerate(zip(c,n)):
 if z<=3.001:continue
 # Main front wall / recess sides; endpoints remain neutral.
 if -28.501<=y<=-23.999 and abs(x)<69 and z<40.801:mat[i]=1
 # Courtyard red/gray framework is not separable in original large planes: neutral fallback, not all-red claim.
 if abs(x)<47.01 and -7.501<=y<=-5.499 and z<40.801:mat[i]=4
 if 46.999<=abs(x)<=49.251 and -5.5<y<32.501 and z<40.801:mat[i]=4
 # Existing recessed open-corridor backs: opaque shadow, never blue glass.
 if abs(y+24)<.002 and any(a-.001<z<a+9.001 for a in [5,17,29]) and any(abs(x-a)<2.651 for a in bays):mat[i]=3
 if abs(y+7.5)<.002 and any(a-.001<z<a+9.001 for a in [5,17,29]) and any(abs(x-a)<3.001 for a in range(-42,43,9)):mat[i]=3
 if abs(abs(x)-49.25)<.002 and any(a-.001<z<a+9.001 for a in [5,17,29]) and any(abs(y-a)<3.501 for a in [0,11,22]):mat[i]=3
 # Bay-specific existing panel faces only: never a continuous stripe across brick piers.
 if -28.501<=y<=-23.999 and any(np.all(abs(t[i,:,0]-a)<=2.651)for a in bays) and any(t[i,:,2].min()>=lo-.001 and t[i,:,2].max()<=hi+.001 for lo,hi in [(14,17),(26,29)]):mat[i]=2
 # Original projecting entry frames and cap; geometry-derived bounded components.
 for ex in [-34,34]:
  if abs(x-ex)<=7.501 and y<-28.49 and 2.999<z<35.001:mat[i]=2
  if abs(x-ex)<=9.001 and -34.001<=y<=-27.999 and 33.999<=z<=36.501:mat[i]=2
  if abs(x-ex)<=10.501 and y<-30.99 and z<5.201:mat[i]=2
  # Existing tall cut backs in entrance, not invented window panes or doors.
  if abs(y+30)<.002 and 15.999<z<30.001 and any(abs(x-ex-a)<1.201 for a in [-4.2,0,4.2]):mat[i]=3
  if abs(y+28)<.002 and 3.001<z<12.001 and abs(x-ex)<3.251:mat[i]=3
 # Roof entire existing main facets; rear-return extensions stay explicitly neutral.
 if z>=40.099 and np.max(t[i,:,1])<=-2.999:mat[i]=0
 if z>=46.999 and abs(y+17)<=.651 and abs(x)<=54.001:mat[i]=0
 # Plain unknown external end and return end faces stay neutral, not default red.
 if (abs(abs(x)-69)<.002 or abs(y-32.5)<.002) and z<40.801:mat[i]=4
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=mat)
(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');assert len(np.unique(mat))==5
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':a,'hex':b,'faces':int(np.sum(mat==i))}for i,(a,b)in enumerate(pal)],'geometry_policy':'3142 original triangles unchanged.','corridor_semantics':'Recess backs illustrate open-corridor shadow, not glazing or black paint.','four_color_printing':'Five appearance labels are not a tested four-filament slicer project.','limits':'Courtyard broad planes/rear roofs/ends neutral; bay panels only where existing triangles support material separation; no new gray belt across brick piers.'},indent=2)+'\n')
q={'status':'PASS','original_STL_sha256':EXPECTED,'triangles':len(m.faces),'materials_used':np.unique(mat).tolist(),'bounds_mm':m.bounds.tolist(),'color_mesh_sha256':hashlib.sha256((R/'color-mesh.npz').read_bytes()).hexdigest()};(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps(q,indent=2)+'\n');print(q)
