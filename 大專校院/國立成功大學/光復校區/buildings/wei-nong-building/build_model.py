"""Wei-Nong same-item quality upgrade, historical exterior, metre source units.
Bounded exterior geometry; final release requires independent visual and format QA.
"""
from pathlib import Path
import json,hashlib,numpy as np,trimesh
from manifold3d import Manifold,Mesh64,CrossSection
from geometry_helpers import box,prism
R=Path(__file__).resolve().parent
S=1000/350;SHIFT=.65;P=[];LOG=[];IDS={}
PALETTE=[('historical illustrative brick','#995747'),('illustrative concrete','#C7C3B6'),('specified green cement tiles illustrative','#607568'),('print-thickened metal frames','#858D8A'),('authored display support NOT terrain','#A7AE9B'),('opaque glazing illustration','#739195'),('historical dark railing','#67706B')]
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
# Source-unit wall-axis controls. Full exterior offsets differ by edge.
bx('authored_display_support_not_terrain',-1.5,83.1,-1.5,42.3,-SHIFT,-.05,4)
WINGS=[('south_main',13.6,54.4,3.0,11.7,4,13.96,15.86),
('north_main',27.2,68.,29.1,37.8,4,15.86,13.96),
('northwest_short',0.,17.,32.1,40.8,3,12.57,10.77),
('west_middle_short',3.4,17.,20.4,29.1,3,10.77,12.57),
('southeast_short',64.6,81.6,0.,8.7,3,10.77,12.57),
('east_middle_short',64.6,78.2,11.7,20.4,3,12.57,10.77)]
# Window solids are shallow exterior recesses, not a claim of hidden interiors.
def facade_window(body,n,a,b,plane,z0,z1,side=-1,cols=4,transom=None):
 body=body-box(a,b,plane-.40,plane+.40,z0,z1)
 back=plane-side*.32
 bx(n+'_opaque_glazing_convention',a-.015,b+.015,back-.12,back+.12,z0-.015,z1+.015,5)
 for x in np.linspace(a,b,cols+1):bx(n+'_frame_thickened',x-.07,x+.07,plane-.07,plane+.07,z0-.03,z1+.03,3)
 for z in [z0,z1]+([] if transom is None else [transom]):bx(n+'_frame_rail_thickened',a-.03,b+.03,plane-.07,plane+.07,z-.07,z+.07,3)
 return body
def F_window(body,n,center,plane,fl,side=-1,axis='x'):
 a,b=center-.35,center+.35;z0,z1=fl+.30,fl+2.64
 if axis=='x':
  body=facade_window(body,n,a,b,plane,z0,z1,side,1,z0+.70)
  bx(n+'_second_transom',a-.02,b+.02,plane-.07,plane+.07,z0+1.64-.07,z0+1.64+.07,3)
 else:
  body=body-box(plane-.40,plane+.40,a,b,z0,z1)
  back=plane-side*.32
  bx(n+'_glazing',back-.12,back+.12,a-.015,b+.015,z0-.015,z1+.015,5)
  for y in [a,b]:bx(n+'_frame',plane-.07,plane+.07,y-.07,y+.07,z0-.03,z1+.03,3)
  for z in [z0,z0+.70,z0+1.64,z1]:bx(n+'_rails',plane-.07,plane+.07,a-.02,b+.02,z-.07,z+.07,3)
 return body
