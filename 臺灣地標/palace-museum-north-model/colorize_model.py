"""Preserve photo-based front colors; infer coherent side/rear material continuity.
Original north museum triangles remain unchanged.
The initial assignment below reconstructs the predecessor before neutral-only extension.
"""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;EXPECTED_STL='0286971124851f5ffeeaade6b98fd056a26275edbd8b83312a2723892bb6340c'
assert hashlib.sha256((R/'model.stl').read_bytes()).hexdigest()==EXPECTED_STL
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==5558
pal=[('Photographed front ochre wall','#C4A269'),('Existing pale front rails and relief','#D4D5CA'),('Existing gray stairs and entrance stone','#989D96'),('Observed outward jade roof slopes','#659C8C'),('Existing broad roof rim ochre interpretation','#BA944F'),('Original recess shadow and opaque canopy','#536B65'),('UNVERIFIED rear inward slopes roof top','#A7ABA5')]
a=np.full(len(m.faces),6,np.int32)
roofs=[(0,20,28.7,138,31,2,131,24),(-24,5.2,30,17,9,1.6,12,4),(24,5.2,30,17,9,1.6,12,4),(0,18.5,38.2,32,26,6.1,15.8,9.8),(-33.5,24,36.8,14.5,14.5,4.5,1.8,1.8),(33.5,24,36.8,14.5,14.5,4.5,1.8,1.8),(-60.5,-6,18.5,24,22,1.7,18,16),(60.5,-6,18.5,24,22,1.7,18,16),(-60.5,-6,25.8,23.5,21.5,4.4,10.5,8.5),(60.5,-6,25.8,23.5,21.5,4.4,10.5,8.5)]
for i,(t,c,n)in enumerate(zip(m.triangles,m.triangles_center,m.face_normals)):
 lo=t.min(0);hi=t.max(0);x,y,z=c;nx,ny,nz=n
 def inside(x0,x1,y0,y1,z0,z1):return lo[0]>=x0-.003 and hi[0]<=x1+.003 and lo[1]>=y0-.003 and hi[1]<=y1+.003 and lo[2]>=z0-.003 and hi[2]<=z1+.003
 def plane(j,v):return np.all(np.abs(t[:,j]-v)<.003)
 if hi[2]<=2.401:continue
 # Source-visible coherent front planes. No material threshold across large triangles.
 if ny<-.99 and (plane(1,6.5)or plane(1,1.8)or plane(1,-23.5)or plane(1,-13.5)):a[i]=0
 if inside(-56,56,-16.51,-12.49,2.3,12.4):a[i]=2
 for sx in [-1,1]:
  if inside(sx*18.9-5.4,sx*18.9+5.4,-34.5,-14.1,2.25,16):a[i]=1 if (abs(x-sx*18.9)>4.4)else 2
  if inside(sx*39.5-21.6,sx*39.5+21.6,-16.1,-14.9,12.15,14.46):a[i]=1
  if inside(sx*60.5-10.6,sx*60.5+10.6,-15.8,-14.7,18.8,21.11):a[i]=1
  if inside(sx*60.5-10.9,sx*60.5+10.9,-15.51,3.51,18.1,19.1)and ny<-.5:a[i]=1
  for dx in [-7,-3.5,0,3.5,7]:
   if inside(sx*60.5+dx-.46,sx*60.5+dx+.46,-13.91,-13.09,20,25.8):a[i]=1
  if inside(sx*60.5-8,sx*60.5+8,-23.5,-23.1,3.4,9.4)and not plane(1,-23.5):a[i]=5
  if inside(sx*60.5-7.5,sx*60.5+7.5,-13.7,-13.3,21.5,25.1)and ny<-.99 and not plane(1,-13.5):a[i]=5
 if inside(-52,52,-16.4,-16.15,3.3,9.1)and ny<-.99:a[i]=5
 # Main upper pavilion front wall is pale, with discrete dark recesses.
 if inside(-12.5,12.5,8.24,8.81,29,38.5):a[i]=1
 if inside(-12,12,8.44,8.76,31.5,36.7)and ny<-.99:a[i]=5
 for xx in np.linspace(-11.5,11.5,8):
  if inside(xx-.4,xx+.4,7.89,8.61,30.5,38):a[i]=1
 if inside(-4.5,4.5,5.63,6.53,23.1,24.8):a[i]=1
 for xx in [-24,24]:
  if inside(xx-2.15,xx+2.15,1,1.91,19.6,28.6):a[i]=1
 if inside(-13,13,-33,-14.3,2.3,12.4)and nz>.1 and nz<.999:a[i]=5
 for xx in np.linspace(-12.7,12.7,9):
  if inside(xx-.26,xx+.26,-32.8,-14.4,3.4,12.8):a[i]=2
 if inside(-13.8,13.8,-14.5,-13.3,12.15,14.46):a[i]=1
 # Complete upward/frontward sloped faces only. Back slopes and horizontal roof remain neutral.
 for rx,ry,rz,w,d,h,tw,td in roofs:
  if inside(rx-w/2,rx+w/2,ry-d/2,ry+d/2,rz-.1,rz+h+.01)and nz>.05 and nz<.999 and ny<-.01 and abs(ny)>2*abs(nx) and hi[1]<=ry+.003:a[i]=3
 for rx,ry,rz,tw,td in [(0,18.5,44.3,15.8,9.8),(-60.5,-6,30.2,10.5,8.5),(60.5,-6,30.2,10.5,8.5)]:
  if inside(rx-tw/2-.58,rx+tw/2+.58,ry-td/2-.58,ry+.01,rz-.15,rz+1.51):a[i]=4
