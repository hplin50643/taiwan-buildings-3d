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
# Official 2023 front photo and official disaster-plan page49 side photo support wall/window continuity; full opposite side and rear service walls are inferred; roof and upper block surfaces remain neutral.
palette=[('Unobserved surfaces neutral','#AAA79F',.86),('Observed front washed-stone grey beige','#A8A79B',.86),('Opaque mixed original front window and entry backs','#526773',.65),('Opaque mixed original entry backing','#48514E',.7),('Original coarse window bars pale','#C8CBC3',.8),('Observed canopy underside pale','#C2C1B3',.86)]
def rgb(h):return tuple(int(h[i:i+2],16)/255 for i in (1,3,5))
def lin(v):return v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4
mesh.materials.clear()
for name,col,rough in palette:
 m=bpy.data.materials.new(name);m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=tuple(lin(v) for v in rgb(col))+(1,);bs.inputs['Roughness'].default_value=rough;m.diffuse_color=tuple(rgb(col))+(1,);mesh.materials.append(m)
import numpy as np
EPS=.003;indices=[];original_indices=[];changed_faces=[];change_categories={}
def bounds(a,b):return bool(np.all(lo>=np.array(a)-EPS) and np.all(hi<=np.array(b)+EPS))
def plane(k,t):return max(abs(q[:,k]-t))<EPS
def front(x,y,z,w,h):return plane(1,y) and n[1]<-.999 and bounds((x-w/2,y,z),(x+w/2,y,z+h))
for p in mesh.polygons:
 q=np.array([verts[j] for j in p.vertices]);n=np.array(p.normal);lo=q.min(0);hi=q.max(0);i=0
 # Observed frontal wall planes only, not unseen long elevations or roof.
 if (front(0,-66,2.8,66,40) and (hi[0]<=-15+EPS or lo[0]>=15-EPS)) or front(0,-71,2.8,30,42):i=1
 # Actual recessed window/entry backs. Opaque mixed appearance, no invented detail.
 for x in [-9,0,9]:
  if front(x,-69.4,19,7,16):i=2
  for z in [23,28,32]:
   if front(x,-72.45,z,7,1.1):i=4
 if front(0,-68.5,4,26,10):i=3
 for x in [-26,26]:
  if front(x,-64.5,6,10,7) or front(x,-64.5,22,10,13):i=2
  for z in [26,30]:
   if front(x,-67.35,z,10,1.1):i=4
  if front(x,-68.5,17,12,1.3):i=1
 if front(0,-74.05,15,35,1.8):i=1
 if plane(2,15) and n[2]<-.999 and bounds((-17.5,-74.05,15),(17.5,-67.55,15)):i=5
 original_indices.append(i);category=None
 # V2 only reassigns neutral original triangles, never changes the palette or mesh.
 if i==0:
  for side in [-1,1]:
   # Long wall planes and exposed faces of existing projecting structural piers.
   if plane(0,side*33) and n[0]*side>.999 and bounds((-34.31,-66,3),(34.31,66,42.3)):
    i=1;category='long_side_wall_continuity'
   for cy in [-52,-30,-8,14,36,58]:
    if bounds((min(side*33,side*34.3),cy-1.7,3),(max(side*33,side*34.3),cy+1.7,42.3)) and abs(n[2])<.001:
     i=1;category='side_structural_pier_continuity'
   # Existing high-window backs and their stone opening returns; no pane subdivision.
   for cy in [-41,-19,3,25,47]:
    if bounds((min(side*31.35,side*33),cy-6,20),(max(side*31.35,side*33),cy+6,35)):
     i=1;category='side_window_stone_returns'
     if plane(0,side*31.35) and n[0]*side>.999:i=2;category='existing_side_window_back_proxy'
    # Existing coarse horizontal bars, including exposed returns.
    for zz in [24,29]:
     if bounds((min(side*32.1,side*34.7),cy-6,zz),(max(side*32.1,side*34.7),cy+6,zz+1.1)):
      i=4;category='existing_side_window_coarse_bars'
   # Existing side doorway only. Actual photographed doorway is partly occluded;
   # dark backing is an explicit continuity inference, not a material survey.
   if bounds((min(side*31.5,side*33),4.5,3),(max(side*31.5,side*33),15.5,12)):
    i=1;category='side_entry_stone_returns'
    if plane(0,side*31.5) and n[0]*side>.999:i=3;category='existing_side_entry_back_proxy'
   # Only vertical outer side canopy fascia; broad unobserved top remains neutral.
   if bounds((min(side*33,side*40),1,13),(max(side*33,side*40),19,14.7)) and abs(n[2])<.001:
    i=1;category='side_canopy_fascia_continuity'
  # Complete hall rear and low service block are genuine external walls, not cuts.
  # Same washed-stone family is a continuity inference without a rear photograph.
  if plane(1,66) and n[1]>.999 and bounds((-33,66,19.8),(33,66,42.3)):
   i=1;category='rear_main_wall_inferred_continuity'
  if abs(n[2])<.001 and bounds((-35,60,3),(35,68,19.8)):
   i=1;category='rear_service_wall_inferred_continuity'
  # Short entrance-front wall returns, not roof or supporting base.
  if plane(0,15) or plane(0,-15):
   if bounds((-15,-71,3),(15,-63,44.8)) and abs(n[0])>.999:i=1;category='front_projecting_wall_returns'
  # Recess stone returns and original coarse frame returns already present in geometry.
  for xx in [-9,0,9]:
   if bounds((xx-3.5,-71,19),(xx+3.5,-69.4,35)):
    i=1;category='front_window_stone_returns'
   for zz in [23,28,32]:
    if bounds((xx-3.5,-72.45,zz),(xx+3.5,-71,zz+1.1)):
     i=4;category='front_window_coarse_bar_returns'
  for xx in [-26,26]:
   for zz,hh in [(6,7),(22,13)]:
    if bounds((xx-5,-66,zz),(xx+5,-64.5,zz+hh)):
     i=1;category='front_side_window_stone_returns'
   for zz in [26,30]:
    if bounds((xx-5,-67.35,zz),(xx+5,-66,zz+1.1)):
     i=4;category='front_side_window_coarse_bar_returns'
   if bounds((xx-6,-68.5,17),(xx+6,-66,18.3)) and abs(n[2])<.001:
    i=1;category='front_sill_fascia_returns'
  if bounds((-13,-71,4),(13,-68.5,14)) and abs(n[1])<.001:
   i=1;category='front_entry_stone_returns'
  if bounds((-17.5,-74.05,15),(17.5,-67.55,16.8)) and abs(n[0])>.999:
   i=1;category='front_canopy_end_fascia'
 if i!=original_indices[-1]:
  changed_faces.append(p.index);change_categories[str(p.index)]=category
 p.material_index=i;indices.append(i)

