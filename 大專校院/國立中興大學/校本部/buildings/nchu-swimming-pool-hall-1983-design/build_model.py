from pathlib import Path
import numpy as np,trimesh,json,hashlib
from manifold3d import Manifold,CrossSection
R=Path(__file__).resolve().parent;P=[];LOG=[];IDS={};S=1000/300
PALETTE=[('cement paint approximate not verified colour','#C6C8BD'),('concrete approximate','#AAADA6'),('roof surface approximate','#969D99'),('stainless railing interpreted','#A7B2AE'),('authored display support not surveyed terrain','#98A88D'),('recess shadow approximate','#52635F'),('closed doors approximate','#75887E'),('brick surfaces approximate','#9B8C7E')]
def box(a,b,c,d,e,f):return Manifold.cube((b-a,d-c,f-e)).translate((a,c,e))
def add(n,m,mat=0):
 assert not m.is_empty(),n
 m=m.as_original();IDS[m.original_id()]=mat;P.append(m);LOG.append({'name':n,'material':mat,'bounds_m':list(m.bounding_box())})
def bx(n,a,b,c,d,e,f,mat=0):add(n,box(a,b,c,d,e,f),mat)
def yz(n,pts,x0,x1,mat=0):
 if sum(pts[i][0]*pts[(i+1)%len(pts)][1]-pts[(i+1)%len(pts)][0]*pts[i][1] for i in range(len(pts)))<0:pts=pts[::-1]
 add(n,CrossSection([pts]).extrude(x1-x0).transform(((0,0,1,x0),(1,0,0,0),(0,1,0,0))),mat)
def rail(n,axis,face,a,b,z0,z1,spacing=.42):
 # Original thin bars are widened to .15m=.50mm at1:300, and spacing relaxed for a non-tested miniature.
 w=.15
 def bar(a,b,c,d,e,f):bx(n,a,b,c,d,e,f,3)
 if axis=='x':
  for z in [z0,z1-w]:bar(a,b,face-w/2,face+w/2,z,z+w)
  for u in np.linspace(a+w/2,b-w/2,max(2,round((b-a)/spacing)+1)):bar(u-w/2,u+w/2,face-w/2-.01,face+w/2+.01,z0+.02,z1-.02)
 else:
  for z in [z0,z1-w]:bar(face-w/2,face+w/2,a,b,z,z+w)
  for u in np.linspace(a+w/2,b-w/2,max(2,round((b-a)/spacing)+1)):bar(face-w/2-.01,face+w/2+.01,u-w/2,u+w/2,z0+.02,z1-.02)
# x grows south (A->R), y grows west (1->7). GL0; no surveyed terrain.
X=[0,6,12,18,24,30,35.8,36.2,42,48,54,60,66,72,78,84,90,95]
Y=[0,5,11.5,18,24.5,31,36.7]
bx('authored_display_support_not_terrain',-3.5,98.5,-3.5,46,-.45,0,4)
bx('main_pool_hall_floor_no_hidden_pool_reconstruction',-.9,95.9,-.9,37.5,0,.8,1)
# Four unequal corner enclosures, following A2/A3. Widths/returns use explicit bays plus drawn wall edges.
T=[(-.9,6.25,-.9,5.2,'north_east'),(89.75,95.9,-.9,5.2,'south_east'),(-.9,6.25,30.8,37.5,'north_west'),(89.75,95.9,30.8,37.5,'south_west')]
for a,b,c,d,n in T:
 body=box(a,b,c,d,0,13.8)
 # A4 asymmetric doors and high stair windows; recesses are bounded exterior representations.
 if n=='north_west':
  body=body-box(a-.1,a+.22,32.3,35.7,.8,3.3)
  bx(n+'_door_recess',a+.14,a+.24,32.3,35.7,.79,3.31,6)
 if n=='south_west':
  for z in [5.0,8.25]:
   body=body-box(b-.22,b+.1,33.0,35.1,z,z+.75)
   bx(n+'_stair_window_recess',b-.24,b-.14,33,35.1,z-.01,z+.76,5)
  body=body-box(b-.22,b+.1,31.2,32.5,.8,3.0);bx(n+'_side_door',b-.24,b-.14,31.2,32.5,.79,3.01,6)
 # West long elevation only NORTH tower has two high windows; south tower west face blank. Source x south/y west are mirrored at export to right-handed XYZ.
 if n=='north_west':
  for z in [5.05,8.25]:
   body=body-box((a+b)/2-1,(a+b)/2+1,d-.22,d+.1,z,z+.70)
   bx(n+'_west_window_shadow',(a+b)/2-1,(a+b)/2+1,d-.24,d-.14,z-.01,z+.71,5)
 add('corner_tower_'+n,body,0)