for name,x0,x1,y0,y1,n,z0,z1 in WINGS:
 a=x0-.055;b=x1+.055;c=y0-.09;d=y1+.09
 body=yz([(c,-.06),(d,-.06),(d,z1-.20),(c,z0-.20)],a,b)
 # Low outer side has C windows. Opposite doors/high windows will be registered separately.
 outlow=z0<z1;outer=c if outlow else d;side=-1 if outlow else 1
 bays=int(round((x1-x0)/3.40))
 for f in range(n):
  fl=1.+3.24*f
  for j in range(bays):
   wa=x0+j*3.4+.18;wb=wa+3.04
   body=facade_window(body,name+'_C_window',wa,wb,outer,fl+.90,fl+2.64,side,4,fl+2.30)
  # Concrete outer sunshade/slab bands read A8/A9, depths graphical±.10.
  bx(name+'_outer_sunshade_band',a,b,outer-.42 if side<0 else outer-.02,outer+.02 if side<0 else outer+.42,fl+2.75,fl+2.93,1)
 # Recessed inner wall: local A19 types, NOT outer gallery glazing.
 inner=d if outlow else c;ins=-side
 patterns=[['D','B1','D']*4,['D','B1','D']*4,['D','B1','B1','B1','D','D','B1','B1','D','D','B1','D'],['D','B1','B1','B1','D','D','B1','D','D','B1','B1','D']]
 for f in range(n):
  fl=1.+3.24*f
  pattern=patterns[f] if name=='north_main' else ['D','B1','D']*4
  for j in range(bays):
   if (name=='northwest_short' and j==0) or (name=='southeast_short' and j==4):
    wa=x0+j*3.4+.18
    body=facade_window(body,name+'_unpaired_end_inner_C',wa,wa+3.04,inner,fl+.90,fl+2.64,ins,4,fl+2.30)
    continue
   typ=pattern[j%len(pattern)];wid=3.04 if typ=='B1' else 1.50
   cx=x0+(j+.5)*3.4
   body=facade_window(body,name+'_inner_'+typ,cx-wid/2,cx+wid/2,inner,fl+2.10,fl+2.64,ins,4 if typ=='B1' else 2)
   if typ=='D' and j%3==0:
    # Door type1 total264=210leaf+54transom; position from bay symbol registration±.15.
    da=x0+j*3.4+.20
    body=facade_window(body,name+'_inner_door_type1',da,da+1.20,inner,fl,fl+2.64,ins,1,fl+2.10)
 # A19B2 sill3.84m (not withdrawn2.84); schedule16short+24main=40.
 # Shortfivebay strips omit the unmatched farend bay; pairedfourbay highwalls remain.
 js=range(bays)
 if name=='northwest_short':js=range(1,5)
 if name=='southeast_short':js=range(0,4)
 for j in js:
  wa=x0+j*3.4+.18;fl=1.+(n-1)*3.24
  body=facade_window(body,name+'_B2_roof_clerestory',wa,wa+3.04,inner,fl+3.84,fl+4.44,ins,4)
 add(name+'_room_envelope',body,0)
 add(name+'_outward_falling_single_pitch_roof',yz([(c,z0-.24),(d,z1-.24),(d,z1),(c,z0)],a-.10,b+.10),2)
 # Five parallel source-visible roof tile strips abstracted, not exact tile counts.
 for y in np.arange(c+.35,d,.65):
  z=z0+(z1-z0)*(y-c)/(d-c)
  bx(name+'_tile_course_abstracted',a-.10,b+.10,y-.035,y+.035,z-.02,z+.035,2)
# Main inward galleries. Open upper volume, no curtainwall.
for n,x0,x1,ywall,yedge in [('south',13.6,54.4,11.7,13.9),('north',27.2,68.,29.1,26.9)]:
 lo,hi=sorted([ywall,yedge]);side=1 if yedge>ywall else -1
 for f in range(4):
  fl=.95+3.24*f
  bx(n+'_open_gallery_slab',x0-.06,x1+.06,lo-.10,hi+.10,fl-.24,fl,1)
  bx(n+'_gallery_edge_beam_band50cm',x0,x1,yedge-.13,yedge+.13,fl-.50,fl,1)
  # A9 guard100cm above walk; additional10 is slab reference, not addedheight.
  if f>0:
   bx(n+'_gallery_lower_curb',x0,x1,yedge-.12,yedge+.12,fl-.01,fl+.10,1)
   for zz in [.45,.86]:bx(n+'_open_gallery_rail',x0,x1,yedge-.07,yedge+.07,fl+zz,fl+zz+.14,6)
  for x in np.arange(x0,x1+.01,3.4):
   bx(n+'_gallery_column',x-.16,x+.16,yedge-.16,yedge+.16,fl-.25,fl+3.25 if f<3 else fl+2.85,1)
 # Lower independent slope over topgallery from room highwall to court loweave.
 top=14.20;low=13.50
 pts=[(ywall,top-.20),(yedge,low-.20),(yedge,low),(ywall,top)]
 add(n+'_gallery_roof_graphical_A8',yz(pts,x0-.10,x1+.10),2)
# Shortwing paired passage:3m open connection, threefloors, not extra rooms.
for name,x0,x1,y0,y1 in [('west_pair',3.4,17.,29.1,32.1),('east_pair',64.6,78.2,8.7,11.7)]:
 for f in range(3):
  fl=.95+3.24*f
  bx(name+'_open_passage_floor',x0-.06,x1+.06,y0-.10,y1+.10,fl-.24,fl,1)
  # Ends visibly open with100cm guard and masonrysidepiers.
  for x in [x0,x1]:
   if f>0:
    for z in [.45,.86]:bx(name+'_end_rail',x-.07,x+.07,y0,y1,fl+z,fl+z+.14,6)
   for y in [y0,y1]:bx(name+'_end_column',x-.15,x+.15,y-.15,y+.15,fl-.25,fl+3.24,0)
