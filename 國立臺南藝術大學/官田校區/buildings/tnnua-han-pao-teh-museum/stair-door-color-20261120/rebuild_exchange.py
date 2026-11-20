"""Modify only the two targeted face properties in the verified source 3MF."""
from pathlib import Path
import hashlib,json,sys,zipfile,xml.etree.ElementTree as E
P=Path(__file__).resolve().parent
src=Path(sys.argv[1]) if len(sys.argv)>1 else P.parent/'facade-layout-v2/model.3mf';dom=json.loads((P/'domain.json').read_text())
assert hashlib.sha256(src.read_bytes()).hexdigest()==dom['original_appearance_3mf_sha256']
core='3D/3dmodel.model'
with zipfile.ZipFile(src) as z:files={name:z.read(name) for name in z.namelist()}
root=E.fromstring(files[core]); n=root.tag.split('}')[0][1:]; E.register_namespace('',n)
q=root.findall('.//m:triangle',{'m':n}); assert len(q)==1524 and len(dom['ids_actual_3mf_zero_based'])==2
for i in dom['ids_actual_3mf_zero_based']:
 for j in ('p1','p2','p3'):
    assert q[i].get(j)=='0';q[i].set(j,'3')
files[core]=E.tostring(root,encoding='utf-8',xml_declaration=True)
with zipfile.ZipFile(P/'model-colored.3mf','w',zipfile.ZIP_DEFLATED) as z:
 for name,content in files.items():
    info=zipfile.ZipInfo(name,(2026,11,20,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,content)
