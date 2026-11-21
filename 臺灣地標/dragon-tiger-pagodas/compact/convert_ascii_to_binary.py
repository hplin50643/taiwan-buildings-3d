"""Convert the exact archived ASCII STL to compact binary STL, without remeshing."""
from pathlib import Path
import argparse, hashlib, struct, math
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--source', required=True, type=Path)
parser.add_argument('--output', required=True, type=Path)
args=parser.parse_args()
source=args.source
assert source.resolve()!=args.output.resolve(), 'Use distinct input and output paths'
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
with args.output.open('xb') as dst:
    dst.write(out)
print('Verified compact binary STL:',len(out),'bytes;',len(records),'triangles')
