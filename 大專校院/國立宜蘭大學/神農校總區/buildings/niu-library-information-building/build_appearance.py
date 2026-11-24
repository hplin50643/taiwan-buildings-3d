"""Add source-guided approximate materials; never modify original mesh or locked previews.
Run Blender 4.3.2: blender -b -t 1 --python-exit-code 1 -P build_appearance.py
Requires original scene.blend and model.stl alongside this script. No source photos embedded.
"""
from pathlib import Path
import sys
import bpy,hashlib,json,math,struct,zipfile,xml.etree.ElementTree as ET
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'scene.blend'))
bpy.context.preferences.filepaths.save_version=0
obj=next(o for o in bpy.context.scene.objects if o.type=='MESH');mesh=obj.data
verts=[tuple(v.co) for v in mesh.vertices];faces=[tuple(p.vertices) for p in mesh.polygons]
assert all(len(f)==3 for f in faces)
def digest(a,fmt):return hashlib.sha256(b''.join(struct.pack(fmt,*r) for r in a)).hexdigest()
before={'vertices':digest(verts,'<3f'),'faces':digest(faces,'<3I')}
# Historical grey-stair study, two source-visible elevations only.
palette=[('Unknown oblique rear roof and base','#AAA79F',.86),('Visible pale grey white tile facade','#D1D3CE',.86),('Original grey taupe shade blades and frames','#9C9B90',.86),('True window backs opaque mixed appearance','#71817C',.86),('True recessed entrance backing','#505B57',.86),('Historical visible stairs and thick guards','#989991',.86)]
def rgb(h):return tuple(int(h[i:i+2],16)/255 for i in (1,3,5))
def lin(v):return v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4
mesh.materials.clear()
for name,col,rough in palette:
 m=bpy.data.materials.new(name);m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=tuple(lin(v) for v in rgb(col))+(1,);bs.inputs['Roughness'].default_value=rough;m.diffuse_color=tuple(rgb(col))+(1,);mesh.materials.append(m)
import numpy as np
EPS=.002;indices=[];original_indices=[];changed_faces=[];change_reasons={};support_records=[]
def bounds(a,b):return bool(np.all(lo>=np.array(a)-EPS) and np.all(hi<=np.array(b)+EPS))
def plane(k,t):return max(abs(q[:,k]-t))<EPS
def boxface(x,y,z,w,d,h):
 a=(x-w/2,y-d/2,z);b=(x+w/2,y+d/2,z+h)
 return bounds(a,b) and any((plane(k,a[k]) and n[k]<-.8) or (plane(k,b[k]) and n[k]>.8) for k in range(3))
