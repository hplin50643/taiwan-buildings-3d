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


# D historical exterior: source-specific orientation, not a mirrored E model.
# x increases east (24axis0 ->1axis82.8), y increases north A0->E21.9, right-handed withZup.
bx('authored_display_base_not_terrain',-2.2,95.,-2.2,24.1,-1.50,-1.20,4)
SW=box(-.135,21.735,-.135,14.035,-1.20,13.25)
SE=box(61.065,82.935,-.135,14.035,-1.20,13.25)
NC=box(14.265,68.535,7.865,22.035,-1.20,13.25)
body=SW+SE+NC
# 75.5 revisedcentraldoor: southside Caxis bay13-12, recessed from outerwall.
body=body-box(39.775,43.025,7.50,10.00,0,2.75)
W=[]
def opening(n,axis,face,c,w,z0,z1,sgn=1,style='normal'):
 global body
 cut=box(c-w/2,c+w/2,face-.30,face+.30,z0,z1) if axis=='y' else box(face-.30,face+.30,c-w/2,c+w/2,z0,z1)
 body=body-cut;W.append((n,axis,face,c,w,z0,z1,sgn,style))
for floor in range(4):
 z=floor*3.5
 for i in range(23):
  c=1.8+i*3.6;south=-.135 if i<6 or i>=17 else 7.865;north=14.035 if i<4 or i>=19 else 22.035
  if floor==0 and i in [0,22]:opening('south_end_entry','y',south,c,3.15,z,z+2.65,-1,'door')
  elif floor==0 and i==11:opening('central_revised_recessed_door','y',10.00,c,2.60,z,z+2.65,-1,'door')
  elif i in [5,17]:opening('south_bathing_high','y',south,c,3.20,z+2.10,z+2.65,-1,'high')
  else:opening('south_room_W3','y',south,c,1.40,z+.90,z+2.65,-1)
  if floor==0 and i==22:opening('north_east_end_entry','y',north,c,3.15,z,z+2.65,1,'door')
  else:opening('north_room_W3','y',north,c,1.40,z+.90,z+2.65,1)
 for n,x,y,sgn in [('west_outer_corridor_W2',-.135,6.94,-1),('west_inner_corridor_W2',14.265,14.94,-1),('east_inner_corridor_W2',68.535,14.94,1),('east_outer_corridor_W2',82.935,6.94,1)]:opening(n,'x',x,y,1.60,z+.90,z+2.65,sgn)
# Visible basement clerestories aboveGL are exterior evidence, not concealed basement reconstruction.
for i in range(23):
 c=1.8+i*3.6;south=-.135 if i<6 or i>=17 else 7.865;north=14.035 if i<4 or i>=19 else 22.035
 if i not in [0,10,11,12,22]:opening('south_visible_basement_clerestory','y',south,c,3.20,-1.10,-.55,-1,'basement')
 if i!=22:opening('north_visible_basement_clerestory','y',north,c,3.20,-1.10,-.55,1,'basement')
add('D_closed_historical_exterior_no_hidden_basement',body,0)
for side in ['south','north']:
 for i in range(24):
  x=i*3.6;face=(-.135 if i<=6 or i>=17 else 7.865) if side=='south' else (14.035 if i<=4 or i>=19 else 22.035);sgn=-1 if side=='south' else 1
  a,b=sorted([face-sgn*.03,face+sgn*.10]);bx(side+'_bay_pilaster_graphic',x-.17,x+.17,a,b,-1.20,13.22,1)
for n,axis,face,c,w,z0,z1,sgn,style in W:
 def panel(tag,u0,u1,v0,v1,d0,d1,mat):
  a,b=sorted([face+sgn*d0,face+sgn*d1])
  if axis=='y':bx(n+tag,u0,u1,a,b,v0,v1,mat)
  else:bx(n+tag,a,b,u0,u1,v0,v1,mat)
 panel('_opaque_back',c-w/2-.015,c+w/2+.015,z0-.015,z1+.015,-.35,-.11,6 if style=='door' else 5)
 fw=.15 # declared0.50mm at1:300 frame adaptation, not originaljoinerymeasurement
 for u in [c-w/2,c+w/2-fw]:panel('_frame_jamb',u,u+fw,z0,z1,-.16,.04,3)
 for zz in [z0,z1-fw]:panel('_frame_rail',c-w/2,c+w/2,zz,zz+fw,-.16,.04,3)
 if style=='normal':
  panel('_full_center_mullion',c-fw/2,c+fw/2,z0,z1,-.15,.025,3)
  panel('_upper_transom',c-w/2,c+w/2,z1-.56,z1-.41,-.15,.025,3)
  fl=round((z0-.90)/3.5)*3.5
  if axis=='y':
   for a,b in [(c-1.61,c-w/2),(c+w/2,c+1.61)]:panel('_dark_mosaic_sidepatch',a,b,fl+.10,z1,-.035,.015,7)
  else:panel('_dark_mosaic_apron',c-w/2,c+w/2,fl+.10,z0,-.035,.015,7)
 elif style in ['high','basement']:
  for u in np.linspace(c-w/2,c+w/2,7)[1:-1]:panel('_clerestory_mullion',u-fw/2,u+fw/2,z0,z1,-.15,.025,3)
  if style=='high':
   fl=round((z0-2.1)/3.5)*3.5;panel('_bath_mosaic_panel',c-w/2,c+w/2,fl+.10,z0,-.035,.015,7)
 else:
  for u in [c-w/4,c,c+w/4]:panel('_entrance_division',u-fw/2,u+fw/2,z0,z1-.5,-.15,.025,3)
  panel('_entrance_transom',c-w/2,c+w/2,z1-.58,z1-.43,-.15,.025,3)
