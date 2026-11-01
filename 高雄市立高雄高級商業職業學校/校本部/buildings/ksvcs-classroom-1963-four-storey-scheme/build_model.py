"""KSVCS1963 original four-storey drawing scheme;4F marked out;construction unverified.
Six linked A1-A6 historical drawings, not present appearance or amended three-storey version. Metres until final1:150 millimetre export.
"""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
from manifold3d import Manifold,CrossSection
R=Path(__file__).resolve().parent;P=[];LOG=[];IDS={};S=1000/150
PALETTE=[('rendered plaster approximate','#CBC8B2'),('base mortar approximate','#A5AAA0'),('roof neutral approximation','#9C9F95'),('window wood approximate','#877B63'),('authored display base not terrain','#ADB4A2'),('opaque window backing','#526970'),('simple closed door exterior','#8C9796'),('rail mortar approximation','#8E938C')]
def box(a,b,c,d,e,f):return Manifold.cube((b-a,d-c,f-e)).translate((a,c,e))
def add(n,m,mat=0):
 assert not m.is_empty(),n
 m=m.as_original();IDS[m.original_id()]=mat;P.append(m);LOG.append({'name':n,'material':mat,'bounds_m':list(m.bounding_box())})
def bx(n,a,b,c,d,e,f,mat=0):add(n,box(a,b,c,d,e,f),mat)
def profile_xz(n,pts,y0,y1,mat=0):
 # CrossSection extrusion local z rotated into world y.
 if sum(pts[i][0]*pts[(i+1)%len(pts)][1]-pts[(i+1)%len(pts)][0]*pts[i][1] for i in range(len(pts)))<0:pts=pts[::-1]
 m=CrossSection([pts]).extrude(y1-y0).rotate((90,0,0)).translate((0,y1,0));add(n,m,mat)
def beam(n,a,b,w=.035,mat=3):
 a=np.array(a);b=np.array(b);vec=b-a;L=np.linalg.norm(vec);z=vec/L;aux=np.array([0.,0.,1.]);
 if abs(z@aux)>.95:aux=np.array([0.,1.,0.])
 x=np.cross(z,aux);x/=np.linalg.norm(x);y=np.cross(z,x)
 # square section hull connecting endpoints, overlapped at endpoints.
 pts=[p+sx*x*w/2+sy*y*w/2 for p in [a-z*.01,b+z*.01] for sx in [-1,1] for sy in [-1,1]]
 add(n,Manifold.hull_points(pts),mat)


# Four storeys as drawn BEFORE interpreting crossout marks. Not a confirmed built building.
LEVELS=[.65,4.05,7.45,10.85];RF=14.25
bx('authored_display_base',-3.80,26.10,-4.60,22.40,-.30,0,4)
bx('ground_platform_FL065',-3.05,25.30,-3.05,21.50,-.01,.65,1)
# A1 labels1..4 withthree35cm treads; fourthlevel isplatform. Equalrises .65/4 are derived, not individually dimensioned.
for i in range(3):bx('south_entrance_steps35_four_levels',9.65,15.35,-4.10+i*.35,-3.04,-.01,(i+1)*(.65/4),1)
body=box(-.18,25.18,-.18,20.18,.63,RF-.10)
W=[]
def opening(n,axis,face,c,w,z0,z1,sgn=1,style='window',cols=4,rows=3):
 global body
 if axis=='y':body=body-box(c-w/2,c+w/2,face-.30,face+.30,z0,z1)
 else:body=body-box(face-.30,face+.30,c-w/2,c+w/2,z0,z1)
 W.append((n,axis,face,c,w,z0,z1,sgn,style,cols,rows))
for k,L in enumerate(LEVELS):
 for side,face,sgn in [('west',-.18,-1),('east',25.18,1)]:
  for c in [2,6,10,14,18]:opening(f'{side}_F{k+1}_window','x',face,c,3.36,L+.12,L+3.08,sgn,'window',4,3)
 for c in [5,20]:
  opening(f'south_F{k+1}_wing','y',-.18,c,8.0,L+.12,L+3.08,-1,'front_ground' if k==0 else 'front_upper',8 if k==0 else 6,2)
  opening(f'north_F{k+1}_wing','y',20.18,c,8.0 if k<=1 else 5.0,L+.12,L+(3.08 if k<=1 else 2.55),1,('window' if k==0 else 'front_upper') if k<=1 else 'plain_panel_group',8 if k==0 else (6 if k==1 else 2),2)
 if k>=2:
  for c in [8.70,16.30]:opening(f'north_F{k+1}_inner_narrow_door','y',20.18,c,.90,L+.03,L+3.08,1,'four_leaf_transom',1,1)
 opening(f'south_F{k+1}_central_door','y',-.18,12.5,4.2,L+.03,L+3.08,-1,'four_leaf_transom',4,1)
