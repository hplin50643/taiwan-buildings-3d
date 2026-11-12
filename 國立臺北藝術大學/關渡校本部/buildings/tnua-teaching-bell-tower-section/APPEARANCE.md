# 北藝大教學大樓鐘樓段｜上部構件延續補色 v2

## 範圍及結果

此件仍是鐘樓、近旁低翼與局部階梯，不是整棟教學大樓，也不包含對面鼓樓。新增補色792個原中性三角面：493面灰石、293面淡灰內側／孔側壁、6面對側瓦坡。保留原403個已上色面及所有材料RGBA、roughness；1,193面保持中性。

原1,134頂點、2,388三角面、112×100×150mm、物件transform、STL及scene全部不變。沒有增窗、玻璃、瓦紋、字、細部或切面。每個改色三角面的所有頂點都落在原構件實際表面，不用面心或任意水平色帶挑選。

## 來源、直接觀察與推估

本輪重新下載並親看[原列DSCF2656照片](https://kandoman.blogspot.com/2017/03/blog-post_25.html)。照片顯示上部外側灰石、內側屏牆與孔側壁較淡、承鐘橫梁淡灰、原山牆屋脊凸片延續石色，已見瓦坡為紅褐色。來源照片只供私人核對，不包含於公開包。

上述觀察支持把原上塔屏牆、山牆、門廊邊柱／橫梁、欄板、樓板邊、孔側壁與承鐘橫梁的完整同構件表面延色。未見或對側面是合理同構件推估，不是逐面有照片或實測色值。另一瓦坡只補原外向斜面，不把屋底、厚度邊或圓簷條染成瓦色。鐘體仍沿用原深色，不擴及承鐘橫梁。

模型−Y為鐘樓正面，+Y連接教學長翼；來源大致對應−X／−Y角度，這是模型配準而非地理羅盤方向。原2017-03-25記錄是刊文日，不是確認的攝影日；本輪未重讀文章／EXIF、沒有取得新Commons角度、不保證2026現況。

## 保留中性的理由

圓簷條雖在照片可見，但呈獨立的深色風化／陰影表面，材質不能直接等同瓦、鐘體金屬或原灰石，因此不猜色。下塔的灰石／磚混合量體、低翼、階梯及人工基座保持原材料。原低部沒有完整材料分界，不能為補色任意切面或染穿混合區。

+Y下部平牆是人工截斷教學長翼的模型邊界，不能把它當成真正背面外牆複製配色或窗列。這與上部已完整建出的鐘廊背向構件不同，後者可按同構件延續。中性只表示此次不作有把握的材質判斷，不代表實物必然灰色。

## 重建與驗證

同層保留原scene.blend與model.stl。以 Blender 4.3.2 執行 blender -b -t 1 --python-exit-code 1 -P build_appearance.py 可重建彩色檔；加上 -- --skip-render 可略過PNG。已在乾淨資料夾重建，逐點、逐面、材質及transform一致，3MF與材料JSON位元一致。

[幾何與材料](appearance-review-v2/model-verification.json) · [完整面界線](appearance-review-v2/boundary-continuity-audit.json) · [乾淨重建](appearance-review-v2/clean-rebuild-equality.json) · [來源登錄](appearance-review-v2/source-register.json) · [本次原QA重跑](appearance-review-v2/rerun-qa-summary.json) · [視覺審核](appearance-review-v2/color-continuity-review.json)。

7張最終圖與2張同相機原圖為900×800、Cycles CPU、96 samples、單執行緒、不降噪。新外觀BLEND不含文字物件、外部來源照片、連結函式庫；渲染路徑相對化，PNG無文字型中繼資料。舊appearance-review為v1歷史，本輪由appearance-review-v2及appearance-freeze.json綁定。

本輪在獨立資料夾重跑原四個數位QA，全部通過：STL原法向／繞序、每邊雙面、單殼、頂點連結單環、重建STL雜湊、scene一致、750個0.2mm輪廓層有效閉合及150層薄特徵篩檢。0.8mm opening loss最大0.5711417295%，仍不等於完整壁厚檢測。

## 列印與發布限制

未實體試印、未Cura／PrusaSlicer實際工具路徑、未多色機台映射測試。鐘下、橫梁、斜簷與細欄杆原支撐及易損風險保留；吊鐘不是可活動件，原照片估計尺寸不等於測繪。

僅本機待審，沒有發布。使用指定commit 123e103381f4d7eb98627857d9b720b8e497ecaa，未重試已被拒絕的HEAD重查或任何GitHub寫入。日後發布須重新取得允許並核對遠端，校級SHA256SUMS本輪未改。
