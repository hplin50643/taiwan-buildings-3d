"""HSNU indoor pool: 2019 design interpretation, not 2022 as-built/current survey.
WIP: source-placement model. No source scans or illustrations in public output.
Axes x:I→A (north→south), y:1→5 (west→east), metre units before1:250 print.
"""
from pathlib import Path
import json,hashlib,numpy as np,trimesh
from manifold3d import Manifold,Mesh64,CrossSection
from geometry_helpers import box,prism,perimeter_band
R=Path(__file__).resolve().parent
S=4.;BASE=.50
AX=[0,9.05,17.45,25.85,34.25,42.65,51.05,59.45,67.90]
AY=[0,9.10,18.10,27.10,33.20]
PALETTE=[('illustrative pale exterior','#D4D5CF'),('illustrative concrete','#B8BBB5'),('illustrative dark fascia','#666D70'),('illustrative frame','#BAC1C0'),('authored display support not terrain','#A6AEA0'),('opaque glazing illustration','#708D98'),('court illustrative turf','#7C9560'),('illustrative metal net','#9AA5A4')]
P=[];LOG=[];IDS={}
def add(n,m,mat=0):
 assert not m.is_empty(),n
 m=m.as_original();IDS[m.original_id()]=mat;P.append(m);LOG.append({'name':n,'material':mat,'bounds_m':list(m.bounding_box())})
def bx(n,a,b,c,d,e,f,mat=0):add(n,box(a,b,c,d,e,f),mat)
def xzsolid(pts,y0,y1):
 if sum(pts[i][0]*pts[(i+1)%len(pts)][1]-pts[(i+1)%len(pts)][0]*pts[i][1] for i in range(len(pts)))<0:pts=pts[::-1]
 return CrossSection([pts]).extrude(y1-y0).transform(((1,0,0,0),(0,0,1,y0),(0,1,0,0)))
# Wall offsets/thickness provisional graphical envelope, not axis bbox assertedasoutside.
OUT=[(-.30,-.30),(68.20,-.30),(68.20,27.40),(34.55,27.40),(34.55,33.50),(-.30,33.50)]
bx('authored_display_base',-5,74,-5,39,-BASE,0,4)
body=prism(OUT,.05,7.0)
# Two-storey north classrooms only, not whole pool volume raised toRF15.
body=body+box(-.30,12.55,-.30,27.40,6.98,11.10)
# Roofhouse east-side portion; outline pendingpixelcontrol, separatedfromlowroof.
body=body+box(-.30,20.80,27.10,33.50,6.98,14.90)
# Court podium highpoint+7.25 / edge+7.10: a shallow hipped drainage surface.
# Implemented as planar facets via convexhull, not a second enclosedstorey.
pts=np.array([[23.45,0,6.95],[67.9,0,6.95],[67.9,27.1,6.95],[23.45,27.1,6.95],[23.45,0,7.10],[67.9,0,7.10],[67.9,27.1,7.10],[23.45,27.1,7.10],[45.675,13.55,7.25]])
add('court_roof_edge710_centre725',Manifold.hull_points(pts),6)
# Surrounding wall and net sourceheightchain, details deliberately pendingfinalcalibration.
add('court_opaque_parapet125',perimeter_band([(23.25,-.20),(68.10,-.20),(68.10,27.30),(23.25,27.30)],.20,7.08,8.35),0)
# Facade openings follow plan bay sequence; framing subdivisions are graphic simplifications.
W=[]
def rectplane(cx,cy,dx,dy,w,dep,z0,z1,off=0):
 nx,ny=-dy,dx
 return prism([(cx+dx*u+nx*v,cy+dy*u+ny*v)for u,v in [(-w/2,off),(w/2,off),(w/2,off+dep),(-w/2,off+dep)]],z0,z1)
def opening(n,cx,cy,dx,dy,w,z0,z1,cols=4,rows=2):
 global body
 body=body-rectplane(cx,cy,dx,dy,w,.48,z0,z1,-.15)
 W.append((n,cx,cy,dx,dy,w,z0,z1,cols,rows))
# West poolface, not mirrored east: G–A alternating DW12/DW4, source-render shallow folds.
for i,(a,b) in enumerate(zip(AX[2:-1],AX[3:])):
 opening(('west_DW12' if i%2==0 else 'west_DW4')+'_bay'+str(i), (a+b)/2,-.30,1,0,b-a-.85,1.0,6.05,8,3)
# East wall only E–D,D–C,C–B plus B–A endDW7. Northern service strip remains opaque/recessed.
for i,(a,b) in enumerate(zip(AX[4:-1],AX[5:])):
 opening(('east_DW4' if i<3 else 'east_DW7')+'_bay'+str(i),(a+b)/2,27.40,-1,0,b-a-.85,1.0,6.05,8,3)
