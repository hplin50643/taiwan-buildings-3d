"""NKNU swimming pool/stand, 1985 original design.
CCCK296 by C. K. Chen. No claim of as-built/current condition.
Source metres, GL0. Fine A4-1 finish +4.77,+8.27,+9.37 (A3 rounds +3cm).
"""
from pathlib import Path
import json,hashlib,numpy as np,trimesh
from manifold3d import Manifold,CrossSection,Mesh64
R=Path(__file__).resolve().parent
P=[];LOG=[]
PALETTE=[('neutral wall','#CBC8BC'),('neutral walking surface','#B4B6B2'),('opaque glazing','#526C74'),('neutral frame','#DEDCD0'),('authored display base','#96958D'),('recess','#37464B')]
def box(a,b,c,d,e,f):
 assert b>a and d>c and f>e
 return Manifold.cube((b-a,d-c,f-e)).translate((a,c,e))
def add(n,m,mat=0):
 assert not m.is_empty(),n
 P.append(m);LOG.append({'name':n,'material':mat,'bounds_m':list(m.bounding_box())})
def bx(n,a,b,c,d,e,f,mat=0):add(n,box(a,b,c,d,e,f),mat)
def along_x(q,x0,x1):
 if sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(q,q[1:]+q[:1]))<0:q=q[::-1]
 m=CrossSection([q]).extrude(x1-x0).to_mesh64();v=np.asarray(m.vert_properties)[:,:3];v=v[:,[2,0,1]];v[:,0]+=x0
 return Manifold(Mesh64(np.array(v,dtype=np.float64,order="C",copy=True),np.array(m.tri_verts,dtype=np.uint64,order="C",copy=True)))
bx('authored_local_display_base',-5.1,61.95,-2,53.25,-.8,-.25,4)
bx('stand_ground_support',0,58.9,0,11.7,-.3,0,4)
bx('source_ground_floor_plinth',0,58.9,0,11.7,0,1.5,1)
bx('backed_changing_room_envelope',.18,58.72,.18,8.7,1.5,4.77)
bx('front_walkway_canopy_slab',0,58.9,8.5,11.7,4.57,4.77,1)
# A2-2: 3.60 rear platform + six 1.10 treads + 1.50 front walkway.
# A4-1 seven risers 0.50m, not seven treads. End circulation is not yet modeled.
bx('stand_rear_upper_platform',4.5,54.4,0,3.6,4.57,8.27,1)
for i in range(6):bx('stand_tread_'+str(i+1),4.5,54.4,3.6+1.1*i,4.7+1.1*i,4.57,7.77-.5*i,1)
bx('stand_front_walkway',4.5,54.4,10.2,11.7,4.57,4.77,1)
bx('stand_rear_parapet',0,58.9,0,.18,0,9.37)
profile=[(0,0),(11.7,0),(11.7,5.87),(3.6,9.37),(0,9.37)]
for a,b in [(0,.18),(58.72,58.9)]:add('stand_side_parapet',along_x(profile,a,b))
# Ground/pool uses A2 local dimension chain; overall site depth differs by 5cm.
# x relative to stand left outer edge; original site origin is x=-3.10.
px0,px1=3.375,53.475;py0,py1=19.40,44.50
voidq=[(-px1,-.18),(-px0,0),(-px0,3),(-px1,3)]
poolvoid=along_x(voidq,py0,py1).rotate((0,0,90))
wash=box(px0-1.7,px1+1.7,py0-1.7,py1+1.7,1.36,1.6)-box(px0-.5,px1+.5,py0-.5,py1+.5,1.30,1.7)
add('raised_pool_court_with_sloped_dry_basin',(box(-3.1,59.95,11.6,49.10,-.3,1.5)+box(4.62,52.23,49.08,51.25,-.3,1.5))-poolvoid-wash,1)
# Basin finish is geometrically supported, neutral blue-grey not a current-colour claim.
liner=along_x([(-px1,-.18),(-px0,0),(-px0,-.035),(-px1,-.215)],py0,py1).rotate((0,0,90))
add('dry_pool_sloped_floor_finish',liner,2)
# Ten painted lane lines are relief marks; no water plane concealing depth.
for j in range(10):
 yy=py0+1.30+j*2.50
 q=[(-(px1-2),-.18+.18*2/50.1+.015),(-(px0+2),-.18*2/50.1+.015),(-(px0+2),-.18*2/50.1-.01),(-(px1-2),-.18+.18*2/50.1-.01)]
 add('pool_lane_floor_mark_'+str(j+1),along_x(q,yy-.055,yy+.055).rotate((0,0,90)),5)
 for xx in [px0+2,px1-2]:
  zz=-.18*(xx-px0)/50.1
  bx('lane_end_mark',xx-.055,xx+.055,yy-.5,yy+.5,zz-.015,zz+.018,5)
