from pathlib import Path
import numpy as np,trimesh,json,hashlib
from manifold3d import Manifold,CrossSection,Mesh64
R=Path(__file__).resolve().parent;P=[];LOG=[];IDS={};S=1000/200
PALETTE=[('limewash illustrative','#D4D0BF'),('concrete illustrative','#ACAFA7'),('cement tile illustrative','#777B76'),('wood joinery illustrative','#8D8071'),('authored support not surveyed terrain','#A5AD9D'),('opaque window illustration','#607B81'),('door illustration','#8C8173')]
def box(a,b,c,d,e,f):return Manifold.cube((b-a,d-c,f-e)).translate((a,c,e))
def add(n,m,mat=0):
 assert not m.is_empty(),n
 m=m.as_original();IDS[m.original_id()]=mat;P.append(m);LOG.append({'name':n,'material':mat,'bounds_m':list(m.bounding_box())})
def bx(n,a,b,c,d,e,f,mat=0):add(n,box(a,b,c,d,e,f),mat)
def yzsolid(pts,x0,x1):
 if sum(pts[i][0]*pts[(i+1)%len(pts)][1]-pts[(i+1)%len(pts)][0]*pts[i][1] for i in range(len(pts)))<0:pts=pts[::-1]
 return CrossSection([pts]).extrude(x1-x0).transform(((0,0,1,x0),(1,0,0,0),(0,1,0,0)))
def yz(n,pts,x0,x1,mat=0):add(n,yzsolid(pts,x0,x1),mat)
# Source-local axes: x follows A1 front elevation left-to-right; y front-to-rear.
# No measured geographic bearing is claimed; original named end elevations are mapped separately.
bx('authored_display_support_not_site',-1.3,44.5,-1.25,7.0,-.35,0,4)
roof=lambda y:7.225-.45*abs(y-2.5)
body=yzsolid([(-.115,0),(5.115,0),(5.115,roof(5.115)-.06),(2.5,7.165),(-.115,roof(-.115)-.06)],-.115,43.315)
for j in range(3):
 a=14.4*j+3.85;b=14.4*j+10.55
 body=body+box(a-.115,b+.115,4.98,6.015,0,2.76)
# Source-grounded openings are inserted below before this exterior is committed.
W=[]
def opening(n,axis,face,c,w,z0,z1,sgn=1,cols=2,rows=3,door=False):
 global body
 cut=box(c-w/2,c+w/2,face-.3,face+.3,z0,z1) if axis=='y' else box(face-.3,face+.3,c-w/2,c+w/2,z0,z1)
 body=body-cut;W.append((n,axis,face,c,w,z0,z1,sgn,cols,rows,door))
# A4 six units as three mirrored pairs; A1's three-unit strip is not blindly doubled.
FRONT=[];DOORS=[]
for i in range(6):
 start=i*7.2;mirror=bool(i%2)
 X=lambda u:start+(7.2-u if mirror else u)
 for c in [1.375,5.45]:
  opening('front_first_W1','y',-.115,X(c),1.575,1.25,2.75,-1,2,3);FRONT.append(X(c))
 opening('front_D1','y',-.115,X(3.20),.90,.30,2.75,-1,1,1,True);DOORS.append((X(3.20),-.115,-1,.30))
 for c in [1.8,5.4]:opening('front_second_W1','y',-.115,X(c),1.575,4.05,5.55,-1,2,3)
 opening('rear_second_W1','y',5.115,X(1.8),1.575,4.05,5.55,1,2,3)
 for c in [4.5,6.3]:opening('rear_second_W4','y',5.115,X(c),1.53,4.825,5.55,1,3,1)
 opening('rear_kitchen_W2','y',6.015,X(4.75),1.59,1.52,2.61,1,2,2)
 opening('rear_bath_W3','y',6.015,X(6.425),1.20,1.73,2.61,1,2,3)
 opening('rear_external_D5_NOT_internal_D3','y',5.115,X(3.30),.80,.20,2.65,1,1,1,True);DOORS.append((X(3.30),5.115,1,.20))
# A0/A1 relative orientation: east is x43.2, one upstairs W1prime; west remains blank.
opening('east_end_W1prime_only','x',43.315,1.8,1.815,4.05,5.55,1,2,3)

add('six_unit_closed_historical_exterior_not_hidden_interior',body,0)
# Roof surface controls are source-derived; .12 skin is explicit numerical/printing adaptation.
for name,y0,y1 in [('front',-.43,2.5),('rear',2.5,5.43)]:
 yz(name+'_gable_roof_skin12_adaptation',[(y0,roof(y0)-.12),(y1,roof(y1)-.12),(y1,roof(y1)),(y0,roof(y0))],-.50,43.70,2)
# Non-dimensioned tile-course relief, visual approximation only; not measured tile module.
for yy in np.arange(-.30,5.4,.34):
 if abs(yy-2.5)<.16:continue
 yz('cement_tile_course_relief_graphic',[(yy,roof(yy)-.01),(yy+.035,roof(yy+.035)-.01),(yy+.035,roof(yy+.035)+.025),(yy,roof(yy)+.025)],-.49,43.69,2)
# Ridge cap image-estimated;722.5 is roof surface, not highest cap.
yz('ridge_cap_graphic_10cm_not_dimensioned',[(2.36,7.162),(2.36,7.242),(2.5,7.325),(2.64,7.242),(2.64,7.162)],-.51,43.71,2)
# Rear RC canopy has deep paired-kitchen strip and shallow doorway wings, not a single large slab.
for j in range(3):
 a=14.4*j+3.85;b=14.4*j+10.55
 bx('rear_RC_deep_roof_GL286_graphic_side450',a-.45,b+.45,4.98,5.90,2.76,2.86,1)
 bx('rear_RC_outer_overhang7_directS3',a-.45,b+.45,5.89,6.35,2.79,2.86,1)
 bx('rear_RC_D5_shallow_left_wing_graphic',a-1.25,a-.44,4.98,5.90,2.76,2.86,1)
 bx('rear_RC_D5_shallow_right_wing_graphic',b+.44,b+1.25,4.98,5.90,2.76,2.86,1)
