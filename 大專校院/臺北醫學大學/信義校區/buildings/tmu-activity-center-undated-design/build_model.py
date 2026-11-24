from pathlib import Path
import json,hashlib,numpy as np,trimesh
from manifold3d import Manifold,CrossSection,Mesh64,FillRule
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

# Historical job5716 exterior-stair version; not built/current survey.
# Axes43.2x24; A12 detailed roof controls, A4 conflict retained in documentation.
PALETTE=[('neutral wall','#CBC8BC'),('neutral terrace','#B4B6B2'),('opaque glazing','#526C74'),('neutral frame','#DEDCD0'),('authored display base','#96958D'),('recess','#37464B'),('interpretive roof','#999D9F')]
bx('authored_display_base',-2.2,49.2,-3.5,27.5,-.5,-.03,4)
bx('authored_local_grade',-1.8,48.8,-3.1,27.1,-.06,0,4)
# Exterior envelope backed solid; no claim of modeled hall interiors.
body=along_x([(0,0),(24,0),(24,9.9),(12,13.50),(0,9.9)],0,43.2)
add('solid_backed_hall_envelope_no_interior',body)
# Independent roof chord/purlin interpretation: upper-chordridge13.675, outer skin13.85.
roof_top=13.85; roof_y0=-.90;roof_y1=24.90;eave=roof_top-.30*(12+.90)
roofq=[(roof_y0,eave-.12),(12,roof_top-.12),(roof_y1,eave-.12),(roof_y1,eave),(12,roof_top),(roof_y0,eave)]
add('two_slope_roof_skin_interpretive_175mm_above_chord',along_x(roofq,-.10,43.30),6)
# Gable fascia shown by A3/A12:1.50m vertical band; local joins backed by envelope.
fascia=[(roof_y0,eave-1.50),(12,roof_top-1.50),(roof_y1,eave-1.50),(roof_y1,eave),(12,roof_top),(roof_y0,eave)]
for a,b in [(-.20,.06),(43.14,43.40)]:add('gable_150cm_fascia',along_x(fascia,a,b),0)
# A7 long-side gutter section: base110cm belowtrussdatum9.55, sloped200cm60deg outward lip.
for side in [-1,1]:
 basey=0 if side==-1 else 24
 q=[(0,8.45),(-.60,8.45),(-1.60,10.182),(-1.44,10.272),(-.48,8.61),(0,8.61)]
 q=[(basey+(-y if side==1 else y),z) for y,z in q]
 add('A7_folded_longside_eaves_gutter',along_x(q,-1.,44.2),0)
 # Connect inner gutterfloor to envelope over small tolerance.
 bx('gutter_inner_connection',-1.,44.2,basey-.08,basey+.08,8.43,9.60,0)
#13columns perside, spacing3.6; structuraldepth andwindow heights partlyscaled fromchosenA3.
for i in range(13):
 x=3.6*i
 for y in [0,24]:bx('side_frame_axis_'+str(i),x-.15,x+.15,y-.20,y+.20,0,9.56,3)
# Glazed infills selectedA3: central4bays blank for exteriorstairs; X symbols not real braces.
def win_y(name,x0,x1,y,z0,z1,ny=2,nx=4):
 # Opaque backed panels extend0.035m beyond envelope, integral not separate floating sheets.
 ya,yb=(y-.055,y+.025) if y==0 else(y-.025,y+.055)
 bx(name+'_backed_glass',x0,x1,ya,yb,z0,z1,2)
 depth=.075
 ya,yb=(y-depth,y+.03) if y==0 else(y-.03,y+depth)
 for x in [x0,x1]+[x0+(x1-x0)*j/nx for j in range(1,nx)]:bx(name+'_vertical_frame',x-.035,x+.035,ya,yb,z0-.035,z1+.035,3)
 for z in [z0,z1]+[z0+(z1-z0)*j/ny for j in range(1,ny)]:bx(name+'_horizontal_frame',x0-.035,x1+.035,ya,yb,z-.035,z+.035,3)