# Three-window/door categories along room facades from A2-1/A6-1.
# Rear small upper vents occupy 11 central bays; stair end bays remain unglazed.
def pane(n,x0,x1,y,z0,z1,louver=False):
 bx(n,x0,x1,y-.045,y+.045,z0,z1,2 if not louver else 5)
 for xx in [x0,x1]:bx(n+'_edge',xx-.035,xx+.035,y-.075,y+.075,z0-.035,z1+.035,3)
 for zz in [z0,z1]:bx(n+'_head',x0-.035,x1+.035,y-.075,y+.075,zz-.035,zz+.035,3)
 if louver:
  for zz in np.arange(z0+.08,z1,.13):bx(n+'_louver',x0,x1,y-.09,y+.09,zz,zz+.04,3)
 else:
  for xx in np.linspace(x0,x1,7)[1:-1]:bx(n+'_mullion',xx-.025,xx+.025,y-.08,y+.08,z0,z1,3)
for j in range(1,12):
 x0=.2+j*4.5+.2;x1=x0+4.1
 pane('rear_upper_vent_'+str(j),x0,x1,0,3.60,4.15,louver=j not in [1,2,11])
# A3-1 pool facade: three distinct source groups, not uniform full-height glazing.
for j in range(1,12):
 x0=.2+j*4.5+.2;x1=x0+4.1
 if j in [1,2,11]:
  pane('DW_upper_transom_'+str(j),x0,x1,8.7,3.60,4.15)
  bx('DW_opaque_door_leaf',x0,x0+.90,8.65,8.75,1.50,3.60,2)
  bx('DW_door_divider',x0+.86,x0+.94,8.61,8.79,1.50,4.15,3)
  if j in [1,2]:
   pane('DW1_lower_glazing',x0+.90,x1,8.7,2.55,3.60)
 elif j in [4,5,8,9]:
  for z0,z1 in [(1.50,1.85),(3.60,4.15)]:
   bx('changing_room_small_screen_band',x0,x1,8.64,8.76,z0,z1,5)
   for xx in np.arange(x0,x1,.23):bx('screen_band_vertical',xx,xx+.04,8.60,8.80,z0,z1,3)
   for zz in np.arange(z0,z1,.18):bx('screen_band_horizontal',x0,x1,8.60,8.80,zz,zz+.04,3)
 else:
  # Plain screened/entrance panels represented by neutral recess and three visible divisions.
  bx('front_three_panel_recess',x0,x1,8.66,8.74,1.50,4.15,0)
  for xx in np.linspace(x0,x1,4):bx('front_three_panel_division',xx-.035,xx+.035,8.60,8.80,1.50,4.15,3)
  bx('front_three_panel_head',x0,x1,8.60,8.80,4.10,4.18,3)
# Exposed basement ventilation bands on grid7..13; height A3-scaled, not a fabricated basement room.
for j in range(6,12):
 x0=.2+j*4.5+.2;pane('rear_low_vent_'+str(j),x0,x0+4.1,0,.10,.60,True)
for j in range(14):
 xc=.2+4.5*j
 bx('front_column',xc-.20,xc+.20,8.5,8.9,1.5,4.77,0)
# A4-3 upper end access steps: 21 risers, 28/28/54cm repeated per 50cm seat rise.
for x0,x1 in [(2.54,4.50),(54.40,56.36)]:
 by=10.2
 for i in range(20):
  depth=[.28,.28,.54][i%3];y1=by;by-=depth
  bx('upper_end_circulation_step',x0,x1,by,y1,4.57,4.77+(i+1)*3.5/21,1)
 bx('upper_end_rear_landing',x0,x1,0,by,4.57,8.27,1)
# Backed side portions adjoining stair strips, not unverified hidden interiors.
for x0,x1 in [(.18,2.54),(56.36,58.72)]:
 bx('end_rear_landing_cover',x0,x1,0,3.6,8.02,8.27,1)
 bx('end_lower_cover',x0,x1,3.55,4.7,7.52,7.77,1)
 bx('end_rear_support',x0,x1,0,.20,4.57,8.25,0)
# A7-4 starting platforms: 0.50m head,0.45m high; small recesses simplified.
for yy in [py0+1.30+j*2.50 for j in range(10)]:
 for xx,sgn in [(px0,-1),(px1,1)]:
  xa,xb=sorted([xx,xx+sgn*.50])
  bx('starting_block_base',xa+.10,xb-.10,yy-.25,yy+.25,1.46,1.94,0)
  bx('starting_block_head',xa,xb,yy-.25,yy+.25,1.87,1.95,3)
