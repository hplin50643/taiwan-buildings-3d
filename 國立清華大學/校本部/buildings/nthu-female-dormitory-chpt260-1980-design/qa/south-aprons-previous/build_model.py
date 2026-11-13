from pathlib import Path
import numpy as np,trimesh,json,hashlib
from manifold3d import Manifold,CrossSection
R=Path(__file__).resolve().parent;P=[];LOG=[];IDS={};S=1000/200
PALETTE=[('white washed finish approximate','#D1D1C7'),('concrete approximate','#AAAFA6'),('roof finish approximate','#B7B8AA'),('window frame approximate','#A6ABA5'),('authored display support not surveyed terrain','#A3AD9B'),('opaque glazing illustration','#546D75'),('closed entrance approximation','#737C79'),('dark mosaic approximate','#858675')]
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


# NTHU CHPT260 historical design. Wall-center reference dimensions, not finished-face bounding box.
from shapely.geometry import Polygon
OUTLINE=[(0,3),(3.6,3),(3.6,0),(18,0),(18,2),(21.6,2),(21.6,5.05),(25.2,5.05),(25.2,4.75),(28.8,4.75),(28.8,8.75),(50.4,8.75),(50.4,11.75),(54,11.75),(54,29.85),(50.4,29.85),(50.4,32.85),(28.8,32.85),(28.8,29.85),(25.2,29.85),(25.2,24.1),(3.6,24.1),(3.6,21.1),(0,21.1)]
outline=Polygon(OUTLINE);assert outline.is_valid
COURTS=[(5.075,17.925,8.55,15.55),(26.95,48.85,17.30,24.30)]
def poly_solid(poly,z0,z1):
 from shapely.geometry.polygon import orient
 if poly.geom_type=="MultiPolygon":
  parts=[poly_solid(g,z0,z1) for g in poly.geoms];v=parts[0]
  for a in parts[1:]:v=v+a
  return v
 poly=orient(poly,sign=1.0)
 paths=[list(poly.exterior.coords)[:-1]]+[list(r.coords)[:-1] for r in poly.interiors]
 return CrossSection(paths).extrude(z1-z0).translate((0,0,z0))
body=poly_solid(outline.buffer(.075,join_style=2),0,6.45)
for x0,x1,y0,y1 in COURTS:body=body-box(x0,x1,y0,y1,.20,8)
bx('authored_display_support_not_surveyed_terrain',-2,56,-2,34.85,-.30,0,4)
# Visible external and courtyard openings follow plan/elevation, pending independent local frame controls.
W=[]
def opening(n,axis,face,c,w,z0,z1,sgn=1,style='normal'):
 global body
 cut=box(c-w/2,c+w/2,face-.28,face+.28,z0,z1) if axis=='y' else box(face-.28,face+.28,c-w/2,c+w/2,z0,z1)
 body=body-cut;W.append((n,axis,face,c,w,z0,z1,sgn,style))
for fl in [0.50,3.50]:
 for i in range(6):
  opening('north_left_room','y',24.175,5.4+i*3.6,1.60,fl+1.00,fl+2.40,1)
  opening('north_right_room','y',32.925,30.6+i*3.6,1.60,fl+1.00,fl+2.40,1)
  opening('south_right_room','y',8.675,30.6+i*3.6,1.60,fl+1.00,fl+2.40,-1)
 for i in range(4):opening('south_left_room','y',-.075,5.4+i*3.6,1.60,fl+1.00,fl+2.40,-1)
 # Side-elevation W2 horizontal washing windows and W5 bathroom windows are not mirrored room windows.
 for n,x,off,sgn in [('west',-.075,0,-1),('east',54.075,8.75,1)]:
  for c in [10.55,19.10]:opening(n+'_bathroom','x',x,c+off,1.40,fl+1.10,fl+2.40,sgn)
  opening(n+'_washing_band','x',x,14.925+off,4.50,fl+1.10,fl+2.40,sgn,'band')
 # Short setback side faces: south and north bedrooms end windows read from elevations.
 for n,x,y,sgn in [('west_north',3.525,22.60,-1),('east_north',50.475,31.35,1)]:opening(n+'_room_end','x',x,y,1.50,fl+1.00,fl+2.40,sgn)
 # Windows facing the two open courts: broad glazed bays with horizontal transom, from A7/A8.
 for k,(x0,x1,y0,y1) in enumerate(COURTS):
  # each actual 3.6m module clipped to the court opening domain
  for i in range(15):
   c=1.8+3.6*i
   a=max(x0+.12,c-1.30);b=min(x1-.12,c+1.30)
   if b-a>.35:
    opening('court%d_south_gallery'%k,'y',y0,(a+b)/2,b-a,fl+(0 if fl<1 else .85),fl+2.45,1,'gallery')
    opening('court%d_north_gallery'%k,'y',y1,(a+b)/2,b-a,fl+(0 if fl<1 else .85),fl+2.45,-1,'gallery')
  for j in range(2):
   c=y0+1.75+j*3.5
   opening('court%d_west_gallery'%k,'x',x0,c,2.60,fl+(0 if fl<1 else .85),fl+2.45,1,'gallery')
   opening('court%d_east_gallery'%k,'x',x1,c,2.60,fl+(0 if fl<1 else .85),fl+2.45,-1,'gallery')
