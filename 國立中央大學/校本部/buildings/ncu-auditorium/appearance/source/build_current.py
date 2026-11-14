"""Current bounded rim-only appearance; historical classifier remains unchanged."""
from pathlib import Path
import importlib.util,json
import numpy as np
S=Path(__file__).resolve().parent;A=S.parent
sp=importlib.util.spec_from_file_location('historical_build',S/'build_appearance.py');old=importlib.util.module_from_spec(sp);sp.loader.exec_module(old)
original_classify=old.classify
TARGET=[9178, 9179, 9181, 9187, 9192, 9195, 9201, 9202, 9204, 9208, 9209, 9215, 9216, 9225, 9226, 9233, 9235, 9240, 9241, 9244, 9245, 9248, 9250, 9253, 9255, 9267, 9270, 9271, 9276, 9278, 9285, 9292, 9293, 9298, 9300, 9304, 9310, 9311, 9322, 9327, 9329, 9334, 9342, 9343, 9348, 9350, 9364, 9365, 9373, 9376, 9382, 9383, 9388, 9390, 9392, 9398, 9403, 9404]
assert len(old.PALETTE)==4
old.PALETTE=old.PALETTE+[('upper_outer_rim_gray_white_background_approximation','#CDCEC5')]
def classify(tri):
 colors,why=original_classify(tri)
 assert len(tri)==9614 and np.bincount(colors).tolist()==[2378, 1056, 6028, 152]
 assert len(TARGET)==58 and (colors[TARGET]==0).all()
 colors[TARGET]=4;why[TARGET]='complete_negative_y_outer_upper_rim_gray_white_background_only'
 assert np.bincount(colors).tolist()==[2320, 1056, 6028, 152, 58]
 return colors,why
old.classify=classify
if __name__=='__main__':
 old.main();p=A/'palette.json';j=json.loads(p.read_text());j['historical_scope']=j['scope'];j['scope']='Only58 complete negative-y uppermost outer rim facets additionally receive gray-white background approximation. Original four shaders and other9556 faces unchanged. Original thick rim, polygon tessellation and unmodeled joints are not measured construction. Top, inner, bottom, positive-y, ends and full-height walls excluded.';p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
