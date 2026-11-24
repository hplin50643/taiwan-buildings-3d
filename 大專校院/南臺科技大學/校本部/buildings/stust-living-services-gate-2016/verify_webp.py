"""Validate current WebP bytes, decoded RGBA and signed same-model evidence."""
import argparse,hashlib,io,json
from pathlib import Path
from PIL import Image
A=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def verify(root,scratch_render=None):
    load=lambda x:json.loads((root/x).read_bytes())
    p=load('cover-lineage-proof.json')
    d=load('DELIVERY-QA.json')
    t=load('NO-TEXT-QA.json')
    f=load('FRAMING-QA.json')
    v=load('SCENE-QA.json')
    g=load('COLOR-FORMAT-GEOMETRY-QA.json')
    mesh=sha((root/'color-mesh.npz').read_bytes())
    assert mesh==d['mesh_sha256']==f['mesh_sha256']==v['mesh_sha256']==g['color_mesh_sha256']==p['qa_display_sources']['color_mesh_sha256']
    assert all(a['status']=='PASS' for a in (d,t,f,v,g))
    for a,h in p['source_sha256'].items():assert sha((root/a).read_bytes())==h,a
    rows=p['qa_display_sources']['files']
    assert len(rows)==10
    assert {Path(a['png']).stem for a in rows if a['role']=='whole'}==set(f['projected_vertex_bounds'])
    for a in rows:
        n=a['png']; b=(root/a['webp']).read_bytes()
        assert a['png_sha256']==d['images_sha256'][n]==t['images_sha256'][n]
        assert a['webp_sha256']==sha(b) and len(b)==a['webp_bytes'],n+' WebP file SHA'
        with Image.open(io.BytesIO(b)) as image:
            assert image.format=='WEBP' and b[12:16]==b'VP8L' and not getattr(image,'is_animated',False)
            assert list(image.size)==a['decoded_dimensions'] and sha(image.convert('RGBA').tobytes())==a['decoded_rgba_sha256'],n+' RGBA SHA'
        if a['role']=='technical_detail':
            raw=(root/n).read_bytes()
            assert sha(raw)==a['png_sha256']
            with Image.open(io.BytesIO(raw)) as old:assert sha(old.convert('RGBA').tobytes())==a['decoded_rgba_sha256']
        if scratch_render is not None and (scratch_render/n).is_file():
            with Image.open(scratch_render/n) as fresh:
                assert list(fresh.size)==a['decoded_dimensions'] and sha(fresh.convert('RGBA').tobytes())==a['decoded_rgba_sha256'],n+' fresh RGBA'
    if scratch_render is not None:
        assert any((scratch_render/a['png']).is_file() for a in rows),'no scratch views matched'
    return len(rows)
if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--scratch-render',type=Path,help='Optional PNG directory generated outside this repository')
    print(verify(A,p.parse_args().scratch_render),'lossless WebP views verified against current model records')
