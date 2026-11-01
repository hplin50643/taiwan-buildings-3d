"""1964 Nantou school combined hall ORIGINAL DESIGN, not verified built/current.
Source CCCK428, dated53.4/job5218. Authoring metres at GL0; FF+.50.
"""
from pathlib import Path
import json,hashlib,numpy as np,trimesh
from manifold3d import Manifold,CrossSection,Mesh
R=Path(__file__).resolve().parent
P=[];LOG=[]
PALETTE=[('neutral wall','#CBC8BC'),('unverified roof finish','#AEB6B4'),('opaque glazing','#526C74'),('simplified frame','#DEDCD0'),('authored base','#96958D'),('backed screen recess','#777C75')]
def box(a,b,c,d,e,f):
 assert b>a and d>c and f>e,(a,b,c,d,e,f)
 return Manifold.cube((b-a,d-c,f-e)).translate((a,c,e))
def add(n,m,mat=0):
 assert not m.is_empty(),n
 P.append(m);LOG.append({'name':n,'material':mat,'bounds_m':list(m.bounding_box())})
def bx(n,a,b,c,d,e,f,mat=0):add(n,box(a,b,c,d,e,f),mat)
def along_x(q,x0,x1):
 if sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(q,q[1:]+q[:1]))<0:q=q[::-1]
 m=CrossSection([q]).extrude(x1-x0).to_mesh();v=np.asarray(m.vert_properties)[:,:3];v=v[:,[2,0,1]];v[:,0]+=x0
 return Manifold(Mesh(np.asarray(v,dtype=np.float32),np.asarray(m.tri_verts,dtype=np.uint32)))
def roofz(y):return 14.12-4.12/13.75*abs(y-13.75)
bx('authored_flat_display_base',-4,51,-3,30.5,-1,0,4)
body=along_x([(0,0),(27.5,0),(27.5,9.99),(13.75,14.0),(0,9.99)],0,47)
add('backed_original_design_envelope',body)
roofq=[(-.3,roofz(-.3)),(13.75,14.12),(27.8,roofz(27.8)),(27.8,roofz(27.8)-.16),(13.75,13.96),(-.3,roofz(-.3)-.16)]
add('pitched_metal_roof_simplified_sheet',along_x(roofq,-.1,47.1),1);LOG[-1]['roof_surface']=True
for y in [-.25,27.75]:bx('long_eave_gutter',-.1,47.1,y-.15,y+.15,9.66,9.84,1)
# Source main axes6+7*5+6 along length. Paired windows are added after A11/A12 datum QA.
for x in [0,6,11,16,21,26,31,36,41,47]:
 for y in [0,27.5]:bx('side_structural_pilaster',x-.14,x+.14,y-.13,y+.13,0,10,0)
for x in [0,47]:
 for y in [0,4.5,9,13.75,18.5,23,27.5]:
  bx('gable_pilaster',x-.14,x+.14,y-.12,y+.12,0,roofz(y)-.16,0)
# Original front two four-leaf entrance groups; A12type1 4.30m wide,3.14m overallheight.
for y0 in [9.25,13.95]:
 bx('front_door_backing',-.12,.07,y0,y0+4.30,.50,3.64,2)
 for yy in [y0,y0+1.075,y0+2.15,y0+3.225,y0+4.3]:bx('front_door_mullion',-.18,.08,yy-.045,yy+.045,.48,3.68,3)
 for zz in [.5,2.9,3.64]:bx('front_door_transom',-.18,.08,y0-.04,y0+4.34,zz-.045,zz+.045,3)