add('closed_main_exterior_four_storeys_no_interiors',body,0)
# Separate central north stair/WC core, including original rooftop enclosure.
core=box(9.85,15.15,10.40,21.50,.63,16.73)
for k,L in enumerate(LEVELS+[RF]):
 for c in [10.9,14.1]:
  for tag,w,z0,z1 in [('square',.60,L+.75,L+1.35),('slit',.90,L+2.12,L+2.34)]:
   core=core-box(c-w/2,c+w/2,21.22,21.65,z0,z1)
   W.append((f'core_F{k+1}_{tag}','y',21.50,c,w,z0,z1,1,'small',2,1))
# Rooftop south door, source plan retained; closed exterior only.
core=core-box(11.70,13.30,10.20,10.70,RF,RF+2.10)
W.append(('rooftop_south_door','y',10.40,12.50,1.60,RF,RF+2.10,-1,'plain_double_door',2,1))
add('north_stair_core_original_rooftop',core,0)
for n,axis,face,c,w,z0,z1,sgn,style,cols,rows in W:
 def panel(tag,u0,u1,v0,v1,d0,d1,mat):
  if u1<=u0 or v1<=v0:return
  a,b=sorted([face+sgn*d0,face+sgn*d1])
  if axis=='y':bx(n+tag,u0,u1,a,b,v0,v1,mat)
  else:bx(n+tag,a,b,u0,u1,v0,v1,mat)
 plain=style in ['plain_double_door','plain_panel_group'];central=style=='four_leaf_transom'
 panel('_opaque_back',c-w/2-.015,c+w/2+.015,z0-.015,z1+.015,-.35,-.10,6 if plain or central else 5)
 for u in [c-w/2,c+w/2-.06]:panel('_jamb',u,u+.06,z0,z1,-.18,.04,3)
 for z in [z0,z1-.06]:panel('_outer_rail',c-w/2,c+w/2,z,z+.06,-.18,.04,3)
 if plain:
  panel('_center_leaf',c-.03,c+.03,z0,z1,-.16,.03,3)
 elif central:
  for i in range(1,cols):
   u=c-w/2+w*i/cols;panel('_four_leaf',u-.03,u+.03,z0,z1,-.16,.03,3)
  panel('_transom_rail',c-w/2,c+w/2,z1-.65,z1-.59,-.16,.03,3)
  for i in range(cols):
   a=c-w/2+i*w/cols+.08;b=c-w/2+(i+1)*w/cols-.08;panel('_transom_glass',a,b,z1-.53,z1-.10,-.15,.00,5)
 else:
  lo,hi=c-w/2,c+w/2
  apron=.36 if style!='small' else 0
  if apron:panel('_opaque_lower_glazed_row',lo,hi,z0,z0+apron,-.17,.015,5)
  if apron:panel('_lower_row_rail',lo,hi,z0+apron-.025,z0+apron+.025,-.17,.035,3)
  if style=='front_upper':
   # Upper south wing end panels are solid below their small transoms, unlike1F all-glazed groups.
   for a,b in [(lo,lo+.8),(hi-.8,hi)]:
    panel('_solid_side_panel',a,b,z0,z1-.70,-.16,.02,3)
    panel('_side_transom_frame',a,b,z1-.76,z1-.70,-.17,.03,3)
    panel('_side_transom_split',(a+b)/2-.025,(a+b)/2+.025,z1-.70,z1,-.16,.03,3)
   lo+=.80;hi-=.80
  for i in range(1,cols):
   u=lo+(hi-lo)*i/cols;panel('_major_mullion',u-.03,u+.03,z0,z1,-.17,.04,3)
  bottom=z0+apron;top=z1-.06
  for j in range(1,rows):
   z=bottom+(top-bottom)*j/rows;panel('_major_horizontal',lo,hi,z-.03,z+.03,-.17,.04,3)
  if style!='small':
   for i in range(cols):
    a=lo+(hi-lo)*i/cols;b=lo+(hi-lo)*(i+1)/cols
    panel('_minor_vertical',(a+b)/2-.02,(a+b)/2+.02,z0,top,-.15,.025,3)
    for j in range(rows):
     z=bottom+(top-bottom)*(j+.5)/rows;panel('_minor_horizontal',a,b,z-.02,z+.02,-.15,.025,3)
# Structural perimeter posts and horizontal slab edges are direct regular grid, not diagonal cancellation strokes.
for x in [0,25]:
 for y in [0,4,8,12,16,20]:bx('perimeter_grid_column60',x-.30,x+.30,y-.30,y+.30,.64,RF,0)
for x in [10,15]:
 for y in [0,20]:bx('front_rear_core_grid_column60',x-.30,x+.30,y-.30,y+.30,.64,RF,0)
for k,z in enumerate(LEVELS[1:]+[RF]):
 west=-3.05 if k==0 else -.30;south=-3.05 if k==0 else -1.50
 bx(f'floor_or_roof_slab_{k+2}',west,25.30,south,21.50,z-.16,z,1)
 # Side beam face approx40cm structural depth, no fictitious curved beam.
 for x0,x1 in [(-.30,.05),(24.95,25.30)]:bx('side_horizontal_floor_beam',x0,x1,0,20,z-.40,z,1)
