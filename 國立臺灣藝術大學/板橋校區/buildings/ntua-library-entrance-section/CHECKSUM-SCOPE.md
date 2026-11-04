# 校驗版本說明：當前交付補充

本檔為 append-only 發布補充；原模型、幾何、材色、原凍結資料及兩校驗表均未修改。

- `SHA256SUMS.txt` 屬原版歷史表。下列精確舊項對當前色版 NOT_RECERTIFIED，不能視為新檔校驗通過；其餘項仍照表核對。
- 無副檔名 `SHA256SUMS` 核對所列當前檔案，不含自身與 FREEZE，也未回填本次兩份追加補充。
- `PUBLICATION-SUPPLEMENT-MANIFEST.json` 綁定全部原凍結公開 payload 與本說明的大小、SHA256、Git blob SHA；不自循環包含自身，其位元組由發布 commit 與外層交付 manifest 綁定。
- 本補充不提高來源材色、幾何、數位 QA 或實體列印可信度；原限制仍見 README。

## 精確歷史項

- `README.md`：舊 SHA256 `99ed8bd649029e37d31faf93b82815228ff84f6af5886a5ef63481461e18378b`；當前 SHA256 `3daf720c14220840be9681be2291567957e70f2108ce495ab9ffbaca621ca72b`。原項 NOT_RECERTIFIED，當前值由新表與交付 manifest 核對。
- `scene.blend`：舊 SHA256 `41e55b02112023e334cfd65d73df30399bc8b56a9b1042476c3d492c9ecf758f`；當前 SHA256 `2a0a1cb6aa4e263f739ef9e824ea13212b6479b416b5aa60407508b38f81ddb3`。原項 NOT_RECERTIFIED，當前值由新表與交付 manifest 核對。

[返回模型說明](README.md) · [當前校驗表](SHA256SUMS) · [發布補充清單](PUBLICATION-SUPPLEMENT-MANIFEST.json)
