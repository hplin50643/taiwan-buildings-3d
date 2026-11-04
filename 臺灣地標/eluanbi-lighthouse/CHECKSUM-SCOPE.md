# 校驗版本說明：當前交付補充

本檔為 append-only 發布補充；原模型、幾何、材色、原凍結資料及兩校驗表均未修改。

- `SHA256SUMS.txt` 屬原版歷史表。下列精確舊項對當前色版 NOT_RECERTIFIED，不能視為新檔校驗通過；其餘項仍照表核對。
- 無副檔名 `SHA256SUMS` 核對所列當前檔案，不含自身與 FREEZE，也未回填本次兩份追加補充。
- `PUBLICATION-SUPPLEMENT-MANIFEST.json` 綁定全部原凍結公開 payload 與本說明的大小、SHA256、Git blob SHA；不自循環包含自身，其位元組由發布 commit 與外層交付 manifest 綁定。
- 本補充不提高來源材色、幾何、數位 QA 或實體列印可信度；原限制仍見 README。

## 精確歷史項

- `scene.blend`：舊 SHA256 `eba743674513ee7f86333acccbb889a13c6ed5e62387237d5ad34efa43c2163e`；當前 SHA256 `f5a1dd2404b4f0376774655ac3730aba1a0494f56899f4bdbf0695b4c3ec22da`。原項 NOT_RECERTIFIED，當前值由新表與交付 manifest 核對。
- `README.md`：舊 SHA256 `3552fcfeb8686042df1c978d43c3a77d68986a94a8d33749f8664309515ebc01`；當前 SHA256 `003dc46ea47552602b30dd1a981c419676b2e62cee93ec998376b0f45349f9c5`。原項 NOT_RECERTIFIED，當前值由新表與交付 manifest 核對。

[返回模型說明](README.md) · [當前校驗表](SHA256SUMS) · [發布補充清單](PUBLICATION-SUPPLEMENT-MANIFEST.json)