# Roof contours are explicitly D: centralnorth; twoends south. Same-direction asymmetrical sawtooth.
def prism_yz(n,pts,x0,x1,mat=2,clip=None):
 if sum(pts[i][0]*pts[(i+1)%len(pts)][1]-pts[(i+1)%len(pts)][0]*pts[i][1] for i in range(len(pts)))<0:pts=pts[::-1]
 m=CrossSection([pts]).extrude(x1-x0).transform(((0,0,1,x0),(1,0,0,0),(0,1,0,0)))
 if clip is not None:m=m^clip
 if not m.is_empty():add(n,m,mat)
def slope_piece(n,x0,x1,y0,y1,z0,z1,wallclip):
 prism_yz(n+'_graphic16_skin',[(y0,z0-.16),(y1,z1-.16),(y1,z1),(y0,z0)],x0,x1)
 prism_yz(n+'_closed_attic_not_structural_solid',[(y0,13.18),(y1,13.18),(y1,z1-.08),(y0,z0-.08)],x0,x1,2,wallclip)
bodyplan=box(-.135,21.735,-.135,14.035,13.17,18)+box(61.065,82.935,-.135,14.035,13.17,18)+box(14.265,68.535,7.865,22.035,13.17,18)
for side,x0,x1 in [('SW',-.175,21.775),('SE',61.025,82.975)]:
 slope_piece(side+'_long_north_to_south',x0,x1,15.75,5.15,14,17.08,bodyplan)
 slope_piece(side+'_short_south',x0,x1,5.15,-1.25,15.86,14,bodyplan)
 bx(side+'_step_vertical_face',x0,x1,5.07,5.23,15.84,17.075,2)
slope_piece('north_center_long',14.225,68.575,23.15,12.55,14,17.08,bodyplan)
slope_piece('north_center_short_middle_only',21.775,61.025,12.55,6.75,15.685,14,bodyplan)
bx('north_middle_step_face',21.775,61.025,12.47,12.63,15.665,17.075,2)
for x0,x1 in [(14.225,21.775),(61.025,68.575)]:bx('north_overlap_step_to_south_long',x0,x1,12.47,12.63,14+3.2*3.08/10.6-.04,17.075,2)
# Sharedexplicit1-1/A2-22 details:23cmfalsebeams,85cmoutsidefascia,50cmUchannel (12+26+12).
GUTTER_CUTS=[]
def eave(n,x0,x1,yout,wall,ib,ie,roof_fn):
 inward=1 if wall>yout else -1;inner=yout+inward*.50;a,b=sorted([yout,inner])
 for i in range(ib,ie):
  u0=max(x0+.12,i*3.6+.115);u1=min(x1-.12,(i+1)*3.6-.115)
  if n=='SW_north_eave185':u1=min(u1,14.225-.001)
  if n=='SE_north_eave185':u0=max(u0,68.575+.001)
  if u1>u0:GUTTER_CUTS.append(box(u0,u1,a+.12,b-.12,13.27,18))
 bx(n+'_gutter_bottom12',x0,x1,a,b,13.15,13.27,2)
 for ya,yb in [(yout,yout+inward*.12),(inner-inward*.12,inner)]:
  lo,hi=sorted([ya,yb]);prism_yz(n+'_gutter_wall12',[(lo,13.16),(hi,13.16),(hi,roof_fn(hi)-.04),(lo,roof_fn(lo)-.04)],x0,x1)
 for i in range(ib,ie+1):
  x=i*3.6;lo,hi=sorted([yout,wall]);prism_yz(n+'_falsebeam23',[(lo,13.16),(hi,13.16),(hi,roof_fn(hi)-.04),(lo,roof_fn(lo)-.04)],max(x0,x-.115),min(x1,x+.115),1)
for side,x0,x1,ib,ie in [('SW',-.175,21.775,0,6),('SE',61.025,82.975,17,23)]:
 eave(side+'_north_eave185',x0,x1,15.75,13.9,ib,ie,lambda y:14+(15.75-y)*3.08/10.6)
 eave(side+'_south_eave125',x0,x1,-1.25,0,ib,ie,lambda y:14+(y+1.25)*1.86/6.4)
