"""Kungtung original school and chapel: late1958 exterior reconstruction.
Units metres, 1FL=0; x0 stair end, y0 west arcade. NOT a present survey.
Historic local grades -.81/-.84 are not flattened into invented terrain.
"""
from pathlib import Path
import json,hashlib,numpy as np,trimesh
from manifold3d import Manifold,Mesh64,CrossSection
from geometry_helpers import box,prism
R=Path(__file__).resolve().parent
S=5.;SHIFT=.65;P=[];LOG=[];IDS={}
PALETTE=[('illustrative exposed concrete','#BDB9AB'),('illustrative slab concrete','#AAA89D'),('illustrative roof finish','#858982'),('print-thickened metal frames','#747F7A'),('authored display support NOT terrain','#A7AE9B'),('opaque glazing illustration','#719297'),('illustrative masonry','#B4A18C')]
def add(n,m,mat=0):
 assert not m.is_empty(),n
 m=m.as_original();IDS[m.original_id()]=mat;P.append(m);LOG.append({'name':n,'material':mat,'bounds_m':list(m.bounding_box())})
def bx(n,a,b,c,d,e,f,mat=0):add(n,box(a,b,c,d,e,f),mat)
def yz(pts,x0,x1):
 if sum(pts[i][0]*pts[(i+1)%len(pts)][1]-pts[(i+1)%len(pts)][0]*pts[i][1] for i in range(len(pts)))<0:pts=pts[::-1]
 return CrossSection([pts]).extrude(x1-x0).transform(((0,0,1,x0),(1,0,0,0),(0,1,0,0)))
def xz(pts,y0,y1):
 if sum(pts[i][0]*pts[(i+1)%len(pts)][1]-pts[(i+1)%len(pts)][0]*pts[i][1] for i in range(len(pts)))<0:pts=pts[::-1]
 return CrossSection([pts]).extrude(y1-y0).transform(((1,0,0,0),(0,0,1,y0),(0,1,0,0)))
# Authoredsupport top-.05 near lowest stairdatum-.04; explicitly not historical site paving.
bx('authored_display_support_not_measured_terrain',-1.1,32.57,-1.0,11.19,-SHIFT,-.05,4)
bx('ground_floor_platform',0,31.47,0,10.19,-.10,0,1)
# Mainrooms recessed behind west open galleries and east brise-soleil.
body=box(5.82,31.30,1.25,9.27,-.06,9.43)+box(22.80,25.80,0,1.30,-.06,9.68)
bx('stair_short_end_solid_wall',0,.30,0,10.19,-.06,9.69,0)
bx('far_short_end_solid_wall',31.22,31.47,0,10.19,-.06,9.69,0)
# Floorstairwell remains open: no boundingbox filled through flightvoids.
for z in [3.45,6.55,9.68]:
 slab=box(.01,31.46,0,10.19,z-.25,z)-box(.30,4.62,3.83,6.72,z-.3,z+.1)
 add('floor_slab_'+str(z),slab,1)
for z0,z1 in [(0,3.45),(3.45,6.55),(6.55,9.68)]:
 for x in [5.82,8.665,11.575,14.395,17.215,20.025,22.845,25.665,28.55,31.32]:
  bx('west_arcade_column',x-.125,x+.125,0,.25,z0-.02,z1,0)
 # Sourceeast10x40fins50pieces, thickenedto.12width for .60mm at1:200.
 for i in range(50):
  x=6.37+.50*i;bx('east_brise_soleil_fin',x-.06,x+.06,9.62,10.02,z0-.02,z1,0)
for z in [3.43,6.53]:
 bx('west_arcade_guardwall',5.78,31.47,0,.15,z-.03,z+1.14,0)
# Upperterraces are open overhead, surrounded by tall perforated screens; not roofed rooms.
for x0,x1 in [(0,.25),(31.22,31.47)]:bx('top_terrace_short_end_screen',x0,x1,0,10.19,9.66,12.89,0)
for y0,y1 in [(0,.25),(9.94,10.19)]:
 for a,b in [(0,8.865),(25.54,31.47)]:bx('top_terrace_long_screen',a,b,y0,y1,9.66,12.89,0)
