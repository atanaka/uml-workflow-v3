# UML Workflow v3

**ビジネスシナリオから本番品質のアプリケーションを自動生成する Claude AI スキル**

*An AI-powered Claude Skill that transforms business scenarios into production-ready applications through a 10-step UML pipeline.*

---

## Overview / 概要

UML Workflow v3 は、Claude AI の [Skills](https://docs.claude.com/en/docs/claude-ai/skills) 機能を活用した、モデルベースシステムエンジニアリング（MBSE）ワークフローです。自然言語で記述されたビジネスシナリオを入力として、UML図の生成からコード・テストの自動生成まで、10ステップのパイプラインを一貫して実行します。

### What it does / できること

```
Business Scenario (text) / ビジネスシナリオ（自然言語）
    ↓
┌─────────────────────────────────────────────────┐
│  Step  1: シナリオ → アクティビティ図             │ scenario to activity diagram
│  Step  2: アクティビティ図 → ユースケース抽出     │ activity diagram to usecases
│  Step  3: ユースケース → クラス図（ドメインモデル）│ usecases to class diagram (domain model)
│  Step  4: クラス図 → ステートマシン図             │ class diagram to statemachine diagrams
│  Step  5: ユースケース → シーケンス図             │ usecases to sequence diagrams
│  Step  6: モデル横断バリデーション                 │ model-validation
│  Step  7: OWASP準拠セキュリティ設計               │ security-design
│  Step  8: フルスタックコード生成                   │ full-stack code generation
│  Step  9: テストコード生成                         │ test code generation
│  Step 10: トレーサビリティマトリクス               │ traceability matrix generation
└─────────────────────────────────────────────────┘
    ↓
Quality Code with UML documentation / 本番品質のアプリケーション + 完全なUMLドキュメント
```

### Key Features / 主な特長

- **10-Step Pipeline** — シナリオからコード・テストまで一気通貫
- **Bilingual Output** — 日本語・英語の両方に対応（コメント・ドキュメント）
- **Caching System** — 中間成果物を自動キャッシュ、再実行時のトークン消費を最大75%削減
- **Flexible Execution** — フル実行、途中再開、単一ステップ実行など複数モード
- **Security-First** — OWASP Top 10準拠のセキュリティ設計を自動生成
- **Full Traceability** — 要件→モデル→コード→テストの追跡マトリクス

### Coming Soon: Commercial support and extensions by a new company/新会社による商用サポート・拡張版

---

## Quick Start / クイックスタート

### Prerequisites / 前提条件

- Claude.ai の **Pro** / **Max** / **Team** / **Enterprise** プラン
- 「Code execution and file creation」が **有効**

### Installation / インストール

1. [Releases](../../releases) から `uml-workflow-v3-github-repo.zip` をダウンロード
2. ZIP を解凍すると **5つの ZIP ファイル** が出現
3. Claude.ai → **Settings** → **Capabilities** → **Skills** セクション
4. 「**Upload skill**」で各 ZIP を1つずつアップロード（5回）
5. 各スキルの**トグルを ON** にする

> 詳細は [docs/INSTALLATION_GUIDE.md](docs/INSTALLATION_GUIDE.md) を参照

### First Run / 最初の実行

新しい会話を開き、以下のように入力してください：

```
uml-workflow-v3を使って、以下のビジネスシナリオからアプリケーションを生成してください。

シナリオ：
従業員が経費申請を提出し、上長が承認・却下する。
経理部門が承認済み申請を精算処理する。
```

Claude が自動的にスキルを認識し、対話的に質問しながら10ステップを実行します。

---

## Architecture / アーキテクチャ

### Skill Composition / スキル構成

```
uml-workflow-v3 (メインオーケストレーター)
├── references/ (内蔵パイプラインスキル ×10)
│   ├── scenario-to-activity-v1      Step 1
│   ├── activity-to-usecase-v1       Step 2
│   ├── usecase-to-class-v1          Step 3
│   ├── class-to-statemachine-v1     Step 4
│   ├── usecase-to-sequence-v1       Step 5
│   ├── model-validator-v1           Step 6
│   ├── security-design-v1           Step 7
│   ├── usecase-to-code-v1           Step 8
│   ├── usecase-to-test-v1           Step 9
│   └── traceability-matrix-v1       Step 10
└── scripts/ (実行エンジン)

usecase-md-to-json       ← UC仕様 Markdown→JSON変換
classdiagram-image-to-json ← 手描きクラス図取込
json-to-models           ← JSON→PlantUML/XMI再生成
classdiagram-to-crud     ← クラス図→CRUD HTML生成
```

メインスキルが10個のパイプラインスキルを `references/` に内蔵し、残り4つは独立したヘルパースキルとして動作します。

### Token Efficiency / トークン効率

references 方式により、Claude の `available_skills` カタログに露出するスキルを16→5に削減（69%減）。必要なスキルだけが実行時に動的にロードされます。

| 実行シナリオ | Token削減率 |
|-------------|-----------|
| 初回フル実行 | 0%（基準） |
| 機能追加（Step 2から再開） | 20-30% |
| モデル調整（Step 3から） | 30-40% |
| モデルのみ（Step 1-7） | 30-35% |
| バリデーションのみ | ~95% |
| 最適組合せ（Step 3＋モデルのみ） | ~75% |

---

## Execution Modes / 実行モード

### 1. Full Workflow / フルワークフロー

```
「uml-workflow-v3で{プロジェクト名}を生成して」
```

全10ステップを実行。初回のプロジェクト生成に使用。

### 2. Resume from Step / 途中から再開

```
「uml-workflowをStep 5から再開してください」
```

指定ステップ以前はキャッシュから復元し、指定ステップ以降を再実行。

### 3. Model Only / モデルのみ

```
「{プロジェクト名}のモデルのみ生成して」
```

Step 1-7 を実行し、コード生成（Step 8-9）をスキップ。設計フェーズに最適。

### 4. Single Step / 単一ステップ

```
「uml-workflowのStep 6（モデル検証）を実行してください」
```

特定のステップのみを実行。バリデーションや特定図の再生成に使用。

### 5. Edit Helpers / モデル修正ツール

```
「この手描きのクラス図を取り込んでください」（画像添付）
「ユースケース仕様のMarkdownを修正したので、JSONに反映して」
```

ヘルパースキルを使った中間成果物の手動修正。

---

## Output Files / 出力ファイル

ワークフロー実行後、以下のファイルが生成されます：

```
{project-name}_activity-data.json       ← アクティビティ図データ
{project-name}_activity.puml            ← PlantUML アクティビティ図
{project-name}_usecase-output.json      ← ユースケース定義
{project-name}_usecase-diagram.puml     ← PlantUML ユースケース図
usecase-specifications/                 ← 個別UC仕様（Cockburn形式）
  ├── UC-001_*.md
  └── UC-002_*.md
{project-name}_domain-model.json        ← ドメインモデル（Single Source of Truth）
{project-name}_class.puml               ← PlantUML クラス図
{project-name}_statemachine.puml        ← PlantUML ステートマシン図
{project-name}_sequence.puml            ← PlantUML シーケンス図
{project-name}_validation-report.md     ← バリデーションレポート
{project-name}_security-config.json     ← セキュリティ設計
{project-name}_traceability-matrix.json ← トレーサビリティマトリクス
{project-name}/                         ← 生成アプリケーション
  ├── backend/
  ├── frontend/
  ├── tests/
  ├── docker-compose.yml
  └── README.md
```

---

## Skill Files / スキルファイル一覧

| # | Skill ZIP | Size | Role |
|---|-----------|------|------|
| 1 | `uml-workflow-v3.zip` | 154KB | Main orchestrator + 10 pipeline skills |
| 2 | `usecase-md-to-json.zip` | 11KB | UC spec Markdown → JSON converter |
| 3 | `classdiagram-image-to-json.zip` | 15KB | Hand-drawn class diagram → JSON |
| 4 | `json-to-models.zip` | 12KB | JSON → PlantUML/XMI regeneration |
| 5 | `classdiagram-to-crud.zip` | 6KB | Class diagram → CRUD HTML fragments |

> `uml-workflow-v3.zip` のみで10ステップパイプラインは動作します。残り4つはモデル手動修正時の補助ツールです。

---

## Version History / バージョン履歴

| Version | Changes |
|---------|---------|
| **v3.0.0** | 10-step pipeline (traceability追加), references化, description 200文字対応, Claude.ai Skills対応 |
| v2.0.0 | 9-step pipeline, キャッシュシステム, XMI最適化, セキュリティ設計 |
| v1.0.0 | 4-step basic pipeline (scenario→usecase→class→code) |

詳細は [CHANGELOG.md](CHANGELOG.md) を参照。

---

## Documentation / ドキュメント

| Document | Description |
|----------|-------------|
| [docs/USER_GUIDE.md](docs/USER_GUIDE.md) | 詳細ユーザーガイド（日英）/ Comprehensive user guide (bilingual) |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | アーキテクチャ解説（日英）/ Architecture overview (bilingual) |
| [docs/INSTALLATION_GUIDE.md](docs/INSTALLATION_GUIDE.md) | インストール手順（日本語）/ Installation guide (Japanese) |
| [docs/INSTALLATION_GUIDE_EN.md](docs/INSTALLATION_GUIDE_EN.md) | Installation guide (English) |
| [skills/uml-workflow-v3/README.md](skills/uml-workflow-v3/README.md) | スキル詳細説明（日英）/ Skill detail guide (bilingual) |
| [CHANGELOG.md](CHANGELOG.md) | 変更履歴（日英）/ Change log (bilingual) |
| [CONTRIBUTING.md](CONTRIBUTING.md) | コントリビューションガイド（日英）/ Contributing guide (bilingual) |
| [examples/expense-report.md](examples/expense-report.md) | サンプルシナリオ（日英）/ Sample scenario (bilingual) |

---

## Requirements / 動作環境

| Item | Requirement |
|------|-------------|
| Platform | Claude.ai (Web / Desktop / Mobile) |
| Plan | Pro / Max / Team / Enterprise |
| Feature | Code execution and file creation: **ON** |
| Skills | 5 ZIPs uploaded via Settings > Capabilities |

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Contributing / コントリビューション

Issues and Pull Requests are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## Acknowledgments

Built with [Claude AI Skills](https://docs.claude.com/en/docs/claude-ai/skills) by [Anthropic](https://www.anthropic.com/).
