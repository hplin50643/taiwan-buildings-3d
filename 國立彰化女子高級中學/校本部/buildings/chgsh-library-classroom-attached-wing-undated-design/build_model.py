"""CHGSH historical library/classroom attached new wing; undated design, NOT present survey.
Source controls metres; display millimetres at1:150. Existing westbuilding/northrepair corridor excluded.
"""
from pathlib import Path
import json,hashlib,numpy as np,trimesh
from manifold3d import Manifold,Mesh64,CrossSection
from geometry_helpers import box
R=Path(__file__).resolve().parent;P=[];LOG=[];IDS={};S=1000/150
PALETTE=[('illustrative washed masonry','#CCC6B5'),('illustrative exposed concrete','#AEB0A8'),('illustrative cement tiles','#858A82'),('illustrative joinery','#94856F'),('authored support not terrain','#A5AD9C'),('opaque glazing illustration','#628089'),('illustrative timber door','#9E8B73'),('model interface cut NOT historical exterior wall','#76827B')]
def add(n,m,mat=0):
 assert not m.is_empty(),n
 m=m.as_original();IDS[m.original_id()]=mat;P.append(m);LOG.append({'name':n,'material':mat,'bounds_m':list(m.bounding_box())})
def bx(n,a,b,c,d,e,f,mat=0):add(n,box(a,b,c,d,e,f),mat)
def yzsolid(pts,x0,x1):
 if sum(pts[i][0]*pts[(i+1)%len(pts)][1]-pts[(i+1)%len(pts)][0]*pts[i][1] for i in range(len(pts)))<0:pts=pts[::-1]
 return CrossSection([pts]).extrude(x1-x0).transform(((0,0,1,x0),(1,0,0,0),(0,1,0,0)))
def xzsolid(pts,y0,y1):
 if sum(pts[i][0]*pts[(i+1)%len(pts)][1]-pts[(i+1)%len(pts)][0]*pts[i][1] for i in range(len(pts)))<0:pts=pts[::-1]
 return CrossSection([pts]).extrude(y1-y0).transform(((1,0,0,0),(0,0,1,y0),(0,1,0,0)))
# x westprojectjoint0 to east45; y newfrontaxis0 to back10.45. No oldcontext asnewmass.
bx('authored_display_support_not_terrain',-.8,46,-1.2,11.4,-.35,0,4)
bx('new_firstfloor_platform_GL066',0,45,-.15,10.45,0,.66,1)
# Lowerclassrooms behind2.80m southarcade; upperlibraryfullwidth.
body=box(0,45,2.8,10.45,.64,5.28)+box(0,45,.20,10.45,5.26,9.28)
W=[]
def opening(tag,face,c,w,z0,z1,side,cols=2,rows=3,door=False):
 global body
 body=body-box(c-w/2,c+w/2,face-.3,face+.3,z0,z1)
 W.append((tag,face,c,w,z0,z1,side,cols,rows,door))
# Five900cm classrooms. Each DW1 / W1 / oppositehand DW1, not identicalhand repetitions.
for room in range(5):
 a=room*9
 for face,side in [(2.8,-1),(10.45,1)]:
  opening('lower_W1_260x234',face,a+4.5,2.60,.66+.96,.66+3.30,side,4,6)
  for c,hand in [(a+1.5,-1),(a+7.5,1)]:
   # Compoundwidth231=95+6+130; handed door andwindow treated independently.
   lo=c-1.155
   dc=lo+.475 if hand==-1 else lo+2.31-.475
   wc=lo+1.01+.65 if hand==-1 else lo+.65
   opening('lower_DW1_door95',face,dc,.95,.66,.66+2.10,side,1,1,True)
   opening('lower_DW1_overdoor_transom114',face,dc,.95,.66+2.16,.66+3.30,side,2,3)
   opening('lower_DW1_sidewindow130',face,wc,1.30,.66+.96,.66+3.30,side,2,6)
for bay in range(15):
 c=bay*3+1.5
 opening('upper_south_W2_260x315',.20,c,2.60,5.28+.15,5.28+3.30,-1,4,8)
 if bay==0:
  opening('upper_north_W3_lower_opaque_panel',10.45,c,2.60,5.28+.96,5.28+3.30,1,4,6)
 else:opening('upper_north_W1',10.45,c,2.60,5.28+.96,5.28+3.30,1,4,6)
