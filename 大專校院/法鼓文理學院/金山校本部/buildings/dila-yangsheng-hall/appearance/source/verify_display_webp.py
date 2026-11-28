"""Verify the released color views; optionally re-render in a disposable copy."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess,tempfile
from PIL import Image

A=Path(__file__).resolve().parents[1]
sha=lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
def rgba(p):
    with Image.open(p) as f:
        im=f.convert("RGBA")
    return list(im.size),hashlib.sha256(im.tobytes()).hexdigest()

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--rebuild",action="store_true")
    parser.add_argument("--blender",default="blender")
    a=parser.parse_args()
    proof=json.loads((A/"qa/display-webp.json").read_text())
    assert set(proof["views"])=={"front","rear","top","elevation"}
    for k,h in proof["native_sha256"].items():
        assert sha(A/k)==h,k
    assert not list((A/"previews").glob("*.png"))
    for view,r in proof["views"].items():
        p=A/"previews"/(view+".webp")
        assert sha(p)==r["webp_sha256"] and rgba(p)==(r["dimensions"],r["rgba_sha256"]),view
        p=A/"previews"/(view+"-640.webp")
        assert sha(p)==r["thumbnail_sha256"] and rgba(p)==(r["thumbnail_dimensions"],r["thumbnail_rgba_sha256"]),view
    if a.rebuild:
        with tempfile.TemporaryDirectory(prefix="dila-color-") as d:
            t=Path(d)
            (t/"source").mkdir()
            (t/"qa").mkdir()
            for k in ("source/render_appearance.py","yangsheng-appearance.3mf","palette.json"):
                shutil.copyfile(A/k,t/k)
            subprocess.run([a.blender,"-b","-t","8","--python-exit-code","1","--python",str(t/"source/render_appearance.py"),"--","--isolated-display-reproduction"],check=True)
            for view,r in proof["views"].items():
                assert rgba(t/"previews"/(view+".png"))==(r["dimensions"],r["rgba_sha256"]),view
    print("Four current color preview pairs verified.")

if __name__=="__main__":
    main()
