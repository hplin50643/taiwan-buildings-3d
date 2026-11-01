"""FSVS historical small storehouse undated exterior; not current use/asbuilt.
Only CCRH11423036; no interior storage or operational/security details. Metres until final1:50 millimetre export.
"""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
from manifold3d import Manifold,CrossSection
R=Path(__file__).resolve().parent;P=[];LOG=[];IDS={};S=20
PALETTE=[('rendered plaster approximate','#CBC8B2'),('base mortar approximate','#A5AAA0'),('roof neutral approximation','#9C9F95'),('window wood approximate','#877B63'),('authored display base not terrain','#ADB4A2'),('opaque window backing','#526970'),('simple closed door exterior','#8C9796')]
def box(a,b,c,d,e,f):return Manifold.cube((b-a,d-c,f-e)).translate((a,c,e))
def add(n,m,mat=0):
 assert not m.is_empty(),n
 m=m.as_original();IDS[m.original_id()]=mat;P.append(m);LOG.append({'name':n,'material':mat,'bounds_m':list(m.bounding_box())})
def bx(n,a,b,c,d,e,f,mat=0):add(n,box(a,b,c,d,e,f),mat)
def profile_xz(n,pts,y0,y1,mat=0):
 # CrossSection extrusion local z rotated into world y.
 if sum(pts[i][0]*pts[(i+1)%len(pts)][1]-pts[(i+1)%len(pts)][0]*pts[i][1] for i in range(len(pts)))<0:pts=pts[::-1]
 m=CrossSection([pts]).extrude(y1-y0).rotate((90,0,0)).translate((0,y1,0));add(n,m,mat)
def beam(n,a,b,w=.035,mat=3):
 a=np.array(a);b=np.array(b);vec=b-a;L=np.linalg.norm(vec);z=vec/L;aux=np.array([0.,0.,1.]);
 if abs(z@aux)>.95:aux=np.array([0.,1.,0.])
 x=np.cross(z,aux);x/=np.linalg.norm(x);y=np.cross(z,x)
 # square section hull connecting endpoints, overlapped at endpoints.
 pts=[p+sx*x*w/2+sy*y*w/2 for p in [a-z*.01,b+z*.01] for sx in [-1,1] for sy in [-1,1]]
 add(n,Manifold.hull_points(pts),mat)


# Historical exterior only. Internal use, mechanisms and furnishing excluded.
bx('authored_display_base',-.95,5.45,-1.45,4.95,-.20,0,4)
bx('floor_display_FF020_graphic',-.10,4.60,-.10,4.10,-.01,.20,1)
bx('front_outer_platform12',.90,3.60,-1.0,.05,-.01,.12,1)
bx('entry_threshold20',1.30,3.20,-.16,.08,.11,.20,1)
# Main roofskin contour transferred from independent multi-baseline raster review.
ZL=3.526;ZR=3.518;ZP=4.51
slopeL=(ZP-ZL)/2.5;slopeR=(ZP-ZR)/2.5
zt=lambda y:ZP-(2-y)*slopeL if y<=2 else ZP-(y-2)*slopeR
# Closed display body to sloped soffit. No interior plan/security components.
pts=[(-.09,.18),(4.09,.18),(4.09,zt(4.09)-.065),(2,ZP-.065),(-.09,zt(-.09)-.065)]
body=CrossSection([pts]).extrude(4.68).rotate((90,0,90)).translate((-.09,0,0))
W=[]
def opening(n,axis,face,c,w,z0,z1,sgn=1):
 global body
 if axis=='y':body=body-box(c-w/2,c+w/2,face-.17,face+.17,z0,z1)
 else:body=body-box(face-.17,face+.17,c-w/2,c+w/2,z0,z1)
 W.append((n,axis,face,c,w,z0,z1,sgn))
for face,sgn,label in [(-.09,-1,'front'),(4.09,1,'rear')]:
 for c in [1.125,3.375]:opening(label+'_high_W','y',face,c,1.15,2.54,3.10,sgn)
opening('front_plain_closed_door','y',-.09,2.25,1.80,.20,2.20,-1)
for face,sgn,label in [(-.09,-1,'left'),(4.59,1,'right')]:
 opening(label+'_high_W','x',face,2.0,1.15,2.54,3.10,sgn)
 for c in [1.45,2.55]:opening(label+'_gable_vent','x',face,c,.32,3.54,4.10,sgn)