interface_door_cut=box(-.05,.32,.30,2.10,5.28,7.83)
body=body-interface_door_cut
add('new_wing_closed_room_exterior_NOT_hidden_interior',body,0)
# Printablewindowinfill with shallow recessedframes; muntins .075m scaled.50mm at1:150.
for tag,face,c,w,z0,z1,side,cols,rows,door in W:
 def panel(suf,x0,x1,zz0,zz1,d0,d1,mat):
  a,b=sorted((face+side*d0,face+side*d1));bx(tag+suf,x0,x1,a,b,zz0,zz1,mat)
 if 'W3_lower' in tag:
  panel('_lower_opaque_board',c-w/2-.02,c+w/2+.02,z0-.02,z0+1.20,-.34,-.12,6)
  panel('_upper_glazing',c-w/2-.02,c+w/2+.02,z0+1.20,z1+.02,-.34,-.12,5)
 else:panel('_infill',c-w/2-.02,c+w/2+.02,z0-.02,z1+.02,-.34,-.12,6 if door else 5)
 if door:panel('_A6_door_20x80_vision_panel',c-.10,c+.10,z0+1.10,z0+1.90,-.14,-.09,5)
 fw=.075
 for xx in [c-w/2,c+w/2-fw]:panel('_jamb',xx,xx+fw,z0,z1,-.16,.025,3)
 for zz in np.linspace(z0,z1,rows+1):panel('_rail',c-w/2,c+w/2,zz-fw/2,zz+fw/2,-.16,.025,3)
 for xx in np.linspace(c-w/2,c+w/2,cols+1)[1:-1]:panel('_mullion',xx-fw/2,xx+fw/2,z0,z1,-.16,.025,3)
# Mainroof plane derived9.58+.5*halfspan, NOTdirectly dimensionedridgecap.
roof=lambda y:12.1925-.5*abs(y-5.225)
for y0,y1 in [(-.35,5.225),(5.225,10.80)]:
 add('mainroof_15cm_shell_graphic_layers',yzsolid([(y0,roof(y0)-.15),(y1,roof(y1)-.15),(y1,roof(y1)),(y0,roof(y0))],0,45.30),2)
# Front/rear ring/fascia closes supportingedge, not a raisedextra floor.
for y0,y1 in [(-.10,.25),(10.20,10.55)]:bx('roof_support_edge_ring_graphic',0,45,y0,y1,9.10,9.55,1)
add('east_only_real_gable_blank_end',yzsolid([(0,9.20),(10.45,9.20),(10.45,roof(10.45)-.10),(5.225,12.0925),(0,roof(0)-.10)],44.80,45),0)
# Gutters sourcevisible, nominal15cm outside diameter is graphic, not a printed schedule.
for yy in [-.38,10.83]:
 gutter=Manifold.cylinder(45.3,.075,.075,24).rotate((0,90,0)).translate((0,yy,roof(yy)-.06));add('mainroof_round_gutter_graphic',gutter,2)
# No westerntriangularwall: original roof/building remains outside modeledscope.
# Theclosed lower cut face is colored as a modelboundary, not an invented exteriorgable.
bx('western_interface_cut_surface_NOT_original_wall',-.012,.012,2.8,10.45,.66,5.28,7)
add('western_interface_upper_cut_surface_NOT_original_wall',box(-.012,.012,.20,10.45,5.28,9.28)-interface_door_cut,7)
# A1/A6 D1 only, new-oldinterface not a freestandingwesternentrance; D2 remains excluded.
bx('west_interface_D1_180x255_wood_back',.13,.34,.28,2.12,5.26,7.85,6)
for yy in [.30,1.20,2.025]:bx('west_interface_D1_jamb',-.035,.18,yy,yy+.075,5.28,7.83,3)
for zz in [5.28,7.38,7.755]:bx('west_interface_D1_rail',-.035,.18,.30,2.10,zz,zz+.075,3)
for yy in [.75,1.65]:
 bx('west_interface_D1_leaf_vision_graphic',.105,.145,yy-.10,yy+.10,6.38,7.18,5)
 bx('west_interface_D1_transom',.105,.145,yy-.39,yy+.39,7.455,7.755,5)
# Roof edge/cap localgraphic estimates±10cm; coursesvisualonly.
for yy in np.arange(-.25,10.8,.36):
 if abs(yy-5.225)<.15:continue
 add('cement_tile_course_graphic_not_module_measurement',yzsolid([(yy,roof(yy)-.01),(yy+.03,roof(yy+.03)-.01),(yy+.03,roof(yy+.03)+.025),(yy,roof(yy)+.025)],0,45.30),2)
