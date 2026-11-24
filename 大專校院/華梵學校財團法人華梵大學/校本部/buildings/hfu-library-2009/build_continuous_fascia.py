from pathlib import Path
import subprocess,sys
R=Path(__file__).resolve().parent
for n in ['colorize_continuous_fascia.py','export_continuous_fascia.py']:subprocess.run([sys.executable,str(R/n)],check=True)
