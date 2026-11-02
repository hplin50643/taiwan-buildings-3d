"""Kungtung south service block1960 bounded exterior reconstruction.
Units metres, 1FL=0; x0 west, y0 south. NOT a present survey.
Local exterior grade is not reconstructed; support is authored, basement hidden.
"""
from pathlib import Path
import json,hashlib,numpy as np,trimesh
from manifold3d import Manifold,Mesh64,CrossSection
from geometry_helpers import box,prism
R=Path(__file__).resolve().parent
S=1000/150;SHIFT=.50;P=[];LOG=[];IDS={}
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
# Authored support, not historical terrain. Hidden basement not reconstructed.
bx('authored_display_support_not_terrain',-1.10,25.15,-2.0,11.50,-SHIFT,-.05,4)
bx('ground_floor',0,22.05,0,10.50,-.10,0,1)
bx('east_firecourt_local_Fminus4cm',22.04,24.05,0,10.50,-.10,-.04,1)
# Ground east2m is covered exterior firecourt, not an enclosed room.
body=box(0,3.20,0,10.50,-.06,6.48)+box(5.75,22.05,0,10.50,-.06,3.45)+box(5.75,24.05,0,10.50,3.44,6.55)
bx('upper_floor_main',5.74,24.05,0,10.50,3.25,3.45,1)
bx('open_stair_north_full_landing',3.19,5.76,5.00,10.50,3.25,3.45,1)
bx('open_stair_south_half_landing',3.19,5.76,1.20,2.515,1.545,1.725,1)
# Source 20risers=10+10; each run9treads28cm, not252/10.
def flight10(n,x0,x1,reverse=False):
 top=[(2.50,0),(2.50,.1725)]
 for i in range(1,10):top.extend([(2.50+i*.28,i*.1725),(2.50+i*.28,(i+1)*.1725)])
 pts=[(2.50,-.17),(5.02,1.555)]+top[::-1]
 if reverse:pts=[(7.52-y,1.725+z) for y,z in pts]
 else:pts=[(7.52-y,z) for y,z in pts]
 # First west rises north-to-south; return east rises south-to-north.
 if reverse:pts=[(7.52-y,z) for y,z in pts]
 add(n,yz(pts,x0,x1),1)
flight10('west_lower10_risers9treads',3.20,4.40)
flight10('east_upper10_risers9treads',4.55,5.75,True)
bx('stair_central_partition15cm',4.40,4.55,2.49,5.03,-.02,3.45,0)
# Open timber guards: source HOLZGELAENDER; dimensions/picketspacing graphical.
# Source does not support an opaque1m board wall.12cm members are print thickening.
for n,y,z in [('north_landing',10.46,3.45),('south_midlanding',1.24,1.725)]:
 for x in np.linspace(3.23,5.72,4):bx(n+'_wood_post',x-.06,x+.06,y-.06,y+.06,z-.22,z+1.0,3)
 for h in [.50,.94]:bx(n+'_open_wood_rail',3.18,5.77,y-.06,y+.06,z+h,z+h+.12,3)
for n,x,zstart,zend in [('west_lower',3.24,1.725,0),('east_return',5.69,1.725,3.45)]:
 for y in np.linspace(2.50,5.02,4):
  z=zstart+(zend-zstart)*(y-2.50)/2.52
  bx(n+'_wood_post',x-.06,x+.06,y-.06,y+.06,z-.23,z+1.02,3)
 for h in [.50,.94]:
  add(n+'_open_sloping_wood_rail',yz([(2.49,zstart+h),(5.03,zend+h),(5.03,zend+h+.12),(2.49,zstart+h+.12)],x-.06,x+.06),3)
