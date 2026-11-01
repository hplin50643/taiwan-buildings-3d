"""CCRH12623005 original undated dormitory design by Chen Ren-ho.
Coordinates are drawing coordinates, not verified geographic directions.
Metres, main axes x0..5.4/y0..6.6, service enclosure x5.4..7.4/y0..1;
outer service inspection slab extends to x8.4. Display scale 1:50.
"""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
from manifold3d import Manifold
R=Path(__file__).resolve().parent;P=[];LOG=[]
PALETTE=[('neutral rendered wall','#D6D2C5'),('neutral concrete','#B9BBB4'),('opaque window backing','#597078'),('neutral frame','#E2DDCB'),('authored display base','#999C96'),('door backing','#777769')]
def box(a,b,c,d,e,f):return Manifold.cube((b-a,d-c,f-e)).translate((a,c,e))
def add(n,m,mat=0):P.append(m);LOG.append({'name':n,'material':mat,'bounds_m':list(m.bounding_box())})
def bx(n,a,b,c,d,e,f,mat=0):add(n,box(a,b,c,d,e,f),mat)
bx('authored_display_base_not_site',-1.0,9.0,-1.0,7.6,-.20,0,4)
# Raised continuous floor and open through passage. Solid room backing is a disclosed exterior-model simplification.
bx('main_floor_GL20',-.115,5.515,-.115,6.715,0,.20,1)
bx('room_pair_lower_solid_backing',-.115,5.515,-.115,2.815,.19,2.98)
bx('room_pair_upper_solid_backing',-.115,5.515,3.785,6.715,.19,2.98)
bx('service_enclosure_solid_backing',5.50,7.515,-.115,1.115,.19,2.98)
bx('service_floor',5.4,7.515,-.115,2.115,0,.20,1)
# 2 cm finish plus 6 cm slab is not a 35 cm thick solid plate.
bx('main_roof_6cm_plus_2cm_finish',-.55,5.95,-.55,7.15,2.97,3.05,1)
bx('wing_roof_6cm_plus_2cm_finish',5.4,7.95,-.55,2.00,2.97,3.05,1)
for x in [0,5.4]:bx('corridor_end_beam_underside270',x-.115,x+.115,2.7,3.9,2.70,2.99,1)
# Flat walls use shallow grooves inferred from drawn elevation rhythm, not material color measurements.
for x in [0,5.4]:
 for a,b in [(-.115,2.70),(3.90,6.715)]:
  for z in [1.35,1.85,2.35]:bx('end_wall_horizontal_joint_relief',x-.123,x+.123,a,b,z,z+.012,1)
# Finish joint rhythm shown on both long elevations; window relief obscures the joints within windows.
for yy,end in [(-.123,7.515),(6.723,5.515)]:
 for zz in [1.35,1.85,2.35]:bx('long_wall_horizontal_joint_relief',-.115,end,yy-.012,yy+.012,zz,zz+.012,1)
# Main W1. All frames are exterior relief over sealed room volumes.
def win_y(name,xc,y,w,z0,z1,service=False):
 x0=xc-w/2;x1=xc+w/2
 bx(name+'_opaque',x0,x1,y-.03,y+.03,z0,z1,2)
 for xx in [x0,x1]:bx(name+'_jamb',xx-.025,xx+.025,y-.04,y+.04,z0-.025,z1+.025,3)
 for z in [z0,z1]:bx(name+'_head_sill',x0-.025,x1+.025,y-.04,y+.04,z-.025,z+.025,3)
 if not service:bx(name+'_center',xc-.018,xc+.018,y-.04,y+.04,z0,z1,3)
 if service:
  bx(name+'_solid_intermediate_7cm',x0,x1,y-.045,y+.045,z0+.40,z0+.47,3)
  for z in [z0+.40,z0+.47,z0+.62,z0+.77]:bx(name+'_transom',x0,x1,y-.04,y+.04,z-.018,z+.018,3)
 else:
  bx(name+'_solid_bottom_sill_15cm',x0,x1,y-.045,y+.045,z0,z0+.15,3)
  bx(name+'_solid_intermediate_10cm',x0,x1,y-.045,y+.045,z0+.65,z0+.75,3)
  for z in [z0+.15,z0+.65,z0+.75,z0+1.20]:bx(name+'_horizontal_split',x0,x1,y-.04,y+.04,z-.018,z+.018,3)
  for xx in [xc-w/4,xc+w/4]:bx(name+'_upper_subframe',xx-.012,xx+.012,y-.04,y+.04,z0+.75,z1,3)
