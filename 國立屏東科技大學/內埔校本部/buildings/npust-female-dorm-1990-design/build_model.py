"""CCCK439 female dormitory, 1990-08-31 design interpretation. Not as-built.
Coordinates metres, x axes1..20, yA..F, GL=0. Scale1:300.
Female A2 controls geometry; shared A4 does NOT control basement location.
"""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
from manifold3d import Manifold
R=Path(__file__).resolve().parent;P=[];LOG=[];IDS={}
PALETTE=[('neutral approximate structural concrete','#BDBBAE'),('selected mosaic color unknown approximate ivory','#DEDACB'),('opaque backed plastic-steel glazing','#647E86'),('neutral window frame approximate','#C5CBC6'),('roof drainage approximate','#999D91'),('entry door neutral approximate','#8B8B7D'),('authored display terrain','#A5AA94'),('contrasting vertical strip color unknown','#A09D8E')]
def box(a,b,c,d,e,f):return Manifold.cube((b-a,d-c,f-e)).translate((a,c,e))
def add(n,m,mat=0):
 assert not m.is_empty(),n
 m=m.as_original();IDS[m.original_id()]=mat;P.append(m);LOG.append({'name':n,'material':mat,'bounds_m':list(m.bounding_box())})
def bx(n,a,b,c,d,e,f,mat=0):add(n,box(a,b,c,d,e,f),mat)
FF=[.65+3.5*i for i in range(4)];RF=14.65;S=1000/300
# Finished wall centre offsets fromA2-3: .135, 5.955+2.92+5.955=14.83.
# Nominal23cm wall. End-wall centre on axis is graphical, not exact finish survey.
X0=-.115;X1=39.715;X2=28.685;X3=68.515
Y0=.020;Y1=15.080;Y2=9.220;Y3=24.280
body=box(X0,X1,Y0,Y1,-.02,RF-.15)+box(X2,X3,Y2,Y3,-.02,RF-.15)
# A2-1 L-shaped basement, not mirrored male section. Closed interior under terrain.
basebody=box(-.125,36.125,5.775,15.225,-3.65,.50)+box(-.125,18.125,-.125,5.90,-3.65,.50)
add('female_basement_L_closed_A2_1_BFL_minus350',basebody,0)
bx('authored_display_plinth',-2,70.4,-2,28.6,-3.80,-3.60,6)
bx('authored_grade_hides_basement_not_survey',-2,70.4,-2,28.6,-3.61,0,6)
# Face openings: n/s coordinate is x, e/w coordinate is y. Cut shallow recess,
# backed glazing overlaps body behind recess; no air-gap shell or invented interiors.
OPEN=[]
def opening(n,side,face,c,w,z,h,typ='W1'):
 global body
 lo=c-w/2;hi=c+w/2;sgn=1 if side in ['n','e'] else -1
 if side in ['n','s']:
  a,b=sorted([face-sgn*.17,face+sgn*.06]);cut=box(lo,hi,a,b,z,z+h)
 else:
  a,b=sorted([face-sgn*.17,face+sgn*.06]);cut=box(a,b,lo,hi,z,z+h)
 body=body-cut;OPEN.append((n,side,face,c,w,z,h,typ))
