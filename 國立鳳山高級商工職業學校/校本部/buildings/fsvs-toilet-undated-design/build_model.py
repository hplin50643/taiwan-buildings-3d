"""CCRH12623009 Chen Ren-ho: undated original toilet-block design, not as-built.
Metres source coordinate: west axis x0, east x11; south y0/north y3; GL0.
Print model1:75. Neutral colours, backed glazing, interior plumbing omitted.
"""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
from manifold3d import Manifold
R=Path(__file__).resolve().parent;P=[];LOG=[]
PALETTE=[('neutral wall','#CEC9BB'),('neutral concrete','#B9BAB5'),('opaque window relief','#546F78'),('window frame','#E1DECF'),('authored base','#95968F'),('recess','#424F52')]
def box(a,b,c,d,e,f):return Manifold.cube((b-a,d-c,f-e)).translate((a,c,e))
def add(n,m,mat=0):P.append(m);LOG.append({'name':n,'material':mat,'bounds_m':list(m.bounding_box())})
def bx(n,a,b,c,d,e,f,mat=0):add(n,box(a,b,c,d,e,f),mat)
bx('authored_display_base',-1.5,11.6,-.65,4.55,-.25,0,4)
bx('raised_floor',-.115,11.115,-.115,3.115,-.01,.45,1)
bx('north_septic_exposed_cover',2.90,11.115,3.10,4.20,0,.45,1)
# Open west vestibule; actual main enclosure begins x3.
add('main_room_hollow_envelope',box(2.885,11.115,-.115,3.115,.43,3.34)-box(2.80,10.885,.115,2.885,.45,3.33))
for y in [0,3]:bx('west_corner_column',-.115,.115,y-.115,y+.115,.43,3.34)
for y in [0,3]:bx('vestibule_open_beam',-.115,3.12,y-.115,y+.115,3.13,3.34)
bx('continuous_flat_roof',-.295,11.295,-.295,3.295,3.33,3.51,1)
# Two open entrance thresholds, shallow external step, not closed walls.
for y in [-.31,3.31]:bx('vestibule_threshold_step',.12,2.88,y-.20,y+.20,0,.23,1)
# West washing trough: open basin with two legs, 100cm total outside footprint.
for yy in [.55,2.45]:bx('wash_basin_support',-.80,-.55,yy-.12,yy+.12,0,1.30,1)
basin=box(-1.0,-.45,.13,2.87,1.20,1.80)-box(-.91,-.54,.22,2.78,1.30,1.85)
add('west_high_water_reservoir',basin,1)
channel=box(-.46,.02,.13,2.87,1.02,1.20)-box(-.38,-.05,.22,2.78,1.10,1.25)
add('west_lower_washing_channel',channel,1)
# Exact clear widths of W2, W1; window sill height interpreted from section raised toilet floor.
def window(n,x0,x1,y,z0=2.065,z1=3.135):
 bx(n+'_opaque',x0,x1,y-.035,y+.035,z0,z1,2)
 for xx in [x0,x1]:bx(n+'_outer_frame',xx-.025,xx+.025,y-.065,y+.065,z0-.025,z1+.025,3)
 for zz in [z0,z0+.25,z0+.50,z0+.57,z0+.82,z1]:bx(n+'_horizontal',x0-.025,x1+.025,y-.065,y+.065,zz-.018,zz+.018,3)
 bx(n+'_inner_mullion',(x0+x1)/2-.018,(x0+x1)/2+.018,y-.060,y+.060,z0,z1,3)
for i in range(8):
 center=3.5225+i*.985
 window('south_W2_'+str(i+1),center-.3925,center+.3925,-.135)
for group,start in enumerate([3.65,7.41]):
 for i in range(5):window('north_W1_'+str(group*5+i+1),start+i*.60,start+i*.60+.54,3.135)
# Fine horizontal masonry joints: shallow relief, not invented glazing.
for y in [-.12,3.12]:
 for z in [.88,1.38,1.88]:bx('facade_horizontal_joint',3.02,11.03,y-.015,y+.015,z,z+.018,1)
# East entry leaf width ~1.15m scaled from elevation; 1.455m label belongs to step.
bx('east_door_opaque',11.10,11.15,.925,2.075,.45,2.53,5)
for yy in [.925,1.50,2.075]:bx('east_door_jamb',11.12,11.19,yy-.025,yy+.025,.45,2.55,3)
for z in [.45,2.53]:bx('east_door_head',11.12,11.19,.900,2.100,z-.025,z+.025,3)
bx('east_entry_canopy',11.05,11.45,.63,2.37,2.58,2.69,1)
bx('east_entry_step',11.10,11.48,.77,2.23,0,.23,1)
# Six exterior vent stacks; cap size/height graphical approximations.
for x in [5,7,9]:
 for y in [-.18,3.18]:
  add('vent_pipe',Manifold.cylinder(3.76,.06,.06,16).translate((x,y,.40)),3)
  add('vent_cap',Manifold.cylinder(.10,.12,.04,16).translate((x,y,4.08)),3)
  for z in [.52,1.65,2.75,3.38]:bx('vent_wall_fixing',x-.075,x+.075,min(y,0 if y<0 else 3)-.02,max(y,0 if y<0 else 3)+.02,z,z+.045,3)
# Cover inspection plates, low neutral relief. Not underground tank contents.
for x in [5.5,8.5]:add('septic_cover_disc',Manifold.cylinder(.025,.25,.25,24).translate((x,3.65,.44)),1)
solid=P[0]
for p in P[1:]:solid=solid+p
scale=1000/75;offset=np.array([5.05,1.95,-.25]);solid=solid.translate(tuple(-offset)).scale((scale,scale,scale))
m=solid.to_mesh64();verts=np.asarray(m.vert_properties)[:,:3];faces=np.asarray(m.tri_verts)
t=trimesh.Trimesh(verts,faces,process=True);assert t.is_watertight and t.is_winding_consistent
cent=t.triangles_center/scale+offset;mat=np.zeros(len(t.faces),dtype=int)
for obj in LOG:
 lo=np.array(obj['bounds_m'][:3]);hi=np.array(obj['bounds_m'][3:]);inside=((cent>=lo-1e-5)&(cent<=hi+1e-5)).all(axis=1)
 surface=np.minimum(abs(cent-lo),abs(cent-hi)).min(axis=1)<1e-5
 if obj['name'].startswith('vent_') or obj['name']=='septic_cover_disc':surface|=inside
 mat[inside&surface]=obj['material']
np.savez_compressed(R/'mesh.npz',vertices=t.vertices,faces=t.faces,materials=mat);t.export(R/'model.stl')
(R/'palette.json').write_text(json.dumps(PALETTE));(R/'components.json').write_text(json.dumps(LOG,indent=2))
q={'status':'geometry_only_pass','watertight':bool(t.is_watertight),'winding_consistent':bool(t.is_winding_consistent),'components':len(t.split()),'triangles':len(t.faces),'scale':'1:75','bounds_mm':t.bounds.tolist(),'mesh_sha256':hashlib.sha256((R/'mesh.npz').read_bytes()).hexdigest()};assert q['components']==1
(R/'BUILD-QA.json').write_text(json.dumps(q,indent=2));print(json.dumps(q))
