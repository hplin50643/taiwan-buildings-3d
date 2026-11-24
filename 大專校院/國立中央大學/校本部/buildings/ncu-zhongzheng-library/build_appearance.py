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
# Undated real official fundraising photographs, not a renovation-completion claim.
palette=[('Unknown roof court infill and display base','#A7AAA4',.86),('Warm white colonnade and front screen webs','#D1CFC0',.84),('Muted grey green coarse screen recess proxy','#66716A',.75),('Grey concrete entrance steps','#A1A29C',.86)]
def rgb(h):return tuple(int(h[i:i+2],16)/255 for i in (1,3,5))
def lin(v):return v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4
mesh.materials.clear()
for name,col,rough in palette:
 m=bpy.data.materials.new(name);m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=tuple(lin(v) for v in rgb(col))+(1,);bs.inputs['Roughness'].default_value=rough;m.diffuse_color=tuple(rgb(col))+(1,);mesh.materials.append(m)
indices=[]
original_indices=[]
changed_faces=[]
change_reasons={}

def plane_support(p,axis,value,other_bounds,normal_sign):
 vs=[mesh.vertices[v].co for v in p.vertices]
 return p.normal[axis]*normal_sign>.999 and all(abs(v[axis]-value)<.002 and all(lo-.002<=v[j]<=hi+.002 for j,(lo,hi) in other_bounds.items()) for v in vs)
def near(v,t,e=.035):return abs(v-t)<e
for p in mesh.polygons:
 x,y,z=p.center;n=p.normal;i=0
 # Source-visible front pale wall and coarse screen reveals, not an arbitrary green wall.
 if -57.51<x<57.51 and -50.01<y<-49.34 and 3<z<36.01:i=1
 if near(y,-49.35,.012) and n.y<-.8 and 6.99<z<36.51:i=2
 # Same observed pale material family on existing surrounding colonnade piers.
 if 3<z<38.01:
  if 52.99<abs(y)<61.01 and any(abs(x-c)<.91 for c in range(-55,56,11)):i=1
  if 60.09<abs(x)<61.91 and any(abs(y-c)<.91 for c in range(-48,49,12)):i=1
 # Outer high fascia/canopy rims only, inner-court faces stay unknown neutral.
 if 35.99<z<42.01:
  if (near(abs(y),58,.015) and n.y*y>0) or (near(abs(x),62,.015) and n.x*x>0):i=1
  if (near(abs(y),59.5,.015) and n.y*y>0) or (near(abs(x),63.5,.015) and n.x*x>0):i=1
 # Existing featureless clock disc remains pale; no fabricated dial marks.
 if y<-59.99 and math.hypot(x,z-39.8)<2.11:i=1
 if abs(x)<37.51 and y<-60.01 and 3<z<5.61:i=3
 # Horizontal roof/court/base and uncertain interiors cannot inherit a facade color.
 if z<=3 or (z>=39.99 and n.z>.8):i=0
 original_indices.append(i);reason=None
 if i==0:
  # Existing side/rear inset infill: complete original supporting facets only.
  # Grey-green comes from the same-building official photograph, direction inferred.
  for axis,value,bounds,sign,label in [(0,54.5,{1:(-50,50),2:(3,36)},1,'right_inset_infill'),(1,50,{0:(-54.5,54.5),2:(3,36)},1,'rear_inset_infill')]:
   if plane_support(p,axis,value,bounds,sign):i=2;reason='inferred_complete_'+label
  # Exact solid outer corner walls and original fascia planes share pale colonnade.
  for axis,value,bounds,sign,label in [(0,-62,{1:(-58,58),2:(3,40)},-1,'left_corner_and_fascia'),(0,62,{1:(-58,58),2:(3,40)},1,'right_corner_and_fascia'),(1,-58,{0:(-62,62),2:(3,40)},-1,'front_corner_and_fascia'),(1,58,{0:(-62,62),2:(3,40)},1,'rear_corner_and_fascia')]:
   if plane_support(p,axis,value,bounds,sign):i=1;reason='inferred_complete_'+label
  # Short end reveals of the original external colonnade cutouts, no mixed facade cutting.
  for axis,value,bounds,sign,label in [(0,-57.5,{1:(-58,58),2:(3,36)},1,'left_end_reveal'),(0,57.5,{1:(-58,58),2:(3,36)},-1,'right_end_reveal'),(1,-52,{0:(-62,62),2:(3,36)},1,'front_end_reveal'),(1,52,{0:(-62,62),2:(3,36)},-1,'rear_end_reveal')]:
   if plane_support(p,axis,value,bounds,sign):i=1;reason='inferred_complete_'+label
 if i!=original_indices[-1]:changed_faces.append(p.index);change_reasons[str(p.index)]=reason
 p.material_index=i;indices.append(i)
