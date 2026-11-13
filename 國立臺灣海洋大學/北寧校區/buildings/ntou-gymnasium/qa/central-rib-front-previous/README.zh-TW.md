# 海大北寧體育館｜小門棚前緣局部灰

**局部材色未完成全館補色；原 strict false / run_checks exit1 與有限例外全部保留。** partial_color_incomplete=true、fully_colored_exterior=false。只小門棚前緣完整2面名義灰，其餘5628面中性；本次同幾何材色QA不是全域最薄壁、零警告或試印合格背書。

| 總覽 | 背側 | 正面 |
|---|---|---|
|![總覽](preview.png)|![背側](rear.png)|![正面](front.png)|
|![背面](back.png)|![西側](west.png)|![東側](east.png)|
|![頂面](top.png)|![小門棚完整前緣](entry-detail.png)|![近端](facade-detail.png)|
|![遠端](roof-detail.png)|||

## 材色及原件
同 ntou-gymnasium 原項目，國立臺灣海洋大學北寧校區體育館場側修版，same-item、count_delta=0，非新棟。原5630三角/STL/build_model.py及107原件字節保留，immutable無OBJ，不新造OBJ。原150×111×41.9mm含底有界近似非測繪、非全校完成。
原 add(-38.5,-29.7,11.7,7,5.5,1) 小棚前緣 y=-32.45 整plane恰2三角，x[-42,-35]z[11.7,12.7]完整矩形；全3頂點有限界1e-5，wholeplane等於finite，單共享邊component，不人工裁色。灰是名義色族不是測量RGB或金屬種類認證。
其餘5628面未知中性：實景通透格棚被原厚實盒簡化，頂/底/側返/小柱不塗；中央大柱底被人遮、字帶/混磚灰主牆/13紅肋未知回返/玻璃與窗背/屋面背側末端全不擴色。不公開照片、不建人物、不貼紋理。

## 必留原 strict 失敗與限定裁定
原 strict false 與 run_checks.py exit1 維持，不改閾值或原幾何。60原Polygon opening loss>1%（24端肋、36上肋末端），峰5.1513425349%，保留94.8486574651%。56300原面密點中1227短首弦，最小0.0000335533604338mm；既有連續根最短6.65393095985mm、真邊距最大0.782656059265mm只是有限補證，不等於全域最薄壁。
12射線/24原三角包含沿面區間，原8 parity flags在其中；沿面不是體積空氣，面上winding0/1不裁定內外。528非邊界控制通過，72面上值僅診斷。原 INDEPENDENT-REVISION-AUDIT.md、所有107檔與early failure/有限裁定歷程原樣留存，不將警告改綠，不重新背書原全QA。
底座朝下、曲殼/入口/小棚可能需支撐，細柱/窗框/肋端及縮放需獨立評估。未實體試印、未切片器工具路徑驗證。本次 watertight/單體積/材色重建通過只證交付不改原幾何，不能消除以上限制。

## 原展示與新版本
原單材scene另存 ORIGINAL-SOURCE-GAP-scene.blend、README另存 ORIGINAL-SOURCE-GAP-README.md，原render_preview.py/previews與全部原QA/early failure檔不改。新scene與appearance.3mf為有據2面局部材色；不是對原幾何修版或全模型准印。

## 來源日期
親看官方正面與作者斜近照，完整小門棚外前邊採作者照，官方正照左端裁切只對位。EXIF DateTime2026-04-21、官方頁更新2026-04-22不是獨立驗證拍攝日；原來源列作者2026-03-19亦保留未獨立認證，不稱2026全館現況。照片私人保存不公開，未確認CC/商用授權。

## 格式與本輪QA
[原STL](model.stl) · [逐面3MF](appearance.3mf) · [新Blender](scene.blend)
物件 NTOU Gymnasium partial color。STL無色；3MF/scene不是四色耗材切片或試印認證。原build_model.py→colorize_model.py→export_appearance.py→validate_color.py；render_color.py/verify_color_scene.py。隔離Shapely2.1.2原build+color精確重建、原bytes/全三角multiset/有限共面域/3MF/scene重開/十圖1200×900/hash，均限本次材色交付。

## English scope
Partial only:2 complete small door-canopy front fascia triangles nominal gray;5628 unknown neutral. Original5630 triangles/107files retained,no originalOBJ. Original strict false/run_checks exit1 retained with60 polygon-loss exceptions,1227 short first chords and12 along-face rays. Color identity and watertight checks are NOT global minimum-wall, zero-warning or physical-print certification. All early failures/adjudication history unchanged. Sameitem/count0,no geometry repair. Photo EXIF/page/original-attributed dates unverified as capture,not verified2026 condition.
