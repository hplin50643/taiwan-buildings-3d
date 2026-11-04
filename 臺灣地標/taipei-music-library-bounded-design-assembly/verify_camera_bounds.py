import bpy,json,ast,hashlib
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
ROOT=Path(__file__).resolve().parent;p=ROOT/'scene.blend';before=hashlib.sha256(p.read_bytes()).hexdigest();bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False,use_scripts=False)
s=bpy.context.scene;cam=s.camera;objects=list(bpy.data.collections['PHYSICAL_ARTIFICIAL_RESEARCH_ASSEMBLY'].objects);refs=bpy.data.collections['SOURCE_ONLY_FINITE_REFERENCES_NO_OPAQUE_FACES'];transforms={}
a=ast.parse((ROOT/'build_scene.py').read_text());fn=next(n for n in a.body if isinstance(n,ast.FunctionDef)and n.name=='state');exec(compile(ast.Module(body=[fn],type_ignores=[]),'local_camera_state','exec'))
report={}
for mode in ['assembled','hypotheses_removed','source_only','exploded']:
 state(mode);bpy.context.view_layer.update();pts=[o.matrix_world@v.co for o in objects if not o.hide_render for v in o.data.vertices]
 if mode=='source_only':pts=[o.matrix_world@Vector(p.co[:3])for o in refs.objects for p in o.data.splines[0].points]
 vv=[world_to_camera_view(s,cam,p)for p in pts];W=s.render.resolution_x;H=s.render.resolution_y
 b=[min(p.x for p in vv)*W,min(1-p.y for p in vv)*H,max(p.x for p in vv)*W,max(1-p.y for p in vv)*H];margin=min(b[0],b[1],W-b[2],H-b[3]);assert margin>20,(mode,b)
 report[mode]={'visible_vertices':len(pts),'render_bounds_px_left_top_right_bottom':b,'minimum_canvas_margin_px':margin,'camera_location':list(cam.location),'camera_rotation_euler':list(cam.rotation_euler),'ortho_scale':cam.data.ortho_scale,'canvas':[W,H],'all_in_front':all(p.z>0 for p in vv)}
assert hashlib.sha256(p.read_bytes()).hexdigest()==before
(ROOT/'ACTUAL-CAMERA-FRAMING-VERIFICATION.json').write_text(json.dumps({'method':'Actual scene mesh vertices transformed per view mode and projected through actual orthographic camera; source-only curve control points. No save. Caption appended outside original render.','scene_sha256':before,'views':report},indent=2)+'\n')
