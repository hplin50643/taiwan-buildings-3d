# 彰師大圖資大樓入口轉角段｜原構件延伸補色 v2

## 本次範圍

延伸原材質到 70 個原中性三角面：28 面凸窗帽板／轉角窗列底返面採原土米色、6 面入口斜罩切口側返面採原墨綠、36 面階梯左右端面採原灰色。每個三角形全部頂點須落入原構件支撐盒及平面，並核對法向；斜罩還須位於原三角斜坡包絡線內。4 個跨出斜罩斜坡範圍的混合面明確排除，不能用中心點選取。

這些未直接見到的頂面、底面與返面，是同構件材料連續性的合理推估，不冒稱照片逐面確認。原 2,244 個有色面及六種材料的 RGBA、Base Color、roughness 均不變。1,368 頂點、3,004 三角面、150 × 105 × 93 mm、transform、STL／OBJ／scene／幾何生成器均保留，沒有新切面、細框、窗、文字或網格。原四張 previews 與歷史 QA 不替換。

## 來源與直接證據

本輪重新下載並親看 [M+ 典藏完工實拍](https://res.cloudinary.com/mplustms/image/upload/w_1000/v1627899124/v2/prod/small/014001_014500/014189_001.jpg)：三列前凸窗、轉角側窗列、土米色窗體與近白窗梃、偏置綠色斜罩、開放柱廊及灰階梯，與原入口角段相符。原深灰綠窗背是玻璃、框、陰影與反光的不透明混合閱讀代理，不是純玻璃色或透明認證。

攝影日未知；項目年代 1986–1989 及 URL 版本／上傳時間都不是攝影日，不宣稱 2026 現況。原 2016 官方會議近照、2018 Commons 另一轉角與校圖本輪未重新讀取，不把舊檔記錄當新現場調查。[來源登錄](appearance-review-v2/source-register.json)記載實際下載雜湊與閱覽範圍。來源照片只作私人研究，不隨包散布、不作貼圖或對照拼貼。

## 為何仍保留中性

實照是白／米黃寬橫帶，原網格只有 z40／54／68 附近 1.3 mm 薄凸線，沒有寬帶完整分界。因此不把窄線染白冒充寬帶，不按三角中心高度造色塊。原大牆、雙色柱及薄凸線保留中性。這是缺少可用材料界線，不是以「未知」一詞禁止合理連續性補色。

仍有 690 面中性，包含大牆／柱與凸線、主屋頂、人工後收邊、原未分區窗凹口、底座及階梯隱藏後收邊。明確核對的 34 個 +Y 人工收邊面原樣保留中性，不能當真正背牆復色。本件只有原入口轉角與短側範圍，沒有擴成全館，不賦予未確認的羅盤方向。模型 −Y 是入口，+X 是凸窗轉角側。

原入口罩繼續使用粗化且不透明的墨綠框／屋皮混合代理；照片細框、深色玻璃格與原網格不完全相符，故不新增透明玻璃、細框網格或小格。柱廊 11.1 mm 真淨空保持開放。裝飾藍綠磁磚、字牌、紅字、欄杆、磚縫與植物均不新增。

## 重建與驗證

原 scene.blend、model.stl 與更新 build_appearance.py 同層，以 Blender 4.3.2 執行：

    blender -b -t 1 --python-exit-code 1 -P build_appearance.py

可加 -- --skip-render 跳過渲染。完整比較圖使用：

    blender -b -t 1 --python-exit-code 1 -P render_review.py

七張終圖與兩張原材料同相機圖，均為 Cycles CPU、96 samples、單執行緒、900 × 800、無降噪、無文字印記。兩組原色比較只還原面材質索引，相機位置、旋轉、正交尺度與照明數值相同。

[逐點逐面與材質驗證](appearance-review-v2/model-verification.json)、[完整面界審核](appearance-review-v2/boundary-continuity-audit.json)、[乾淨重建](appearance-review-v2/clean-rebuild-equality.json)、[九圖人工檢視](appearance-review-v2/color-continuity-review.json)分別記錄。新 3MF 與 BLEND 的頂點、三角連接、材料索引逐一核對；原有色面的所有材質數值不變。

原 validate_model.py 與 validate_sections.py 在獨立目錄以原樣腳本與固定版本依賴重跑通過，包含參數重建 STL 雜湊、原 scene/STL 同形、封閉拓撲及 465 層 canonical 截面。0.8 mm opening 最大損失為 0.2235%，仍保留原限制。[數位 QA 摘要](appearance-review-v2/original-qa-rerun-summary.json)。未做 Cura／Prusa 工具路徑、全局最小壁厚保證、實體試印或多色設備映射。斜罩、深窗及柱廊頂仍需支撐與拆除評估。

新 appearance.blend 無文字物件、文字區塊、外部照片、linked libraries 或絕對渲染路徑。原 appearance-review 保留 v1 歷史，本輪有效檢查位於 appearance-review-v2。

## 發布狀態

僅本機準備，未建立 GitHub blob／commit／PR／ref、未發布及未遠端讀回。使用固定基底 123e103381f4d7eb98627857d9b720b8e497ecaa；最新 HEAD 重查在先前拒絕後未重試或繞道。校級 SHA256SUMS 未改，之後若獲允許發布須重核最新基底並合併校級校驗檔。本輪不聲稱已完成發布。
