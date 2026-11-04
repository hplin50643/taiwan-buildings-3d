# 校驗版本說明：當前交付補充

本檔為 append-only 發布補充；原模型、幾何、材色、原凍結資料及兩校驗表均未修改。

- `SHA256SUMS.txt` 屬原版歷史表。下列精確舊項對當前色版 NOT_RECERTIFIED，不能視為新檔校驗通過；其餘項仍照表核對。
- 無副檔名 `SHA256SUMS` 核對所列當前檔案，不含自身與 FREEZE，也未回填本次兩份追加補充。
- `PUBLICATION-SUPPLEMENT-MANIFEST.json` 綁定全部原凍結公開 payload 與本說明的大小、SHA256、Git blob SHA；不自循環包含自身，其位元組由發布 commit 與外層交付 manifest 綁定。
- 本補充不提高來源材色、幾何、數位 QA 或實體列印可信度；原限制仍見 README。

## 精確歷史項

- `scene.blend`：舊 SHA256 `dcfacfc287167ef8da3efb237103ccd0923b7e2a2d9cbb5171ce2025f003744c`；當前 SHA256 `bdf96f150c8419688d0873af1420e201be5014d2e07e1f853ea470d40f68f45c`。原項 NOT_RECERTIFIED，當前值由新表與交付 manifest 核對。
- `README.md`：舊 SHA256 `453b43492688a20281138e5b517019435f428c97c239316cf3ffc4831810f804`；當前 SHA256 `0d95fa42c0c8c704d825db50331496be01c2363e9db7b4642f09377bca05e63f`。原項 NOT_RECERTIFIED，當前值由新表與交付 manifest 核對。

[返回模型說明](README.md) · [當前校驗表](SHA256SUMS) · [發布補充清單](PUBLICATION-SUPPLEMENT-MANIFEST.json)