def frontback(x,z,w,h,y=-50.2):return plane(1,y) and n[1]<-.99 and bounds((x-w/2,y,z),(x+w/2,y,z+h))
def rightback(y,z,w,h,x=46.2):return plane(0,x) and n[0]>.99 and bounds((x,y-w/2,z),(x,y+w/2,z+h))
for p in mesh.polygons:
 q=np.array([verts[j] for j in p.vertices]);n=np.array(p.normal);lo=q.min(0);hi=q.max(0);i=0
 if plane(1,-52) and n[1]<-.99 and bounds((-48,-52,2.8),(48,-52,78)):i=1
 if plane(0,48) and n[0]>.99 and bounds((48,-52,2.8),(48,67,78)):i=1
 for x in [7,15,35,47]:
  if boxface(x,-51,2.9,3,3.1,21.5):i=1
 for y in [-44,-29,-14]:
  if boxface(47,y,2.9,3.1,3,12):i=1
 if boxface(46,-29,12.5,4,33,2):i=1
 # Original lower left canopy is known in source, retained coarse grey material.
 if boxface(-20,-54,12.5,40,6,1.8):i=2
 for x in [-32,-24,-16,-8]:
  for z,h in [(5,7.2),(15,8.1)]:
   if frontback(x,z,6,h,-50.25):i=3
 for x in [-32,-24,-16,-8,9,19,29,39]:
  for z in ([26,37,48,59] if x<0 else [37,48,59]):
   if frontback(x,z,6.4 if x<0 else 7.1,8.2):i=3
   for dx in [-2.6,2.6]:
    if boxface(x+dx,-52,z-.2,1.1,4.2,8.6):i=2
   if boxface(x,-52.3,z+5.7,7.7,4.1,1.2):i=2
 for z in [29,40,51,62]:
  if frontback(0,z,5.8,1.7):i=3
 for x in [5,11,15,21.2,25,32,36,43]:
  if frontback(x,26,1.9,8.5):i=3
 for x in [9,19,29,39]:
  if frontback(x,70,5.5,5.4):i=3
 for j,y in enumerate([-38,-22,-6,10,26,42,58]):
  for dy in [-3.3,3.3]:
   yy=y+dy
   if rightback(yy,70,4.4,5.4):i=3
   for z in [37,48,59]:
    if j==3:continue
    if rightback(yy,z,4.7,8.2):i=3
    if boxface(48,yy,z+5.7,4,5.8,1.15):i=2
   if j<3:
    if rightback(yy,26,2,8.5):i=3
   elif j!=3:
    if rightback(yy,26,4.7,8.2):i=3
   if j>1:
    for z in [5,15]:
     if rightback(yy,z,4.6,7.2):i=3
 if rightback(10,26,5.2,41.1,46.1):i=3
 for z in np.arange(27.5,66,5):
  if boxface(48,10,z,4,5.4,1.1):i=2
 for x in [12,24,39]:
  if frontback(x,5,9,14,-35.4):i=4
 # Main flared stair and guards use the exact individual original boxes.
 for k in range(20):
  w=24-5*min(k/9,1);y=-72+k*1.35;h=(k+1)*.6
  if bounds((25-w/2,y-.8,2.9),(25+w/2,y+.8,2.9+h)) and ((plane(2,2.9+h) and n[2]>.99) or (plane(1,y-.8) and n[1]<-.99)):i=5
  for sg in [-1,1]:
   if boxface(25+sg*(w/2+.6),y,2.9,2,1.85,h+2):i=5
 for k in range(4):
  y=-58+k*1.4;h=.55*(k+1)
  if bounds((-42,y-.8,2.9),(2,y+.8,2.9+h)) and ((plane(2,2.9+h) and n[2]>.99) or (plane(1,y-.8) and n[1]<-.99)):i=5
 if hi[2]<=3+EPS:i=0
 p.material_index=i;indices.append(i);original_indices.append(i)

# V2: reuse the original palette on complete original outside surfaces only.
# All candidate vertices must lie in a bounded support and on a material plane.
# Undocumented elevations are explicit same-building continuity inferences.
supports=[]
def support(label,origin,u,v,umin,umax,vmin,vmax,zmin,zmax,back=False):
 supports.append(dict(label=label,origin=origin,u=u,v=v,umin=umin,umax=umax,vmin=vmin,vmax=vmax,zmin=zmin,zmax=zmax,back=back))
def window(label,origin,u,v,width,depth,z,height):
 support(label,origin,u,v,-width/2,width/2,-depth,0,z,z+height,True)
# Local u is facade tangent, local v points out of the building.
for x in [7,18,29,40]:
 for z in [6,17,28,39,50,61,70]:window('rear_window', [x,67], [1,0],[0,1],6.5,1.8,z,5.4)
for y in [17,31,45,59]:
 for z in [6,17,28,39,50,61,70]:window('return_window',[0,y],[0,1],[-1,0],8.5,1.8,z,5.4)
a=np.array([-48.,-52.]);b=np.array([-20.,8.]);t=(b-a)/np.linalg.norm(b-a);outward=np.array([-t[1],t[0]])
for f in [.16,.36,.56,.76,.92]:
 for z in [6,17,28,39,50,61,70]:window('oblique_window',(a+f*(b-a)).tolist(),t.tolist(),outward.tolist(),7.5,1.8,z,5.4)
