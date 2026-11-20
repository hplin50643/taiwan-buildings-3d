"""Add the required object-level fallback to one explicitly face-colored 3MF.

Each triangle already defines a complete color assignment. The fallback is
the base palette index 0 and never overrides any triangle.
All XML bytes except the two object attributes and all other ZIP members'
uncompressed bytes are preserved. Input is never written.
"""
from pathlib import Path
import argparse,re,zipfile,xml.etree.ElementTree as ET
def normalize(source: Path, destination: Path):
    assert source.resolve()!=destination.resolve()
    with zipfile.ZipFile(source) as src:
        infos = src.infolist()
        model, = [i.filename for i in infos if i.filename.lower().endswith('.model')]
        payload = {i.filename:src.read(i) for i in infos}
        comment=src.comment
    xml=payload[model];root=ET.fromstring(xml)
    obj, = root.findall('.//{*}object')
    group, = root.findall('.//{*}basematerials')
    gid=group.attrib['id'];bases=group.findall('{*}base');ts=obj.findall('.//{*}triangle')
    assert ts and gid.isdecimal() and all(t.get('pid')==gid and t.get('p1') is not None and t.get('p2')==t.get('p3')==t.get('p1') and 0<=int(t.get('p1'))<len(bases) for t in ts)
    # Use the same base index as the documented resource-default convention.
    fallback='0'
    if obj.get('pid')==gid and obj.get('pindex')==fallback:return False
    assert obj.get('pid') is None and obj.get('pindex') is None
    added=f' pid="{gid}" pindex="{fallback}"'.encode()
    matches=list(re.finditer(rb'<(?:[A-Za-z_][\w.-]*:)?object(?=\s)[^<>]*>',xml));match,=matches
    final=xml[:match.end()-1]+added+xml[match.end()-1:]
    updated=ET.fromstring(final)
    u,=updated.findall('.//{*}object')
    assert u.attrib.pop('pid')==gid and u.attrib.pop('pindex')==fallback
    assert ET.tostring(updated)==ET.tostring(root)
    destination.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(destination,'w') as dst:
        dst.comment=comment
        for i in infos:dst.writestr(i,final if i.filename==model else payload[i.filename])
    with zipfile.ZipFile(destination) as dst:
        assert dst.testzip() is None and dst.namelist()==list(payload)
        for name in payload:assert dst.read(name)==(final if name==model else payload[name])
    return True
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('input',type=Path); p.add_argument('output',type=Path); a=p.parse_args()
    print('normalized' if normalize(a.input,a.output) else 'already normalized; input left unchanged')