for y in [0,24]:
 for i in [0,1,2,3,4,9,10]:
  x=3.6*i+.15
  if i not in [4,9]:win_y('W1_330x120',x,x+3.30,y,1.50,2.70)
  else:win_y('D3_330x270',x,x+3.30,y,.75,3.45,ny=2,nx=4)
  # SourceW2labels150 and325notidentical: preserveA3opening envelope withlimitedpanes.
  win_y('W2_group_A3_envelope_estimated_sill',x,x+3.30,y,5.10,8.35,ny=4 if i<2 else 2,nx=4)
 # Last bay solid aschosenA3; blankcentralfourbays notfilledbyotherrevision glazing.
# Gablepaneljoints correspondingA1 widthaxes; frontdoorsD1+D2 groups beneathopaque upperwall.
for x in [0,43.2]:
 for y in [5.175,9.125,14.875,18.825]:
  top=roof_top-.3*abs(y-12)-1.5
  bx('gable_vertical_panel_seam',x-.035,x+.035,y-.045,y+.045,3.65,top,3)
def win_x(name,x,y0,y1,z0,z1,n=4):
 xa,xb=(x-.055,x+.025) if x==0 else(x-.025,x+.055)
 bx(name+'_backed',xa,xb,y0,y1,z0,z1,2)
 xa,xb=(x-.075,x+.03) if x==0 else(x-.03,x+.075)
 for y in [y0,y1]+[y0+(y1-y0)*j/n for j in range(1,n)]:bx(name+'_v',xa,xb,y-.035,y+.035,z0-.03,z1+.03,3)
 for z in [z0,z1,z1-.70]:bx(name+'_h',xa,xb,y0-.03,y1+.03,z-.035,z+.035,3)
win_x('front_D1_540x270',43.2,9.3,14.7,.75,3.45,6)
win_x('front_D2_left_360x270',43.2,5.7,9.3,.75,3.45)
win_x('front_D2_right_360x270',43.2,14.7,18.3,.75,3.45)
# Front raisedapron and5steps at15cm; extentsA1scaled notA2upper338.
bx('front_platform_A1_scaled',43.15,46.95,4.625,19.375,0,.75,1)
for k in range(5):bx('front_five_step_15cm',46.90+k*.15,47.05+k*.15,4.625,19.375,0,.75-.15*k,1)
# A1flowerwells320cmwide withscaled380cmprojection; A7different405x530notmixed.
for y0,y1 in [(1.425,4.625),(19.375,22.575)]:
 outer=box(43.15,47.0,y0,y1,0,1.05);inner=box(43.38,46.77,y0+.23,y1-.23,.18,1.1)
 add('A1_front_flower_well_scaled_projection',outer-inner,0)
# A2upperfrontplatform explicit338projection x1475wide;90cm parapet simplified.
bx('A2_front_upper_gallery_platform',43.15,46.58,4.625,19.375,3.80,4.0,1)
for y in [4.625,19.375]:bx('upper_platform_end_parapet',43.2,46.58,y-.09,y+.09,3.99,4.90)
bx('upper_platform_front_parapet',46.42,46.58,4.625,19.375,3.99,4.90)
# Rearopaque lowglazingband A3; side service door and access steps approximate location.
for y0,y1 in [(5.325,8.975),(9.275,14.725),(15.025,18.675),(18.975,23.85)]:win_x('rear_lower_glazing_A3',0,y0,y1,.75,2.45,4)
win_x('rear_service_door',0,3.75,4.75,1.85,4.0,2)
for k in range(10):bx('rear_stage_access_scaled_steps',-2.0+k*.20,-1.78+k*.20,3.55,4.95,0,.185*(k+1),1)
# External20risers at19cm; top~4.00 perA8, bottom+.20 coordination assumptionNOT measuredGL.
# No added20cmthreshold: lowerfoot isanchoredwithplainunderfill explicitdisplay support.
# A7 open underside: stepped thin slabs, not a filled ramp. Opposite-side flights reverse per A2.
def stair_prism(q,y0,y1,flip):
 if flip:q=[(50.10-x,z) for x,z in q]
 return along_x([(-x,z) for x,z in q],0,y1-y0).rotate((0,0,90)).translate((0,y0,0))