assert before=={'vertices':digest([tuple(v.co) for v in mesh.vertices],'<3f'),'faces':digest([tuple(p.vertices) for p in mesh.polygons],'<3I')}
obj['appearance_policy']='Source-guided approximate sRGB; same exact vertices/triangles as original; unknown or unresolved surfaces neutral'
scene=bpy.context.scene;scene['appearance_revision']='color-v2-side-continuity'
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
(R/'appearance-materials.json').write_text(json.dumps({'revision':'color-v2-side-continuity','geometry':before,'palette':[{'name':n,'srgb':c,'roughness':r} for n,c,r in palette],'changed_faces':changed_faces,'change_categories':change_categories,'original_face_material_indices':original_indices,'face_counts':dict(Counter(indices)),'face_material_indices':indices,'limits':['Photographic approximation, not calibrated real finish values','Original hall geometry and approximate roof retained, no facade detail added','Official NCCU 2023 front photograph and official disaster-plan page49 side photograph inspected. Grey beige long side walls and existing deep pier faces use original wall family; existing high-window backs and coarse bars use original opaque dark and pale materials. Opposite side continuity is an explicit inference, not a measured match. Rear main and stage/service external walls use inferred stone continuity without adding rear windows. Roof, service-block top, broad canopy tops, steps and base remain neutral. Original geometry and all previously colored faces/material RGBA/roughness preserved. No added panes, text, posters or structures','No actual trial print; original partial-model QA caveats remain']},indent=2))
# New images only; locked previews/front.png and original scene are never overwritten.
views={'front':((-170,-290,145),(0,0,23),205),'rear':((170,290,145),(0,0,23),205),'elevation':((0,-350,23),(0,0,23),205),'source-angle':((0,-300,90),(0,0,23),205),'left':((-300,0,130),(0,0,23),205),'right':((300,0,130),(0,0,23),205),'top':((0,0,380),(0,0,23),205)}
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
