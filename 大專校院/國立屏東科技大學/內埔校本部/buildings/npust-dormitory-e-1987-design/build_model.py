from pathlib import Path
import numpy as np,trimesh,json,hashlib
from manifold3d import Manifold,CrossSection
R=Path(__file__).resolve().parent;P=[];LOG=[];IDS={};S=1000/300
PALETTE=[('light mosaic approximate','#C9C7B7'),('concrete approximate','#AAAFA6'),('roof finish approximate','#B7B8AA'),('window frame approximate','#A6ABA5'),('authored display support not surveyed terrain','#A3AD9B'),('opaque glazing illustration','#546D75'),('closed entrance approximation','#737C79'),('dark mosaic approximate','#858675')]
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


# E historical exterior, same-package entrance completion from directly linked prime details.
# x0axis24,x82.8axis1; normalizedyA0,B8,C13.9,topE21.9(roofcallsitD).
bx('authored_display_base_not_terrain',-2.2,85.,-2.2,24.1,-1.50,-1.20,4)
NW=box(-.135,21.735,7.865,22.035,-1.20,13.25)
NE=box(61.065,82.935,7.865,22.035,-1.20,13.25)
SC=box(14.265,68.535,-.135,14.035,-1.20,13.25)
body=NW+NE+SC
# Firstfloor13-12bay is actual recessed porch from75.5plan, NOT a flush ordinarywindow.
body=body-box(39.775,43.025,11.90,14.40,0,2.75)
W=[]
def opening(n,axis,face,c,w,z0,z1,sgn=1,style='normal'):
 global body
 cut=box(c-w/2,c+w/2,face-.30,face+.30,z0,z1) if axis=='y' else box(face-.30,face+.30,c-w/2,c+w/2,z0,z1)
 body=body-cut;W.append((n,axis,face,c,w,z0,z1,sgn,style))
for floor in range(4):
 z=floor*3.5
 for i in range(23):
  c=1.8+i*3.6;front=7.865 if i<4 or i>=19 else -.135;back=22.035 if i<6 or i>=17 else 14.035
  opening('south_room','y',front,c,1.50,z+.95,z+2.65,-1)
  if floor==0 and i in [0,22]:opening('north_end_entry','y',back,c,3.15,z,z+2.65,1,'door')
  elif floor==0 and i==11:opening('central_revised_recessed_door','y',11.90,c,2.60,z,z+2.65,1,'door')
  elif i in [5,17]:opening('north_bathing_high','y',back,c,3.10,z+2.20,z+2.70,1,'high')
  else:opening('north_room','y',back,c,1.50,z+.95,z+2.65,1)
 for n,x,y,sgn in [('west_outer_corridor',-.135,15.10,-1),('west_inner_corridor',14.265,6.80,-1),('east_inner_corridor',68.535,6.80,1),('east_outer_corridor',82.935,15.10,1)]:opening(n,'x',x,y,1.55,z+.95,z+2.65,sgn)
# Only the uncancelled western three-bay basement has visible south clerestories.
for c in [1.8,5.4,9.0]:opening('south_west_visible_basement_clerestory','y',7.865,c,3.20,-1.10,-.55,-1,'clerestory')
add('closed_E_historical_exterior_no_hidden_basement_interior',body,0)
# Readvisiblefacadepierwidthapprox.34; notstructuraldimension claim.
for side in ['south','north']:
 for i in range(24):
  x=i*3.6;face=(7.865 if i<=4 or i>=19 else -.135) if side=='south' else (22.035 if i<=6 or i>=17 else 14.035);sgn=-1 if side=='south' else 1
  a,b=sorted([face-sgn*.03,face+sgn*.10]);bx(side+'_bay_pilaster_estimated',x-.17,x+.17,a,b,-1.20,13.22,1)
