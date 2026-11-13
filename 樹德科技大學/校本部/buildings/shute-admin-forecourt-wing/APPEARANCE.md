# 樹德行政前庭翼｜完整屋頂格架背面補色 v2

## 本次修正與界線

本輪只將 **50 個原中性三角面** 延用原有「Concrete fins and grille」混凝土灰 #A2A49E。這些是原模型屋頂開放格架在 y=25 的完整後表面，不是主建築的背立面。舊規則將所有 y≥24 朝後面都視為終止面，因而連同已建模的屋頂格架背面也變成中性。

每個候選三角面的全部頂點均須位於原格架的 y=25 平面、x[-63,58]、z[77.5,91.5] 範圍，且法向向後；再將整個三角形與八個既有開口範圍裁切，要求正面積交集為零。不是只靠面中心選取，不拆面、不補洞、不新增窗列、文字、欄杆或幾何。

保留 **5,520 個原有色面**、八種原材質的 diffuse RGBA、shader Base Color、roughness。2,839 頂點、5,734 三角面、150 × 87 × 104 mm、全部座標、面順序與 transform 不變。原 STL、scene.blend、幾何產生器、previews 四張圖及歷史 QA 均不改，校級校驗檔與學校代表圖也不改。

**164 面仍中性**：主翼 y=24 人造終止面 4 面、短回翼 y=24.5 人造終止面 4 面、主屋頂 34 面、人工底座與入口鋪面 122 面。模型本來只是前庭翼段，不能把大面封閉終止牆當成真實建築完整後牆而補色。未改這些中性面，不表示它們的實物材質已經確認。

## 本輪親看來源

- [教育部網站所載校方 113 年度報告](https://ws-proj.moe.edu.tw/001/Upload/568/relfile/13271/17377/accab4cb-8092-4855-9d38-65f37b5a9f0f.pdf)，印刷頁 12／PDF 第 13 頁的校園空照。本輪重用既有且 SHA256 對上原來源紀錄的抽出 JPEG，親看實際像素，沒有重新下載或重讀整份 PDF。空照支持屋頂開放格架為淡色混凝土構件，但解析度不足以量測每片背面色值。
- [104 行政大樓近景](https://guide.104.com.tw/backend/media/origin/school/703.jpg)。本輪重用既有且 SHA256 對上原來源紀錄的 JPEG，親看實際像素。圖中六片灰色翼片與上方連接構件同屬混凝土外觀；主牆粉褐、塔體暖米、玻璃深綠和框銀灰沿用原色。

來源支持構件的材料類別；**格架隱蔽背面的精確顏色是同一構件連續性推估，不是照片直接證實**。不將兩張照片說成完整四立面測繪；照片實際日期未知，報告 2025-04-02 metadata 建立日不等於攝影日，不稱 2026 現況。色值是視覺近似、未色卡校準。完整紀錄見 [source-register.json](appearance-review-v2/source-register.json)。不在公開包散布照片、PDF、私人審核資料或貼圖。

## 重現與驗證

原 scene.blend、model.stl 與更新 build_appearance.py 同層，以 Blender 4.3.2 執行：

    blender -b -t 1 --python-exit-code 1 -P build_appearance.py -- --skip-render
    blender -b -t 1 --python-exit-code 1 -P render_review.py

第一步生成材質 BLEND、Core 3MF 與逐面索引。第二步生成七張終圖與兩張恢復原色的前／後比較圖；全部為 Cycles CPU、96 samples、單執行緒、900 × 800、無降噪及文字印記。比較圖的相機位置、旋轉、正交尺度、照明、材質值完全相同，只有原面材質索引還原。build_appearance.py 不加 skip-render 時也產生七個終圖角度。

[逐點逐面幾何及材質驗證](appearance-review-v2/model-verification.json)、[完整構件界線審核](appearance-review-v2/boundary-continuity-audit.json)、[乾淨重建](appearance-review-v2/clean-rebuild-equality.json)、[九張圖片實際檢視](appearance-review-v2/color-continuity-review.json)與[原數位 QA 重跑摘要](appearance-review-v2/original-qa-rerun-summary.json)分開記錄。3MF 頂點與面索引精確對應 BLEND，使用原 palette、單位及 build 結構；未分割成多列印零件，也未設定 AMS、噴頭或耗材映射。

原 QA 的 1,977 個小於 0.8 mm 法向短段、最短約 0.01331 mm，及 3 個方向旗標不被本次補色消除。限定根部與邊界證據仍須連同原 QA.md 閱讀，不可改稱所有方向厚度都達 0.8 mm。未做實體試印或切片工具路徑驗證；屋頂橫樑、凹陽台與遮陽片仍需支撐及橋接評估。

新 appearance.blend 無文字物件、文字區塊、外部照片及 linked libraries，render 路徑相對化。新圖已移除文字 metadata。本輪檢查在 appearance-review-v2，原 appearance-review 繼續作為 v1 歷史資料。

## 發布狀態

本輪只在本機準備，未發布 GitHub blob、commit、ref 或 PR，未完成遠端讀回。固定基底 123e103381f4d7eb98627857d9b720b8e497ecaa；本輪未查核最新遠端版本。後續發布需要重新核對最新基底、合併校級校驗檔及實際遠端讀回，不能以本機準備冒稱已發布。


## 四條上層帶窗既有豎框前表面修色 v3
依原生成器已明示backed mullions的40個完整前表面有限共面域，將80三角面由玫瑰牆材1改為既有銀灰金屬材6。全頂點核y=-17.04及原x柱中心16+4.3k/四窗段界，不切新界或造框；側面、端面、return窗、遮陽板及其他混域原樣保留，不聲稱全部框面已重配色。原框數/寬仍是近似，不提高測繪可信度。其餘5654面、8材值、座標/transform、STL/scene/previews與原v2格架背50面修正均不變。
本輪worker直接取得與舊登錄SHA一致的104前照JPEG並實看；獨審另次URL回HTML，故記錄回應不穩定，不宣稱網址一直回相同照片。合法歷史原幅亦同SHA；照片可見四條窗帶淺銀灰豎框，非牆面粉褐。官方航拍沿用已保存且SHA一致的抽圖並實看，未重下載整份PDF；航拍只支持建築身分/整體，不用小像素推斷框色。來源日期未知，不能當現況。原appearance-sources歷史保留，現次依MULLION-FRONT-SOURCE-QA.json；照片私用不公開。
原91blob與root90條SHA256SUMS全部吻合，無歷史例外；BASELINE-CHECKSUM-AUDIT.json列原expected/actual與精確保存路徑。7原生900×800圖與2原基線同相機比較寫入新v3，不覆寫v2歷史。原1977個短法向段、最短0.01331mm及3方向旗標未修，不稱全面壁厚通過或可免支撐試印。
