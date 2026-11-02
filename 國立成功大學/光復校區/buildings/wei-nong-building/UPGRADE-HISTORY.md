# 唯農同項目品質更新與保留舊檔

2026-11-02 更新既有 wei-nong-building；套件數增加 0。新幾何、程式、10張渲染與QA均以本目錄 README.md、freeze-manifest.json、SHA256SUMS 為準。

舊發布 commit 0880c2105d09c6283ab3f7a7e1c213f43251d27e 可追溯更新前檔案；Git歷史不刪除。以下原有輔助檔原樣保留，**屬舊版，不能用其舊截面、薄件檢查或預覽認證新版模型**，不應替代新版重建入口 build_model.py + geometry_helpers.py：

- `check_thin.py`
- `cross_sections.json`
- `previews/elevation.png`
- `previews/front.png`
- `previews/rear.png`
- `render_preview.py`
- `requirements.txt`
- `sources.json`
- `thin-feature-check.json`
- `validate_sections.py`
- `validation.json`

學校層級早期 model-manifest.json、bundle-validation.json、inventory.json 及批次 manifest 是歷史快照，本次不覆寫；現行索引是 model-index.json。本次不是物理試印、現況測繪或所有舊檔重新認證。來源原圖與私人參考仍不公開。