# A4-1 front parapet and rail; nominal pipes thickened to0.10m for scale geometry.
bx('stand_front_low_curb',.18,58.72,11.52,11.70,4.75,5.07,0)
bx('stand_front_rail',.18,58.72,11.53,11.63,5.77,5.87,3)
for xx in np.linspace(.25,58.65,27):bx('stand_front_rail_post',xx-.05,xx+.05,11.53,11.63,5.02,5.87,3)
# A6-1 boundary frame only; diamond mesh itself omitted, not falsely solidified.
# Source nominal west23*2.72 and north15*2.73 are approximate: fit named perimeter run.
def fence_x(n,a,b,y,count):
 bx(n+'_kerb',a,b,y-.08,y+.08,1.45,1.65,0)
 for xx in np.linspace(a,b,count+1):bx(n+'_post',xx-.06,xx+.06,y-.06,y+.06,1.60,3.55,3)
 for zz in [1.70,3.45]:bx(n+'_rail',a,b,y-.05,y+.05,zz,zz+.10,3)
def fence_y(n,x,a,b,count):
 bx(n+'_kerb',x-.08,x+.08,a,b,1.45,1.65,0)
 for yy in np.linspace(a,b,count+1):bx(n+'_post',x-.06,x+.06,yy-.06,yy+.06,1.60,3.55,3)
 for zz in [1.70,3.45]:bx(n+'_rail',x-.05,x+.05,a,b,zz,zz+.10,3)
fence_x('front_boundary_frame_schematic',-3.05,59.90,49.10,23)
fence_y('left_boundary_frame_schematic',-3.05,11.70,49.10,15)
# Existing opposite campus wall only represented at low enclosing outline; no invented ornament.
bx('existing_right_wall_outline',59.80,59.95,0,49.10,1.45,2.40,0)
# Front original outdoor access stairs: ten risers to1.50m; placement from A2-1 end bays.
for xa,xb,reverse in [(2.1,4.62,False),(52.23,54.75,True)]:
 for j in range(10):
  a,b=(xa+j*.252,xa+(j+1)*.252) if not reverse else (xb-(j+1)*.252,xb-j*.252)
  bx('front_outdoor_access_step',a,b,49.08,51.25,-.28,(j+1)*.15,1)
# A5 main stair exits: bounded covered recess, not invented complete internal stairs.
for xa,xb in [(.18,2.39),(56.51,58.72)]:
 bx('end_low_passage',xa,xb,4.7,10.2,4.55,4.80,1)
 bx('end_upper_exit_landing',xa,xb,3.3,4.7,4.55,5.03,1)
 bx('end_small_threshold_step',xa,xb,4.7,5.05,4.55,4.87,1)
 # dark backed doorway under the cover; hidden lower stair assembly intentionally omitted
 bx('backed_stair_exit_recess',xa,xb,3.28,3.34,5.0,7.45,5)
 for j in range(4):bx('bounded_stair_exit_step',xa,xb,2.2+j*.28,2.48+j*.28,4.4,4.40+(j+1)*.1575,1)
# North end D5 rolling entry: 2.00m x3.50m from A5-1/A6-1, backed opaque.
bx('north_D5_rolling_entry',-.06,.06,.60,2.60,0,3.50,5)
for zz in np.arange(.08,3.5,.16):bx('rolling_entry_slats',-.085,.07,.60,2.60,zz,zz+.035,3)
# A2-1 six ladders: three along each long edge, positions scaled from symbols.
# A7-4 width0.60m, top0.75m above deck; U bends angularised, rods thickened0.10m.
for xx in [px0+1.5,(px0+px1)/2,px1-1.5]:
 for yy,sgn in [(py0,1),(py1,-1)]:
  yi,yo=yy+sgn*.15,yy-sgn*.40;bot=-.18*(xx-px0)/50.1
  for xr in [xx-.30,xx+.30]:
   bx('ladder_inside_rail',xr-.05,xr+.05,yi-.05,yi+.05,bot+.10,2.25,3)
   bx('ladder_outer_fixing',xr-.05,xr+.05,yo-.05,yo+.05,1.44,2.25,3)
   bx('ladder_angular_top',xr-.05,xr+.05,min(yi,yo)-.05,max(yi,yo)+.05,2.15,2.25,3)
  for zz in [bot+.15,bot+.45,bot+.75,bot+1.05,bot+1.35]:bx('ladder_rung',xx-.35,xx+.35,yi-.05,yi+.05,zz,zz+.10,3)
