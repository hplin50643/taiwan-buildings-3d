from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).resolve().parent/"validate_color.py"),run_name="__main__")