# Four exposed longfacade segments; bathroom W4 strips at outermost endbays.
segments=[('south_A','s',Y0,0,11),('north_D','n',Y1,0,8),('north_F','n',Y3,8,19),('south_C','s',Y2,11,19)]
for level,z in enumerate(FF):
 for nm,side,face,start,end in segments:
  for bay in range(start,end):
   c=3.6*(bay+.5);typ='W4' if bay in [0,18] else 'W1';w=3.2 if typ=='W4' else 1.4;h=.55 if typ=='W4' else 1.75;sill=2.10 if typ=='W4' else .90
   if level==0 and nm in ['south_A','south_C'] and bay in [1,17]:continue
   if level==0 and nm=='north_F' and bay==9:continue # main entrance, separate below
   # Ground lounge exterior retains W1; W6/W7 are internal corridor openings.
   opening(f'{nm}_{level}_bay{bay+1}_{typ}',side,face,c,w,z+sill,h,typ)
 # Outer end baths: W2 highvents in corridor-zone, NOT W3.
 opening(f'west_outer_W2_{level}','w',X0,7.55,2.2,z+2.1,.55,'W2')
 opening(f'east_outer_W2_{level}','e',X3,16.75,2.2,z+2.1,.55,'W2')
 # Step endfaces show the broad corridor windows seen in end elevations.
 opening(f'west_step_W3_{level}','w',X2,16.75,2.2,z+.9,1.75,'W3')
 opening(f'east_step_W3_{level}','e',X1,7.55,2.2,z+.9,1.75,'W3')
for nm,face,bay in [('west',Y0,1),('east',Y2,17)]:
 opening(nm+'_ground_stair_W4','s',face,3.6*(bay+.5),3.2,2.75,.55,'W4')
 opening(nm+'_ground_stair_D5','s',face,3.6*bay+.70,1.0,.20,2.10,'D5')
# North vestibule is open atF, door lies graphically2.5m inside.
body=body-box(32.525,35.875,21.77,24.60,.44,3.30)
opening('recessed_main_DW1','n',21.78,34.2,3.35,.65,2.65,'DW1')
add('four_storey_staggered_closed_backing',body,1)
for n,side,face,c,w,z,h,typ in OPEN:
 sign=1 if side in ['n','e'] else -1;lo=c-w/2;hi=c+w/2
 def fb(name,l,r,d0,d1,z0,z1,ma):
  a,b=sorted([face+sign*d0,face+sign*d1])
  if side in ['n','s']:bx(n+'_'+name,l,r,a,b,z0,z1,ma)
  else:bx(n+'_'+name,a,b,l,r,z0,z1,ma)
 fb('sealed_glazing',lo,hi,-.205,-.145,z,z+h,5 if typ in ['DW1','D5'] else 2)
 for k,x in enumerate([lo,hi-.06]+([] if typ=='D5' else [c-.03])):fb('frame_'+str(k),x,x+.06,-.16,-.10,z,z+h,3)
 horizontal=[z,z+h]
 if typ in ['W1','W3']:horizontal.append(z+1.2)
 if typ=='W6':horizontal.append(z+2.55)
 if typ=='DW1':horizontal.append(z+2.1)
 for k,zz in enumerate(horizontal):fb('transom_'+str(k),lo,hi,-.16,-.10,zz-.03,zz+.03,3)
 # Recess surrounded by source12cmRC thin wrap, depth graphicalapproximation.
 for k,x in enumerate([lo-.12,hi]):fb('RC_side_'+str(k),x,x+.12,-.17,.10,z-.08,z+h+.08,1)
 fb('RC_sill',lo-.12,hi+.12,-.17,.10,z-.12,z,1)
# Slab/floor bands follow continuous outer faces, source widths approximated.
for k,z in enumerate(FF+[RF]):
 bx(f'southwing_floorband_{k}',-.175,39.775,-.275,15.375,z-.20,z,0)
 plate=box(28.625,68.575,8.925,24.575,z-.20,z)
 if k==0:plate=plate-box(32.525,35.875,21.77,24.60,z-.25,z+.05)
 add(f'northwing_floorband_{k}',plate,0)
# External columns, graphical35x55cm, retained separately from wall-centre dimensions.
for nm,side,face,start,end in segments:
 y=0 if nm=='south_A' else (15.1 if nm=='north_D' else (24.3 if nm=='north_F' else 9.2))
 for j in range(start,end+1):bx(f'{nm}_external_column_axis{j+1}',j*3.6-.175,j*3.6+.175,y-.275,y+.275,.45,RF+.02,7)
