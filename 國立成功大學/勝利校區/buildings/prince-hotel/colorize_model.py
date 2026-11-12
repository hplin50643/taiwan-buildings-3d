"""Original 2802-triangle color mapping only; no subdivision or new geometry."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;EXPECTED='cf5263cd1a58f66ee38a8ecc5aacc955cb286320808485da817b9754c3de7b60'
assert hashlib.sha256((R/'model.stl').read_bytes()).hexdigest()==EXPECTED
m=trimesh.load(R/'model.stl',process=True,force='mesh');assert len(m.faces)==2802 and m.is_watertight
pal=[('Bounded same-component brick-family inference','#AB7960'),('Approximate pale existing trim and intrados','#D4CEB9'),('Existing clock discs off-white','#E0E2DC'),('Generic recess shadow not night illumination','#485355'),('UNVERIFIED wall slab roof sides neutral','#A7ABA5')]
t=m.triangles;c=m.triangles_center;mat=np.full(len(c),4,np.int32)
for i,(x,y,z) in enumerate(c):
 lo=t[i].min(axis=0);hi=t[i].max(axis=0);nz=m.face_normals[i,2]
 if z<=3.001:continue
 # Tower same component color family inference, never extend into unrelated main facade.
 if lo[0]>=31.999 and hi[0]<=56.001 and lo[1]>=-26.001 and hi[1]<=.001 and hi[2]<=138.001:mat[i]=0
 # Cylinder vertical skin: all original vertices on radius19; curved topology already present.
 rr=np.linalg.norm(t[i,:,:2]-[49,-26],axis=1)
 if abs(np.dot(m.face_normals[i,:2],c[i,:2]-[49,-26])-19*np.cos(np.pi/64))<.03 and hi[2]<=33.901 and abs(nz)<.01:mat[i]=0
 # Coherent existing crown vertical faces; horizontal roofs remain unknown.
 if any(lo[2]>=a-.001 and hi[2]<=a+h+.001 for a,h in [(116,1.4),(124,1.4),(137,3)]) and lo[0]>=29.499 and hi[0]<=58.501 and lo[1]>=-28.501 and hi[1]<=2.501 and abs(nz)<.01:mat[i]=1
 if lo[2]>=32.999 and hi[2]<=35.201 and np.all(abs(rr-21)<.02) and abs(nz)<.01:mat[i]=1
 # Only existing clock disc surfaces, not inferred numerals or logo.
 if np.all(np.linalg.norm(t[i,:,[0,2]].T-[44,131],axis=1)<=4.102) and lo[1]>=-27.001 and hi[1]<=-25.799:mat[i]=2
 if np.all(np.linalg.norm(t[i,:,[1,2]].T-[-13,131],axis=1)<=4.102) and lo[0]>=55.999 and hi[0]<=57.201:mat[i]=2
 # Hotel facade and tower discrete recess backs: generic shadow, no glowing-yellow paint.
 if abs(y+14.6)<.002 and any(abs(x-a)<6.001 for a in [-49,-33,-17,-1,15]) and any(a-.001<z<a+8.001 for a in range(35,108,11)):mat[i]=3
 if abs(y+25.2)<.002 and any(abs(x-a)<2.001 for a in [37,43,49]) and any(a-.001<z<a+7.001 for a in range(37,111,9)):mat[i]=3
 # Original arched recess intrados only, not invented exterior white trim rings.
 for a,w,zz,hh,back,front in [(a,16,7,19,-40.6,-42.6) for a in [-52,-30,-8,14]]+[(a,10,12,15,-42.55,-44.85) for a in [41,56]]:
  if lo[0]>=a-w/2-.002 and hi[0]<=a+w/2+.002 and lo[2]>=zz-.002 and hi[2]<=zz+hh+.002 and lo[1]>=front-.002 and hi[1]<=back+.002:
   mat[i]=3 if abs(y-back)<.002 else 1
 # Roof horizontal faces remain neutral even above tower and cylinder.
 if nz>.99 and z>30:mat[i]=4
# Bounded new official daytime front fascia, not underside or roof top.
old=mat.copy();hit=np.all(abs(t[:,:,1]+20)<.002,axis=1)&np.all(t[:,:,2]>=110.999,axis=1)&np.all(t[:,:,2]<=113.501,axis=1)&np.all(t[:,:,0]>=-64.501,axis=1)&np.all(t[:,:,0]<=32.001,axis=1)
assert np.flatnonzero(hit).tolist()==[261,262] and np.all(mat[hit]==4)
mat[hit]=5;pal.append(('Bounded daytime main roof front fascia pale grey family','#BEC2BC'))
assert np.array_equal(old[~hit],mat[~hit])
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=mat)
(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');assert len(np.unique(mat))==6
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':a,'hex':b,'faces':int(np.sum(mat==i))}for i,(a,b)in enumerate(pal)],'geometry_policy':'2802 original triangles unchanged.','limits':'Tower and cylinder brick-family continuity is explicit same-component inference. Long wall/slabs remain neutral; two highest roof front fascia faces use bounded new official daytime palegrey evidence, not top or soffit; no warm illumination painted. Pale arch intrados only, no added white rings. Unknown roofs and sides neutral.','printing':'Six appearance labels are not a tested multi-filament slicer project.'},indent=2)+'\n')
q={'status':'PASS','original_STL_sha256':EXPECTED,'triangles':len(m.faces),'materials_used':np.unique(mat).tolist(),'bounds_mm':m.bounds.tolist(),'color_mesh_sha256':hashlib.sha256((R/'color-mesh.npz').read_bytes()).hexdigest()};(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps(q,indent=2)+'\n');print(q)
