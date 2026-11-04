# 校驗版本說明：當前交付補充

本檔為 append-only 發布補充；原模型、幾何、材色、原凍結資料及兩校驗表均未修改。

- `SHA256SUMS.txt` 屬原版歷史表。下列精確舊項對當前色版 NOT_RECERTIFIED，不能視為新檔校驗通過；其餘項仍照表核對。
- 無副檔名 `SHA256SUMS` 核對所列當前檔案，不含自身與 FREEZE，也未回填本次兩份追加補充。
- `PUBLICATION-SUPPLEMENT-MANIFEST.json` 綁定全部原凍結公開 payload 與本說明的大小、SHA256、Git blob SHA；不自循環包含自身，其位元組由發布 commit 與外層交付 manifest 綁定。
- 本補充不提高來源材色、幾何、數位 QA 或實體列印可信度；原限制仍見 README。

## 精確歷史項

- `README.md`：舊 SHA256 `46204ccf7d3a6370a3c688bb3ea04fed2a7fea601350352cf03aee7bf3bab385`；當前 SHA256 `08dcc383b5a7c07e2c334fc952d6931cf4e990734bfbd6b5df627bfd448fec50`。原項 NOT_RECERTIFIED，當前值由新表與交付 manifest 核對。
- `scene.blend`：舊 SHA256 `6685c4c6591945de6947ab2a1d65845617fcf95a7e148ac2133a8d41a0b655c6`；當前 SHA256 `33c2b7b3689fcb57aa43f3f57201082eed42df14c999aecedda1a33e06f94023`。原項 NOT_RECERTIFIED，當前值由新表與交付 manifest 核對。

[返回模型說明](README.md) · [當前校驗表](SHA256SUMS) · [發布補充清單](PUBLICATION-SUPPLEMENT-MANIFEST.json)
