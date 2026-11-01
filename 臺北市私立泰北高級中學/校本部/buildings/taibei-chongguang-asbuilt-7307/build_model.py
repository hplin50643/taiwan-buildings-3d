"""Taibei Chongguang building, museum CGEP116 job7307 as-built drawing state.
Not a survey of 2026. Metres in authored geometry; 1:250 millimetre output.
Hidden interiors simplified to solid backed exterior; no reference images bundled.
"""
from pathlib import Path
import json,hashlib,zipfile,xml.etree.ElementTree as ET
import numpy as np,trimesh
from manifold3d import Manifold,CrossSection,OpType
R=Path(__file__).resolve().parent
P=[];LOG=[]
PALETTE=[('neutral concrete','#C9C6BA'),('unverified roof finish','#B9BCB8'),('opaque glazing','#547078'),('window frame','#DEDCD0'),('authored base','#92948D'),('dark vent','#616A69')]
def box(a,b,c,d,e,f):
 assert b>a and d>c and f>e,(a,b,c,d,e,f)
 return Manifold.cube((b-a,d-c,f-e)).translate((a,c,e))
def poly(q,z,h):return CrossSection([q]).extrude(h-z).translate((0,0,z))
def add(name,m,mat=0):
 P.append(m.set_properties(1,lambda pos,old:[mat]));LOG.append({'name':name,'material':mat,'bounds_m':list(m.bounding_box())})
def bx(name,a,b,c,d,e,f,mat=0):add(name,box(a,b,c,d,e,f),mat)
def face(name,a,b,z0,z1,thick=.22,mat=0):
 a=np.array(a,float);b=np.array(b,float);v=b-a;n=np.array([-v[1],v[0]])/np.linalg.norm(v)*thick/2
 add(name,poly([a-n,b-n,b+n,a+n],z0,z1),mat)
 LOG[-1]['plane_xy']=[a.tolist(),b.tolist(),thick]
def panel(name,x0,x1,y,z0,z1):
 # Backed exterior pane; the raised outline is printable, not void glass.
 bx(name,x0,x1,y-.09,y+.09,z0,z1,2)
 for x in [x0,x1,(x0+x1)/2]:bx(name+'_mullion',x-.06,x+.06,y-.15,y+.15,z0-.05,z1+.05,3)
 for z in [z0,z1,(z0+z1)/2]:bx(name+'_transom',x0-.06,x1+.06,y-.15,y+.15,z-.06,z+.06,3)
# Base in modelling metres; conceptual plane not surveyed terrain.
base=box(-7,63,-7,32,-5.1,0)-box(4.8,35.2,23.8,27.2,-4.5,.1)
add('authored_display_base_with_source_lightwell_cutaway',base,4)
bx('visible_basement_north_backing',5,35,20.0,24,-4.52,.44)
for k in range(1,7):
 panel('visible_basement_north_window',k*5+.3,(k+1)*5-.3,24,-3.75,-.5)
# Main lower footprint A-D=24m, east taper. X grids 0..50 then7.136m.
lower=[(0,0),(50,0),(57.136,12),(40.4,24),(0,24)]
# GL is0;1F+.45,2F4.95,3F8.35,4F11.45,5F15.95,RF27.10.
lower_index=len(P)
add('lower_three_storey_exterior_envelope',poly(lower,4.75,15.95))
# Source 1F south arcade at A-B; all backed rooms begin at B=3.8.
ground=[(0,3.8),(52.3,3.8),(57.136,12),(40.4,24),(0,24)]
g=poly(ground,.40,4.95)-box(5,25,-.1,13.64,.46,4.76)-box(25,35,-.1,10.36,.46,4.76)
add('ground_backed_rooms',g)
add('ground_floor_plinth',poly(lower,0,.45),1)
for x in range(0,46,5):bx('ground_arcade_column',x-.27,x+.27,-.25,.3,.42,4.96)
# West stair/elevator enclosure source 1F; entrance open between x0..5 only at specified throat.
bx('west_stair_ground',0,5,0,3.95,.4,4.95)
# Front/rear ledges at2F and fourthfloor slab edges.
for z in [4.95,11.45,15.95]:
 bx('south_slab_edge',-.3,45.3,-.32,.32,z-.25,z+.05)
 bx('north_slab_edge',-.3,35.3,23.68,24.32,z-.25,z+.05)
