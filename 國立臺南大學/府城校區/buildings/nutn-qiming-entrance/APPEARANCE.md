# 啟明苑入口端｜同構件延續補色 v2

## 本輪結果與原模型範圍

維持府城校區啟明苑入口端局部標段，不是全館。新增164個原中性三角面：36面磚紅高塔外牆、128面米白低廳／門廊／陽台轉折。原374個已上色面、所有原RGBA與roughness保持；478面仍中性。

原498頂點、1,016三角面、150×105×84.5mm與transform不變。原STL、scene、重建程式、四張鎖定預覽與歷史檢查不替換；不切面、增窗、添玻璃、磚縫、字、設備或細欄杆。每個改色三角面均以所有頂點、表面法向及完整原構件邊界判定，沒有用面心跨界塗色。

## 來源與推估

本輪重新下載並親看三張校方照片：[017](https://www.nutn.edu.tw/gac780/picture/01/017.jpg)、[018](https://www.nutn.edu.tw/gac780/picture/01/018.jpg)、[035](https://www.nutn.edu.tw/gac780/picture/01/035.jpg)。017與035可辨高塔紅磚、低廳與門廊米白；018可見淺色長廳的側牆及簷口。035顯示曲陽台實心欄板與柱梁是米白材料家族，薄金屬扶手不同，但原模型未建且不新增。

高塔原完整獨立量體未著色的+X與+Y垂直外面依磚紅家族延續；塔後壁y29不是低廳的人工截斷。低廳原+X側、非截斷的簷口轉折、門廊大簷側與底、樓板垂直邊、實心直線欄板與弧形欄板的內外弧和狹頂依米白家族延續。

未見或背向範圍屬合理同構件推估，不是每一面都有照片佐證。原色值仍是未校準近似，照片曝光／樹影差異不擬造材料分界。原模型離散塔窗與實照連續玻璃帶有差距，本輪保持原幾何和已上色窗背，不假造窗列或框。

三照的拍攝日期未知。本輪未重查網頁、EXIF或校圖，既有網站更新時間不是攝影日，不保證2026現況。照片只供私人核對，公開包不含原照。

## 保留中性與人工截斷

低廳後截面y41、其屋簷後截面y43.5與入口量體後界y31.5保持原材質；它們沒有足夠依據當作完整真實背立面。這與已完整建立、可按同量體延續的高塔後壁不同。模型方向是原座標，不是地理方位。

塔帽與廣屋頂、屋頂小機房、高側帶窗與其他未辨明窗框側壁、深上廊立柱、階梯及人工底座不猜色。曲陽台只補原實心欄板，不塗其行走樓板頂面。中性表示本次不作有把握的判斷，不表示實物灰色。

## 驗證、重建及審核

原scene.blend與model.stl同層保留。Blender 4.3.2執行 blender -b -t 1 --python-exit-code 1 -P build_appearance.py 可重建彩色外觀，加 -- --skip-render 略過PNG。乾淨資料夾重建已驗證逐點、逐面、材質與transform一致，3MF及材料JSON位元一致。

[幾何材料核對](appearance-review-v2/model-verification.json) · [完整面界線檢查](appearance-review-v2/boundary-continuity-audit.json) · [全頂點取景](appearance-review-v2/framing-audit.json) · [乾淨重建](appearance-review-v2/clean-rebuild-equality.json) · [來源登錄](appearance-review-v2/source-register.json) · [本輪原QA重跑](appearance-review-v2/rerun-qa-summary.json) · [最終視覺審核](appearance-review-v2/color-continuity-review.json)。

7張最終圖與2張同相機原圖採900×800、Cycles CPU、96 samples、單執行緒、不降噪；圖像審核以連結記錄的已查看圖檔雜湊為準。原圖僅恢復原面材質配置，燈光、相機、色值與渲染設定相同。新appearance.blend無文字物件、文字區塊、來源影像或外部函式庫，輸出路徑相對化；PNG清除文字型中繼資料。歷史appearance-review為v1，本輪使用appearance-review-v2及appearance-freeze.json。

在獨立資料夾重新執行原validate_model.py、check_contour_validity.py、check_thin_features.py，全通過。包含STL法向與繞序、水密、每邊兩面、單殼、頂點link單環、重建STL雜湊及scene一致，423個0.2mm輪廓層有效閉合；85個1mm高度薄特徵取樣，0.8mm opening最大損失0.08503376045%，超1%層數0。這不是完整壁厚或工具路徑檢查。

## 列印及發布限制

未實體試印、未Cura／PrusaSlicer實際工具路徑或多色機台映射測試，不保證AMS相容、免支撐或任意縮放可印。門廊、陽台、挑簷及窗洞上沿的橋接與支撐風險保留，照片估計尺寸不等於測繪。

僅本機待審，沒有發布。基準為指定commit 123e103381f4d7eb98627857d9b720b8e497ecaa；未重試已拒絕的最新HEAD查核或GitHub寫入。校級SHA256SUMS未改，日後取得允許發布時仍須核對最新遠端與合併校級雜湊。
