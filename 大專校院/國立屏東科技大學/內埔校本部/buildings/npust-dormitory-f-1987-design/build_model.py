"""NPUST historical F dormitory1987; corrected F-only source package. Units metres to1:200 mm. No current/asbuilt claim."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
from manifold3d import Manifold,CrossSection
R=Path(__file__).resolve().parent;P=[];LOG=[];IDS={};S=5
PALETTE=[('light mosaic approximate','#C9C7B7'),('concrete approximate','#AAAFA6'),('roof finish approximate','#B7B8AA'),('window frame approximate','#A6ABA5'),('authored display support not surveyed terrain','#A3AD9B'),('opaque glazing illustration','#546D75'),('closed entrance approximation','#737C79'),('dark mosaic approximate','#858675')]
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


# F-only exterior. x0=axis18,x61.2=axis1; y0=A,y8=B,y13.9=C,y21.9=D.
# Excludes E A4-7 and unassigned A4-8. No hidden rooms or terrain inferred.
bx('authored_display_support_not_terrain',-2.2,63.4,-2.2,24.1,-.85,-.55,4)
body=box(-.135,36.135,7.865,22.035,-.55,13.25)+box(25.065,61.335,-.135,14.035,-.55,13.25)
W=[]
def opening(n,axis,face,c,w,z0,z1,sgn=1,style='normal'):
 global body
 cut=box(c-w/2,c+w/2,face-.30,face+.30,z0,z1) if axis=='y' else box(face-.30,face+.30,c-w/2,c+w/2,z0,z1)
 body=body-cut;W.append((n,axis,face,c,w,z0,z1,sgn,style))
# South silhouette: 7 recessed northern-wing bays then10 southern-wing bays.
# North: bathing band at northern-wing bays9/10; no mirrored facade assumption.
for floor in range(4):
 z=floor*3.5
 for i in range(17):
  c=1.8+3.6*i;face=7.865 if i<7 else -.135
  if floor==0 and i==0:opening('south_entry','y',face,c,3.15,z,z+2.65,-1,'door')
  else:opening('south_room','y',face,c,1.50,z+.95,z+2.65,-1)
  face=22.035 if i<10 else 14.035
  if i in [8,9]:opening('north_bathing_high','y',face,c,3.10,z+2.20,z+2.70,1,'high')
  elif floor==0 and i==16:opening('north_entry','y',face,c,3.15,z,z+2.65,1,'door')
  else:opening('north_room','y',face,c,1.50,z+.95,z+2.65,1)
 for n,x,y,sgn in [('west_outer_corridor',-.135,15.10,-1),('west_inner_corridor',25.065,6.80,-1),('east_outer_corridor',61.335,6.80,1)]:opening(n,'x',x,y,1.55,z+.95,z+2.65,sgn)
 opening('east_inner_bathing_high','x',36.135,18.25,5.40,z+2.20,z+2.70,1,'high')
add('closed_F_only_exterior_no_interior_reconstruction',body,0)
# Source-visible facade columns: approximate visible width .34, small authored relief.
for side in ['south','north']:
 for i in range(18):
  x=i*3.6;face=(7.865 if i<=7 else -.135) if side=='south' else (22.035 if i<=10 else 14.035);sgn=-1 if side=='south' else 1
  # Discontinuous changes also have the actual corner from the solid envelope.
  a,b=sorted([face-sgn*.03,face+sgn*.10]);bx(side+'_bay_pilaster_estimated',x-.17,x+.17,a,b,-.55,13.22,1)
# Window framing and distinctive side mosaic patches; opaque backing seals the printable exterior.
for n,axis,face,c,w,z0,z1,sgn,style in W:
 def panel(tag,u0,u1,v0,v1,d0,d1,mat):
  a,b=sorted([face+sgn*d0,face+sgn*d1])
  if axis=='y':bx(n+tag,u0,u1,a,b,v0,v1,mat)
  else:bx(n+tag,a,b,u0,u1,v0,v1,mat)
 panel('_opaque_back',c-w/2-.015,c+w/2+.015,z0-.015,z1+.015,-.35,-.11,6 if style=='door' else 5)
 fw=.09 # .45mm at1:200; printable relief, not original joinery thickness.
 for u in [c-w/2,c+w/2-fw]:panel('_frame_jamb',u,u+fw,z0,z1,-.16,.04,3)
 for zz in [z0,z1-fw]:panel('_frame_rail',c-w/2,c+w/2,zz,zz+fw,-.16,.04,3)
 if style=='normal':
  panel('_lower_center_mullion',c-fw/2,c+fw/2,z0,z1-.48,-.15,.025,3)
  panel('_transom_rail',c-w/2,c+w/2,z1-.53,z1-.44,-.15,.025,3)
  floor=int(round((z0-.95)/3.5));fl=floor*3.5
  if axis=='y':
   for a,b in [(c-1.61,c-w/2),(c+w/2,c+1.61)]:panel('_dark_mosaic_sidepatch',a,b,fl+.10,z1,-.035,.015,7)
  else:panel('_dark_mosaic_apron',c-w/2,c+w/2,fl+.10,z0,-.035,.015,7)
 elif style=='high':
  for u in np.arange(c-w/2+.50,c+w/2,.50):panel('_clerestory_mullion',u-fw/2,u+fw/2,z0,z1,-.15,.025,3)
  fl=round((z0-2.2)/3.5)*3.5
  panel('_bath_mosaic_panel',c-w/2,c+w/2,fl+.10,z0,-.035,.015,7)
 else:
  for u in [c-w/4,c,c+w/4]:panel('_entrance_division',u-fw/2,u+fw/2,z0,z1-.5,-.15,.025,3)
  panel('_entrance_transom',c-w/2,c+w/2,z1-.55,z1-.46,-.15,.025,3)
# Small entrance risers shown by F elevations; derived equal rises, not canceled site walkway.
for n,c,face,sgn in [('south',1.8,7.865,-1),('north',59.4,14.035,1)]:
 for j in range(3):
  a,b=sorted([face,face+sgn*(3-j)*.28]);bx(n+'_visible_entry_riser_derived',c-1.62,c+1.62,a,b,-.55,-.55+(j+1)*.55/3,1)
# F roof profile 10.50+6.50, rise3.05, vertical step1.16; opposite wings face inward.
# Attic exterior volume is closed for printing; not representation of structural solid roof thickness.
def roof(n,x0,x1,ystart,direction):
 p=[(0,13.18),(17,13.18),(17,14),(10.5,15.89),(10.5,17.05),(0,14)]
 pts=[(ystart+direction*u,z) for u,z in p]
 if sum(pts[i][0]*pts[(i+1)%len(pts)][1]-pts[(i+1)%len(pts)][0]*pts[i][1] for i in range(len(pts)))<0:pts=pts[::-1]
 add(n,CrossSection([pts]).extrude(x1-x0).rotate((90,0,90)).translate((x0,0,0)),2)
# Longitudinal ends are17.5cm fromaxes perF roofplan; A3end100 is transverse, NOT longitudinal.
roof('north_wing_F_roof_opposed_long_slope',-.175,36.175,23.15,-1)
roof('south_wing_F_roof_opposed_long_slope',25.025,61.375,-1.25,1)
# Gable five-circle vents visibly shown on F ends: shallow opaque external relief only.
for n,x,y,sgn in [('NW',-.175,13.85,-1),('NE',36.175,13.85,1),('SW',25.025,8.05,-1),('SE',61.375,8.05,1)]:
 for dy,dz in [(0,.38),(-.20,.06),(.20,.06),(-.13,-.23),(.13,-.23)]:
  # radius .10m raster estimate; depth .09m = .45mm in print, no hidden ventilation system.
  cyl=Manifold.cylinder(.10,.10,.10,24).rotate((0,90,0)).translate((x-.05,y+dy,15.80+dz));add('gable_'+n+'_vent_shallow_representation',cyl,5)

solid=P[0]
for p in P[1:]:solid=solid+p
solid=solid.simplify(0.000001)
solid=solid.translate((-30.6,-10.95,.85)).scale((S,S,S))
m=solid.to_mesh64();v=np.asarray(m.vert_properties)[:,:3];f=np.asarray(m.tri_verts);materials=np.zeros(len(f),dtype=int)
for i,oid in enumerate(m.run_original_id):materials[m.run_index[i]//3:m.run_index[i+1]//3]=IDS[int(oid)]
t=trimesh.Trimesh(v.astype(np.float32).astype(np.float64),f,process=False);t.merge_vertices(digits_vertex=8);keep=t.nondegenerate_faces();materials=materials[keep];t.update_faces(keep);t.remove_unreferenced_vertices();assert t.is_watertight and t.is_winding_consistent;assert len(t.split())==1,[(len(c.faces),c.bounds.tolist()) for c in t.split()]
np.savez_compressed(R/'mesh.npz',vertices=t.vertices,faces=t.faces,materials=materials);t.export(R/'model.stl');(R/'palette.json').write_text(json.dumps(PALETTE));(R/'components.json').write_text(json.dumps(LOG,ensure_ascii=False,indent=2))
q={'status':'PASS_GEOMETRY_ONLY','triangles':len(t.faces),'components':len(t.split()),'watertight':bool(t.is_watertight),'winding':bool(t.is_winding_consistent),'scale':'1:200','datum':'1FL0; F drawingGL-.55, authoredsupportnotterrain','bounds_mm':t.bounds.tolist(),'mesh_sha256':hashlib.sha256((R/'mesh.npz').read_bytes()).hexdigest()};(R/'BUILD-QA.json').write_text(json.dumps(q,indent=2));print(json.dumps(q))