# Roof footprint outer straight parapet. Internal zigzags onA2-4 are roof drains,
# NOT serrated outside wall. Thin10cm parapet thickened inward to18cm for display.
for name,a,b,c,d in [('southwing',-.175,39.775,-.275,15.375),('northwing',28.625,68.575,8.925,24.575)]:bx(name+'_roof_surface',a+.18,b-.18,c+.18,d-.18,RF-.02,RF+.025,4)
outline=[(-.175,-.275),(39.775,-.275),(39.775,8.925),(68.575,8.925),(68.575,24.575),(28.625,24.575),(28.625,15.375),(-.175,15.375)]
# inward side known from counterclockwise outline
for i,((a,b),(c,d)) in enumerate(zip(outline,outline[1:]+outline[:1])):
 if b==d:
  sy=1 if c>a else -1;y0,y1=sorted([b,b+sy*.18]);bx(f'roof_parapet120_{i}',min(a,c),max(a,c),y0,y1,RF-.04,15.85,1)
 else:
  sx=-1 if d>b else 1;x0,x1=sorted([a,a+sx*.18]);bx(f'roof_parapet120_{i}',x0,x1,min(b,d),max(b,d),RF-.04,15.85,1)
# Thirty-two explicitly labelled100cm column stubs, not tanks.
for wing,rows,axes in [('south',[5.9,9.2],range(3,11)),('north',[15.1,18.4],range(9,17))]:
 for y in rows:
  for j in axes:bx(f'{wing}_roof_stub_{j+1}_{y}',j*3.6-.175,j*3.6+.175,y-.275,y+.275,RF-.03,RF+1,0)
# Two373/375cm wall-centre-width roofstair enclosures. EndpointsA..C/C..E from roof plan,
# wall-centre depth907.5cm from written dimension; small finishoffsets retained.
for nm,x,y,cw in [('west',3.6,0,3.73),('east',61.2,9.2,3.75)]:
 left=x-(cw-3.6)/2-.06;right=x+3.6+(cw-3.6)/2+.06
 inner=y+9.1375-1.56
 bx(nm+'_stairhead_closed',left,right,y+.0025,inner+.06,RF-.04,17.45,1)
 bx(nm+'_stairhead20cm_roof',left-.03,right+.03,y-.0275,y+9.2275,17.45,17.65,0)
 # A4 open roof-covered156cm north porch: no invented fullheight exterior wall.
 for xx in [left,right-.20]:bx(nm+'_porch_corner_post',xx,xx+.20,y+8.9975,y+9.1975,RF-.03,17.50,0)
 bx(nm+'_porch_top_beam',left,right,y+8.9975,y+9.1975,17.20,17.50,0)
 bx(nm+'_porch_floor_plus30',left,right,inner-.02,y+9.1975,RF-.03,RF+.30,0)
 # A2-4 D3 and210x55 window share the recessed north wall; naming followslocalcallout.
 bx(nm+'_roof_D3_backed',left+.12,left+1.12,inner+.04,inner+.105,RF+.30,RF+2.40,5)
 for xx in [left+.12,left+1.06]:bx(nm+'_D3_jamb',xx,xx+.06,inner+.095,inner+.13,RF+.30,RF+2.4,3)
 bx(nm+'_D3_head',left+.12,left+1.12,inner+.095,inner+.13,RF+2.34,RF+2.4,3)
 wx=left+1.30
 bx(nm+'_roof_local_W2_210x55',wx,wx+2.10,inner+.04,inner+.105,RF+2.20,RF+2.75,2)
 for xx in [wx,wx+1.02,wx+2.04]:bx(nm+'_roof_window_frame',xx,xx+.06,inner+.095,inner+.13,RF+2.2,RF+2.75,3)
 for zz in [RF+2.20,RF+2.75]:bx(nm+'_roof_window_edge',wx,wx+2.10,inner+.095,inner+.13,zz-.03,zz+.03,3)
