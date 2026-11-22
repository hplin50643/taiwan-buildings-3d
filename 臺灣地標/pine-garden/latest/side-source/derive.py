"""Derive exact bounded existing side masonry map and color-only 3MF from legacy files."""
from pathlib import Path
from zipfile import ZipFile
import json,hashlib,re,struct,sys
q=Path(sys.argv[1]); a=json.loads((q/'face-material-map.json').read_text()); stl=(q/'model.stl').read_bytes()
assert hashlib.sha256(stl).hexdigest()==a['source_stl_sha256']
hold=set().union(*(a[k] for k in ('roof','front_masonry','white_hold_door_back','white_hold_transom_back','excluded_side_gable_vent'))); grouped={}
for sign in (-1,1):
    ids=[]
    for i,t in enumerate(struct.iter_unpack('<12fH',stl[84:])):
        v=[t[k:k+3] for k in (3,6,9)]
        if t[0]*sign>.9999 and all(abs(x-sign*65)<.0002 and -21.0001<=y<=23.0001 and 5.3999<=z<=44.8001 for x,y,z in v):
            assert i not in hold; ids.append(i)
    assert len(ids)==28; grouped[str(sign)]=ids
(q/'side-face-proof.json').write_text(json.dumps(grouped,indent=2)+'\n')
ids=set().union(*grouped.values())
with ZipFile(q/'model.3mf') as old, ZipFile(q/'current.3mf','w') as new:
    for info in old.infolist():
        file=old.read(info.filename)
        if info.filename=='3D/3dmodel.model':
            lines=list(re.finditer(rb'<triangle [^<>]+/>',file)); assert len(lines)==5874
            assert all(b'v1="' in line.group() for line in lines)
            changed=file; off=0
            for i,line in enumerate(lines):
                if i in ids:
                    raw=line.group()
                    if b'p1=' not in raw:
                        replace=raw.replace(b' />',b' pid="1" p1="2" />')
                    else:
                        assert b'p1="0"' in raw and b'p2=' not in raw and b'p3=' not in raw
                        replace=raw.replace(b'p1="0"',b'p1="2"')
                    assert replace!=raw
                    changed=changed[:line.start()+off]+replace+changed[line.end()+off:]
                    off+=len(replace)-len(raw)
            file=changed
        new.writestr(info,file)