# Central1.80m trough has bottom, not a void through storage rooms.
bx('trough_reinforced_bottom',16.10,17.90,0,10.50,5.75,5.95,1)
# Remove the uppervolume above troughbottom before walls are added.
body=body-box(16.35,17.65,-.01,10.51,5.95,7.10)
for a,b in [(16.10,16.35),(17.65,17.90)]:bx('trough_sidewall_lip7m',a,b,0,10.50,5.93,7.0,0)
# Roofedge6.77 derived,2% towardtrough is transparent surface coordination±.25m.
add('west_roof',box(0,3.20,0,10.50,6.47,6.77),2)
add('main_roof_2percent_to_trough',xz([(5.75,6.50),(16.10,6.293),(16.10,6.563),(5.75,6.77)],0,10.50),2)
add('east_roof_2percent_to_trough',xz([(17.90,6.377),(24.05,6.50),(24.05,6.77),(17.90,6.647)],0,10.50),2)
# Sunshades source8cm, thickened12cm=.8mm at1:150;70cm clear stand-off.
bx('south_standoff_sunshade_thickened8to12cm',5.75,16.35,-.82,-.70,5.17,6.77,0)
for x0,x1 in [(-.82,-.70),(24.75,24.87)]:bx('end_standoff_sunshade_thickened8to12cm',x0,x1,0,10.50,5.17,6.77,0)
# Visible transverse screen ties correspond to plan columnpositions.
for x in [5.90,8.495,11.05,13.605,16.10]:bx('south_screen_tie',x-.08,x+.08,-.75,.10,6.50,6.70,0)
for y in [.25,3.62,6.98,10.25]:
 bx('west_screen_tie',-.75,.12,y-.08,y+.08,6.50,6.70,0)
 bx('east_screen_tie',23.95,24.80,y-.08,y+.08,6.50,6.70,0)
# Open firecourt eastcolumns; positions to be checked with facade review.
for y in [.16,3.60,7.10,10.34]:bx('east_ground_exterior_column',23.80,24.05,y-.16,y+.16,-.04,3.46,0)
for a,b in [(0,.25),(10.25,10.50)]:bx('east_firecourt25cm_end_returnwall',22.04,24.05,a,b,-.05,3.26,0)
# Chimney localplan84cm square; topgraphical±.10, no invented tallstack.
add('exterior_chimney_with_graphical_top_recess',box(21.21,22.05,-1.59,-.75,-.05,6.77)-box(21.405,21.855,-1.395,-.945,6.52,6.85),0)
# Direct windowgroups and graphical grid subdivision; glazing opaque print convention.
def window(n,a,b,plane,z0,z1,axis='x',side=-1,cols=6,rows=4):
 global body
 # side outwardnormal. Backing inset22cm; frames80mm=.53mm at1:150.
 cy=plane-side*.22
 if axis=='x':
  body=body-box(a,b,plane-.32,plane+.32,z0,z1)
  bx(n+'_infill',a-.012,b+.012,cy-.11,cy+.11,z0-.012,z1+.012,5)
  for q in np.linspace(a,b,cols+1):bx(n+'_mullion',q-.04,q+.04,plane-.05,plane+.05,z0-.01,z1+.01,3)
  for z in np.linspace(z0,z1,rows+1):bx(n+'_rail',a-.01,b+.01,plane-.05,plane+.05,z-.04,z+.04,3)
 else:
  body=body-box(plane-.32,plane+.32,a,b,z0,z1)
  bx(n+'_infill',cy-.11,cy+.11,a-.012,b+.012,z0-.012,z1+.012,5)
  for q in np.linspace(a,b,cols+1):bx(n+'_mullion',plane-.05,plane+.05,q-.04,q+.04,z0-.01,z1+.01,3)
  for z in np.linspace(z0,z1,rows+1):bx(n+'_rail',plane-.05,plane+.05,a-.01,b+.01,z-.04,z+.04,3)
BAYS=[(6.10,8.335),(8.655,10.890),(11.210,13.445),(13.765,16.000)]
for a,b in BAYS:
 window('south_ground_large_window',a,b,0,0,2.10,rows=6)
 window('south_ground_transom',a,b,0,2.40,3.10,rows=2)
 window('north_ground_low_window',a,b,10.50,.75,1.45,side=1,rows=2)
 window('south_upper_window',a,b,0,4.10,6.20,rows=6)
 window('north_upper_window',a,b,10.50,4.10,6.20,side=1,rows=6)
