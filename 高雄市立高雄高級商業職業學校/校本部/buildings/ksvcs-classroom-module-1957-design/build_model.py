"""KSVCS1957 historical classroom module, intentionally truncated at existing interface.
Only CCRH11423001; corrected FL/GL reference; no neighboring building. Metres until final1:50 millimetre export.
"""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
from manifold3d import Manifold,CrossSection
R=Path(__file__).resolve().parent;P=[];LOG=[];IDS={};S=20
PALETTE=[('rendered plaster approximate','#CBC8B2'),('base mortar approximate','#A5AAA0'),('roof neutral approximation','#9C9F95'),('window wood approximate','#877B63'),('authored display base not terrain','#ADB4A2'),('opaque window backing','#526970'),('simple closed door exterior','#8C9796'),('authored section fill NOT facade','#C2A38C')]
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


# Scoped historical classroom. x9.60 is an authored truncation, NOT facade.
bx('authored_display_base',-.95,10.0,-3.75,8.85,-.20,0,4)
bx('classroom_FL050',-.235,9.60,-.235,8.035,-.01,.50,1)
bx('corridor_FL040',-.235,9.60,-2.935,.10,-.01,.40,1)
# No neighboring building, no false gable decoration at x9.60.
roofz=lambda y:6.800-.45*abs(y-3.90)
pts=[(-.185,.48),(7.985,.48),(7.985,roofz(7.985)-.08),(3.90,6.72),(-.185,roofz(-.185)-.08)]
body=CrossSection([pts]).extrude(9.785).rotate((90,0,90)).translate((-.185,0,0))
W=[]
def opening(n,axis,face,c,w,z0,z1,sgn=1):
 global body
 if axis=='y':body=body-box(c-w/2,c+w/2,face-.25,face+.25,z0,z1)
 else:body=body-box(face-.25,face+.25,c-w/2,c+w/2,z0,z1)
 W.append((n,axis,face,c,w,z0,z1,sgn))
for c in [1.6,8.0]:opening('front_door','y',-.185,c,1.40,.50,3.30,-1)
opening('front_window','y',-.185,4.80,2.80,.55,3.30,-1)
for c in [1.6,4.8,8.0]:opening('rear_window','y',7.985,c,2.80,.55,3.30,1)
for c in [3.50,4.30]:opening('non_interface_gable_vent','x',-.185,c,.30,5.15,5.75,-1)
add('closed_exterior_body_no_interior',body,0)
# Interface cut receives only neutral section coloration; no facade details.
cutpts=[(-.185,.49),(7.985,.49),(7.985,roofz(7.985)-.079),(3.90,6.721),(-.185,roofz(-.185)-.079)]
# Cut plane is colored after boolean, without a second coincident solid.
for n,axis,face,c,w,z0,z1,sgn in W:
 def panel(tag,u0,u1,v0,v1,d0,d1,mat):
  a,b=sorted([face+sgn*d0,face+sgn*d1])
  if axis=='y':bx(n+tag,u0,u1,a,b,v0,v1,mat)
  else:bx(n+tag,a,b,u0,u1,v0,v1,mat)
 door='door' in n;vent='vent' in n
 panel('_opaque_back',c-w/2-.015,c+w/2+.015,z0-.015,z1+.015,-.30,-.10,6 if door else 5)
 for u in [c-w/2,c+w/2-.05]:panel('_jamb',u,u+.05,z0,z1,-.16,.035,3)
 for z in [z0,z1-.05]:panel('_rail',c-w/2,c+w/2,z,z+.05,-.16,.035,3)
 if vent:
  for z in np.arange(z0+.07,z1-.04,.07):panel('_louver_simplified',c-w/2,c+w/2,z,z+.025,-.14,.035,3)
 elif door:
  panel('_center',c-.025,c+.025,z0,z1,-.14,.03,3)
  for z in [1.30,2.60]:panel('_panel_transom_rail',c-w/2,c+w/2,z,z+.06,-.14,.03,3)
  for u in [c-.35,c+.35]:
   panel('_upper_leaf_glazing',u-.25,u+.25,1.40,2.52,-.13,.00,5)
   panel('_leaf_glazing_mullion',u-.015,u+.015,1.40,2.52,-.12,.025,3)
   for z in [1.75,2.10]:panel('_leaf_glazing_cross',u-.25,u+.25,z,z+.025,-.12,.025,3)
   panel('_transom_glass',u-.25,u+.25,2.70,3.20,-.13,.00,5)
   panel('_transom_cross',u-.015,u+.015,2.70,3.20,-.12,.025,3)
 else:
  # Four vertical leaves, three light rows, low boarded apron visible in elevations.
  panel('_solid_wood_apron',c-w/2,c+w/2,z0,1.10,-.16,.005,3)
  panel('_center_pair_mullion',c-.05,c+.05,z0,z1,-.15,.04,3)
  for u in [c-.70,c+.70]:panel('_leaf_divider',u-.025,u+.025,z0,z1,-.14,.035,3)
  for z in [1.10,1.82,2.54]:panel('_light_row',c-w/2,c+w/2,z,z+.05,-.14,.035,3)
  for u in np.arange(c-w/2+.08,c+w/2-.03,.14):panel('_apron_board',u,u+.025,z0,1.10,-.14,.025,3)
  for i in range(4):
   u=c-w/2+(i+.5)*w/4
   panel('_glass_vertical_bar',u-.014,u+.014,1.16,3.24,-.13,.015,3)
   for z in [1.48,2.18,2.90]:panel('_glass_horizontal_bar',u-.29,u+.29,z,z+.025,-.13,.015,3)