# Northern east service openings from A2-01, heights graphically bounded without windowdetail sheet.
opening('east_DW5_access',12.1,33.50,-1,0,3.4,1.0,3.80,4,2)
opening('east_W3_service',21.0,33.50,-1,0,2.4,3.30,4.10,3,1)
opening('east_W4_service',24.0,33.50,-1,0,2.0,3.30,4.10,2,1)
opening('service_end_D15',34.55,30.7,0,1,1.0,1.0,3.10,1,1)
# Southern end pool glazing partitions supported by plan and southwest perspective; fine divisions approximate.
opening('south_pool_end_glazing',68.20,13.55,0,1,25.70,1.,6.05,18,3)
# North classroom windows: section height150 and three classroombays; adjacentcorridor not filled as additionalclassroom.
for y0,y1 in zip(AY[:3],AY[1:4]):
 opening('north_classroom_upper_strip',-.30,(y0+y1)/2,0,-1,y1-y0-1.2,7.05,8.55,8,1)
 opening('north_ground_strip_graphic',-.30,(y0+y1)/2,0,-1,y1-y0-1.2,3.75,4.55,8,1)
opening('west_northclassroom_upper',5.7,-.30,1,0,7.6,7.05,8.55,8,1)
opening('west_northclassroom_lower_graphic',5.7,-.30,1,0,7.6,3.75,4.55,8,1)
# North-east public hall doors, localentrance levels retained rather than groundzero assumption.
opening('north_hall_DW1',-.30,30.15,0,-1,4.0,1.0,4.6,4,2)
opening('east_hall_DW2',5.5,33.50,-1,0,5.3,1.0,4.6,6,2)
# Courtyard-facing north classrooms; roomfront lines H, open exterior terrace beyondcorridor.
for y0,y1 in zip(AY[:3],AY[1:4]):opening('terrace_classroom_strip',12.55,(y0+y1)/2,0,1,y1-y0-1.1,7.80,9.30,8,1)
# Visible strip on east highroom outerface: small windows, not curtainwall.
# Highroom visibleopenings are cut in actualouter screen below, not buriedbehindblankpanels.
# A4-01 directouter screen: RF11.00+250=13.50; bottom7.05+150=8.55.
# Do not lift theactualroof11.10. Darkband colorboundary11.10 isgraphic, notELmeasurement.
bx('north_lowroof_outer_screen_direct_chain',-.90,-.64,-.65,27.4,8.55,13.50,0)
bx('north_lowroof_dark_fascia_graphic_color',-.93,-.88,-.65,27.4,11.10,13.50,2)
bx('north_lowroof_return_screen',-.90,12.75,-.65,-.40,10.75,13.50,0)
bx('north_lowroof_return_dark_graphic_color',-.93,12.75,-.68,-.63,11.10,13.50,2)
bx('lowroof_plate_to_external_screen',-.91,12.75,-.65,27.4,10.95,11.10,0)
for yy in [0,9.1,18.1,27.1]:bx('north_facade_return_pier_graphic',-.91,-.25,yy-.22,yy+.22,1.0,13.50,0)
# High screen: directplan170projection/1785span; height16.20±.15fromsectionprojection.
# Screen surface thickness and folds illustrative, not missingA4-06 detailaccuracy.
body=body+box(-1.70,-1.50,26.9,34.90,7.0,16.20)+box(-1.70,17.85,34.70,34.90,7.0,16.20)+box(17.65,17.85,33.30,34.90,7.0,16.20)
# Visiblep33 Northeast openings, graphicalposition/height±.25m; actualouterface not buriedwindows.
opening('high_screen_east_near_corner_strip',5.3,34.90,-1,0,4.5,9.10,10.10,5,1)
opening('high_screen_east_far_large_window',13.5,34.90,-1,0,5.3,8.20,10.10,5,2)
for yy in [29.1,32.2]:opening('high_screen_north_pair',-1.70,yy,0,-1,2.1,8.65,10.10,2,1)
bx('highscreen_cantilever_support',-1.7,20.825,26.9,34.9,6.85,7.05,0)
# Small highroof blueglazed grid is one roof surface, not five skylightvoids or solar panels.
body=body-box(-.05,20.60,27.35,33.25,14.81,15.0)
bx('high_roof_glazing_nominal1490',-.05,20.60,27.35,33.25,14.80,14.90,5)
for x in np.linspace(0,20.5,11):bx('high_roof_grid_transverse',x-.06,x+.06,27.35,33.25,14.89,14.98,3)
for y in np.linspace(27.35,33.25,5):bx('high_roof_grid_longitudinal',-.05,20.6,y-.06,y+.06,14.89,14.98,3)
# Visible external roof equipment only. Plan220/210 controls, simplified silhouettes, no internal systems.
# Tank length3.8 and heatpumpheight1.4 aregraphic estimates, not equipment fabrication dimensions.
for k,yy in enumerate([4.0754,7.2754,10.4754]):
 bx('HWT_external_support_'+str(k),2.3,6.1,yy-.85,yy+.85,11.08,11.28,1)
 tank=Manifold.cylinder(3.4,1.1,1.1,48).rotate((0,90,0)).translate((2.5,yy,12.35))
 for xx in [2.5,5.9]:tank=tank+Manifold.sphere(1,32).scale((.2,1.1,1.1)).translate((xx,yy,12.35))
 add('HWT_external_horizontal_silhouette_'+str(k),tank,0)
