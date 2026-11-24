# 成大未來館現存前棟：現版外觀與重建

[現版五視角 WebP 與下載](../README.md) · [來源及限制](SOURCES.md) · [授權](LICENSE-NOTICE.md) · [技術渲染證據](../render-proof.json)

現版為 2026-11-14 的定界材色修正：現存前棟 5,044 三角面幾何不變，18 個原中性入口內側面改用既有材質；共 529 面外觀代理、4,515 面未查證中性。未更改地坪、樓梯、側牆或屋頂，不代表實測原色或實體列印。

下載[原樣的可離線重建 ZIP](rebuild-source.zip)，解壓後依 appearance/source/requirements-current.txt 安裝依賴並從解壓根目錄執行：

```sh
python -B appearance/source/build_current.py
python -B appearance/source/verify_current.py
blender -b -t 4 --python-exit-code 1 --python appearance/source/render_current.py
```

[完整 11 月發布說明、證據界線及原生場景](https://github.com/hplin50643/taiwan-buildings-3d/blob/c7b49cd7bd8b5a7d842c4e41f30a46f5bb0e8551/%E5%9C%8B%E7%AB%8B%E6%88%90%E5%8A%9F%E5%A4%A7%E5%AD%B8/%E5%8B%9D%E5%88%A9%E6%A0%A1%E5%8D%80/buildings/future-venue-front/appearance/README.md)以前版不可變檔案保留。[舊單色／原外觀對照及舊校驗](https://github.com/hplin50643/taiwan-buildings-3d/blob/aedc01f56772525b942a46a0cf63eee23adee46e/%E5%9C%8B%E7%AB%8B%E6%88%90%E5%8A%9F%E5%A4%A7%E5%AD%B8/%E5%8B%9D%E5%88%A9%E6%A0%A1%E5%8D%80/buildings/future-venue-front/appearance/README.md)不是現版展示。