# Main south entry is recessed inside its bay. Two-storey stair glazing differs from ordinary rooms.
opening('main_entry','y',4.975,23.4,2.60,.44,2.85,-1,'door')
opening('entry_upper_window','y',4.975,23.4,2.60,4.50,5.90,-1,'band')
for n,x,y,sgn in [('west_stair',-.075,4.75,-1),('east_stair',54.075,13.50,1),('central_stair',21.675,3.8,1)]:opening(n,'x',x,y,1.45,2.00,5.90,sgn,'tall')
for n,x,y,sgn in [('west_side_door',-.075,7.85,-1),('east_side_door',54.075,16.60,1)]:opening(n,'x',x,y,1.40,.5,2.80,sgn,'door')
add('historical_closed_exterior_with_two_open_courts',body,0)
for n,axis,face,c,w,z0,z1,sgn,style in W:
 def panel(tag,u0,u1,v0,v1,d0,d1,mat):
  a,b=sorted([face+sgn*d0,face+sgn*d1])
  if axis=='y':bx(n+tag,u0,u1,a,b,v0,v1,mat)
  else:bx(n+tag,a,b,u0,u1,v0,v1,mat)
 panel('_opaque_back',c-w/2-.012,c+w/2+.012,z0-.012,z1+.012,-.32,-.10,6 if style=='door' else 5)
 fw=.10 # 0.50mm frame at 1:200; declared printing adaptation.
 for u in [c-w/2,c+w/2-fw]:panel('_jamb',u,u+fw,z0,z1,-.14,.025,3)
 for z in [z0,z1-fw]:panel('_rail',c-w/2,c+w/2,z,z+fw,-.14,.025,3)
 if style=='normal':
  panel('_center',c-fw/2,c+fw/2,z0,z1-.37,-.14,.02,3)
  for z in [z1-.37,z1-.25,z1-.13]:panel('_transom_louver',c-w/2,c+w/2,z,z+.065,-.14,.02,3)
  panel('_recessed_apron',c-w/2,c+w/2,z0-.65,z0,-.02,.01,7)
 else:
  count=max(2,round(w/.65))
  for i in range(1,count):
   u=c-w/2+i*w/count;panel('_division',u-fw/2,u+fw/2,z0,z1,-.14,.02,3)
  panel('_transom',c-w/2,c+w/2,z1-.35,z1-.25,-.14,.02,3)
  if style=='tall':panel('_stair_level_rail',c-w/2,c+w/2,3.5,3.60,-.14,.02,3)
# Thin pilasters/articulated panels calibrated from A5; not exposed structural column dimensions.
for face,x0,x1,sgn in [(24.175,3.6,25.2,1),(32.925,28.8,50.4,1),(-.075,3.6,18,-1),(8.675,28.8,50.4,-1)]:
 for x in np.arange(x0,x1+.01,3.6):
  a,b=sorted([face-sgn*.02,face+sgn*.055]);bx('facade_vertical_panel_joint',x-.045,x+.045,a,b,.15,5.90,1)
# Plan roof +50cm from wall-center datum, not +50cm from finished wall.
from shapely.geometry import box as shapely_box,Point
roofpoly=outline.buffer(.50,join_style=2)
for x0,x1,y0,y1 in COURTS:roofpoly=roofpoly.difference(shapely_box(x0,y0,x1,y1))
court_shapes=[shapely_box(x0,y0,x1,y1) for x0,x1,y0,y1 in COURTS]
roof=poly_solid(roofpoly,6.38,6.50)
# 1/100 toward courts; piecewise triangulated graphic drainage, bounded +10cm.
# Not inferred RC shape, concealed drains or a surveyed level surface.
def drainage(pt):
 if pt[2]>6.49:pt[2]=6.50+min(.10,.01*min(g.distance(Point(pt[0],pt[1])) for g in court_shapes))
 return pt
