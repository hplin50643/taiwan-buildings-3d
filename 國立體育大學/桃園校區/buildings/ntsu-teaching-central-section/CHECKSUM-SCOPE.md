# 校驗版本說明：當前交付補充

本檔為 append-only 發布補充；原模型、幾何、材色、原凍結資料及兩校驗表均未修改。

- `SHA256SUMS.txt` 屬原版歷史表。下列精確舊項對當前色版 NOT_RECERTIFIED，不能視為新檔校驗通過；其餘項仍照表核對。
- 無副檔名 `SHA256SUMS` 核對所列當前檔案，不含自身與 FREEZE，也未回填本次兩份追加補充。
- `PUBLICATION-SUPPLEMENT-MANIFEST.json` 綁定全部原凍結公開 payload 與本說明的大小、SHA256、Git blob SHA；不自循環包含自身，其位元組由發布 commit 與外層交付 manifest 綁定。
- 本補充不提高來源材色、幾何、數位 QA 或實體列印可信度；原限制仍見 README。

## 精確歷史項

- `README.md`：舊 SHA256 `f3512cb92878e0c4d2d76b8f35dc418e164545a88fb3d84e6e1938415b741e72`；當前 SHA256 `5ecaf6a7fe86e5008040e770b3f6161245a53ea1a6bd4a471ef28da149a28423`。原項 NOT_RECERTIFIED，當前值由新表與交付 manifest 核對。
- `scene.blend`：舊 SHA256 `1ee62dbb06169e45ba6c2ff863b86febeafdaec36f913b1005dc3c403d492545`；當前 SHA256 `3363e65c22d2dee89093e8b3cf2a3e6896c2da61571185779e134087fa7a8ba2`。原項 NOT_RECERTIFIED，當前值由新表與交付 manifest 核對。

[返回模型說明](README.md) · [當前校驗表](SHA256SUMS) · [發布補充清單](PUBLICATION-SUPPLEMENT-MANIFEST.json)
