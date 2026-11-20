"""Read-only release validation, not a model or preview rebuild."""
import hashlib, io, json, zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

import numpy as np

root = Path(__file__).resolve().parent
def read(name):
    return (root / name).read_bytes()
def verify(ok, description):
    if not ok:
        raise ValueError(description)
def digest(data):
    return hashlib.sha256(data).hexdigest()

for line in read("SHA256SUMS").decode().splitlines():
    expected, filename = line.split("  ", 1)
    verify(Path(filename).name == filename and digest(read(filename)) == expected,
           f"Release checksum: {filename}")
for manifest in ("CHEEK-MANIFEST.json", "FREEZE-MANIFEST.json"):
    entries = json.loads(read(manifest))["files"]
    for item in entries:
        payload = read(item["path"])
        verify(len(payload) == item["bytes"] and digest(payload) == item["sha256"],
               f"{manifest}: {item['path']}")

with zipfile.ZipFile(io.BytesIO(read("cheek-baseline-inputs.zip"))) as archive:
    expected = {name: archive.read(next(n for n in archive.namelist() if Path(n).name == name))
                for name in ("model.stl", "model.obj", "color-mesh.npz", "palette.json", "appearance.3mf")}
for name in ("model.stl", "model.obj", "palette.json"):
    verify(read(name) == expected[name], f"Original bytes: {name}")
baseline = np.load(io.BytesIO(expected["color-mesh.npz"]), allow_pickle=False)
current = np.load(io.BytesIO(read("color-mesh.npz")), allow_pickle=False)
verify(baseline.files == current.files, "Array inventory")
for key in ("vertices", "faces"):
    verify(baseline[key].dtype == current[key].dtype and
           np.array_equal(baseline[key], current[key]), f"Original array: {key}")
old, new = baseline["materials"], current["materials"]
change = json.loads(read("cheek-return-change.json"))
ids = change["ids"]
verify(old.dtype == new.dtype and len(new) == 5250 and
       np.flatnonzero(old != new).tolist() == sorted(ids) and
       np.all(old[ids] == 1) and np.all(new[ids] == 0), "Exact changed face IDs and transition")
materials = json.loads(read("appearance-materials.json"))
counts = np.bincount(new, minlength=2).tolist()
verify(counts == [74, 5176] == [m["faces"] for m in materials["palette"]],
       "Current material counts")
verify(sorted(sum(materials["domain_face_indices"].values(), [])) ==
       np.flatnonzero(new == 0).tolist(), "Current documented material domains")
with zipfile.ZipFile(io.BytesIO(read("appearance.3mf"))) as archive:
    model = ET.fromstring(archive.read("3D/3dmodel.model"))
ns = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}
with zipfile.ZipFile(io.BytesIO(expected["appearance.3mf"])) as archive:
    old_model = ET.fromstring(archive.read("3D/3dmodel.model"))
faces = model.findall(".//m:triangle", ns)
vertices = model.findall(".//m:vertex", ns)
verify(model.attrib.get("unit") == "millimeter" and
       np.array_equal([[int(t.attrib[k]) for k in ("v1", "v2", "v3")] for t in faces],
                      current["faces"]) and
       np.array_equal([int(t.attrib["p1"]) for t in faces], new) and
       [v.attrib for v in vertices] == [v.attrib for v in old_model.findall(".//m:vertex", ns)] and
       np.allclose(np.array([[float(v.attrib[k]) for k in ("x", "y", "z")] for v in vertices]),
                   current["vertices"], rtol=0.0, atol=5e-9),
       "3MF geometry, order, units and per-face colors")
print(json.dumps({"status": "PASS", "mode": "read-only publication verification",
                  "triangles": len(new), "counts": counts, "changed_face_ids": ids}))
