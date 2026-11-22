from pathlib import Path
from zipfile import ZipFile
import json,struct,sys,collections
from xml.etree import ElementTree as E
import lib3mf
q=Path(sys.argv[1]); ids=set().union(*json.loads((q/'side-face-proof.json').read_text()).values())
old,new=[ZipFile(q/n) for n in ('model.3mf','current.3mf')]
assert old.namelist()==new.namelist()
for n in old.namelist():
 if n!='3D/3dmodel.model':assert old.read(n)==new.read(n)
o,n=[E.fromstring(z.read('3D/3dmodel.model')) for z in (old,new)]
nodes=lambda elem,tag:elem.findall('.//{*}'+tag)
assert len(nodes(o,'object'))==len(nodes(n,'object'))==1
for tag in ('base','vertex','item'):assert [x.attrib for x in nodes(o,tag)]==[x.attrib for x in nodes(n,tag)]
v=[tuple(float(x.attrib[k]) for k in ('x','y','z')) for x in nodes(n,'vertex')]
s=(q/'model.stl').read_bytes()
actual=[]
for i,(a,b,t) in enumerate(zip(nodes(o,'triangle'),nodes(n,'triangle'),struct.iter_unpack('<12fH',s[84:]),strict=True)):
 fa,fb=[tuple(int(k.attrib[f'v{j}']) for j in (1,2,3)) for k in (a,b)]
 assert fa==fb and tuple(v[j] for j in fb)==tuple(t[j:j+3] for j in (3,6,9))
 if i in ids:
    assert a.attrib.get('p1','0')=='0' and b.attrib.get('p1')=='2' and b.attrib['pid']=='1'
 else: assert a.attrib==b.attrib
 actual.append(int(b.attrib.get('p1','0')))
assert collections.Counter(actual)=={0:1401,1:122,2:4351}
w=lib3mf.get_wrapper(); mod=w.CreateModel();r=mod.QueryReader('3mf');r.SetStrictModeActive(True);r.ReadFromFile(str(q/'current.3mf'))
assert r.GetWarningCount()==0
print('PASS same all oriented STL triangle coordinates/order; exact 56 material delta; no geometry or archive member drift; strict lib3mf 2.5.0 zero warnings')
