"""CCCK253, July1976 original design interpretation. Not current/as-built.
Metres: localGL=EL255.00; FF+0.16, 3.50m storeys. Print scale1:200.
Architectural plans/schedules govern bathroom-window conflict with A3 elevation.
"""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
from manifold3d import Manifold
R=Path(__file__).resolve().parent;P=[];LOG=[];IDS={}
PALETTE=[('approximate neutral washed aggregate','#C3C0AE'),('approximate mosaic tile selected sample unknown','#DDD9C9'),('opaque backed aluminum glazing','#617D83'),('neutral aluminum frame','#C5CAC6'),('recessed corridor surface','#B6B1A3'),('door leaf approximate neutral','#8B897A'),('authored display terrain','#A5AA94'),('roof waterproofing approximate','#8B8F86')]
def box(a,b,c,d,e,f):return Manifold.cube((b-a,d-c,f-e)).translate((a,c,e))
def add(n,m,mat=0):
 assert not m.is_empty(),n
 m=m.as_original();IDS[m.original_id()]=mat;P.append(m);LOG.append({'name':n,'material':mat,'bounds_m':list(m.bounding_box())})
def bx(n,a,b,c,d,e,f,mat=0):add(n,box(a,b,c,d,e,f),mat)
X0=-.150;X1=42.150;Y0=-.115;YN=6.500;BYN=5.900;ROOM_N=4.60;STAIR=38.5
FF=[.16+3.5*i for i in range(4)];RF=14.16
def bay_center(b):return 1.7325 if b==0 else (40.2675 if b==11 else 1.75+3.5*b)
# Base with a graphical north-side sunken basement lightwell. Not surveyed terrain.
bx('authored_display_plinth',-2,44,-2.5,10,-4.0,-3.55,6)
bx('south_display_grade',-2,44,-2.5,Y0+.05,-3.56,0,6)
bx('west_display_grade',-2,X0+.05,Y0-.05,10,-3.56,0,6);bx('east_display_grade',X1-.05,44,Y0-.05,10,-3.56,0,6)
bx('north_lightwell_display_bottom',X0-.20,X1+.20,BYN-.05,10,-3.56,-1.05,6)
# Basement closed backing; glazing exposed only in shallow north lightwell.
bx('basement_closed_backing_EL25186',-.15,42.15,-.115,BYN,-3.60,.15,0)
# Main room block is sealed for fabrication; east staircase bay remains visible through corridor.
room=box(X0,STAIR,Y0,ROOM_N,.13,RF-.13)
for z in FF:
 for bay in range(11):
  cx=bay_center(bay);sill=2.05 if bay<3 else .90;h=.85 if bay<3 else 2.0
  room=room-box(cx-.75,cx+.75,-.25,.06,z+sill,z+sill+h)
add('sealed_room_block_11bays_backed_window_recesses',room,1)
wall=box(STAIR,X1,Y0,.15,.13,RF)
for z in FF:wall=wall-box(39.5175,41.0175,-.25,.06,z+.90,z+2.90)
add('east_stair_south_wall_backed_window_recesses',wall,1)
bx('east_stair_east_end_wall',X1-.23,X1,.15,YN,.13,RF,1)
bx('west_end_wall',X0,X0+.23,ROOM_N,YN,.13,RF,1)
# Four floor plates follow finished walking surfaces; structural top is3cm lower.
for i,z in enumerate(FF):
 slab=box(X0,X1,Y0,YN,z-.16,z)
 if i>0:slab=slab-box(STAIR+.30,X1-.30,.40,4.25,z-.20,z+.04)
 add(f'floor_{i+1}_plate_FF_{z:.2f}',slab,0)
 bx(f'north_corridor_{i+1}_surface',X0+.23,X1-.23,ROOM_N,YN-.20,z-.025,z+.005,4)
 # Open cantilever corridor: no invented full-height outer column row.
 bx(f'north_corridor_{i+1}_104cm_parapet_print20cm',X0,X1,YN-.20,YN,z-.05,z+1.04,1)
 for j in range(13):
  x=max(X0,min(X1-.08,j*3.5));bx(f'corridor_{i+1}_parapet_joint_{j}',x,x+.05,YN-.211,YN+.009,z,z+1.04,0)
