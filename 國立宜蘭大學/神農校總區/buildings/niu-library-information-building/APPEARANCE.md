# 宜蘭大學圖書資訊大樓｜完整原面延伸補色 v2

## 本次變更

把 3,195 個原中性三角面改用原有材料，包含 3,013 個淡灰白外牆／女兒牆外側／原窗凹口實牆回折面，以及 182 個既有後端、回折、斜側窗洞的灰綠不透明混合窗背面。使用原模型已有的完整構件面界，所有頂點都必須落在明確支撐範圍及平面內，並核對面法向，沒有面中心選取、任意切面或新開窗。

後端、回折與斜側的外觀不是直接照片證實，而是根據同棟已見正面／右側的材料族作合理連續性推估。原後窗位置本來就近似，本次未把它們改稱已確認現況。窗背色綜合玻璃、窗框、窗簾、陰影與反光，是不透明混合表觀，不是純玻璃認證。

6,549 個原有色面、六種原材質的 RGBA、Base Color 與 roughness 全保留；4,892 頂點、10,120 三角面、109 × 150 × 82.1 mm、transform 不變。原 STL、OBJ、scene.blend、幾何生成器、五張 previews 及歷史 QA 保留。本輪不改校級校驗檔及學校代表圖。

## 實際檢視的來源

本輪親看[校方《校園變遷》PDF](https://lic.niu.edu.tw/var/file/10/1010/img/8/211903019.pdf)實體第 18–19 頁（印刷頁 162–163），使用同批先前已下載且雜湊確認的官方原檔，不重複下載 22 MB PDF。跨頁大圖是同一張兩面高角度照片，不算兩張獨立視角。舊學寮、廚房照片不拿來替本館配色。

另重新下載並親看[國際事務處入口照片](https://isa.niu.edu.tw/var/file/73/1073/img/facilities-library-1.jpg)。兩來源支持正面與右長側淡灰白磁磚，既有灰褐遮陽片及灰綠混合窗背。本輪將這些材料延伸到同棟完整外牆、窗洞實牆回折與已存在窗背，明示隱蔽面與另一側為推估。

照片日期未註。2004 年竣工紀錄及 PDF 建立時間都不是攝影日，不宣稱 2026 現況。入口新照的紅橙多色與文字跨原階梯面內、缺少對應界線，故保留原校史灰階梯與扶牆，不把整級塗紅或新增字。其餘平面圖、館舍用途頁、消防表與較新工程紀錄本輪未重讀。來源雜湊、閱覽範圍見 [source-register.json](appearance-review-v2/source-register.json)。不散布來源照片或 PDF，不嵌照片貼圖。

## 保留中性的具體界線

仍有 376 面保持原中性，包括人工底座、屋頂平台、女兒牆內側／頂面、屋頂設備、低階梯側／底面，以及入口穿廊內未能區分材料或混合構件的面。對這些面沒有足夠完整材料界，沒有跨面內界線塗色，也未將真正開放穿廊變成窗。

原已識別外牆與窗凹口不因歷史文件稱「未知」就禁止連續性補色；本次逐面篩選有完整幾何支撐的範圍。中性面不是已確認實物灰色，已補色也不表示四面測繪或精確材質調查。磁磚縫、細框、招牌、空調、光電、植物及新窗列都不新增。

## 重建與驗證

原 scene.blend、model.stl 與更新 build_appearance.py 同層，使用 Blender 4.3.2 執行：

    blender -b -t 1 --python-exit-code 1 -P build_appearance.py

產生彩色 BLEND、Core 3MF、逐面材質索引及七角度圖。可加 -- --skip-render 跳過圖像。再執行：

    blender -b -t 1 --python-exit-code 1 -P render_review.py

產生七張終圖及兩張還原原色的前／後同相機比較。全部 Cycles CPU、96 samples、單執行緒、900 × 800、無降噪、無文字印記。原色比較只有面材料索引不同，相機位置、旋轉、正交尺度與照明完全相同。

[逐點逐面幾何及材質驗證](appearance-review-v2/model-verification.json)、[完整面界審核](appearance-review-v2/boundary-continuity-audit.json)、[乾淨重建](appearance-review-v2/clean-rebuild-equality.json)和[九張圖片人工檢視](appearance-review-v2/color-continuity-review.json)分開記錄。原數位 QA 已在獨立目錄原樣重跑：[摘要](appearance-review-v2/original-qa-rerun-summary.json)包括 411 個 0.2 mm 取樣層、83 個薄特徵取樣層及約 0.0502% 最大 opening 損失，無 >1% 取樣層。

數位 QA 不等於切片工具路徑或實體試印。入口雙層穿廊、雨棚與遮陽片仍需支撐、橋接及支撐拆除評估，不保證任意縮放、免支撐可印、結構安全或設備材料映射。3MF 無 AMS／耗材／機台設定。

新 appearance.blend 無文字物件、文字區塊、外部照片或 linked libraries，render 路徑為相對路徑。公開變更包無來源照片、私人參考檔與本機絕對路徑。原 appearance-review 是 v1 歷史，這次的有效驗證在 appearance-review-v2。

## 發布狀態

只在本機準備，未發布、未建立 GitHub blob／commit／PR／ref。固定基底 123e103381f4d7eb98627857d9b720b8e497ecaa；最新 HEAD 重查因先前拒絕未重試。後續發布仍須在授權允許時重核最新基底、合併校級校驗檔並真正遠端讀回；本輪不宣稱已完成這些步驟。