for i in range(3):bx('front_entrance_steps',-2.4+i*.8,0,8.9,18.8,0,(i+1)*.5/3,1)
# A12 exact window modules; A5 global elevations scaled at +/-0.10m, not conflicting A11 local floors.
def pane_y(n,x0,x1,y,z0,z1):
 bx(n,x0,x1,y-.08,y+.08,z0,z1,2)
 for xx in [x0,(x0+x1)/2,x1]:bx(n+'_frame',xx-.035,xx+.035,y-.13,y+.13,z0-.04,z1+.04,3)
 for zz in [z0,z0+(z1-z0)*.25,z0+(z1-z0)*.5,z1]:bx(n+'_transom',x0-.04,x1+.04,y-.13,y+.13,zz-.035,zz+.035,3)
def pane_x(n,x,y0,y1,z0,z1):
 bx(n,x-.08,x+.08,y0,y1,z0,z1,2)
 for yy in [y0,(y0+y1)/2,y1]:bx(n+'_frame',x-.13,x+.13,yy-.035,yy+.035,z0-.04,z1+.04,3)
 for zz in [z0,(z0+z1)/2,z1]:bx(n+'_transom',x-.13,x+.13,y0-.04,y1+.04,zz-.035,zz+.035,3)
for y in [0,27.5]:
 for xc in [.65]+[v+d for v in [6,11,16,21,26,31,36,41] for d in [-.75,.75]]:
  pane_y('upper_B_window',xc-.5,xc+.5,y,7.0,9.5)
  if not any(abs(xc-c)<1.4 for c in [21,36]):pane_y('lower_A_window',xc-.5,xc+.5,y,2.0,4.5)
 for xc in [21,36]:
  pane_y('side_type4_double_door',xc-.75,xc+.75,y,.8,4.45)
  # A5 door ground follows local raised apron; base grade remains schematic.
  bx('side_door_canopy',xc-1.8,xc+1.8,y-.6,y+.6,4.43,4.55,1)
  for j in range(4):
   ya,yb=(y-1.2+j*.3,y) if y==0 else (y,y+1.2-j*.3)
   bx('side_door_step',xc-1,xc+1,ya,yb,0,(j+1)*.2,1)
# Back gable has three paired window bands; middle pair continues into roof triangle.
for yc in [4.5,13.75,23]:
 for dy in [-.75,.75]:
  for lo,hi in [(2.1,4.0),(6.5,9.0)]:pane_x('back_window_pair',47,yc+dy-.5,yc+dy+.5,lo,hi)
  if yc==13.75:
   y0,y1=yc+dy-.5,yc+dy+.5;h0,h1=roofz(y0)-.85,roofz(y1)-.85
   add('back_high_trapezoid_window',along_x([(y0,11.5),(y1,11.5),(y1,h1),(y0,h0)],46.94,47.08),2)
   for yy in [y0,(y0+y1)/2,y1]:bx('back_high_window_frame',46.90,47.14,yy-.035,yy+.035,11.46,roofz(yy)-.81,3)
   add('back_high_window_sloped_head',along_x([(y0,h0-.04),(y1,h1-.04),(y1,h1+.04),(y0,h0+.04)],46.90,47.14),3)
   bx('back_high_window_sill',46.90,47.14,y0-.04,y1+.04,11.46,11.54,3)
for yc in [7.2,20.3]:
 pane_x('back_type3_single_exit',47,yc-.4,yc+.4,1.9,4.55)
 bx('back_exit_canopy',46.9,47.7,yc-1.2,yc+1.2,4.55,4.68,1)
 for j in range(8):bx('back_exit_steps',47,49.0-j*.23,yc-.75,yc+.75,0,(j+1)*1.9/8,1)
# Front screen is a backed coarse low-relief grid, not invented individual historic brick ornament.
screen=[(7.9,4.35),(19.6,4.35),(19.6,roofz(19.6)-.7),(13.75,13.42),(7.9,roofz(7.9)-.7)]
mask=along_x(screen,-.25,.08)
add('front_backed_breeze_block_screen',along_x(screen,-.14,.08),5)
for yy in np.arange(7.9,19.61,.42):add('screen_grid_vertical_simplification',box(-.24,.02,yy-.035,yy+.035,4.3,13.5)^mask,3)
for zz in np.arange(4.35,13.5,.42):
 m=box(-.24,.02,7.9,19.6,zz-.035,zz+.035)^mask
 if not m.is_empty():add('screen_grid_horizontal_simplification',m,3)
