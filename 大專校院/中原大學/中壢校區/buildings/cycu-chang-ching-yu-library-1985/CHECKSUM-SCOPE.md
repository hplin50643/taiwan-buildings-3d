# Checksum scope for the reconciliation version

This documentation-only version supersedes the prior candidate manifest; it does not alter model, material, image, source-review, independent-review or engineering bytes.

## Exact pre-existing historical exception

`qa/north-soffit-previous/SHA256SUMS` records `README.md` as `abe1b1ceff20faca23a2aacd0996343d6ec5899428098e6e38cc172bb04ca99c`. The corresponding archived file is exactly `qa/north-soffit-previous/README.md`, whose actual SHA256 is `7696228536fca2e7664c11706a99f7dee22affa1d2cfdf1aa91d723a068ef3c7`. These do **not** match. This is the one pre-existing exception among the 109 baseline checksum entries; the other 108 match the baseline files. Paths absent from the partial previous-record archive were checked against the exact baseline originals, not unrelated current same-name files.

Both archived files are byte-identical to their baseline counterparts at commit `38caa43aef914829c7c7b59716926ab94d4c3f17`. The baseline README Git blob is `41066c57e449b3a4ba42cd988cd04b36f03a0e37`. The original bytes intended by the recorded `abe1...` checksum and the reason it became stale are not established. The old checksum is preserved, not repaired, waived as a match, or replaced by a current hash.

The distinct current root `README.md` has SHA256 `c26d9acb14e2ededaa84702b7ac8f587b449dd0b635ad9778dd78c4567cbef18`. That verifies this current document only, not the historical record.

## Current and historical manifests

The new root `SHA256SUMS` and `CHECKSUM-RECONCILIATION-FREEZE-MANIFEST.json` govern this reconciliation version. The unchanged `NORTH-SOFFIT-FREEZE-MANIFEST.json` governs the superseded pre-reconciliation candidate; its references to the old checksum scope and root checksum file are historical and must not be tested against their replacements. Exact original copies of those two files are preserved under `qa/checksum-reconciliation-original/`. The original `appearance-freeze.json` and previous QA/checksum files remain historical evidence, not current-model validation.

The preserved original independent review is a review of the superseded candidate. Its `file_sha256["CHECKSUM-SCOPE.md"]` is `4711de82c368e83fd7dfa66efef845a5677cd10dd5e2f0160481cd698258dce3`, which resolves exactly to the retained snapshot `qa/checksum-reconciliation-original/CHECKSUM-SCOPE.md`, not the replacement root scope document. This single explicit historical path mapping does not rewrite or repair the original review. All other original independent work-input and image hashes still match their exact current work-relative paths. The separate reconciliation review must bind the new scope bytes. Do not resolve hashes by basename. See `CHECKSUM-RECONCILIATION.json` for baseline evidence and `CHECKSUM-RECONCILIATION-INDEPENDENT-QA.json` for the separate supplement review. No original QA hash or source snapshot is changed. Original engineering limitations, including the recorded cross-layer cases, are unchanged.
