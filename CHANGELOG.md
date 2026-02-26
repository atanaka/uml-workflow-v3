# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [3.0.0] - 2026-02-26

### Added
- **Step 10: Traceability Matrix** — 要件→モデル→コード→テストの完全な追跡マトリクスを自動生成
- **Claude.ai Skills 対応** — Settings > Capabilities から ZIP アップロードでインストール可能
- **INSTALLATION_GUIDE.md** — 一般ユーザー向けのインストール手順書
- **English installation guide** — 英語版インストールガイド
- **サンプルシナリオ** — 経費申請システムのデモ用シナリオ

### Changed
- **references 化** — 10個のパイプラインスキルをメインスキル内の `references/` に統合。available_skills カタログ露出を16→5に削減（69%削減）
- **description 200文字対応** — Claude.ai の制約に合わせて全スキルの description を200文字以内に短縮
- **タイトル更新** — "v2 Enhanced" → "v3" に統一

### Optimized
- **トークンコスト** — available_skills のトークン消費を 1,700→600 に削減（65%削減）
- **インストール工数** — アップロード対象を15 ZIP→5 ZIP に削減

## [2.0.0] - 2026-02

### Added
- **Step 7: Security Design** — OWASP Top 10 準拠のセキュリティ設計自動生成
- **Step 9: Test Generation** — ユースケースベースのテストコード生成
- **Caching System** — 中間成果物の自動キャッシュ・再利用機能
- **XMI Optimization** — XMI 生成のデフォルト OFF 化（40%高速化）
- **Staged Execution** — 任意のステップからの再開・単一ステップ実行
- **Bilingual Support** — 日本語・英語の両言語対応
- **Interactive Workflow** — ask_user_input_v0 による対話的パラメータ収集

### Changed
- パイプラインを4ステップ→9ステップに拡張
- domain-model.json を Single Source of Truth として全ステップで共有

## [1.0.0] - 2026-01

### Added
- **Step 1: Scenario → Activity Diagram** — ビジネスシナリオからアクティビティ図を生成
- **Step 2: Activity → Use Cases** — アクティビティ図からユースケースを抽出
- **Step 3: Use Cases → Class Diagram** — ユースケースからドメインモデル（クラス図）を生成
- **Step 4: Use Cases → Code** — ユースケースとクラス図からフルスタックコードを生成
- **Helper Skills** — usecase-md-to-json, classdiagram-image-to-json, json-to-models, classdiagram-to-crud
- **PlantUML Output** — 全 UML 図を PlantUML 形式で出力
- **JSON Intermediate Format** — 機械可読な中間データ形式