# Ground courtyard source A30prime: two open perforated bridge strips, not a solid courtyard.
for x0,x1 in [(23.8,27.2),(54.4,57.8)]:
 for a,b in [(x0+.53,x0+1.10),(x1-1.10,x1-.53)]:bx('ground_court_bridge_solid_edge',a,b,15.,25.80,.40,.95,1)
 for y in np.arange(15.,25.81,.42):bx('ground_court_bridge_abstracted_grating',x0+1.08,x1-1.08,y-.07,y+.07,.80,.95,1)
 # Narrow endlandings connect bridge to source groundcorridor zones.
 for ya,yb in [(13.8,15.05),(25.75,27.)]:bx('ground_bridge_end_landing',x0+.53,x1-.53,ya,yb,.40,.95,1)
# Courtyard upper bridges: direct plan spot levels3.83/7.07/10.31.
# End transition geometry deliberately pending separate source control, NOT ramp-invented.
for name,x0,x1 in [('west',23.8,27.2),('east',54.4,57.8)]:
 for y in [17.05,23.75]:
  for x in [x0,x1]:bx(name+'_court_bridge_column',x-.18,x+.18,y-.18,y+.18,-.06,10.33,1)
 for fl in [3.83,7.07,10.31]:
  bx(name+'_upper_bridge_source_EL',x0,x1,15.0,25.8,fl-.24,fl,1)
  for x in [x0+.07,x1-.07]:
   for z in [.45,.86]:bx(name+'_bridge_rail_graphical',x-.07,x+.07,15.0,25.8,fl+z,fl+z+.14,6)
   for y in np.arange(15.,25.81,1.35):bx(name+'_bridge_rail_post_graphical',x-.07,x+.07,y-.07,y+.07,fl-.03,fl+1.,6)
 # Retaining sides visible in A30prime ground-section, bounded depth not hiddenbasement.
 for x in [x0+.53,x1-.53]:bx(name+'_ground_bridge_edge_support',x-.10,x+.10,15.,25.8,-.06,.95,1)
# Tall cores are segmented, not whole9.55m depth raised to18.16.
for n,a,b,c,d,highc,highd,highx in [('southwest',6.37,12.16,5.6,15.15,5.6,11.7,1),('northeast',69.44,75.23,25.65,35.2,29.1,35.2,-1)]:
 body=box(a,b,c,d,-.06,13.80)
 # Tall toilet/water-tank section walls andsloping topframe: A8 direct16.96/18.16.
 za,zb=(16.96,18.16) if highx>0 else (18.16,16.96)
 top=xz([(a,13.75),(b,13.75),(b,zb),(a,za)],highc,highd)
 # Top bay visibly open-frame above local tanklid, not a solid flatbox.
 top=top-box(a+.25,b-.25,highc+.25,highd-.25,16.74,18.4)
 body=body+top
 hx=b if highx>0 else a
 body=body-box(hx-.30,hx+.30,highc+.35,highd-.35,17.15,17.95)
 # Stair-side lower roof/reference14.00 and1.20 parapetframe; graphicalregistration±.15.
 lowc,lowd=(11.7,15.15) if n=='southwest' else (25.65,29.1)
 bx(n+'_low_stair_roof14m',a,b,lowc,lowd,13.75,14.,2)
 for y in [lowc,lowd]:bx(n+'_low_roof_parapet_frame',a,b,y-.10,y+.10,14.,15.20,0)
 # A7tankcover3.75x6.02 is localinside cover, notwholecore.
 tx=(a+b)/2;ty=(highc+highd)/2
 bx(n+'_local_water_tank_lid_graphical_level',tx-1.875,tx+1.875,ty-3.01,ty+3.01,16.76,16.96,1)
 # A19F:70x234cm,sill30cm; source22groups,notallfaces.
 for f in range(4):
  fl=1.+3.24*f
  if n=='southwest':
   body=F_window(body,n+'_south_F',7.4,c,fl,-1)
   body=F_window(body,n+'_west_F',10.4,a,fl,-1,'y')
  else:
   body=F_window(body,n+'_north_F',74.2,d,fl,1)
   body=F_window(body,n+'_east_F',30.4,b,fl,1,'y')
 # A8externalstairvisibleplatformpattern: recessed darkface, NOT glazedcurtainwall or hiddenstairs.
 plane=a if n=='southwest' else b;side=-1 if n=='southwest' else 1
 ya,yb=lowc+.20,lowd-.20
 body=body-box(plane-.40,plane+.40,ya,yb,.15,12.95)
 back=plane-side*.32
 bx(n+'_external_stair_recess_not_glass',back-.12,back+.12,ya-.02,yb+.02,.13,12.97,6)
 for y in [ya,yb]:bx(n+'_stair_side_pier',plane-.10,plane+.10,y-.10,y+.10,.10,13.05,0)
 for z in [1.+j*1.62 for j in range(8)]:bx(n+'_visible_halflevel_platform_band_graphical',plane-.13,plane+.13,ya-.04,yb+.04,z-.12,z+.12,1)
 # Separate highhorizontalvent, notFwindow norupperopenframe; A8graphical±.15.
 yc=(highc+highd)/2-.75 if n=='northeast' else (highc+highd)/2+.75
 body=body-box(plane-.40,plane+.40,yc-.90,yc+.90,16.20,16.60)
 bx(n+'_high_horizontal_vent_dark_recess',back-.12,back+.12,yc-.92,yc+.92,16.18,16.62,6)
 for z in [16.20,16.60]:bx(n+'_vent_horizontal_frame',plane-.07,plane+.07,yc-.95,yc+.95,z-.06,z+.06,3)
 for y in [yc-.90,yc+.90]:bx(n+'_vent_side_frame',plane-.07,plane+.07,y-.06,y+.06,16.18,16.62,3)
 # Round high aperture visible on outer longface; diameter1m graphical±.15.
 yc=highc if n=='southwest' else highd
 hole=Manifold.cylinder(.8,.50,.50,48).rotate((90,0,0)).translate((b-.85 if highx>0 else a+.85,yc+.4,16.8))
 body=body-hole
 add(n+'_segmented_tall_core',body,0)