# Complete original outer-colonnade ceiling, not front-only triangle clipping.
soffit_ids=[337, 338, 339, 340, 341, 342, 343, 344, 346, 347, 348, 349, 351, 352, 353, 354, 390, 391, 392, 395, 396, 397, 398, 399, 400, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 415, 416, 417, 418, 419, 421, 422, 424, 425, 426, 427, 539, 540, 541, 542, 545, 546, 547, 548, 549, 550, 551, 553, 554, 555, 556, 557, 559, 560, 561, 562, 563, 566, 567, 568, 569, 570, 586, 587, 588, 591, 592, 593, 594, 595, 597, 598, 600, 601, 602, 603, 604, 605, 845, 846, 847, 848, 849, 850, 851, 852, 853, 854, 855, 857, 858, 859, 860, 861, 862, 863, 864, 865, 866, 900, 901, 902, 903, 904, 905, 906, 907, 908, 909, 910, 911, 912, 913, 914, 915, 916, 917, 919, 920, 921, 922, 923, 924, 925, 926, 927, 928, 929, 930, 1162, 1163, 1164, 1165, 1166, 1167, 1168, 1169, 1170, 1171, 1172, 1173, 1174, 1175, 1176, 1178, 1179, 1180, 1181, 1182, 1183, 1184, 1185, 1186, 1187, 1188, 1189, 1190, 1191, 1192, 1219, 1220, 1221, 1222, 1223, 1224, 1225, 1226, 1227, 1228, 1229, 1230, 1231, 1232, 1233, 1234, 1235, 1236, 1237, 1238, 1239, 1240, 1242, 1243, 1244, 1245, 1246, 1247, 1248, 1249, 1250, 1251, 1252, 1253, 1357, 1358, 1359, 1360, 1361, 1362, 1363, 1364, 1365, 1366, 1367, 1368, 1369, 1370, 1371, 1372, 1373, 1374, 1375, 1376, 1377, 1378, 1379, 1380, 1381, 1382, 1383, 1384, 1385, 1386, 1387, 1388, 1389, 1390, 1391, 1392, 1393, 1430, 1431, 1432, 1433, 1434, 1435, 1436, 1437, 1438, 1439, 1440, 1441, 1442, 1443, 1445, 1446, 1447, 1448, 1449, 1450, 1451, 1452, 1453]
assert all(indices[i]==0 for i in soffit_ids)
for i in soffit_ids:
 p=mesh.polygons[i]
 assert p.normal.z < -.999
 for vi in p.vertices:
  a=mesh.vertices[vi].co
  assert abs(a.z-36)<.002 and -62.002<=a.x<=62.002 and -58.002<=a.y<=58.002
  assert abs(a.x)>=54.498 or abs(a.y)>=49.998
 p.material_index=1;indices[i]=1
assert before=={'vertices':digest([tuple(v.co) for v in mesh.vertices],'<3f'),'faces':digest([tuple(p.vertices) for p in mesh.polygons],'<3I')}
obj['appearance_policy']='Source-guided approximate sRGB; same exact vertices/triangles as original; complete right/rear inset walls use inferred existing grey-green; left mixed wall unchanged; corner/fascia/reveal planes inferred warm white; roof/court/base and mixed surfaces remain neutral'
scene=bpy.context.scene;scene['appearance_revision']='color-v3-colonnade-soffit'
scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=96;scene.cycles.seed=0;scene.cycles.use_denoising=False
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
(R/'appearance-materials.json').write_text(json.dumps({'revision':'color-v3-colonnade-soffit','geometry':before,'palette':[{'name':n,'srgb':c,'roughness':r} for n,c,r in palette],'prior_v2_changed_faces':changed_faces,'soffit_changed_faces':soffit_ids,'change_reasons':change_reasons,'original_face_material_indices':original_indices,'face_counts':dict(Counter(indices)),'face_material_indices':indices,'limits':['Photographic approximation, not calibrated real finish values','Opaque glazing proxies, no real transparency or physical material certification','Complete right/rear inset infill inferred grey-green; mixed left plane remains original from same-building photograph; orientation and window layout not verified. Roof/court/base and ambiguous mixed surfaces neutral. Coarse screen recess remains an opaque proxy, not certified glazing.','No actual trial print; original partial-model QA caveats remain']},indent=2))
# New images only; locked previews/front.png and original scene are never overwritten.
views={'front':((-195,-220,155),(0,0,21),190),'rear':((195,230,160),(0,0,21),190),'elevation':((0,-260,21),(0,0,21),190),'source-angle':((-210,-260,60),(0,0,21),190),'left':((-280,0,120),(0,0,21),190),'right':((280,0,120),(0,0,21),190),'top':((0,0,300),(0,0,0),190)}
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
