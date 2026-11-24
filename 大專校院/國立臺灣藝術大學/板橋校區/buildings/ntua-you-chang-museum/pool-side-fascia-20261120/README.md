# 有章藝術博物館舊行政大樓改造館｜水池側簷帶補色

現版為同一座舊行政大樓改造館，只改水池側既有簷帶兩面。請看[現版五視角](../README.md)與[現版校驗](../PUBLIC-MODEL-SHA256SUMS)；[診斷前後原圖及原發布說明](https://github.com/hplin50643/taiwan-buildings-3d/blob/5018bb0b9c8fd679e1155e09afd8814e9dc88166/%E5%9C%8B%E7%AB%8B%E8%87%BA%E7%81%A3%E8%97%9D%E8%A1%93%E5%A4%A7%E5%AD%B8/%E6%9D%BF%E6%A9%8B%E6%A0%A1%E5%8D%80/buildings/ntua-you-chang-museum/pool-side-fascia-20261120/README.md)留在歷史版本作 QA，不在現版畫廊展示。

[現版 3MF](model-colored.3mf) · [可編輯 Blender](scene.blend) · [相同幾何 STL](../model.stl) · [現版渲染證據](../render-proof.json)

## 歷史參照與範圍

[館方水池側照片](https://museum.ntua.edu.tw/upfiles/HF5/DSC05978.jpg) 可見無外梯的長側門窗上方有一條連續灰簷帶。樹枝、樹叢遮住兩端小段；這些短段是依同一連續構件作局部延伸，並非獨立照片證明。[館方外梯側照片](https://museum.ntua.edu.tw/upfiles/HF5/04.jpg) 只用來辨認構件和方向，不支持改另一側。照片 EXIF 分別自報 **2007-11-01** 與 **2007-10-24**，無時區或獨立拍攝日期核證，2017 為影像修改時間，皆不是 2026 年現況。未隨包放入照片，也不是材料鑑定或校準色票。

- 只處理模型 +Y 法向、y=19 mm、x 約 ±68.5 mm、z 約 44.3–46.4 mm 的兩個原三角面（約 287.70 mm²）。原水池側簷帶短側端、水平頂底面、瓦、牆、框、玻璃後材料及立體字本身不改。
- 保留原 8,560 個三角面與 4,202 個頂點，不切面、不加頂點。原有 1,002 個字正面、130 個窗背材質指派皆原樣；新增的灰色槽僅供該兩面。
- 仍是尺寸近似的外觀展示模型，未切片或試印。上圖為新配對診斷渲染，非替換代表圖。

## 獨立重建與驗證

從不可變版本下載[原基準 Blender](https://github.com/hplin50643/taiwan-buildings-3d/blob/5018bb0b9c8fd679e1155e09afd8814e9dc88166/%E5%9C%8B%E7%AB%8B%E8%87%BA%E7%81%A3%E8%97%9D%E8%A1%93%E5%A4%A7%E5%AD%B8/%E6%9D%BF%E6%A9%8B%E6%A0%A1%E5%8D%80/buildings/ntua-you-chang-museum/appearance/scene.blend)及[原基準 3MF](https://github.com/hplin50643/taiwan-buildings-3d/blob/5018bb0b9c8fd679e1155e09afd8814e9dc88166/%E5%9C%8B%E7%AB%8B%E8%87%BA%E7%81%A3%E8%97%9D%E8%A1%93%E5%A4%A7%E5%AD%B8/%E6%9D%BF%E6%A9%8B%E6%A0%A1%E5%8D%80/buildings/ntua-you-chang-museum/appearance/ntua-you-chang-museum-appearance.3mf)放入本模型資料夾下的 appearance/。基準依 [domain.json](domain.json) 核 SHA-256；配置後不需要網路或私人照片。輸出會覆寫變體檔，請在隔離的副本執行：

    blender -b appearance/scene.blend -t 4 --python-exit-code 1 -P pool-side-fascia-20261120/apply_pool_fascia.py -- --qa-renders
    python3 pool-side-fascia-20261120/rebuild_exchange.py

[確切面域](domain.json) · [格式與材質](verification.json) · [視覺 QA](visual-QA.json) · [隔離重建](reproduction-QA.json) · [不可變原發布校驗](https://github.com/hplin50643/taiwan-buildings-3d/blob/5018bb0b9c8fd679e1155e09afd8814e9dc88166/%E5%9C%8B%E7%AB%8B%E8%87%BA%E7%81%A3%E8%97%9D%E8%A1%93%E5%A4%A7%E5%AD%B8/%E6%9D%BF%E6%A9%8B%E6%A0%A1%E5%8D%80/buildings/ntua-you-chang-museum/pool-side-fascia-20261120/SHA256SUMS)。