add('closed_historical_exterior_no_interior',body,0)
for n,axis,face,c,w,z0,z1,sgn in W:
 def panel(tag,u0,u1,v0,v1,d0,d1,mat):
  a,b=sorted([face+sgn*d0,face+sgn*d1]);
  if axis=='y':bx(n+tag,u0,u1,a,b,v0,v1,mat)
  else:bx(n+tag,a,b,u0,u1,v0,v1,mat)
 isdoor='door' in n;vent='vent' in n
 panel('_opaque_back',c-w/2-.01,c+w/2+.01,z0-.01,z1+.01,-.23,-.08,6 if isdoor else 5)
 for u in [c-w/2,c+w/2-.05]:panel('_jamb',u,u+.05,z0,z1,-.12,.035,6 if isdoor else 3)
 for z,h in [(z0,.06),(z1-.05,.05)]:panel('_edge',c-w/2,c+w/2,z,z+h,-.12,.035,6 if isdoor else 3)
 if isdoor:
  # Plain closed two-leaf outer surface only, no locking/operational detail.
  panel('_center_leaf_seam',c-.018,c+.018,z0,z1,-.10,.015,6)
 elif vent:
  for z in np.linspace(z0+.10,z1-.08,7):panel('_simplified_external_louver',c-w/2+.035,c+w/2-.035,z,z+.025,-.10,.04,3)
 else:panel('_two_pane_divider',c-.025,c+.025,z0,z1,-.12,.035,3)
# Source-visible horizontal finish courses, not invented masonry specification.
for z in np.arange(.60,3.50,.45):
 band=box(-.105,4.605,-.105,4.105,z,z+.018)-box(-.085,4.585,-.085,4.085,z-.01,z+.03)
 for n,axis,face,c,w,z0,z1,sgn in W:
  if z0-.03<=z<=z1+.03:
   if axis=='y':band=band-box(c-w/2-.02,c+w/2+.02,face-.20,face+.20,z-.01,z+.03)
   else:band=band-box(face-.20,face+.20,c-w/2-.02,c+w/2+.02,z-.01,z+.03)
 add('horizontal_exterior_finish_course_graphic',band,0)
# Separate pitched sheets retain unequal eave estimates;6.5cm visual thickness simplified.
for lo,hi,za,zb in [(-.50,2.,ZL,ZP),(2.,4.50,ZP,ZR)]:
 pp=[(lo,za-.065),(hi,zb-.065),(hi,zb),(lo,za)]
 add('pitched_roof_skin_raster_control',CrossSection([pp]).extrude(5.40).rotate((90,0,90)).translate((-.45,0,0)),2)
# 15cm edge fascia at eaves, source profile simplified externally.
for y,z in [(-.50,ZL),(4.50,ZR)]:bx('eave_fascia15_graphic',-.45,4.95,y-.025,y+.025,z-.15,z+.005,2)
# Rounded ridge cap,highest4.67, no operational details.
cap=Manifold.cylinder(5.40,.085,.085,32).rotate((0,90,0)).translate((-.45,2.,4.585));add('ridge_cap_nominal_top467',cap,2)
bx('ridge_cap_hidden_connector',-.44,4.94,1.95,2.05,4.48,4.57,2)
# Independent270x100 door canopy,249top/233underside.
bx('front_canopy270x100_top249_bottom233',.90,3.60,-1.00,.06,2.33,2.49,1)

solid=P[0]
for p in P[1:]:solid=solid+p
solid=solid.translate((-2.25,-1.75,.20)).scale((S,S,S))
m=solid.to_mesh64();v=np.asarray(m.vert_properties)[:,:3];f=np.asarray(m.tri_verts);materials=np.zeros(len(f),dtype=int)
for i,oid in enumerate(m.run_original_id):materials[m.run_index[i]//3:m.run_index[i+1]//3]=IDS[int(oid)]
t=trimesh.Trimesh(v,f,process=False);t.merge_vertices(digits_vertex=12);keep=t.nondegenerate_faces();materials=materials[keep];t.update_faces(keep);t.remove_unreferenced_vertices();assert t.is_watertight and t.is_winding_consistent;assert len(t.split())==1,[(len(c.faces),c.bounds.tolist()) for c in t.split()]
np.savez_compressed(R/'mesh.npz',vertices=t.vertices,faces=t.faces,materials=materials);t.export(R/'model.stl');(R/'palette.json').write_text(json.dumps(PALETTE));(R/'components.json').write_text(json.dumps(LOG,ensure_ascii=False,indent=2))
q={'status':'PASS_GEOMETRY_ONLY','triangles':len(t.faces),'components':len(t.split()),'watertight':bool(t.is_watertight),'winding':bool(t.is_winding_consistent),'scale':'1:50','datum':'GL0; authoredsupportnotterrain','bounds_mm':t.bounds.tolist(),'mesh_sha256':hashlib.sha256((R/'mesh.npz').read_bytes()).hexdigest()};(R/'BUILD-QA.json').write_text(json.dumps(q,indent=2));print(json.dumps(q))