# Guardrails: south/north masonry-pattern bands; north staircore divides balcony.
def rail_y(n,y,x0,x1,z,h=.90,pattern=True):
 bx(n,x0,x1,y-.10,y+.10,z-.015,z+h,0)
 if pattern:
  for row in range(3):
   zz=z+.03+row*(h-.06)/3
   shift=.70 if row%2 else 0
   for a in np.arange(x0-1.4+shift,x1,1.40):
    lo=max(x0+.025,a+.025);hi=min(x1-.025,a+1.375)
    if hi>lo:
     for sgn in [-1,1]:bx(n+'_jointed_face_approx',lo,hi,y+sgn*.105-.012,y+sgn*.105+.012,zz,zz+(h-.06)/3-.025,1)
 bx(n+'_cap',x0-.015,x1+.015,y-.13,y+.13,z+h-.06,z+h,1)
for k,z in enumerate(LEVELS[1:]+[RF]):
 south=-3.05 if k==0 else -1.50;west=-3.05 if k==0 else -.30;h=1.0 if z==RF else .90
 rail_y('south_balcony_or_parapet',south,west,25.30,z,h,pattern=k!=0)
 if k==0:
  #2Fsourcepanel ornament differs fromupper brickjoint bands; simplified rectangular relief, not holes.
  for zz in [z+.10,z+.59]:bx('second_floor_south_panel_relief',west,25.30,south-.125,south-.095,zz,zz+.14,1)
  for xx in np.arange(west+.25,25.0,1.40):bx('second_floor_south_panel_vertical_accent',xx,xx+.09,south-.13,south-.095,z+.12,z+.79,1)
 rail_y('north_left_balcony',21.50,west,9.85,z,h)
 rail_y('north_right_balcony',21.50,15.15,25.30,z,h)
 if k==0 or z==RF:
  for x in ([west,25.30] if z==RF else [west]):bx('west_east_guard_or_parapet',x-.10,x+.10,south,21.50,z-.015,z+h,0)
# Flat stair roof direct5.70x11.45 datum chain150+800+195, south overhang35 only.
bx('stair_roof570x1145_top1685',9.65,15.35,10.05,21.50,16.71,16.85,1)

solid=P[0]
for p in P[1:]:solid=solid+p
solid=solid.simplify(0.000001)
solid=solid.translate((-11.,-9.3,.30)).scale((S,S,S))
m=solid.to_mesh64();v=np.asarray(m.vert_properties)[:,:3];f=np.asarray(m.tri_verts);materials=np.zeros(len(f),dtype=int)
for i,oid in enumerate(m.run_original_id):materials[m.run_index[i]//3:m.run_index[i+1]//3]=IDS[int(oid)]
t=trimesh.Trimesh(v.astype(np.float32).astype(np.float64),f,process=False)
t.merge_vertices(digits_vertex=8);keep=t.nondegenerate_faces();materials=materials[keep];t.update_faces(keep);t.remove_unreferenced_vertices()
assert t.is_watertight and t.is_winding_consistent
# Float32-consistent export may leave closed coplanar numerical tetrahedra at shared material boundaries.
# Remove ONLY zero-thickness/zero-volume components; never discard disconnected architectural geometry.
removed_flat_faces=0
cc=trimesh.graph.connected_components(t.face_adjacency,nodes=np.arange(len(t.faces)),min_len=1)
if len(cc)>1:
 largest=max(cc,key=len);keep=np.ones(len(t.faces),dtype=bool)
 for ids in cc:
  if ids is largest:continue
  sub=t.submesh([ids],append=True,repair=False)
  assert min(sub.extents)<1e-6 and abs(sub.volume)<1e-6,(len(ids),sub.bounds,sub.volume)
  keep[ids]=False;removed_flat_faces+=len(ids)
 materials=materials[keep];t.update_faces(keep);t.remove_unreferenced_vertices()
assert t.is_watertight and t.is_winding_consistent and len(t.split())==1
np.savez_compressed(R/'mesh.npz',vertices=t.vertices,faces=t.faces,materials=materials);t.export(R/'model.stl');(R/'palette.json').write_text(json.dumps(PALETTE));(R/'components.json').write_text(json.dumps(LOG,ensure_ascii=False,indent=2))
q={'status':'PASS_GEOMETRY_ONLY','triangles':len(t.faces),'removed_zero_volume_numerical_faces':removed_flat_faces,'components':len(t.split()),'watertight':bool(t.is_watertight),'winding':bool(t.is_winding_consistent),'scale':'1:150','datum':'GL0; authoredsupportnotterrain','bounds_mm':t.bounds.tolist(),'mesh_sha256':hashlib.sha256((R/'mesh.npz').read_bytes()).hexdigest()};(R/'BUILD-QA.json').write_text(json.dumps(q,indent=2));print(json.dumps(q))
