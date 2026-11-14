"""Keep native renderer bytes; add only the new sixth shader's .88 roughness."""
from pathlib import Path
S=Path(__file__).resolve().parent;A=S.parent
path=S/'render_appearance.py';text=path.read_text()
a=".4 if 'glazing' in p['id'] else .78"
b=".88 if p['id']=='AB_crown_light_khaki_background_approximation' else (.4 if 'glazing' in p['id'] else .78)"
assert text.count(a)==1;text=text.replace(a,b);compile(text,str(path),'exec')
p=A/'qa/render-manifest.json';saved=p.read_bytes() if p.exists() else None
try:
 exec(compile(text,str(path),'exec'),{'__file__':str(path),'__name__':'__main__'})
 (A/'qa/current-render-manifest.json').write_bytes(p.read_bytes())
finally:
 if saved is not None:p.write_bytes(saved)
 elif p.exists():p.unlink()
