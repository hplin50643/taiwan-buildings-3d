# 校驗版本說明：當前交付補充

本檔為 append-only 發布補充；原模型、幾何、材色、原凍結資料及兩校驗表均未修改。

- `SHA256SUMS.txt` 屬原版歷史表。下列精確舊項對當前色版 NOT_RECERTIFIED，不能視為新檔校驗通過；其餘項仍照表核對。
- 無副檔名 `SHA256SUMS` 核對所列當前檔案，不含自身與 FREEZE，也未回填本次兩份追加補充。
- `PUBLICATION-SUPPLEMENT-MANIFEST.json` 綁定全部原凍結公開 payload 與本說明的大小、SHA256、Git blob SHA；不自循環包含自身，其位元組由發布 commit 與外層交付 manifest 綁定。
- 本補充不提高來源材色、幾何、數位 QA 或實體列印可信度；原限制仍見 README。

## 精確歷史項

- `README.md`：舊 SHA256 `5d458acdd40c1e0f389111ef4349e6f0989346e475ab5ebc1afd96d5fac7bc66`；當前 SHA256 `fa8b26ef515bbca90dbfd95f2cd61432132fd1e2b0b3e4caed8e3ac731f9eea5`。原項 NOT_RECERTIFIED，當前值由新表與交付 manifest 核對。
- `scene.blend`：舊 SHA256 `64aaa9a090ad5dd022dd9435d27bbd12b3155d57709d8d3439059f2c7f39b2ec`；當前 SHA256 `d9c5b60090c40b11f500d25f1e45fbbc7bb5a36965731706d55543541e404b1d`。原項 NOT_RECERTIFIED，當前值由新表與交付 manifest 核對。

[返回模型說明](README.md) · [當前校驗表](SHA256SUMS) · [發布補充清單](PUBLICATION-SUPPLEMENT-MANIFEST.json)