# Inner stair nuclei: sloping solidwall13.40→14.75, outer openframe15.86.
for n,a,b,c,d,up in [('northwest',18.49,23.85,25.46,29.1,True),('southeast',57.75,63.11,11.7,15.34,False)]:
 za,zb=(13.40,14.75) if up else (14.75,13.40)
 body=xz([(a,-.06),(b,-.06),(b,zb),(a,za)],c,d)
 for f in range(1,4):
  fl=1.+f*3.24
  body=F_window(body,n+'_inner_stair_F',19.3 if up else 62.3,c if up else d,fl,-1 if up else 1)
 add(n+'_sloping_stair_core',body,0)
 for x in [a,b]:bx(n+'_upper_open_frame_post',x-.10,x+.10,c,d,13.20,15.86,0)
 for y in [c,d]:bx(n+'_upper_open_frame_beam',a,b,y-.10,y+.10,15.66,15.86,0)
# A15 three-storey end entrance galleries, notfourlevelcourtyardbridges.
# SE coordinates; NW is the documented opposing plan placement, details remain bounded.
def entry(n,x0,flip=False):
 def Y(y):return 40.8-y if flip else y
 def eb(tag,a,b,c,d,z0,z1,mat=1):
  ya,yb=sorted([Y(c),Y(d)]);bx(n+tag,a,b,ya,yb,z0,z1,mat)
 for f in range(3):
  fl=.95+3.24*f
  eb('_rear_connecting_gallery',x0,x0+10.2,8.6,11.8,fl-.24,fl)
  if f>0:
   eb('_front_open_gallery_floor',x0+1.37,x0+8.71,3.,8.8,fl-.24,fl)
   # A15 entry gallery guard shown solid; notglasscurtainwall.
   eb('_entry_solid_guard',x0+1.37,x0+8.71,3.,3.20,fl-.02,fl+1.,1)
 # Four corner columns leavefrontopen.
 for x in [x0+1.37,x0+8.71]:
  for y in [3.,8.70]:eb('_entry_corner_column',x-.17,x+.17,y-.17,y+.17,-.06,10.67,0)
 eb('_entry_roof',x0+1.37,x0+8.71,3.,8.8,10.43,10.67)
 eb('_entry_roof_parapet60cm',x0+1.37,x0+8.71,3.,3.20,10.65,11.27)
 # A17direct450clearstepwidth;outer1020=170+680+170.
 a=x0+2.85;b=a+4.50
 for j in range(2):eb('_lower18cm_rise',a,b,2.70+j*.35,3.40,-.06,.05+(j+1)*.18)
 eb('_middle_platform_EL41',a-.25,b+.25,3.40,6.80,-.06,.41)
 for j in range(3):eb('_upper18cm_rise',a,b,6.80+j*.35,7.85,-.06,.41+(j+1)*.18)
 eb('_upper_platform_EL95',a-.25,b+.25,7.85,8.75,-.06,.95)
 # Nearsteps low sidewalls; exactsmalledgeprofilegraphical±.15.
 # Source A17 screen walls added separately; do not replace them with genericrails.
