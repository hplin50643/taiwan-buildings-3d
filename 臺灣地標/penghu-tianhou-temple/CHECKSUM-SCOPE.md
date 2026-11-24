# 校驗版本說明：現行 WebP 與固定歷史
- 現行 `SHA256SUMS` 核對目前資料夾內的公開檔案（不含校驗表自身）。展示圖的檔案 SHA-256、尺寸與解碼 RGBA SHA-256 另由 `verify_display_webp.py` 依未改寫的展示渲染紀錄核對。
- 原 `FREEZE-MANIFEST.json`、`PUBLICATION-SUPPLEMENT-MANIFEST.json` 和 `SHA256SUMS.txt` 保留原位元組但不拿來核對現行目錄。請在[固定原局部材色交付版本](https://github.com/hplin50643/taiwan-buildings-3d/tree/cd2698cb09b3b73d7e4ce5ea46304c1f1f1d8ef6/%E8%87%BA%E7%81%A3%E5%9C%B0%E6%A8%99/penghu-tianhou-temple)下載原 README、原校驗表及十張展示 PNG；該版本可直接核對原無副檔名 SHA256SUMS。原凍結清單及追加發布清單原先各有同樣 15 項與此公開版本不一致（十張展示 PNG、兩校驗表、`DELIVERY-QA.json`、`render_color.py`、`scene.blend`），不宣稱該清單已通過；未修改兩份歷史清單。原單色歷史表也未重新認證。
- [固定既有 WebP 發布版本](https://github.com/hplin50643/taiwan-buildings-3d/tree/0026a5ef79b7fbbf6a3e49690ec72721fea6c153/%E8%87%BA%E7%81%A3%E5%9C%B0%E6%A8%99/penghu-tianhou-temple)仍含原展示頁與原展示校驗表。兩個歷史的 `previews/*.png` 不是現行展示圖，也不是這十張的逐像素等同替代對象；保留原檔。
- 本次不改模型、材色、幾何、渲染器或重建腳本。屋瓦和彩繪未完成、未實際試印。