# Chapel closed shell below roofs; no invented interior furnishings.
chapel=box(8.665,25.79,0,10.19,9.66,12.78)-box(8.915,25.54,.25,9.94,9.70,13)
add('chapel_low_external_shell',chapel,0)
# Late roofplan has a westshoulder in towerbay, not an unintended long black gap.
add('tower_bay_west_roof_shoulder',yz([(0,12.71),(2.05,12.71+2.05*1.22/8.04),(2.05,12.89+2.05*1.22/8.04),(0,12.89)],22.93,25.79),2)
# East altar strip 1.90 clear, late3/1 reference. Main highskin14.11 NOT14.22.
roofhighy=8.04
add('chapel_main_single_slope_roof',yz([(0,12.71),(roofhighy,13.93),(roofhighy,14.11),(0,12.89)],8.665,22.945),2)
add('altar_strip_graphical_microslope1288_to1280',yz([(roofhighy,12.70),(10.19,12.62),(10.19,12.80),(roofhighy,12.88)],8.665,25.79),2)
# Clerestory glazing only in source strip, not allfacades.
bx('east_clerestory_infill',8.865,22.745,roofhighy-.045,roofhighy+.045,13.04,13.76,5)
bx('clerestory_lower_spandrel',8.84,22.77,roofhighy-.08,roofhighy+.08,12.80,13.05,0)
bx('clerestory_upper_spandrel',8.84,22.77,roofhighy-.08,roofhighy+.08,13.75,14.02,0)
for group in range(5):
 a=8.865+group*(22.745-8.865)/5;b=8.865+(group+1)*(22.745-8.865)/5
 for x in [a,a+.45,b-.45,b]:bx('clerestory_five_groups_sidevents',x-.045,x+.045,roofhighy-.08,roofhighy+.08,13.03,13.77,3)
for z in [13.05,13.75]:bx('clerestory_horizontal_frame',8.84,22.77,roofhighy-.08,roofhighy+.08,z-.045,z+.045,3)
# Endroof wedgewalls, below main slope and above12.78shell.
for x0,x1 in [(8.665,8.865),(22.745,22.945)]:add('chapel_sloping_roof_end_wall',yz([(0,12.76),(roofhighy,12.76),(roofhighy,14.02),(0,12.80)],x0,x1),0)
bx('stair_canopy_own_1278_datum',0,5.82,3.83,6.72,12.35,12.78,2)
# Externalstair selectedlate3/3: first L-run20risers (11+9), upper18 (9+9).
# Functionalstairs are solid stepped shells with sloped undersides, no internalbuildingstairs.
def flight(n,axis,lo,hi,across0,across1,z0,z1,count):
 step=(hi-lo)/count;rise=(z1-z0)/count
 pts=[(lo,z0-.16),(hi,z1-.16),(hi,z1)]
 for i in range(count-1,-1,-1):pts.extend([(lo+i*step,z0+(i+1)*rise),(lo+i*step,z0+i*rise)])
 m=xz(pts,across0,across1) if axis=='x' else yz(pts,across0,across1)
 add(n,m,1)
# Firstflight fromnear1.15y up to centralturn, then xreturn tofloorcorridor.
# Elevenrisers/ten28cmtreads, not2.8/11 equal treaddepth.
top=[(1.15,-.04),(1.15,-.04+.1735)]
for i in range(1,11):top.extend([(1.15+i*.28,-.04+i*.1735),(1.15+i*.28,-.04+(i+1)*.1735)])
add('first_L_11_risers_10_treads28cm',yz([(1.15,-.20),(3.95,1.7085)]+top[::-1],.90,2.10),1)
bx('first_turn_platform',.90,2.115,3.935,5.40,1.7085,1.8685,1)
flight('first_upper_return_9_risers','x',2.10,4.62,3.95,5.15,1.8685,3.43,9)
for label,z0,z1 in [('to_third',3.43,6.53),('to_chapel_terrace',6.53,9.73)]:
 mid=(z0+z1)/2
 # lower goes x4.62 toward2.10; mirror rising profile along x.
 pts=[(2.10,mid-.16),(4.62,z0-.16),(4.62,z0)]
 for i in range(9):pts.extend([(4.62-i*.28,z0+(i+1)*(mid-z0)/9),(4.62-(i+1)*.28,z0+(i+1)*(mid-z0)/9)])
 add(label+'_lower_return9',xz(pts,5.40,6.60),1)
 bx(label+'_turn',.90,2.115,3.935,6.60,mid-.17,mid,1)
 flight(label+'_upper_return9','x',2.10,4.62,3.95,5.15,mid,z1,9)
