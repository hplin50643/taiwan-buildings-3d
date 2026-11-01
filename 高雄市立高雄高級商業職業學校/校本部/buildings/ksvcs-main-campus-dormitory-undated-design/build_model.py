"""KSVCS main campus single-unit dormitory undated historical design; not as-built.
Only CCRH11423034. Metres until final1:50 millimetre export.
"""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
from manifold3d import Manifold,CrossSection
R=Path(__file__).resolve().parent;P=[];LOG=[];IDS={};S=20
PALETTE=[('yellow water paint approximation','#D8CF9C'),('washed finish approximate','#8F958D'),('roof mortar approximation','#C6C6B4'),('wood frame approximation','#8E8062'),('authored base not terrain','#A7AD9D'),('opaque backed window glass','#526D70'),('exposed red brick approximate','#9A5E48')]
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

bx('authored_display_base_not_terrain',-.9,7.4,-1.65,8.1,-.20,0,4)
# Historical room footprint and open entrance porch are distinct.
foot=box(-.115,6.115,-.115,7.615,0,.45)+box(4.085,6.115,-1.115,.05,0,.40)
add('raised_main_floor45_service40',foot,1)
bx('open_front_porch40',2.70,4.20,-1.05,.05,0,.40,1)
for i,h in enumerate([.10,.25]):bx('front_entry_steps',2.70,4.20,-1.60+i*.30,-1.0,0,h,1)
bx('entry_threshold45',2.73,4.17,-.18,.02,.39,.45,1)
# Walls23cm, all windows backed for closed printable envelope.
body=box(-.115,6.115,-.115,7.615,.43,3.25)+box(4.085,6.115,-1.115,.1,.38,3.25)
# Opaque closed exterior display, interior room voids omitted.
# Open the main-to-kitchen connection; interiors are not a complete room layout.
# Internal connection omitted in closed exterior display.
W=[]
def opening(n,axis,face,c,w,z0,z1,sgn=1):
 global body
 if axis=='y':body=body-box(c-w/2,c+w/2,face-.16,face+.16,z0,z1)
 else:body=body-box(face-.16,face+.16,c-w/2,c+w/2,z0,z1)
 W.append((n,axis,face,c,w,z0,z1,sgn))
opening('front_room_W','y',-.115,1.35,2.20,1.40,3.21,-1)
opening('front_entry_D','y',-.115,3.45,1.44,.40,3.24,-1)
opening('front_kitchen_W1','y',-1.115,5.10,1.30,2.30,3.21,-1)
for c in [1.35,4.65]:opening('rear_room_W','y',7.615,c,2.20,1.40,3.21)
opening('side_room_W','x',6.115,6.15,2.20,1.40,3.21)
opening('side_bath_W1','x',6.115,3.90,1.15,2.30,3.21)
opening('side_toilet_W2','x',6.115,2.475,.55,2.30,3.21)
opening('side_kitchen_D1','x',6.115,.65,.80,.40,2.55)
add('exterior_shell_blank_opposite_side',body,0)
# 95cm exposed-red-brick lower band, split at real openings.
plinth=box(-.128,6.128,-.128,7.628,.45,1.40)+box(4.072,6.128,-1.128,.03,.40,1.35)
plinth=plinth-box(-.11,6.11,-.11,7.61,.44,1.41)-box(4.09,6.11,-1.11,.02,.39,1.40)
for n,axis,face,c,w,z0,z1,sgn in W:
 if axis=='y':plinth=plinth-box(c-w/2,c+w/2,face-.18,face+.18,z0,z1)
 else:plinth=plinth-box(face-.18,face+.18,c-w/2,c+w/2,z0,z1)
