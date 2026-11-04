"""Rebuild from numeric parameters only. Existing mesh/scene inputs are never copied.
Python3+NumPy, Blender4.3.2; no network. OUTPUT must be a new directory.
"""
from pathlib import Path
import argparse,json,shutil,subprocess,sys,hashlib,os
ROOT=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('output',type=Path);p.add_argument('--skip-render',action='store_true');a=p.parse_args();out=a.output.resolve();out.mkdir(parents=True,exist_ok=False)
shutil.copytree(ROOT/'generators',out/'generators');(out/'inputs').mkdir();(out/'parts').mkdir()
shutil.copy2(ROOT/'inputs/reference-baselines.json',out/'inputs/reference-baselines.json')
for name in ['build_scene.py','export_3mf.py','caption_previews.py','sanitize_metadata.py']:shutil.copy2(ROOT/name,out/name)
env=os.environ.copy();env['BLENDER_USER_CONFIG']=str(out/'blender-config')
def run(cmd,log):
 with (out/log).open('w')as f:subprocess.run(cmd,check=True,stdout=f,stderr=subprocess.STDOUT,env=env)
run([sys.executable,str(out/'generators/orthogonal/generate_orthogonal.py'),'--output',str(out/'rebuilt-orthogonal')],'orthogonal.log')
run(['blender','-b','--factory-startup','--disable-autoexec','--python',str(out/'generators/curved/build_curved_v7.py'),'--',str(out/'rebuilt-curved')],'curved.log')
objects=[];bindings=[]
for f in sorted((out/'rebuilt-orthogonal').glob('*.mesh.json')):
 if '.reference64.'in f.name:continue
 d=json.loads(f.read_text());objects.append({'id':d['id'],'vertices_mm':d['vertices'],'triangles':d['triangles']});bindings.append({'id':d['id'],'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
f=out/'rebuilt-curved/geometry.json'
for d in json.loads(f.read_text())['objects']:
 objects.append({'id':d['id'],'vertices_mm':d['vertices_mm'],'triangles':d['triangles']});bindings.append({'id':d['id'],'geometry_file_sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
(out/'inputs/physical-meshes.json').write_text(json.dumps({'units':'model millimetres','scale':'1:800; world metres ×1.25','objects':objects,'bindings':bindings},separators=(',',':'))+'\n')
for f in list((out/'rebuilt-orthogonal').glob('*.stl'))+list((out/'rebuilt-curved').glob('*.stl')):shutil.copy2(f,out/'parts'/f.name)
run([sys.executable,str(out/'export_3mf.py')],'3mf.log')
if not a.skip_render:
 run(['blender','-b','--factory-startup','--disable-autoexec','--python',str(out/'build_scene.py')],'scene.log')
 run([sys.executable,str(out/'caption_previews.py')],'captions.log')
 run([sys.executable,str(out/'sanitize_metadata.py')],'hygiene.log')
report={'only_generators_and_small_numeric_inputs_supplied':True,'parts':{},'geometry_records_exact':json.loads((ROOT/'inputs/physical-meshes.json').read_text())['objects']==objects,'three_mf_byte_exact':(ROOT/'assembly.3mf').read_bytes()==(out/'assembly.3mf').read_bytes()}
for f in sorted((out/'parts').glob('*.stl')):report['parts'][f.name]={'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'byte_exact':f.read_bytes()==(ROOT/'parts'/f.name).read_bytes()}
if not a.skip_render:
 from PIL import Image
 report['render_rgba_exact']={f.name:Image.open(f).convert('RGBA').tobytes()==Image.open(ROOT/'previews'/f.name).convert('RGBA').tobytes()for f in (out/'previews').glob('*.png')}
(out/'FULL-EMPTY-DIRECTORY-REBUILD-REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
assert report['geometry_records_exact']and report['three_mf_byte_exact']and all(x['byte_exact']for x in report['parts'].values())
if not a.skip_render:assert all(report['render_rgba_exact'].values())