# Staircentral spine and landings anchoredtofloor shell.
bx('stair_central_spine',2.10,4.62,5.15,5.40,-.06,12.36,0)
for z in [3.43,6.53,9.73]:bx('stair_floor_landing',4.59,5.87,3.83,6.72,z-.19,z+.005,1)
# Late bell tower: inclined open frame, not a rectangular solid tower.
# Profile trace MSMG plus M6MG3-3, graphical envelope uncertainty±.35m.
add('tower_right_inclined_wall',xz([(25.60,12.72),(25.80,12.72),(26.696,17.85),(26.49,17.78)],2.05,8.25),0)
add('tower_sloped_top_cap',xz([(22.59,16.79),(26.69,17.64),(26.696,17.85),(22.611,17.0)],2.05,8.25),0)
# Diagonal pierced panel carries16columns x7rows; holes are NOT glazing.
# x(z) interpolates printedlate profile; lower invisible continuation ties into mainroof.
def px(z):return 22.611+(17-z)*(25.797-22.611)/(17-12.89)
panel=xz([(px(12.72)-.1,12.72),(px(12.72)+.1,12.72),(22.711,17),(22.511,17)],2.05,8.25)
for row in range(7):
 for col in range(16):
  z=14.20+row*.36;y=2.32+col*.352
  panel=panel-box(px(z+.28)-.3,px(z)+.3,y,y+.25,z,z+.26)
add('tower_diagonal_true_lattice_panel_112_apertures',panel,0)
# Side frame struts, shownopen inlatewest view. No duplicated reinforcementtick geometry.
for y in [2.05,8.05]:
 add('tower_left_edge_strut',xz([(22.78,12.72),(23.01,12.72),(22.72,17),(22.50,17)],y,y+.20),0)
# Cross graphic dimensions fromlate shortendelevation, notprintedcentimetres.
bx('cross_vertical_graphical',22.36,22.61,5.025,5.275,13.72,20.85,3)
bx('cross_horizontal_graphical',22.36,22.61,2.985,7.315,18.48,18.73,3)
# Tower visiblebell is a schematic exterior silhouette only; no mechanical detail.
bx('bell_suspension_beam',24.1,24.35,2.1,8.2,16.80,17.12,0)
bx('bell_suspension',24.15,24.30,5.02,5.28,15.75,16.85,3)
add('bell_schematic_silhouette',Manifold.cylinder(.65,.40,.20,24).translate((24.22,5.15,15.10)),3)
for z,ymax in [(1.8685,5.40),(4.98,6.60),(8.13,6.60)]:bx('turnplatform_loadbearing_guard',.78,.92,3.935,ymax,z-.16,z+1.20,0)
# Guardwalls followupperflights, leavingactual voidbeneathstairs.
for z0,z1 in [(1.8685,3.43),(4.98,6.53),(8.13,9.73)]:
 add('upper_stair_guard_slope',xz([(2.10,z0-.10),(4.64,z1-.10),(4.64,z1+1.05),(2.10,z0+1.05)],3.80,3.95),0)
for z0,z1 in [(3.43,4.98),(6.53,8.13)]:
 add('lower_stair_guard_slope',xz([(2.10,z1-.10),(4.64,z0-.10),(4.64,z0+1.05),(2.10,z1+1.05)],6.60,6.75),0)
add('first_L_guard',yz([(1.15,-.04),(3.95,1.8685),(3.95,2.9185),(1.15,1.01)],.75,.90),0)