# Existing source-facing front and right openings: reveal planes only. Their
# original backing faces already have material and are never overwritten.
for x in [-32,-24,-16,-8]:
 for z,h in [(5,7.2),(15,8.1)]:window('front_lower_window',[x,-52],[1,0],[0,-1],6,1.75,z,h)
for x in [-32,-24,-16,-8,9,19,29,39]:
 for z in ([26,37,48,59] if x<0 else [37,48,59]):window('front_louver_window',[x,-52],[1,0],[0,-1],6.4 if x<0 else 7.1,1.8,z,8.2)
for z in [29,40,51,62]:window('front_horizontal_slit',[0,-52],[1,0],[0,-1],5.8,1.8,z,1.7)
for x in [5,11,15,21.2,25,32,36,43]:window('front_vertical_slit',[x,-52],[1,0],[0,-1],1.9,1.8,26,8.5)
for x in [9,19,29,39]:window('front_top_window',[x,-52],[1,0],[0,-1],5.5,1.8,70,5.4)
for j,y in enumerate([-38,-22,-6,10,26,42,58]):
 for dy in [-3.3,3.3]:
  yy=y+dy;window('right_top_window',[48,yy],[0,1],[1,0],4.4,1.8,70,5.4)
  for z in [37,48,59]:
   if j!=3:window('right_main_window',[48,yy],[0,1],[1,0],4.7,1.8,z,8.2)
  if j<3:window('right_slit',[48,yy],[0,1],[1,0],2,1.8,26,8.5)
  elif j!=3:window('right_lower_main_window',[48,yy],[0,1],[1,0],4.7,1.8,26,8.5)
  if j>1:
   for z in [5,15]:window('right_lower_window',[48,yy],[0,1],[1,0],4.6,1.8,z,7.2)
window('right_continuous_recess',[48,10],[0,1],[1,0],5.2,1.9,26,41.1)
# Original continuous external wall planes, including outer parapet faces.
walls=[('front_wall',[-48,-52],[1,0],[0,-1],96),('right_wall',[48,-52],[0,1],[1,0],119),('rear_wall',[0,67],[1,0],[0,1],48),('return_wall',[0,8],[0,1],[-1,0],59),('shoulder_wall',[-20,8],[1,0],[0,1],20),('oblique_wall',a.tolist(),t.tolist(),outward.tolist(),float(np.linalg.norm(b-a)))]
for p in mesh.polygons:
 if original_indices[p.index]!=0:continue
 q=np.array([verts[j] for j in p.vertices]);n=np.array(p.normal);lo=q.min(0);hi=q.max(0)
 if hi[2]<=3+EPS:continue
 chosen=None
 for label,origin,u,v,L in walls:
  local=q[:,:2]-origin;uu=local@np.array(u);vv=local@np.array(v)
  if np.max(abs(vv))<EPS and uu.min()>=-EPS and uu.max()<=L+EPS and lo[2]>=3-EPS and hi[2]<=79.6+EPS and np.dot(n[:2],v)>.99:
   chosen=(1,label,'complete_outside_wall_plane',{'origin':origin,'u':u,'v':v,'umin':0,'umax':L,'zmin':3,'zmax':79.6});break
 for ix,r in enumerate(supports):
  local=q[:,:2]-r['origin'];uu=local@np.array(r['u']);vv=local@np.array(r['v']);uv=np.column_stack([uu,vv,q[:,2]])
  low=np.array([r['umin'],r['vmin'],r['zmin']]);high=np.array([r['umax'],r['vmax'],r['zmax']])
  if not (np.all(uv>=low-EPS) and np.all(uv<=high+EPS)):continue
  nn=np.array([np.dot(n[:2],r['u']),np.dot(n[:2],r['v']),n[2]])
  if max(abs(vv-r['vmin']))<EPS and nn[1]>.99:
   chosen=(3,r['label'],'complete_original_window_back',ix);break
  # Cut side walls point INTO the original opening, unlike an outside box.
  if any(max(abs(uv[:,k]-bound))<EPS and nn[k]*sg>.99 for k,bound,sg in [(0,r['umin'],1),(0,r['umax'],-1),(2,r['zmin'],1),(2,r['zmax'],-1)]):
   chosen=(1,r['label'],'complete_original_window_reveal',ix);break
 if chosen:
  i,label,kind,record=chosen;p.material_index=i;indices[p.index]=i;changed_faces.append(p.index)
  change_reasons[str(p.index)]={'family':label,'kind':kind,'support':record,'basis':'All vertices and outward normal fit a complete original bounded material support; same-building continuity inference, not direct evidence for every hidden face.'}