# Four corridor supports; last post clipped to the authored structural-axis cutoff.
cz=lambda y:4.645+.35*y
for x in [0,3.2,6.4,9.6]:
 pp=[(-2.925,.39),(-2.475,.39),(-2.475,cz(-2.475)-.06),(-2.925,cz(-2.925)-.06)]
 add('corridor_column45',CrossSection([pp]).extrude(min(x+.225,9.60)-(x-.225)).rotate((90,0,90)).translate((x-.225,0,0)),0)
pp=[(-2.925,3.40),(-2.475,3.40),(-2.475,cz(-2.475)-.06),(-2.925,cz(-2.925)-.06)]
add('corridor_outer_tie_beam',CrossSection([pp]).extrude(9.825).rotate((90,0,90)).translate((-.225,0,0)),0)
# Actual main support referenceGL5.00, nominalridgeframe6.755; skin+4.5cm interpretation.
for lo,hi in [(-.635,3.90),(3.90,8.435)]:
 za,zb=roofz(lo),roofz(hi)
 add('main_roof_skin_slope045',CrossSection([[(lo,za-.08),(hi,zb-.08),(hi,zb),(lo,za)]]).extrude(10.05).rotate((90,0,90)).translate((-.45,0,0)),2)
# Separate lower roof: written supportchain/pitch retained; skin offset within raster tolerance.
cz=lambda y:4.645+.35*y
add('corridor_roof_slope035_join4645',CrossSection([[(-3.335,cz(-3.335)-.08),(.05,cz(.05)-.08),(.05,cz(.05)),(-3.335,cz(-3.335))]]).extrude(10.05).rotate((90,0,90)).translate((-.45,0,0)),2)
# Non-interface side roof edge only. Absolutely no decorative return at x9.60.
for lo,hi in [(-.635,3.90),(3.90,8.435)]:
 beam('non_interface_roof_barge',(-.45,lo,roofz(lo)-.035),(-.45,hi,roofz(hi)-.035),.10,2)
beam('non_interface_corridor_edge',(-.45,-3.335,cz(-3.335)-.035),(-.45,.05,cz(.05)-.035),.10,2)
for y in [-.635,8.435]:bx('main_eave_fascia',-.45,9.60,y-.025,y+.025,roofz(y)-.16,roofz(y)+.003,2)
bx('corridor_eave_fascia',-.45,9.60,-3.36,-3.31,cz(-3.335)-.14,cz(-3.335),2)
# Simplified source-visible rounded cap; no ornamental motif invented. Nominaltop7.05±.15.
cap=Manifold.cylinder(10.05,.155,.155,24).rotate((0,90,0)).translate((-.45,3.9,6.895));add('ridge_cap_nominal705_graphic',cap,2)


solid=P[0]
for p in P[1:]:solid=solid+p
solid=solid.simplify(0.000001)
solid=solid.translate((-4.5,-2.55,.20)).scale((S,S,S))
m=solid.to_mesh64();v=np.asarray(m.vert_properties)[:,:3];f=np.asarray(m.tri_verts);materials=np.zeros(len(f),dtype=int)
for i,oid in enumerate(m.run_original_id):materials[m.run_index[i]//3:m.run_index[i+1]//3]=IDS[int(oid)]
materials[np.all(np.abs(v[f][:,:,0]-102)<1e-6,axis=1)]=7
t=trimesh.Trimesh(v.astype(np.float32).astype(np.float64),f,process=False);t.merge_vertices(digits_vertex=8);keep=t.nondegenerate_faces();materials=materials[keep];t.update_faces(keep);t.remove_unreferenced_vertices();assert t.is_watertight and t.is_winding_consistent;assert len(t.split())==1,[(len(c.faces),c.bounds.tolist()) for c in t.split()]
np.savez_compressed(R/'mesh.npz',vertices=t.vertices,faces=t.faces,materials=materials);t.export(R/'model.stl');(R/'palette.json').write_text(json.dumps(PALETTE));(R/'components.json').write_text(json.dumps(LOG,ensure_ascii=False,indent=2))
q={'status':'PASS_GEOMETRY_ONLY','triangles':len(t.faces),'components':len(t.split()),'watertight':bool(t.is_watertight),'winding':bool(t.is_winding_consistent),'scale':'1:50','datum':'GL0; authoredsupportnotterrain','bounds_mm':t.bounds.tolist(),'mesh_sha256':hashlib.sha256((R/'mesh.npz').read_bytes()).hexdigest()};(R/'BUILD-QA.json').write_text(json.dumps(q,indent=2));print(json.dumps(q))