for a,b in [(.35,3.40),(3.72,6.78),(7.10,10.15)]:
 window('west_ground_high_window',a,b,0,2.40,3.10,axis='y',rows=2,cols=8)
 window('west_upper_window',a,b,0,4.10,5.50,axis='y',rows=4,cols=8)
 window('west_upper_window_high_band',a,b,0,5.75,6.45,axis='y',rows=2,cols=8)
 window('east_upper_window',a,b,24.05,4.10,5.50,axis='y',side=1,rows=4,cols=8)
 window('east_upper_window_high_band',a,b,24.05,5.75,6.45,axis='y',side=1,rows=2,cols=8)
 window('east_recessed_firecourt_high_window',a,b,22.05,2.40,3.10,axis='y',side=1,rows=2,cols=8)
for a,b in [(16.45,18.715),(19.035,21.30)]:window('north_kitchen_high_window',a,b,10.50,2.40,3.10,side=1,rows=2)
window('south_kitchen_high_band',18.40,21.20,0,2.40,3.10,rows=2,cols=8)
window('west_inner_ground_ventband_graphical',.25,7.75,3.20,2.40,3.10,axis='y',side=1,cols=20,rows=2)
window('west_inner_upper_ventband_graphical',.25,4.85,3.20,5.75,6.45,axis='y',side=1,cols=12,rows=2)
# Passage doors in walls bordering actual stair landing. Heights graphical ±.10m.
for x,y0,y1,z,side in [(3.20,5.02,5.92,3.45,1),(5.75,5.02,5.92,3.45,-1),(5.75,6.30,7.70,0,-1),(3.20,7.98,8.88,0,1)]:
 window('stair_landing_door',y0,y1,x,z+.04,z+2.14,axis='y',side=side,cols=2,rows=2)


add('bounded_room_envelope',body,0)
solid=P[0]
for p in P[1:]:solid=solid+p
solid=solid.set_tolerance(.0001).simplify(.0001).translate((-12.025,-5.25,SHIFT)).scale((S,S,S))
m=solid.to_mesh64();v=np.asarray(m.vert_properties)[:,:3];f=np.asarray(m.tri_verts);materials=np.zeros(len(f),dtype=int)
for i,oid in enumerate(m.run_original_id):materials[m.run_index[i]//3:m.run_index[i+1]//3]=IDS[int(oid)]
m=Manifold(Mesh64(v.astype(np.float32).astype(np.float64),f.astype(np.uint64),face_id=np.arange(len(f),dtype=np.uint64),tolerance=.00001)).simplify(.00001).to_mesh64();materials=materials[np.asarray(m.face_id,dtype=int)]
t=trimesh.Trimesh(np.asarray(m.vert_properties)[:,:3].astype(np.float32).astype(np.float64),np.asarray(m.tri_verts),process=False);t.merge_vertices(digits_vertex=5);keep=t.nondegenerate_faces();materials=materials[keep];t.update_faces(keep);t.remove_unreferenced_vertices()
np.savez_compressed(R/'mesh.npz',vertices=t.vertices,faces=t.faces,materials=materials);t.export(R/'model.stl');(R/'palette.json').write_text(json.dumps(PALETTE));(R/'components.json').write_text(json.dumps(LOG,ensure_ascii=False,indent=2))
q={'status':'WIP_PARTIAL_GEOMETRY_NOT_RELEASE','triangles':len(t.faces),'watertight':bool(t.is_watertight),'scale':'1:150','bounds_mm':t.bounds.tolist(),'mesh_sha256':hashlib.sha256((R/'mesh.npz').read_bytes()).hexdigest()};(R/'BUILD-QA.json').write_text(json.dumps(q,indent=2));print(json.dumps(q))
