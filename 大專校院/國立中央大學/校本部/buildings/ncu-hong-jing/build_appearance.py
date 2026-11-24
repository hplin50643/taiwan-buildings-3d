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
# Official university history PDF records repaint to pink in 2010. Pink is an uncalibrated visual approximation from its photos, not 2026 current survey.
palette=[('Unknown rear roof outer ends display base','#A7A9A5',.86),('Post-2010 photo approximate muted pink wall','#BA9E92',.85),('Dark grey green original lower glazing proxy','#536562',.5),('Pale grey green original clerestory mixed proxy','#A5AEA3',.65),('Grey entrance steps','#A2A19B',.85)]
def rgb(h):return tuple(int(h[i:i+2],16)/255 for i in (1,3,5))
def lin(v):return v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4
mesh.materials.clear()
for name,col,rough in palette:
 m=bpy.data.materials.new(name);m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=tuple(lin(v) for v in rgb(col))+(1,);bs.inputs['Roughness'].default_value=rough;m.diffuse_color=tuple(rgb(col))+(1,);mesh.materials.append(m)
indices=[]
def near(v,t,e=.035):return abs(v-t)<e
bays=[(-57,-17,61),(-40,-17,61),(-23,-17,61),(-7,-19,89),(13,-33.5,101),(30,-47.5,108),(48,-47.5,108)]
for p in mesh.polygons:
 x,y,z=p.center;n=p.normal;i=0
 # Existing stepped front wall planes only, not all sides of similarly-colored volumes.
 for lo,hi,front,top in [(-66,-16,-17,64.8),(-18,4,-19,93.8),(3,23,-33.5,105.8),(21,63,-47.5,111.8),(-9,23,-52.5,31.8)]:
  if lo-.01<x<hi+.01 and near(y,front,.015) and n.y<-.8 and 3<z<top+.01:i=1
 # Source-visible inset returns on original step in the facade.
 if near(x,3,.015) and n.x<-.8 and -33.51<y<-18.99 and 3<z<105.81:i=1
 if near(x,21,.015) and n.x<-.8 and -47.51<y<-33.49 and 3<z<111.81:i=1
 # Existing recess backs. Narrow upper slots include curtains/AC in photo: pale mixed proxy, no added equipment.
 for cx,front,h in bays:
  if abs(x-cx)<6.01 and near(y,front+1.5,.015) and n.y<-.8:
   for lo in range(9,h-6,15):
    if cx==13 and lo<33:continue
    if lo-.01<z<lo+7.01:i=2
    if lo+7.99<z<lo+10.41:i=3
 if near(x,4.5,.015) and n.x<-.8 and -31.01<y<-22.99 and any(lo-.01<z<lo+7.01 for lo in [38,53,68,83]):i=2
 if near(y,-51,.015) and n.y<-.8 and ((-1.51<x<15.51 and 3<z<15.01) or (-6.01<x<20.01 and 17.99<z<26.01)):i=2
 # Original small ventilation-slot backs only; not invented extra openings.
 if near(y,-18.5,.015) and n.y<-.8 and any(abs(x-xx)<1.51 for xx in [-11,-3]) and 84.99<z<87.41:i=3
 if near(y,-32.5,.015) and n.y<-.8 and any(abs(x-xx)<1.51 for xx in [10,17]) and 95.99<z<98.41:i=3
 if -8.01<x<22.01 and -55.851<y<-51.349 and 3<z<4.91 and (n.z>.8 or (n.y<-.8 and any(near(y,yy,.015) for yy in [-55.85,-54.45,-53.05])) or (abs(n.x)>.8 and any(near(x,xx,.015) for xx in [-8,22]))):i=4
 if z<=3 or (n.z>.8 and z>30):i=0
 p.material_index=i;indices.append(i)
