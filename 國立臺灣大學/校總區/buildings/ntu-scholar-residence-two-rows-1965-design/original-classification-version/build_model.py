"""NTU type-B scholar residences: 1965 historical two-row exterior.
Two authored independent supports; relative placement is NOT historic site geometry.
"""
from pathlib import Path
import json,hashlib,numpy as np,trimesh
from manifold3d import Manifold,Mesh64,CrossSection
from geometry_helpers import box
R=Path(__file__).resolve().parent;S=5.;SHIFT=.55;P=[];LOG=[];IDS={}
PALETTE=[('illustrative pale render','#C8C6B5'),('illustrative washed aggregate','#A9A99D'),('illustrative small tile','#9C9D90'),('print-thickened window frames','#7D8884'),('authored display supports not terrain','#ADB19F'),('opaque glazing illustration','#788D92'),('doors and metal details','#8A8171'),('yard boundary FOOTPRINT convention not historic height','#747D68')]
def add(n,m,mat=0):
 assert not m.is_empty(),n
 m=m.as_original();IDS[m.original_id()]=mat;P.append(m);LOG.append({'name':n,'material':mat,'bounds_m':list(m.bounding_box())})
def bx(n,a,b,c,d,e,f,mat=0):add(n,box(a,b,c,d,e,f),mat)
def yz(pts,a,b):
 if sum(pts[i][0]*pts[(i+1)%len(pts)][1]-pts[(i+1)%len(pts)][0]*pts[i][1] for i in range(len(pts)))<0:pts=pts[::-1]
 return CrossSection([pts]).extrude(b-a).transform(((0,0,1,a),(1,0,0,0),(0,1,0,0)))
def opening(body,name,cx,plane,z0,w,h,side,cols=2,transom=None,door=False):
 a,b=cx-w/2,cx+w/2;z1=z0+h
 body=body-box(a,b,plane-.24,plane+.24,z0,z1)
 back=plane-side*.18
 bx(name+'_opaque_recess',a-.01,b+.01,back-.06,back+.06,z0-.01,z1+.01,6 if door else 5)
 if door:
  gp=back+side*.065
  # A4 glazed upper light and visible door-leaf glass, not lock/hardware detail.
  tz=z0+(2.01 if 'D2' in name else 2.)
  bx(name+'_transom_glass',a+.04,b-.04,gp-.015,gp+.015,tz+.04,z1-.04,5)
  gw,gh,gz=(.50,1.00,z0+.85) if 'D2' in name else (.40,.40,z0+1.40)
  bx(name+'_leaf_glass',cx-gw/2,cx+gw/2,gp-.015,gp+.015,gz,gz+gh,5)
  for xx in [cx-gw/2,cx+gw/2]:bx(name+'_leaf_glass_frame',xx-.025,xx+.025,gp-.025,gp+.025,gz-.025,gz+gh+.025,3)
  for zz in [gz,gz+gh]:bx(name+'_leaf_glass_rail',cx-gw/2-.025,cx+gw/2+.025,gp-.025,gp+.025,zz-.025,zz+.025,3)

 for x in np.linspace(a,b,cols+1):bx(name+'_frame',x-.04,x+.04,plane-.045,plane+.045,z0-.02,z1+.02,3)
 for z in [z0,z1]+([] if transom is None else [z0+transom]):bx(name+'_rail',a-.02,b+.02,plane-.045,plane+.045,z-.04,z+.04,3)
 return body
