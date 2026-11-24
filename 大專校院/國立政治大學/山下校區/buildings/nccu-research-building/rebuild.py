"""Rebuild the four native artifacts and five WebPs into a separate new directory."""
import argparse
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from export_display_webp import validate

A=Path(__file__).resolve().parent

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--blender',default='blender')
    p.add_argument('--threads',default='4')
    args=p.parse_args()
    dest=args.output.resolve()
    if dest.exists() or A in dest.parents:
        p.error('Choose a new output directory outside the package')
    core=('model.stl','model.3mf','mesh.json','palette.json')
    with tempfile.TemporaryDirectory(prefix='nccu-native-rebuild-') as tmp:
        stage=Path(tmp)
        (stage/'previews').mkdir();(stage/'qa').mkdir()
        for name in ('build_model.py','render_model.py'):
            shutil.copyfile(A/name,stage/name)
        subprocess.run([sys.executable,str(stage/'build_model.py')],cwd=stage,check=True)
        for name in core:
            if (A/name).read_bytes()!=(stage/name).read_bytes():
                raise ValueError(f'Native rebuild differs: {name}')
        subprocess.run([args.blender,'-b','-t',args.threads,'--python-exit-code','19',
                        '-P',str(stage/'render_model.py')],cwd=stage,check=True)
        output=stage/'display';output.mkdir()
        validate(A,stage,output)
        dest.mkdir()
        shutil.copytree(output,dest/'previews')
        for name in (*core,'scene.blend'):
            shutil.copyfile(stage/name,dest/name)
    print('Native core and all five signed WebPs reproduced; historic raw PNGs checked in temporary staging')

if __name__=='__main__':
    main()
