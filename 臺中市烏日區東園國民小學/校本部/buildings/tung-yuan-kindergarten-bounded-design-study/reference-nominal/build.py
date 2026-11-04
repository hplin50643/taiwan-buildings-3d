import bpy,bmesh,json,math,struct,hashlib
from pathlib import Path
from mathutils import Vector
P=Path(__file__).resolve().parent;W=P.parent
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
S=.06;T=.8;records=[];objects=[]
def pw(v,a,b):
 i=0
 while i<len(a)-2 and v>a[i+1]:i+=1
 return b[i]+(v-a[i])*(b[i+1]-b[i])/(a[i+1]-a[i])
def py(y):return pw(y,[340,523,621,804,939,1028],[0,770,1180,1950,2515,2890])*S
def px(x,shift=0):return (x+shift-499)*4.2*S
def eu(u):return pw(u,[655,745,879,1063,1160,1344],[2890,2515,1950,1180,770,0])*S
def ez(v,lower=False):return pw(v,[938,1075,1150,1236,1241],[1270,695,380,20,0])*S if lower else pw(v,[299,435,509,595,600],[1270,695,380,20,0])*S
def mat(n,c):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);return m
neutral=mat('PROXY neutral unverified enclosure',(.56,.59,.60));window=mat('PROXY opaque mixed window-door not glass',(.37,.44,.47));white=mat('SOURCE family approximate white on mapped front',(.88,.88,.85));silver=mat('SOURCE courtyard roof nominal silver family',(.67,.70,.72));back=mat('PROXY artificial back and cut returns',(.40,.44,.48));platform=mat('PROXY bounded platform artificial cuts',(.62,.58,.51))
def mesh(name,vs,fs,material=neutral):
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);me.materials.append(material);me.materials.append(back)
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();return o

def prism(name,poly,axis,c,sign=1,t=T,material=neutral):
 # polygon coordinates are (horizontal coordinate on face, height) for X/Y faces orXY forZ.
 def world(q,z,d):return(c+d,q,z)if axis=='X'else((q,c+d,z)if axis=='Y'else(q,z,c+d))
 n=len(poly);vs=[world(q,z,d)for d in [0,-sign*t]for q,z in poly];fs=[tuple(range(n)),tuple(range(2*n-1,n-1,-1))]+[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)]
 o=mesh(name,vs,fs,material)
 for f in o.data.polygons:f.material_index=0 if f.index==0 else 1
 return o
def boxcut(o,axis,c,rect):
 a,b,z0,z1=rect;cut=prism('CUT',[(a,z0),(b,z0),(b,z1),(a,z1)],axis,c+5,1,10)
 bpy.context.view_layer.objects.active=o;m=o.modifiers.new('whole assembly excluded','BOOLEAN');m.operation='DIFFERENCE';m.solver='EXACT';m.object=cut;bpy.ops.object.modifier_apply(modifier=m.name);bpy.data.objects.remove(cut,do_unlink=True)
def register(o,cl,extra):
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();o.data.update();objects.append(o)
 if o.name=='SOURCE_NORMALIZED_F_GABLE':
  for f in o.data.polygons:f.material_index=0 if all(abs(o.data.vertices[k].co.y-py(1034))<1e-5 for k in f.vertices) else 1
 records.append({'id':o.name,'class':cl,**extra})
def wall(name,axis,c,sign,q0,q1,z0,z1,holes):
 o=prism(name,[(q0,z0),(q1,z0),(q1,z1),(q0,z1)],axis,c,sign)
 clipped=[]
 for h in holes:
  a,b,lo,hi=h;a=max(a,q0);b=min(b,q1);lo=max(lo,z0);hi=min(hi,z1)
  if b-a<.02 or hi-lo<.02:continue
  boxcut(o,axis,c,(a,b,lo,hi));clipped.append([a,b,lo,hi])
  # Slightly smaller removable opaque assembly proxy; not a glass or true opening claim.
  if b-a>.3 and hi-lo>.3:
   pp=prism(name+'__MIXED_'+str(len(clipped)),[(a+.15,lo+.15),(b-.15,lo+.15),(b-.15,hi-.15),(a+.15,hi-.15)],axis,c-sign*.25,sign,.6,window)
   register(pp,'PROXY_MIXED_ASSEMBLY',{'artificial_clearance_mm':.15,'artificial_recess_mm':.25,'parent':name,'real_frame_geometry':False})
 register(o,'PROXY_DESIGN_ENCLOSURE_BAND',{'plane_axis':axis,'plane_mm':c,'range':[q0,q1,z0,z1],'excluded_whole_groups':clipped,'back_thickness_mm':T,'hidden_height':'nominal design band, not exact asbuilt','joints':'not merged; collision review required'})
