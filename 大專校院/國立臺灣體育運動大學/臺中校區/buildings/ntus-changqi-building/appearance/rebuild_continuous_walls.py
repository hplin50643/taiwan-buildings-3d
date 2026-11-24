from pathlib import Path
import subprocess,sys
A=Path(__file__).resolve().parent
for n in ['build_continuous_walls.py','export_continuous_walls.py']:subprocess.run([sys.executable,str(A/n)],check=True)