# Exterior columns + horizontal lintels. Three sides are truly open, NOT giant invented glazing.
for x in X[1:-1]:
 if 6.2<x<89.8:
  bx('east_main_column',x-.22,x+.22,-.22,.22,.78,10.65,0)
  # paired narrow vertical intermediate posts visible between main bays
for a,b in zip(X[:-1],X[1:]):
 if b-a<1 or a<6 or b>90:continue
 for x in [a+(b-a)/3,a+2*(b-a)/3]:bx('east_secondary_post',x-.10,x+.10,-.13,.13,.78,10.65,0)
 rail('east_210cm_railing_print_thickened','x',0,a+.18,b-.18,.8,2.9)
bx('east_lintel',6.1,89.9,-.25,.25,9.95,10.65,0)
for x,side in [(0,'north'),(95,'south')]:
 for y in Y[1:-1]:bx(side+'_column',x-.22,x+.22,y-.22,y+.22,.78,10.65+y/36.7,0)
 for a,b in zip(Y[1:-2],Y[2:-1]):
  for y in [a+(b-a)/3,a+2*(b-a)/3]:bx(side+'_secondary_post',x-.13,x+.13,y-.10,y+.10,.78,10.65,0)
  rail(side+'_210cm_railing_print_thickened','y',x,a+.18,b-.18,.8,2.9)
 bx(side+'_lintel',x-.25,x+.25,5.05,30.95,9.95,10.65,0)
# West stand / service block. Not a full second floor across the hall.
west=box(6.0,90.0,30.95,37.5,.78,7.95)
# thirteen small horizontal service windows, omitting the entrance-covered bay.
for a,b in zip(X[:-1],X[1:]):
 if a<6 or b>90 or b-a<1:continue
 c=(a+b)/2
 if 30<c<36.3:continue
 west=west-box(c-1.05,c+1.05,37.26,37.65,3.20,3.85)
 bx('west_service_window_recess',c-1.06,c+1.06,37.20,37.30,3.19,3.86,5)
 for dx in [-.52,0,.52]:bx('west_small_window_division',c+dx-.05,c+dx+.05,37.28,37.40,3.2,3.85,3)
add('west_service_and_spectator_block_exterior',west,0)
for a,b in zip(X[:-1],X[1:]):
 if a<6 or b>90 or b-a<1:continue
 bx('west_high_bay_left_post',a-.18,a+.18,36.5,36.9,7.9,11.65,0)
 bx('west_high_opening_base',a,b,36.45,36.95,7.85,8.05,0)
 rail('west_high_30cm_guard_print_thickened','x',36.7,a+.18,b-.18,7.95,8.25,1.2)