def upperholes(floor):
 boxes=([[893,531,1047,595],[1174,531,1255,595],[1265,539,1310,586]]if floor==1 else [[893,455,1047,509],[1174,455,1255,509],[1258,458,1315,509]])
 return [[min(eu(a),eu(c)),max(eu(a),eu(c)),min(ez(b),ez(d)),max(ez(b),ez(d))]for a,b,c,d in boxes]
def rearholes(floor):
 boxes=([[697,1174,823,1236],[874,1174,903,1236],[953,1174,1104,1236],[1273,1175,1326,1235]]if floor==1 else [[697,1087,823,1121],[874,1087,903,1121],[953,1087,1104,1121],[1273,1088,1326,1120]])
 def y(u):return pw(u,[655,838,935,1119,1254,1344],[0,770,1180,1950,2515,2890])*S
 return [[y(a),y(c),min(ez(b,True),ez(d,True)),max(ez(b,True),ez(d,True))]for a,b,c,d in boxes]
for floor,shift,right,left,core,z0,z1 in [(1,-68,638,437,624,20*S,380*S),(2,0,569,368,555,380*S,645*S)]:
 for n,lo,hi,x in [('AB',334,530,right),('CORE',530,615,core),('CD',615,862,right)]:wall(f'PROXY_{floor}F_COURT_{n}','X',px(x,shift),1,py(lo),py(hi),z0,z1,upperholes(floor))
 wall(f'PROXY_{floor}F_REAR','X',px(left,shift),-1,py(334),py(862),z0,z1,rearholes(floor))
 # Core transverse returns evidenced in plan, artificial height band; no invented5px full-height jamb recess.
 for y,sgn in [(530,-1),(615,1)]:wall(f'PROXY_{floor}F_CORE_RETURN_{y}','Y',py(y),sgn,px(core,shift),px(right,shift),z0,z1,[])
 # Service north recess from independent1213, not a rectangle extrusion.
 loop=([(437,934),(587,934),(587,946),(616,946),(616,934),(638,934),(638,1034),(437,1034)]if floor==1 else[(368,934),(518,934),(518,946),(547,946),(547,934),(569,934),(569,1034),(368,1034)])
 door=(535,558)if floor==1 else(466,489)
 for i,(a,b)in enumerate(zip(loop,loop[1:]+loop[:1])):
  # F end replaced by independently defined gable, not duplicate slab.
  if a[1]==b[1]==1034:continue
  if a[0]==b[0]:
   sign=1 if a[0]==right else -1
   wall(f'PROXY_{floor}F_SERVICE_{i}','X',px(a[0],shift),sign,min(py(a[1]),py(b[1])),max(py(a[1]),py(b[1])),z0,z1,rearholes(floor)if a[0]==left else [])
  else:
   # North access height unproven: leave entire vertical door interval unbuilt, no panel.
   lo,hi=sorted([px(a[0],shift),px(b[0],shift)]);parts=[(lo,hi)]
   if a[1]==934:
    dl,dh=px(door[0],shift),px(door[1],shift);parts=[(lo,min(hi,dl)),(max(lo,dh),hi)]
   for k,(l,h)in enumerate(parts):
    if h>l+.01:wall(f'PROXY_{floor}F_SERVICE_{i}_{k}','Y',py(a[1]),-1,l,h,z0,z1,[])
