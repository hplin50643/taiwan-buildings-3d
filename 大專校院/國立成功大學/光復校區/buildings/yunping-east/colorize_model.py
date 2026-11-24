"""Bounded color interpretation on unchanged Yunping east geometry."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;EXPECTED_STL='2e53b2878c951d668f6ab134393c3393f3a4dbe65e358b12be149961fe09836f'
assert hashlib.sha256((R/'model.stl').read_bytes()).hexdigest()==EXPECTED_STL
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==6576
pal=[('Observed brick family','#AA705E'),('Existing gray frame and slab edges','#B0B0A5'),('Source-matched window glass recess','#405C68'),('Open corridor and arch shadow','#555953'),('UNVERIFIED neutral rear roof and ambiguous planes','#A7ABA5'),('Display support','#AAA79E')];mat=np.full(len(m.faces),4,dtype=np.int32)
for i,(t,(x,y,z),n)in enumerate(zip(m.triangles,m.triangles_center,m.face_normals)):
 lo=t.min(0);hi=t.max(0);nx,ny,nz=n
 if hi[2]<=3.001:mat[i]=5;continue
 # Full original front field remains neutral: no face-safe horizontal paint boundary.
 if abs(y+52.5)<.003 and ny<-.99:mat[i]=4
 if lo[1]>=-53.701 and hi[1]<=-51.499 and hi[2]<=91.401 and lo[2]>=7.999:
  if abs(y+51.5)<.003 and ny<-.99:mat[i]=2
 # Existing lower projecting grid only. No new face at the true gray-finish boundary.
 if hi[1]<=-52.001 and lo[1]>=-54.001 and lo[2]>=2.999 and hi[2]<=37.201:
  if any(lo[0]>=xx-.602 and hi[0]<=xx+.602 for xx in range(-65,66,10)) or any(lo[2]>=zz-.002 and hi[2]<=zz+1.202 for zz in [14,25,36]):mat[i]=1
 # Court-facing brick fields and recessed open corridors (not glass walls).
 if (abs(y+27.5)<.003 and ny>.99) or (abs(y-25)<.003 and ny<-.99):mat[i]=0
 if (abs(y+28.5)<.003 and ny>.99)or(abs(y-26)<.003 and ny<-.99):mat[i]=3
 for zz in [8,19,30,41,52,63,74,85]:
  if lo[2]>=zz-1-.002 and hi[2]<=zz+.302 and lo[0]>=-34.001 and hi[0]<=54.001 and ((lo[1]>=-28.201 and hi[1]<=-25.199)or(lo[1]>=22.699 and hi[1]<=25.701)):mat[i]=1
 # Inner end x=-34, discreet grid recesses only.
 if abs(x+34)<.003 and nx>.99:mat[i]=0
 if abs(x+35)<.003 and nx>.99 and lo[2]>=23.999 and hi[2]<=85.001 and lo[1]>=-9.751 and hi[1]<=9.751:mat[i]=2
 # Door arch back is shadow, not painted glass.
 if nx>.9 and -38<x<-34 and hi[2]<=19.01 and lo[1]>=-7.01 and hi[1]<=7.01:mat[i]=3
 # Small front portal is only bounded gray family, no added doorway detail.
 if lo[0]>=-19.501 and hi[0]<=3.501 and hi[1]<=-52.5 and hi[2]<=23.001:mat[i]=1
 if abs(y+58.6)<.003 and ny<-.99:mat[i]=3
 # No evidence for flat roofs; never turn them into brick-colored roofs.
 if nz>.9 and z>90:mat[i]=4
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=mat);(R/'palette.json').write_text(json.dumps(pal,ensure_ascii=False,indent=2)+'\n')
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':a,'hex':b,'faces':int((mat==i).sum())}for i,(a,b)in enumerate(pal)],'geometry_policy':'6576 original triangles unchanged, no new surfaces.','limits':['The entire outer long wall field remains neutral: existing triangles cross observed lower-gray/upper-brick boundaries. Only original projecting gray frames and discrete recesses receive color.','Discrete original window recesses cannot reproduce continuous real glazing strips.','Unverified outer and north walls and roof neutral.','Six materials not a verified four-filament project.']},ensure_ascii=False,indent=2)+'\n')
q={'status':'PASS','original_STL_sha256':EXPECTED_STL,'triangles':len(m.faces),'materials_used':np.unique(mat).tolist(),'watertight':bool(m.is_watertight),'color_mesh_sha256':hashlib.sha256((R/'color-mesh.npz').read_bytes()).hexdigest()};(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps(q,indent=2));print(q)
