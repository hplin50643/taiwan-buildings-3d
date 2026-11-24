# 發布版校驗與版本範圍

現行僅局部補色：染色 74 面（原正面 48＋靠門窗框 −X 外頰 26），中性 5,176 面，共 5,250 面；原幾何不變，模型數不增加。原狀文字與舊 QA 留作歷史紀錄。現行材質統計見 `appearance-materials.json`，本次幾何、材質、來源及預覽驗證以 `CHEEK-QA.json`、`CHEEK-SOURCE-SCOPE.json` 與 `CHEEK-PREVIEW-RECEIPTS.json` 為準。舊版可由公開原件重建基準 ZIP 查閱。

- `sha256sum -c SHA256SUMS`：校驗本次發布清單（不含校驗檔自身）。
- `FREEZE-MANIFEST.json`：現行發布檔案清單與 SHA-256，排除自身及外層 `SHA256SUMS`。
- `CHEEK-MANIFEST.json`：校驗本次發布內容，排除自身與上述兩個外層校驗檔。
- 既存的 `previews/` 是舊版附圖，不屬於這次清單且保留不動；以建築根目錄的十張預覽為本次版本。

現行可執行 `python validate_color.py`，採唯讀方式檢查校驗、對照基準 NPZ、核對 3MF 與面材統計，不重建、不寫 QA。舊產色與重建／寫入型校驗腳本不應對發布根目錄執行；原始腳本仍可在另解壓的歷史基準中查閱。

本次只同步發行文件與校驗清單，模型、材質交換檔和十張公開預覽均與原凍結 QA 產品逐位元一致。參考原圖不公開。