# Pure display coordinates: no representation of A0 interbuilding distance/rotation.
ROWS=[('six_unit_row',6,0.,0.),('four_unit_row',4,5.7,19.)]
for name,n,x0,y0 in ROWS:
 L=n*5.7;a=x0-.12;b=x0+L+.12;c=y0-.12;d=y0+7.62
 bx(name+'_independent_authored_support',x0-1.6,x0+L+1.6,y0-2.0,y0+12.0,-SHIFT,-.03,4)
 body=box(a,b,c,d,-.05,6.60)
 # Alternating unit orientation is source paired-plan evidence, not mirrored whole facades.
 for j in range(n):
  flip=j%2==1
  X=lambda q:x0+j*5.7+(5.7-q if flip else q)
  for level,fl in enumerate([.45,3.45]):
   front=[('W1',.9,1.45,1.75,.80),('W3',4.65,1.60,.975,.80)]
   if level:front.insert(1,('W1',2.7,1.45,1.75,.80))
   for typ,x,w,h,sill in front:
    body=opening(body,name+f'_{j}_{level}_front_{typ}',X(x),c,fl+sill,w,h,-1,2,1.25 if typ=='W1' else .4875)
   rear=[('W1',.9,1.45,1.75,.80),('W4',3.25,.52,1.75,.80)] if level==0 else [('W1',q,1.45,1.75,.80) for q in [.9,2.7,4.65]]
   for typ,x,w,h,sill in rear:body=opening(body,name+f'_{j}_{level}_rear_{typ}',X(x),d,fl+sill,w,h,1,1 if typ=='W4' else 2,1.25)
  body=opening(body,name+f'_{j}_front_D1',X(3.),c,.45,1.00,2.55,-1,1,2.,True)
  body=opening(body,name+f'_{j}_rear_D2',X(4.2),d,.45,.90,2.56,1,1,2.01,True)
  # Source short steps and landings; no private interior stair layout.
  for face,xc,sgn in [('front',X(3.),-1),('rear',X(4.2),1)]:
   edge=c if sgn<0 else d
   for k,z in enumerate([.15,.30,.45]):
    near=.90-k*.30
    p,q=sorted((edge,edge+sgn*near))
    bx(name+f'_{j}_{face}_near_step',xc-.65,xc+.65,p-.01,q+.01,-.05,z,1)
  # Each household back court remains open air; boundary height UNDOCUMENTED:20cm display footprint only, not historical wall height.
  ux=x0+j*5.7
  for wx in [ux,ux+5.7]:bx(name+f'_{j}_rear_court_divider',wx-.10,wx+.10,d-.02,y0+11.50,-.05,.20,7)
  # A1 backyard gate70cm atx2.90..3.60, not aligned to rearD2.
  gate=X(3.25);e=y0+11.5
  bx(name+f'_{j}_rear_court_end_left',ux-.10,gate-.35,e-.10,e+.10,-.05,.20,7)
  bx(name+f'_{j}_rear_court_end_right',gate+.35,ux+5.8,e-.10,e+.10,-.05,.20,7)
 # Continuous facade floor bands, not an invented open balcony.
 for plane,side in [(c,-1),(d,1)]:
  p,q=sorted((plane,plane+side*.20))
  cp,cq=sorted((plane,plane+side*1.20))
  bx(name+'_first_floor_source120cm_canopy',a,b,cp-.01,cq+.01,3.30,3.45,1)
  # Thin tile panels between openings, as source elevation material divisions.
  for j in range(n+1):
   x=x0+j*5.7
   bx(name+'_expressed_party_pier',x-.10,x+.10,p-.015,q+.015,-.04,6.45,1)
  for j in range(n):
   mid=x0+j*5.7+2.15 if j%2==0 else x0+j*5.7+3.55
   bx(name+'_upper_small_tile_panel',mid-.35,mid+.35,plane-.025,plane+.025,3.48,6.40,2)
 add(name+'_exterior_shell',body,0)
 # Roof datum coordination: A1 exterior7.05; local finish6.70±.10.
 # 1:50 gentle finish slope to two long edges, interior ridge nominal6.775.
 roof=yz([(y0-.12,6.44),(y0+7.62,6.44),(y0+7.62,6.70),(y0+3.75,6.775),(y0-.12,6.70)],x0-.30,x0+L+.30)
 add(name+'_bounded_roof_finish_1in50',roof,1)
 # Distinct outward-upturned long eaves, not a60cm solid slab.
 front=[(y0-1.18,7.05),(y0-1.08,7.05),(y0-.90,6.70),(y0+.05,6.70),(y0+.05,6.45),(y0-1.00,6.45)]
 add(name+'_front_upturned_eave',yz(front,x0-.30,x0+L+.30),1)
 rear=[(2*y0+7.5-y,z) for y,z in front];add(name+'_rear_upturned_eave',yz(rear,x0-.30,x0+L+.30),1)
 # Side fascia joins top outline; decorative panel-chain826 cannot redefine750 depth.
 for xx in [x0-.30,x0+L+.18]:
  bx(name+'_side_roof_fascia',xx,xx+.12,y0-1.18,y0+8.68,6.60,7.05,1)
 # Endwall finish joints use relative spacing only; no invented end windows.
 marks=np.cumsum([50,120,183,120,183,120])/826*7.5
 for xx in [a,b]:
  for yy in marks:bx(name+'_side_graphical_finish_joint',xx-.012,xx+.012,y0+yy-.025,y0+yy+.025,.10,6.40,1)
  for zz in [1.45,4.30]:bx(name+'_side_horizontal_finish_joint',xx-.012,xx+.012,c,d,zz-.025,zz+.025,1)
