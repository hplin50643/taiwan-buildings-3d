# 校驗版本與原檔交付範圍說明

本說明是追加的發布補充，未修改本機原凍結模型、README、舊校驗表或原 FREEZE-MANIFEST.json。此處未修改凍結原件不表示遠端同名根校驗表仍保留舊 bytes；根表新版取代與巢狀表保留的差異詳見下文。原凍結清單不包含本補充。

現行根目錄 SHA256SUMS 僅核驗其明列的當前檔案，不涵蓋其自身、原 FREEZE-MANIFEST.json 或本次補充。PUBLICATION-SUPPLEMENT-MANIFEST.json 另列原公開交付檔與本說明的 bytes、SHA256 及 Git blob SHA；補充清單本身依 Git commit 識別，不自我循環。

材色、年代、模型範圍與原 QA 限制仍依原文件；本說明不補簽列印性、歷史建成狀態或全實景材色認證。

## 歷史校驗表與精確公開別名

原 SHA256SUMS.txt 維持歷史 bytes。下列項目是原版路徑與摘要，不得用它們宣稱當前同名檔案已通過原版校驗（NOT_RECERTIFIED）。每列已將歷史摘要核對到公開的完整原檔別名；同名現行檔案仍須依新表及交付清單核驗。未列項目不獲豁免。

- 歷史表 `SHA256SUMS.txt`，表 SHA256 `5da4589bb8d342534ae58f2d9982f2e75f39c3fc23f27b647fa4725fbeef141a`；歷史 target `BUILD-QA.json`，SHA256 `6003140c1d05e2771de559c71327bd74219f9f679986ef9b67181bcca8edd04e`。當前同路徑 SHA256：`本批未提供此同名路徑`。
  公開完整歷史別名：[original-classification-version/BUILD-QA.json](original-classification-version/BUILD-QA.json)、[original-classification-qa-aliases/ORIGINAL-CLASSIFICATION-BUILD-QA.json](original-classification-qa-aliases/ORIGINAL-CLASSIFICATION-BUILD-QA.json)。
- 歷史表 `SHA256SUMS.txt`，表 SHA256 `5da4589bb8d342534ae58f2d9982f2e75f39c3fc23f27b647fa4725fbeef141a`；歷史 target `DOC-QA.json`，SHA256 `7d0f14ec795a9cbeeaba272097bac80a7f30803cc0a8d327a6fb469ec8c1c88c`。當前同路徑 SHA256：`本批未提供此同名路徑`。
  公開完整歷史別名：[original-classification-version/DOC-QA.json](original-classification-version/DOC-QA.json)、[original-classification-qa-aliases/ORIGINAL-CLASSIFICATION-DOC-QA.json](original-classification-qa-aliases/ORIGINAL-CLASSIFICATION-DOC-QA.json)。
- 歷史表 `SHA256SUMS.txt`，表 SHA256 `5da4589bb8d342534ae58f2d9982f2e75f39c3fc23f27b647fa4725fbeef141a`；歷史 target `FORMAT-QA.json`，SHA256 `0e33d866be0e8b2ad9be560ae40f42bf7686b7aa977da9491b3cf18548dff90b`。當前同路徑 SHA256：`本批未提供此同名路徑`。
  公開完整歷史別名：[original-classification-version/FORMAT-QA.json](original-classification-version/FORMAT-QA.json)、[original-classification-qa-aliases/ORIGINAL-CLASSIFICATION-FORMAT-QA.json](original-classification-qa-aliases/ORIGINAL-CLASSIFICATION-FORMAT-QA.json)。
- 歷史表 `SHA256SUMS.txt`，表 SHA256 `5da4589bb8d342534ae58f2d9982f2e75f39c3fc23f27b647fa4725fbeef141a`；歷史 target `FRAMING-QA.json`，SHA256 `4c9cb50e49828e3437924b91375d79dcb8129f208b5c2343c842d2b81bd5ab7a`。當前同路徑 SHA256：`1653ce8e72a93a00ef035982dd25b029748b2f74b2e147a6cd80fc5da8f71bf7`。
  公開完整歷史別名：[original-classification-version/FRAMING-QA.json](original-classification-version/FRAMING-QA.json)。
- 歷史表 `SHA256SUMS.txt`，表 SHA256 `5da4589bb8d342534ae58f2d9982f2e75f39c3fc23f27b647fa4725fbeef141a`；歷史 target `IDENTITY-QA.json`，SHA256 `bcf8339cccdce326141443e33f7fb6053fe1840ad87b47486fb5e8f8247e18e7`。當前同路徑 SHA256：`本批未提供此同名路徑`。
  公開完整歷史別名：[original-classification-version/IDENTITY-QA.json](original-classification-version/IDENTITY-QA.json)、[original-classification-qa-aliases/ORIGINAL-CLASSIFICATION-IDENTITY-QA.json](original-classification-qa-aliases/ORIGINAL-CLASSIFICATION-IDENTITY-QA.json)。
