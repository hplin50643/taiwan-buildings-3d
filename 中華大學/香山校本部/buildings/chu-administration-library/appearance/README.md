# 中華大學行政暨圖資大樓｜現行限域外觀

## 模型預覽

| 模型預覽 | 模型預覽 | 模型預覽 |
| :---: | :---: | :---: |
| ![現行正面](previews/front.webp)<br>正面 | ![現行左側](previews/left.webp)<br>左側 | ![現行右側](previews/right.webp)<br>右側 |
| ![現行背面](previews/rear.webp)<br>背面：北窄坡有限補色 | ![現行俯視](previews/top.webp)<br>頂視 | |

[現行 3MF](chu-administration-library-appearance.3mf) · [現行 Blender](scene.blend) · [原 STL](../model.stl) · [當前校驗表](../CURRENT-SHA256SUMS) · [渲染來源與視角](render-proof.json)

現行版為同一棟既有模型。四個材質槽中，原 204 面前窗背、18 面南坡、8 面上前帶，共 230 面保留；再加 18 個完整北窄坡三角面，沿用既有南坡紅瓦近似色。合計 248 面有配色，19,432 面維持未知中性。這是成對屋坡同材延續的推估，不是獨立北立面照片確證、完整外牆復色或現況。未塗屋頂其他部位、主牆、冠部及簷邊。原 STL 位元、9,830 頂點、19,680 三角面、面序及 150 × 100 × 約 61.8 mm 尺度不變。不含鄰棟國際會議廳。

原幾何以公開外觀及校方資料作有限近似，未測繪、未實體試印。原檢查仍是 all-checks passed=false，兩程式非零退出、10 項局部例外及環根支承 71.6256% 未抹除；不能把局部例外或某一冠部的 100% 與整體放行混稱。來源原照只作私人核對，不附於套件。

[北窄坡獨立域核對](qa-continuous-walls/independent-domain-review.json) · [交換核對](qa-continuous-walls/exchange-validation.json) · [原來源與限制](SOURCES.md) · [授權限制](LICENSE-NOTICE.md)

## 重現與歷史

現行三個模型格式可以獨立開啟。需要重建時，在暫存目錄解壓[獨立重建源碼](rebuild-continuous-source.zip)，依該包依賴以 Python 執行 `appearance/source/build_continuous_walls.py`；交換使用 `verify_continuous_exchange.py`，Blender 4.3.2 使用 `render_continuous_walls.py`。原重建流程的 PNG 中間檔只在暫存處用於校驗，不作公開預覽。現行 WebP 由最新已發布 Blender 場景直接重渲，不改材色。

[原 230 面說明及單色 QA 對照](https://github.com/hplin50643/taiwan-buildings-3d/blob/cb5044f0a43e95502514e7da26c07ba0494bc980/%E4%B8%AD%E8%8F%AF%E5%A4%A7%E5%AD%B8/%E9%A6%99%E5%B1%B1%E6%A0%A1%E6%9C%AC%E9%83%A8/buildings/chu-administration-library/appearance/README.md)、[前次外觀校驗](https://github.com/hplin50643/taiwan-buildings-3d/blob/cb5044f0a43e95502514e7da26c07ba0494bc980/%E4%B8%AD%E8%8F%AF%E5%A4%A7%E5%AD%B8/%E9%A6%99%E5%B1%B1%E6%A0%A1%E6%9C%AC%E9%83%A8/buildings/chu-administration-library/appearance/CONTINUATION-SHA256SUMS)和[固定整包校驗](https://github.com/hplin50643/taiwan-buildings-3d/blob/cb5044f0a43e95502514e7da26c07ba0494bc980/%E4%B8%AD%E8%8F%AF%E5%A4%A7%E5%AD%B8/%E9%A6%99%E5%B1%B1%E6%A0%A1%E6%9C%AC%E9%83%A8/buildings/chu-administration-library/PUBLIC-MODEL-SHA256SUMS)只供歷史驗證，不是現行3MF、場景或預覽的下載入口。歷史報告與原重建流程以固定提交保全，不改內容。
