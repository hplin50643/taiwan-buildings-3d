"""Build deterministic continuation exchange assets, preserving canonical mesh tokens."""
import struct,sys,hashlib,json,zipfile,xml.etree.ElementTree as E
from pathlib import Path
R=Path(__file__).resolve().parent
BASE=Path(sys.argv[1]).resolve(); D=Path(sys.argv[2]).resolve();D.mkdir(exist_ok=True)
N='http://schemas.microsoft.com/3dmanufacturing/core/2015/02'
E.register_namespace('',N);app=BASE/'appearance'
old=app/'cyut-poding-library-appearance.3mf'
src=hashlib.sha256((BASE/'model.stl').read_bytes()).hexdigest()
assert src=='caac8ffd529735147d3004e1477b9f5da4ffb8b5d3dd3481242b3ec78b9e16c9'
fmap=json.loads((app/'face-materials.json').read_text());indices=fmap['face_material_indices']
assert fmap['source_stl_sha256']==src and (len(indices),indices.count(0),indices.count(1),indices.count(2))==(7254,6816,316,122)
domain=json.loads((R/'domain-core.json').read_text())[0]['faces']
assert len(domain)==45 and all(indices[i]==0 for i in domain)
name='CYUT setback wall cool gray stone-like proxy';hexcolor='#B5BABB'
with zipfile.ZipFile(old) as a:
  root=E.fromstring(a.read('3D/3dmodel.model'));mats=root.find('.//{*}basematerials')
  assert [x.get('displaycolor') for x in mats]==['#AAA79FFF','#667F87FF','#9CABABFF']
  E.SubElement(mats,'{'+N+'}base',name=name,displaycolor=hexcolor+'FF')
  ts=root.findall('.//{*}triangle');assert len(ts)==7254
  for i,tr in enumerate(ts):
    assert tr.get('pid')==mats.get('id') and all(int(tr.get(k,tr.get('p1')))==indices[i] for k in ['p1','p2','p3'])
  for i in domain:
    for k in ['p1','p2','p3']:ts[i].set(k,'3')
    indices[i]=3
    fmap['face_reasons'][i]='Full connected original upper setback wall plane, excluding window holes. Nominal cool gray not calibrated.'
  with zipfile.ZipFile(D/'appearance.3mf','w',zipfile.ZIP_DEFLATED) as b:
    for k in a.namelist():
      ii=zipfile.ZipInfo(k,(2026,11,20,0,0,0));ii.compress_type=zipfile.ZIP_DEFLATED
      b.writestr(ii,E.tostring(root,encoding='utf-8',xml_declaration=True) if k=='3D/3dmodel.model' else a.read(k))
(D/'face-materials.json').write_text(json.dumps(fmap,indent=2,ensure_ascii=False)+'\n')
pal=json.loads((app/'palette.json').read_text())
pal['materials'].append(dict(id=name,srgb=hexcolor))
pal['scope']='Preserve all 438 prior colored window backs; add 45 cool-gray setback exterior wall triangles; retain 6771 neutral. No geometry change.'
pal['colors']+=' Added independent approximate cool gray from official oblique photo and ground VR, not measured.'
(D/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