support_records=supports

assert before=={'vertices':digest([tuple(v.co) for v in mesh.vertices],'<3f'),'faces':digest([tuple(p.vertices) for p in mesh.polygons],'<3I')}
obj['appearance_policy']='Original geometry and material values preserved; full exterior-wall and existing window-support color continuity is inferred; unresolved surfaces stay neutral'
scene=bpy.context.scene;scene['appearance_revision']='color-v2-full-face-continuity'
scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=96;scene.cycles.seed=0;scene.cycles.use_denoising=False
scene.render.threads_mode='FIXED';scene.render.threads=1
scene.render.resolution_x=900;scene.render.resolution_y=800
for attr in dir(scene.render):
 if attr.startswith('use_stamp'):
  try:setattr(scene.render,attr,False)
  except (TypeError,AttributeError):pass
scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.82,.85,.89,1);scene.world.node_tree.nodes['Background'].inputs[1].default_value=.65
scene.view_settings.view_transform='Standard';scene.view_settings.look='Medium High Contrast';scene.view_settings.exposure=0;scene.view_settings.gamma=1
# New appearance lighting only: remove inherited lamps, never change original scene.
for lamp in list(scene.objects):
 if lamp.type=='LIGHT':bpy.data.objects.remove(lamp,do_unlink=True)
for name,energy,ang,rot in [('Key',2.1,.16,(28,-26,-32)),('Fill',.55,.35,(-20,32,140))]:
 light=bpy.data.lights.new(name,'SUN');light.energy=energy;light.angle=ang;o=bpy.data.objects.new(name,light);bpy.context.collection.objects.link(o);o.rotation_euler=tuple(math.radians(a) for a in rot)

