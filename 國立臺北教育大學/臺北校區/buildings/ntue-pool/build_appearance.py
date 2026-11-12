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
# Two local official PDF photographs support central entrance components only.
palette=[('Uncertified surfaces and mixed screens neutral', '#AAA79F', 0.86), ('Observed brick piers and right end plane', '#A96952', 0.88), ('Original true backing mixed glazing proxy', '#6E7D80', 0.7), ('Observed gray portal and planter front', '#858983', 0.88)]
def rgb(h):return tuple(int(h[i:i+2],16)/255 for i in (1,3,5))
def lin(v):return v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4
mesh.materials.clear()
for name,col,rough in palette:
 m=bpy.data.materials.new(name);m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=tuple(lin(v) for v in rgb(col))+(1,);bs.inputs['Roughness'].default_value=rough;m.diffuse_color=tuple(rgb(col))+(1,);mesh.materials.append(m)
import numpy as np
EPS=.003;indices=[];original_indices=[];changed_faces=[];change_reasons={}
def bounds(a,b):return bool(np.all(lo>=np.array(a)-EPS) and np.all(hi<=np.array(b)+EPS))
def plane(k,t):return max(abs(q[:,k]-t))<EPS
for p in mesh.polygons:
 q=np.array([verts[j] for j in p.vertices]);n=np.array(p.normal);lo=q.min(0);hi=q.max(0);i=0
 for x in [-35,-25,-15,-5,5,15,25,35,45,55]:
  if bounds((x-1.1,-12.5,3),(x+1.1,-7.5,34)) and abs(n[2])<.001 and (plane(1,-12.5) or plane(0,x-1.1) or plane(0,x+1.1)):i=1
 if plane(0,69) and n[0]>.999 and bounds((69,-10,2.8),(69,36,33.1)):i=1
 for c in [-30,-20,-10,0,10,20,30,40,50,60]:
  if plane(1,-7.25) and n[1]<-.999 and bounds((c-3.8,-7.25,7),(c+3.8,-7.25,30)):i=2
 if plane(0,67.1) and n[0]>.999:
  if any(bounds((67.1,y-w/2,z),(67.1,y+w/2,z+hh)) for y,w,z,hh in [(3,7,7,10),(15,7,7,10),(2,8,21,10),(19,20,21,10)]):i=2
 for x in [-62,-53,-44]:
  if plane(1,-26.75) and n[1]<-.999 and bounds((x-3.7,-26.75,4),(x+3.7,-26.75,20)):i=2
 for x in [-69,-37]:
  if bounds((x-1.7,-47.5,3),(x+1.7,-22.5,35)) and abs(n[2])<.001 and (plane(1,-47.5) or plane(0,x-1.7) or plane(0,x+1.7)):i=3
 if bounds((-70.7,-48.5,33.5),(-35.3,-21.5,36.5)) and ((plane(1,-48.5) and n[1]<-.999) or (abs(n[0])>.999 and (plane(0,-70.7) or plane(0,-35.3)))):i=3
 if plane(1,-14.5) and n[1]<-.999 and bounds((-37.5,-14.5,3),(69.5,-14.5,6.6)):i=3
 p.material_index=i;indices.append(i);original_indices.append(i)

# Extend only complete original component supports. The five screen bars,
# large incomplete side/rear facade proxies, and artificial ground stay neutral.
for p in mesh.polygons:
 if original_indices[p.index]!=0:continue
 q=np.array([verts[j] for j in p.vertices]);n=np.array(p.normal);lo=q.min(0);hi=q.max(0);i=0;reason=None
 # Full gray portal canopy: photo confirms soffit, other faces are continuous
 # concrete component inference; no wall face is captured by its support box.
 if bounds((-70.7,-48.5,33.5),(-35.3,-21.5,36.5)) and ((plane(2,33.5) and n[2]<-.999) or (plane(2,36.5) and n[2]>.999) or (plane(1,-21.5) and n[1]>.999)):
  i=3;reason='gray_portal_canopy_complete_soffit_top_rear'
 # Rear end caps of the two original side-wall solids. Their front and
 # lateral faces are already gray. Excludes adjoining rear connector rail.
 for x in [-69,-37]:
  if plane(1,-22.5) and n[1]>.999 and bounds((x-1.7,-22.5,3),(x+1.7,-22.5,33.5)):
   i=3;reason='gray_portal_sidewall_rear_caps'
 # Existing right-end shallow window reveals, all 3 vertices inside exactly
 # one original window prism and on its original jamb/head/sill plane.
 # No new opening or triangle subdivision; backing stays original bluegray.
 for y,w,z,hh in [(3,7,7,10),(15,7,7,10),(2,8,21,10),(19,20,21,10)]:
  if bounds((67.1,y-w/2,z),(69,y+w/2,z+hh)) and ((plane(1,y-w/2) and n[1]>.999) or (plane(1,y+w/2) and n[1]<-.999) or (plane(2,z) and n[2]>.999) or (plane(2,z+hh) and n[2]<-.999)):
   i=1;reason='brick_right_end_complete_window_reveal_inference'
 # One exposed right cap of the low continuous planter. Top and rear tray
 # proxy are not gray because soil/vegetation is not separately modeled.
 if plane(0,69.5) and n[0]>.999 and bounds((69.5,-14.5,3),(69.5,-11.5,6.6)):
  i=3;reason='gray_planter_right_end_cap'
 if reason:
  p.material_index=i;indices[p.index]=i;changed_faces.append(p.index);change_reasons[str(p.index)]={'family':reason,'basis':'Whole original support; hidden returns and exact material depth are explicitly inferred from adjacent same component, not directly surveyed.'}

assert before=={'vertices':digest([tuple(v.co) for v in mesh.vertices],'<3f'),'faces':digest([tuple(p.vertices) for p in mesh.polygons],'<3I')}
obj['appearance_policy']='Original geometry and colored faces preserved; complete portal and right window component returns inferred; mixed screens and incomplete broad facades neutral'
scene=bpy.context.scene;scene['appearance_revision']='color-v2-complete-component-returns'
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
(R/'appearance-materials.json').write_text(json.dumps({'revision':'color-v2-complete-component-returns','geometry':before,'palette':[{'name':n,'srgb':c,'roughness':r} for n,c,r in palette],'original_face_material_indices':original_indices,'changed_faces':changed_faces,'change_reasons':change_reasons,'face_counts':dict(Counter(indices)),'face_material_indices':indices,'limits':['Photographic approximation, not calibrated real finish values','Complete portal gray canopy soffit/top/rear and sidewall rear caps, right-end brick opening reveals, and planter right cap. Direct official front/right photos and visitor entrance photo support brick and gray component families; exact hidden returns are continuity inference. Architect describes greenwalls and opposite indoor photo shows extensive windows, so incomplete large rear/left facade proxies remain neutral instead of solid brick. Five original screen bars span incompatible red and dark systems and remain neutral; no splitting, added geometry, decals or equipment. Original colored faces and RGBA/roughness preserved. Capture dates unverified; not a 2026-condition survey','No actual trial print; original partial-model QA caveats remain']},indent=2))
# New images only; locked previews/front.png and original scene are never overwritten.
views={'front':((-220,-300,165),(0,0,20),190),'rear':((220,300,165),(0,0,20),190),'elevation':((0,-350,40),(0,0,20),190),'source-angle':((180,-300,110),(0,0,20),190),'left':((-320,0,150),(0,0,20),190),'right':((320,0,150),(0,0,20),190),'top':((0,0,380),(0,0,20),190)}
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
