import bpy,json,sys,math,hashlib
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parent
OUT=Path(sys.argv[sys.argv.index('--')+1])if'--'in sys.argv else ROOT
OUT.mkdir(exist_ok=True,parents=True);(OUT/'previews').mkdir(exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=.001
s.render.engine='CYCLES';s.cycles.samples=32;s.cycles.use_denoising=False;s.render.resolution_x=1400;s.render.resolution_y=1000;s.render.resolution_percentage=100
s.world=bpy.data.worlds.new('World');s.world.color=(.45,.45,.45);s.render.image_settings.file_format='PNG';s.render.film_transparent=False
s.view_settings.view_transform='Standard';s.view_settings.look='Medium High Contrast';s.view_settings.exposure=0;s.view_settings.gamma=1

def mat(name,c):
 m=bpy.data.materials.new(name);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=.78;return m
mats={'A':mat('NEUTRAL_A_NOT_SOURCE_COLOR',(.55,.60,.64)),'B':mat('NEUTRAL_B_NOT_SOURCE_COLOR',(.64,.61,.56)),'CENTRAL':mat('NEUTRAL_CENTRAL_NOT_SOURCE_COLOR',(.62,.65,.61)),'base':mat('ARTIFICIAL_DISPLAY_BASE',(.34,.37,.39)),'skin':mat('HYPOTHETICAL_SKIN_AND_SUPPORT_NEUTRAL',(.76,.76,.72)),'ref':mat('FINITE_REFERENCE_LINE_NOT_WALL',(.12,.32,.42))}
phys=bpy.data.collections.new('PHYSICAL_ARTIFICIAL_RESEARCH_ASSEMBLY');s.collection.children.link(phys)
refs=bpy.data.collections.new('SOURCE_ONLY_FINITE_REFERENCES_NO_OPAQUE_FACES');s.collection.children.link(refs)
objects=[];meta=json.loads((ROOT/'inputs/physical-meshes.json').read_text())
for d in meta['objects']:
 m=bpy.data.meshes.new(d['id']);m.from_pydata(d['vertices_mm'],[],d['triangles']);m.update();o=bpy.data.objects.new(d['id'],m);phys.objects.link(o);objects.append(o)
 o['role']='ARTIFICIAL_BASE_NOT_BUILDING_SLAB' if d['id']=='ARTIFICIAL_SHARED_BASE' else 'FULL_HEIGHT_MANUFACTURING_PROXY_FRAME'if d['id']in('A','B','CENTRAL')else'DETACHABLE_HYPOTHETICAL_SKIN_WITH_ENTIRE_SUPPORT'
 o['not_actual_building_or_print_certification']=True;o.data.materials.append(mats.get(d['id'],mats['base']if d['id']=='ARTIFICIAL_SHARED_BASE'else mats['skin']))
for d in json.loads((ROOT/'inputs/reference-baselines.json').read_text())['records']:
 c=bpy.data.curves.new('REF_'+d['id'],'CURVE');c.dimensions='3D';c.resolution_u=1;c.bevel_depth=.085;c.bevel_resolution=0;p=c.splines.new('POLY');p.points.add(len(d['points_mm'])-1)
 for v,pt in zip(p.points,d['points_mm']):v.co=(*pt,1)
 o=bpy.data.objects.new('REF_'+d['id'],c);refs.objects.link(o);c.materials.append(mats['ref']);o['scope']=d['scope']
refs.hide_render=True;refs.hide_viewport=True
bpy.ops.mesh.primitive_plane_add(size=1000,location=(90,50,-2.05));ground=bpy.context.object;ground.name='RENDER_GROUND_NOT_MODEL';ground.data.materials.append(mat('RENDER_GROUND',(.93,.94,.95)))
for loc,power,size in [((40,-70,240),65000,180),((230,160,180),45000,160)]:
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.data.energy=power;o.data.shape='DISK';o.data.size=size
bpy.ops.object.camera_add(location=(300,-300,240));cam=bpy.context.object;cam.rotation_euler=(Vector((90,50,30))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=248;s.camera=cam
transforms={}
def state(mode):
 refs.hide_render=mode!='source_only';refs.hide_viewport=mode!='source_only'
 for o in objects:
  o.location=(0,0,0);o.hide_render=False;o.hide_viewport=False
  if mode=='source_only':o.hide_render=True;o.hide_viewport=True
  if mode=='hypotheses_removed' and o.name not in ('A','B','CENTRAL','ARTIFICIAL_SHARED_BASE'):o.hide_render=True;o.hide_viewport=True
  if mode=='exploded':
   shift={'A':(-25,0,16),'B':(25,0,16),'CENTRAL':(0,-30,16),'C8_NOMINAL_PLATFORM':(0,10,45),'L5_NOMINAL_PLATFORM':(0,-30,38),'A_NOMINAL_ROOF_SUPPORT_0':(-35,-15,65),'A_NOMINAL_ROOF_SUPPORT_1':(-35,15,65),'B_FINITE_UPPER_CANDIDATE_PROXY':(35,0,65),'SOUTH_UPPER_BAND_NOMINAL_REFERENCE_PLANE':(60,0,28)}.get(o.name,(0,0,0));o.location=shift
 # Frame every visible physical vertex; no cropped exploded roof or support.
 pts=[o.matrix_world @ v.co for o in objects if not o.hide_render for v in o.data.vertices]
 if not pts:pts=[Vector(p) for d in json.loads((ROOT/'inputs/reference-baselines.json').read_text())['records'] for p in d['points_mm']]
 bpy.context.view_layer.update()
 pts=[v.co + o.location for o in objects if not o.hide_render for v in o.data.vertices] if mode!='source_only' else pts
 center=Vector(tuple((min(p[k] for p in pts)+max(p[k] for p in pts))/2 for k in range(3)))
 cam.location=center+Vector((210,-350,210));cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler();bpy.context.view_layer.update()
 inv=cam.matrix_world.inverted();local=[inv@p for p in pts];w=max(p.x for p in local)-min(p.x for p in local);h=max(p.y for p in local)-min(p.y for p in local)
 cam.data.ortho_scale=max(w,h*s.render.resolution_x/s.render.resolution_y)*1.18
 transforms[mode]={o.name:{'translation_mm':list(o.location),'hidden':o.hide_render}for o in objects}
for mode in ['assembled','hypotheses_removed','source_only','exploded']:
 state(mode);s.render.filepath=str(OUT/'previews'/f'{mode}.png');bpy.ops.render.render(write_still=True)
state('assembled');s.render.filepath='//previews/assembled.png';bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'scene.blend'))
(OUT/'VIEW-MODE-TRANSFORMS.json').write_text(json.dumps({'scope':'Exploded transforms are presentation only, not the insertion trajectories. Assembled is identity. Source-only excludes fullheight proxies, artificial carriers/base and conditional roof shapes.','modes':transforms},indent=2)+'\n')
(OUT/'SCENE-BUILD-REPORT.json').write_text(json.dumps({'physical_object_count':len(objects),'triangles':sum(len(o.data.polygons)for o in objects),'reference_curve_count':len(refs.objects),'source_inputs':{p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in (ROOT/'inputs').glob('*.json')},'all_physical_identity_on_save':all(tuple(o.location)==(0,0,0)for o in objects),'hypotheses_removed_includes_all_dedicated_supports':True},indent=2)+'\n')
