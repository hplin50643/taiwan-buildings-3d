from pathlib import Path
import subprocess,sys
R=Path(__file__).resolve().parent
for n in ['colorize_continuous_ribbon.py','export_continuous_ribbon.py']:subprocess.run([sys.executable,str(R/n)],check=True)