bx('west_high_lintel',6.0,90,36.45,36.95,10.60,11.65,0)
# Roof: monoplane top11.80->12.80 (low end derived). .20 skin is graphic shell thickness, not measured construction.
y0,y1=0,36.7
roofpts=[(y0,11.60),(y1,12.60),(y1,12.80),(y0,11.80)]
yz('main_monopitch_roof_skin_graphic_20cm',roofpts,-.25,95.25,2)
# Both outer perimeter roof beams have depth120; interior roof framing deliberately not reconstructed.
for a,b in [(-.25,.25),(94.75,95.25)]:yz('end_roof_beam_120cm',[(0,10.6),(36.7,11.6),(36.7,12.8),(0,11.8)],a,b,1)
bx('east_roof_edge_beam_120cm',0,95,-.20,.20,10.6,11.8,1)
bx('west_roof_edge_beam_120cm',0,95,36.5,36.9,11.6,12.8,1)
# External 270cm high fascia is separate from roof structure; approximate thickness/profile .20m.
# Low eastern projecting gutter and tall upstand hide the lowroof edge.
yz('east_projecting_fascia_270cm', [(-1.45,10.10),(-1.65,10.35),(-1.35,12.8),(-1.15,12.8),(-1.43,10.45),(.05,10.45),(.05,10.10)],-.9,95.9,0)
# Link gutterto beam at10.55 without moving its documented outerbottom/top.
bx('east_gutter_connection',-.9,95.9,-1.40,.05,10.4,10.62,1)
bx('west_fascia_270cm',6.1,89.9,36.85,37.12,10.10,12.80,0)
# North/south projecting edge facia, plan profile unknown at smallscale: disclosed approximate .2thickness.
for a,b in [(-1.5,-1.25),(96.25,96.5)]:bx('end_external_fascia_270cm',a,b,5.0,31.0,10.10,12.80,0)
for a,b in [(-1.5,.05),(94.95,96.5)]:bx('end_fascia_bottom_soffit',a,b,5,31,10.10,10.35,1)
# Entrance: A2 firstlevel irregular 15.30m projection zone, A3 upper9.40x6.80 distinctly smaller.
# Door hall right7m,3.2mlanding,5.1m stair zone. 1FL+1.20 != mainpool+.80.
bx('entry_GL120_floor_right_hall',29.2,36.2,37.4,43.9,0,1.2,1)
bx('entry_GL120_landing',22.7,29.3,40.4,43.9,0,1.2,1)
# Six visible approach treads bounded by120rise; subdivisions graphic, not directlydimensioned.
for k in range(6):bx('entry_approach_six_graphic_treads',20.9+k*.30,22.7,40.4,43.9,0,.2*(k+1),1)
# Upper northside stairwell descends below1FL inA2. Hiddenbelowgradeflight intentionallyomitted, not fabricated.
# Low enclosure rim followsA2; basement flight/interiornotinexteriorscope.
bx('entry_stair_boundary_low_wall',20.85,26.05,40.20,40.40,0,1.3,0)
bx('entry_front_low_wall',22.65,29.25,43.72,43.95,1.18,2.30,0)
# Roof and facade above hall, roof projection9.4x6.8 fromA3.
bx('entry_roof_RF520',26.8,36.2,37.5,44.3,4.88,5.2,1)
bx('entry_front_fascia_top565',26.8,36.2,44.10,44.3,4.88,5.65,0)
bx('entry_north_fascia_top565',26.8,27.0,37.4,44.3,4.88,5.65,0)
bx('entry_south_fascia_top565',36.0,36.2,37.4,44.3,4.88,5.65,0)
for x in [29.2,36.1]:
 for y in [37.5,43.85]:bx('entry_column_graphic',x-.15,x+.15,y-.15,y+.15,1.18,4.9,0)
bx('entry_closed_south_wall',36.0,36.2,37.4,43.9,1.18,4.9,0)
bx('entry_closed_exterior_solid_no_hidden_interior',29.25,36.1,37.4,43.8,1.18,4.9,0)
# Two double-door groups face north (fixed x29.2), not the west-facing outer wall.
bx('entry_west_solid_wall',29.2,36.2,43.7,43.9,1.18,4.9,0)
bx('entry_north_wall_return_near',29.1,29.3,37.4,38.8,1.18,4.9,0)
bx('entry_north_wall_return_far',29.1,29.3,42.7,43.9,1.18,4.9,0)
bx('entry_north_header',29.1,29.3,38.7,42.8,4.35,4.9,0)
bx('entry_north_two_double_doors',29.14,29.30,38.75,42.75,1.18,4.38,5)
for y in np.linspace(38.8,42.7,5):bx('entry_north_door_division',29.04,29.24,y-.07,y+.07,1.18,4.4,3)
bx('entry_north_transom',29.04,29.24,38.75,42.75,3.45,3.60,3)
# Texturemarkings/materialcolour estimates only; noauthorclaims currentcondition or printtestedmodel.

solid=P[0]
for p in P[1:]:solid=solid+p
solid=solid.set_tolerance(0.0001).simplify(0.0001)
solid=solid.translate((-47.5,-21.25,.45)).scale((S,-S,S))
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
q={'status':'PASS_GEOMETRY_ONLY','triangles':len(t.faces),'components':len(t.split()),'watertight':bool(t.is_watertight),'winding':bool(t.is_winding_consistent),'scale':'1:300','datum':'GL0; poolFL+.80; entryFL+1.20; towers13.80; authoredsupportnotterrain','bounds_mm':t.bounds.tolist(),'mesh_sha256':hashlib.sha256((R/'mesh.npz').read_bytes()).hexdigest()};(R/'BUILD-QA.json').write_text(json.dumps(q,indent=2));print(json.dumps(q))