for n,axis,face,c,w,z0,z1,sgn,style in W:
 def panel(tag,u0,u1,v0,v1,d0,d1,mat):
  a,b=sorted([face+sgn*d0,face+sgn*d1])
  if axis=='y':bx(n+tag,u0,u1,a,b,v0,v1,mat)
  else:bx(n+tag,a,b,u0,u1,v0,v1,mat)
 panel('_opaque_back',c-w/2-.015,c+w/2+.015,z0-.015,z1+.015,-.35,-.11,6 if style=='door' else 5)
 fw=.15 # printadaptation.50mmat1:300, notsourcejoinerysize.
 for u in [c-w/2,c+w/2-fw]:panel('_frame_jamb',u,u+fw,z0,z1,-.16,.04,3)
 for zz in [z0,z1-fw]:panel('_frame_rail',c-w/2,c+w/2,zz,zz+fw,-.16,.04,3)
 if style=='normal':
  panel('_lower_center_mullion',c-fw/2,c+fw/2,z0,z1-.48,-.15,.025,3)
  panel('_transom_rail',c-w/2,c+w/2,z1-.56,z1-.41,-.15,.025,3)
  fl=round((z0-.95)/3.5)*3.5
  if axis=='y':
   for a,b in [(c-1.61,c-w/2),(c+w/2,c+1.61)]:panel('_dark_mosaic_sidepatch',a,b,fl+.10,z1,-.035,.015,7)
  else:panel('_dark_mosaic_apron',c-w/2,c+w/2,fl+.10,z0,-.035,.015,7)
 elif style=='clerestory':
  for u in np.linspace(c-w/2,c+w/2,7)[1:-1]:panel('_clerestory_mullion',u-fw/2,u+fw/2,z0,z1,-.15,.025,3)
 elif style=='high':
  for u in np.arange(c-w/2+.50,c+w/2,.50):panel('_clerestory_mullion',u-fw/2,u+fw/2,z0,z1,-.15,.025,3)
  fl=round((z0-2.2)/3.5)*3.5;panel('_bath_mosaic_panel',c-w/2,c+w/2,fl+.10,z0,-.035,.015,7)
 else:
  for u in [c-w/4,c,c+w/4]:panel('_entrance_division',u-fw/2,u+fw/2,z0,z1-.5,-.15,.025,3)
  panel('_entrance_transom',c-w/2,c+w/2,z1-.58,z1-.43,-.15,.025,3)
# Outerendstairs visiblypresent; simplifiedequalrisers fromdrawingGL difference.
# Central prime entry added separately below after its profile helper.
for c in [1.8,81.0]:
 for j in range(6):bx('outer_end_entry_steps_interpreted',c-1.62,c+1.62,22.00,22.035+(6-j)*.30,-1.20,-1.20+(j+1)*.20,1)
# Thinroofskins and closedattics are separate from the exterior85cmdownstand and23cmfalsebeams.
def prism_yz(n,pts,x0,x1,mat=2,clip=None):
 if sum(pts[i][0]*pts[(i+1)%len(pts)][1]-pts[(i+1)%len(pts)][0]*pts[i][1] for i in range(len(pts)))<0:pts=pts[::-1]
 m=CrossSection([pts]).extrude(x1-x0).transform(((0,0,1,x0),(1,0,0,0),(0,1,0,0)))
 if clip is not None:m=m^clip
 if not m.is_empty():add(n,m,mat)
# E prime detail: north-facing C=13.90. E measured placement is 3.50m +/-0.10,
# NOT a claim that the D printed350/545 dimension directly applies to E.
# Reference-coordinate helper maps this independently calibrated local entry northwards.
def entry_bx(n,a,b,c,d,e,f,mat=0):bx(n,a,b,21.9-d,21.9-c,e,f,mat)
def entry_prism(n,pts,x0,x1,mat=0):prism_yz(n,[(21.9-y,z) for y,z in pts],x0,x1,mat)
entry_bx('central_prime_upper_landing350_PLAN_MEASURED',39.775,43.025,4.50,10.02,-1.20,0,1)
for xa,xb in [(35.95,39.825),(42.975,46.85)]:
 entry_bx('central_prime_side_landing335',xa,xb,4.65,8.01,-1.20,0,1)
 entry_bx('central_prime_front_lowwall45',xa,xb,4.65,5.00,-.02,.45,0)
