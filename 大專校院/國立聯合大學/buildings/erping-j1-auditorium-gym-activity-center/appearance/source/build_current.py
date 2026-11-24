from pathlib import Path
import importlib.util,json
import numpy as np
S=Path(__file__).resolve().parent;A=S.parent
sp=importlib.util.spec_from_file_location('historical_build',S/'build_appearance.py');old=importlib.util.module_from_spec(sp);sp.loader.exec_module(old)
original_classify=old.classify;assert len(old.PALETTE)==7
old.PALETTE.append(('lowest_arc_riser_warm_approximation','#A99B86'))
TARGET=[167, 169, 170, 171, 175, 176, 177, 182, 184, 185, 188, 189, 190, 192, 193, 194, 203, 204, 206, 209, 210, 211, 215, 216, 218, 221, 222, 224, 227, 228, 229, 230, 231, 232, 233, 234, 236, 238, 239, 241, 251, 252, 254, 257, 258, 259, 263, 264, 265, 267, 268, 269, 273, 274, 275, 277, 278, 279, 284, 286, 288, 291, 294, 296, 300, 302, 303, 307, 310, 312, 314, 317, 319, 322, 323, 324, 328, 329, 330, 333, 334, 335, 338, 339, 341, 343, 345, 347, 348, 351, 352, 354, 356, 357, 358, 360, 361, 362, 363, 364, 372, 374, 375, 378, 381, 382, 383, 385, 386, 390, 392, 394, 397, 400, 401, 403, 404, 405, 409, 411, 413, 415, 417, 419, 421, 422, 425, 428]
def classify(tri):
 colors,why=original_classify(tri);assert len(tri)==16168 and np.bincount(colors).tolist()==[3348, 10709, 328, 242, 124, 2, 1415]
 assert (colors[TARGET]==0).all();colors[TARGET]=7;why[TARGET]='bounded_J1_lowest_arc_riser_background'
 assert np.bincount(colors).tolist()==[3220, 10709, 328, 242, 124, 2, 1415, 128];return colors,why
old.classify=classify
if __name__=='__main__':
 old.main();p=A/'palette.json';j=json.loads(p.read_text());j['historical_scope']=j['scope'];j['scope']='只原最低i0完整弧前立64平面/128三角作暖褐背景近似，排踏面/側端/底/上六級及其餘構件；不稱逐級測繪或材種測色。 source4原pixelcrop和source3/4完整1600可辨暖褐前立與淺米踏面，左塔/車輛錐筒局部遮端僅同一原弧構件有限延續，不能聲稱全域直接實見；source0/1/2為同棟補充，非獨立交叉測色。 原七粗級、64分段弧與真實級數/曲率/鼻緣細分不同；不修原幾何，右實轉階/坡道不延色。原塔對原最低弧不相交，照片塔遮影不等模型切除。 原step底2.3被base頂2.4扣，選域至2.95；最小原塔淨空2.256984mm，右terrace與原弧無交。每平面全三角雙向支承有非零浮點差，詳candidate，不聲稱全零。 五張當次官方1920×1280全部GET200，逐張完整1600及source4原像素700×280裁圖/nativefront親看；舊README第五圖失敗是歷史，本次已成功，不改原歷史。 EXIF各欄由當次公開來源原件讀取；無相應Originaloffset時不可借Digitized或OffsetTime，不認證拍攝日期或2026現況。 40原件、root17/app21及ZIP6同樹、16168面7shader/native4CPU48已依本案核；原geometry/STL/order/七shader/歷史QA與README保持。 僅26可讀完成/HOLDprefix精確排重，缺失舊索引不稱全庫核完；新案私人來源審核不公開，不改凍包/index或發布。';p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
