# 聯大八甲 D1／D2 客家研究學院：七材質外觀版

沿用原 **4,476 三角面／2,240 頂點**，不改原 STL 位元、座標、面序或幾何；這是既有模型外觀改版，不增加模型包數。

| 模型預覽 | 模型預覽 | 模型預覽 |
| :---: | :---: | :---: |
| 正面<br>![正面](previews/front.png) | 背面保持中性<br>![背面](previews/rear.png) | ![正立面](previews/elevation.png) |
| ![頂視](previews/top.png) |  |  |

[表面色 3MF](nuud12-appearance.3mf) · [可編輯 Blender](scene.blend) · [材質色表](palette.json) · [逐面指派與依據](face-materials.json) · [原 STL](../model.stl)

## 來源與配色邊界

親自核對官方 [客家學院相簿](https://secretary.nuu.edu.tw/p/132-1003-1095.php?Lang=zh-tw) 的 [D1 照片 4](https://secretary.nuu.edu.tw/var/file/3/1003/gallery/95/1095/gallery_1095_5846559_25626.jpg)、[D2 照片 1](https://secretary.nuu.edu.tw/var/file/3/1003/gallery/95/1095/gallery_1095_9536606_25626.jpg)。EXIF DateTimeOriginal 分別為 **2025-03-02 14:52:18／15:09:50**，不以後續修改日當拍攝日；時區與日期未獨立核實，不聲稱 2026 現況。使用完整可解碼照片，早期傳輸不完整的 D2 副本不作最終 hash 證據；照片不隨包散布。

- D1 前棟與 D2 後棟已見正面結構灰色，前露台基座、左端及 D2 入口館牆奶油色；D2 原入口雨棚深綠色，原支柱淺色，不添字樣、招牌或室內設備。
- 只有原 D1 獨立窗槽與 D2 入口窗槽凹背配灰藍玻璃，原粗窗梃深灰。D1 上廊、D2 三層走廊與塔樓深凹包含門、牆和窗，不能當整片玻璃，保守中性／灰色。
- **D1 右端紅磚與奶油水平帶未完整配色**：原大面沒有足夠的實景色帶邊界，而且原看板面與照片方向為簡化對應。兩側寬大未分割面維持中性，不全染紅而省略色帶，也不切面假造色帶。照片確有紅磚，這是本版保守未還原區。原看板框灰色／內容留白，不複製廣告。
- 原四組實心黏合光伏小板配低彩度藍色，周邊屋頂中性；不增架高支架、管線或水塔。原厚實欄牆不是精確金屬欄杆；不畫細桿假造不存在的幾何。
- 原共底台與兩樓相對位置、坡度、窗數及外梯均是照片概略推估，不是測繪；不據此主張實際連通關係。照片後方 E3、其他前景館舍與植栽不包括。
- 未見後側、無法登錄的側面與其他屋頂中性。原 STL／面序／座標不變，不增加模型數，不宣稱物理列印成功。

[原幾何與來源限制](../README.md) · [來源覆核](qa/source-review.json)

## 重建與核驗

安裝 [依賴](source/requirements.txt)，Blender 使用 4.3.2。由本資料夾上層提供原 model.stl：

1. `python appearance/source/build_appearance.py`
2. `python appearance/source/verify_exchange.py`
3. `blender -b -t 3 --python-exit-code 1 -P appearance/source/render_appearance.py`
4. `blender -b -t 3 --python-exit-code 1 -P appearance/source/verify_scene.py`

[獨立重建 ZIP](rebuild-source.zip)含原 STL、四支程式及依賴，不含第三方照片；不取代原建模腳本。[逐檔 SHA256](SHA256SUMS)

[交換／拓撲 QA](qa/exchange-validation.json)核對原座標與面序、全部面材質、單連通、有向水密邊、頂點 link 單環、正體積與零退化／重複面；lib3mf 嚴格讀取零警告，實際編輯單材質再存讀，其他材質及面指派不變。SDK 六位小數量化誤差另列。

[Blender 存讀與編輯](qa/scene-validation.json) · [渲染記錄](qa/render-manifest.json) · [獨立重建](qa/rebuild-validation.json)

## 製造限制照舊

尺寸仍為 150 × 118 × 58 mm；原 STL、建模程式、場景及歷史 QA 保留。原層檢與薄特徵檢查本次未重跑，不能由材質 QA 代替。

3MF 是同一網格的表面色，不是各材質各自封閉的分色實體、切片專案、噴頭映射或 G-code。切片 GUI、多材料路徑與實體列印未測；柱頭、屋簷、窗框及薄邊仍須評估材料、支撐及拆除風險，沒有保證可印或免支撐。


## 2026-11-14 有限外觀修正（新接續交付版）

僅D1原最低三個踏面與正面階面完整域共12面，改用新灰7（#979C94，roughness .88）；原7材質不變。D1來源中的灰階梯與米色側裙分開，D2照片不可替代D1材質證據。原14粗階及寬11.5不是實測階數或尺寸；真實中段平台、細鼻口、欄杆、接縫未建模，不修幾何。不改上11階、平台、側裙、基座或D2階梯。

顏色僅外觀材料家族近似，不是校準色或材種鑑定。公開照片不證明2026現況。原STL、幾何、順序、代表圖與原視角保持；浮點面域差異保留，非宣稱零誤差。歷史QA與製造限制仍適用。
# Public references

- https://secretary.nuu.edu.tw/p/132-1003-1095.php?Lang=zh-tw
- https://secretary.nuu.edu.tw/var/file/3/1003/gallery/95/1095/gallery_1095_5846559_25626.jpg
- https://secretary.nuu.edu.tw/var/file/3/1003/gallery/95/1095/gallery_1095_9536606_25626.jpg

Source0 D1 lower steps; source1 D2 context only. No private evidence hashes.

現版共 8 個顯示材質（含未知中性色）。上方原材質數、面域與QA描述為歷史版本，僅由本節有限範圍更新。本版是新接續建置，不是尋回遺失草稿；不新增幾何或擴充補色範圍。

本節提及原ZIP/QA/校驗數目屬歷史記錄，不是現版ZIP清單。現版ZIP僅含原STL、必要舊建置與渲染程式、三支現版包裝／驗證程式、requirements-current.txt與本README及授權說明（如原有）。完整來源研究、照片、私人審核與廣泛校驗清單不公開。PUBLIC-MODEL-SHA256SUMS僅核當前交付產品；原QA不替代當前驗證。

現版命令：`python -B appearance/source/build_current.py`、`python -B appearance/source/verify_current.py`、`blender -b -t 4 --python-exit-code 1 --python appearance/source/render_current.py`。依requirements-current.txt安裝必要依賴。直接執行舊builder會重建歷史配色。包裝程式僅執行固定本地舊程式，新增材質時只替換新材質粗糙度運算；寫模型、材質、場景、原視角PNG與當前本地QA。歷史報告先保存再還原；原不存在時只刪該次產生的舊名報告。不進行網路或憑證操作。