for xa,xb in [(35.90,36.10),(46.70,46.90)]:entry_bx('central_prime_side_lowwall45',xa,xb,4.65,8.01,-.02,.45,0)
# Six treads and seven risers betweenupper0 andlowerfinishedcourt-1.05; localnetwidth3.10graphic.
entry_bx('central_prime_lower_finish_strip_not_entire_court',39.85,42.95,2.55,2.70,-1.20,-1.05,1)
for j in range(6):entry_bx('central_prime_six_treads_seven_risers',39.85,42.95,2.70+j*.30,4.51,-1.20,-1.05+(j+1)*.15,1)
# Centralflightcontinuous sidewalls,25cmcore/35cmcap. Slopeheight45cm is graphic coordination,
# not an independentlydimensioned every-step control. Caps extendoutwards preserving3.10netwidth.
for xa,xb,ca,cb in [(39.60,39.85,39.50,39.85),(42.95,43.20,42.95,43.30)]:
 entry_prism('central_prime_sloping_sidewall25',[(2.55,-1.2),(5.,-1.2),(5.,.45),(4.5,.45),(2.7,-.60),(2.55,-.60)],xa,xb,0)
 entry_prism('central_prime_sloping_cap35_graphic',[(2.55,-.70),(2.7,-.70),(4.5,.35),(5.,.35),(5.,.45),(4.5,.45),(2.7,-.60),(2.55,-.60)],ca,cb,1)

def slope_piece(n,x0,x1,y0,y1,z0,z1,wallclip):
 # .16m is declared graphic/print representation, notknownstructuralslabthickness.
 prism_yz(n+'_estimated16_skin',[(y0,z0-.16),(y1,z1-.16),(y1,z1),(y0,z0)],x0,x1)
 prism_yz(n+'_closed_attic_not_structural_solid',[(y0,13.18),(y1,13.18),(y1,z1-.08),(y0,z0-.08)],x0,x1,2,wallclip)
bodyplan=box(-.135,21.735,7.865,22.035,13.17,18)+box(61.065,82.935,7.865,22.035,13.17,18)+box(14.265,68.535,-.135,14.035,13.17,18)
for side,x0,x1 in [('NW',-.175,21.775),('NE',61.025,82.975)]:
 slope_piece(side+'_long',x0,x1,6.15,16.75,14,17.08,bodyplan)
 slope_piece(side+'_short',x0,x1,16.75,23.15,15.86,14,bodyplan)
 # .16thickverticalstepface closes visible attic edge whereoutsidewall.
 bx(side+'_step_vertical_face',x0,x1,16.67,16.83,15.84,17.075,2)
slope_piece('south_center_long',14.225,68.575,-1.25,9.35,14,17.08,bodyplan)
# Critical: southernshortplaneONLYbetweenNwings; overlapzonesdropontoNlongplaneperA4-7.
slope_piece('south_center_short_middle_only',21.775,61.025,9.35,15.15,15.685,14,bodyplan)
bx('south_middle_step_face',21.775,61.025,9.27,9.43,15.665,17.075,2)
for x0,x1 in [(14.225,21.775),(61.025,68.575)]:
 # Otherroofat9.35:14+(9.35-6.15)*3.08/10.6, explicitintersectionnotanotherfullshortroof.
 bx('south_overlap_step_to_north_long',x0,x1,9.27,9.43,14+3.2*3.08/10.6-.04,17.075,2)
# Fascia/gutter50cm width: outer12, inner12 andbottom12,26cm openchannel.
GUTTER_CUTS=[]
def eave(n,x0,x1,yout,wall,axis_start,axis_end,roof_fn):
 inward=1 if wall>yout else -1;inner=yout+inward*.50
 a,b=sorted([yout,inner])
 for i in range(axis_start,axis_end):
  u0=max(x0+.12,i*3.6+.115);u1=min(x1-.12,(i+1)*3.6-.115)
  # Northern low eave hidden below southern roof in overlap: no through-cut there.
  if n=='NW_south_eave185':u1=min(u1,14.225-.001)
  if n=='NE_south_eave185':u0=max(u0,68.575+.001)
  if u1>u0:GUTTER_CUTS.append(box(u0,u1,a+.12,b-.12,13.27,18))
 bx(n+'_gutter_bottom12',x0,x1,a,b,13.15,13.27,2)
 for ya,yb in [(yout,yout+inward*.12),(inner-inward*.12,inner)]:
  lo,hi=sorted([ya,yb]);prism_yz(n+'_gutter_wall12',[(lo,13.16),(hi,13.16),(hi,roof_fn(hi)-.04),(lo,roof_fn(lo)-.04)],x0,x1)
 for i in range(axis_start,axis_end+1):
  x=i*3.6
  lo,hi=sorted([yout,wall]);prism_yz(n+'_falsebeam23',[(lo,13.16),(hi,13.16),(hi,roof_fn(hi)-.04),(lo,roof_fn(lo)-.04)],max(x0,x-.115),min(x1,x+.115),1)
