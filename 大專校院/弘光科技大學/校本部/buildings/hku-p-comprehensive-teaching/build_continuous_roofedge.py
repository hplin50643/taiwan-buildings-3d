from pathlib import Path
import subprocess,sys
R=Path(__file__).resolve().parent
for n in ['colorize_continuous_roofedge.py','export_continuous_roofedge.py']:subprocess.run([sys.executable,str(R/n)],check=True)