# Exterior first-floor north balcony in source1F, no invented rear bays on blank east stagewall.
# 1F source label is BALCONY, not bathrooms. Projection1.50m marked in plan and supported by section.
bx('first_floor_north_balcony',5,35,23.9,25.5,.20,.45,1)
face('first_floor_north_balcony_rail',(5,25.5),(35,25.5),1.35,1.5,.16,3)
for x in np.arange(5,35.01,2):bx('first_floor_balcony_post',x-.07,x+.07,25.43,25.57,.42,1.5,3)
for k in range(1,7):panel('firstfloor_north_DW',k*5+.3,(k+1)*5-.3,24,.7,4.2)
# Source2F projecting3m balconies; parapet rails, not a narrow slabedge.
for xa,xb,ya,yb in [(5,44.3,-3,0),(0,39.5,24,27)]:
 bx('second_floor_balcony_slab',xa,xb,ya,yb,4.68,4.95,1)
 yo=ya if ya<0 else yb
 face('balcony_rail',(xa,yo),(xb,yo),5.90,6.05,.16,3)
 for x in np.arange(xa,xb+.01,2.0):bx('balcony_post',x-.07,x+.07,yo-.07,yo+.07,4.92,6.04,3)
 face('balcony_end_rail',(xa,ya),(xa,yb),5.90,6.05,.16,3)
 face('balcony_end_rail',(xb,ya),(xb,yb),5.90,6.05,.16,3)
# Fifth-floor hall projects3m beyond A/D, then tapers to acute east stageend.
hall=[(0,-3),(36.7,-3),(57.136,12),(36.7,27),(0,27)]
hall_low=[(0,-3),(40,-3),(40,0),(57.136,12),(36.7,27),(0,27)]
hall_high=[(0,-3),(35,-3),(35,0),(40,0),(57.136,12),(36.7,27),(0,27)]
add('upper_gymnasium_hall_lower',poly(hall_low,15.95,19.97)-box(35,40,-3.1,.01,19.70,20.1))
add('upper_gymnasium_hall_upper',poly(hall_high,19.95,26.65))
bx('mezzanine_outdoor_terrace_slab',35,40,-3,0,19.55,19.70,1)
face('mezzanine_platform_rail',(35,-3),(40,-3),20.60,20.75,.15,3)
for x in [35,37.5,40]:bx('platform_rail_post',x-.07,x+.07,-3.07,-2.93,19.7,20.72,3)
roof=[(-.7,-4.2),(36.9,-4.2),(58.6,12),(36.9,28.2),(-.7,28.2)]
add('roof_eave_and_flat_roof',poly(roof,26.35,27.10)-box(2.6,4.6,6.0,13.0,26.98,27.2),1)
# RF stair position engraved as a shallow plan symbol; depth is print convention, NOT measured stairwell.
for yy in np.arange(6.4,12.7,.45):bx('roof_stair_plan_symbol',2.65,4.55,yy,yy+.08,26.97,27.015,5)
for xx in [13.8,31.0]:
 bx('roof_vent_low_relief',xx-.7,xx+.7,11.3,12.7,27.08,27.16,5)
 for yy in np.arange(11.4,12.65,.22):bx('roof_vent_grille_relief',xx-.65,xx+.65,yy,yy+.07,27.14,27.20,3)
# Source roof perimeter guardrail1.10m: solid low kerb and rail/posts.
for a,b in zip(hall,hall[1:]+hall[:1]):
 face('roof_kerb',a,b,27.05,27.26,.22)
 face('roof_top_rail',a,b,28.08,28.22,.15,3)
 a=np.array(a);b=np.array(b);L=np.linalg.norm(b-a)
 for t in np.linspace(0,1,max(2,int(L/2)+1)):
  x,y=a+(b-a)*t;bx('roof_guard_post',x-.075,x+.075,y-.075,y+.075,27.12,28.2,3)
panel('southern_5F_east_final_window',35.35,39.65,-3,16.85,19.55)
# Main facade pilasters and cantilever brackets sourceA13/A4.
for x in range(0,36,5):
 for y,s in [(0,-1),(24,1)]:
  bx('facade_column',x-.20,x+.20,y-.28,y+.28,4.85,15.98)
  # three metre exterior triangle at4F-to5F, not a full wall.
  yz=[(y,11.45),(y+s*3,15.95),(y,15.95)]
  # extrusion inX: rotate prism constructedxy(y,z), extrusion alongz then rotate.

  # Above transform requires independent validation of bounds; explicit hull safer below.
  v=np.array([[x-.22,y,11.45],[x-.22,y+s*3,16.00],[x-.22,y,16.00],[x+.22,y,11.45],[x+.22,y+s*3,16.00],[x+.22,y,16.00]])
  tm=trimesh.convex.convex_hull(v);from manifold3d import Mesh
  outer=Manifold(Mesh(np.asarray(tm.vertices,dtype=np.float32),np.asarray(tm.faces,dtype=np.uint32)))
  iv=np.array([[xx,yy,zz] for xx in [x-.4,x+.4] for yy,zz in [(y+s*.55,12.85),(y+s*2.35,15.40),(y+s*.55,15.40)]])
  it=trimesh.convex.convex_hull(iv);hole=Manifold(Mesh(np.asarray(it.vertices,dtype=np.float32),np.asarray(it.faces,dtype=np.uint32)))
  add('cantilever_bracket',outer-hole)
