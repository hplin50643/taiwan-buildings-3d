"""KSVCS undated warehouse alteration historical exterior, CCRH11423055.
Nominal roof340cm / ceiling257 vsderived254cm preserved; no current survey. Metres until final1:50 millimetre export.
"""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
from manifold3d import Manifold,CrossSection
R=Path(__file__).resolve().parent;P=[];LOG=[];IDS={};S=20
PALETTE=[('rendered plaster approximate','#CBC8B2'),('base mortar approximate','#A5AAA0'),('roof neutral approximation','#9C9F95'),('window wood approximate','#877B63'),('authored display base not terrain','#ADB4A2'),('opaque window backing','#526970'),('simple closed door exterior','#8C9796'),('source-visible overfired facebrick approximate','#78675E')]
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


# Historical alteration design only. Axesx0..9, mainy0..7.5; porch y-1.8..0.
# Roofskin relation is an adopted finish-layer interpretation, NOT a new source-measured maximum.
skin=lambda y:3.4375-.01*abs(y-3.75)
bx('authored_display_base',-.70,9.70,-2.40,8.50,-.20,0,4)
bx('main_floor_nominal_FL050',-.165,9.165,-.165,7.665,-.01,.50,1)
bx('cantilever_porch_platform_FL042',-.165,9.165,-1.80,.05,-.01,.42,1)
body=box(-.115,9.115,-.115,7.615,.48,3.045)
W=[]
def opening(n,axis,face,c,w,z0,z1,sgn=1,style='large'):
 global body
 if axis=='y':body=body-box(c-w/2,c+w/2,face-.24,face+.24,z0,z1)
 else:body=body-box(face-.24,face+.24,c-w/2,c+w/2,z0,z1)
 W.append((n,axis,face,c,w,z0,z1,sgn,style))
for c in [1.5,4.5]:opening('front_D','y',-.115,c,1.41,.50,2.66,-1,'door')
opening('front_W','y',-.115,7.5,2.68,1.26,3.04,-1)
for c in [1.5,4.5]:opening('rear_W','y',7.615,c,2.68,1.26,3.04,1)
opening('rear_W1','y',7.615,7.5,1.80,2.33,3.04,1,'high')
for c in [1.875,5.625]:opening('left_W1','x',-.115,c,1.80,2.33,3.04,-1,'high')
add('closed_historical_warehouse_exterior_no_storage_interior',body,0)
for n,axis,face,c,w,z0,z1,sgn,style in W:
 def panel(tag,u0,u1,v0,v1,d0,d1,mat):
  a,b=sorted([face+sgn*d0,face+sgn*d1])
  if axis=='y':bx(n+tag,u0,u1,a,b,v0,v1,mat)
  else:bx(n+tag,a,b,u0,u1,v0,v1,mat)
 door=style=='door';high=style=='high'
 panel('_opaque_back',c-w/2-.01,c+w/2+.01,z0-.01,z1+.01,-.29,-.10,6 if door else 5)
 for u in [c-w/2,c+w/2-.03]:panel('_jamb',u,u+.03,z0,z1,-.16,.04,3)
 for z,h in [(z0,.04 if not high else .06),(z1-.05,.05)]:panel('_frame_edge',c-w/2,c+w/2,z,z+h,-.16,.04,3)
 if door:
  panel('_two_closed_leaves',c-.018,c+.018,z0,z1,-.15,.025,3)
  for z in [z0+.44,z0+1.22]:panel('_source_panel_rail',c-w/2,c+w/2,z,z+.06,-.15,.025,3)
  for cc in [c-w/4,c+w/4]:
   for zz0,zz1 in [(z0+.08,z0+.40),(z0+.54,z0+1.16),(z0+1.32,z1-.18)]:panel('_simple_wood_panel',cc-w/4+.07,cc+w/4-.07,zz0,zz1,-.14,.005,6)
 else:
  for i in range(1,4):
   u=c-w/2+w*i/4;panel('_four_leaf_mullion',u-.025,u+.025,z0,z1,-.16,.04,3)
  if high:
   panel('_W1_two_row_rail',c-w/2,c+w/2,2.685,2.715,-.16,.04,3)
   # Original exteriorfinebars approximated as printable relief, not an operational/security reconstruction.
   for u in np.arange(c-w/2+.075,c+w/2,.15):panel('_external_bar_print_thickened',u-.0125,u+.0125,z0,z1,-.09,.065,3)
  else:
   panel('_transom_rail6',c-w/2,c+w/2,2.40,2.46,-.16,.04,3)
   for i in range(4):
    a=c-w/2+i*w/4;b=c-w/2+(i+1)*w/4;cc=(a+b)/2
    panel('_small_vertical',cc-.0165,cc+.0165,1.30,3.01,-.14,.025,3)
    for z in [1.30+1.10/3,1.30+2.20/3,2.46+.55/2]:panel('_small_horizontal',a,b,z-.0165,z+.0165,-.14,.025,3)