bx('front_entrance_shelter',-.75,.1,6.5,21.0,4.02,4.18,1)
# A5 facade-scaled shallow vertical divisions; they do not create invented windows.
for x,ys in [(0,[1.5,3,4.5,6,7.5,20,21.5,23,24.5,26]),(47,[1.5,3,6,7.5,9,10.5,12,15.5,17,18.5,20,21.5,24.5,26])]:
 for yy in ys:bx('gable_shallow_vertical_rib',x-.16,x+.16,yy-.065,yy+.065,.1,roofz(yy)-.55,0)
for yy in [4.2,9.5,18.0,23.3]:
 bx('back_low_vent',46.96,47.12,yy-.35,yy+.35,.38,.88,5)
 for zz in [.45,.60,.75]:bx('back_vent_louver',47.05,47.16,yy-.35,yy+.35,zz,zz+.055,3)
# A5 end gable portal bands: about0.75m vertical depth from drawing, not whole roof thickness.
frameq=[(0,10),(13.75,14.12),(27.5,10),(27.5,9.25),(13.75,13.37),(0,9.25)]
for x0,x1 in [(-.25,.05),(46.95,47.25)]:
 add('gable_sloping_portal_frame',along_x(frameq,x0,x1),3)
 for y0,y1 in [(0,.7),(26.8,27.5)]:bx('gable_portal_end_column',x0,x1,y0,y1,0,10,3)
print('components',len(P),flush=True)
# Boolean union preserves constant material properties on component surfaces.
solid=P[0].set_properties(0,lambda pos,old:[])
for part in P[1:]:solid=solid+part.set_properties(0,lambda pos,old:[])
solid=solid.simplify(0.000001)
assert solid.status().name=='NoError',solid.status()
solid=solid.translate((-23.5,-13.75,1.0)).scale((5,5,5))
m=solid.to_mesh64();vp=np.array(m.vert_properties);tri=np.asarray(m.tri_verts)
verts,inv=np.unique(np.round(vp[:,:3],5),axis=0,return_inverse=True);faces=inv[tri]
mat=np.zeros(len(tri),dtype=int)
cent=vp[tri,:3].mean(axis=1)/5+np.array([23.5,13.75,-1.0])
for item in LOG:
 lo=np.array(item['bounds_m'][:3]);hi=np.array(item['bounds_m'][3:]);inside=((cent>=lo-1e-4)&(cent<=hi+1e-4)).all(axis=1);surface=np.minimum(abs(cent-lo),abs(cent-hi)).min(axis=1)<1e-4
 if 'plane_xy' in item:
  aa,bb,th=item['plane_xy'];aa=np.array(aa);bb=np.array(bb);vv=bb-aa;nn=np.array([-vv[1],vv[0]])/np.linalg.norm(vv);distance=abs((cent[:,:2]-aa)@nn);surface |= abs(distance-th/2)<1e-4
 if item.get('roof_surface'):surface |= abs(cent[:,2]-(14.12-4.12/13.75*abs(cent[:,1]-13.75)))<1e-4
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
q={'triangles':len(faces),'vertices':len(verts),'watertight':bool(t.is_watertight),'winding_consistent':bool(t.is_winding_consistent),'bounds_mm':t.bounds.tolist(),'extents_mm':t.extents.tolist(),'volume_mm3':t.volume,'mesh_sha256':hashlib.sha256((R/'mesh.npz').read_bytes()).hexdigest(),'scale':'1:200','status':'GEOMETRY_PASS_SEE_SEPARATE_SOURCE_AND_RENDER_QA'}
(R/'BUILD-QA.json').write_text(json.dumps(q,indent=2));print(json.dumps(q),flush=True)