# Independent normalized end profiles. F yellowcolumn/corridor never filled.
fpoly=[(-554.4*S,20*S),(-554.4*S,645*S),(-625*S,645*S),(0,1270*S),(625*S,645*S),(294*S,645*S),(294*S,20*S)]
fo=prism('SOURCE_NORMALIZED_F_GABLE',fpoly,'Y',py(1034),1,material=white)
for a,b,c,d in [(934,554,991,570),(1008,554,1024,570)]:
 r=((a-1000)*4.2*S,(c-1000)*4.2*S,min(ez(b),ez(d)),max(ez(b),ez(d)));boxcut(fo,'Y',py(1034),r)
 pp=prism('PROXY_F_LOW_WINDOW_'+str(a),[(r[0]+.15,r[2]+.15),(r[1]-.15,r[2]+.15),(r[1]-.15,r[3]-.15),(r[0]+.15,r[3]-.15)],'Y',py(1034)-.25,1,.6,window);register(pp,'PROXY_MIXED_ASSEMBLY',{'original_WE_bbox':[a,b,c,d]})
register(fo,'SOURCE_NORMALIZED_PROFILE_WITH_ARTIFICIAL_BACK',{'source':'1052 Fwhite7point domain','normalized_roof_triangle':True,'yellowcolumn_and_corridor_unbuilt':True})
apix=[[868,1235],[868,1087],[850,1087],[1000,938],[1148,1087],[1131,1087],[1131,1226],[990,1235]]
apoly=[]
for u,v in apix:
 x=(1000-u)*4.2*S;z=ez(v,True)
 if v==938:x=0;z=1270*S
 if v==1087:
  z=645*S
  if u==850:x=625*S
  if u==1148:x=-625*S
 apoly.append((x,z))
ao=prism('SOURCE_NORMALIZED_A_END',apoly,'Y',py(334),-1)
for a,b,c,d in [(880,1178,930,1235),(868,1095,936,1162)]:
 x0=(1000-c)*4.2*S;x1=(1000-a)*4.2*S;boxcut(ao,'Y',py(334),(x0,x1,min(ez(b,True),ez(d,True)),max(ez(b,True),ez(d,True))))
register(ao,'SOURCE_NORMALIZED_PROFILE_WITH_ARTIFICIAL_BACK',{'upper_door_occlusion':'conservative whole bounding union; not a true doorhole','slopedbase_retained':True,'colour':'neutral'})
# Two normalized roofskins; clip onlyback at ridge. Unknown projected domains remain omitted.
for side,lo,hi,hole in [('left',1325,1473,[1342,517,1412,628]),('right',1473,1622,[1534,517,1605,628])]:
 def rx(x):return (x-1473)*625/(1473-1325 if x<=1473 else 1622-1473)*S
 vs=[];idx={};quads=[]
 def vertex(x,y):
  if(x,y)not in idx:idx[x,y]=len(vs);X=rx(x);vs.append((X,py(y),1270*S-abs(X)))
  return idx[x,y]
 for a,b in zip([lo,hole[0],hole[2]],[hole[0],hole[2],hi]):
  for c,d in zip([334,hole[1],hole[3]],[hole[1],hole[3],1034]):
   if hole[0]<(a+b)/2<hole[2]and hole[1]<(c+d)/2<hole[3]:continue
   quads.append([vertex(a,c),vertex(b,c),vertex(b,d),vertex(a,d)])
 N=len(vs);off=(T/math.sqrt(2)*(1 if side=='left'else -1),0,-T/math.sqrt(2))
 for x,y,z in list(vs):
  bx=x+off[0];bz=z+off[2]
  if(side=='left'and bx>0)or(side=='right'and bx<0):bx=0;bz=1270*S-T*math.sqrt(2)
  vs.append((bx,y,bz))
 fs=list(quads)+[[i+N for i in reversed(q)]for q in quads];edges={}
 for q in quads:
  for a,b in zip(q,q[1:]+q[:1]):edges.setdefault(tuple(sorted((a,b))),[]).append((a,b))
 for ab in edges.values():
  if len(ab)==1:a,b=ab[0];fs.append([a,b,b+N,a+N])
 o=mesh('SOURCE_NORMALIZED_ROOF_'+side,vs,fs,silver if side=='right'else neutral)
 for f in o.data.polygons:f.material_index=0 if f.index<len(quads)else 1
 register(o,'SOURCE_NORMALIZED_SHELL_ARTIFICIAL_BACK',{'RF_unbuilt_mask':hole,'front_equation':'Z=76.2-abs(X)','artificial_back_normal_mm':T,'ridge_back_clip':True})
