"""嘉義農專嘉禾館：1981–1982 CCCK226 revised historical exterior, not current survey.
Metres before print conversion. Source scans remain private. Explicit limits in README.
"""
from pathlib import Path
import json,hashlib,numpy as np,trimesh
from manifold3d import Manifold,Mesh64,CrossSection
from geometry_helpers import box,prism
R=Path(__file__).resolve().parent
S=1000/250;BASE=.50;RF=14.53
AXES_X=np.arange(0,55.01,5).tolist()
AXES_Y=[0,4,10,15,20,25,30,35,41,45]
# Actual asymmetric wall-reference offsets; not a claim these are surveyed outside faces.
X0,X1,Y0,Y1=-2.19,57.29,-2.29,47.29
# Final unique coordination: nominal high dividing line14.53, 1% drainage to both sides.
# Absolute vertical positioning remains source-interpretation uncertainty ±0.24m.
def roof_z(y):return RF-.01*abs(y-22.5)
# W2 spatial A10/A11 preferred to uncoordinated A20 generic FL+169 (65cm discrepancy).
WINDOW_BOTTOM,WINDOW_TOP=10.67,11.97
PALETTE=[('illustrative pale mosaic','#CBC8BC'),('illustrative exposed concrete','#B6B6AC'),('illustrative roof finish','#8E938B'),('illustrative window frame','#D3D4CA'),('authored display support not surveyed terrain','#A5AD9C'),('opaque glazing illustration','#607D89'),('illustrative door','#8D9791'),('fan hood illustrative metal','#A5ADB0')]
P=[];LOG=[];IDS={}
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
def chamfer(a,b,c,d,ch=.87):return [(a+ch,c),(b-ch,c),(b,c+ch),(b,d-ch),(b-ch,d),(a+ch,d),(a,d-ch),(a,c+ch)]
# Display support is authored; source local paving levels remain separate.
bx('authored_display_support_not_terrain',-4.3,65.2,-4.3,49.3,-BASE,0,4)
# 226 main body: side exterior corridors remain open under the overhanging upper enclosure.
# Wall-centre I/B offset .24 beyond axes; exteriorwall thickness nominal.24m.
body=box(-.64,55.64,3.64,41.36,.08,5.19)
# Upper interior core is recessed behind the open perimeter; not a solid lower bounding box.
body=body+box(9.8,48.8,9.8,35.2,5.17,8.96)
# A13 rearstagewall rises to9.63; never a false open clerestory above5.19.
body=body+box(-.64,.20,3.64,41.36,5.17,9.63)
# Recessed entrance at x52.60, not full width occupied to the front columnline.
body=body-box(52.60,56.5,10.12,34.88,0,5.19)
# Front hall platform follows local1.03/1.08; side corridor remains low and open.
bx('main_hall_floor_control_108',-.60,52.62,3.65,41.35,0,1.08,1)
# Upper chamfered enclosure intersects two explicitly section-controlled profiles.
xprofile=[(X0+.87,8.11),(X1-.87,8.11),(X1,8.98),(X1,13.66),(X1-.87,RF),(X0+.87,RF),(X0,13.66),(X0,8.98)]
yprofile=[(Y0+.87,8.11),(Y1-.87,8.11),(Y1,8.98),(Y1,13.66),(Y1-.87,RF),(Y0+.87,RF),(Y0,13.66),(Y0,8.98)]
upper=xzsolid(xprofile,Y0,Y1)^yzsolid(yprofile,X0,X1)^prism(chamfer(X0,X1,Y0,Y1),8.1,RF+.01)
# Clear upper interior top for explicitly sloped finish; external parapet/chamfer stays14.53.
upper=upper-box(X0+1.02,X1-1.02,Y0+1.02,Y1-1.02,13.90,RF+.1)
# A11 middlefacade is recessed40cm behind the outer upper/loweredge, not flush.
for cut in [box(X0+.9,X1-.9,Y0-.01,Y0+.40,9.98,12.66),box(X0+.9,X1-.9,Y1-.40,Y1+.01,9.98,12.66),box(X1-.40,X1+.01,Y0+.9,Y1-.9,9.98,12.66)]:upper=upper-cut
W=[]
def rectplane(cx,cy,dx,dy,w,depth,z0,z1,offset=0):
 nx,ny=-dy,dx
 return prism([(cx+dx*u+nx*v,cy+dy*u+ny*v) for u,v in [(-w/2,offset),(w/2,offset),(w/2,offset+depth),(-w/2,offset+depth)]],z0,z1)