for side,x0,x1,ib,ie in [('NW',-.175,21.775,0,6),('NE',61.025,82.975,17,23)]:
 eave(side+'_south_eave185',x0,x1,6.15,8,ib,ie,lambda y:14+(y-6.15)*3.08/10.6)
 eave(side+'_north_eave125',x0,x1,23.15,21.9,ib,ie,lambda y:14+(23.15-y)*1.86/6.4)
eave('middle_south_eave125',14.225,68.575,-1.25,0,4,19,lambda y:14+(y+1.25)*3.08/10.6)
eave('middle_north_eave125',21.775,61.025,15.15,13.9,6,17,lambda y:14+(15.15-y)*1.685/5.8)
# Gableventshallowfivecircles, onlyexternalrelief; hiddenventilationomitted.
for n,x,y in [('NW',-.135,15.6),('NE',82.935,15.6),('SW',14.265,8.05),('SE',68.535,8.05)]:
 for dy,dz in [(0,.38),(-.20,.06),(.20,.06),(-.13,-.23),(.13,-.23)]:add('gable_'+n+'_vent_shallow',Manifold.cylinder(.10,.11,.11,24).rotate((0,90,0)).translate((x-.05,y+dy,15.85+dz)),5)
solid=P[0]
for p in P[1:]:solid=solid+p
# Shared detail: open26cm gutter, segmented by E bay ribs; no hidden pipes modeled.
for cut in GUTTER_CUTS:
 cut=cut.as_original();IDS[cut.original_id()]=2;solid=solid-cut
solid=solid.set_tolerance(0.0001).simplify(0.0001)
solid=solid.translate((-41.4,-10.95,1.5)).scale((S,S,S))
m=solid.to_mesh64();v=np.asarray(m.vert_properties)[:,:3];f=np.asarray(m.tri_verts);materials=np.zeros(len(f),dtype=int)
for i,oid in enumerate(m.run_original_id):materials[m.run_index[i]//3:m.run_index[i+1]//3]=IDS[int(oid)]
# Normalize to STL float32 first, then collapse coincident boolean seam edges
# with Manifold at 0.00001 mm tolerance; face_id preserves source material.
from manifold3d import Mesh64
normalized=Manifold(Mesh64(v.astype(np.float32).astype(np.float64),f.astype(np.uint64),face_id=np.arange(len(f),dtype=np.uint64),tolerance=0.00001)).simplify(0.00001).to_mesh64()
materials=materials[np.asarray(normalized.face_id,dtype=int)]
v=np.asarray(normalized.vert_properties)[:,:3];f=np.asarray(normalized.tri_verts)
t=trimesh.Trimesh(v.astype(np.float32).astype(np.float64),f,process=False);t.merge_vertices(digits_vertex=5);keep=t.nondegenerate_faces();materials=materials[keep];t.update_faces(keep);t.remove_unreferenced_vertices();assert t.is_watertight and t.is_winding_consistent;assert len(t.split())==1,[(len(c.faces),c.bounds.tolist()) for c in t.split()]
np.savez_compressed(R/'mesh.npz',vertices=t.vertices,faces=t.faces,materials=materials);t.export(R/'model.stl');(R/'palette.json').write_text(json.dumps(PALETTE));(R/'components.json').write_text(json.dumps(LOG,ensure_ascii=False,indent=2))
q={'status':'PASS_GEOMETRY_ONLY','triangles':len(t.faces),'components':len(t.split()),'watertight':bool(t.is_watertight),'winding':bool(t.is_winding_consistent),'scale':'1:300','datum':'1FL0; E drawingGL-1.20, authoredsupportnotterrain','bounds_mm':t.bounds.tolist(),'mesh_sha256':hashlib.sha256((R/'mesh.npz').read_bytes()).hexdigest()};(R/'BUILD-QA.json').write_text(json.dumps(q,indent=2));print(json.dumps(q))