# Bounded platform, two artificialcut edges; not fullfloor slab.
poly=[(px(x),py(y))for x,y in [(569,842),(644,842),(741,939),(605,1076),(569,1040)]]
o=prism('PROXY_BOUNDED_2F_PLATFORM',poly,'Z',380*S,1,1.0,platform);register(o,'PROXY_FINITE_PLATFORM',{'source':'1213 and1215','artificial_thickness_mm':1,'artificial_cut_edges':'5691040→569842→644842','not_complete_slab':True})
# Entry remains only an openline curve, not an imaginary slab or wall.
cu=bpy.data.curves.new('UNBUILT_1F_ENTRY_GUIDE','CURVE');cu.dimensions='3D';cu.bevel_depth=.12;sp=cu.splines.new('POLY');line=[(713,1022),(768,966),(824,1022)];sp.points.add(len(line)-1)
for v,(x,y)in zip(sp.points,line):v.co=(px(x,-68),py(y),20*S,1)
o=bpy.data.objects.new('UNBUILT_1F_ENTRY_GUIDE display only',cu);bpy.context.collection.objects.link(o)
# Export each separatemesh, never call their concatenation printablewholebuilding.
(P/'parts').mkdir(exist_ok=True)
for o in objects:
 data=bytearray(b'TUNG YUAN NOMINAL RESEARCH SOURCE/PROXY SEPARATE PART'.ljust(80,b' '));data+=struct.pack('<I',len(o.data.polygons))
 for f in o.data.polygons:
  v=[o.data.vertices[i].co for i in f.vertices];assert len(v)==3;data+=struct.pack('<12fH',*f.normal,*v[0],*v[1],*v[2],0)
 path=P/'parts'/(o.name+'.stl');path.write_bytes(data)
 for r in records:
  if r['id']==o.name:r.update({'file':str(path.relative_to(P)),'sha256':hashlib.sha256(data).hexdigest(),'triangles':len(o.data.polygons),'bbox':[[min(v.co[k]for v in o.data.vertices)for k in range(3)],[max(v.co[k]for v in o.data.vertices)for k in range(3)]]})
(P/'BUILD-RECORD.json').write_text(json.dumps({'status':'INTEGRATED_BOUNDED_DESIGN_TRIAL_NO_PUBLICATION_NO_FIT_CERTIFICATE','parts':records,'not_fullbuilding':True,'closed_roombox_claim':False,'source_originals_edited':False},indent=2)+'\n')
sc=bpy.context.scene;sc.render.engine='BLENDER_WORKBENCH';sc.display.shading.light='STUDIO';sc.display.shading.color_type='MATERIAL';sc.display.shading.show_shadows=False;sc.display.shading.show_cavity=True;sc.world.color=(.94,.94,.94);sc.display.shading.background_type='WORLD';sc.render.resolution_x=1500;sc.render.resolution_y=1300;sc.render.resolution_percentage=100;sc.view_settings.view_transform='Standard'
bpy.ops.object.camera_add();cam=bpy.context.object;cam.data.type='ORTHO';sc.camera=cam
for name,loc,tar,scale in [('court-oblique',(270,-190,210),(0,90,35),265),('rear-oblique',(-270,300,210),(0,90,35),265),('top',(0,90,500),(0,90,35),250),('entry-end',(130,430,150),(0,100,35),250)]:
 cam.location=loc;cam.rotation_euler=(Vector(tar)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale;sc.render.filepath=str(P/(name+'.png'));bpy.ops.render.render(write_still=True)
sc.render.filepath='//court-oblique.png';bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(P/'scene.blend'))