def opening(tag,cx,cy,dx,dy,w,z0,z1,cols=2,rows=1,which='body',mat=5):
 global body,upper
 cut=rectplane(cx,cy,dx,dy,w,.43,z0,z1,-.18)
 if which=='upper':upper=upper-cut
 else:body=body-cut
 W.append((tag,cx,cy,dx,dy,w,z0,z1,cols,rows,mat))
# 33 windows perlongside;27front:6subdivisions per10m repeatedsource rhythm.
for x in [(i+.5)*55/33 for i in range(33)]:
 opening('W2_upper_south_146x130',x,Y0+.40,1,0,1.46,WINDOW_BOTTOM,WINDOW_TOP,2,1,'upper')
 opening('W2_upper_north_146x130',x,Y1-.40,-1,0,1.46,WINDOW_BOTTOM,WINDOW_TOP,2,1,'upper')
for y in [(i+.5)*45/27 for i in range(27)]:
 opening('W2_upper_front_146x130',X1-.40,y,0,1,1.46,WINDOW_BOTTOM,WINDOW_TOP,2,1,'upper')
# Roof skin highline convention; no extra A27 materialstackaboveRF.
xa,xb,ya,yb=X0+1.00,X1-1.00,Y0+1.00,Y1-1.00
roof=yzsolid([(ya,13.88),(yb,13.88),(yb,roof_z(yb)),(22.5,RF),(ya,roof_z(ya))],xa,xb)
add('sloped_roof_A7_highline_coordination_not_measured_EL',roof,2)
# Exposed periphery columns and low side paving: column shapes simplified at modelscale.
for x in AXES_X:
 for y in [0,45]:
  bx('side_periphery_column',x-.30,x+.30,y-.30,y+.30,.05,8.20,1)
for y in [10,15,20,25,30,35]:
 bx('front_periphery_column',54.70,55.30,y-.30,y+.30,1.03,8.20,1)
# Back columns at unchangedstructuralaxis, not old highstair geometry.
for y in [0,10,20,25,35,45]:bx('rear_periphery_column',-.30,.30,y-.30,y+.30,.05,8.20,1)
for a,b in [(-.40,3.78),(41.22,45.40)]:
 bx('open_side_corridor_low_paving',-.70,55.7,a,b,0,.10,1)
# Four high U-shaped20cm RC supportwalls: A5 plan and A9 blank fullheightbays, NOT lowguards.
for y,sgn in [(0,1),(45,-1)]:
 for a in [5,45]:
  bx('side_high_U_RC_wall_horizontal',a,a+5,y-.10,y+.10,.05,8.20,1)
  for x in [a,a+5]:
   bx('side_high_U_RC_wall_return',x-.10,x+.10,min(y,y+sgn*1.1),max(y,y+sgn*1.1),.05,8.20,1)
# Revised226 lower-room façades. Wallfaces offset from columnaxes; roomFLs differ.
for side,y,dx in [('B',3.64,1),('I',41.36,-1)]:
 for x in [2.5,7.5,47.5,52.5]:
  fl=2.28 if x<10 else 1.08
  opening('W5_'+side+'_room_FL',x,y,dx,0,4.40,fl+.80,fl+2.30,3,1)
 for x in [22.5,27.5,32.5,42.5]:
  fl=1.03 if x in [22.5,27.5,32.5] else 1.08
  opening('W4_'+side+'_high_window',x,y,dx,0,4.40,fl+1.80,fl+2.45,4,1)
 # Sideentry actually recessed326cm, not a door painted onto solid outsidewall.
 if side=='B':
  body=body-box(10.3,14.7,3.4,7.02,1.03,3.78)
  opening('WD5_B_recessed_side_entrance',12.5,7.02,1,0,4.40,1.03,3.73,4,2,mat=6)
 else:
  body=body-box(10.3,14.7,37.98,41.6,1.03,3.78)
  opening('WD5_I_recessed_side_entrance',12.5,37.98,-1,0,4.40,1.03,3.73,4,2,mat=6)
 # Different A19 under-stage window, width/height graphically bounded ±.15, NOT A20W4.
 opening('A19_understage_'+side+'_window_graphic',2.5,y,dx,0,2.20,1.30,1.95,3,1)