# 2026-11-17 inferred pink wall continuity on complete original exterior wall planes.
# Whole triangle boundary tests; never paint window recesses, roofs or gallery floor.
wall_continuity_baseline=list(indices)
wall_planes=[(0, -66, [-66, -17, 3], [-66, 47, 64.8], 'low_0_0'), (0, -16, [-16, -17, 3], [-16, 47, 64.8], 'low_0_1'), (1, -17, [-66, -17, 3], [-16, -17, 64.8], 'low_1_0'), (1, 47, [-66, 47, 3], [-16, 47, 64.8], 'low_1_1'), (0, -18, [-18, -19, 3], [-18, 47, 93.8], 'mid_0_0'), (0, 4, [4, -19, 3], [4, 47, 93.8], 'mid_0_1'), (1, -19, [-18, -19, 3], [4, -19, 93.8], 'mid_1_0'), (1, 47, [-18, 47, 3], [4, 47, 93.8], 'mid_1_1'), (0, 3, [3, -33.5, 3], [3, 47.5, 105.8], 'high_0_0'), (0, 23, [23, -33.5, 3], [23, 47.5, 105.8], 'high_0_1'), (1, -33.5, [3, -33.5, 3], [23, -33.5, 105.8], 'high_1_0'), (1, 47.5, [3, 47.5, 3], [23, 47.5, 105.8], 'high_1_1'), (0, 21, [21, -47.5, 3], [21, 47.5, 111.8], 'right_0_0'), (0, 63, [63, -47.5, 3], [63, 47.5, 111.8], 'right_0_1'), (1, -47.5, [21, -47.5, 3], [63, -47.5, 111.8], 'right_1_0'), (1, 47.5, [21, 47.5, 3], [63, 47.5, 111.8], 'right_1_1'), (0, -9, [-9, -52.5, 3], [-9, -25.5, 31.8], 'entry_0_0'), (0, 23, [23, -52.5, 3], [23, -25.5, 31.8], 'entry_0_1'), (1, -52.5, [-9, -52.5, 3], [23, -52.5, 31.8], 'entry_1_0'), (1, -25.5, [-9, -25.5, 3], [23, -25.5, 31.8], 'entry_1_1')]
wall_groups={}
for axis,coordinate,lower,upper,label in wall_planes:
 selected=[]
 for p in mesh.polygons:
  vv=[mesh.vertices[k].co for k in p.vertices]
  if indices[p.index]==0 and all(abs(v[axis]-coordinate)<.0002 for v in vv) and all(lower[a]-.0002<=v[a]<=upper[a]+.0002 for v in vv for a in range(3)):
   selected.append(p.index)
   p.material_index=1;indices[p.index]=1
 wall_groups[label]=selected
assert wall_groups=={'low_0_0': [168, 169], 'low_0_1': [], 'low_1_0': [], 'low_1_1': [170, 171, 172], 'mid_0_0': [175, 176, 177, 179, 184, 187, 188, 189, 197, 198, 199, 200, 201, 206, 208, 209, 210, 211, 212, 213, 214, 215, 216, 221, 222, 223, 226, 227, 228, 231, 233, 238, 240, 241, 263, 264], 'mid_0_1': [], 'mid_1_0': [], 'mid_1_1': [261, 262, 267, 268], 'high_0_0': [382, 384, 386, 388], 'high_0_1': [], 'high_1_0': [], 'high_1_1': [385, 389, 390], 'right_0_0': [511, 569], 'right_0_1': [479, 572], 'right_1_0': [], 'right_1_1': [568, 570, 571, 574], 'entry_0_0': [581, 582], 'entry_0_1': [593, 596], 'entry_1_0': [], 'entry_1_1': [583, 584]}
wall_changed=sorted(set(sum(wall_groups.values(),[])))
assert before=={'vertices':digest([tuple(v.co) for v in mesh.vertices],'<3f'),'faces':digest([tuple(p.vertices) for p in mesh.polygons],'<3I')}
obj['appearance_policy']='Source-guided approximate sRGB; same exact vertices/triangles as original; rear walls inferred same post-2010 pink family; roofs remain neutral'
scene=bpy.context.scene;scene['appearance_revision']='color-v4-post2010-pink-inferred'
scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=32;scene.cycles.seed=0;scene.cycles.use_denoising=False
scene.render.threads_mode='FIXED';scene.render.threads=1
scene.render.resolution_x=900;scene.render.resolution_y=800
for attr in dir(scene.render):
 if attr.startswith('use_stamp'):
  try:setattr(scene.render,attr,False)
  except (TypeError,AttributeError):pass
scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.82,.85,.89,1);scene.world.node_tree.nodes['Background'].inputs[1].default_value=.65
scene.view_settings.view_transform='Standard';scene.view_settings.look='Medium High Contrast';scene.view_settings.exposure=0;scene.view_settings.gamma=1
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
(R/'appearance-materials.json').write_text(json.dumps({'revision':'color-v4-post2010-pink-inferred','wall_continuity_baseline_face_material_indices':wall_continuity_baseline,'wall_continuity_groups':wall_groups,'wall_continuity_changed_faces':wall_changed,'geometry':before,'palette':[{'name':n,'srgb':c,'roughness':r} for n,c,r in palette],'face_counts':dict(Counter(indices)),'face_material_indices':indices,'source_revision':{'url':'https://ncusec.ncu.edu.tw/no90/page2.pdf','basis':'2010 repaint history and accompanying post-repaint photos; publication/photo date not verified; not a 2026 survey','wall_srgb':'#BA9E92','method':'Visual approximate muted pink, not calibrated pixel colorimetry'},'limits':['Photographic approximation, not calibrated real finish values','Opaque glazing proxies, no real transparency or physical material certification','Exterior wall colors extended by material continuity inference, not verified by new side/rear imagery; roofs and window recesses unchanged','No actual trial print; original partial-model QA caveats remain']},indent=2))
# New images only; locked previews/front.png and original scene are never overwritten.
views={'front':((-195,-260,160),(0,0,55.9),210),'rear':((195,260,160),(0,0,55.9),210),'elevation':((0,-300,55.9),(0,0,55.9),210),'source-angle':((130,-300,70),(0,0,55.9),210),'top':((0,0,330),(0,0,0),210)}
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
