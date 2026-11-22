# 現行展示與不可變更的交付快照

本次只更新兩份等同 README 的展示連結，增加現行模型的 WebP 圖，原模型、渲染 PNG 與審核檔不動。現行下載檔案及 README 使用根目錄 `SHA256SUMS`；WebP 大圖、縮圖與重渲染證據使用 [展示校驗](display/SHA256SUMS)。來源快照調和的凍結清單保持原檔，驗證其原始 README／CHECKSUM-SCOPE 時請從 [WebP 更新前的固定提交](https://github.com/hplin50643/taiwan-buildings-3d/tree/6f305e2967d5670c894ae535fa590a3df5c40679/%E5%9C%8B%E7%AB%8B%E8%87%BA%E7%81%A3%E5%A4%A7%E5%AD%B8/%E6%A0%A1%E7%B8%BD%E5%8D%80/buildings/ntu-main-library) 取出同一快照的檔案，不拿目前的展示文件混驗。

# 來源快照調和補充為準

本版本新增 [來源快照調和說明](SOURCE-REVIEW-RECONCILIATION.md) 及逐檔驗證 JSON。原獨審 SOURCE-QA 雜湊僅對應另存的審核時快照，不驗證目前同名來源檔案；原報告本身保持不變。新根 SHA256SUMS 及 SOURCE-REVIEW-RECONCILIATION-FREEZE-MANIFEST.json 核驗補充版本，原 scope FREEZE、原根表別名及原獨審維持原版本作用域。以下原說明中「當次」須依上述快照／最終檔案區別解讀。

# 鐘亭外域撤色勘誤校驗範圍

本次只將已確認跨越真實材界的完整8面外共面域撤回中性，不新增觀察色；原三角、STL、OBJ與建模程式不變。

- 根目錄 SHA256SUMS 核對所列本次檔案，不包含各SHA256SUMS本身與本次BELFRY-WITHDRAWAL-FREEZE-MANIFEST。
- BELFRY-WITHDRAWAL-FREEZE-MANIFEST.json 綁定全部本次交付檔案，不自包含；私人來源PDF/照片、比較圖、日誌與.blend1不公開。
- 舊FREEZE-MANIFEST、INDEPENDENT-COLOR-VISUAL-QA及qa/belfry-withdrawal-previous的資料保留為歷史，不代表本次檔案通過舊校驗。
- 本次以BELFRY-WITHDRAWAL開頭及重新產生的COLOR、SCENE、FRAMING、NO-TEXT、DELIVERY QA為準。

原混材共面域107減為106，其餘106域保持原面和索引，不宣稱全模型材界正確。16內返方案HOLD仍未放行。來源拍攝日期未確定，非當前現況或測繪認證，未實際列印。
