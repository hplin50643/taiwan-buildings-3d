"""Use Blender 4.3.2+: blender -b appearance/scene.blend -P side-color-20261120/apply_side_color.py -- --qa-renders"""
import bpy,json,sys,hashlib
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
P=Path(__file__).resolve().parent
domain=json.loads((P/'domain.json').read_text())
orig=Path(bpy.data.filepath);assert hashlib.sha256(orig.read_bytes()).hexdigest()==domain['original_appearance_blend_sha256']
s=bpy.context.scene
obj=next(o for o in s.objects if o.type=='MESH' and len(o.data.polygons)==2444)
cam=s.camera;ids=[]
for pl in obj.data.polygons:
    q=[obj.matrix_world@obj.data.vertices[i].co for i in pl.vertices]
    if any(all(abs(v.y-(43.05-i*1.15))<1e-4 for v in q) for i in range(12)) and (q[1]-q[0]).cross(q[2]-q[0]).normalized().y>.99999:ids.append(pl.index)
assert ids==sorted(domain['ids']) and len(ids)==32
assert len(obj.data.materials)==3 and obj.data.materials[2].name=='lightgray_open_pavilion_columns'
assert all(obj.data.polygons[i].material_index==0 for i in ids)
for i in ids:obj.data.polygons[i].material_index=2
out=P/'scene.blend'
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
        for label,pos,aim,zoom in [('end-overview',(220,232,132),(0,0,13),205),('stair-riser-detail',(126,190,62),(61.2,36.7,8.4),33)]:
            w.light='FLAT' if label=='stair-riser-detail' else 'STUDIO'
            cam.location=Vector(pos);cam.rotation_euler=(Vector(aim)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=zoom
            bpy.context.view_layer.update()
            vtx=range(len(obj.data.vertices)) if label=='end-overview' else {k for i in ids for k in obj.data.polygons[i].vertices}
            uv=[world_to_camera_view(s,cam,obj.matrix_world @ obj.data.vertices[k].co) for k in vtx]
            box=[min(q.x for q in uv),max(q.x for q in uv),min(q.y for q in uv),max(q.y for q in uv)]
            assert 0<box[0]<box[1]<1 and 0<box[2]<box[3]<1,box
            fn=f'{phase}-{label}'
            frame[fn]={'normalized_projected_bounds_xy':box,'tested_vertices':'whole original printable object' if label=='end-overview' else 'complete targeted stair risers only','camera_position':pos,'target':aim,'ortho_scale':zoom}
            s.render.filepath=str(P/(fn+'.png'));bpy.ops.render.render(write_still=True)
            strip_png_metadata(P/(fn+'.png'))
    (P/'framing-QA.json').write_text(json.dumps(frame,indent=2)+'\n')
