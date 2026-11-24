"""Verify current TUT appearance WebP files and binding to frozen source evidence."""
import argparse, hashlib, io, json
from pathlib import Path
from PIL import Image
A=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def verify(root,rebuild=None):
    read=lambda f:json.loads((root/f).read_bytes())
    proof=read('display-proof.json')
    manifest={a['path']:a for a in read('appearance-publication-manifest.json')['files']}
    previous=read('appearance-reproduction-qa.json')
    assert previous['passed'] and previous['original_STL_SHA256']==proof['current_native_sha256']['model.stl']
    assert previous['source_archive_SHA256']==proof['current_native_sha256']['appearance-rebuild-source.zip']
    for f,h in proof['current_native_sha256'].items():
        assert sha((root/f).read_bytes())==h,f
    viewset={r['view'] for r in read('appearance-render-manifest.json')['views']}
    assert len(proof['view_checks'])==len(viewset)==4
    assert {Path(r['archive_filename']).stem for r in proof['view_checks']}==viewset
    for a in proof['view_checks']:
        n=a['archive_filename']
        assert previous['checks'][n] and manifest[a['original']]['sha256']==a['source_sha256']
        b=(root/a['webp']).read_bytes()
        assert len(b)==a['webp_bytes'] and sha(b)==a['webp_sha256'],n+' WebP SHA'
        with Image.open(io.BytesIO(b)) as image:
            assert image.format=='WEBP' and b[12:16]==b'VP8L' and not getattr(image,'is_animated',False)
            assert list(image.size)==a['size'] and sha(image.convert('RGBA').tobytes())==a['decoded_rgba_sha256'],n+' RGBA SHA'
        if rebuild is not None:
            f=(rebuild/n).read_bytes()
            with Image.open(io.BytesIO(f)) as im:
                assert list(im.size)==a['size'] and sha(im.convert('RGBA').tobytes())==a['decoded_rgba_sha256'],n+' fresh RGBA'
    return len(viewset)
if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--rebuilt-package',type=Path,help='Optional output directory of the isolated appearance rebuild')
    print(verify(A,p.parse_args().rebuilt_package),'lossless WebP views verified against current model records')
