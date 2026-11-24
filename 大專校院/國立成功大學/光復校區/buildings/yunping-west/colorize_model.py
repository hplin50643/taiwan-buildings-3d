"""Bounded appearance-only update; original 3822 triangles unchanged."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;EXPECTED='aa45e3be5e40607dd0255c9fdc0a36647fbdfd3b5c4296548dde7511e5f4b02f'
assert hashlib.sha256((R/'model.stl').read_bytes()).hexdigest()==EXPECTED
m=trimesh.load(R/'model.stl',process=True,force='mesh');assert len(m.faces)==3822 and m.is_watertight
pal=[('Approximate observed high-block brick family','#AA705E'),('Identifiable existing window recess gray-blue','#405C68'),('UNVERIFIED low front wing portal north roof and base neutral','#A7ABA5')]
t=m.triangles;c=m.triangles_center;mat=np.full(len(c),2,np.int32)
for i,(x,y,z) in enumerate(c):
 if z<=3.001:continue
 # Entire original higher shaft front, with whole triangles preserving coarse brick planes.
 if t[i,:,2].min()>=37.899 and t[i,:,1].min()>=-45.001 and t[i,:,1].max()<=-43.999 and -43.001<=x<=-6.999:mat[i]=0
 # Existing east/west shaft surfaces, not low transverse frontage.
 if -43.001<=x<=-41.999 or -8.001<=x<=-6.999:
  if t[i,:,1].max()<=24.001 and (t[i,:,1].min()>=-29.501 or t[i,:,2].min()>=37.899):mat[i]=0
 # Inward face of rear transverse volume; no inferred north or outer-end colors.
 if abs(y-24)<.002 and (x<-42.999 or x>-7.001):mat[i]=0
 # Only actual recessed backs use gray-blue, never broad solid walls/continuous glass.
 if abs(y+44.1)<.002 and any(a-.001<z<a+6.001 for a in [43,54,65,76]):mat[i]=1
 if abs(y+44.1)<.002 and 84.999<z<91.301:mat[i]=1
 if (abs(x+42.1)<.002 or abs(x+7.9)<.002) and any(a-.001<z<a+6.001 for a in [8,19,30,41,52,63,74,85]) and any(abs(y-a)<3.501 for a in [-31,-21,-11,-1,9,19]):
  if y>-29.501 or z>=37.899:mat[i]=1
 # Strong exclusions: unknown low wing, all north/outside end and roof horizontal surfaces.
 if (t[i,:,2].max()<=37.901 and t[i,:,1].max()<=-29.499) or y>=50.999 or x<=-55.099 or z>=93.899:mat[i]=2
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=mat)
(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');assert len(np.unique(mat))==3
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':a,'hex':b,'faces':int(np.sum(mat==i))}for i,(a,b)in enumerate(pal)],'geometry_policy':'3822 original triangles unchanged.','limits':'Entire low front wing and portal neutral; continuous photographic glass strips lack original topology and are not invented. North, outer end and roofs neutral.','printing':'Three appearance labels are not a tested four-filament slicer project.'},indent=2)+'\n')
q={'status':'PASS','original_STL_sha256':EXPECTED,'triangles':len(m.faces),'materials_used':np.unique(mat).tolist(),'bounds_mm':m.bounds.tolist(),'color_mesh_sha256':hashlib.sha256((R/'color-mesh.npz').read_bytes()).hexdigest()};(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps(q,indent=2)+'\n');print(q)
