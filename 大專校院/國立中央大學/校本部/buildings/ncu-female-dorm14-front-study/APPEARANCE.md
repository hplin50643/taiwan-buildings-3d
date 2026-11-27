# 中央女14舍入口局部｜狹長窗槽返邊補色 v2

## 本次改動

僅補色原有58個狹長窗槽的頂、底、左、右實體返邊，共464個原先中性的三角面，沿用既有淺灰青色材料。116個暗色槽背、所有4209個原有色面，以及9種材料的RGBA與粗糙度完全不變。不新增文字、孔洞、窗框、接縫、裝飾或透明玻璃。

每個返邊均以原開口的完整矩形支撐面判定；全三角面的3個頂點均須位於正確平面與原切槽界限內，並驗證完整面積。不是只看面心，不把跨材料三角面隨意切成斜色塊。

## 實照與推論分開

已重新實際閱讀[校方入口原照片](https://shsd.ncu.edu.tw/uploads/images/S__49291284.jpg)，[官方宿舍相簿](https://shsd.ncu.edu.tw/Dormitory)為原身份來源。照片直接可見淺灰青磁磚框／牆與狹長暗槽；本次把同一外牆實體的小返邊沿用淺灰青，屬同構件材料延續推論，並非隱藏返邊已逐一實測。照片拍攝日期不明，不宣稱2026現況。來源照片不隨公開模型發布。

照片中的低雨棚同時有綠色半透明板及紅色細框，原模型並無完整分件，不能直接把全部薄邊與底面刷成綠色。因此雨棚不修改；原綠色上面仍是不透明近似。拱框與前柱可辨識面本已完整著色，也不重塗。

這是入口局部量體研究，不是全棟模型。人工後平切、兩端截面、屋頂、粗化正面空白、入口深處及底座維持原色，仍有1441個中性面。2008年另一面照片未配準到本模型，不用它猜造或補色後立面。

## 幾何與材質保留

原3005個頂點／6114個三角面、150×83×122.8mm尺寸與transform逐項不變。STL、OBJ、scene.blend、build_model.py、原三圖與原幾何QA不替換。新版appearance.blend／appearance.3mf使用同一原頂點及三角面，不拆分、不重採樣。

原有 appearance-review 保留為 v1 歷史。目前外觀範圍沿用 [color-v2 原發布凍結](https://github.com/hplin50643/taiwan-buildings-3d/tree/d6b2917d55633c7b4baa02842f33998513c1cf61/%E5%A4%A7%E5%B0%88%E6%A0%A1%E9%99%A2/%E5%9C%8B%E7%AB%8B%E4%B8%AD%E5%A4%AE%E5%A4%A7%E5%AD%B8/%E6%A0%A1%E6%9C%AC%E9%83%A8/buildings/ncu-female-dorm14-front-study/appearance-freeze.json)；[現行展示與像素校驗](display/render-proof.json)使用無失真 WebP，原彩色 PNG 仍可在[固定版本](https://github.com/hplin50643/taiwan-buildings-3d/tree/d6b2917d55633c7b4baa02842f33998513c1cf61/%E5%A4%A7%E5%B0%88%E6%A0%A1%E9%99%A2/%E5%9C%8B%E7%AB%8B%E4%B8%AD%E5%A4%AE%E5%A4%A7%E5%AD%B8/%E6%A0%A1%E6%9C%AC%E9%83%A8/buildings/ncu-female-dorm14-front-study/appearance)查閱。現行補色審核見 [appearance-review-v2](appearance-review-v2/color-continuity-review.json)。[幾何與材質驗證](appearance-review-v2/model-verification.json)、[邊界與58槽檢查](appearance-review-v2/boundary-continuity-audit.json)、[來源區分](appearance-review-v2/source-register.json)、[乾淨重建](appearance-review-v2/clean-rebuild-equality.json)與[相機一致性](appearance-review-v2/camera-consistency.json)可核對。

## 可重現與渲染

Blender4.3.2：`blender -b -t 1 --python-exit-code 1 -P build_appearance.py`。原scene.blend與model.stl置於同目錄，無需來源照片。CyclesCPU、96samples、seed0、單執行緒、關閉降噪，900×800。七個新角度及兩個原色同相機比較皆由實際模型渲染並逐張檢視。原始重建輸出 PNG 無文字 metadata；新BLEND無文字物件、來源圖片、外部連結或絕對本機路徑，輸出路徑採相對路徑。

獨立乾淨目錄重建後，3MF與材料JSON逐byte相同；BLEND幾何、transform、每面材料、RGBA與粗糙度語義相同。彩色3MF無指定AMS映射。

原估計尺寸、局部範圍及列印限制不變。高牆、細框、拱圈、入口橋、低簷需支撐／橋接與移除性評估；未做實體試印或新增正式切片。幾何保留不等於免支撐或保證可印。

以 Python（Pillow）和 Blender 4.3.2 執行 `python verify_display.py --rebuild` 可在暫存重繪七張；重新生成的 PNG 以解碼像素核對，不改動現行模型、圖片或校驗檔。

技術審核中的 PNG 檔名與雜湊保留當時紀錄：[v1 固定發布](https://github.com/hplin50643/taiwan-buildings-3d/tree/a082f159f0855aaed589a9c04a115586ffae888e/%E5%9C%8B%E7%AB%8B%E4%B8%AD%E5%A4%AE%E5%A4%A7%E5%AD%B8/%E6%A0%A1%E6%9C%AC%E9%83%A8/buildings/ncu-female-dorm14-front-study/appearance)及 [v2 固定發布](https://github.com/hplin50643/taiwan-buildings-3d/tree/d6b2917d55633c7b4baa02842f33998513c1cf61/%E5%A4%A7%E5%B0%88%E6%A0%A1%E9%99%A2/%E5%9C%8B%E7%AB%8B%E4%B8%AD%E5%A4%AE%E5%A4%A7%E5%AD%B8/%E6%A0%A1%E6%9C%AC%E9%83%A8/buildings/ncu-female-dorm14-front-study/appearance)。原色同相機比較與原三張中性幾何驗證圖仍留在現行套件，不列入最新彩色圖廊。
