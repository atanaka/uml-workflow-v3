# Changelog

All notable changes to this project will be documented in this file.

## [3.3.0] - 2026-05-13

### Added — Papyrus 7.1.0 公式サポート
- **json-to-models v1.3.1**: EMF 形式 XMI (`*_class-model-emf.uml`) を生成し、Papyrus 7.1.0 で直接編集可能に
- **abstract クラス対応**: `domain-model.json` の `entities[]` に `is_abstract: boolean` フィールド追加（OMG/EMF 両形式で `isAbstract="true"` 属性出力）
- **XMI 二形式同時出力**: `--xmi-format={both|omg|emf|none}` を新設、`--no-xmi` は `none` のエイリアスとして互換維持
- **PNG ベストエフォート生成**: 3 段階フォールバック (PlantUML CLI → `java -jar plantuml.jar` → Docker サーバー HTTP)
- **DEMO-GUIDE.md**: 「Papyrus 7.1.0 でクラス図を編集する」章を新規追加（Step 1〜6 + トラブルシューティング）

### Changed
- **SKILL.md**: XMI 質問を 4 択化 (両形式 / EMF / OMG / 生成しない)
- **SKILL.md**: ファイル命名規則を `*_class-model.xmi` → `*_class-model-omg.uml` および `*_class-model-emf.uml` に更新

### Fixed
- 旧版 `generate_xmi_from_json` の lxml 関連実行時エラー 2 件を修正
  - `Element("xmi:XMI", ...)` → Clark notation (`Element(f"{{{XMI_NS}}}XMI", ...)`)
  - `tostring(..., encoding='unicode', xml_declaration=True)` → `tostring(..., encoding='UTF-8', xml_declaration=True).decode('utf-8')`

### Verified
- **Papyrus 7.1.0 実機検証**: Mini (3 クラス, 1 Association) + Comprehensive (8 クラス + 2 Enumeration + 7 Association) で 26 機能 100% PASS
- **重要発見**: Papyrus 7.1+ は `.uml` 単体取り込みで `.aird` / `.di` / `.notation` を自動補完するため、json-to-models 側での `.aird` 生成は不要

## [3.2.0] - 2026-03

### Added
- **キャッシュパスのローカル化**: `~/.uml-workflow-cache` 配下に変更、`/mnt/user-data/outputs/` 非存在環境でも動作
- **Phase A→B ハンドオフ自動化**: `save_phase_a_state()` / `load_phase_a_state()` 実装、テックスタック選択のコピペ不要
- **DEMO-GUIDE.md** 同梱: 初回セットアップ〜Phase A/B 実行の手順書
- **Makefile**: PIPELINE.md ↔ SKILL.md 同期と `make sync` / `make check` / `make zip` ターゲット

### Fixed
- `restore_all_cached_files()` 関数を実装（SKILL.md から参照されていたが未実装だった）

## [3.1.0] - 2026-02-27

### Added
- **2-Phase Auto-Split Architecture**: Full workflow automatically splits into Phase A (Steps 1-7) and Phase B (Steps 8-10) across separate conversations to prevent context window exhaustion
- **Template Lazy Loading**: `usecase-to-code-v1` templates (language examples, documentation templates) extracted to separate files and loaded on demand
- **AUTO-SPLIT CHECKPOINT**: Explicit checkpoint after Step 7 with Phase B instructions for user

### Changed
- **SKILL.md**: Reduced from 1,552 to 911 lines (38% reduction, ~4K tokens saved)
- **usecase-to-code-v1 PIPELINE.md**: Reduced from 2,826 to 1,678 lines (30% reduction, ~6K tokens saved)
- **Standalone usecase-to-code-v1**: Same template split applied for consistency
- Execution plan display now shows Phase A/B split

### Removed
- Duplicate Python pseudocode section in SKILL.md (was redundant with PHASE 4)
- Verbose Usage Examples, Best Practices, Cache Management sections (compressed to tables)
- `uml-workflow-v2-enhanced` — consolidated into v3

### Fixed
- **Context window exhaustion at Step 8**: Root cause was ~120K tokens consumed before Step 8 PIPELINE load. Now Phase A uses ~91K and Phase B uses ~60K, both safely within 200K limit

## [3.0.0] - 2026-02-19

### Added
- Renamed from `uml-workflow-v2-enhanced` to `uml-workflow-v3`
- Security-first 10-step pipeline (was 9 steps in v2)
- `security-design-v1` integrated as Step 7
- `traceability-matrix-v1` added as Step 10
- Bilingual support (Japanese/English) across all skills
- Cache system for intermediate artifacts
- XMI generation toggle (OFF by default for 40% speedup)

### Skills Included
1. scenario-to-activity-v1
2. activity-to-usecase-v1
3. usecase-to-class-v1
4. class-to-statemachine-v1
5. usecase-to-sequence-v1
6. model-validator-v1
7. security-design-v1
8. usecase-to-code-v1
9. usecase-to-test-v1
10. json-to-models (optional)
11. usecase-md-to-json (optional)
12. classdiagram-image-to-json (optional)
