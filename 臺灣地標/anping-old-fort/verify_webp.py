"""Verify Anping's six current lossless WebP files without checked-in PNGs."""
import argparse,hashlib,io,json
from pathlib import Path
from PIL import Image
A=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def verify(root,rebuilt=None):
    load=lambda p:json.loads((root/p).read_bytes())
    d=load('qa/display-proof.json')
    old=load('qa/clean-public-rebuild-validation.json')
    assert old['all_pass'] and all(old['exact_artifact_bytes'].values())
    hist={x['file']:x for x in old['previews']}
    assert set(hist)=={f'previews/{name}.png' for name in d['views']} and len(hist)==6
    for f,h in d['model_sha256'].items():
        assert sha((root/f).read_bytes())==h,f
    for name,r in d['views'].items():
        legacy=f'previews/{name}.png'
        oldrow=hist[legacy]
        assert oldrow['png_bytes_identical'] and oldrow['decoded_pixel_bytes_identical']
        assert oldrow['mode']=='RGBA' and oldrow['sha256']==r['current_png_sha256']
        assert oldrow['decoded_pixel_sha256']==r['decoded_rgba_sha256'] and oldrow['dimensions']==r['dimensions']
        w=(root/f'previews/{name}-current.webp').read_bytes()
        assert len(w)==r['webp_bytes'] and sha(w)==r['current_webp_sha256'],name+' WebP SHA'
        with Image.open(io.BytesIO(w)) as im:
            assert im.format=='WEBP' and w[12:16]==b'VP8L' and not getattr(im,'is_animated',False)
            assert list(im.size)==r['dimensions'] and sha(im.convert('RGBA').tobytes())==r['decoded_rgba_sha256'],name+' RGBA SHA'
        if rebuilt is not None:
            b=(rebuilt/legacy).read_bytes()
            assert sha(b)==r['current_png_sha256'],name+' rebuilt historical PNG byte SHA'
            with Image.open(io.BytesIO(b)) as im:
                assert list(im.size)==r['dimensions'] and sha(im.convert('RGBA').tobytes())==r['decoded_rgba_sha256'],name+' rebuilt RGBA'
    return len(hist)
if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--rebuilt',type=Path,help='Optional scratch package containing newly produced PNGs')
    print(verify(A,p.parse_args().rebuilt),'lossless WebP views verified')
