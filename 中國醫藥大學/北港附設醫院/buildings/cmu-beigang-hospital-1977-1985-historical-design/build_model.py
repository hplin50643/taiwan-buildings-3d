"""CMU Beigang historical exterior, 1977–1985 per-sheet composite.
Working model pending independent visual QA. No interiors/current survey implied.
Metres in source coordinates, exported millimetres at1:400.
"""
from pathlib import Path
import json,hashlib,numpy as np,trimesh
from manifold3d import Manifold,Mesh64,CrossSection
from geometry_helpers import box,prism,perimeter_band,y_intersections,square_vault_cap
R=Path(__file__).resolve().parent;C=json.loads((R/'geometry_controls.json').read_text());D=C['floors'];P=[];LOG=[];IDS={};S=2.5
PALETTE=[('illustrative cream masonry','#C9C2AF'),('illustrative concrete bands','#AFAEAA'),('illustrative roof finish','#999C94'),('illustrative frame','#787F80'),('authored support not surveyed terrain','#A3AB9C'),('opaque glazing illustration','#5D7981'),('illustrative door','#7F8886'),('illustrative translucent rooflight','#B6CDCE')]
def add(n,m,mat=0):
 if m.is_empty():raise ValueError(n)
 m=m.as_original();IDS[m.original_id()]=mat;P.append(m);LOG.append({'name':n,'material':mat,'bounds_m':list(m.bounding_box())})
def bx(n,a,b,c,d,e,f,mat=0):add(n,box(a,b,c,d,e,f),mat)
bx('authored_display_support_not_site',-9,119,-4,85,-.65,0,4)
Z=[(0,5.16),(5.16,9.10),(9.12,12.18),(12.18,15.24),(15.24,18.30),(18.30,21.36),(21.36,24.78)]
FL=[1.2,5.16,9.12,12.18,15.24,18.3,21.72];B={k:prism(v['polygon_m'],a-.01,b) for (k,v),(a,b) in zip(D.items(),Z)}
for key,dat in D.items():
 for pp in dat.get('additional_polygons_m',[]):
  a,b=Z[int(key[0])-1];B[key]=B[key]+prism(pp,a-.01,b)
# Northterrace is15cm below3FL, only where not coveredbythethird-floor body.
north_cut=box(-10,67.05,55.95,85,8.78,10.50)-prism(D['3F']['polygon_m'],8.70,10.60)
B['2F']=B['2F']-north_cut
W=[];OPENING_AUDIT=[];OPENING_REVISIONS=[]
def win(floor,x,side,w,z0,z1,tag,cols=2,face=None,axis='y'):
 key=str(floor)+'F';original_x=x;original_w=w
 polys=[D[key]['polygon_m']]+D[key].get('additional_polygons_m',[])
 hits=[]
 for poly in polys:
  pts=poly if axis=='y' else [[b,a]for a,b in poly]
  for (u0,v0),(u1,v1) in zip(pts,pts[1:]+pts[:1]):
   if min(u0,u1)<=x<max(u0,u1):hits.append((v0+(v1-v0)*(x-u0)/(u1-u0),u0,v0,u1,v1))
 if not hits:raise ValueError((key,x,axis))
 hit=(min if side<0 else max)(hits,key=lambda q:q[0]);actual=hit[0]
 if face is None or abs(face-actual)<=.35:face=actual
 _,u0,v0,u1,v1=hit
 if abs((v1-v0)/(u1-u0))>.05:
  OPENING_REVISIONS.append({'floor':floor,'axis':axis,'tag':tag,'original_center':x,'original_width':w,'action':'omitted graphic candidate on sloping wall; no fictitious rectangular projection'})
  return
 lo=max(x-w/2,min(u0,u1)+.08);hi=min(x+w/2,max(u0,u1)-.08)
 if hi-lo<.60:
  OPENING_REVISIONS.append({'floor':floor,'axis':axis,'tag':tag,'original_center':x,'original_width':w,'action':'omitted unresolved graphic corner sliver narrowerthan60cm'})
  return
 x=(lo+hi)/2;w=hi-lo
 if abs(w-original_w)>.001:OPENING_REVISIONS.append({'floor':floor,'axis':axis,'tag':tag,'original_center':original_x,'original_width':original_w,'center':x,'width':w,'action':'graphic strip clipped to actual continuous straightwall segment,08cm corner clearance'})
 cut=box(x-w/2,x+w/2,face-.40,face+.40,z0,z1) if axis=='y' else box(face-.40,face+.40,x-w/2,x+w/2,z0,z1)
 OPENING_AUDIT.append({'floor':floor,'axis':axis,'face':face,'center':x,'width':w,'z':[z0,z1],'side':side,'tag':tag})
 B[key]=B[key]-cut;W.append((tag,axis,face,x,w,z0,z1,side,cols))
