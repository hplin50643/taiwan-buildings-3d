"""Convert the unchanged parent ASCII STL to compact binary STL, without remeshing.
Run from this directory: python convert_ascii_to_binary.py
"""
from pathlib import Path
import hashlib, struct, math
R=Path(__file__).resolve().parent
source=R.parent/'model.stl'
b=source.read_bytes()
assert hashlib.sha256(b).hexdigest()=='6e1c338abc56367db05ceb285e223071e96eb950f847d7895347387233de68b7'
lines=iter(b.decode('ascii').splitlines())
records=[]
for line in lines:
    bits=line.split()
    if bits[:2]!=['facet','normal']:
        continue
    assert len(bits)==5
    normal=list(map(float,bits[2:]))
    assert next(lines).split()==['outer','loop']
    vertices=[]
    for _ in range(3):
        v=next(lines).split();assert len(v)==4 and v[0]=='vertex'
        vertices.extend(map(float,v[1:]))
    assert next(lines).split()==['endloop']
    assert next(lines).split()==['endfacet']
    assert all(math.isfinite(v) for v in normal+vertices)
    records.append(struct.pack('<12fH',*(normal+vertices),0))
assert len(records)==133722
out=b'\0'*80+struct.pack('<I',len(records))+b''.join(records)
assert hashlib.sha256(out).hexdigest()=='9c8d83832ee8de3908ed20a9a76c70913feb8c93220bd94974ee1d1cfe4fc65e'
(R/'model-binary.stl').write_bytes(out)
print('Verified compact binary STL:',len(out),'bytes;',len(records),'triangles')
