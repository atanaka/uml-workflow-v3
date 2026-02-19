# CHANGELOG

## v3.0.0 (2026-02-19)

### 🎉 v2-enhanced から v3 へのリネーム

uml-workflow-v2-enhanced を正式に **uml-workflow-v3** に改称しました。
v2（8ステップ版）と明確に区別し、バージョン体系を整理しています。

### ✨ v3 の主な特徴（v1 比較）

- **9ステップワークフロー**: セキュリティ設計（Step 7）・テスト生成（Step 9）を追加
- **キャッシュシステム**: 中間成果物の自動保存・再利用（最大75% token削減）
- **段階的実行**: 任意のステップから再開可能
- **XMI最適化**: デフォルトOFF（40%高速化）
- **オプションスキル統合**: json-to-models・usecase-md-to-json・classdiagram-image-to-json を正式サポート
- **多言語対応**: 日本語・英語・バイリンガル

### 📦 利用スキル

**メインスキル（9ステップ）**
- scenario-to-activity-v1
- activity-to-usecase-v1
- usecase-to-class-v1
- class-to-statemachine-v1
- usecase-to-sequence-v1
- model-validator-v1
- security-design-v1
- usecase-to-code-v1
- usecase-to-test-v1

**オプションスキル**
- json-to-models
- usecase-md-to-json
- classdiagram-image-to-json

---

## v2.0.0（旧: uml-workflow-v2-enhanced）

- キャッシュ・段階的実行・XMI最適化を統合
- セキュリティ設計スキル（security-design-v1）追加
- テスト生成スキル（usecase-to-test-v1）追加

## v1.0.0（uml-workflow-v1）

- 基本的な8ステップワークフロー
- scenario → activity → usecase → class → statemachine → sequence → validate → code
