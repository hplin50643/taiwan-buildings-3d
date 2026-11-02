from pathlib import Path
import bpy,numpy as np,json,math,hashlib,sys
from mathutils import Vector
R=Path(__file__).resolve().parent
ONLY_VIEW=next((x.split('=',1)[1] for x in sys.argv if x.startswith('--only-view=')),None)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
d=np.load(R/'mesh.npz');v=d['vertices'];f=d['faces'];mi=d['materials'];pal=json.loads((R/'palette.json').read_text())
m=bpy.data.meshes.new('validated_printable_mesh');m.from_pydata(v.tolist(),[],f.tolist());m.update();o=bpy.data.objects.new('NCKU Wei-Nong historical design quality upgrade',m);bpy.context.collection.objects.link(o)
o['source_mesh_sha256']=hashlib.sha256((R/'mesh.npz').read_bytes()).hexdigest();o['scale']='1:350';o['scope']='Wei-Nong historical exterior quality upgrade; not present survey'
for name,col in pal:
 mat=bpy.data.materials.new(name);rgb=tuple(int(col[i:i+2],16)/255 for i in (1,3,5));mat.diffuse_color=(*rgb,1);mat.use_nodes=True;bs=mat.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*rgb,1);bs.inputs['Roughness'].default_value=.72;m.materials.append(mat)
for p,k in zip(m.polygons,mi):p.material_index=int(k)
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=48;scene.cycles.use_denoising=False;scene.render.resolution_x=1200;scene.render.resolution_y=900;scene.render.resolution_percentage=100
scene.world.color=(.7,.7,.7);scene.view_settings.view_transform='Standard';scene.view_settings.look='Medium High Contrast'
for loc,power,size in [((100,-180,400),500000,250),((-220,120,240),350000,180),((0,350,200),350000,250),((300,-80,220),250000,180),((-80,-120,45),60000,75)]:
 bpy.ops.object.light_add(type='AREA',location=loc);l=bpy.context.object;l.data.energy=power;l.data.shape='DISK';l.data.size=size
 l.rotation_euler=(Vector((0,0,45))-l.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add();cam=bpy.context.object;scene.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=370
views={'preview':(-220,-330,230),'rear':(220,330,230),'front':(0,-550,25),'back':(0,550,25),'west':(-550,0,25),'east':(550,0,25),'top':(0,0,550)}
# In-render notice is part of the scene, NOT architectural/print geometry.
bpy.ops.object.text_add();caption=bpy.context.object;caption.name='HISTORICAL_SCHEME_NOTICE_NOT_PRINT_GEOMETRY';caption.parent=cam
fontpath=Path('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')
if fontpath.exists():
 caption.data.font=bpy.data.fonts.load(str(fontpath));caption.data.body='成大唯農大樓｜同項目品質更新\n1981時期歷史圖示；非現況測繪\n局部基準差5cm；未實際列印'
else:caption.data.body='NCKU WEI-NONG HISTORICAL EXTERIOR\nSame-item quality update / unprinted'
caption.data.align_x='LEFT';caption.data.space_line=1.0
cm=bpy.data.materials.new('caption emission');cm.use_nodes=True;cm.node_tree.nodes.clear();em=cm.node_tree.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(.95,.95,.95,1);out=cm.node_tree.nodes.new('ShaderNodeOutputMaterial');cm.node_tree.links.new(em.outputs[0],out.inputs['Surface']);caption.data.materials.append(cm)
if hasattr(caption,'visible_shadow'):caption.visible_shadow=False
# Camera-space notice backing is NOT architectural/print geometry.
bm=bpy.data.meshes.new('notice_backing');bm.from_pydata([(-.5,-.5,0),(.5,-.5,0),(.5,.5,0),(-.5,.5,0)],[],[(0,1,2,3)])
backing=bpy.data.objects.new('NOTICE_BACKDROP_NOT_PRINT_GEOMETRY',bm);bpy.context.collection.objects.link(backing);backing.parent=cam
bgmat=bpy.data.materials.new('notice_backdrop_emission');bgmat.use_nodes=True;bgmat.node_tree.nodes.clear();be=bgmat.node_tree.nodes.new('ShaderNodeEmission');be.inputs['Color'].default_value=(.035,.035,.035,1);bo=bgmat.node_tree.nodes.new('ShaderNodeOutputMaterial');bgmat.node_tree.links.new(be.outputs[0],bo.inputs['Surface']);bm.materials.append(bgmat)
if hasattr(backing,'visible_shadow'):backing.visible_shadow=False

def update_caption():
 sc=cam.data.ortho_scale;caption.location=(-.45*sc,-.29*sc,-10);caption.rotation_euler=(0,0,0);caption.data.size=.026*sc
 backing.location=(-.355*sc,-.322*sc,-10.1);backing.scale=(.23*sc,.090*sc,1);backing.rotation_euler=(0,0,0)
from bpy_extras.object_utils import world_to_camera_view
framing={}
for name,loc in views.items():
 if ONLY_VIEW and name!=ONLY_VIEW:continue
 cam.location=loc;target=Vector((0,0,25));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=175 if name in ['west','east'] else 340
 bpy.context.view_layer.update()
 for _ in range(20):
  pts=[world_to_camera_view(scene,cam,Vector(x)) for x in v];bounds=[min(p.x for p in pts),max(p.x for p in pts),min(p.y for p in pts),max(p.y for p in pts)]
  if bounds[0]>.03 and bounds[1]<.97 and bounds[2]>.14 and bounds[3]<.97:break
  cam.data.ortho_scale*=1.08;bpy.context.view_layer.update()
 assert bounds[0]>.03 and bounds[1]<.97 and bounds[2]>.14 and bounds[3]<.97,(name,bounds)
 update_caption();framing[name]=bounds;scene.render.filepath=str(R/(name+'.png'));bpy.ops.render.render(write_still=True)
if framing:
 prior=R/'FRAMING-QA.json'
 if ONLY_VIEW and prior.exists():
  old=json.loads(prior.read_text())
  if old.get('mesh_sha256')==o['source_mesh_sha256']:framing={**old['projected_vertex_bounds'],**framing}
 prior.write_text(json.dumps({'status':'PASS','mesh_sha256':o['source_mesh_sha256'],'projected_vertex_bounds':framing},indent=2))

# Two deliberately cropped detail views, not full-model framing claims.
for name,loc,target,ortho in [('entry-detail',(130,-170,100),(53,-38,17),95),('courtyard-detail',(15,-140,210),(0,0,22),140),('roof-detail',(-100,130,230),(-20,15,35),160)]:
 if ONLY_VIEW and name!=ONLY_VIEW:continue
 cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=ortho;update_caption();scene.render.filepath=str(R/(name+'.png'));bpy.ops.render.render(write_still=True)
cam.location=views['preview'];cam.rotation_euler=(Vector((0,0,25))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=340
update_caption()
bpy.ops.wm.save_as_mainfile(filepath=str(R/'scene.blend'),compress=True)
