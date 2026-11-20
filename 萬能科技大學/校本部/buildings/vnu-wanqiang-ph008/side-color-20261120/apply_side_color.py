"""From package root: blender -b scene.blend -P side-color-20261120/apply_side_color.py -- [--qa-renders]."""
import bpy,json,sys
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
P=Path(__file__).resolve().parent
def put_json(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def strip_png_run_metadata(path):
    # Remove Blender's local File / timing chunks without recompressing pixels.
    data=path.read_bytes();assert data[:8]==b'\x89PNG\r\n\x1a\n'
    keep=[data[:8]];i=8
    while i<len(data):
        size=int.from_bytes(data[i:i+4],'big');kind=data[i+4:i+8];end=i+12+size
        assert end<=len(data)
        if kind not in {b'tEXt',b'zTXt',b'iTXt',b'tIME',b'eXIf'}:keep.append(data[i:end])
        i=end
    assert i==len(data) and keep[-1][4:8]==b'IEND'
    path.write_bytes(b''.join(keep))
config=json.loads((P/'domain.json').read_text()); hex_color='536C62'
scene=bpy.context.scene; obj=bpy.data.objects['Printable_VNU']; cam=scene.camera
assert len(obj.data.polygons)==1004 and len(obj.data.materials)==1
assert obj.data.materials[0].name=='Warm stone preview only'
assert all(p.material_index==0 for p in obj.data.polygons)
coords=[[obj.data.vertices[k].co for k in p.vertices] for p in obj.data.polygons]
ids=[i for i,v in enumerate(coords) if all(abs(q.x-67.2)<1e-4 for q in v) and any(all(abs(q.y-y)<=1.1001 for q in v) for y in [-24,5])]
assert ids==config['ids']
old=(cam.location.copy(),cam.rotation_euler.copy(),cam.data.ortho_scale,scene.render.filepath)
views=[('right-overview',(225,-155,115),(0,2,30),212),('right-wall-detail',(220,-38,68),(63,5,28),91)]
do_render='--qa-renders' in sys.argv
out={}
for phase in ['before','after']:
    if phase=='after':
        for m in bpy.data.materials:
            if m.users==0:m.use_fake_user=True
        m=bpy.data.materials.new('VNU Wanqiang right-column outer face gray green; uncalibrated')
        m.diffuse_color=tuple(((int(hex_color[i:i+2],16)/255+.055)/1.055)**2.4 for i in [0,2,4])+(1,)
        obj.data.materials.append(m)
        for i in ids:obj.data.polygons[i].material_index=1
    if do_render:
        for label,loc,aim,scale in views:
            cam.location=loc;cam.rotation_euler=(Vector(aim)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale
            bpy.context.view_layer.update()
            ix=range(len(obj.data.vertices)) if label.endswith('overview') else sorted({k for i in ids for k in obj.data.polygons[i].vertices})
            v=[world_to_camera_view(scene,cam,obj.matrix_world @ obj.data.vertices[i].co) for i in ix]
            bb=[min(p.x for p in v),max(p.x for p in v),min(p.y for p in v),max(p.y for p in v)]
            assert 0 < bb[0]<bb[1]<1 and 0<bb[2]<bb[3]<1,bb
            out[f'{phase}-{label}']={'normalized_projection_bbox':bb,'domain':'all original mesh vertices' if label.endswith('overview') else 'all target right-wall vertices','camera_location':loc,'camera_aim':aim,'orthographic_scale':scale}
            scene.render.filepath=str(P/(phase+'-'+label+'.png'))
            bpy.ops.render.render(write_still=True)
            strip_png_run_metadata(Path(scene.render.filepath))
cam.location,cam.rotation_euler,cam.data.ortho_scale,scene.render.filepath=old
bpy.context.view_layer.update()
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(P/'scene.blend'))
if do_render:put_json(P/'framing-QA.json',out)
