# 北護學思樓2021｜七根南凸柱側返同材質延續

## 模型預覽

| 總覽 | 背側 | 正面 |
|---|---|---|
|![總覽](preview.png)|![背側](rear.png)|![正面](front.png)|
|![背面](back.png)|![西側](west.png)|![東側](east.png)|
|![頂面](top.png)|![完整北四排外框](entry-detail.png)|![西框union](facade-detail.png)|
|![東框union](roof-detail.png)|||

## 本次北護學思樓｜七根南凸柱完整側返有限補色

局部補色仍未完成。以目前 18 面北側中灰、16 面南凸柱淡白為固定原色基準，只將南面前七根凸柱的 14 個完整側返域，共 536 個原三角由未知中性 index 1 延續既有名義淡白 index 2（#E0E0D9）。現在材料面數為 [18, 17600, 552]，全 18170 原面、9041 原點與順序、STL、三色票原始 bytes 均不變；所有 17634 未選面不變。沒有切面、增加構件、補缺口或改尺寸。

中心 x = −65.5、−50.5、−35.5、−20.5、−5.5、9.5、24.5，各 x ±1.3 的側面，y −33.8 至 −32.4、z 11.5 至 78.3。每側為原 CSG 留下的完整缺口輪廓，不是隨意矩形塗滿：1.4×66.8 − 0.8×(0.8+8×1.2+0.4) = 84.88 mm²，14 域名義共 1188.32 mm²。原 float32 座標保留造成每域約 0.000147 mm² 差異，以 0.0003 mm² 容差核對，不 round 原點。各域整個 66.8 mm 前緣連接既有淡色前面，全 5448 共面連通域維持單一材。柱體另有 0.2 mm 埋入主體，沒有補出隱藏面。

第八根 x=39.5 與東側樓梯量體 union 複雜，兩側全不選，但原淡色正面保留。橫帶前面、頂底、窗凹面/背面、主牆、樓梯深色帶、地面柱、屋頂及其餘外牆均不改。這不是整棟染白，也不把北中灰鏡射到南。

來源：本次親看兩張校方操場南面照片，均重取並核對原登記 SHA256；承包商潤弘 2021 建築履歷 PDF 第 58 頁下圖輔助對位。同頁上圖是北面，不拿其顏色支持南面。照片可辨淡直柱與暗橫窗/凹口分離，本次 1.4 mm 側深、66.8 mm 全高延色是同一凸柱的有限推論，並非每面全深全高都由照片實見；局部樹遮與陰影不當作另一種建材。原柱幾何為粗化近似，顏色 HEX 未校準，也不是現況測量。官方圖片拍攝日期未確定；2021-10-01 是 PDF 文件日期、2024-08-15 是網頁存檔日，不是逐張拍攝日期，不聲稱 2026 現況。

原 SOUTH-PILASTER-SOURCE-QA 的 SOURCE_SCOPE_SUPPORTED_PENDING_FINAL_MODEL_REVIEW 狀態及所有舊 QA 原樣保留；本次兩道獨立有限域審核與新輸出、交換格式、場景 QA 分別另存 qa-continuous-pilasters，不回寫歷史狀態。原 22 根地面柱／890 個跨層角損警告樣本及原有限例外仍有效，890 不是柱數；本次不重新簽署原全部工程或製造 QA，未做 FFF 切片與實體試印。三展示材可編輯並不等於三料列印已驗證。

照片及原 PDF 僅私人核對，沒有打包、公開貼圖或假定再利用授權。重建使用固定 SHA 公開原 NPZ、原 STL 與 palette，執行 build_continuous_pilasters.py；輸出精確 3MF，另以 lib3mf strict 讀取及獨立修改往返、Blender 材質與單點改存重開、原交付場景重渲染比對、ZIP 隔離重建核對。原場景和新十視角是模型本身渲染，沒有文字覆蓋或私人照片。

下列原說明與統計為歷史記錄，若數量不同以本段及本次 QA 為準。

---

場景僅同步更新 source_mesh_sha256 以對應本次含 536 面材質指派變更的 color-mesh.npz；原 scope 與全部其他原屬性、完整材質定義及幾何不變。固定原 18 北灰面與 16 南柱正面全部保留，不回退舊版色域。七柱側返僅作同柱族材料延續推論，不把未建細縫、原簡化柱及遮擋區提升為測繪或逐面照片證實。其他未知後側中性、原工程與來源日期限制及未實印條件完整保留。三槽 palette.json 原 bytes 不變。

本頁為現行說明；根 README.zh-TW.md 保留原文與原 bytes，僅作歷史記錄。

## 前版說明與保留限制（完整歷史文字）

# 北護學思樓2021｜南面八凸柱正面有限淡白補色

局部補色未完成。保留原18北面中灰，新增南面八凸柱正面16原三角，共34配色、18136未知中性、18170原三角。原兩色票與所有未選索引保持，中性仍index1；新名義淡白#E0E0D9附於index2，不把北中灰鏡射到南，也不將中性普遍染白。

