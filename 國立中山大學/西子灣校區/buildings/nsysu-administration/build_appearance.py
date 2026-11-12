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
# Four official admin-main-block photos; not adjacent red campus wings, dates unknown.
palette=[('Unknown sides rear roofs base','#A7AAA5',.86),('Muted brick red source-visible front wall','#9D6757',.86),('Pale grey beige original columns beams trim','#BBBBA9',.85),('Grey blue upper window proxies','#7D9596',.58),('Dark grey green lower window proxies','#414D49',.65),('Deep grey green entrance proxy','#293A34',.7),('Neutral grey original steps','#969B91',.86)]
def rgb(h):return tuple(int(h[i:i+2],16)/255 for i in (1,3,5))
def lin(v):return v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4
mesh.materials.clear()
for name,col,rough in palette:
 m=bpy.data.materials.new(name);m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=tuple(lin(v) for v in rgb(col))+(1,);bs.inputs['Roughness'].default_value=rough;m.diffuse_color=tuple(rgb(col))+(1,);mesh.materials.append(m)
indices=[];original_indices=[];changed_faces=[];change_reasons={}
def near(v,t,e=.035):return abs(v-t)<e
def boxed(p,x0,x1,y0,y1,z0,z1):
 return all(x0-.015<=mesh.vertices[v].co.x<=x1+.015 and y0-.015<=mesh.vertices[v].co.y<=y1+.015 and z0-.015<=mesh.vertices[v].co.z<=z1+.015 for v in p.vertices)
