"""Untouched original temple triangles, bounded exterior tile and stone families."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib,math
R=Path(__file__).resolve().parent;EXPECTED_STL='711cc5fe4d900955600e1fc5fea5930b3b1db1b7e12fc4cc3b35730c18d47206';assert hashlib.sha256((R/'model.stl').read_bytes()).hexdigest()==EXPECTED_STL
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==29236
pal=[('Source-bounded front orange tile family','#AC6948'),('Observed front gray stone family','#93948C'),('Existing front eave dark underside','#4D4841'),('Original genuine aperture shadows','#424743'),('UNVERIFIED ornaments roof backs walls and base','#B8BAB6')]
a=np.full(len(m.faces),4,np.int32)
roofs=[(0,-46,16.1,70,25,8,1.7),(-49,-46,14.1,27,23,6.2,1.7),(49,-46,14.1,27,23,6.2,1.7),(0,9,18.3,65,44,3.1,1.4),(0,9,22.3,65*.83,44*.79,7,1.8)]
def grid_height(x,y,cx,cy,z,w,d,h,up):
 # Re-evaluate original roof triangular grid, not a new surface/mesh.
 gx=np.clip((x-cx+w/2)/w*48,0,48);gy=np.clip((y-cy+d/2)/d*24,0,24);ix=np.minimum(np.floor(gx).astype(int),47);iy=np.minimum(np.floor(gy).astype(int),23);s=gx-ix;t=gy-iy
 def at(i,j):
  u=-1+2*i/48;v=-1+2*j/24;ax=np.abs(u);ay=np.abs(v);hip=np.minimum(1,np.maximum(0,(1-ax)/.27))
  return z+h*np.minimum((1-ay)**1.45,hip)+up*(ax**8+ay**8)*(.35+.65*ax*ay)+.38*(i%2)*np.maximum(0,np.sin(np.pi*j/24))**.25
 z00=at(ix,iy);z10=at(ix+1,iy);z01=at(ix,iy+1);z11=at(ix+1,iy+1)
 return np.where(s+t<=1,(1-s-t)*z00+s*z10+t*z01,(1-t)*z10+(s+t-1)*z11+(1-s)*z01)
for i,(t,c,n)in enumerate(zip(m.triangles,m.triangles_center,m.face_normals)):
 lo=t.min(0);hi=t.max(0);nx,ny,nz=n
 def inside(x0,x1,y0,y1,z0,z1):return lo[0]>=x0-.004 and hi[0]<=x1+.004 and lo[1]>=y0-.004 and hi[1]<=y1+.004 and lo[2]>=z0-.004 and hi[2]<=z1+.004
 def plane(j,v):return np.all(np.abs(t[:,j]-v)<.004)
 if hi[2]<=3.001:continue
 # Front hall and central courtyard front stone planes, not all four fused walls.
 for cx,cy,w,d,hh in [(0,-46,70,25,13),(-49,-46,27,23,11),(49,-46,27,23,11),(0,9,65,44,15.2)]:
  fy=cy-(d-2)/2
  if plane(1,fy)and inside(cx-w/2,cx+w/2,fy-.01,fy+.01,3,hh+4.01)and ny<-.99:a[i]=1
  # Original front engaged cylindrical columns and cap blocks.
  py=cy-d/2+1.5
  for xx in np.linspace(cx-w/2+3,cx+w/2-3,7):
   rad=np.linalg.norm(t[:,:2]-[xx,py],axis=1)
   if rad.max()<=.751 and lo[2]>=4.999 and hi[2]<=hh+4.001:a[i]=1
   if inside(xx-1,xx+1,py-1.05,py+1.05,hh+2.45,hh+3.55):a[i]=1
 # Existing front and central steps/platform top/front faces only.
 if inside(-15,15,-63.25,-57.5,2.8,4.66)and(nz>.99 or ny<-.99):a[i]=1
 if inside(-29,29,-20.5,9,3,6.91)and nz>.99:a[i]=1
 for sx in [-1,1]:
  if inside(sx*20-5,sx*20+5,-18,-10,2.8,5.21)and(nz>.99 or ny<-.99):a[i]=1
 # Actual front cut backs, dark shadow not reconstructed red doors.
 for xx in [-24,-12,0,12,24]:
  if plane(1,-55.5)and inside(xx-2.75,xx+2.75,-55.51,-55.49,4.5,13.5):a[i]=3
 for xx in [-30,30]:
  if plane(1,-55)and inside(xx-3.21,xx+3.21,-55.01,-54.99,6.99,13.41):a[i]=3
 for xx in [-49,49]:
  if plane(1,-56.5)and inside(xx-3.1,xx+3.1,-56.51,-56.49,4.2,12.9):a[i]=3
 for xx in [-18,-9,0,9,18]:
  if plane(1,-10.5)and inside(xx-2.6,xx+2.6,-10.51,-10.49,6.3,16.3):a[i]=3
 # Skin facets agree with all three vertices of the original roof grid;
 # rear halves, heightfield closures and ornamental crests are excluded.
 for cx,cy,zz,w,d,hh,up in roofs:
  if inside(cx-w/2,cx+w/2,cy-d/2,cy,zz-.001,zz+hh+up+.4):
   if nz>.01 and np.max(np.abs(t[:,2]-grid_height(t[:,0],t[:,1],cx,cy,zz,w,d,hh,up)))<.025:a[i]=0
  if plane(1,cy-d/2)and inside(cx-w/2,cx+w/2,cy-d/2-.01,cy-d/2+.01,zz-.8,zz+up*1.01)and ny<-.99:a[i]=2
 # Existing front sectors of three hexagonal tower roofs, not hexagonal wall paint.
 for cx in [-49,49]:
  cy=-22
  for zz,rad,hh in [(17.1,11.6,3.6),(23.3,10.2,3.2),(28.8,9.4,4.1)]:
   if hi[1]<=cy+.002 and lo[2]>=zz-.002 and hi[2]<=zz+hh+.002 and nz>.01 and nz<.999:
    uv=(t[:,:2]-[cx,cy])/[1.12,.84];apothem=rad*np.cos(np.pi/6)*(1-.58*(t[:,2]-zz)/hh)
    for angle in np.arange(60,361,60):
     pp=uv@np.array([np.cos(np.radians(angle)),np.sin(np.radians(angle))])
     if np.max(np.abs(pp-apothem))<.006:a[i]=0
  if plane(1,-27.8)and inside(cx-2.25,cx+2.25,-27.81,-27.79,6.5,15.1):a[i]=3

# 2026-11 local continuity extension. Preserve every pre-existing assignment.
# These remain estimates, not photogrammetric or date-specific paint measurements.
original_assignments=a.copy()
extension_domain=np.full(len(a),'',dtype='<U40')
def gallery_height(x,y,cx,cy):
 # Original gallery roof is a 24 x 24, unribbed heightfield rotated 90 degrees.
 xx=y-cy; yy=-(x-cx); gx=np.clip((xx+62.5)/125*24,0,24); gy=np.clip((yy+8)/16*24,0,24)
 ix=np.minimum(np.floor(gx).astype(int),23); iy=np.minimum(np.floor(gy).astype(int),23); s=gx-ix; t=gy-iy
 def at(i,j):
  u=-1+2*i/24; v=-1+2*j/24; ax=np.abs(u); ay=np.abs(v)
  return 16.7+3*np.minimum((1-ay)**1.45,np.minimum(1,np.maximum(0,(1-ax)/.27)))+.65*(ax**8+ay**8)*(.35+.65*ax*ay)
 z00=at(ix,iy);z10=at(ix+1,iy);z01=at(ix,iy+1);z11=at(ix+1,iy+1)
 return np.where(s+t<=1,(1-s-t)*z00+s*z10+t*z01,(1-t)*z10+(s+t-1)*z11+(1-s)*z01)
for i,(t,n) in enumerate(zip(m.triangles,m.face_normals)):
 if a[i]!=4: continue
 lo=t.min(0);hi=t.max(0);nx,ny,nz=n
 if nz<=.01: continue
 def inside(x0,x1,y0,y1,z0,z1):
  return lo[0]>=x0-.004 and hi[0]<=x1+.004 and lo[1]>=y0-.004 and hi[1]<=y1+.004 and lo[2]>=z0-.004 and hi[2]<=z1+.004
 for j,(cx,cy,zz,w,d,hh,up) in enumerate(roofs):
  if inside(cx-w/2,cx+w/2,cy-d/2,cy+d/2,zz-.001,zz+hh+up+.4) and np.max(np.abs(t[:,2]-grid_height(t[:,0],t[:,1],cx,cy,zz,w,d,hh,up)))<.025:
   a[i]=0;extension_domain[i]='front_main_hall_tile_continuity'
 for cx in [-49,49]:
  cy=-22
  for zz,rad,hh in [(17.1,11.6,3.6),(23.3,10.2,3.2),(28.8,9.4,4.1)]:
   if lo[2]>=zz-.002 and hi[2]<=zz+hh+.002 and nz<.999:
    uv=(t[:,:2]-[cx,cy])/[1.12,.84];apothem=rad*np.cos(np.pi/6)*(1-.58*(t[:,2]-zz)/hh)
    for angle in np.arange(60,361,60):
     pp=uv@np.array([np.cos(np.radians(angle)),np.sin(np.radians(angle))])
     if np.max(np.abs(pp-apothem))<.006:
      a[i]=0;extension_domain[i]='tower_tile_continuity'
 for cx in [-59,59]:
  if inside(cx-8,cx+8,6-62.5,6+62.5,16.699,20.5) and np.max(np.abs(t[:,2]-gallery_height(t[:,0],t[:,1],cx,6)))<.025:
   a[i]=0;extension_domain[i]='gallery_tile_family_inference'
# Same-building rear-hall tile-family inference. The visible rear-hall tile
# rows in the temple's 1998 guide photograph corroborate an orange tile family,
# but exact current color and unphotographed slopes remain estimates.
rear_roofs=[(0,54,16.5,70,26,3.1,1.4),(0,54,20.5,70*.83,26*.79,6.8,1.8),(-48,54,15.1,28,27,6.2,1.7),(48,54,15.1,28,27,6.2,1.7)]
for i,(t,n) in enumerate(zip(m.triangles,m.face_normals)):
 if a[i]!=4 or n[2]<=.01:continue
 lo=t.min(0);hi=t.max(0)
 for cx,cy,zz,w,d,hh,up in rear_roofs:
  if lo[0]>=cx-w/2-.004 and hi[0]<=cx+w/2+.004 and lo[1]>=cy-d/2-.004 and hi[1]<=cy+d/2+.004 and lo[2]>=zz-.005 and hi[2]<=zz+hh+up+.404 and np.max(np.abs(t[:,2]-grid_height(t[:,0],t[:,1],cx,cy,zz,w,d,hh,up)))<.025:
   a[i]=0;extension_domain[i]='rear_hall_tile_family_inference'
# A triangle's vertices can all meet a roof intersection while its interior is
# an original horizontal wall/column top. Do not disguise such flat cut caps as
# tiles. All pre-existing colored faces stay untouched.
excluded_horizontal=(original_assignments==4)&(a==0)&(m.face_normals[:,2]>.999999)
a[excluded_horizontal]=4;extension_domain[excluded_horizontal]=''
# Original 0.01 mm simplification can tilt a few former horizontal caps.
# Check whole-face interior samples, not only corners at the roof intersection.
near_flat_ids=np.flatnonzero((original_assignments==4)&(a==0)&(m.face_normals[:,2]>.999))
pts=m.triangles[near_flat_ids];pts=np.concatenate([pts,pts.mean(1)[:,None,:],(pts+np.roll(pts,1,axis=1))/2],axis=1)
best=np.full(len(near_flat_ids),np.inf)
for cx,cy,zz,w,d,hh,up in roofs+rear_roofs:
 xx=pts[:,:,0];yy=pts[:,:,1];inside=(xx.min(1)>=cx-w/2-.004)&(xx.max(1)<=cx+w/2+.004)&(yy.min(1)>=cy-d/2-.004)&(yy.max(1)<=cy+d/2+.004)
 err=np.abs(pts[:,:,2]-grid_height(xx,yy,cx,cy,zz,w,d,hh,up)).max(1)
 best=np.minimum(best,np.where(inside,err,np.inf))
for cx in [-59,59]:
 xx=pts[:,:,0];yy=pts[:,:,1];inside=(xx.min(1)>=cx-8-.004)&(xx.max(1)<=cx+8+.004)&(yy.min(1)>=-56.5-.004)&(yy.max(1)<=68.5+.004)
 err=np.abs(pts[:,:,2]-gallery_height(xx,yy,cx,6)).max(1)
 best=np.minimum(best,np.where(inside,err,np.inf))
excluded_near_horizontal=near_flat_ids[best>=.03]
a[excluded_near_horizontal]=4;extension_domain[excluded_near_horizontal]=''
assert np.array_equal(a[original_assignments!=4],original_assignments[original_assignments!=4])
assert np.all(original_assignments[a!=original_assignments]==4)
np.savez_compressed(R/'continuity-map.npz',original_materials=original_assignments,materials=a,domain=extension_domain,excluded_horizontal_face_ids=np.flatnonzero(excluded_horizontal),excluded_near_horizontal_face_ids=excluded_near_horizontal)

np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a)
(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
q={'status':'PASS','original_STL_sha256':EXPECTED_STL,'triangles':len(m.faces),'materials_used':np.unique(a).tolist(),'color_mesh_sha256':hashlib.sha256((R/'color-mesh.npz').read_bytes()).hexdigest(),'prior_colored_faces_preserved':int((original_assignments!=4).sum()),'neutral_faces_reassigned':int((a!=original_assignments).sum()),'changed_domains':{s:int((extension_domain==s).sum())for s in np.unique(extension_domain)if s},'preserved_palette_and_roughness':True,'horizontal_interface_facets_excluded':int(excluded_horizontal.sum()),'simplified_near_horizontal_interface_facets_excluded':len(excluded_near_horizontal)}
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps(q,indent=2)+'\n')
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'geometry_policy':'29236 original triangles unchanged','limits':['Only original tile skin slope facets are extended; all prior colored facets remain unchanged.','Front/main hall and tower roof slopes extend established tile material by continuity; rear-hall roof skins use same-building tile-family inference, corroborated by the temple guide rear-hall photograph captioned 1998.','Gallery tile-family inference uses visible gallery roofs beside the official tower reference; not a separately measured roof survey.','Every unknown wall, ornament, roof closure, horizontal intersection patch and display base remains neutral; rear-hall roof skins are now included by explicit tile-family inference.','Palette names are retained for stable identity: front/original unverified labels describe material provenance, not updated selected-face bounds.','Five appearance labels are not a tested four-filament slicer project.']},indent=2)+'\n')
print(q)
