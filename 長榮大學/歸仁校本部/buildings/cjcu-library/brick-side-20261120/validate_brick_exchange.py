"""Validate exported topology, bounded materials and strict 3MF edit round trip in a private work dir."""
from pathlib import Path
import sys,json,hashlib,numpy as np,lib3mf,zipfile,xml.etree.ElementTree as ET
P,Q=map(Path,sys.argv[1:]);Q.mkdir(exist_ok=True,parents=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
n=np.load(P/'color-mesh.npz');v,f,a=(n[x] for x in ('vertices','faces','materials'));dom=json.loads((P/'verified-face-domain.json').read_text())
assert len(v)==1953 and len(f)==3942 and np.bincount(a).tolist()==[3850,92] and np.flatnonzero(a).tolist()==dom['ids']
t=np.frombuffer((P/'model.stl').read_bytes(),offset=84,dtype=[('n','<f4',(3,)),('v','<f4',(3,3)),('a','<u2')])['v'];assert np.array_equal(t,v[f])
with zipfile.ZipFile(P/'appearance.3mf') as z:
 assert z.testzip() is None
 x=ET.fromstring(z.read('3D/3dmodel.model'))
ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
vt=x.findall('.//m:vertex',ns);tt=x.findall('.//m:triangle',ns)
assert np.array_equal(np.array([[float(q.get(k)) for k in 'xyz'] for q in vt]),v)
assert np.array_equal(np.array([[int(q.get('v'+str(k))) for k in (1,2,3)] for q in tt]),f)
assert np.array_equal(np.array([[int(q.get('p'+str(k))) for k in (1,2,3)] for q in tt]),np.repeat(a[:,None],3,axis=1))
w=lib3mf.get_wrapper()
def read(path):
 m=w.CreateModel();r=m.QueryReader('3mf');r.SetStrictModeActive(True);r.ReadFromFile(str(path));assert r.GetWarningCount()==0
 it=m.GetMeshObjects();assert it.MoveNext();o=it.GetCurrentMeshObject();assert not it.MoveNext();assert o.IsValid() and o.IsManifoldAndOriented()
 it=m.GetBaseMaterialGroups();assert it.MoveNext();g=it.GetCurrentBaseMaterialGroup();props=g.GetAllPropertyIDs();assert len(props)==2 and not it.MoveNext()
 uv=np.array([list(x.Coordinates) for x in o.GetVertices()]);uf=np.array([list(x.Indices) for x in o.GetTriangleIndices()]);up=np.array([list(x.PropertyIDs) for x in o.GetAllTriangleProperties()])
 pal=[(g.GetName(i),[getattr(g.GetDisplayColor(i),q) for q in ('Red','Green','Blue','Alpha')]) for i in props];return m,g,props,uv,uf,up,pal
orig=sha(P/'appearance.3mf');m,g,props,uv,uf,up,pal=read(P/'appearance.3mf')
assert np.array_equal(uv,v) and np.array_equal(uf,f) and np.array_equal(up,np.array(props)[np.repeat(a[:,None],3,axis=1)])
c=g.GetDisplayColor(props[1]);c.Blue=(c.Blue+19)%256;g.SetDisplayColor(props[1],c);tmp=Q/'private-sdk-edited.3mf';m.QueryWriter('3mf').WriteToFile(str(tmp))
_,_,_,rv,rf,rp,rpal=read(tmp);delta=float(np.max(abs(rv-uv)))
assert delta<.00002 and np.array_equal(rf,uf) and np.array_equal(rp,up) and [i for i,(x,y) in enumerate(zip(pal,rpal)) if x!=y]==[1]
assert sha(P/'appearance.3mf')==orig
out=dict(status='PASS',vertices=len(v),triangles=len(f),count_by_material=[3850,92],original_triangle_coordinates_and_order_exact=True,xml_three_corner_materials_exact=True,strict_sdk_zero_warnings=True,private_sdk_palette_edit_roundtrip=True,roundtrip_coordinate_max_mm=delta,public_3mf_sha256=orig)
(Q/'exchange-review.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