entry('southeast',54.4)
entry('northwest',17.,True)
# A17内側入口屏牆:170cm inset,not high room endwalls.
# Left circle supported by2B lookingleft; right matched by2m planopening.
# y1.7..7.9/center5.5 andzcenter1.95 are graphical±.15, R1.00 direct.
for x in [56.10,62.90]:
 wall=yz([(1.70,-.06),(7.90,-.06),(7.90,4.19),(7.60,4.19),(2.45,3.17),(1.70,3.17)],x-.125,x+.125)
 hole=Manifold.cylinder(.70,1.,1.,64).rotate((0,90,0)).translate((x-.35,5.50,1.95))
 add('SE_entry_inner_screen_with_R100_circle',wall-hole,0)
# OpposingNWscreengeometry not independentlydetailed: no mirroredcircleinvented.
# Fourlevel short connectors between outer stair cores and main inner galleries (A4-A6).
for n,a,b,c,d in [('SW',12.10,13.70,11.70,13.90),('NE',67.90,69.50,26.90,29.10)]:
 for f in range(4):
  fl=.95+f*3.24
  bx(n+'_core_gallery_connector',a,b,c,d,fl-.24,fl,1)
  if f>0:
   for y in [c,d]:
    for z in [.45,.86]:bx(n+'_connector_guard',a,b,y-.07,y+.07,fl+z,fl+z+.14,6)
# Bridge endsteps derived2x18cm from direct36cm level difference.
# Tread run35cm is bounded graphical reconstruction, not direct dimensioned detail.
for x0,x1 in [(23.8,27.2),(54.4,57.8)]:
 for bridge in [3.83,7.07,10.31]:
  # down from southern gallery tobridge; rise toward northern gallery
  for j in range(2):
   z=bridge+(2-j)*.18
   bx('south_bridge_end18cm_step_graphical_run',x0,x1,14.29+j*.35,14.66+j*.35,bridge-.27,z,1)
   z=bridge+(j+1)*.18
   bx('north_bridge_end18cm_step_graphical_run',x0,x1,25.79+j*.35,26.16+j*.35,bridge-.27,z,1)
  bx('south_bridge_gallery_joint',x0,x1,13.80,14.31,bridge+.12,bridge+.36,1)
  bx('north_bridge_gallery_joint',x0,x1,26.49,27.00,bridge+.12,bridge+.36,1)
# Local uncertainty limits remain in SOURCE-CONTROLS.json; no hidden interiors inferred.
solid=P[0]
for p in P[1:]:solid=solid+p
solid=solid.set_tolerance(.0001).simplify(.0001).translate((-40.8,-20.4,SHIFT)).scale((S,S,S))
m=solid.to_mesh64();v=np.asarray(m.vert_properties)[:,:3];f=np.asarray(m.tri_verts);materials=np.zeros(len(f),dtype=int)
for i,oid in enumerate(m.run_original_id):materials[m.run_index[i]//3:m.run_index[i+1]//3]=IDS[int(oid)]
m=Manifold(Mesh64(v.astype(np.float32).astype(np.float64),f.astype(np.uint64),face_id=np.arange(len(f),dtype=np.uint64),tolerance=.00001)).simplify(.00001).to_mesh64();materials=materials[np.asarray(m.face_id,dtype=int)]
t=trimesh.Trimesh(np.asarray(m.vert_properties)[:,:3].astype(np.float32).astype(np.float64),np.asarray(m.tri_verts),process=False);t.merge_vertices(digits_vertex=4);keep=t.nondegenerate_faces();materials=materials[keep];t.update_faces(keep);t.remove_unreferenced_vertices()
np.savez_compressed(R/'mesh.npz',vertices=t.vertices,faces=t.faces,materials=materials);t.export(R/'model.stl');(R/'palette.json').write_text(json.dumps(PALETTE));(R/'components.json').write_text(json.dumps(LOG,ensure_ascii=False,indent=2))
q={'status':'WIP_PARTIAL_GEOMETRY_NOT_RELEASE','triangles':len(t.faces),'watertight':bool(t.is_watertight),'scale':'1:350','bounds_mm':t.bounds.tolist(),'mesh_sha256':hashlib.sha256((R/'mesh.npz').read_bytes()).hexdigest()};(R/'BUILD-QA.json').write_text(json.dumps(q,indent=2));print(json.dumps(q))
