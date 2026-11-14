"""Execute unchanged native renderer, preserve its historical report bytes."""
from pathlib import Path
import runpy
S=Path(__file__).resolve().parent; A=S.parent
p=A/'qa/render-manifest.json'; saved=p.read_bytes() if p.exists() else None
try:
 runpy.run_path(str(S/'render_appearance.py'),run_name='__main__')
 current=p.read_bytes();(A/'qa/current-render-manifest.json').write_bytes(current)
finally:
 if saved is not None:p.write_bytes(saved)
 elif p.exists():p.unlink()