# Roof full plate, no unsupported invented penthouse or tank.
bx('roof_plate_RF1416',X0,X1,Y0,YN,RF-.16,RF,0)
bx('roof_drainage_surface_simplified',X0+.20,X1-.20,Y0+.20,YN-.20,RF-.01,RF+.02,7)
for name,a,b,c,d in [('north',X0,X1,YN-.20,YN),('west',X0,X0+.20,Y0,YN),('east',X1-.20,X1,Y0,YN)]:bx('roof_90cm_parapet_'+name,a,b,c,d,RF-.03,RF+.90,1)
# South serrated parapet/roof edge followsA2, continuous10cm fins followA3/A4.
prev=X0
for bay in range(12):
 lo=bay_center(bay)-.85;hi=bay_center(bay)+.85
 bx(f'roof_south_between_bays_{bay}',prev,lo,Y0,Y0+.20,RF-.03,RF+.90,1)
 bx(f'roof_south_projected_bay_slab_{bay}',lo,hi,-.415,Y0+.20,RF-.16,RF,0)
 bx(f'roof_south_projected_parapet_{bay}',lo,hi,-.415,-.215,RF-.03,RF+.90,1)
 for xx in [lo,hi-.10]:bx(f'roof_south_parapet_return_{bay}',xx,xx+.10,-.415,Y0+.20,RF-.03,RF+.90,1)
 prev=hi
bx('roof_south_last_end',prev,X1,Y0,Y0+.20,RF-.03,RF+.90,1)
# Detailed south projecting surrounds;glassdatum isgraphicallyestimatedwithinmainwall.
PROJECT=-.415;GLASS=0.0
for level,z in enumerate(FF):
 for bay in range(12):
  cx=bay_center(bay);lo=cx-.75;hi=cx+.75
  sill=2.05 if bay<3 else .90;h=.85 if bay<3 else 2.0
  # Projecting side fins continue vertically; outer sill covers raised opaque spandrel.
  for x in [lo-.10,hi]:bx(f'south_bay{bay}_L{level}_sidefin',x,x+.10,PROJECT,.05,z,z+3.5,1)
  bx(f'south_bay{bay}_L{level}_sillbox',lo,hi,PROJECT,.05,z-.02,z+.90,1)
  bx(f'south_bay{bay}_L{level}_glazing',lo,hi,GLASS-.04,.08,z+sill,z+sill+h,2)
  for x in [lo,hi-.055,cx-.0275]:bx(f'south_window_jamb_{bay}_{level}',x,x+.055,GLASS-.07,GLASS+.02,z+sill,z+sill+h,3)
  for zz in [z+sill,z+sill+h]+([] if bay<3 else [z+sill+1.2]):bx(f'south_window_transom_{bay}_{level}',lo,hi,GLASS-.07,GLASS+.02,zz-.0275,zz+.0275,3)
  bx(f'south_window_top_lintel_{bay}_{level}',lo,hi,Y0,.05,z+sill+h,z+3.5,1)
# North room-side door transoms and bathroom ventilators, recessed behind open gallery.
for level,z in enumerate(FF):
 for bay in range(1,11):
  if bay in [0,2]:continue
  x=bay*3.5+.45
  bx(f'north_D1_leaf_{bay}_{level}',x,x+.90,ROOM_N-.015,ROOM_N+.055,z,z+2.10,5)
  bx(f'north_D1_fanlight_{bay}_{level}',x,x+.90,ROOM_N-.015,ROOM_N+.055,z+2.10,z+2.90,2)
  for xx in [x,x+.86]:bx(f'north_D1_frame_{bay}_{level}',xx,xx+.04,ROOM_N+.045,ROOM_N+.085,z,z+2.90,3)
  for zz in [z+2.10,z+2.90]:bx(f'north_D1_transom_{bay}_{level}',x,x+.90,ROOM_N+.045,ROOM_N+.085,zz-.025,zz+.025,3)
 for bay in [0,2]:
  x=bay*3.5+.15;bx(f'north_bath_W3_{bay}_{level}',x,x+3.20,ROOM_N-.015,ROOM_N+.055,z+2.05,z+2.90,2)
  for xx in [x,x+.80,x+1.6,x+2.4,x+3.15]:bx(f'north_W3_mullion_{bay}_{level}',xx,xx+.05,ROOM_N+.045,ROOM_N+.09,z+2.05,z+2.90,3)
  for zz in [z+2.05,z+2.90]:bx(f'north_W3_edge_{bay}_{level}',x,x+3.20,ROOM_N+.045,ROOM_N+.09,zz-.025,zz+.025,3)
