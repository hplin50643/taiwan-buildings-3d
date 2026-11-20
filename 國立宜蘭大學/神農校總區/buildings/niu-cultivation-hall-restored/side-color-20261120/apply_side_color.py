"""Use Blender 5.2+: blender -b models/v1/scene.blend -P side-color-20261120/apply_side_color.py -- --qa-renders"""
import bpy,json,sys,hashlib
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
P=Path(__file__).resolve().parent
domain=json.loads((P/'domain.json').read_text()); mapold=json.loads((P/'original-palette-and-face-map.json').read_text())
orig=Path(bpy.data.filepath); assert hashlib.sha256(orig.read_bytes()).hexdigest()==mapold['source_scene_sha256']
s=bpy.context.scene; obj=bpy.data.objects[domain['print_mesh']]; cam=s.camera
assert len(obj.data.polygons)==1832
assert [m.name for m in obj.data.materials]==[m['name'] for m in mapold['materials']]
assert [p.material_index for p in obj.data.polygons]==mapold['material_indices_original_ordered_STL']
ids=[]
for p in obj.data.polygons:
    q=[obj.matrix_world @ obj.data.vertices[k].co for k in p.vertices]
    n=(q[1]-q[0]).cross(q[2]-q[0])
    if n.x<0 and n.z<0 and max(abs(v.x+v.z+39.1) for v in q)<2e-5:ids.append(p.index)
assert ids==[297,322]==domain['ids']
# Preserve baseline camera, world, Cycles settings, paths, and the six existing materials.
for i in ids: obj.data.polygons[i].material_index=2
out=P/'models/v1/scene.blend';out.parent.mkdir(parents=True,exist_ok=True)
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=False,relative_remap=False)
if '--qa-renders' in sys.argv:
    # Inspection render settings below are temporary; saved project is not modified.
    s.render.engine='BLENDER_WORKBENCH'; w=s.display.shading
    w.light='STUDIO';w.color_type='MATERIAL';w.show_shadows=False;w.show_cavity=True;w.cavity_type='BOTH'
    w.background_type='WORLD'; s.world.color=(0.095,0.105,0.12)
    s.view_settings.view_transform='Standard';s.render.image_settings.file_format='PNG'
    s.render.film_transparent=False;s.render.use_stamp=False
    s.render.resolution_x=1200;s.render.resolution_y=820;s.render.resolution_percentage=100
    frame={}
    def strip_png_metadata(p):
        raw=p.read_bytes(); assert raw[:8]==b'\x89PNG\r\n\x1a\n'
        out=[raw[:8]]; j=8
        while j<len(raw):
            n=int.from_bytes(raw[j:j+4],'big');k=raw[j+4:j+8];end=j+12+n
            assert end<=len(raw)
            if k not in {b'tEXt',b'zTXt',b'iTXt',b'tIME',b'eXIf'}:out.append(raw[j:end])
            j=end
        assert j==len(raw) and out[-1][4:8]==b'IEND'
        p.write_bytes(b''.join(out))
    for phase,mi in [('before',0),('after',2)]:
        for i in ids: obj.data.polygons[i].material_index=mi
        for label,pos,aim,zoom in [('left-overview',(-255,-142,35),(0,-7,23),224),('left-eave-detail',(-195,-15,17),(-76,0,33),96)]:
            cam.location=Vector(pos);cam.rotation_euler=(Vector(aim)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=zoom
            bpy.context.view_layer.update()
            vtx=range(len(obj.data.vertices)) if label=='left-overview' else {k for i in ids for k in obj.data.polygons[i].vertices}
            uv=[world_to_camera_view(s,cam,obj.matrix_world @ obj.data.vertices[k].co) for k in vtx]
            box=[min(q.x for q in uv),max(q.x for q in uv),min(q.y for q in uv),max(q.y for q in uv)]
            assert 0<box[0]<box[1]<1 and 0<box[2]<box[3]<1,box
            fn=f'{phase}-{label}'
            frame[fn]={'normalized_projected_bounds_xy':box,'tested_vertices':'whole original printable object' if label=='left-overview' else 'complete left eave bevel only','camera_position':pos,'target':aim,'ortho_scale':zoom}
            s.render.filepath=str(P/(fn+'.png'));bpy.ops.render.render(write_still=True)
            strip_png_metadata(P/(fn+'.png'))
    (P/'framing-QA.json').write_text(json.dumps(frame,indent=2)+'\n')
