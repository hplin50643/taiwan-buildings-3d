"""Check image identity and links without overwriting the historical report."""
from pathlib import Path
import hashlib,json,re,subprocess,sys

R=Path(__file__).resolve().parent
U=R/"appearance"
subprocess.run([sys.executable,str(U/"source/verify_display_webp.py")],check=True)
slug=R.name
target=(R/"README.md").resolve()
cs="docs/display/catalog/dila-jinshan"
rx=re.compile(r"\[!\[[^\]]*\]\(([^)]+)\)\]\(([^)]+)\)")
for p in (R/"README.md",U/"README.md"):
    pairs=rx.findall(p.read_text())
    assert len(pairs)==4 and len(set(s for s,_ in pairs))==4,p
    for src,href in pairs:
        assert src.endswith("-640.webp") and href==src.replace("-640.webp",".webp"),p
        assert (p.parent/src).is_file() and (p.parent/href).is_file()
repo=R.parents[4]
catalog=repo/cs
proof=json.loads((catalog/"RENDER-PROOF.json").read_text())
card=next(x for x in proof["cards"] if "/"+slug+"/" in x["model"])
assert hashlib.sha256((repo/card["model"]).read_bytes()).hexdigest()==card["model_sha256"]
thumb=repo/card["preview"]
assert hashlib.sha256(thumb.read_bytes()).hexdigest()==card["preview_sha256"]
for p in (R.parents[1]/"README.md",R.parents[2]/"README.md"):
    pairs=rx.findall(p.read_text())
    selected=[(s,h) for s,h in pairs if (p.parent/s).resolve()==thumb.resolve()]
    assert len(selected)==1 and (p.parent/selected[0][1]).resolve()==target,p
print("Color detail and existing catalog image links verified.")
