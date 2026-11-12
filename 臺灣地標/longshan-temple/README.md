# 艋舺龍山寺｜既有屋面側背補色

| 彩色預覽 | 彩色預覽 | 彩色預覽 |
|---|---|---|
| ![前斜視](preview.png) | ![後斜視](rear.png) | ![前面](front.png) |
| ![背面](back.png) | ![左側](west.png) | ![右側](east.png) |
| ![頂視](top.png) | ![三川殿前面](entry-detail.png) | ![鐘鼓塔](facade-detail.png) |
| ![中殿屋坡](roof-detail.png) | | |

## 補色範圍與可信度

同一既有龍山寺縮景，套數不增加（count_delta 0）。保留原 14,620 頂點、29,236 三角面、STL 位元組、build_model.py、物件位置／旋轉／縮放及尺寸 142 × 150 × 36.6500015 mm。這次修改材質索引，不重建原來的近似配置、屋脊、塔形或門洞。

- **同構件材色延伸，屬推估**：前殿、兩側入口與中殿既有橘瓦色，延伸到同一原屋面可辨識的側坡、後坡；兩座鐘鼓塔只延伸既有斜坡瓦殼，不染塔牆、垂直封邊或雕飾。
- **後殿屬同建物瓦色推估**：四組可辨的原後殿屋皮也延續既有橘瓦色族。寺方導覽標示 1998 年的後殿照片可見橘色系瓦列，作同族推估佐證；不是精確現況色證，並未逐一拍攝所有背坡。
- **側廊屬同類瓦色推估**：寺方鐘鼓樓照片可見鄰接側廊瓦色，對應模型既有側廊屋皮。不是每一整面都有實景逐面確證，也不是校色色票。
- 只改原中性材質的 **13,366 個完整三角面**：前／中殿 4,721 面、兩塔 270 面、側廊 1,483 面、後殿 6,892 面。原已彩色 7,043 面全部保留，原五種材質的名稱、RGBA、Base Color 與 roughness 0.72 不變。材質標籤的「front」與「UNVERIFIED」保留歷史識別，實際選面範圍以本頁與 continuity-map.npz 為準。
- **未把灰面一律當漏色**：前石材、凹影、屋脊剪黏粗塊、展示底座與融合幾何留下的水平片保留。另排除 836 個三頂點碰巧落在交線、但面內仍是水平牆／柱頂的中性片，並以面內取樣再排除 5 個原簡化網格中的近水平頂面；只在三頂點符合原屋面高度場、法線向上但不是水平牆／柱頂的原斜面上補瓦色，不用包圍盒或三角形中心強行拼色，也不新增彩繪界線。
- **已逐面核對可見灰楔與鋸齒**：中殿長灰楔在原 z=19.2 mm 水平牆／柱頂面；前殿與兩側入口細灰齒分別在原 z=17／15 mm 水平頂面。它們不是斜瓦面漏選，而是舊幾何的牆柱頂穿出曲屋緣，仍保留原中性色。後殿也套用相同的水平／近水平交會面排除。見 ROOF-INTERSECTION-QA.json 的原面 ID、法線及高度場誤差與 TILE-SURFACE-QA.json 面內取樣；這些灰形狀不代表實景漆色界線，本次不藉改色掩飾原幾何交會。
- **側背粗牆不刷色**：寺方導覽指出三川殿背面是開放式對看廳，原模型的封閉粗牆不能當成可實測的真實牆面。後殿門扇、雕飾與彩繪也不能套成整片牆色，這些仍中性；屋皮已獨立按同族瓦色推估補色。
- 官網舊實景照片未註完整拍攝日期或校色資訊。這是保守、明示推估的外觀補色，**不是現況測繪或歷史復原**。不新增龍雕、綠簷帶、金字、門窗、燈籠或室內陳設。

## 無字圖與模型

十張圖為同一 3D 模型實際多視角渲染，無字幕、無印記；沿用原去字版相機、鏡頭、構圖及照明。Cycles CPU、單執行緒、96 samples、不降噪。entry-detail、facade-detail、roof-detail 為有意裁切細部，其他七張通過完整模型邊界檢查。

[彩色 3MF](appearance.3mf) · [彩色 Blender](scene.blend) · [原 STL](model.stl)

STL 不帶色；3MF 使用五種基本材質標籤，不代表已完成四色耗材配色或切片。**未試印、未進行切片列印驗證**，不保證免支撐。

## 重建與檢查

保留原 build_model.py 建立幾何；colorize_model.py 先重現原前面材色，再只延伸原中性瓦坡；export_appearance.py 輸出基本材料 3MF；Blender 4.3.2 執行 render_color.py 生成十圖與 scene.blend。使用 numpy、trimesh、manifold3d；實際驗證環境版本見 CLEAN-REBUILD-QA.json。

依序執行：python build_model.py、python colorize_model.py、python export_appearance.py、blender -b -t 1 --python render_color.py、python validate_color.py。validate_color.py --rebuild 可另建立保留的乾淨重建目錄，核對幾何、原彩面、所有材質索引與 3MF XML；verify_color_scene.py 重新開啟 Blender 比對場景。

COLOR-FORMAT-GEOMETRY-QA.json、CLEAN-REBUILD-QA.json、ROOF-INTERSECTION-QA.json、TILE-SURFACE-QA.json、SCENE-QA.json、FRAMING-QA.json、NO-TEXT-QA.json 與 DELIVERY-QA.json 為本次檢查。歷史 monochrome／前面材色報告與 editable.blend 保留但不是本次彩色入口，不把舊報告當成本次通過證據。

## 來源與權利

寺方三川殿、中殿、後殿、鐘鼓樓實景與官方語音導覽，網址、影像雜湊、判讀／推估範圍見 [FACADE-COLOR-SOURCE-REGISTER.json](FACADE-COLOR-SOURCE-REGISTER.json)。官照只作私人比對，不隨模型上傳、不作模型貼圖。公開可讀不等於可再散布，未取得來源照片商用授權。本次獨立材質不是原照重製。