新查得校方操場南立面照片new-official-3(700×466)及9(865×315)顯示淺色直柱與深橫窗帶分離。原凸柱正面y=-33.8在橫帶y=-33.2前方，八個中心x[-65.5,-50.5,-35.5,-20.5,-5.5,9.5,24.5,39.5]各±1.3，z[11.5,78.3]，全頂點/法向與完整共面域驗證共16面。上部暗窗帶之間仍可辨淺色直條；部分下端樹遮採同柱有限連續推定，不宣稱每面或整高直接可見。原構件深度/尺寸近似不因配色成為測量結果，HEX未校準。

不取柱側返／頂底／背面、地面22柱、水平深帶、窗背、最高柵格、其他牆面、天井、雨棚、屋面設備。原2021身份、舊四種可讀性展示材歷程與全部aliases、工程檢核例外保持；890是跨層角損失樣本不是890柱，原22地柱及最大2.0436738%有限例外未獲新工程認證。校方文章刊登日不是照片拍攝日，不宣稱2026現況，原49.9m未分配建物的限制與2022疑鏡像照片不作定位的限制不變。

來源URL/hash見SOUTH-PILASTER-SOURCE-QA；兩照與裁切私人保存，不公開或作貼圖、不推定商用權。來源QA固定SOURCE_SCOPE_SUPPORTED_PENDING_FINAL_MODEL_REVIEW，最終獨審另檔。原文件/QA存qa/south-pilaster-previous，以下舊18面統計僅歷史，不代表本次。三展示材非已驗三料切片，未實體試印，無幾何或全域工程再認證，未發布。

## 原版說明與工程限制（原字節文字，以下統計為歷史）

# 北護學思樓2021｜北四排外框前面局部灰

**既有四材展示非實景全色；其餘未知域尚未完成分色。** partial_color_incomplete=true、fully_colored_exterior=false。僅北四排外框完整18三角名義中深灰，其他18152面中性。保留原22柱/890跨層角損有限例外，非新列印合格背書。


## 材色範圍
同 ntunhs-xuesi-2021 原項目，國立臺北護理健康大學石牌校區學思樓，same-item、count_delta=0。原18170三角/STL/build_model.py及30原件字節不變，immutable無OBJ。北向原模型+Y；預覽朝北，未依疑鏡像空拍重新定方位。
完整y=33.65外框plane恰18三角，四原矩形union成單共享邊連通域：兩豎x=-67/28.5,w1.8,z34..64.4及兩橫x=-19.2,w97,z34..35.5/63.3..64.8。全3頂點有限矩形聯集等於wholeplane，不人工切色。下方白柱y33.6不在域，不混染。
其餘18152面中性：框側後返、窗背/實板、南向不同柱橫帶、混灰白logo側牆、屋頂太陽能/設備、天井、地面柱/雨棚全不擴。

## 四材展示轉換
原scene四個neutral/depth/frame閱讀展示材不是原單色或已認證實景全色。新來源限定版本只18面；原scene/README公開另存 ORIGINAL-SOURCE-GAP-scene.blend／ORIGINAL-SOURCE-GAP-README.md，原render_preview.py/previews及所有原QA原bytes保留，舊深凹不解讀成黑玻璃。新色QA不追認原幾何/全模型列印品質。

## 必留原幾何及列印限制
原22根地面方柱對應890個跨層警告樣本，不是890根柱。最大角損約2.0436738%、保留97.9563262%；角損在0.41mm角鄰域，原局部法向射線最小2.5999984mm、角外殘差等全部保留原報告。這是具體位置有限例外，非全域最薄壁/零警告/工具路徑或實體試印合格。沒有修補幾何、沒有重簽原全部QA；支撐/縮放/切片仍需獨立評估。
施工履歷49.9m屬整案且未分學思與爾雅，不作本棟精確標高。2022疑鏡像航照不定東西；模型原有界比例、低層平面未全得與不同期來源限制照留。原主體11F+B2，地下不重建；含底150×78×90.5mm是示意非精測。

## 來源與日期
親看履歷PDF54下完工照、58上北向日照、59上日照；54上施工網及59下夜色排除，58下僅對位。2021承包商發表背景非逐張capture，2024archive是存檔時間非拍攝，不稱2026現況。原PDF/照片私存不公開不貼紋理、不建人，未確認CC/商用授權。

## 格式與本次QA
[原STL](model.stl) · [新逐面3MF](appearance.3mf) · [新Blender](scene.blend)
物件 NTUNHS Xuesi 2021 partial color；STL無色，3MF/scene非四色耗材切片/試印認證。原build_model.py→colorize_model.py→export_appearance.py→validate_color.py，render_color.py/verify_color_scene.py。隔離Shapely2.1.2原build+color精確重建/原bytes/全三角multiset/材域共面/3MF/scene重開/十圖1200×900/hash只驗本輪未改幾何及材色交付，不替代原有限例外或全域列印測試。

## English scope
Partial source-gap variant,not monochrome discovery:18 complete north outer-frame front triangles medium gray;18152 neutral. Original18170 triangles/30files unchanged,no originalOBJ. Four old display materials and scene/renderer/QA preserved. 22columns/890cross-layer corner-loss samples,max2.0436738percent is a retained finite local exception,not global minimum-wall or printability certification.49.9m project total not building-specific;2022mirror-suspect aerial not orientation evidence.2021publication/2024archive not verified capture or2026. Sameitem/count0,no geometry repair or physical print.
