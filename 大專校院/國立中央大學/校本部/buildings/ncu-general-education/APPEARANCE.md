# 國立中央大學綜教館｜有限外側回折補色

## 範圍與材料證據

以官方[校友通訊第85期第2頁](https://in.ncu.edu.tw/alumni/enews/no85/page2.pdf)外照核對：灰綠圓角梯核、粉灰懸出教學翼、淺灰框／薄簷、暗灰綠凹窗。照片日期未知，非測色、非2026現況認證。本次實際讀取PDF並查看第一頁外照及下方內院照；原無障礙內院照片網址回應503，未把它列作本次成功讀取證據。

只把原材質0中、可辨識為同一構件的梯核左外側與圓角前緣、上前翼右側短回折、既有薄簷兩側緣，換為既有材料1／2／3。原已著色面完全不變；原材料的RGBA、節點Base Color及roughness完全不變，不新增材質。外側延伸是依同構件連續性的近似，不宣稱有每一面同角度照片。

補查校方[校園災害防救計畫第 2-11 頁（PDF 第 16 頁）](https://military.ncu.edu.tw/download/112_0008_%E6%A0%A1%E5%9C%92%E7%81%BD%E5%AE%B3%E9%98%B2%E6%95%91%E8%A8%88%E7%95%AB%E6%9B%B8-%E6%9C%AC%E6%96%87-112.3.28.pdf#page=16)的綜教館斜前外照：可區分灰色梯核、粉灰前翼及相鄰淺灰框帶。畫面未拍到主體背向，也無法把內院材料定位到原模型的實心簡化面，因此不改現行配色。圖冊調查日期不等於照片拍攝日期。

## 大背面保留中性的原因

官方PDF同頁內院照直接顯示紅磚內院，有材料分區證據；但原幾何只把後深度做成實心簡化塊，沒有對應內院與環狀走廊，所以無法把每一個背面對應到真實粉灰外牆、紅磚內院或人工終止面。不能以人工簡化面冒充外牆，也不能把紅磚泛套全部側後。主體右外側、後終止面、核心後面、屋頂、底座與其他未辨識面仍中性。這是限域補色，不是全館外觀補色完成。

## 不變與限制

446頂點、896三角面、150×100×70.8mm、transform、STL與scene.blend保留；不新增窗陣、磚縫、細橫帶、內院、任何幾何。窗仍是不透明色塊代理。原模型尺寸未測繪、背深度簡化及原切片檢查限制延續，未實體試印。

## 重建與檢查

同目錄保留原scene.blend與model.stl，Blender4.3.2執行：

    blender -b -t 1 --python-exit-code 1 -P build_appearance.py

產生7角度實網格渲染，96 samples、denoise=False、無stamp／文字／PNG文字metadata；相機名稱不是地理方位。3MF逐頂點、逐面頂點順序、每面材料與BLEND核對，原材料全值及已著色面檢查見appearance-review-v2。

原 appearance-review 保留為 v1 歷史，不覆寫原審核。配色範圍沿用 [color-v2 原發布凍結](https://github.com/hplin50643/taiwan-buildings-3d/tree/d1263d958a5073dbcae7f4a0798c47b4555efae8/%E5%A4%A7%E5%B0%88%E6%A0%A1%E9%99%A2/%E5%9C%8B%E7%AB%8B%E4%B8%AD%E5%A4%AE%E5%A4%A7%E5%AD%B8/%E6%A0%A1%E6%9C%AC%E9%83%A8/buildings/ncu-general-education/appearance-freeze.json)，現行公開圖檔與像素校驗見 [WebP 渲染對照](display/render-proof.json)。

照片/PDF不隨公開包；渲染不是實景照片。沒有指定耗材或AMS映射，切片器支援需另核對。

以 Python（Pillow）和 Blender 4.3.2 執行 `python verify_display.py --rebuild` 可在暫存重繪七張；重新生成的 PNG 以解碼像素核對，不改動現行模型、圖片或校驗檔。

技術審核中的 PNG 檔名與雜湊保留當時紀錄：[v1 固定發布](https://github.com/hplin50643/taiwan-buildings-3d/tree/e6b27b66bfd1c4607cb9c63d002d482ffe8c6c40/%E5%9C%8B%E7%AB%8B%E4%B8%AD%E5%A4%AE%E5%A4%A7%E5%AD%B8/%E6%A0%A1%E6%9C%AC%E9%83%A8/buildings/ncu-general-education/appearance)及 [v2 固定發布](https://github.com/hplin50643/taiwan-buildings-3d/tree/d1263d958a5073dbcae7f4a0798c47b4555efae8/%E5%A4%A7%E5%B0%88%E6%A0%A1%E9%99%A2/%E5%9C%8B%E7%AB%8B%E4%B8%AD%E5%A4%AE%E5%A4%A7%E5%AD%B8/%E6%A0%A1%E6%9C%AC%E9%83%A8/buildings/ncu-general-education/appearance)。審核用的原新同鏡位對照與原三張中性幾何驗證圖仍留在現行套件，不列入最新彩色圖廊。
