"""Existing-material extension, preserving historical classifier source bytes."""
from pathlib import Path
import importlib.util,json
import numpy as np
S=Path(__file__).resolve().parent;A=S.parent
sp=importlib.util.spec_from_file_location('historical_build',S/'build_appearance.py');old=importlib.util.module_from_spec(sp);sp.loader.exec_module(old)
original_classify=old.classify
TARGET=[4247,4248,4249,4250]+list(range(4252,4274))
assert len(old.PALETTE)==4 and old.PALETTE[1][1]=='#967F88'
def classify(tri):
 colors,why=original_classify(tri)
 assert len(tri)==5270 and np.bincount(colors).tolist()==[4046,560,456,208]
 assert len(TARGET)==26 and (colors[TARGET]==0).all()
 colors[TARGET]=1;why[TARGET]='bounded_original_upper_gable_existing_mauve_family_approximation'
 assert np.bincount(colors).tolist()==[4020,586,456,208]
 return colors,why
old.classify=classify
if __name__=='__main__':
 old.main();p=A/'palette.json';j=json.loads(p.read_text());j['historical_scope']=j['scope'];j['scope']='Historical four-material assignments preserved; 26 complete original upper front-gable faces additionally use existing dusty mauve brick-family approximation. Original linking-bay cut removes the lower gable and opens the circular cut into a notch: no complete real gable or enclosed oculus is reconstructed. Gray rim, curved border, louver and exact proportions are absent. No side/back/underside/other tower extension or calibrated material claim.';p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