print('components',len(P),flush=True)
solid=P[0]
for m in P[1:]:solid=solid+m
solid=solid.simplify(1e-6).translate((-28.425,-25.625,.8)).scale((4,4,4))
m=solid.to_mesh64();vp=np.asarray(m.vert_properties);tri=np.asarray(m.tri_verts)
verts,inv=np.unique(np.round(vp[:,:3],5),axis=0,return_inverse=True);faces=inv[tri];mat=np.zeros(len(faces),dtype=int)
valid=(faces[:,0]!=faces[:,1])&(faces[:,1]!=faces[:,2])&(faces[:,0]!=faces[:,2])
areas=np.linalg.norm(np.cross(verts[faces[:,1]]-verts[faces[:,0]],verts[faces[:,2]]-verts[faces[:,0]]),axis=1)
valid &= areas>0
print('removed_numeric_zero_area',int((~valid).sum()),flush=True)
faces=faces[valid];mat=mat[valid]
# Conform numeric collinear seam edges after 0.00001mm coordinate snapping.
for iteration in range(5):
 t=trimesh.Trimesh(verts,faces,process=False)
 if t.is_watertight:break
 edges=np.sort(t.edges,axis=1);ue,c=np.unique(edges,axis=0,return_counts=True);bad=ue[c==1]
 print('seam_iteration',iteration,'boundary',len(bad),'nonmanifold',int((c>2).sum()),flush=True)
 candidates=np.unique(bad);splits={}
 for a,b in bad:
  av,bv=verts[a],verts[b];v=bv-av;den=v@v
  if den<1e-14:continue
  ts=(verts[candidates]-av)@v/den
  dist=np.linalg.norm(verts[candidates]-(av+ts[:,None]*v),axis=1)
  pick=(ts>1e-6)&(ts<1-1e-6)&(dist<1.1e-5)
  ids=candidates[pick][np.argsort(ts[pick])]
  if len(ids):splits[(int(a),int(b))]=ids.tolist()
 if not splits:break
 newfaces=[];newmat=[];vv=verts.tolist()
 for f,ma in zip(faces,mat):
  polygon=[];changed=False
  for a,b in zip(f,np.roll(f,-1)):
   polygon.append(int(a));ids=splits.get(tuple(sorted((int(a),int(b)))),[])
   if ids:
    changed=True;polygon.extend(ids if a<b else ids[::-1])
  if changed:
   center=len(vv);vv.append(np.mean(verts[f],axis=0).tolist())
   for a,b in zip(polygon,polygon[1:]+polygon[:1]):newfaces.append([a,b,center]);newmat.append(ma)
  else:newfaces.append(f.tolist());newmat.append(ma)
 verts=np.asarray(vv);faces=np.asarray(newfaces);mat=np.asarray(newmat)
t=trimesh.Trimesh(verts,faces,process=False)
print('watertight',t.is_watertight,'winding',t.is_winding_consistent,flush=True)

if not t.is_watertight:
 ee,cc=np.unique(np.sort(t.edges,axis=1),axis=0,return_counts=True)
 print('BAD_EDGE_COORDS',[(int(c),(verts[e]/4+np.array([28.425,25.625,-.8])).tolist()) for e,c in zip(ee,cc) if c!=2],flush=True)
assert t.is_watertight and t.is_winding_consistent
cent=t.triangles_center/4+np.array([28.425,25.625,-.8]);mat=np.zeros(len(t.faces),dtype=int)
for item in LOG:
 lo=np.array(item['bounds_m'][:3]);hi=np.array(item['bounds_m'][3:]);inside=((cent>=lo-1e-4)&(cent<=hi+1e-4)).all(axis=1);surface=np.minimum(abs(cent-lo),abs(cent-hi)).min(axis=1)<1e-4
 if item['name']=='dry_pool_sloped_floor_finish' or item['name'].startswith('pool_lane_floor_mark'):surface|=abs(cent[:,2]-(-.18*(cent[:,0]-px0)/50.1+(0.015 if item['name'].startswith('pool_lane') else 0)))<1e-4
 mat[inside&surface]=item['material']
np.savez_compressed(R/'mesh.npz',vertices=t.vertices,faces=t.faces,materials=mat)
t.export(R/'model.stl');(R/'components.json').write_text(json.dumps(LOG,indent=2));(R/'palette.json').write_text(json.dumps(PALETTE))
q={'status':'GEOMETRY_PASS_SEE_SEPARATE_SOURCE_AND_RENDER_QA','triangles':len(t.faces),'watertight':bool(t.is_watertight),'components':len(t.split()),'scale':'1:250','mesh_sha256':hashlib.sha256((R/'mesh.npz').read_bytes()).hexdigest(),'scope':'historical original design, not asbuilt/current survey'}
(R/'BUILD-QA.json').write_text(json.dumps(q,indent=2));print(json.dumps(q),flush=True)