OPENINGS={'west_lower': {'ground_main_bays_x_m': [[5.95, 8.6], [8.95, 11.45], [11.8, 14.2], [14.7, 17.15], [17.55, 20.0], [20.4, 22.7], [26.5, 28.3], [28.65, 31.1]], 'ground_door_ranges_x_m': [[12.75, 13.8], [21.24, 22.2], [29.65, 30.65]]}, 'west_upper_openings': [{'id': 'statue_niche', 'x_range_m': [0.28, 2.1], 'z_range_m': [10.62, 12.75], 'type': '凹龕/立像輪廓，非普通窗'}, {'id': 'stair_horizontal_1', 'x_range_m': [2.37, 3.99], 'z_range_m': [11.45, 11.89], 'type': '圖示矩形開口'}, {'id': 'stair_horizontal_2', 'x_range_m': [2.97, 3.96], 'z_range_m': [10.74, 11.16], 'type': '圖示矩形開口'}, {'id': 'chapel_01', 'x_range_m': [9.63, 9.99], 'z_range_m': [10.72, 12.14], 'type': '圖示矩形開口'}, {'id': 'chapel_02', 'x_range_m': [10.27, 10.8], 'z_range_m': [10.72, 11.29], 'type': '圖示矩形開口'}, {'id': 'chapel_03', 'x_range_m': [9.63, 10.78], 'z_range_m': [10.2, 10.46], 'type': '圖示矩形開口'}, {'id': 'chapel_04', 'x_range_m': [12.16, 13.79], 'z_range_m': [11.71, 12.13], 'type': '圖示矩形開口'}, {'id': 'chapel_05', 'x_range_m': [12.78, 13.8], 'z_range_m': [11.23, 11.53], 'type': '圖示矩形開口'}, {'id': 'chapel_06', 'x_range_m': [15.73, 16.02], 'z_range_m': [10.66, 11.73], 'type': '圖示矩形開口'}, {'id': 'chapel_07', 'x_range_m': [16.51, 16.94], 'z_range_m': [11.73, 12.11], 'type': '圖示矩形開口'}, {'id': 'chapel_08', 'x_range_m': [16.24, 16.72], 'z_range_m': [11.11, 11.35], 'type': '圖示矩形開口'}, {'id': 'chapel_09', 'x_range_m': [19.42, 19.7], 'z_range_m': [10.64, 11.58], 'type': '圖示矩形開口'}, {'id': 'chapel_10', 'x_range_m': [20.3, 20.98], 'z_range_m': [11.28, 12.08], 'type': '圖示矩形開口'}, {'id': 'chapel_11', 'x_range_m': [20.32, 21.97], 'z_range_m': [10.22, 10.6], 'type': '圖示矩形開口'}], 'east_upper': {'stair_end_openings': [{'x_range_m': [3.45, 3.8], 'z_range_m': [10.55, 12.15]}, {'x_range_m': [1.1, 2.7], 'z_range_m': [11.4, 12.2]}, {'x_range_m': [2.25, 2.7], 'z_range_m': [10.15, 10.55]}], 'far_terrace_screen_opening': {'x_range_m': [28.7, 31.2], 'z_range_m': [10.1, 12.15]}}, 'short_ends': {'stair_end_openings': [{'y_range_m': [5.84, 7.27], 'z_range_m': [3.01, 3.46]}, {'y_range_m': [5.78, 6.78], 'z_range_m': [1.86, 2.77]}, {'y_range_m': [6.35, 7.54], 'z_range_m': [7.21, 7.71]}, {'y_range_m': [5.57, 5.89], 'z_range_m': [6.14, 7.5]}, {'y_range_m': [3.7, 4.92], 'z_range_m': [7.02, 7.45]}, {'y_range_m': [4.7, 5.14], 'z_range_m': [6.44, 6.73]}, {'y_range_m': [4.05, 4.49], 'z_range_m': [5.9, 6.3]}, {'y_range_m': [3.0, 3.32], 'z_range_m': [7.85, 8.94]}, {'y_range_m': [1.97, 2.59], 'z_range_m': [7.55, 8.19]}]}}
# Literal graphical facadecontrols are embedded for two-input reproducibility.
# Values±.15m, not printed dimensions; opaque glazing is print convention.
CUTS=[]
def win(n,x0,x1,y,z0,z1,cols,rows,side=-1):
 global body
 body=body-box(x0,x1,y-.31,y+.31,z0,z1)
 cy=y-side*.22
 bx(n+'_opaque_infill',x0-.01,x1+.01,cy-.11,cy+.11,z0-.01,z1+.01,5)
 for x in np.linspace(x0,x1,cols+1):bx(n+'_mullion',x-.04,x+.04,y-.045,y+.045,z0,z1,3)
 for z in np.linspace(z0,z1,rows+1):bx(n+'_rail',x0,x1,y-.045,y+.045,z-.04,z+.04,3)
for a,b in OPENINGS['west_lower']['ground_main_bays_x_m']:
 win('west_ground_small_grid',a,b,1.25,.65,3.0,max(4,round((b-a)/.38)),7)