for n,axis,face,c,w,z0,z1,sgn,cols,rows,door in W:
 def panel(tag,u0,u1,v0,v1,d0,d1,mat=3):
  a,b=sorted([face+sgn*d0,face+sgn*d1])
  if axis=='y':bx(n+tag,u0,u1,a,b,v0,v1,mat)
  else:bx(n+tag,a,b,u0,u1,v0,v1,mat)
 panel('_opaque_infill',c-w/2-.015,c+w/2+.015,z0-.015,z1+.015,-.35,-.11,6 if door else 5)
 fw=.10 # explicit .50mm frame adaptation at1:200, not original5cm joinery.
 for u in [c-w/2,c+w/2-fw]:panel('_jamb',u,u+fw,z0,z1,-.16,.04)
 for z in [z0,z1-fw]:panel('_edge_rail',c-w/2,c+w/2,z,z+fw,-.16,.04)
 if not door:
  for u in np.linspace(c-w/2,c+w/2,cols+1)[1:-1]:panel('_mullion',u-fw/2,u+fw/2,z0+.015,z1-.015,-.17,.05)
  for z in np.linspace(z0,z1,rows+1)[1:-1]:panel('_row',c-w/2,c+w/2,z-fw/2,z+fw/2,-.16,.04)
 else:
  panel('_opaque_glazed_upper_light',c-w/2+.07,c+w/2-.07,z1-.45,z1-.07,-.12,-.09,5)
  panel('_upper_transom',c-w/2,c+w/2,z1-.55,z1-.45,-.16,.04)
  for u in [c-w/6,c+w/6]:panel('_lower_vertical_door_division',u-fw/2,u+fw/2,z0+.02,z1-.47,-.17,.05)
# Front window canopies S5:50cm projection/7cm thick; doors S4:80/8cm.
# Heights use section underside2.76, not uniform guessed10cm derivedfromrear286.
for c in FRONT:bx('front_window_S5_canopy50_thickness7',c-.91,c+.91,-.50,.03,2.76,2.83,1)
for c,face,sgn,fl in DOORS:
 if sgn==-1:bx('front_door_S4_canopy80_thickness8',c-.60,c+.60,-.80,.03,2.76,2.84,1)
 # Local threshold/approach graphic only; not a construction-precise outdoor staircase.
 a,b=sorted([face,face+sgn*.32]);bx('door_threshold_approach_graphic',c-.55,c+.55,a,b,0,fl/2,1)
 a,b=sorted([face-sgn*.03,face+sgn*.15]);bx('door_upper_threshold_graphic',c-.52,c+.52,a,b,0,fl,1)
# Eave gutters are exterior graphic U profiles, not drainage-performance models.
for n,y0,y1 in [('front',-.57,-.40),('rear',5.40,5.57)]:
 trough=box(-.50,43.70,y0,y1,5.77,5.93)-box(-.52,43.72,y0+.045,y1-.045,5.835,6.1)
 add(n+'_eave_U_gutter_graphic',trough,1)
# A1/A2 downpipes are visible but diameter exaggerated from7.5 to12cm for printing.
for x in [0,7.2,14.4,21.6,28.8,36.0,43.2]:
 bx('front_rainpipe_12cm_print_adaptation',x-.06,x+.06,-.18,-.08,.05,5.95,1)

solid=P[0]
for p in P[1:]:solid=solid+p
solid=solid.set_tolerance(.0001).simplify(.0001).translate((-21.6,-2.875,.35)).scale((S,S,S))
m=solid.to_mesh64();v=np.asarray(m.vert_properties)[:,:3];f=np.asarray(m.tri_verts);materials=np.zeros(len(f),dtype=int)
for i,oid in enumerate(m.run_original_id):materials[m.run_index[i]//3:m.run_index[i+1]//3]=IDS[int(oid)]
m=Manifold(Mesh64(v.astype(np.float32).astype(np.float64),f.astype(np.uint64),face_id=np.arange(len(f),dtype=np.uint64),tolerance=.00001)).simplify(.00001).to_mesh64();materials=materials[np.asarray(m.face_id,dtype=int)]
t=trimesh.Trimesh(np.asarray(m.vert_properties)[:,:3].astype(np.float32).astype(np.float64),np.asarray(m.tri_verts),process=False);t.merge_vertices(digits_vertex=5);keep=t.nondegenerate_faces();materials=materials[keep];t.update_faces(keep);t.remove_unreferenced_vertices();assert t.is_watertight and t.is_winding_consistent and len(t.split())==1
np.savez_compressed(R/'mesh.npz',vertices=t.vertices,faces=t.faces,materials=materials);t.export(R/'model.stl');(R/'palette.json').write_text(json.dumps(PALETTE));(R/'components.json').write_text(json.dumps(LOG,ensure_ascii=False,indent=2))
q={'status':'PASS_GEOMETRY_ONLY','triangles':len(t.faces),'components':1,'watertight':bool(t.is_watertight),'winding':bool(t.is_winding_consistent),'scale':'1:200','bounds_mm':t.bounds.tolist(),'mesh_sha256':hashlib.sha256((R/'mesh.npz').read_bytes()).hexdigest()};(R/'BUILD-QA.json').write_text(json.dumps(q,indent=2));print(json.dumps(q))