add('source_exposed_red_brick_lower_band',plinth,6)
for n,axis,face,c,w,z0,z1,sgn in W:
 def panel(tag,u0,u1,v0,v1,d0,d1,mat):
  a,b=sorted([face+sgn*d0,face+sgn*d1]);
  if axis=='y':bx(n+tag,u0,u1,a,b,v0,v1,mat)
  else:bx(n+tag,a,b,u0,u1,v0,v1,mat)
 isdoor='_D' in n
 panel('_opaque_back',c-w/2-.01,c+w/2+.01,z0-.01,z1+.01,-.22,-.075,3 if isdoor else 5)
 for u in [c-w/2,c+w/2-.055]:panel('_jamb',u,u+.055,z0,z1,-.12,.035,3)
 for z in [z0,z1-.055]:panel('_head_sill',c-w/2,c+w/2,z,z+.055,-.12,.035,3)
 if isdoor:
  if n=='front_entry_D':
   panel('_transom_opaque_glass',c-w/2+.05,c+w/2-.05,2.60,z1-.05,-.08,-.04,5)
   panel('_transom_bar',c-w/2,c+w/2,2.55,2.60,-.12,.04,3)
   panel('_side_leaf_division',c-w/2+.55-.025,c-w/2+.55+.025,z0,2.55,-.12,.04,3)
   for u in [c-w/6,c+w/6]:panel('_three_transom_lights',u-.018,u+.018,2.60,z1,-.09,.02,3)
   for u in [c-w*.35,c+w*.15]:panel('_wood_leaf_panel',u-.10,u+.10,z0+.15,z1-.80,-.09,-.03,3)
  else:
   for u in np.linspace(c-w/2+.06,c+w/2-.06,5):panel('_single_leaf_board',u-.012,u+.012,z0+.08,z1-.08,-.09,.015,3)
 else:
  cols,rows=(2,3) if n=='side_toilet_W2' else ((2,3) if 'W1' in n else (3,6))
  for u in np.linspace(c-w/2,c+w/2,cols+1)[1:-1]:panel('_vertical_muntin',u-.018,u+.018,z0,z1,-.09,.02,3)
  for k,z in enumerate(np.linspace(z0,z1,rows+1)[1:-1]):
   thick=.10 if rows==6 and k==2 else .036
   panel('_horizontal_muntin',c-w/2,c+w/2,z-thick/2,z+thick/2,-.09,.02,3)
# Roof external envelope only:36cm rib/hollow construction represented externally.
# Core roof outline follows main axes and kitchen/entry extension; eaves separately below.
roof=box(-.115,6.115,-.115,7.90,3.24,3.60)+box(4.085,6.115,-1.115,.02,3.24,3.60)
add('main_ribbed_roof_external_envelope36',roof,2)
# Side service strip remains outdoor, with6cm cantilever atGL3.24..3.30.
sideeave=box(6.08,6.43,-1.13,7.90,3.24,3.30)+box(6.40,7.0,1.95,4.80,3.24,3.30)
add('lower_side_eave6cm_drop30',sideeave,2)
# Rear perimeter follows main roof, no undocumented6cm low rear eave.
bx('front_BB_thin_canopy12_plus_finish4',-.115,4.20,-1.13,.02,3.44,3.60,2)
# Outdoor wet-area slab and basins: nominal circular vessels followplan, not rooms.
bx('outdoor_service_apron',6.10,7.0,1.95,4.80,0,.15,1)
for y in [2.50,3.35]:
 outer=Manifold.cylinder(.65,.32,.32,32).translate((6.52,y,.14));inner=Manifold.cylinder(.65,.265,.265,32).translate((6.52,y,.22));add('outdoor_round_basin_estimated',outer-inner,1)
trough=box(6.16,6.87,4.00,4.65,.14,.80)-box(6.23,6.80,4.07,4.58,.25,.84);add('outdoor_sink_graphic_estimate',trough,1)

solid=P[0]
for p in P[1:]:solid=solid+p
solid=solid.translate((-3.25,-3.3,.20)).scale((S,S,S))
m=solid.to_mesh64();v=np.asarray(m.vert_properties)[:,:3];f=np.asarray(m.tri_verts);materials=np.zeros(len(f),dtype=int)
for i,oid in enumerate(m.run_original_id):materials[m.run_index[i]//3:m.run_index[i+1]//3]=IDS[int(oid)]
t=trimesh.Trimesh(v,f,process=False);t.merge_vertices(digits_vertex=12);keep=t.nondegenerate_faces();materials=materials[keep];t.update_faces(keep);t.remove_unreferenced_vertices();assert t.is_watertight and t.is_winding_consistent;assert len(t.split())==1,[(len(c.faces),c.bounds.tolist()) for c in t.split()]
np.savez_compressed(R/'mesh.npz',vertices=t.vertices,faces=t.faces,materials=materials);t.export(R/'model.stl');(R/'palette.json').write_text(json.dumps(PALETTE));(R/'components.json').write_text(json.dumps(LOG,ensure_ascii=False,indent=2))
q={'status':'PASS_GEOMETRY_ONLY','triangles':len(t.faces),'components':len(t.split()),'watertight':bool(t.is_watertight),'winding':bool(t.is_winding_consistent),'scale':'1:50','datum':'GL0; authoredsupportnotterrain','bounds_mm':t.bounds.tolist(),'mesh_sha256':hashlib.sha256((R/'mesh.npz').read_bytes()).hexdigest()};(R/'BUILD-QA.json').write_text(json.dumps(q,indent=2));print(json.dumps(q))
