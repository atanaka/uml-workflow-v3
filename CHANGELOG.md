# Changelog / 変更履歴

All notable changes to this project will be documented in this file.  
このプロジェクトへの注目すべき変更はすべてここに記録されます。

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).  
フォーマットは [Keep a Changelog](https://keepachangelog.com/ja/1.1.0/) に準拠しています。

---

## [3.0.0] - 2026-02-26

### Added / 追加

- **Step 10: Traceability Matrix / トレーサビリティマトリクス**  
  Requirements → Model → Code → Test の完全な双方向追跡マトリクスを自動生成します。  
  Auto-generates a full bidirectional traceability matrix: Requirements → Model → Code → Tests.

- **Claude.ai Skills 正式対応 / Official Claude.ai Skills Support**  
  Settings > Capabilities の「Upload skill」から ZIP をアップロードするだけでインストールできます。  
  Install by uploading a ZIP via Settings > Capabilities > "Upload skill" — no manual file operations needed.

- **INSTALLATION_GUIDE.md（日本語）/ Japanese Installation Guide**  
  一般ユーザー向けのステップバイステップのインストール手順書を追加しました。  
  Added a step-by-step installation guide for end users.

- **INSTALLATION_GUIDE_EN.md（English）/ English Installation Guide**  
  英語版インストールガイドを追加しました。  
  Added the English-language installation guide.

- **docs/USER_GUIDE.md — バイリンガル詳細ユーザーガイド / Bilingual Comprehensive User Guide**  
  実際の開発フローに沿った詳細な使い方ガイドを追加しました。  
  Added a detailed usage guide aligned with real-world development workflows.

- **docs/ARCHITECTURE.md — アーキテクチャドキュメント / Architecture Document**  
  スキル構成・データフロー・設計判断をまとめたアーキテクチャドキュメントを追加しました。  
  Added an architecture document covering skill composition, data flows, and design decisions.

- **examples/expense-report.md — サンプルシナリオ / Sample Scenario**  
  経費申請システムのデモ用シナリオ（日英バイリンガル）を追加しました。  
  Added a bilingual demo scenario for an expense report management system.

### Changed / 変更

- **references 化 / References-Based Architecture**  
  10個のパイプラインスキルをメインスキルの `references/` に統合しました。  
  `available_skills` カタログへの露出を 16 → 5 スキルに削減（69%削減）。  
  Integrated all 10 pipeline skills into the `references/` directory of the main skill.  
  Reduced `available_skills` catalog exposure from 16 → 5 skills (69% reduction).

- **description フィールド 200文字対応 / 200-character description limit**  
  Claude.ai の制約に合わせて全スキルの description を 200文字以内に短縮しました。  
  Shortened all skill descriptions to ≤ 200 characters to comply with the Claude.ai constraint.

- **タイトル統一 / Title Unification**  
  "v2 Enhanced" → "v3" に全ドキュメントで統一しました。  
  Updated all documents from "v2 Enhanced" to "v3" consistently.

- **バイリンガル化 / Full Bilingualization**  
  README・CHANGELOG・CONTRIBUTING・インストールガイドをすべて日英バイリンガルに改訂しました。  
  Revised README, CHANGELOG, CONTRIBUTING, and all guides to be fully bilingual (Japanese + English).

### Optimized / 最適化

- **トークンコスト / Token Cost**  
  `available_skills` のトークン消費を約 1,700 → 600 に削減（約65%削減）。  
  Reduced `available_skills` token consumption from ~1,700 → ~600 (~65% reduction).

- **インストール工数 / Install Effort**  
  アップロードが必要な ZIP の数を 15 → 5 に削減。  
  Reduced the number of ZIPs to upload from 15 to 5.

---

## [2.0.0] - 2026-02

### Added / 追加

- **Step 7: セキュリティ設計 / Security Design**  
  OWASP Top 10 準拠のセキュリティ設計を自動生成します。  
  Automatically generates OWASP Top 10–compliant security design.

- **Step 9: テスト生成 / Test Generation**  
  ユースケースベースのテストコード（ユニット + E2E）を生成します。  
  Generates use case–based test code (unit tests + E2E tests).

- **キャッシュシステム / Caching System**  
  中間成果物の自動キャッシュと再利用機能を追加しました。  
  Added automatic caching and reuse of intermediate artifacts.

- **XMI最適化 / XMI Optimization**  
  XMI 生成をデフォルト OFF に変更し、最大40%の高速化を実現しました。  
  Changed XMI generation to OFF by default, achieving up to 40% speed improvement.

- **段階的実行 / Staged Execution**  
  任意のステップからの再開・単一ステップ実行・モデルのみモードを追加しました。  
  Added resume from any step, single-step execution, and model-only mode.

- **バイリンガルサポート / Bilingual Support**  
  日本語・英語の出力を選択できるバイリンガルサポートを追加しました。  
  Added bilingual support with Japanese and English output selection.

- **対話的ワークフロー / Interactive Workflow**  
  `ask_user_input_v0` を使った対話的なパラメータ収集を実装しました。  
  Implemented interactive parameter collection using `ask_user_input_v0`.

### Changed / 変更

- パイプラインを 4 ステップ → 9 ステップに拡張しました。  
  Expanded the pipeline from 4 steps to 9 steps.

- `domain-model.json` を Single Source of Truth として全ステップで共有するように変更しました。  
  Changed `domain-model.json` to be shared as the Single Source of Truth across all steps.

---

## [1.0.0] - 2026-01

### Added / 追加

- **Step 1: シナリオ → アクティビティ図 / Scenario → Activity Diagram**  
  ビジネスシナリオからアクティビティ図を生成します。  
  Generates an activity diagram from a business scenario.

- **Step 2: アクティビティ図 → ユースケース / Activity → Use Cases**  
  アクティビティ図からユースケースを抽出します。  
  Extracts use cases from an activity diagram.

- **Step 3: ユースケース → クラス図 / Use Cases → Class Diagram**  
  ユースケースからドメインモデル（クラス図）を生成します。  
  Generates a domain model (class diagram) from use cases.

- **Step 4: ユースケース → コード / Use Cases → Code**  
  ユースケースとクラス図からフルスタックコードを生成します。  
  Generates full-stack code from use cases and the class diagram.

- **ヘルパースキル / Helper Skills**  
  `usecase-md-to-json`, `classdiagram-image-to-json`, `json-to-models`, `classdiagram-to-crud` を追加しました。  
  Added helper skills: `usecase-md-to-json`, `classdiagram-image-to-json`, `json-to-models`, `classdiagram-to-crud`.

- **PlantUML出力 / PlantUML Output**  
  すべての UML 図を PlantUML 形式で出力します。  
  All UML diagrams are output in PlantUML format.

- **JSON中間フォーマット / JSON Intermediate Format**  
  機械可読な中間データフォーマット（JSON）を採用しました。  
  Adopted a machine-readable intermediate data format (JSON).