# South facade: west stair band then classroom/library bays5..35; east balcony below stage hall.
for y in [0,24]:
 for k in range(1,10 if y==0 else 8):
  x0=k*5+.35;x1=(k+1)*5-.35
  for z0,z1 in [(5.85,7.95),(8.75,10.95),(12.10,15.25)]:
   if y==0 and ((k==9 and z0<11) or (k==8 and 8<z0<11)):
    P[lower_index]=P[lower_index]-box(x0,x1,-.1,1.2,z0,z1)
    face('south_east_corridor_rail',(x0,0),(x1,0),z0+.65,z0+.8,.16,3)
    for x in np.arange(x0,x1,.8):bx('corridor_baluster',x-.06,x+.06,-.07,.07,z0,z0+.8,3)
   else:panel('lower_window',x0,x1,y,z0,z1)
# Hall clerestory/tall glazing source north/south bays2..7.
for y in [-3,27]:
 for k in range(1,7):
  for z0,z1 in [(16.85,19.55),(21.0,24.95)]:panel('hall_window',k*5+.35,(k+1)*5-.35,y,z0,z1)
 for x in range(0,36,5):bx('hall_pilaster',x-.20,x+.20,y-.3,y+.3,15.8,26.65)
# Visible east balcony recess on4F source: carve terrace separately from opaque mass.
# Geometry correction performed before union: subtract opening atx50..57 below hall.
cut=box(50.3,58,-.2,11.9,11.65,15.7)
northterrace=poly([(40,20.20),(45.4,20.20),(40,24.15)],11.65,15.7)
P[lower_index]=P[lower_index]-cut-northterrace
for z0,z1 in [(5.2,8.1),(8.65,11.2),(11.75,15.6)]:
 for y0,y1 in [(.3,3.5),(4.1,10.1)]:
  P[lower_index]=P[lower_index]-box(-.1,2.1,y0,y1,z0,z1)
  face('west_open_balcony_rail',(0,y0),(0,y1),z0+.85,z0+1.0,.16,3)
  for y in np.arange(y0,y1,.8):bx('west_balcony_baluster',-.07,.07,y-.06,y+.06,z0,z0+.98,3)
# East stair core; A13 controls RF 27.10m.
bx('east_stair_core',50.0,58.136,-3.0,2.25,.3,27.10)
# Drawn water tank above east core; plan3.55m is not height; top controlled by A13, not contemporary equipment.
bx('tower_top_cap',49.85,58.28,-3.15,2.40,26.95,27.20,1)
panel('tower_high_window',52.2,56.0,-3.01,22.8,24.5)
# A13 source-scaled arch outline, not an arched doorway or presumed shell opening.
theta=np.linspace(0,np.pi,25)
outer=[(54.1+2.35*np.cos(t),24.3+2.0*np.sin(t)) for t in theta]
inner=[(54.1+2.25*np.cos(t),24.3+1.9*np.sin(t)) for t in theta[::-1]]
add('tower_window_arch_outline_relief',poly(outer+inner,0,.20).rotate((90,0,0)).translate((0,-2.91,0)),3)
# A13 tower east openings: elevations estimated individually from the drawing, not equal storey repeats.
for zc in [8.3,12.3,16.3,19.5,24.0]:
 bx('tower_east_small_window',58.05,58.24,-2.6,-2.0,zc-.6,zc+.6,2)
 for yy in [-2.6,-2.0]:bx('tower_small_window_jamb',58.08,58.29,yy-.045,yy+.045,zc-.64,zc+.64,3)
 for zz in [zc-.6,zc+.6]:bx('tower_small_window_sill',58.08,58.29,-2.64,-1.96,zz-.045,zz+.045,3)
# West/sourceexternal stair to2F: stepped supported run, source-side setback.
for i in range(25):
 z=.45+(i+1)*4.5/25
 bx('west_external_stair',-5.7+(i)*5.7/25,-5.7+(i+1)*5.7/25,0,2.4,0,z)