AX=[0,5.85,11.7,17.55,23.4,30.6,37.8,45,52.2,59.4,66.6,67.05,74.25,81.45,88.65,94.5,100.35,106.2,112.05]
# Nine720cm bays, two discrete openings perbay;45cm structural joint remains separate.
centers=[]
for a in [23.4,30.6,37.8,45,52.2,59.4,67.05,74.25,81.45]:centers.extend([a+1.8,a+5.4])
# Upper longfacade positions from A30/A31 and corresponding individual floor plans.
for lev in range(3,7):
 fl=FL[lev-1]
 for side in [-1,1]:
  for x in centers:win(lev,x,side,2.45,fl+1.05,fl+2.40,'upper_discrete_room_window_graphic',2)
# Longends: visible balcony bays differ on north/south, do not mirror complete elevations.
BAL=[]
for lev in range(2,7):
 fl=FL[lev-1]
 for side,starts in [(-1,[88.65,94.5,100.35,106.2]),(1,[88.65,94.5,100.35])]:
  for a in starts:
   x=a+2.925;win(lev,x,side,4.90,fl+.80,fl+2.65,'east_end_balcony_glazed_back',4)
   BAL.append((lev,a,a+5.85,side,1.20))
for lev in [5,6]:
 fl=FL[lev-1]
 for a in [5.85,11.7,17.55]:
  win(lev,a+2.925,-1,4.90,fl+.80,fl+2.65,'west_south_three_balcony_bays',4);BAL.append((lev,a,a+5.85,-1,1.20))
for lev in [3,4,5,6]:
 fl=FL[lev-1]
 for a in [0,5.85,11.7,17.55]:
  win(lev,a+2.925,1,4.90,fl+.80,fl+2.65,'west_north_four_balcony_bays',4);BAL.append((lev,a,a+5.85,1,1.20))
# Fourth-floor southern projection is closed rooms, NOT the fifth-floor balcony repeated.
for lev in [3,4]:
 fl=FL[lev-1]
 for a in [5.85,11.7,17.55]:win(lev,a+2.925,-1,3.15,fl+1.05,fl+2.40,'west_south_lower_different_room_windows',3)
# Seventh-floor A20 room-specific mapping, not copied downstairs bedroom centres.
# Composite balcony-door heights are facade-graphic; W3 90 applies only towindowbands.
for side,cc in [(1,[25.2,28.8,32.4,36.0,39.6,43.2]),(-1,[25.2,28.8,32.4,36.0,39.6,43.2,46.8,50.4,54.0,57.6,61.2,68.85,72.45,76.05,79.65,83.25,86.85])]:
 for x in cc:win(7,x,side,2.50,23.22,24.12,'seventh_specific_room_or_communal_graphic_window_band',2)
for side,start in [(1,0),(-1,88.65)]:
 for j in range(8):
  a=start+2.925*j;x=a+1.4625
  win(7,x,side,2.30,21.82,24.12,'seventh_7016_balcony_door_glazing_composite_graphic',3)
  BAL.append((7,a,a+2.925,side,1.35))
for x in [50.4,54.0,57.6,61.2]:
 win(7,x,1,.95,21.82,24.12,'seventh_7001_north_balcony_door_graphic',1)
 BAL.append((7,x-1.65,x+1.65,1,1.50))
