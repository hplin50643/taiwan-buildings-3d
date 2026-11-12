# 中興大學行政前棟與柱廊段｜有限原面延伸補色 v2

## 本次變更

依同棟、同構件材料連續性，把 895 個原中性三角面補上原有材料：680 面延用米黃灰牆色，215 面延用原灰階梯色。範圍為既有窗洞實牆回折面、入口與兩翼之間短回牆、原空白牌面的側緣、前側簷口與完整前側挑簷／柱廊底面，以及既有階梯側邊和前平台。所有三角形頂點及法向都必須符合明確範圍，不以面中心判斷，不切面、不改幾何、不新開窗。

這些延伸面中未直接被照片看見的部分屬連續性推估。不是完整四面測繪，也不是精確色票或材質鑑定。原 2,082 個有色面、五種材質的 RGBA／Base Color／roughness 完全保留。原有 80 面不透明混合窗背及 752 面窗框均未改動，不新增窗背。

原 1,551 頂點、3,290 三角面、150 × 62 × 66.30 mm 與 transform 不變。原 STL、scene.blend、build_model.py、四張 previews、歷史 QA 及學校代表圖維持不變；本輪校級校驗檔不改。

## 本輪實際檢視來源

重新下載並親看[2024 年 8 月行政大樓正面實照](https://upload.wikimedia.org/wikipedia/commons/8/85/NCHU_Administration_Bldg%2C_Taichung%2C_Aug_2024_%281%29.jpg)，來自[Commons 檔案頁](https://commons.wikimedia.org/wiki/File:NCHU_Administration_Bldg%2C_Taichung%2C_Aug_2024_%281%29.jpg)。本輪實際讀取 EXIF 的 DateTimeOriginal 為 2024:08:25 15:44:12，未帶時區。原文件記載作者 Ralff Nestor Nacor 及 CC BY-SA 4.0；本輪未重讀授權頁，亦不重新散布照片。

實照可見米黃灰前牆與巨柱、窗框、退縮入口、簷口及灰階梯。依既有構件面界延續原配色，不把陰影當成新材質。沒有新增任何屋頂紅帶、春聯紅帶、金字、細窗格、植栽、欄杆、冷氣、污漬或剝落細節；原長柱沒有春聯色塊邊界，不能把整根塗紅。

本輪僅親看這一張原始實照。10 月實照、校方相簿與其他來源未重讀，不稱已用多角度確認。2024 照片不代表 2026 現況。圖片雜湊及查閱範圍見 [來源登記](appearance-review-v2/source-register.json)，交付不含來源照片、貼圖或私人參考包。

## 保留中性與截斷界線

313 個三角面仍保留原中性。背側 y=20、21.5、22.5、23 的各段是模型的人為後截面，沒有把它們當成真實背立面上色。兩翼末端 x=±68 及翼屋頂端部 x=±69.5 的完整大面也不據此宣稱實牆。原已著色的橫帶端部保持原狀。

原上部量體的長側三角面跨越有依據的前伸部分和未確認進深，不能只塗半個三角形，因此維持中性。屋頂上表面、底座、後端平台、混合界線的地面小條及未能界定的簷底面也保留。中性不是確認現物灰色，局部補色不等於全館復原。

## 重建與核驗

原 scene.blend、model.stl 與更新 build_appearance.py 同層，以 Blender 4.3.2 執行：

    blender -b -t 1 --python-exit-code 1 -P build_appearance.py

可加 -- --skip-render 跳過圖像；再執行：

    blender -b -t 1 --python-exit-code 1 -P render_review.py

輸出七張終圖和兩張還原原材料索引的前／後對照圖。全部使用 Cycles CPU、96 samples、單執行緒、900 × 800、無降噪、無文字印記。對照圖的相機位置、旋轉、正交尺度、照明及材質值完全相同，只恢復原逐面材質索引。

[逐點逐面幾何／材質驗證](appearance-review-v2/model-verification.json)、[完整面界與截面排除審核](appearance-review-v2/boundary-continuity-audit.json)、[乾淨重建比較](appearance-review-v2/clean-rebuild-equality.json)、[九圖親視檢查](appearance-review-v2/color-continuity-review.json)分別記錄。

四支原數位 QA 程式已在獨立目錄原樣重跑：[摘要](appearance-review-v2/original-qa-rerun-summary.json)。幾何驗證通過，332 個 0.2 mm 間隔斷面全部閉合有效，67 個 1.0 mm 間隔薄特徵取樣的最大 opening 損失比例約 0.07533%，無超過 1% 的取樣層。原 STL 重建雜湊相等。

這些是數位檢查，不是實體試印或切片工具路徑驗證。挑簷、雙層柱廊仍需評估支撐及拆除，不能保證任意縮放或免支撐列印。3MF 不設定 AMS、機台或耗材映射。appearance.blend 無文字區塊、文字物件、外部照片、linked libraries；render 路徑為相對路徑。

## 發布狀態

本輪只在本機準備，未發布、未建 GitHub blob／commit／PR／ref。固定基底 123e103381f4d7eb98627857d9b720b8e497ecaa；最新 HEAD 重查因先前拒絕未重試或繞過。之後發布仍須在允許時重新核對最新基底、處理校級校驗檔並真正遠端下載驗證。

原 appearance-review 為 v1 歷史；本次有效驗證另列 appearance-review-v2，沒有覆寫歷史資料。
