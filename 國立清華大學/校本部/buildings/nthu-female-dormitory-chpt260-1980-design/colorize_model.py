"""Only twelve complete historic apron front domains change material7 to designwhite0."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib,zipfile,xml.etree.ElementTree as E
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='509024f81f6f07eb86c0d45a53127465b26719188f50e83c4f052ecc1058fb0b';assert H(R/'model.stl')==expected
B=R/'original-version' if (R/'original-version').exists() else R
d=np.load(B/'mesh.npz');v=d['vertices'];f=d['faces'];old=d['materials'].astype(np.int32);a=old.copy();m=trimesh.Trimesh(v,f,process=False);t=m.triangles;n=m.face_normals;assert len(f)==23818
if (B/'model.3mf').exists():
 with zipfile.ZipFile(B/'model.3mf') as z:e=E.fromstring(z.read('3D/3dmodel.model'))
 ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'};vv=np.array([[float(x.attrib[k])for k in ['x','y','z']]for x in e.findall('.//m:vertex',ns)]);ff=np.array([[int(x.attrib[k])for k in ['v1','v2','v3']]for x in e.findall('.//m:triangle',ns)]);ma=np.array([int(x.attrib['p1'])for x in e.findall('.//m:triangle',ns)])
 assert np.array_equal(ff,f) and np.array_equal(ma,old) and np.allclose(vv,v,atol=1e-7,rtol=0)
ids=np.flatnonzero(np.abs(t[:,:,1]-38.8).max(1)<1e-5);assert len(ids)==24 and (old[ids]==7).all()
D={};chosen=[]
for row,z in enumerate([5.75,20.75]):
 for i in range(6):
  cx=(5.4+i*3.6-27)*5;sel=ids[((t[ids,:,0]>=cx-4-1e-5)&(t[ids,:,0]<=cx+4+1e-5)&(t[ids,:,2]>=z-1e-5)&(t[ids,:,2]<=z+3.25+1e-5)).all(1)];assert len(sel)==2 and abs(m.area_faces[sel].sum()-26)<.001
  D[f'north_left_apron_row{row+1}_bay{i+1}']=sel.tolist();chosen.extend(sel)
assert set(chosen)==set(ids);a[ids]=0;assert np.flatnonzero(a!=old).tolist()==ids.tolist()
ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999;cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1)
# Preserve historical color-boundaries; newly white domains must be complete components.
selected=set(ids)
for c in cs:
 if selected.intersection(c):assert set(c).issubset(selected) and len(c)==2
pal=json.loads((B/'palette.json').read_text());assert len(pal)==8 and pal[0][1]=='#D1D1C7'
np.savez_compressed(R/'color-mesh.npz',vertices=v,faces=f,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':D,'changed_face_count':24,'material_transition':'Exactly24 originalmaterial7 to0; all other original8-family assignments unchanged and not newly certified.','coplanar_components':len(cs),'selected_coplanar_components':12,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'23818 original triangles unchanged','limits':['1980designwhite not asbuilt/current; original otherfamilies remain historical illustrations.','Single two-courtyard building; current name unverified.','Originalwindow1.6vs2.6/R44/unknownwaterbox/printlimits retained.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':23818,'changed_faces':24,'all_other_material_assignments_unchanged':True,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],len(cs))