# Small bath vents are separately graphic-mapped, not bedroom-sizedglazing.
for x in [13.2,16.5,20.0]:win(7,x,-1,.90,23.42,24.12,'seventh_bath_high_vent_graphic',1)
# Westservice corridor faces the drying terrace; twoelevation bands, no bedroomrow.
for x in [2.9,8.8]:win(7,x,-1,3.8,23.22,24.12,'seventh_service_corridor_band_graphic',3)
# Northopenroof court retains actualback wall and enddoors; no fictitiousfrontwall glazing.
for x in [82.5,93.3]:win(7,x,1,.95,21.82,24.12,'seventh_north_terrace_enddoor_graphic',1)
# Stair facade bands: graphic width2.8±.2m; short glazed bands and tall solid spandrels.
# East lowest band is not the west double-door entrance.
for lev,(za,zb) in enumerate([(2.7,4.0),(6.7,8.0),(10.2,11.5),(13.2,14.5),(16.3,17.6),(19.4,20.7)],1):
 for side,c in [(-1,53.2),(1,53.7)]:
  if lev==1 and side==-1:win(1,48.9,side,2.8,1.2,3.95,'west_stair_ground_double_door_graphic',2,axis='x')
  else:win(lev,c,side,2.8,za,zb,'end_stair_segmented_glazing_graphic_not_continuous_glass',2,axis='x')
# Latest A15 1F closed rooms stop ataxis16; the nexttwo bays remain open undercroft.
for x in [68.85,72.45,76.05,79.65,83.25,86.85,91.575,97.425]:
 for side in [-1,1]:win(1,x,side,2.45,2.2,4.2,'latest_A15_east_ground_closed_room_glazing_graphic',2)
for x in [68.85,72.45,76.05,79.65,83.25,86.85]:
 for side in [-1,1]:win(2,x,side,2.45,6.2,8.2,'second_east_central_room_glazing_graphic',2)
# Podium south-facing glazing, discontinuous duecourtyards; heights graphic fromA30.
for lev in [1,2]:
 fl=FL[lev-1]
 for a,b in [(0,11.7),(17.55,23.4),(23.4,37.8),(45,67.05)]:
  for x in np.arange(a+1.45,b-.5,2.9):win(lev,float(x),-1,2.35,fl+1.0,fl+3.0,'south_podium_segmented_glazing',2)
# North podium is not a duplicate southern facade: narrow secondfloor strip in main northroomfront.
for x in np.arange(16,57,3.4):win(2,float(x),1,2.70,6.90,8.00,'north_podium_narrow_band_graphic',3)
for x in [18,21.4,42,45.4,48.8]:win(1,x,1,2.70,2.2,4.2,'north_podium_discontinuous_lower_windows',3)
# East/west podium facade strips are individually placed fromA30/A31, not mirrored.
def side_win(lev,y,side,w,z0,z1,tag,cols=3):
 pts=[[b,a] for a,b in D[str(lev)+'F']['polygon_m']];xx=y_intersections(pts,y)
 face=xx[0] if side<0 else xx[-1]
 win(lev,y,side,w,z0,z1,tag,cols,face,'x')
for lev in [1,2]:
 lo,hi=(2.20,4.20) if lev==1 else (6.20,8.20)
 for y in [7.2,13.0,18.8]:side_win(lev,y,1,4.80,lo,hi,'east_south_podium_three_large_frames',4)
 for y in [68.0,73.0,78.0]:side_win(lev,y,1,3.90,lo if lev==1 else 6.90,hi if lev==1 else 8.0,'east_north_podium_separated_windows',3)
 for y in [3.2,8.7,14.2]:side_win(lev,y,-1,4.55,lo,hi,'west_south_podium_three_large_frames',4)
 side_win(lev,25.8,-1,5.3,lo,hi,'west_podium_local_window_beside_blank_wall',4)
 for y in [68.0,72.4,76.8]:side_win(lev,y,-1,3.80,lo if lev==1 else 6.90,hi if lev==1 else 8.0,'west_north_podium_narrow_not_south_copy',4)