# Original broad rear vent + west narrow stair windows basedA13, all non-photometric colors.
for z0,z1 in [(.7,4.2),(5.4,7.95),(8.8,10.95),(12.1,15.4)]:
 bx('west_north_square_window',-.10,.09,20.6,23.4,z0,z1,2)
bx('west_central_vertical_window',-.1,.08,10.7,13.3,.7,19.8,2)
for z in [4.95,8.35,11.45,15.95]:bx('west_central_transom',-.16,.09,10.65,13.35,z-.07,z+.07,3)
bx('west_hall_horizontal_window',-.1,.08,5.0,19.0,21.5,25.4,2)
for y in [-2.6,24.6]:
 for z in [16.6,22.1]:bx('west_hall_side_window',-.1,.08,y,y+1.8,z,z+3.2,2)
# A13 north/east and A4: tall finned opening on NE diagonal, not blank wall.
def ne(x):return np.array([x,24-(x-40.4)*12/16.736])
a,b=ne(45.35),ne(49.65)
face('northeast_tall_backed_window',a,b,.65,10.70,.25,2)
for t in np.linspace(0,1,7):
 c=a+(b-a)*t;d=(b-a)/np.linalg.norm(b-a)*.07
 face('northeast_vertical_fin',c-d,c+d,.62,10.75,.42,3)
for z in [.65,10.70]:face('northeast_window_frame',a,b,z-.07,z+.07,.42,3)
va,vb=ne(41.9),ne(43.4)
face('northeast_low_vent',va,vb,1.9,3.55,.24,5)
for z in np.arange(2.0,3.55,.22):face('northeast_low_vent_louver',va,vb,z,z+.08,.36,3)
# Main source front entrance glazing behind arcade rather than sealing atfrontline.
for x,y in [(5,13.64),(15,13.64),(25,10.36)]:panel('recorded_lobby_door',x+.25,x+1.75,y,.5,2.6)
print('components',len(P),flush=True)
# Boolean union preserves constant material properties on component surfaces.
solid=P[0].set_properties(0,lambda pos,old:[])
for part in P[1:]:solid=solid+part.set_properties(0,lambda pos,old:[])
solid=solid.simplify(0.000001)
assert solid.status().name=='NoError',solid.status()
solid=solid.translate((-28,12*-1,5.1)).scale((4,4,4))
m=solid.to_mesh64();vp=np.array(m.vert_properties);tri=np.asarray(m.tri_verts)
verts,inv=np.unique(np.round(vp[:,:3],5),axis=0,return_inverse=True);faces=inv[tri]
mat=np.zeros(len(tri),dtype=int)
cent=vp[tri,:3].mean(axis=1)/4+np.array([28,12,-5.1])
for item in LOG:
 lo=np.array(item['bounds_m'][:3]);hi=np.array(item['bounds_m'][3:]);inside=((cent>=lo-1e-4)&(cent<=hi+1e-4)).all(axis=1);surface=np.minimum(abs(cent-lo),abs(cent-hi)).min(axis=1)<1e-4
 if 'plane_xy' in item:
  aa,bb,th=item['plane_xy'];aa=np.array(aa);bb=np.array(bb);vv=bb-aa;nn=np.array([-vv[1],vv[0]])/np.linalg.norm(vv);distance=abs((cent[:,:2]-aa)@nn);surface |= abs(distance-th/2)<1e-4
 mat[inside&surface]=item['material']
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
assert t.is_watertight and t.is_winding_consistent
np.savez_compressed(R/'mesh.npz',vertices=verts,faces=faces,materials=mat)
t.export(R/'model.stl')
(R/'components.json').write_text(json.dumps(LOG,ensure_ascii=False,indent=2))
(R/'palette.json').write_text(json.dumps(PALETTE))
q={'triangles':len(faces),'vertices':len(verts),'watertight':bool(t.is_watertight),'winding_consistent':bool(t.is_winding_consistent),'bounds_mm':t.bounds.tolist(),'extents_mm':t.extents.tolist(),'volume_mm3':t.volume,'mesh_sha256':hashlib.sha256((R/'mesh.npz').read_bytes()).hexdigest(),'scale':'1:250','status':'GEOMETRY_PASS_SEE_SEPARATE_SOURCE_AND_RENDER_QA'}
(R/'BUILD-QA.json').write_text(json.dumps(q,indent=2));print(json.dumps(q),flush=True)
