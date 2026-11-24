# 發布版校驗與版本範圍

現行是局部外觀：原右端外壁及角柱前面 10 磚色面保留，角柱 +X 外側增 5 面，合計 15 暖磚／1,201 中性。原 1,216 面及幾何不變，套件數不增加。中性表示未驗證，不代表實景灰。照片僅支持這一側的名義材族延續，未試印或新切片。現行材質統計見 `appearance-materials.json`；已完成的獨立 QA 適用於本次保留不動的模型與預覽。原 QA 原文（包括製作時仍待獨立審查的狀態）保留，未當成新進行的測試。

- `sha256sum --strict -c SHA256SUMS` 核對此次發布清單（不含校驗檔本身）。
- `FREEZE-MANIFEST.json` 列此次發布內容，排除自身與外層 `SHA256SUMS`。
- `RETURN-MANIFEST.json` 列此次發布內容，排除自身和上述兩個外層校驗檔；原獨立 QA 對應的凍結清單 SHA 另外明列。
- 原版 `SHA256SUMS`、`FREEZE-MANIFEST.json`、材質統計和 README 保留在 `return-baseline-inputs.zip`，ZIP 與其輸入鎖未改。
- 既有 `previews/` 是保留的舊版附圖，未納入本次清單；以建築根目錄十張圖為此次版面。未發布參考原圖或 PDF。