for y in [28,32.5,37,41.5,46]:side_win(2,y,1,4.0,6.9,8.0,'east_central_long_narrow_band',4)
for y in [26,43.2]:side_win(1,y,1,3.1,2.2,4.2,'east_ground_discontinuous_windows',3)
side_win(1,32.3,1,5.50,1.20,3.95,'east_main_entrance_glazed_opening',4)
for key,b in B.items():add(key+'_closed_historical_exterior_no_interior',b,0)
# Window backs and printable frame relief, dimensional adaptation explicitly documented.
for tag,axis,face,x,w,z0,z1,side,cols in W:
 def panel(suffix,u0,u1,v0,v1,d0,d1,mat):
  a,b=sorted([face+side*d0,face+side*d1])
  if axis=='y':bx(tag+suffix,u0,u1,a,b,v0,v1,mat)
  else:bx(tag+suffix,a,b,u0,u1,v0,v1,mat)
 panel('_opaque_infill',x-w/2-.02,x+w/2+.02,z0-.02,z1+.02,-.45,-.18,5)
 fw=.16
 for xx in [x-w/2,x+w/2-fw]:panel('_jamb',xx,xx+fw,z0,z1,-.22,.04,3)
 for zz in [z0,z1-fw]:panel('_rail',x-w/2,x+w/2,zz,zz+fw,-.22,.04,3)
 for xx in np.linspace(x-w/2,x+w/2,cols+1)[1:-1]:panel('_mullion',xx-fw/2,xx+fw/2,z0,z1,-.22,.05,3)
# Balcony frames are open recesses ratherthan solid extruded wings.
for lev,a,b,side,dep in BAL:
 ys=y_intersections(D[str(lev)+'F']['polygon_m'],(a+b)/2);face=ys[0] if side<0 else ys[-1];fl=FL[lev-1];y0,y1=sorted([face-side*.15,face+side*dep])
 bx('balcony_slab_source_depth_graphic',a-.03,b+.03,y0,y1,fl-.18,fl+.04,1)
 ra,rb=sorted([face+side*(dep-.18),face+side*dep]);bx('balcony_solid_front_rail_graphic',a-.03,b+.03,ra,rb,fl,fl+.90,1)
 for x in [a,b-.18]:bx('balcony_vertical_side_frame_graphic',x-.03,x+.21,y0,y1,fl,fl+2.90,1)
# Open eastern two-bay undercroft from lateA15, not solid rooms or glazing.
fx=D['1F']['affine_x'];fy=D['1F']['affine_y']
def source1(px,py):return (fx[0]*px+fx[1],fy[0]*py+fy[1])
for py in [364,427,503]:
 xx,yy=source1(1299,py);bx('east_ground_open_undercroft_three_source_traced_columns',xx-.25,xx+.25,yy-.25,yy+.25,0,5.18,1)
# Source spot+180=GL1.20 platform, adjacentspot+105=GL.45, not a newclosedroom.
x0,y1=source1(1246,414);x1,y0=source1(1300,482)
bx('east_undercroft_partial_platform_GL120',x0-.1,x1,y0,y1,0,1.2,1)
# Five visible diagram-step bands approximate the75cm exterior drop, not an exact schedule.
_,yb=source1(1300,492)
for j in range(5):
 yy=y0-(j+1)*(y0-yb)/5
 bx('east_undercroft_graphic_step_not_exact_riser',x0-.1,x1,yy,y0,0,1.2-(j+1)*.15,1)
# Low roofs and exterior circulation retain their separate levels.
for name,pts,z in [('south_podium',D['2F']['polygon_m'],9.12),('upper_main',D['7F']['polygon_m'],25.08)]:
 skin=prism(pts,z-.18,z)
 if name=='south_podium':skin=skin-north_cut
 add(name+'_nominal_roof_skin',skin,2)
 if name=='upper_main':add('main_parapet_RF2478_plus120_NOT_skin_plus120',perimeter_band(pts,.20,25.07,25.98),1)
 else:add('podium_parapet110_south_direct_other_edges_graphic_continuation',perimeter_band(pts,.20,9.10,10.22)-north_cut,1)
