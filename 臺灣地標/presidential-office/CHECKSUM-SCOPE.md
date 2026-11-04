# 校驗版本說明：當前交付補充

本檔為 append-only 發布補充。原凍結模型、幾何、材色、歷史文件與兩份校驗表均未修改。

- `SHA256SUMS.txt` 是原版歷史校驗表，保留原位元組，不是新增色版的完整校驗入口。下列精確項目不追認為當前檔案通過（NOT_RECERTIFIED）；其餘項目仍照表驗證。
- 無副檔名的 `SHA256SUMS` 核對其所列的當前檔案，不含自身與 FREEZE，也不宣稱涵蓋這次新增的兩份發布補充。
- `PUBLICATION-SUPPLEMENT-MANIFEST.json` 記錄全部原凍結公開 payload 與本說明的大小、SHA256、Git blob SHA；它不循環包含自身，其位元組由發布 Git commit 與批次交付 manifest 綁定。
- 此說明只釐清校驗版本，不提高原來源、幾何、材色、數位 QA 或實體列印可信度。完整限制仍見原 README。

## 原歷史表中不適用於新色版的精確項目

- `README.md`：舊表 SHA256 `71b65b98b5c24217126727d68b9f761f41c03ed142a078205e6c348432600d06`；當前 SHA256 `aaace2381f3404e7f9eb7403ddee237bc888a0f53b53c8e80e71dfc804a7da7e`。舊項 NOT_RECERTIFIED，當前值由新 `SHA256SUMS` 與交付 manifest 核對。

[返回模型說明](README.md) · [當前檔案校驗表](SHA256SUMS) · [發布補充清單](PUBLICATION-SUPPLEMENT-MANIFEST.json)