for y in [-.135,6.735]:
 for xc in [1.35,4.05]:win_y('W1_width150_outer_GL105_270',xc,y,1.50,1.05,2.70)
for xc in [5.90,6.90]:win_y('W3_width45',xc,-.135,.45,1.70,2.70,True)
# Service doors are on the inner return at y1; lower panels and transoms simplified to shallow relief.
for xc,w in [(5.90,.60),(6.90,.60)]:
 bx('service_door_leaf',xc-w/2,xc+w/2,1.095,1.145,.20,2.00,5)
 for xx in [xc-w/2,xc+w/2]:bx('service_door_frame',xx-.022,xx+.022,1.12,1.17,.20,2.02,3)
 for z in [.20,1.30,2.00]:bx('service_door_crossrail',xc-w/2,xc+w/2,1.12,1.17,z-.02,z+.02,3)
# Outside slab over service inspection tank. Underground plumbing and tank intentionally not modelled.
bx('outer_service_inspection_slab',7.40,8.40,-.115,2.115,0,.20,1)
add('inspection_cover_disc_estimated',Manifold.cylinder(.020,.16,.16,32).translate((7.90,.90,.20)),1)
# Entrance apron at each end of the through passage; shallow extra step for 20 cm floor.
for x0,x1 in [(-.55,.01),(5.39,5.95)]:bx('corridor_entry_apron',x0,x1,2.70,3.90,0,.10,1)
# Two external pipe stacks seen in rear elevation. Diameter, location and height are graphical estimates.
for yy in [.35,1.65]:
 add('service_pipe_graphically_estimated',Manifold.cylinder(3.45,.045,.045,20).translate((7.54,yy,.20)),3)
 add('service_pipe_cap_graphically_estimated',Manifold.cylinder(.07,.075,.055,20).translate((7.54,yy,3.60)),3)
 for zz in ([.25,1.35,2.60] if yy<1 else [.25]):bx('service_pipe_attachment',7.49,7.59,yy-.055,yy+.055,zz,zz+.04,3)
solid=P[0]
for p in P[1:]:solid=solid+p
scale=20.;offset=np.array([4.,3.3,-.20]);solid=solid.translate(tuple(-offset)).scale((scale,scale,scale))
m=solid.to_mesh64();t=trimesh.Trimesh(np.asarray(m.vert_properties)[:,:3],np.asarray(m.tri_verts),process=True)
assert t.is_watertight and t.is_winding_consistent and len(t.split())==1
cent=t.triangles_center/scale+offset;mat=np.zeros(len(t.faces),dtype=int)
for obj in LOG:
 lo=np.array(obj['bounds_m'][:3]);hi=np.array(obj['bounds_m'][3:]);inside=((cent>=lo-1e-5)&(cent<=hi+1e-5)).all(axis=1);surface=np.minimum(abs(cent-lo),abs(cent-hi)).min(axis=1)<1e-5
 if obj['name']=='inspection_cover_disc_estimated':surface|=inside
 mat[inside&surface]=obj['material']
np.savez_compressed(R/'mesh.npz',vertices=t.vertices,faces=t.faces,materials=mat);t.export(R/'model.stl')
(R/'palette.json').write_text(json.dumps(PALETTE));(R/'components.json').write_text(json.dumps(LOG,indent=2))
q={'status':'PASS_GEOMETRY','watertight':bool(t.is_watertight),'winding_consistent':bool(t.is_winding_consistent),'components':len(t.split()),'triangles':len(t.faces),'scale':'1:50','bounds_mm':t.bounds.tolist(),'mesh_sha256':hashlib.sha256((R/'mesh.npz').read_bytes()).hexdigest()};(R/'BUILD-QA.json').write_text(json.dumps(q,indent=2));print(json.dumps(q))