north_outline=[(14.0,55.95),(59.4,55.95),(59.4,80.0),(14.0,80.0)]
add('north_terrace_roof_GL897',prism(north_outline,8.78,8.97),2)
add('north_parapet_graphic110_continuation_top1007',perimeter_band(north_outline,.20,8.96,10.07),1)
# Lowerterrace18+12cm finish aboveRFprime21.36, not seventhFL21.72.
terr=prism(D['6F']['polygon_m'],21.35,21.66)-prism(D['7F']['polygon_m'],21.0,22.0)
if not terr.is_empty():add('sixth_roof_terrace_finish2166',terr,2)
# Lecturehall andnorthmechanicalroom are distinct podium height controls.
bx('lecturehall_upper_exterior_roof1116',11.7,30.6,11.7,29.25,9.10,11.16,0)
bx('north_mechanicalroom_upper_exterior_roof1218',17.55,45,65.475,77.375,8.95,12.18,0)
# A16 north outsidewalk: slab+120cm rail, not enclosedfullstorybody.
bx('north_exterior_walk_floor',14.0,46.0,77.20,80.0,5.00,5.16,1)
bx('north_walk120_RC_rail',14.0,46.0,79.80,80.0,5.15,6.36,1)
# A17 eastern entrance canopy,GL4.18; plan-traced footprint, not a fullstorey room.
bx('east_entrance_canopy418',70.1,81.8,29.9,36.8,3.98,4.18,1)
for yy in [29.9,36.8]:bx('east_canopy_visible_support_graphic',79.7,80.1,yy-.20,yy+.20,0,4.0,1)
# A15 mainentrance spots180/104: localdoor1.20, foot.44; no complete terrain reconstruction.
bx('mainentry_graphic_landing_GL120',66.7,68.4,29.6,35.6,0,1.20,1)
bx('mainentry_localfoot_GL044_NOT_complete_site',68.3,71.0,29.6,35.6,0,.44,1)
for j in range(5):
 bx('mainentry_five_graphic_step_bands_count_not_verified',68.3,68.4+(j+1)*.36,29.6,35.6,.43,1.20-j*.76/5,1)
# West stair foot nominalGL0 only fromA31 elevation; no independent A15 spot,±.20m interpretation.
wx0,wy1=source1(266,501);wx1,wy0=source1(284,524);wland,_=source1(294,524)
bx('westentry_graphic_landing_GL120',wx1,wland,wy0,wy1,0,1.20,1)
for j in range(8):
 bx('westentry_eight_graphic_bands_NOT_exact_stair_schedule',wx0+j*(wx1-wx0)/8,wx1+.05,wy0,wy1,0,(j+1)*1.20/8,1)
# Southerncourtyard is left open; only a low authored approach is shown, no realterrain inference.
# Rooflight array A52a: 12x6 ceiling grid, inner10x4 rooflights;1.75pitch.
for i in range(10):
 for j in range(4):
  x=33.525+1.75*i;y=32.475+1.75*j
  bx('rooflight_RC_seat',x-.75,x+.75,y-.75,y+.75,9.10,9.42,1)
  bx('rooflight_louver_base40',x-.60,x+.60,y-.60,y+.60,9.40,9.82,3)
  for zz in [9.48,9.60,9.72]:add('rooflight_louver_relief',perimeter_band([(x-.64,y-.64),(x+.64,y-.64),(x+.64,y+.64),(x-.64,y+.64)],.08,zz,zz+.05),1)
  add('rooflight_square_vault_rise50_curve_approximation',square_vault_cap(x,y,9.82,1.2,.5),7)
