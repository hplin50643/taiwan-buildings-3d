"""Original Weiwuying surfaces; color only, unchanged ASCII STL and triangles."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;EXPECTED_STL='13b1a18eb3f24fad733478a1efc9531be5bc52167cc7f1b4fa33494fa78b40cb';assert hashlib.sha256((R/'model.stl').read_bytes()).hexdigest()==EXPECTED_STL
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==38690
pal=[('Observed broad roof top silver off-white','#D6D8D5'),('Observed front-right outer fascia warm light gray','#D4D3CC'),('Original front-right inset backing gray-green glass','#668078'),('Original mullions restrained gray','#8B9690'),('Original explicit theater seating concrete gray','#AEB3AE'),('UNVERIFIED bowl wells underside rear and model base','#B7B9B3')];a=np.full(len(m.faces),5,np.int32)
def rawtop(x,y):return 16.5+9.5*np.exp(-((x+26)/29)**2-((y-12)/26)**2)+7*np.exp(-((x-27)/25)**2-((y+8)/25)**2)-6*np.exp(-((x+44)/10)**2-((y+46)/9)**2)
def top(x,y):
 z=rawtop(x,y);rr=np.sqrt((x-15)**2+(y-51)**2);return np.where(rr<27,np.minimum(z,5.5+np.maximum(0,rr-6)*.66),z)
for i,(t,n)in enumerate(zip(m.triangles,m.face_normals)):
 lo=t.min(0);hi=t.max(0);x,y,z=t.T;nx,ny,nz=n
 def inside(x0,x1,y0,y1,z0,z1):return lo[0]>=x0-.003 and hi[0]<=x1+.003 and lo[1]>=y0-.003 and hi[1]<=y1+.003 and lo[2]>=z0-.003 and hi[2]<=z1+.003
 rr=np.sqrt((x-15)**2+(y-51)**2);bowlactive=(rr<27)&(rawtop(x,y)>5.5+np.maximum(0,rr-6)*.66)
 well=False
 for wx,wy,w,d in [(-35,8,7,5),(0,14,8,6),(36,8,6,4)]:
  if lo[0]>=wx-w/2-.04 and hi[0]<=wx+w/2+.04 and lo[1]>=wy-d/2-.04 and hi[1]<=wy+d/2+.04:well=True
 # Match original analytic top, not merely upward normals. Mixed bowl and wells neutral.
 if nz>.1 and np.max(abs(z-top(x,y)))<.055 and not bowlactive.any() and not well:a[i]=0
 # Original external front/right edge equations, NOT the inset band backing.
 ef=-47*(1-.025*abs(x/68)**12);er=68*(1-.025*abs(y/47)**12)
 if ((np.max(abs(y-ef))<.055 and ny<-.25) or (np.max(abs(x-er))<.055 and nx>.25)) and lo[2]>4 and not bowlactive.any():a[i]=1
 # Original band inner backs use the distinct band sampling equations.
 yf=-47*(1-.025*abs(x/66.3)**12);zf=top(x,yf)
 xr=68*(1-.025*abs(y/45.825)**12);zr=top(xr,y)
 if lo[0]>=-29-.005 and hi[0]<=65+.005 and np.max(abs(y-(yf+.68)))<.025 and np.all(z>=zf-1.825) and np.all(z<=zf-.625) and ny<-.5:a[i]=2
 if lo[1]>=-44-.005 and hi[1]<=44+.005 and np.max(abs(x-(xr-.68)))<.025 and np.all(z>=zr-1.825) and np.all(z<=zr-.625) and nx>.5:a[i]=2
 # Original independent mullion boxes, all their vertices must fit exact tiny primitives.
 for xx in np.arange(-27,64,3.5):
  yy=-47*(1-.025*abs(xx/66.3)**12);zz=float(top(xx,yy))
  if inside(xx-.35,xx+.35,yy-.12,yy+.48,zz-1.97,zz-.47):a[i]=3
 for yy in np.arange(-41,44,3.5):
  xx=68*(1-.025*abs(yy/45.825)**12);zz=float(top(xx,yy))
  if inside(xx-.48,xx+.12,yy-.35,yy+.35,zz-1.97,zz-.47):a[i]=3
 # Only original ring-strip top/riser geometry, never radial paint over the bowl floor.
 for rad in np.arange(9,25,2.3):
  zz=5.5+(rad-6)*.66;outer=np.max(abs(rr-rad))<.055;inner=np.max(abs(rr-(rad-1.3)))<.055
  topseat=np.max(abs(z-(zz+.8)))<.015 and np.all(rr>=rad-1.36) and np.all(rr<=rad+.055)
  riser=(outer or inner) and np.all(z>=zz-.715) and np.all(z<=zz+.815)
  if lo[1]>=20-.005 and hi[1]<=50+.005 and (topseat or riser):a[i]=4
 if well:a[i]=5
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'geometry_policy':'38690 original triangles unchanged; original ASCII STL bytes unchanged','limits':['Analytic top equation and exact inset backings, not whole normal-up or whole slab color.','Bowl mixed landscaping and light wells neutral; no grass or equipment added.','Unverified sculpted underside and rear neutral; no black shadow paint.','Model base neutral representational, not surveyed site paving.','Six basic material labels not a verified multi-filament slicer project.']},indent=2)+'\n');q={'status':'PASS','original_STL_sha256':EXPECTED_STL,'triangles':len(m.faces),'materials_used':np.unique(a).tolist(),'color_mesh_sha256':hashlib.sha256((R/'color-mesh.npz').read_bytes()).hexdigest()};(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps(q,indent=2));print(q);print(np.unique(a,return_counts=True))