eave('middle_north_eave125',14.225,68.575,23.15,21.9,4,19,lambda y:14+(23.15-y)*3.08/10.6)
eave('middle_south_eave125',21.775,61.025,6.75,8,6,17,lambda y:14+(y-6.75)*1.685/5.8)
# 76.6 easternannex: southern590cm strip, NOT cross-sheetC-D letter substitution.
bx('east_annex_closed_visible_base_no_exposed_subgrade',82.80,92.80,0,5.90,-1.20,0,0)
bx('east_annex_15cm_slab',82.80,92.80,0,5.90,-.15,0,1)
bx('east_annex_south_parapet140_detail_priority',82.80,92.80,0,.10,-.02,1.40,0)
bx('east_annex_north_parapet140_detail_priority',82.80,92.80,5.80,5.90,-.02,1.40,0)
bx('east_annex_east_parapet140_detail_priority',92.70,92.80,0,5.90,-.02,1.40,0)
# Primecentralentry: landing350 fromC8; sidewings300clear+35cap; onlylocalentry, no31msharedcourt.
bx('central_prime_upper_landing350',39.775,43.025,4.50,10.02,-1.20,0,1)
for xa,xb in [(35.95,39.825),(42.975,46.85)]:
 bx('central_prime_side_landing335',xa,xb,4.65,8.01,-1.20,0,1)
 bx('central_prime_front_lowwall45',xa,xb,4.65,5.00,-.02,.45,0)
for xa,xb in [(35.90,36.10),(46.70,46.90)]:bx('central_prime_side_lowwall45',xa,xb,4.65,8.01,-.02,.45,0)
# Six treads and seven risers betweenupper0 andlowerfinishedcourt-1.05; localnetwidth3.10graphic.
bx('central_prime_lower_finish_strip_not_entire_court',39.85,42.95,2.55,2.70,-1.20,-1.05,1)
for j in range(6):bx('central_prime_six_treads_seven_risers',39.85,42.95,2.70+j*.30,4.51,-1.20,-1.05+(j+1)*.15,1)
# Centralflightcontinuous sidewalls,25cmcore/35cmcap. Slopeheight45cm is graphic coordination,
# not an independentlydimensioned every-step control. Caps extendoutwards preserving3.10netwidth.
for xa,xb,ca,cb in [(39.60,39.85,39.50,39.85),(42.95,43.20,42.95,43.30)]:
 prism_yz('central_prime_sloping_sidewall25',[(2.55,-1.2),(5.,-1.2),(5.,.45),(4.5,.45),(2.7,-.60),(2.55,-.60)],xa,xb,0)
 prism_yz('central_prime_sloping_cap35_graphic',[(2.55,-.70),(2.7,-.70),(4.5,.35),(5.,.35),(5.,.45),(4.5,.45),(2.7,-.60),(2.55,-.60)],ca,cb,1)
# ThreeDW1 endentrances: southWest directly2/A4-1, otherDW1 coordinatedsameclass, notthreeindependentdimensions.
for c,face,sgn in [(1.8,-.135,-1),(81.,-.135,-1),(81.,14.035,1)]:
 outer=face+sgn*1.65;lo,hi=sorted([outer+sgn*.15,face]);bx('end_entry_lower_finish10',c-1.625,c+1.625,lo,hi,-1.20,-1.10,1)
 for j in range(6):
  a,b=sorted([face,face+sgn*(6-j)*.275]);bx('end_entry_six_175mm_risers',c-1.625,c+1.625,a,b,-1.20,-1.10+(j+1)*.175,1)
 a,b=sorted([face-sgn*.02,face+sgn*.10]);bx('end_entry_threshold5',c-1.625,c+1.625,a,b,-.06,0,1)
# Onlythetwooutergablefive-holeclustersshownA3-2, not inventedinnerclusters.
for n,x,y in [('west_outer',-.135,3.90),('east_outer',82.935,3.90)]:
 for dy,dz in [(0,.20),(-.16,0),(.16,0),(-.10,-.18),(.10,-.18)]:add(n+'_five_vent_cluster_graphic',Manifold.cylinder(.10,.08,.08,20).rotate((0,90,0)).translate((x-.05,y+dy,15.+dz)),5)
solid=P[0]
for p in P[1:]:solid=solid+p
for cut in GUTTER_CUTS:
 cut=cut.as_original();IDS[cut.original_id()]=2;solid=solid-cut
solid=solid.set_tolerance(0.0001).simplify(0.0001)
solid=solid.translate((-46.4,-10.95,1.5)).scale((S,S,S))

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
q={'status':'PASS_GEOMETRY_ONLY','triangles':len(t.faces),'components':len(t.split()),'watertight':bool(t.is_watertight),'winding':bool(t.is_winding_consistent),'scale':'1:300','datum':'1FL0; D externalGL-1.20/courtfinish-1.05; authoredsupportnotterrain','bounds_mm':t.bounds.tolist(),'mesh_sha256':hashlib.sha256((R/'mesh.npz').read_bytes()).hexdigest()};(R/'BUILD-QA.json').write_text(json.dumps(q,indent=2));print(json.dumps(q))
