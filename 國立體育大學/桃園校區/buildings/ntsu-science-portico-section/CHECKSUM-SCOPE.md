# 校驗版本說明：當前交付補充

本檔為 append-only 發布補充；原模型、幾何、材色、原凍結資料及兩校驗表均未修改。

- `SHA256SUMS.txt` 屬原版歷史表。下列精確舊項對當前色版 NOT_RECERTIFIED，不能視為新檔校驗通過；其餘項仍照表核對。
- 無副檔名 `SHA256SUMS` 核對所列當前檔案，不含自身與 FREEZE，也未回填本次兩份追加補充。
- `PUBLICATION-SUPPLEMENT-MANIFEST.json` 綁定全部原凍結公開 payload 與本說明的大小、SHA256、Git blob SHA；不自循環包含自身，其位元組由發布 commit 與外層交付 manifest 綁定。
- 本補充不提高來源材色、幾何、數位 QA 或實體列印可信度；原限制仍見 README。

## 精確歷史項

- `README.md`：舊 SHA256 `2b2683c60a595888dc4f65c7d9f5f1619e6cd37bbce0d17e5cdb46e9aecd14c8`；當前 SHA256 `feede0735a96d016b4708b90cb6348560a3010135696ff40569ea564a53a39ec`。原項 NOT_RECERTIFIED，當前值由新表與交付 manifest 核對。
- `scene.blend`：舊 SHA256 `50867259ac618a79ff84db633da99d5ed89d37881f53d66150cd7c09de6af0bf`；當前 SHA256 `3481925b89a4935e05074b462809812848a95d0749b4bb987ec861fad695160c`。原項 NOT_RECERTIFIED，當前值由新表與交付 manifest 核對。

[返回模型說明](README.md) · [當前校驗表](SHA256SUMS) · [發布補充清單](PUBLICATION-SUPPLEMENT-MANIFEST.json)