# Main entry: explicit45cm landing,65cm interior; ramp665x150,1:14.
# +45 versus nominal665/14=47.5 discrepancy retained as ramp foot-2.5cm.
# Vestibule depth2.5m and site placement are graphical estimates.
def wedge(n,x0,x1,y0,y1,z0,z1,along='x'):
 pts=[]
 for x,y in [(x0,y0),(x1,y0),(x1,y1),(x0,y1)]:
  top=z0+(z1-z0)*((x-x0)/(x1-x0) if along=='x' else (y-y0)/(y1-y0))
  pts.extend([(x,y,-.04),(x,y,top)])
 add(n,Manifold.hull_points(pts),0)
wedge('entry_vestibule_slope_65_to45',32.525,35.875,21.77,25.90,.65,.45,'y')
bx('entry_45cm_landing',32.4,36.0,25.85,27.40,-.04,.45,0)
for k in range(3):bx(f'entry_north_step_{k}',32.55,35.85,27.40+k*.30,27.70+k*.30,-.04,.45-(k+1)*.15+.005,0)
wedge('east_access_ramp_665cm_1to14',35.99,42.65,25.90,27.40,.45,-.025)
# Low15cm-wide rampcurbs approximate15cm height, not fabricatedhandrailcompliance.
for yy in [25.75,27.40]:
 wedge('ramp_low_curb',35.99,42.65,yy,yy+.15,.60,.125)
for nm,face,bay in [('west',Y0,1),('east',Y2,17)]:
 bx(nm+'_D5_landing',3.6*bay+.05,3.6*bay+1.35,face-.60,face+.05,-.03,.20,0)
 bx(nm+'_D5_step',3.6*bay+.05,3.6*bay+1.35,face-.90,face-.55,-.03,.10,0)
solid=P[0]
for p in P[1:]:solid=solid+p
solid=solid.translate((-34.2,-12.9,3.8)).scale((S,S,S)).simplify(.0001)
m=solid.to_mesh64();v=np.asarray(m.vert_properties)[:,:3];f=np.asarray(m.tri_verts);materials=np.zeros(len(f),dtype=int)
for i,oid in enumerate(m.run_original_id):materials[m.run_index[i]//3:m.run_index[i+1]//3]=IDS[int(oid)]
t=trimesh.Trimesh(v,f,process=False);t.merge_vertices(digits_vertex=12)
# Remove numerical degenerate triangles after seam merge, keep material alignment.
keep=t.nondegenerate_faces();materials=materials[keep];t.update_faces(keep);t.remove_unreferenced_vertices()
# Boolean floating-point coincidence can retain a zero-volume coplanar tetrahedron.
# Remove ONLY isolated closed pieces with subnanometre thickness and zero volume.
keep=np.ones(len(t.faces),dtype=bool);removed=0
for idx in trimesh.graph.connected_components(t.face_adjacency,nodes=np.arange(len(t.faces))):
 c=t.submesh([idx],append=True)
 if len(idx)<=8 and min(c.extents)<1e-9 and abs(c.volume)<1e-10:
  keep[idx]=False;removed+=len(idx)
materials=materials[keep];t.update_faces(keep);t.remove_unreferenced_vertices()
assert t.is_watertight and t.is_winding_consistent;assert len(t.split())==1,[(len(c.faces),c.bounds.tolist(),c.volume) for c in t.split()]

np.savez_compressed(R/'mesh.npz',vertices=t.vertices,faces=t.faces,materials=materials);t.export(R/'model.stl');(R/'palette.json').write_text(json.dumps(PALETTE));(R/'components.json').write_text(json.dumps(LOG,ensure_ascii=False,indent=2))
q={'status':'PASS_GEOMETRY_ONLY','numerical_zero_volume_faces_removed':removed,'triangles':len(t.faces),'components':len(t.split()),'watertight':bool(t.is_watertight),'winding':bool(t.is_winding_consistent),'scale':'1:300','bounds_mm':t.bounds.tolist(),'mesh_sha256':hashlib.sha256((R/'mesh.npz').read_bytes()).hexdigest()};(R/'BUILD-QA.json').write_text(json.dumps(q,indent=2));print(json.dumps(q))