for a,b in OPENINGS['west_lower']['ground_door_ranges_x_m']:
 # Adddoorsinfront ofwindowgraphic, consistentwithsameopening; do notmove tofrontguards.
 body=body-box(a,b,.9,1.6,0,2.1)
 for i in range(len(P)):
  if LOG[i]['name'].startswith('west_ground_small_grid'):
   door_void=box(a,b,.9,1.65,0,2.1).as_original();IDS[door_void.original_id()]=3;P[i]=P[i]-door_void
 bx('west_ground_door',a,b,1.28,1.62,-.02,2.1,3)
for z0,z1 in [(5.65,6.35),(8.75,9.45)]:
 for a,b in [(5.9,22.8),(25.8,31.2)]:win('west_recessed_high_windows',a,b,1.25,z0,z1,round((b-a)/.40),2)
# Eastglazing liesbehind50fins; no mirroredwestdoors.
for fl,top in [(0,3.45),(3.45,6.55),(6.55,9.68)]:
 win('east_fin_shadow_window_band',5.95,31.15,9.27,fl+.85,top-.35,50,3,1)
# Trueterracewall apertures, not glazedpanels. Westchapelholes remain external apertures.
for q in OPENINGS['west_upper_openings']:
 a,b=q['x_range_m'];c,d=q['z_range_m']
 if q['id']=='statue_niche':
  # Shallowrecessandplainframe; sculpturalfigure intentionallynotinvented.
  CUTS.append(box(a,b,-.1,.14,c,d))
 else:CUTS.append(box(a,b,-.10,.40,c,d))
for q in OPENINGS['east_upper']['stair_end_openings']+[OPENINGS['east_upper']['far_terrace_screen_opening']]:
 a,b=q['x_range_m'];c,d=q['z_range_m'];CUTS.append(box(a,b,9.80,10.30,c,d))
# Originalreview misassignedend; sourcecorrection relocates to x0; initial y values retained after direct end-elevation check.
for q in OPENINGS['short_ends']['stair_end_openings']:
 a,b=q['y_range_m'];c,d=q['z_range_m'];CUTS.append(box(-.10,.40,a,b,c,d))
 # Backing opacity exposes the sourceaperturewithoutinventedinteriorplan.
 # Stairopenings trueapertures, noopaque backpanel across the stairvoid.

add('lower_room_envelope',body,6)
solid=P[0]
for p in P[1:]:solid=solid+p
for cut in CUTS:
 cut=cut.as_original();IDS[cut.original_id()]=0;solid=solid-cut
solid=solid.set_tolerance(.0001).simplify(.0001).translate((-15.735,-5.095,SHIFT)).scale((S,S,S))
m=solid.to_mesh64();v=np.asarray(m.vert_properties)[:,:3];f=np.asarray(m.tri_verts);materials=np.zeros(len(f),dtype=int)
for i,oid in enumerate(m.run_original_id):materials[m.run_index[i]//3:m.run_index[i+1]//3]=IDS[int(oid)]
m=Manifold(Mesh64(v.astype(np.float32).astype(np.float64),f.astype(np.uint64),face_id=np.arange(len(f),dtype=np.uint64),tolerance=.00001)).simplify(.00001).to_mesh64();materials=materials[np.asarray(m.face_id,dtype=int)]
t=trimesh.Trimesh(np.asarray(m.vert_properties)[:,:3].astype(np.float32).astype(np.float64),np.asarray(m.tri_verts),process=False);t.merge_vertices(digits_vertex=5);keep=t.nondegenerate_faces();materials=materials[keep];t.update_faces(keep);t.remove_unreferenced_vertices()
np.savez_compressed(R/'mesh.npz',vertices=t.vertices,faces=t.faces,materials=materials);t.export(R/'model.stl');(R/'palette.json').write_text(json.dumps(PALETTE));(R/'components.json').write_text(json.dumps(LOG,ensure_ascii=False,indent=2))
q={'status':'WIP_PARTIAL_GEOMETRY_NOT_RELEASE','triangles':len(t.faces),'watertight':bool(t.is_watertight),'scale':'1:200','bounds_mm':t.bounds.tolist(),'mesh_sha256':hashlib.sha256((R/'mesh.npz').read_bytes()).hexdigest()};(R/'BUILD-QA.json').write_text(json.dumps(q,indent=2));print(json.dumps(q))