roof=roof.warp(drainage);add('roof_graphic_1percent_drainage',roof,2)
parapet=roofpoly.difference(roofpoly.buffer(-.15,join_style=2))
add('perimeter_and_court_parapet_100cm',poly_solid(parapet,6.40,7.50),0)
# Source A7: 88cm clear rooflight, 8cm seat, 30cm from slab bottom minus12cm slab.
# Drawing's shallow cap conflicts with literal R44+diameter88 semicircle.
# Choose documented graphic cap rise25cm, NOT an exact R44 reconstruction.
xc,yc=22.5,12.05
add('rooflight_seat_8cm_graphic',Manifold.cylinder(.20,.52,.52,64).translate((xc,yc,6.48)),1)
import math
r=.44;h=.25;Rcap=(r*r+h*h)/(2*h);zc=6.68+h-Rcap
rings=12;segs=64;verts=[]
for j in range(rings):
 theta=math.asin(r/Rcap)*(1-j/rings)
 rr=Rcap*math.sin(theta);zz=zc+Rcap*math.cos(theta)
 for i in range(segs):verts.append((xc+rr*math.cos(i*2*math.pi/segs),yc+rr*math.sin(i*2*math.pi/segs),zz))
verts.append((xc,yc,6.68+h));tip=len(verts)-1;verts.append((xc,yc,6.67));bottom=len(verts)-1
faces=[]
for j in range(rings-1):
 for i in range(segs):
  a=j*segs+i;b=j*segs+(i+1)%segs;c=(j+1)*segs+i;d=(j+1)*segs+(i+1)%segs;faces.extend([(a,b,c),(b,d,c)])
for i in range(segs):faces.extend([((rings-1)*segs+i,(rings-1)*segs+(i+1)%segs,tip),((i+1)%segs,i,bottom)])
from manifold3d import Mesh64
add('rooflight_shallow_cap_interpreted_not_literal_R44',Manifold(Mesh64(np.array(verts,dtype=float),np.array(faces,dtype=np.uint64))),5)
# Low entrance steps from drawing's +45cm entry, 3 shown risers; side entries +50cm simplified.
for j in range(3):bx('main_entry_three_shown_steps',22.05,24.75,4.975-(3-j)*.30,5.10,0,(j+1)*.15,1)
for x,cy,sgn in [(0,7.85,-1),(54,16.60,1)]:
 for j in range(3):
  a,b=sorted([x-sgn*.10,x+sgn*(3-j)*.30]);bx('side_entry_steps_graphic',a,b,cy-.75,cy+.75,0,(j+1)*.50/3,1)
solid=P[0]
for p in P[1:]:solid=solid+p
solid=solid.set_tolerance(0.0001).simplify(0.0001)
solid=solid.translate((-27,-16.425,.30)).scale((S,S,S))
m=solid.to_mesh64();v=np.asarray(m.vert_properties)[:,:3];f=np.asarray(m.tri_verts);materials=np.zeros(len(f),dtype=int)
for i,oid in enumerate(m.run_original_id):materials[m.run_index[i]//3:m.run_index[i+1]//3]=IDS[int(oid)]
# Normalize to STL float32 first, then collapse coincident boolean seam edges
# with Manifold at 0.00001 mm tolerance; face_id preserves source material.
from manifold3d import Mesh64
normalized=Manifold(Mesh64(v.astype(np.float32).astype(np.float64),f.astype(np.uint64),face_id=np.arange(len(f),dtype=np.uint64),tolerance=0.00001)).simplify(0.00001).to_mesh64()
materials=materials[np.asarray(normalized.face_id,dtype=int)]
v=np.asarray(normalized.vert_properties)[:,:3];f=np.asarray(normalized.tri_verts)
t=trimesh.Trimesh(v.astype(np.float32).astype(np.float64),f,process=False);t.merge_vertices(digits_vertex=8);keep=t.nondegenerate_faces();materials=materials[keep];t.update_faces(keep);t.remove_unreferenced_vertices();assert t.is_watertight and t.is_winding_consistent;assert len(t.split())==1,[(len(c.faces),c.bounds.tolist()) for c in t.split()]
np.savez_compressed(R/'mesh.npz',vertices=t.vertices,faces=t.faces,materials=materials);t.export(R/'model.stl');(R/'palette.json').write_text(json.dumps(PALETTE));(R/'components.json').write_text(json.dumps(LOG,ensure_ascii=False,indent=2))
q={'status':'PASS_GEOMETRY_ONLY','triangles':len(t.faces),'components':len(t.split()),'watertight':bool(t.is_watertight),'winding':bool(t.is_winding_consistent),'scale':'1:200','datum':'GL0; 1FL+.50; RF6.50; authoredsupportnotterrain','bounds_mm':t.bounds.tolist(),'mesh_sha256':hashlib.sha256((R/'mesh.npz').read_bytes()).hexdigest()};(R/'BUILD-QA.json').write_text(json.dumps(q,indent=2));print(json.dumps(q))
