# 澎湖科大實驗大樓入口段｜階梯端面補色 v2

## 本次範圍

只把 49 個原中性三角面補為原有的階梯石材色，總面積約 87 mm²。位置是 x=-68 mm、y=-44.5 至 -17.5 mm 的真正階梯左端。原 v1 程式對所有 x=-68 面套用「人工側切面」規則，誤把伸出建築前方的階梯端面一起中性化。本次區分真正牆體裁切與原階梯構件，不把整個 x=-68 平面一律上色。

完整三角形須位於原四級階梯的折線輪廓內。生成器以 YZ 多邊形裁切核對完整覆蓋面積，獨立審核另用三角形減去階梯輪廓聯集，核對越界面積接近零；不是依面中心點推算，也沒有切分網格。

原 2,196 個有色面不變，包括 1,183 個既有玻璃／門窗框面；八種材料的 RGBA、Base Color 及 roughness 全數保留。1,143 頂點、2,290 三角面、150 × 78 × 81.6 mm、物件 transform、原 STL 與 scene.blend 均保留，未增窗、門、文字、細框、貼圖或幾何。

## 直接證據與推估

本輪重新下載並親看[澎湖科大官方入口近照](https://www.npu.edu.tw/df_ufiles/034/s_r0345943%281%29.jpg)：近白門廊、兩圓柱、淡米灰磁磚牆、五組前方門窗、右側深框雨棚及灰色階梯，與原模型的入口段相符。既有窗色是不透明的玻璃／反光近似，不是純玻璃色或透明認證。

階梯踏面／立面及材質類別可直接辨識；左端受畫面邊界、視角及植栽限制，新增端面色是同一階梯材料連續性的合理推估，不能稱逐面照片證實。使用原階梯材料，不用照片陰影另造黑帶或改動原色。

官方照片 SHA256 與原 v1 來源登錄一致。拍攝日期未知；導覽頁 2018-09-06 更新日不等於照片拍攝日，也不代表 2026 現況。原平面圖、廣場／後側照片及 2022 屋頂整修會議本輪未重新讀取。詳見[本輪來源登錄](appearance-review-v2/source-register.json)。來源照片僅私人研究，不附入模型包、不作模型貼圖。

## 仍保持中性的範圍

保留 45 個中性面：33 個底座面與 12 個人工牆側／背／頂封口面。真正牆側 x=±68 位於 y≥0，背面 y=20，頂面 z=79，均不補色為實際立面或屋頂。階梯端面位於負 y，與這些牆體切面在空間與用途上不同。

本件仍是門廊與前兩層立面局部，不是整棟建築，沒有增高到山牆或補造側翼。模型 −Y 是入口前方；不賦予未核實羅盤方位。照片中細磁磚縫、字牌、欄杆、燈具、植物及更高退縮窗列均未新增。

## 重建與驗證

原 scene.blend、model.stl 與更新 build_appearance.py 同層，以 Blender 4.3.2 執行：

    blender -b -t 1 --python-exit-code 1 -P build_appearance.py -- --skip-render
    blender -b -t 1 --python-exit-code 1 -P render_review.py

七張終圖與兩張原材料同相機比較均為 Cycles CPU、96 samples、單執行緒、900 × 800、無降噪、無文字印記。原色比較只還原面材質索引，相機、照明及材料數值相同。七視角：斜前、人工背切面、正面、同來源低角、左、右、上視。舊五張 previews 及 v1 appearance-review 保留不變；本輪有效審核位於 appearance-review-v2。

[逐點逐面／材料／3MF 核對](appearance-review-v2/model-verification.json)、[完整面支撐範圍](appearance-review-v2/boundary-continuity-audit.json)、[乾淨重建](appearance-review-v2/clean-rebuild-equality.json)、[九圖檢視](appearance-review-v2/color-continuity-review.json)分別記錄。新 appearance.blend 無文字物件／文字區塊、外部照片、linked libraries 或絕對渲染路徑。

原 validate_model.py、check_contour_validity.py、check_thin_features.py、check_recess_rays.py 在獨立目錄以原樣腳本及原固定版本依賴重跑；結果見[本輪原 QA 重跑](appearance-review-v2/original-qa-rerun-summary.json)。檢查包括重建 STL 雜湊、封閉拓撲、原 scene/STL 同形、408 層 0.2 mm 輪廓與 opening、13 項原面射線。0.8 mm opening 最大面積損失約 0.0466%，不是全面最小壁厚保證。未做實體試印、多色設備映射或 Cura／Prusa 工具路徑；門廊頂板、雨棚、挑梁及窗洞上緣仍需支撐與拆除評估。

## 本機狀態

只在本機準備，未建立 GitHub blob／commit／PR／ref，未發布或遠端讀回。基底固定為 123e103381f4d7eb98627857d9b720b8e497ecaa；先前最新 HEAD 讀取遭拒後，未重試或改路徑繞過。校級 SHA256SUMS 未動，之後若獲允許發布，須先重核最新基底與校級校驗檔。


## 右雨棚前橫梁上端三完整原域修正 v3
僅6面（2194,2199,2200,2209,2212,2213）改為原深框材5，涵蓋前橫梁z=44.5至44.6上唇正/背面及z=44.6頂面3個完整連通共面域。原分類的高度門檻與板近似容差將同一橫梁上端誤套牆磁磚/雨棚板色；原生成器證明完整域均屬此橫梁。官方照片支持前橫梁深框家族，頂及背唇為明示同構件延伸推估，非直接逐面照片色證。兩端融合板/梁域、上方建築梁底與主牆混合域均不改，不切割任何網格。
其餘2284面與8項原材值、geometry、transform、原STL/scene及五張previews保持。原v2階梯49面修正不變，舊QA/影像保留為原版本；本次7張原生900×800圖與2張恢復本次基線面索引的比較由render_review.py寫入appearance與appearance-review-v3，舊v2記錄未重寫。原照片日期、局部模型、缺失小構件與列印支撐限制全部保留。不聲稱新造完整建築、已試印或已發布。來源照片私人保存，不附公開包。新審核RAIN-BEAM-INDEPENDENT-QA.json，源審快照RAIN-BEAM-SOURCE-QA.json。
