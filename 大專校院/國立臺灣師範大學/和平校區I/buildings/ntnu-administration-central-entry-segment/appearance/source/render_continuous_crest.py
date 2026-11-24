from pathlib import Path
S=Path(__file__).resolve().parent;p=S/'render_appearance.py'
text=p.read_text().replace('qa/render-manifest.json','qa/continuous-crest-render-manifest.json')
exec(compile(text,str(p),'exec'),{'__file__':str(p),'__name__':'__main__'})