- 歷史表 `SHA256SUMS.txt`，表 SHA256 `5da4589bb8d342534ae58f2d9982f2e75f39c3fc23f27b647fa4725fbeef141a`；歷史 target `PUBLICATION-DOC-QA.json`，SHA256 `def6024f6afc833b200040157a30c26daaef56bf25f9f9f31012f4886e2d4d56`。當前同路徑 SHA256：`本批未提供此同名路徑`。
  公開完整歷史別名：[original-classification-version/PUBLICATION-DOC-QA.json](original-classification-version/PUBLICATION-DOC-QA.json)、[original-classification-qa-aliases/ORIGINAL-CLASSIFICATION-PUBLICATION-DOC-QA.json](original-classification-qa-aliases/ORIGINAL-CLASSIFICATION-PUBLICATION-DOC-QA.json)。
- 歷史表 `SHA256SUMS.txt`，表 SHA256 `5da4589bb8d342534ae58f2d9982f2e75f39c3fc23f27b647fa4725fbeef141a`；歷史 target `README.md`，SHA256 `45e9bfca91ad0a8c009e883549479fe0d648abf8db4f4eb5ffa3198ffb3ffeb9`。當前同路徑 SHA256：`261999e1823b0aaedaaa4850564059d4de6bb99b2b111b9c6c5ccec05ade6d91`。
  公開完整歷史別名：[ORIGINAL-SOURCE-GAP-README.md](ORIGINAL-SOURCE-GAP-README.md)、[original-classification-version/README.md](original-classification-version/README.md)。
- 歷史表 `SHA256SUMS.txt`，表 SHA256 `5da4589bb8d342534ae58f2d9982f2e75f39c3fc23f27b647fa4725fbeef141a`；歷史 target `REBUILD-QA.json`，SHA256 `e747bc1052a7e4e2e42fac83faed791de6c630a7420805403fa6f8df5489df3c`。當前同路徑 SHA256：`本批未提供此同名路徑`。
  公開完整歷史別名：[original-classification-version/REBUILD-QA.json](original-classification-version/REBUILD-QA.json)、[original-classification-qa-aliases/ORIGINAL-CLASSIFICATION-REBUILD-QA.json](original-classification-qa-aliases/ORIGINAL-CLASSIFICATION-REBUILD-QA.json)。
- 歷史表 `SHA256SUMS.txt`，表 SHA256 `5da4589bb8d342534ae58f2d9982f2e75f39c3fc23f27b647fa4725fbeef141a`；歷史 target `SCENE-QA.json`，SHA256 `c59bd4b36bf4155ce8c3759d9d8cdb947717693ec23fc67ea2d3d23b0e0a7bb1`。當前同路徑 SHA256：`05c0eb4cb4639d3936ace608db0c68319ee236abad396e06b485029e251fad6d`。
  公開完整歷史別名：[original-classification-version/SCENE-QA.json](original-classification-version/SCENE-QA.json)。
- 歷史表 `SHA256SUMS.txt`，表 SHA256 `5da4589bb8d342534ae58f2d9982f2e75f39c3fc23f27b647fa4725fbeef141a`；歷史 target `SOURCE-VISUAL-QA.json`，SHA256 `c4b433b2484cb247f1aadc61b9645bd70c6e6ce1c8b5287c68851e9e7561d940`。當前同路徑 SHA256：`本批未提供此同名路徑`。
  公開完整歷史別名：[original-classification-version/SOURCE-VISUAL-QA.json](original-classification-version/SOURCE-VISUAL-QA.json)、[original-classification-qa-aliases/ORIGINAL-CLASSIFICATION-SOURCE-VISUAL-QA.json](original-classification-qa-aliases/ORIGINAL-CLASSIFICATION-SOURCE-VISUAL-QA.json)。
- 歷史表 `SHA256SUMS.txt`，表 SHA256 `5da4589bb8d342534ae58f2d9982f2e75f39c3fc23f27b647fa4725fbeef141a`；歷史 target `back.png`，SHA256 `dd32740433f55ae6188129413c27bea7493c6a5518ecc093f80813d348a49863`。當前同路徑 SHA256：`11fbc7817367cb9d748f0ad7833c0e315d64be8c2b6535343997679cb78d9fa4`。
  公開完整歷史別名：[original-classification-version/back.png](original-classification-version/back.png)。