for y0,y1,ywall,flip in [(-1.40,-.20,0,True),(24.20,25.40,24,False)]:
 start=21.60;mid=23.85;second=25.05;top=27.30;end=28.50
 for xa,za in [(start,.20),(second,2.10)]:
  q=[(xa,za-.15),(xa,za+.19)]
  for k in range(10):
   xx=xa+k*.25;zz=za+.19*(k+1)
   if k:q.append((xx,zz))
   q.append((xx+.25,zz))
  q.extend([(xa+2.50,za+1.90-.20),(xa,za-.15)])
  add('exterior_open_underside_stepped_slab',stair_prism(q,y0,y1,flip),1)
 for xa,xb,z in [(mid,second,2.10),(top,end,4.0)]:
  add('exterior_thin_landing',stair_prism([(xa-.02,z-.20),(xb+.02,z-.20),(xb+.02,z),(xa-.02,z)],y0,y1,flip),1)
 mx0,mx1=(50.10-second,50.10-mid) if flip else(mid,second)
 bx('exterior_midlanding_short_beam_scaled_40cm',mx1-.30,mx1,min(y0,ywall),max(y1,ywall),1.70,2.10,1)
 # Lowerfoot plain authored grade connection, restricted to first25cm; not a source datum claim.
 add('exterior_lowerfoot_coordination_support',stair_prism([(start,-.02),(start+.25,-.02),(start+.25,.30),(start,.30)],y0,y1,flip),1)
 tx0,tx1=(50.10-end,50.10-top) if flip else(top,end)
 bx('exterior_landing_wall_connection',tx0,tx1,min(y0,ywall),max(y1,ywall),3.80,4.,1)
 win_y('exterior_gallery_D8',tx0+.10,tx0+1.10,ywall,4.,6.,ny=1,nx=1)
 for xa,xb,za,zb in [(start,mid,.20,2.10),(mid,second,2.10,2.10),(second,top,2.10,4.),(top,end,4.,4.)]:
  q=[(xa,za-.04),(xb,zb-.04),(xb,zb+.85),(xa,za+.85)]
  add('exterior_stair_parapet_simplified',stair_prism(q,y0-.10 if ywall==0 else y1-.05,y0+.05 if ywall==0 else y1+.10,flip),0)
# Unifiedmesh export in1:200mm.
solid=P[0]
for part in P[1:]:solid=solid+part
solid=solid.simplify(1e-7).translate((-22.0,-12.0,.5)).scale((1000/200,)*3)
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
 ee=np.sort(t.edges,axis=1); uu,cc=np.unique(ee,axis=0,return_counts=True);print('bad edges metres',t.vertices[np.unique(uu[cc>2])]/5+np.array([22.,12.,-.5]),flush=True)
assert t.is_watertight and t.is_winding_consistent
cent=t.triangles_center/(1000/200)+np.array([22.,12.,-.5]);mat=np.zeros(len(t.faces),dtype=int)
for a in LOG:
 lo=np.array(a['bounds_m'][:3]);hi=np.array(a['bounds_m'][3:]);inside=((cent>=lo-1e-4)&(cent<=hi+1e-4)).all(axis=1);surface=np.minimum(abs(cent-lo),abs(cent-hi)).min(axis=1)<1e-4;mat[inside&surface]=a['material']
np.savez_compressed(R/'mesh.npz',vertices=t.vertices,faces=t.faces,materials=mat)
t.export(R/'model.stl');(R/'components.json').write_text(json.dumps(LOG,indent=2));(R/'palette.json').write_text(json.dumps(PALETTE))
q={'status':'PASS_GEOMETRY','triangles':len(t.faces),'watertight':bool(t.is_watertight),'winding':bool(t.is_winding_consistent),'components':len(t.split()),'scale':'1:200','mesh_sha256':hashlib.sha256((R/'mesh.npz').read_bytes()).hexdigest()}
(R/'BUILD-QA.json').write_text(json.dumps(q,indent=2));print(q,flush=True)
