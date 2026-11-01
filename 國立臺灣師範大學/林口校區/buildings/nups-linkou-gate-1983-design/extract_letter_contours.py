"""Optional regenerate neutral text contours from installed NotoSansCJKBoldTC. Fontnotcopied."""
from fontTools.ttLib import TTFont
from fontTools.pens.basePen import BasePen
from pathlib import Path
import json
font=TTFont('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',fontNumber=3);gs=font.getGlyphSet();cm=font.getBestCmap()
class Pen(BasePen):
 def __init__(self):super().__init__(gs);self.paths=[];self.p=[]
 def _moveTo(self,p):self.p=[p]
 def _lineTo(self,p):self.p.append(p)
 def _curveToOne(self,a,b,c):
  d=self._getCurrentPoint()
  for i in range(1,13):
   t=i/12;self.p.append(tuple((1-t)**3*d[k]+3*(1-t)**2*t*a[k]+3*(1-t)*t*t*b[k]+t**3*c[k] for k in [0,1]))
 def _qCurveToOne(self,a,b):
  d=self._getCurrentPoint()
  for i in range(1,13):
   t=i/12;self.p.append(tuple((1-t)**2*d[k]+2*(1-t)*t*a[k]+t*t*b[k] for k in [0,1]))
 def _closePath(self):self.paths.append(self.p);self.p=[]
 def _endPath(self):self._closePath()
res={}
for ch in '國立僑生大學先修班':
 p=Pen();gs[cm[ord(ch)]].draw(p);pts=[v for q in p.paths for v in q];lo=[min(v[k] for v in pts) for k in [0,1]];hi=[max(v[k] for v in pts) for k in [0,1]]
 res[ch]=[[[(v[k]-lo[k])/(hi[k]-lo[k])*.8 for k in [0,1]] for v in q] for q in p.paths]
Path(__file__).with_name('letter-contours.json').write_text(json.dumps(res,ensure_ascii=False))