# Basement W4 strip from plan, displayed with sealed glazing and a recessed terrain lightwell.
for bay in range(2,10):
 x=bay*3.5+.15;w=3.20
 if bay==2:x+=1.60;w=1.60
 bx(f'basement_W4_backed_{bay}',x,x+w,BYN-.015,BYN+.06,-.85,-.20,2)
 for xx in np.linspace(x,x+w-.05,3 if bay==2 else 5):bx(f'basement_W4_mullion_{bay}',xx,xx+.05,BYN+.045,BYN+.09,-.85,-.20,3)
 for z in [-.85,-.20]:bx(f'basement_W4_edge_{bay}',x,x+w,BYN+.045,BYN+.09,z-.025,z+.025,3)
# Two end ground doors at the corridor edge, as shown in A3; no repeated end windows.
for side,x0,x1 in [('west',X0-.06,X0+.02),('east',X1-.02,X1+.06)]:
 bx(side+'_end_door_backing',x0,x1,YN-1.55,YN-.35,.16,2.56,5)
 for yy in [YN-1.55,YN-.40]:bx(side+'_door_jamb',x0-.02,x1+.02,yy,yy+.05,.16,2.56,3)
 bx(side+'_door_head',x0-.02,x1+.02,YN-1.55,YN-.35,2.51,2.56,3)
# Simplified visible dogleg stair flights within source eastmost bay,21 risers/storey.
for level,z in enumerate(FF[:-1]):
 bx(f'stair_{level}_middle_landing',STAIR+.22,X1-.22,.35,1.55,z+1.62,z+1.75,0)
 for k in range(10):
  y=4.25-(k+1)*.27;bx(f'stair_{level}_lower_{k}',STAIR+.25,STAIR+1.55,y,y+.29,z-.03,z+(k+1)*.175,0)
 for k in range(11):
  y=1.55+k*(2.7/11);bx(f'stair_{level}_upper_{k}',STAIR+1.70,X1-.25,y,y+2.7/11+.015,z+1.60,z+1.75+(k+1)*(1.75/11),0)
solid=P[0]
for p in P[1:]:solid=solid+p
solid=solid.translate((-21,-3.5,4.0)).scale((5,5,5)).simplify(.0001)
m=solid.to_mesh64();v=np.asarray(m.vert_properties)[:,:3];f=np.asarray(m.tri_verts);materials=np.zeros(len(f),dtype=int)
for i,oid in enumerate(m.run_original_id):materials[m.run_index[i]//3:m.run_index[i+1]//3]=IDS[int(oid)]
t=trimesh.Trimesh(v,f,process=False);t.merge_vertices(digits_vertex=13);assert t.is_watertight and t.is_winding_consistent;assert len(t.split())==1,(len(t.split()),'detached geometry')
np.savez_compressed(R/'mesh.npz',vertices=t.vertices,faces=t.faces,materials=materials);t.export(R/'model.stl');(R/'palette.json').write_text(json.dumps(PALETTE));(R/'components.json').write_text(json.dumps(LOG,ensure_ascii=False,indent=2))
q={'status':'PASS_GEOMETRY_ONLY','triangles':len(t.faces),'components':len(t.split()),'watertight':bool(t.is_watertight),'winding':bool(t.is_winding_consistent),'scale':'1:200','bounds_mm':t.bounds.tolist(),'mesh_sha256':hashlib.sha256((R/'mesh.npz').read_bytes()).hexdigest()};(R/'BUILD-QA.json').write_text(json.dumps(q,indent=2));print(json.dumps(q))