# Two matching13.05m towerframes,5.275m shortedge glyph interpretation±.10m.
# Position traced aboutaxes9–10 andK/J, not expanded to the north mainroof.
tx=55.8;ty=53.20
tower=box(tx-6.525,tx+6.525,ty-2.6375,ty+2.6375,24.77,30.14)
TW=[(-1,tx,1.20,25.50,26.20),(-1,tx,1.20,28.10,28.80),(1,tx,1.50,28.10,28.80),(1,tx,4.80,26.20,26.60),(1,tx-4.5,.95,24.80,26.80),(1,tx+4.5,.95,24.80,26.80)]
for side,xx,ww,z0,z1 in TW:
 face=ty+side*2.6375;tower=tower-box(xx-ww/2,xx+ww/2,face-.4,face+.4,z0,z1)
 aa,bb=sorted([face-side*.45,face-side*.18]);bx('tower_elevation_graphic_opaque_window',xx-ww/2-.02,xx+ww/2+.02,aa,bb,z0-.02,z1+.02,5)
 aa,bb=sorted([face-side*.22,face+side*.04])
 for zz in [z0,z1-.16]:bx('tower_window_rail_graphic',xx-ww/2,xx+ww/2,aa,bb,zz,zz+.16,3)
 for xxxx in [xx-ww/2,xx+ww/2-.16]:bx('tower_window_jamb_graphic',xxxx,xxxx+.16,aa,bb,z0,z1,3)
add('tower_two_levels_1305_nominal5275',tower,0)
add('tower_180_parapet3194_cross_section_coordination',perimeter_band([(tx-6.525,ty-2.6375),(tx+6.525,ty-2.6375),(tx+6.525,ty+2.6375),(tx-6.525,ty+2.6375)],.20,30.12,31.94),0)
for xx in [tx-3.2,tx+3.2]:bx('tower_60cm_covered_roof_hatch',xx-.30,xx+.30,ty-.30,ty+.30,30.13,30.24,1)
for zz in [27.64,30.14]:bx('tower_north120_raincanopy',tx-6.525,tx+6.525,ty+2.5,ty+3.8375,zz-.18,zz,1)
# Numerical consolidation only; no claim of physical print success.
solid=P[0]
for p in P[1:]:solid=solid+p
solid=solid.set_tolerance(.0001).simplify(.0001).translate((-55,-40,.65)).scale((S,S,S))
m=solid.to_mesh64();v=np.asarray(m.vert_properties)[:,:3];f=np.asarray(m.tri_verts);materials=np.zeros(len(f),dtype=int)
for i,oid in enumerate(m.run_original_id):materials[m.run_index[i]//3:m.run_index[i+1]//3]=IDS[int(oid)]
m=Manifold(Mesh64(v.astype(np.float32).astype(np.float64),f.astype(np.uint64),face_id=np.arange(len(f),dtype=np.uint64),tolerance=.00001)).simplify(.00001).to_mesh64();materials=materials[np.asarray(m.face_id,dtype=int)]
t=trimesh.Trimesh(np.asarray(m.vert_properties)[:,:3].astype(np.float32).astype(np.float64),np.asarray(m.tri_verts),process=False);t.merge_vertices(digits_vertex=5);keep=t.nondegenerate_faces();materials=materials[keep];t.update_faces(keep);t.remove_unreferenced_vertices()
(R/'opening-revisions.json').write_text(json.dumps(OPENING_REVISIONS,ensure_ascii=False,indent=2))
(R/'opening-controls.json').write_text(json.dumps(OPENING_AUDIT,ensure_ascii=False,indent=2))
np.savez_compressed(R/'mesh.npz',vertices=t.vertices,faces=t.faces,materials=materials);t.export(R/'model.stl');(R/'palette.json').write_text(json.dumps(PALETTE));(R/'components.json').write_text(json.dumps(LOG,ensure_ascii=False,indent=2))
q={'status':'WIP_NOT_FINAL_SOURCE_OR_PRINT_QA','triangles':len(t.faces),'watertight':bool(t.is_watertight),'winding':bool(t.is_winding_consistent),'scale':'1:400','bounds_mm':t.bounds.tolist(),'mesh_sha256':hashlib.sha256((R/'mesh.npz').read_bytes()).hexdigest()};(R/'BUILD-QA.json').write_text(json.dumps(q,indent=2));print(json.dumps(q))