add('ridgecap_graphic_10cm_rise_NOT_printed_control',yzsolid([(5.08,12.11),(5.08,12.23),(5.225,12.2925),(5.37,12.23),(5.37,12.11)],0,45.32),2)
# Southverticalfins165 perA6,5x20cm retained; .333mm thicknessat1:150, unprintedfragile.
for bay in range(15):
 for j in range(1,12):
  x=bay*3+.20+2.60*j/12
  bx('A6_south_fin_11_per_W2_165_total',x-.025,x+.025,-.10,.10,5.26,8.60,1)
# Upperfin topbottom anchors fromfloor/ringbands, no arbitrary midspanbrackets.
bx('front_secondfloor_band_fin_anchor',0,45,-.12,.32,5.10,5.30,1)
bx('front_windowhead_fin_anchor',0,45,-.12,.32,8.56,9.28,1)
# South shallowarcades R350, crown4.18/centre.68: 2cm floor/radius-chain difference retained.
# Pillars .30x.42 andclear2.70 are A1/A2 graphic estimates±.05/.10m, not dimensionedW2width.
arcade=box(0,45,-.21,.21,.64,5.30)
for bay in range(15):
 c=bay*3+1.5;xx=np.linspace(c-1.35,c+1.35,29)
 pp=[(c-1.35,.64),(c+1.35,.64)]+[(float(x),float(.68+np.sqrt(3.5**2-(x-c)**2)))for x in xx[::-1]]
 arcade=arcade-xzsolid(pp,-.25,.25)
add('south_fifteen_R350_shallow_arcades',arcade,1)
# Fullsecondfloor slab spansopen2.8m lowercorridor; not enclosedgroundfloor.
bx('secondfloor_over_arcade',0,45,-.21,2.85,5.08,5.30,1)
for x in np.arange(0,45.01,3):
 bx('south_upper_pilaster_graphic30',max(0,x-.15),min(45,x+.15),-.21,.32,5.26,9.30,1)
# Only east end has exteriorarchedpassage. West is projectjoint, no invented closingwall.
east=box(44.80,45,-.21,2.85,.64,5.30)
yy=np.linspace(.15,2.65,29);pp=[(.15,.64),(2.65,.64)]+[(float(y),float(.68+np.sqrt(3.5**2-(y-1.4)**2)))for y in yy[::-1]]
east=east-yzsolid(pp,44.75,45.05);add('east_end_arcade_sideportal_graphic',east,1)

# NUMERICAL_FINALIZATION
solid=P[0]
for p in P[1:]:solid=solid+p
solid=solid.set_tolerance(.0001).simplify(.0001).translate((-22.5,-5.225,.35)).scale((S,S,S))
m=solid.to_mesh64();v=np.asarray(m.vert_properties)[:,:3];f=np.asarray(m.tri_verts);materials=np.zeros(len(f),dtype=int)
for i,oid in enumerate(m.run_original_id):materials[m.run_index[i]//3:m.run_index[i+1]//3]=IDS[int(oid)]
m=Manifold(Mesh64(v.astype(np.float32).astype(np.float64),f.astype(np.uint64),face_id=np.arange(len(f),dtype=np.uint64),tolerance=.00001)).simplify(.00001).to_mesh64();materials=materials[np.asarray(m.face_id,dtype=int)]
t=trimesh.Trimesh(np.asarray(m.vert_properties)[:,:3].astype(np.float32).astype(np.float64),np.asarray(m.tri_verts),process=False);t.merge_vertices(digits_vertex=5);keep=t.nondegenerate_faces();materials=materials[keep];t.update_faces(keep);t.remove_unreferenced_vertices()
np.savez_compressed(R/'mesh.npz',vertices=t.vertices,faces=t.faces,materials=materials);t.export(R/'model.stl');(R/'palette.json').write_text(json.dumps(PALETTE));(R/'components.json').write_text(json.dumps(LOG,ensure_ascii=False,indent=2))
q={'status':'WIP_NOT_FINAL_SOURCE_OR_PRINT_QA','triangles':len(t.faces),'watertight':bool(t.is_watertight),'winding':bool(t.is_winding_consistent),'scale':'1:150','bounds_mm':t.bounds.tolist(),'mesh_sha256':hashlib.sha256((R/'mesh.npz').read_bytes()).hexdigest()};(R/'BUILD-QA.json').write_text(json.dumps(q,indent=2));print(json.dumps(q))