scene.render.filepath='//appearance/front.png'
for text in list(bpy.data.texts):bpy.data.texts.remove(text)
bpy.ops.wm.save_as_mainfile(filepath=str(R/'appearance.blend'))
# Core 3MF base materials per original triangle: no geometry splitting/resampling.
ns='http://schemas.microsoft.com/3dmanufacturing/core/2015/02';ET.register_namespace('',ns)
e=lambda tag,attrs={}:ET.Element('{'+ns+'}'+tag,attrs)
root=e('model',{'unit':'millimeter','xml:lang':'en-US'});res=ET.SubElement(root,'{'+ns+'}resources');bm=ET.SubElement(res,'{'+ns+'}basematerials',{'id':'1'})
for name,col,_ in palette:ET.SubElement(bm,'{'+ns+'}base',{'name':name,'displaycolor':col+'FF'})
o=ET.SubElement(res,'{'+ns+'}object',{'id':'2','type':'model'});m=ET.SubElement(o,'{'+ns+'}mesh');vs=ET.SubElement(m,'{'+ns+'}vertices')
for v in verts:ET.SubElement(vs,'{'+ns+'}vertex',dict(zip(['x','y','z'],[format(c,'.17g') for c in v])))
ts=ET.SubElement(m,'{'+ns+'}triangles')
for f,i in zip(faces,indices):ET.SubElement(ts,'{'+ns+'}triangle',{'v1':str(f[0]),'v2':str(f[1]),'v3':str(f[2]),'pid':'1','p1':str(i),'p2':str(i),'p3':str(i)})
build=ET.SubElement(root,'{'+ns+'}build');ET.SubElement(build,'{'+ns+'}item',{'objectid':'2'})
with zipfile.ZipFile(R/'appearance.3mf','w',zipfile.ZIP_DEFLATED) as out:
 for n,b in {'3D/3dmodel.model':ET.tostring(root,encoding='utf-8',xml_declaration=True),'[Content_Types].xml':b'<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>','_rels/.rels':b'<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>'}.items():
  info=zipfile.ZipInfo(n,date_time=(2026,10,29,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;out.writestr(info,b)
from collections import Counter
(R/'appearance-materials.json').write_text(json.dumps({'revision':'color-v2-full-face-continuity','geometry':before,'palette':[{'name':n,'srgb':c,'roughness':r} for n,c,r in palette],'original_face_material_indices':original_indices,'changed_faces':changed_faces,'change_reasons':change_reasons,'window_supports':support_records,'face_counts':dict(Counter(indices)),'face_material_indices':indices,'limits':['Photographic approximation, not calibrated real finish values','Opaque mixed glazing backing only; true open courts, arch and upper frames remain open','School-history physical PDF18-19 printed162-163 are one cross-page exterior image, freshly viewed from the same verified locally cached official PDF; official entrance JPEG freshly downloaded and viewed. Existing front/right pale tile supports qualified continuity to complete rear, return, oblique and outer parapet wall faces, all original opening reveals, and original rear/return/oblique opaque mixed window backs. Those hidden or opposite extents are inferred, not directly photographed. Existing geometry and all precolored faces and RGBA/roughness are preserved. Original recess positions remain approximate. Roof fields, parapet inner and top faces, equipment, unpartitioned portico cuts, mixed-boundary faces and artificial base stay unchanged. Source photo dates unknown; no2026condition claim. Historical grey stairs preserved, newer red-orange multi-color stair artwork excluded because original faces have no matching boundaries. No face splits, new windows, letters, fine frames, tile joints, photos, or geometry changes','No actual trial print; original partial-model QA caveats remain']},indent=2))
# New images only; locked previews/front.png and original scene are never overwritten.
views={'front':((200,-250,150),(0,0,40),220),'rear':((-180,250,150),(0,0,40),220),'elevation':((0,-300,40),(0,0,40),220),'source-angle':((230,-200,180),(0,0,40),220),'left':((-320,0,135),(0,0,40),220),'right':((320,0,135),(0,0,40),220),'top':((0,0,400),(0,0,40),220)}
out=R/'appearance';out.mkdir(exist_ok=True);camera_records=[]
for name,(pos,target,scale) in ([] if '--skip-render' in sys.argv else views.items()):
 c=scene.camera;c.location=pos;c.rotation_euler=(Vector(target)-c.location).to_track_quat('-Z','Y').to_euler();c.data.ortho_scale=scale
 inv=c.rotation_euler.to_matrix().transposed();projected=[inv@(obj.matrix_world@Vector(corner)-c.location) for corner in obj.bound_box]
 width=max(v.x for v in projected)-min(v.x for v in projected);height=max(v.y for v in projected)-min(v.y for v in projected)
 c.data.ortho_scale=max(width,height*scene.render.resolution_x/scene.render.resolution_y)*1.18
 camera_records.append({'view':name,'location':list(c.location),'rotation_euler':list(c.rotation_euler),'ortho_scale':c.data.ortho_scale,'target':list(target)})
 scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
 data=(out/(name+'.png')).read_bytes(); cleaned=data[:8]; off=8
 while off<len(data):
  length=struct.unpack_from('>I',data,off)[0];typ=data[off+4:off+8];body=data[off+8:off+8+length];key=body.split(b'\0',1)[0]
  variable=typ in (b'tEXt',b'zTXt',b'iTXt') # no private path/date/timing metadata
  if not variable:cleaned+=data[off:off+length+12]
  off+=length+12
 (out/(name+'.png')).write_bytes(cleaned)
if camera_records:(R/'render-cameras.json').write_text(json.dumps(camera_records,indent=2))
print('APPEARANCE_DONE',before,dict(Counter(indices)))