# A1 back elevation: one vent per mirrored pair, end-view rungs on one end only.
for name,n,x0,y0 in ROWS:
 for j in range(n//2):
  x=x0+5.7+j*11.4;y=y0+7.1
  add(name+'_rear_vent_graphical_height',Manifold.cylinder(1.05,.06,.06,16).translate((x,y,6.60)),6)
  bx(name+'_vent_cap_graphical',x-.13,x+.13,y-.13,y+.13,7.60,7.65,1)
 # Source1inch steel embedment rungs thickened8cm; no unsupported second end.
 x=x0-.12;y=y0+6.60
 for z in np.linspace(3.20,6.35,10):
  bx(name+'_single_end_embedded_rung',x-.28,x-.20,y-.25,y+.25,z-.04,z+.04,6)
  for yy in [y-.25,y+.25]:bx(name+'_rung_embedment',x-.28,x+.015,yy-.04,yy+.04,z-.04,z+.04,6)
solid=P[0]
for p in P[1:]:solid=solid+p
solid=solid.set_tolerance(.0001).simplify(.0001).translate((-17.1,-14.5,SHIFT)).scale((S,S,S))
m=solid.to_mesh64();v=np.asarray(m.vert_properties)[:,:3];f=np.asarray(m.tri_verts);materials=np.zeros(len(f),dtype=int)
for i,oid in enumerate(m.run_original_id):materials[m.run_index[i]//3:m.run_index[i+1]//3]=IDS[int(oid)]
m=Manifold(Mesh64(v.astype(np.float32).astype(np.float64),f.astype(np.uint64),face_id=np.arange(len(f),dtype=np.uint64),tolerance=.00001)).simplify(.00001).to_mesh64();materials=materials[np.asarray(m.face_id,dtype=int)]
t=trimesh.Trimesh(np.asarray(m.vert_properties)[:,:3].astype(np.float32).astype(np.float64),np.asarray(m.tri_verts),process=False);t.merge_vertices(digits_vertex=4);keep=t.nondegenerate_faces();materials=materials[keep];t.update_faces(keep);t.remove_unreferenced_vertices()
np.savez_compressed(R/'mesh.npz',vertices=t.vertices,faces=t.faces,materials=materials);t.export(R/'model.stl');(R/'palette.json').write_text(json.dumps(PALETTE));(R/'components.json').write_text(json.dumps(LOG,ensure_ascii=False,indent=2))
q={'status':'WIP_SOURCE_BOUNDED_EXTERIOR_NOT_RELEASE','triangles':len(t.faces),'watertight':bool(t.is_watertight),'connected_components':len(t.split(only_watertight=False)),'scale':'1:200','bounds_mm':t.bounds.tolist(),'mesh_sha256':hashlib.sha256((R/'mesh.npz').read_bytes()).hexdigest()};(R/'BUILD-QA.json').write_text(json.dumps(q,indent=2));print(json.dumps(q))