for p in mesh.polygons:
 x,y,z=p.center;nx,ny,nz=p.normal;i=0
 # Original front brick-backed main wall and upper box; unknown sides/rear left neutral.
 if near(y,-34.5,.015) and ny<-.8 and boxed(p,-59,59,-34.5,-34.5,2.8,64.2):i=1
 if near(y,-49.5,.015) and ny<-.8 and boxed(p,-65,65,-49.5,-49.5,65.4,88.4):i=1
 # Four actual24-facet columns, no arbitrary shadow staining or banners.
 for xx in [-54,-18,18,54]:
  if boxed(p,xx-2.05,xx+2.05,-46.05,-41.95,3,64):i=2
 for xx in [-42,-30,-6,6,30,42]:
  if boxed(p,xx-.675,xx+.675,-42.35,-39.65,29,63):i=2
 for zz in [27,39,51,62]:
  if boxed(p,-56.5,56.5,-45.5,-36.5,zz,zz+2.2):i=2
 # Existing projecting upper soffit slab; not broad roof or invented vertical piers.
 if boxed(p,-67,67,-51,59,63,65.6) and (nz<-.8 or (ny<-.8 and near(y,-51,.015))):i=2
 # Actual lower window backing planes, not portico depth or adjacent bays.
 for xx in [-44,-26,26,44]:
  for zz in [7,18,30,42,54]:
   if near(y,-33.3,.015) and ny<-.8 and boxed(p,xx-6.5,xx+6.5,-33.3,-33.3,zz,zz+7.3):i=4
 for xx in [-10,10]:
  for zz in [30,42,54]:
   if near(y,-33.3,.015) and ny<-.8 and boxed(p,xx-7,xx+7,-33.3,-33.3,zz,zz+7.3):i=4
 if near(y,-33.1,.015) and ny<-.8 and boxed(p,-15,15,-33.1,-33.1,3,24):i=5
 for xx in range(-58,59,12):
  if near(y,-48.2,.015) and ny<-.8 and boxed(p,xx-5.25,xx+5.25,-48.2,-48.2,67,74):i=3
  if boxed(p,xx-.5,xx+.5,-51,-49,67,74):i=2
 if near(y,-46.5,.015) and ny<-.8 and boxed(p,-17,17,-46.5,-46.5,78,84.7):i=4
 for xx in [-60,60]:
  if near(y,-48.4,.015) and ny<-.8 and boxed(p,xx-3.25,xx+3.25,-48.4,-48.4,78,81.8):i=3
 # Existing balcony base slab and narrow top face pale; original curved fascia red, not added text/rail.
 if boxed(p,-18,18,-52,-38,29,31.4):i=2
 if near(z,35.4,.015) and nz>.8 and boxed(p,-18,18,-52,-38,35.4,35.4):i=2
 if abs(nz)<.01 and ny<0 and boxed(p,-18,18,-52,-38,29,35.4):
  for k in range(48):
   aa=math.pi-k*math.pi/48;bb=math.pi-(k+1)*math.pi/48
   ax,ay=18*math.cos(aa),-38-14*math.sin(aa);bx,by=18*math.cos(bb),-38-14*math.sin(bb)
   dx,dy=bx-ax,by-ay;ll=math.hypot(dx,dy)
   if all(abs((mesh.vertices[v].co.x-ax)*dy-(mesh.vertices[v].co.y-ay)*dx)/ll<.015 for v in p.vertices):i=1
 for k in range(4):
  if boxed(p,-39,39,-58.3+2*k,-55.7+2*k,2.8,3.4+.8*k):i=6
 if z<=3:i=0
 original_indices.append(i);reason=None
 # V2 only extends materials over complete original triangles and their known
 # construction supports. Never cut color by a triangle centroid or rebuild mesh.
 q=[mesh.vertices[v].co for v in p.vertices]
 def plane(axis,value):return all(abs(v[axis]-value)<.015 for v in q)
 if i==0 and max(v.z for v in q)>3.001:
  # Continuous original pale soffit slab: vertical perimeter only, not its roof.
  if boxed(p,-67,67,-51,59,63,65.6) and abs(nz)<.01 and (plane(0,-67) or plane(0,67) or plane(1,59)):
   i=2;reason='inferred_pale_existing_soffit_slab_vertical_perimeter'
  # The original front upper box already uses a dominant brick-wall proxy,
  # omitting thin pale surface bands not represented in the mesh. Continue the
  # SAME proxy on whole side/rear support planes, not a height-cut triangle set.
  # Side/rear window reveals are independently bounded original cut surfaces.
  if i==0 and boxed(p,-65,65,-49.75,57.75,65.6,90.4) and abs(nz)<.01:
   if plane(0,-65) or plane(0,65) or plane(1,57.5) or plane(1,57.75) or plane(1,-49.75):
    i=1;reason='dominant_brick_proxy_existing_upper_box_complete_outer_support'
  # Original side upper window back and four shallow reveals. The side window
  # family is inferred; no new windows, strips, glass overlays or frames.
  for side in [-1,1]:
   lo,hi=sorted([side*63.5,side*65])
   for yy in [-36,-20,-4,12,28,44]:
    if i==0 and boxed(p,lo,hi,yy-6,yy+6,67,74):
     if plane(0,side*63.5):i=3;reason='inferred_existing_upper_side_window_opaque_back'
     else:i=2;reason='inferred_existing_upper_side_window_pale_reveals'
  # 2024 actual rear supports pale upper window family; exact window positions
  # remain original simplified geometry, not a reconstruction from this photo.
  for xx in range(-54,55,18):
   if i==0 and boxed(p,xx-7,xx+7,56.1,57.5,68,75):
    if plane(1,56.1):i=3;reason='source_supported_existing_upper_rear_window_opaque_back'
    else:i=2;reason='source_supported_existing_upper_rear_window_pale_reveals'
  # Existing lower rear aperture backs and brick reveals, consistent with the
  # official rear-ramp photo and local 2024 rear view. Full wall stays neutral:
  # actual pale columns cross its unsupported original large coplanar surface.
  for xx in [-48,-30,-12,12,30,48]:
   for zz in [10,23,36,49]:
    if i==0 and boxed(p,xx-6,xx+6,51.15,52.5,zz,zz+7):
     if plane(1,51.15):i=4;reason='inferred_existing_lower_rear_window_opaque_back'
     else:i=1;reason='source_supported_brick_existing_lower_rear_window_reveals'
  # Existing front lower openings: direct detailed photo supports brick returns.
  front_openings=[(xx,zz,6.5) for xx in [-44,-26,26,44] for zz in [7,18,30,42,54]]+[(xx,zz,7) for xx in [-10,10] for zz in [30,42,54]]
  for xx,zz,half in front_openings:
   if i==0 and boxed(p,xx-half,xx+half,-34.5,-33.3,zz,zz+7.3) and not plane(1,-33.3):
    i=1;reason='source_supported_brick_existing_front_lower_window_reveals'
  if i==0 and boxed(p,-15,15,-34.5,-33.1,3,24) and not plane(1,-33.1):
   i=1;reason='source_supported_brick_existing_front_door_reveals'
  # Existing upper front window reveals follow the pale frame family already
  # assigned to its mullions, without inventing missing bands on the broad wall.
  for xx in range(-58,59,12):
   if i==0 and boxed(p,xx-5.25,xx+5.25,-49.5,-48.2,67,74) and not plane(1,-48.2):
    i=2;reason='source_supported_pale_existing_front_upper_window_reveals'
 if i!=original_indices[-1]:changed_faces.append(p.index);change_reasons[str(p.index)]=reason
 p.material_index=i;indices.append(i)