# A5/A9 small external WD3 at staircasebay8-9; localpavingnotroomFL.
opening('WD3_B_external_access',35.75,3.64,1,0,1.50,.14,2.24,2,1,mat=6)
opening('WD3_I_external_access',35.75,41.36,-1,0,1.50,.15,2.25,2,1,mat=6)
# I-side low ventilating strips visible on revised A9, not mirrored toB.
for x in [22.5,27.5,32.5]:opening('I_male_bath_low_vent_graphic',x,41.36,-1,0,4.0,1.18,1.45,8,1)
# New under-stage rear doors (A5 auxiliaryplan/A8); original high exteriorDingstairs omitted.
for y in [11.8,33.2]:opening('rear_understage_D1_graphic',-.64,y,0,-1,1.00,.10,2.20,1,1,mat=6)
# Upper Bing entrances: rear-wall plane, A15 WD2a100x210; y placement graphical ±.25m.
for y in [10.8,34.2]:opening('rear_upper_Bing_WD2a',-.64,y,0,-1,1.00,2.23,4.33,1,1,mat=6)
# Front hall: dedicated doors and intervening fixed glass at recessedwall.
for y in [13.6,21.4,23.6,31.2]:opening('front_hall_WD2b',52.60,y,0,1,2.20,1.08,3.18,2,1,mat=6)
for y in [17.5,27.4]:opening('front_hall_W1',52.60,y,0,1,4.40,1.08,3.78,4,2)
# Slender sourceframe beams at external columnlines, no fabricated curtainwall.
for a,b in [(0,5),(10,45),(50,55)]:
 for y in [0,45]:bx('side_lower_exposed_frame_beam',a-.3,b+.3,y-.30,y+.30,4.89,5.19,1)
for y in [0,45]:
 for a,b in [(0,5),(50,55)]:
  bx('side_end_exposed_lower_frame_beam',a-.30,b+.30,y-.30,y+.30,3.63,3.93,1)
# Main entrance A10a: landing +103,7risesx14,6treadsx45 fromlocal+5.
# Plan platformchain measured from frontcolumn55:4.15m then2.70m run. No realterrainassertion.
bx('front_entrance_landing_revised226',52.58,59.79,10.15,34.85,0,1.03,1)
for k in range(6):
 # descending from landingoutwards; lowest firsttread at+.19, last at+.89.
 z=1.03-.14*(k+1)
 bx('front_entrance_step_7rises_6treads',59.79+.45*k,59.79+.45*(k+1),10.15,34.85,0,z,1)
bx('front_local_paving_plus005_not_global_terrain',59.74,64.49,9.95,35.05,0,.05,1)
# Rear corner 丙 flights, adoptedA15; mirroredactualpair, not cancelledhighflights.
# Sourceplan long566=286run+170landing+100approach+10wall; 140clearwidth.
# Absolute flight placement from revised A5 graphics ±.20m, not exactly on B/I axes.
# Ascend inward: south B→C, north I→H. Direct run286 + landing280 =566cm.
for side,ys,sgn in [('south',6.0,1),('north',39.0,-1)]:
 xlo,xhi=-1.40,0.02
 top=[(0,.05)]
 for k in range(11):
  z=.05+(k+1)*(2.18/12)
  top.extend([(.26*k,z),(.26*(k+1),z)])
 top.extend([(2.86,2.23),(5.66,2.23)])
 # Nominal13cm waist; preserve open underside rather than solid ramp to ground.
 poly=top+[(5.66,2.10),(2.86,2.10),(0,-.08)]
 add('rear_low_Bing_'+side+'_waist13cm_and_treads',yzsolid([(ys+sgn*u,z)for u,z in poly],xlo,xhi),1)
 for u in [2.96,5.56]:
  yy=ys+sgn*u
  bx('rear_low_Bing_'+side+'_platform_support',xlo,xhi,yy-.10,yy+.10,.05,2.12,1)
 gp=[(0,-.08),(2.86,2.10),(5.66,2.10),(5.66,3.23),(2.86,3.23),(0,1.05)]
 add('rear_low_Bing_'+side+'_following_solid_guard',yzsolid([(ys+sgn*u,z)for u,z in gp],xlo-.12,xlo+.02),1)
add('revised226_main_exterior_preserving_open_perimeter',body,0)
add('chamfered_upper_enclosure_rear_blank_not_oldhighstairs',upper,0)
for tag,cx,cy,dx,dy,w,z0,z1,cols,rows,mat in W:
 add(tag+'_opaque_infill_not_glassprint',rectplane(cx,cy,dx,dy,w+.02,.17,z0-.02,z1+.02,.10),mat)
 fw=.10 # 0.4mm at1:250 printingadaptation, notsourceframethickness
 for u in np.linspace(-w/2,w/2,cols+1):add(tag+'_frame',rectplane(cx+dx*u,cy+dy*u,dx,dy,fw,.30,z0,z1,-.07),3)
 for z in np.linspace(z0,z1,rows+1):add(tag+'_rail',rectplane(cx,cy,dx,dy,w,.30,z-fw/2,z+fw/2,-.07),3)
