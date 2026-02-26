# UML Workflow v3 / UMLワークフロー v3

**ビジネスシナリオから本番品質のアプリケーションを自動生成する Claude AI スキル**  
**A Claude AI Skill that transforms business scenarios into production-ready applications via a 10-step UML pipeline. / ビジネスシナリオから本番品質のアプリケーションを自動生成する Claude AI スキル**

## Coming Soon: Commercial support and extensions / 新会社による商用サポート・拡張版

---

## Overview / 概要

UML Workflow v3 は、Claude AI の [Skills](https://docs.claude.com/en/docs/claude-ai/skills) 機能を活用した、モデルベースシステムエンジニアリング（MBSE）ワークフローです。自然言語で記述されたビジネスシナリオを入力として、UML図の生成からコード・テストの自動生成まで、10ステップのパイプラインを一貫して実行します。

UML Workflow v3 は、Claude AI の Skills 機能を活用した MBSE ワークフローです。自然言語のビジネスシナリオを入力として、UML図の生成からコード・テスト自動生成まで、10ステップのパイプラインを一貫して実行します。 / UML Workflow v3 is a Model-Based Systems Engineering (MBSE) workflow powered by Claude AI Skills. It takes a natural-language business scenario as input and runs a complete 10-step pipeline — from UML diagram generation through full-stack code and test automation.

### What it does / できること

```
ビジネスシナリオ（自然言語） / Business Scenario (Natural Language)
    ↓
┌──────────────────────────────────────────────────────────────────┐
│  Step  1: シナリオ → アクティビティ図 / Scenario → Activity Diagram      │
│  Step  2: アクティビティ図 → ユースケース / Activity → Use Cases          │
│  Step  3: ユースケース → クラス図 / Use Cases → Class Diagram             │
│  Step  4: クラス図 → ステートマシン図 / Class → State Machine             │
│  Step  5: ユースケース → シーケンス図 / Use Cases → Sequence Diagrams     │
│  Step  6: モデル横断バリデーション / Cross-Model Validation               │
│  Step  7: OWASP準拠セキュリティ設計 / OWASP-Compliant Security Design     │
│  Step  8: フルスタックコード生成 / Full-Stack Code Generation             │
│  Step  9: テストコード生成 / Test Code Generation                         │
│  Step 10: トレーサビリティマトリクス / Traceability Matrix                │
└──────────────────────────────────────────────────────────────────┘
    ↓
本番品質のアプリケーション + 完全なUMLドキュメント + 追跡可能なエビデンス
Production-Ready Application + Full UML Documentation + Traceable Evidence
```

### Key Features / 主な特長

- **10-Step Pipeline** — シナリオからコード・テストまで一気通貫 / End-to-end automation from scenario to code and tests
- **Bilingual Output** — 日本語・英語の両方に対応（コメント・ドキュメント）/ Japanese and English output supported (comments & docs)
- **Caching System** — 中間成果物を自動キャッシュ、再実行時のトークン消費を最大75%削減 / Auto-caches intermediate artifacts; up to 75% token reduction on reruns
- **Flexible Execution** — フル実行、途中再開、単一ステップ実行など複数モード / Full run, resume from step, single-step, and more
- **Security-First** — OWASP Top 10準拠のセキュリティ設計を自動生成 / OWASP Top 10–compliant security design auto-generated at Step 7
- **Full Traceability** — 要件→モデル→コード→テストの双方向追跡マトリクス / Bidirectional traceability matrix: requirements ↔ model ↔ code ↔ tests

---

## Quick Start / クイックスタート

### Prerequisites / 前提条件

- Claude.ai の **Pro** / **Max** / **Team** / **Enterprise** プラン / Claude.ai **Pro**, **Max**, **Team**, or **Enterprise** plan
- 「Code execution and file creation」が **有効** / "Code execution and file creation" feature **enabled**

### Installation / インストール

1. [Releases](../../releases) から `uml-workflow-v3-all-skills.zip` をダウンロード / Download `uml-workflow-v3-all-skills.zip` from [Releases](../../releases)
2. ZIP を解凍すると **5つの ZIP ファイル** が出現 / Extract — you will find **5 ZIP files** inside
3. Claude.ai → **Settings** → **Capabilities** → **Skills** セクションを開く / Open Claude.ai → **Settings** → **Capabilities** → **Skills**
4. 「**Upload skill**」で各 ZIP を1つずつアップロード（5回）/ Click "**Upload skill**" and upload each ZIP one by one (5 times total)
5. 各スキルの**トグルを ON** にする / Toggle each skill **ON**

> 詳細は [docs/INSTALLATION_GUIDE.md](docs/INSTALLATION_GUIDE.md) | [English guide](docs/INSTALLATION_GUIDE_EN.md)

### First Run / 最初の実行

新しい会話を開き、以下のように入力してください：/ Open a new Claude conversation and type:

```
uml-workflow-v3を使って、以下のビジネスシナリオからアプリケーションを生成してください。

シナリオ：
従業員が経費申請を提出し、上長が承認・却下する。
経理部門が承認済み申請を精算処理する。
```

```
Use uml-workflow-v3 to generate an application from the following business scenario.

Scenario:
Employees submit expense reports. Managers approve or reject them.
The accounting department processes approved expense reports for reimbursement.
```

Claude が自動的にスキルを認識し、対話的に質問しながら10ステップを実行します。 / Claude will automatically recognize the skill, ask a few configuration questions, and execute all 10 steps.

---

## Architecture / アーキテクチャ

### Skill Composition / スキル構成

```
uml-workflow-v3 (メインオーケストレーター / Main Orchestrator)
├── references/ (内蔵パイプラインスキル ×10 / 10 built-in pipeline skills)
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
└── scripts/ (実行エンジン / Execution engine)

usecase-md-to-json         ← UC仕様 Markdown→JSON変換 / UC spec Markdown→JSON converter
classdiagram-image-to-json ← 手描きクラス図取込 / Hand-drawn class diagram importer
json-to-models             ← JSON→PlantUML/XMI再生成 / JSON→PlantUML/XMI regenerator
classdiagram-to-crud       ← クラス図→CRUD HTML生成 / Class diagram→CRUD HTML generator
```

メインスキルが10個のパイプラインスキルを `references/` に内蔵し、残り4つは独立したヘルパースキルとして動作します。 / The main skill bundles all 10 pipeline skills inside `references/`. The remaining 4 operate as independent helper skills.


### Token Efficiency / トークン効率

`references/` 方式により、Claude の `available_skills` カタログに露出するスキルを16→5に削減（69%減）。必要なスキルだけが実行時に動的にロードされます。 / The `references/` approach reduces skills in Claude's `available_skills` catalog from 16 to 5 (69% reduction). Only required skills are loaded dynamically at runtime.


| 実行シナリオ / Scenario | Token削減率 / Reduction |
|------------------------|------------------------|
| 初回フル実行 / First full run | 0%（基準 / baseline） |
| 機能追加（Step 2から再開）/ Add feature (resume from Step 2) | 20–30% |
| モデル調整（Step 3から）/ Model tweak (from Step 3) | 30–40% |
| モデルのみ（Step 1–7）/ Model only (Steps 1–7) | 30–35% |
| バリデーションのみ / Validation only | ~95% |
| 最適組合せ（Step 3＋モデルのみ）/ Optimal combo (Step 3 + model only) | ~75% |

---

## Execution Modes / 実行モード

### 1. Full Workflow / フルワークフロー

```
「uml-workflow-v3で{プロジェクト名}を生成して」
"Generate {project-name} with uml-workflow-v3"
```

全10ステップを実行。初回のプロジェクト生成に使用。 / Executes all 10 steps. Use this for initial project generation.

### 2. Resume from Step / 途中から再開

```
「uml-workflowをStep 5から再開してください」
"Resume uml-workflow from Step 5"
```

指定ステップ以前はキャッシュから復元し、指定ステップ以降を再実行。機能追加などに最適。 / Restores prior steps from cache and re-executes from the specified step onward. Ideal for adding features.

### 3. Model Only / モデルのみ

```
「{プロジェクト名}のモデルのみ生成して」
"Generate models only for {project-name}"
```

Step 1–7 を実行し、コード生成（Step 8–9）をスキップ。設計フェーズや要件確認に最適。 / Runs Steps 1–7 and skips code generation (Steps 8–9). Best for design-phase or requirements review.

### 4. Single Step / 単一ステップ

```
「uml-workflowのStep 6（モデル検証）を実行してください」
"Run Step 6 (model validation) of uml-workflow"
```

特定のステップのみを実行。モデル手動修正後のバリデーションや特定図の再生成に使用。 / Executes one specific step in isolation. Use after manually editing a model or to regenerate a specific diagram.

### 5. Edit Helpers / モデル修正ツール

```
「この手描きのクラス図を取り込んでください」（画像添付 / attach image）
「ユースケース仕様のMarkdownを修正したので、JSONに反映して」
"I've edited the use case Markdown specs. Please update the JSON."
```

ヘルパースキルを使った中間成果物の手動修正。 / Use helper skills to manually edit intermediate artifacts between steps.

---

## Output Files / 出力ファイル

ワークフロー実行後、以下のファイルが生成されます：/ After running the workflow, the following files are generated:

```
{project-name}_activity-data.json       ← Step 1: アクティビティ図データ / Activity diagram data
{project-name}_activity.puml            ← Step 1: PlantUML アクティビティ図 / PlantUML activity diagram
{project-name}_usecase-output.json      ← Step 2: ユースケース定義 / Use case definitions
{project-name}_usecase-diagram.puml     ← Step 2: PlantUML ユースケース図 / PlantUML use case diagram
usecase-specifications/                 ← Step 2: 個別UC仕様（Cockburn形式）/ Individual UC specs (Cockburn format)
  ├── UC-001_*.md
  └── UC-002_*.md
{project-name}_domain-model.json   ⭐   ← Step 3: ドメインモデル（Single Source of Truth）
{project-name}_class.puml               ← Step 3: PlantUML クラス図 / PlantUML class diagram
{project-name}_statemachine.puml        ← Step 4: PlantUML ステートマシン図 / PlantUML state machine diagram
{project-name}_sequence.puml            ← Step 5: PlantUML シーケンス図 / PlantUML sequence diagram
{project-name}_validation-report.md     ← Step 6: バリデーションレポート / Validation report
{project-name}_security-config.json     ← Step 7: セキュリティ設計 / Security design
{project-name}_traceability-matrix.json ← Step 10: トレーサビリティマトリクス / Traceability matrix
{project-name}/                         ← Step 8: 生成アプリケーション / Generated application
  ├── backend/
  ├── frontend/
  ├── tests/
  ├── docker-compose.yml
  └── README.md
```

---

## Skill Files / スキルファイル一覧

| # | Skill ZIP | Size | Role / 役割 |
|---|-----------|------|------------|
| 1 | `uml-workflow-v3.zip` | 154KB | Main orchestrator + 10 pipeline skills / メインオーケストレーター＋10パイプラインスキル |
| 2 | `usecase-md-to-json.zip` | 11KB | UC spec Markdown → JSON converter / UC仕様Markdown→JSON変換 |
| 3 | `classdiagram-image-to-json.zip` | 15KB | Hand-drawn class diagram → JSON / 手描きクラス図取込 |
| 4 | `json-to-models.zip` | 12KB | JSON → PlantUML/XMI regeneration / JSON→PlantUML/XMI再生成 |
| 5 | `classdiagram-to-crud.zip` | 6KB | Class diagram → CRUD HTML fragments / クラス図→CRUD HTML生成 |

> `uml-workflow-v3.zip` のみで10ステップパイプラインは動作します。残り4つはモデル手動修正時の補助ツールです。 / `uml-workflow-v3.zip` alone is sufficient to run the full 10-step pipeline. The other 4 ZIPs are optional helper tools for manual model editing.

---

## Version History / バージョン履歴

| Version | Changes / 変更内容 |
|---------|--------------------|
| **v3.0.0** | 10-step pipeline (Step 10 Traceability Matrix added / トレーサビリティマトリクス追加), references architecture, Claude.ai Skills support / Claude.ai Skills正式対応 |
| v2.0.0 | 9-step pipeline, caching system / キャッシュシステム, XMI optimization / XMI最適化, security design / セキュリティ設計 |
| v1.0.0 | 4-step basic pipeline（シナリオ→ユースケース→クラス図→コード）/ 4-step basic pipeline (scenario → use cases → class diagram → code) |

詳細は [CHANGELOG.md](CHANGELOG.md) を参照。/ See [CHANGELOG.md](CHANGELOG.md) for full details.

---

## Documentation / ドキュメント

| Document | Description / 説明 |
|----------|--------------------|
| [docs/USER_GUIDE.md](docs/USER_GUIDE.md) | 詳細ユーザーガイド / Comprehensive user guide (bilingual) |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | アーキテクチャ解説 / Architecture overview (bilingual) |
| [docs/INSTALLATION_GUIDE.md](docs/INSTALLATION_GUIDE.md) | インストール手順（日本語）/ Installation guide (Japanese) |
| [docs/INSTALLATION_GUIDE_EN.md](docs/INSTALLATION_GUIDE_EN.md) | インストール手順（英語）/ Installation guide (English) |
| [skills/uml-workflow-v3/README.md](skills/uml-workflow-v3/README.md) | スキル詳細説明 / Skill detail guide (bilingual) |
| [CHANGELOG.md](CHANGELOG.md) | 変更履歴 / Change log (bilingual) |
| [CONTRIBUTING.md](CONTRIBUTING.md) | コントリビューションガイド / Contributing guide (bilingual) |
| [examples/expense-report.md](examples/expense-report.md) | サンプルシナリオ / Sample scenario (bilingual) |

---

## Requirements / 動作環境

| Item / 項目 | Requirement / 要件 |
|-------------|-------------------|
| Platform / プラットフォーム | Claude.ai (Web / Desktop / Mobile) |
| Plan / プラン | Pro / Max / Team / Enterprise |
| Feature / 機能 | Code execution and file creation: **ON** |
| Skills / スキル | 5 ZIPs uploaded via Settings > Capabilities |

---

## License / ライセンス

MIT License — see [LICENSE](LICENSE) for details. / 詳細は [LICENSE](LICENSE) を参照。

---

## Contributing / コントリビューション

Issues and Pull Requests are welcome. / Issue・Pull Request 歓迎です。  
See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. / ガイドラインは [CONTRIBUTING.md](CONTRIBUTING.md) を参照。

---

## Acknowledgments / 謝辞

Built with [Claude AI Skills](https://docs.claude.com/en/docs/claude-ai/skills) by [Anthropic](https://www.anthropic.com/). / [Anthropic](https://www.anthropic.com/) の [Claude AI Skills](https://docs.claude.com/en/docs/claude-ai/skills) を活用して構築。