assert before=={'vertices':digest([tuple(v.co) for v in mesh.vertices],'<3f'),'faces':digest([tuple(p.vertices) for p in mesh.polygons],'<3I')}
obj['appearance_policy']='Original geometry and colors preserved; complete original window/soffit supports extended, mixed surfaces and artificial cuts neutral'
scene=bpy.context.scene;scene['appearance_revision']='color-v2-side-rear-continuity'
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
(R/'appearance-materials.json').write_text(json.dumps({'revision':'color-v2-side-rear-continuity','geometry':before,'palette':[{'name':n,'srgb':c,'roughness':r} for n,c,r in palette],'changed_faces':changed_faces,'change_reasons':change_reasons,'original_face_material_indices':original_indices,'face_counts':dict(Counter(indices)),'face_material_indices':indices,'limits':['Photographic approximation, not calibrated real finish values','Opaque glazing proxies, no real transparency or physical material certification','Existing window backs and returns plus soffit perimeter extended using same-family materials. Original upper-box dominant brick proxy extended on complete side/rear outer support planes; fine pale surface bands absent from mesh remain omitted consistently. Lower rear broad walls have substantial pale columns without matching model boundaries and stay neutral. Artificial side joins, roof, lightwell and stair volumes stay neutral. No new windows or details.','No actual trial print; original partial-model QA caveats remain']},indent=2))
# New images only; locked previews/front.png and original scene are never overwritten.
views={'front':((-195,-280,165),(0,0,46.5),220),'rear':((195,280,165),(0,0,46.5),220),'elevation':((0,-330,46.5),(0,0,46.5),220),'source-angle':((-150,-270,85),(0,0,46.5),220),'left':((-330,0,150),(0,0,46.5),220),'right':((330,0,150),(0,0,46.5),220),'top':((0,0,350),(0,0,0),220)}
out=R/'appearance';out.mkdir(exist_ok=True)
for name,(pos,target,scale) in ([] if '--skip-render' in sys.argv else views.items()):
 c=scene.camera;c.location=pos;c.rotation_euler=(Vector(target)-c.location).to_track_quat('-Z','Y').to_euler();c.data.ortho_scale=scale
 inv=c.rotation_euler.to_matrix().transposed();projected=[inv@(obj.matrix_world@Vector(corner)-c.location) for corner in obj.bound_box]
 width=max(v.x for v in projected)-min(v.x for v in projected);height=max(v.y for v in projected)-min(v.y for v in projected)
 c.data.ortho_scale=max(width,height*scene.render.resolution_x/scene.render.resolution_y)*1.18
 scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
 data=(out/(name+'.png')).read_bytes(); cleaned=data[:8]; off=8
 while off<len(data):
  length=struct.unpack_from('>I',data,off)[0];typ=data[off+4:off+8];body=data[off+8:off+8+length];key=body.split(b'\0',1)[0]
  variable=typ in (b'tEXt',b'zTXt',b'iTXt') # no private path/date/timing metadata
  if not variable:cleaned+=data[off:off+length+12]
  off+=length+12
 (out/(name+'.png')).write_bytes(cleaned)
print('APPEARANCE_DONE',before,dict(Counter(indices)))
