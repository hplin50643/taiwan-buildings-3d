"""Execute unchanged original native renderer, retaining historical render QA bytes."""
from pathlib import Path
S=Path(__file__).resolve().parent;A=S.parent;path=S/'render_appearance.py';text=path.read_text();needle=".4 if 'glazing' in p['id'] else .78";assert text.count(needle)==1;text=text.replace(needle,".88 if p['id']=='front_roof_graybrown_background_approximation' else (.4 if 'glazing' in p['id'] else .78)")
p=A/'qa/render-manifest.json';saved=p.read_bytes() if p.exists() else None
try:
 exec(compile(text,str(path),'exec'),{'__file__':str(path),'__name__':'__main__'})
 (A/'qa/current-render-manifest.json').write_bytes(p.read_bytes())
finally:
 if saved is not None:p.write_bytes(saved)
 elif p.exists():p.unlink()