original_materials=a.copy(); categories={}; changes=[]
for i,(t,c,n) in enumerate(zip(m.triangles,m.triangles_center,m.face_normals)):
 if a[i]!=6: continue
 lo=t.min(0);hi=t.max(0);x,y,z=c;nx,ny,nz=n;category=None;new=6
 def inside(x0,x1,y0,y1,z0,z1):return lo[0]>=x0-.003 and hi[0]<=x1+.003 and lo[1]>=y0-.003 and hi[1]<=y1+.003 and lo[2]>=z0-.003 and hi[2]<=z1+.003
 def plane(j,v):return np.all(np.abs(t[:,j]-v)<.003)
 # Whole original slope triangles. Horizontal tops, downward soffits and rims
 # are separate material domains and cannot be selected by centroid alone.
 for rx,ry,rz,w,d,h,tw,td in roofs:
  if inside(rx-w/2,rx+w/2,ry-d/2,ry+d/2,rz-.1,rz+h+.01) and .05<nz<.999:
   new=3;category='same_roof_family_slopes_inferred'
 # Exact primitive footprints of existing raised rim bars/corner caps.
 # The bounded inner horizontal roof plate never belongs to these footprints.
 for rx,ry,rz,tw,td in [(0,18.5,44.3,15.8,9.8),(-60.5,-6,30.2,10.5,8.5),(60.5,-6,30.2,10.5,8.5)]:
  for xx in [rx-tw/2,rx+tw/2]:
   if inside(xx-.425,xx+.425,ry-(td+1)/2,ry+(td+1)/2,rz-.15,rz+.65):new=4;category='existing_raised_rim_inferred'
  for yy in [ry-td/2,ry+td/2]:
   if inside(rx-(tw+.8)/2,rx+(tw+.8)/2,yy-.425,yy+.425,rz-.15,rz+.65):new=4;category='existing_raised_rim_inferred'
  for xx in [rx-tw/2,rx+tw/2]:
   for yy in [ry-td/2,ry+td/2]:
    if inside(xx-.575,xx+.575,yy-.575,yy+.575,rz-.15,rz+1.5):new=4;category='existing_rim_corner_inferred'
 # Principal gallery real exterior planes. The rear structural belt and
 # broad lower terrace stay neutral, not borrowed from the ochre front.
 if abs(nz)<.001 and ((inside(-67,67,6.5,33.5,12,29.1) and (plane(0,-67) or plane(0,67))) or (inside(-67,67,6.5,33.5,13.1,29.1) and plane(1,33.5))):
  new=0;category='gallery_exterior_wall_inferred'
 # Shallow facade projections: same solid walls, not fake windows or relief.
 for xx in [-24,24]:
  if abs(nz)<.001 and inside(xx-7,xx+7,1.8,8.8,12.4,30.3) and (plane(0,xx-7) or plane(0,xx+7)):
   new=0;category='facade_projection_return_inferred'
 # Terminal towers have front ochre on both their tall ground wall and upper
 # wall. Extend only exact original vertical shell planes, not balconies.
 for xx in [-60.5,60.5]:
  if abs(nz)<.001 and inside(xx-10,xx+10,-23.5,26.5,2.4,18.8) and (plane(0,xx-10) or plane(0,xx+10) or plane(1,26.5)):
   new=0;category='terminal_lower_wall_inferred'
  if abs(nz)<.001 and inside(xx-8.25,xx+8.25,-13.5,1.5,19.7,26) and (plane(0,xx-8.25) or plane(0,xx+8.25) or plane(1,1.5)):
   new=0;category='terminal_upper_wall_inferred'
 # Existing central pavilion front is pale stone family. Match its coherent
 # plain side/rear wall shell, without adding any missing doors/windows.
 if abs(nz)<.001 and inside(-12.5,12.5,8.5,28.5,30.5,38.5) and (plane(0,-12.5) or plane(0,12.5) or plane(1,28.5)):
  new=1;category='central_pavilion_wall_inferred'
 if new!=6:
  a[i]=new;categories[category]=categories.get(category,0)+1
  changes.append({'face':i,'old':6,'new':int(new),'reason':category})
assert np.array_equal(a[original_materials!=6],original_materials[original_materials!=6])
(R/'FACADE-COLOR-CHANGESET.json').write_text(json.dumps({'status':'PASS','scope':'Whole original neutral triangles only; side/rear continuity inference, not a face-by-face photographic survey.','categories':categories,'changed_faces':len(changes),'changes':changes},indent=2)+'\n')
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a)
(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'geometry_policy':'5558 original triangles unchanged','limits':['Original photo-based front colors preserved; coherent side/rear shell continuation is inferred.','Horizontal roof tops, lower terrace, ambiguous mixed triangles and unsupported components stay neutral.','Original opaque canopy remains solid, not a transparent reconstruction.','Seven materials, not a verified four-filament print.']},indent=2)+'\n')
q={'status':'PASS','original_STL_sha256':EXPECTED_STL,'triangles':len(m.faces),'materials_used':np.unique(a).tolist(),'color_mesh_sha256':hashlib.sha256((R/'color-mesh.npz').read_bytes()).hexdigest()};(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps(q,indent=2));print(q)