- 歷史表 `SHA256SUMS.txt`，表 SHA256 `5da4589bb8d342534ae58f2d9982f2e75f39c3fc23f27b647fa4725fbeef141a`；歷史 target `east.png`，SHA256 `1f0a1b509e4623900adb89222ea8946d9a913c0b2a4e3a24cd41ce2de01e0246`。當前同路徑 SHA256：`da8c5dde3de161786a322cfeef82781b77c86e86d65693b1c4a935c9fa8c920c`。
  公開完整歷史別名：[original-classification-version/east.png](original-classification-version/east.png)。
- 歷史表 `SHA256SUMS.txt`，表 SHA256 `5da4589bb8d342534ae58f2d9982f2e75f39c3fc23f27b647fa4725fbeef141a`；歷史 target `front.png`，SHA256 `5ca4583607fa454ec8c260744c54a6cd836cfbc915189538090912dc619505d3`。當前同路徑 SHA256：`8af6e2e3522a627f6f18a700ebd71189224ba1331db9d69531961b6395520606`。
  公開完整歷史別名：[original-classification-version/front.png](original-classification-version/front.png)。
- 歷史表 `SHA256SUMS.txt`，表 SHA256 `5da4589bb8d342534ae58f2d9982f2e75f39c3fc23f27b647fa4725fbeef141a`；歷史 target `palette.json`，SHA256 `abe8e1cb4e68212f5f60722d104fe0de517f89840b89387512c0abbcd1074454`。當前同路徑 SHA256：`88507d5f95eeb22198dc5ab1b1b69aa47391b53b4cb1cfac5f7361d6091f8a2c`。
  公開完整歷史別名：[original-classification-version/palette.json](original-classification-version/palette.json)。
- 歷史表 `SHA256SUMS.txt`，表 SHA256 `5da4589bb8d342534ae58f2d9982f2e75f39c3fc23f27b647fa4725fbeef141a`；歷史 target `preview.png`，SHA256 `784dba534c22923fec2ca0610a0374dff7d28c873b8d40e3e279da9005fc5064`。當前同路徑 SHA256：`0c63c928831a4aaf95ca263eee05227dc02ecaab28df7c36d040fdfd37bbfafc`。
  公開完整歷史別名：[original-classification-version/preview.png](original-classification-version/preview.png)。
- 歷史表 `SHA256SUMS.txt`，表 SHA256 `5da4589bb8d342534ae58f2d9982f2e75f39c3fc23f27b647fa4725fbeef141a`；歷史 target `rear.png`，SHA256 `4decd2a4275ee4676efe915bbc41f380a12cc6ca10c9e886b1fd09a9c4d8846c`。當前同路徑 SHA256：`406c82c2947998385b659670d7270522268aa38e6eeeaa4d50974685e5e34579`。
  公開完整歷史別名：[original-classification-version/rear.png](original-classification-version/rear.png)。
- 歷史表 `SHA256SUMS.txt`，表 SHA256 `5da4589bb8d342534ae58f2d9982f2e75f39c3fc23f27b647fa4725fbeef141a`；歷史 target `scene.blend`，SHA256 `bd32a6a214ee93039ddf345d28784f518807af49d3a36e4ebea4788be634b9ba`。當前同路徑 SHA256：`5c975c58368e029eee13200a5a10c153abfbeb7e2917f19108961ee7c1c6e5c8`。
  公開完整歷史別名：[ORIGINAL-SOURCE-GAP-scene.blend](ORIGINAL-SOURCE-GAP-scene.blend)、[original-classification-version/scene.blend](original-classification-version/scene.blend)。
- 歷史表 `SHA256SUMS.txt`，表 SHA256 `5da4589bb8d342534ae58f2d9982f2e75f39c3fc23f27b647fa4725fbeef141a`；歷史 target `top.png`，SHA256 `12788ae04bf5794007e5aba80ca2d5f5e3c5e27d4c7cc2fe0a95808c4018f9d7`。當前同路徑 SHA256：`e567de961b5116797c49e19a680542ca74f15c6a028d730feda57c164c54b1e7`。
  公開完整歷史別名：[original-classification-version/top.png](original-classification-version/top.png)。
- 歷史表 `SHA256SUMS.txt`，表 SHA256 `5da4589bb8d342534ae58f2d9982f2e75f39c3fc23f27b647fa4725fbeef141a`；歷史 target `west.png`，SHA256 `8cd32604d856d8073500f470a27af5ed3732fb33380b8adaef7401bf075cd1d6`。當前同路徑 SHA256：`e0544d6337a4d50ea1eb105682897844ec56445bf1ac86021db78cd32467ce8e`。
  公開完整歷史別名：[original-classification-version/west.png](original-classification-version/west.png)。