# Eight domecovers: A7 centres+explicit A27 cover93x118/rise33; curb16±7cm graphically reconstructed.
SKYLIGHTS=[(27.5,12.5),(22.5,17.5),(27.5,17.5),(32.5,17.5),(22.5,27.5),(27.5,27.5),(32.5,27.5),(27.5,32.5)]
for i,(x,y) in enumerate(SKYLIGHTS):
 z=roof_z(y)
 bx('skylight_%02d_curb_graphic16cm'%i,x-.60,x+.60,y-.60,y+.60,z-.03,z+.16,1)
 dome=Manifold.sphere(1,32).scale((.465,.59,.33)).translate((x,y,z+.16))
 dome=dome-box(x-1,x+1,y-1,y+1,z-1,z+.155)
 add('skylight_%02d_cover_93x118_rise33'%i,dome,5)
# Exterior fans only: no blades,wiring,controls. Datumcurb16±7cm graphical.
FANS=[(x,y)for y in [12.5,32.5]for x in [22.5,32.5]]+[(x,y)for y in [17.5,27.5]for x in [7.5,17.5,37.5]]
for i,(x,y) in enumerate(FANS):
 z=roof_z(y)
 bx('fan_%02d_architectural_seat1355'%i,x-.6775,x+.6775,y-.6775,y+.6775,z-.03,z+.16,1)
 add('fan_%02d_base1372_height80'%i,Manifold.cylinder(.08,.686,.686,48).translate((x,y,z+.16)),7)
 add('fan_%02d_neck165'%i,Manifold.cylinder(.165,.50,.60,48).translate((x,y,z+.24)),7)
 # SourceNO SCALE: hoodskirtcurve and cone tip radii are explicitly illustrative outline estimates.
 add('fan_%02d_max1524_skirt_graphic'%i,Manifold.cylinder(.14,.762,.48,48).translate((x,y,z+.405)),7)
 add('fan_%02d_truncated_cone_graphic_tip'%i,Manifold.cylinder(.593,.48,.22,48).translate((x,y,z+.545)),7)
# NUMERICAL_FINALIZATION
solid=P[0]
for p in P[1:]:solid=solid+p
solid=solid.set_tolerance(.0001).simplify(.0001).translate((-27.5,-22.5,BASE)).scale((S,S,S))
m=solid.to_mesh64();v=np.asarray(m.vert_properties)[:,:3];f=np.asarray(m.tri_verts);materials=np.zeros(len(f),dtype=int)
for i,oid in enumerate(m.run_original_id):materials[m.run_index[i]//3:m.run_index[i+1]//3]=IDS[int(oid)]
m=Manifold(Mesh64(v.astype(np.float32).astype(np.float64),f.astype(np.uint64),face_id=np.arange(len(f),dtype=np.uint64),tolerance=.00001)).simplify(.00001).to_mesh64();materials=materials[np.asarray(m.face_id,dtype=int)]
t=trimesh.Trimesh(np.asarray(m.vert_properties)[:,:3].astype(np.float32).astype(np.float64),np.asarray(m.tri_verts),process=False);t.merge_vertices(digits_vertex=5);keep=t.nondegenerate_faces();materials=materials[keep];t.update_faces(keep);t.remove_unreferenced_vertices()
np.savez_compressed(R/'mesh.npz',vertices=t.vertices,faces=t.faces,materials=materials);t.export(R/'model.stl');(R/'palette.json').write_text(json.dumps(PALETTE));(R/'components.json').write_text(json.dumps(LOG,ensure_ascii=False,indent=2))
q={'status':'WIP_NOT_FINAL_SOURCE_OR_PRINT_QA','triangles':len(t.faces),'watertight':bool(t.is_watertight),'winding':bool(t.is_winding_consistent),'scale':'1:250','bounds_mm':t.bounds.tolist(),'mesh_sha256':hashlib.sha256((R/'mesh.npz').read_bytes()).hexdigest()};(R/'BUILD-QA.json').write_text(json.dumps(q,indent=2));print(json.dumps(q))