for k,yy in enumerate([3.8072,6.9072,10.0072]):
 bx('heatpump_external_box_graphic_'+str(k),8.0,10.1,yy-1.05,yy+1.05,11.08,12.50,1)
 for xx in [8.525,9.575]:
  for y in [yy-.525,yy+.525]:add('heatpump_top_fan_symbol',Manifold.cylinder(.04,.38,.38,24).translate((xx,y,12.49)),2)
# West exterior shallow foldedpanels graphicprojection.25±.15; not a deepzigzag wholewall.
for x in AX[2:]:
 add('west_shallow_folded_panel_graphic',xzsolid([(x-.65,1.0),(x+.25,1.0),(x+.85,7.0),(x-.05,7.0)],-.60,-.31),0)
# A2-01 publicentrance outline; DW1spot obscured, +.95 isexplicitcoordination notreadvalue.
# Treadcount schematic, not as-built stairdetail. No invented37cm threshold.
bx('north_DW1_platform_nominal095_uncertain_datum',-2.55,-.29,27.25,33.10,0,.95,1)
for k in range(5):
 z=.95-(k+1)*(.77/6)
 bx('north_entry_graphic_tread',-2.55-.24*(k+1),-2.55-.24*k,27.25,33.10,0,z,1)
bx('north_entry_local_paving018',-3.95,-3.70,27.1,33.25,0,.18,1)
# EastDW2 +95platform/+25outside aredirectspots; samegraphic stepdetail disclaimer.
bx('east_DW2_platform095',3.1,8.2,33.48,34.50,0,.95,1)
for k in range(4):
 bx('east_entry_graphic_tread',3.1,8.2,34.50+.28*k,34.50+.28*(k+1),0,.95-(k+1)*.14,1)
bx('east_entry_local_paving025',2.9,8.4,35.6,35.9,0,.25,1)
# East accessible approach: visible140+140-wide bands, return+.63 and end+.25/+.95.
# Exact x11.24/11.96 breakpoints are a coordination derived from1:12, not printedrunlengths.
# Upper rectangle purpose is unclear; no invented high planterwall/interior features.
bx('ramp_outer_low_approach025',9.05,11.25,34.90,36.30,0,.25,1)
add('ramp_outer_456cm_1in12_coordination',xzsolid([(11.24,0),(15.80,0),(15.80,.63),(11.24,.25)],34.90,36.30),1)
bx('ramp_G_return063',15.79,17.20,33.49,36.30,0,.63,1)
add('ramp_inner_384cm_1in12_coordination',xzsolid([(11.96,0),(15.80,0),(15.80,.63),(11.96,.95)],33.49,34.91),1)
bx('ramp_inner_high_approach095',8.15,11.97,33.49,34.91,0,.95,1)
def rail(n,x0,x1,y,z0,z1):
 # 1m railheight and .12m printablemembers schematic, not accessibilitydesign dimensions.
 add(n+'_top',xzsolid([(x0,z0+.88),(x1,z1+.88),(x1,z1+1),(x0,z0+1)],y-.06,y+.06),7)
 for xx in np.linspace(x0,x1,max(2,int((x1-x0)/1.0)+1)):
  zz=z0+(z1-z0)*(xx-x0)/(x1-x0)
  bx(n+'_post',xx-.06,xx+.06,y-.06,y+.06,max(0,zz-.03),zz+1,7)
rail('ramp_outer_guard_low',9.05,11.24,36.30,.25,.25)
rail('ramp_outer_guard_slope',11.24,15.80,36.30,.25,.63)
rail('ramp_return_guard',15.80,17.20,36.30,.63,.63)
rail('ramp_centre_lowdivider',11.96,15.80,34.90,.95,.63)
for yy in [33.55,34.9,36.25]:bx('ramp_return_end_guard',17.14,17.26,yy-.06,yy+.06,.60,1.63,7)
bx('ramp_return_end_rail',17.14,17.26,33.50,36.30,1.51,1.63,7)
# Northentry sideguards, not across doorway or stairmouth.
for yy in [27.25,33.10]:
 rail('north_entry_platform_guard',-2.55,-.30,yy,.95,.95)
 rail('north_entry_step_guard',-3.75,-2.55,yy,.18,.95)