# Source-visible brick areas are localized, not a brick texture applied to every wall.
def brickpatch(n,x0,x1,z0,z1,face,sgn):
 for row,z in enumerate(np.arange(z0,z1,.12)):
  for x in np.arange(x0-.3+(row%2)*.15,x1,.30):
   a=max(x0,x+.01);b=min(x1,x+.29);c=min(z+.105,z1)
   if b>a and c>z:
    y0,y1=sorted([face+sgn*(-.02),face+sgn*.025]);bx(n,a,b,y0,y1,z,c,7)
brickpatch('front_center_door_left_brick',3.,3.795,.50,3.04,-.115,-1)
brickpatch('front_center_door_right_brick',5.205,6.,.50,3.04,-.115,-1)
brickpatch('front_center_door_head_brick',3.,6.,2.66,3.04,-.115,-1)
brickpatch('front_W_underbrick',6.,9.,.50,1.26,-.115,-1)
brickpatch('rear_two_W_underbrick',0.,6.,.50,1.26,7.615,1)
# Main36cm nominal assembly is represented externally; hidden ribs/hollowblocks omitted, not structuralsolid claim.
for lo,hi in [(-.165,3.75),(3.75,7.665)]:
 add('main_roof_external_rib_envelope',CrossSection([[(lo,3.04),(hi,3.04),(hi,skin(hi)),(lo,skin(lo))]]).extrude(9.33).rotate((90,0,90)).translate((-.165,0,0)),2)
# Front canopy is cantilevered: NO invented external columns.2+12+2finished shell16cm.
lo,hi=-1.80,-.10
add('front_cantilever_canopy_finished16',CrossSection([[(lo,skin(lo)-.16),(hi,skin(hi)-.16),(hi,skin(hi)),(lo,skin(lo))]]).extrude(9.33).rotate((90,0,90)).translate((-.165,0,0)),2)
lo,hi=-1.80,-1.70
add('front_downturned_fascia_nominal32',CrossSection([[(lo,skin(lo)-.32),(hi,skin(hi)-.32),(hi,skin(hi)),(lo,skin(lo))]]).extrude(9.33).rotate((90,0,90)).translate((-.165,0,0)),2)
# Rearprojection45 measured fromrearaxis, finished2+6+2=10; commonnominalbottom3.04.
bx('rear_lower_eave_finished10_top314_bottom304',-.165,9.165,7.64,7.95,3.04,3.14,2)

solid=P[0]
for p in P[1:]:solid=solid+p
solid=solid.simplify(0.000001)
solid=solid.translate((-4.5,-2.9,.20)).scale((S,S,S))
m=solid.to_mesh64();v=np.asarray(m.vert_properties)[:,:3];f=np.asarray(m.tri_verts);materials=np.zeros(len(f),dtype=int)
for i,oid in enumerate(m.run_original_id):materials[m.run_index[i]//3:m.run_index[i+1]//3]=IDS[int(oid)]
t=trimesh.Trimesh(v.astype(np.float32).astype(np.float64),f,process=False);t.merge_vertices(digits_vertex=8);keep=t.nondegenerate_faces();materials=materials[keep];t.update_faces(keep);t.remove_unreferenced_vertices();assert t.is_watertight and t.is_winding_consistent;assert len(t.split())==1,[(len(c.faces),c.bounds.tolist()) for c in t.split()]
np.savez_compressed(R/'mesh.npz',vertices=t.vertices,faces=t.faces,materials=materials);t.export(R/'model.stl');(R/'palette.json').write_text(json.dumps(PALETTE));(R/'components.json').write_text(json.dumps(LOG,ensure_ascii=False,indent=2))
q={'status':'PASS_GEOMETRY_ONLY','triangles':len(t.faces),'components':len(t.split()),'watertight':bool(t.is_watertight),'winding':bool(t.is_winding_consistent),'scale':'1:50','datum':'GL0; authoredsupportnotterrain','bounds_mm':t.bounds.tolist(),'mesh_sha256':hashlib.sha256((R/'mesh.npz').read_bytes()).hexdigest()};(R/'BUILD-QA.json').write_text(json.dumps(q,indent=2));print(json.dumps(q))