# Eaststair sideguard, coarseprintableposts only.
for xx in [3.1,8.2]:
 for yy in [33.65,34.5,35.5]:
  zz=.95 if yy<=34.5 else .39
  bx('east_entry_guard_post',xx-.06,xx+.06,yy-.06,yy+.06,zz-.02,zz+1,7)
 pts=[(33.60,1.83),(34.50,1.83),(35.50,1.27),(35.50,1.39),(34.50,1.95),(33.60,1.95)]
 add('east_entry_guard_following_top',CrossSection([pts]).extrude(.12).transform(((0,0,1,xx-.06),(1,0,0,0),(0,1,0,0))),7)
# A-axis exterior narrowwalk only. Independentcarpark ramp/116siteequipment zone excluded.
bx('south_A_axis_walk095',68.18,70.20,.2,27.1,0,.95,1)
for y in np.arange(.3,27.0,1.2):bx('south_walk_printable_guard',70.10,70.22,y-.06,y+.06,.95,2.95,7)
bx('south_walk_guard_top',70.10,70.22,.2,27.1,2.83,2.95,7)
# Exterior court fence is deliberately coarse printable lattice, not exact wovenmesh.
for y in [-.10,27.20]:
 for x in np.linspace(23.35,68.0,46):bx('court_printable_net_vertical',x-.05,x+.05,y-.05,y+.05,8.30,11.85,7)
 for z in np.linspace(8.35,11.85,5):bx('court_printable_net_horizontal',23.30,68.05,y-.05,y+.05,z-.05,min(z+.05,11.85),7)
 for x in np.linspace(23.35,68.,10):bx('court_net_post',x-.09,x+.09,y-.09,y+.09,8.25,11.85,7)
for x in [23.35,68.0]:
 for y in np.linspace(-.10,27.20,29):bx('court_printable_net_end_vertical',x-.05,x+.05,y-.05,y+.05,8.30,11.85,7)
 for z in np.linspace(8.35,11.85,5):bx('court_printable_net_end_horizontal',x-.05,x+.05,-.15,27.25,z-.05,min(z+.05,11.85),7)
add('historical_pool_and_north_classroom_shell',body,0)
for n,cx,cy,dx,dy,w,z0,z1,cols,rows in W:
 add(n+'_opaque_glazing_infill',rectplane(cx,cy,dx,dy,w+.02,.18,z0-.01,z1+.01,.15),5)
 for u in np.linspace(-w/2,w/2,cols+1):add(n+'_frame',rectplane(cx+dx*u,cy+dy*u,dx,dy,.10,.28,z0,z1,-.04),3)
 for z in np.linspace(z0,z1,rows+1):add(n+'_rail',rectplane(cx,cy,dx,dy,w,.28,z-.05,z+.05,-.04),3)
solid=P[0]
for p in P[1:]:solid=solid+p
solid=solid.set_tolerance(.0001).simplify(.0001).translate((-33.95,-16.6,BASE)).scale((S,S,S))
m=solid.to_mesh64();v=np.asarray(m.vert_properties)[:,:3];f=np.asarray(m.tri_verts);materials=np.zeros(len(f),dtype=int)
for i,oid in enumerate(m.run_original_id):materials[m.run_index[i]//3:m.run_index[i+1]//3]=IDS[int(oid)]
# Quantize to STLfloat32 first, then remove sub-resolution degeneracy with original materialfaceIDs.
m=Manifold(Mesh64(v.astype(np.float32).astype(np.float64),f.astype(np.uint64),face_id=np.arange(len(f),dtype=np.uint64),tolerance=.00001)).simplify(.00001).to_mesh64();materials=materials[np.asarray(m.face_id,dtype=int)]
t=trimesh.Trimesh(np.asarray(m.vert_properties)[:,:3].astype(np.float32).astype(np.float64),np.asarray(m.tri_verts),process=False);t.merge_vertices(digits_vertex=5);keep=t.nondegenerate_faces();materials=materials[keep];t.update_faces(keep);t.remove_unreferenced_vertices()
np.savez_compressed(R/'mesh.npz',vertices=t.vertices,faces=t.faces,materials=materials);t.export(R/'model.stl');(R/'palette.json').write_text(json.dumps(PALETTE));(R/'components.json').write_text(json.dumps(LOG,ensure_ascii=False,indent=2))
q={'status':'WIP_SOURCE_PLACEMENT_NOT_RELEASE','triangles':len(t.faces),'watertight':bool(t.is_watertight),'scale':'1:250','bounds_mm':t.bounds.tolist(),'mesh_sha256':hashlib.sha256((R/'mesh.npz').read_bytes()).hexdigest()};(R/'BUILD-QA.json').write_text(json.dumps(q,indent=2));print(json.dumps(q))
