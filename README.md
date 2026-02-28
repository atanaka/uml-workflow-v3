# UML Workflow v3 / UMLワークフロー v3

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Claude Skills](https://img.shields.io/badge/Claude-Agent_Skills-blueviolet)](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)
[![Skills Count](https://img.shields.io/badge/Skills-14-green)]()

**ビジネスシナリオから本番品質のアプリケーションを自動生成する Claude AI スキル**  
**A Claude AI Skill that transforms business scenarios into production-ready applications via a 10-step UML pipeline.**

## Coming Soon! - Commercial support from a new company / 準備中の新会社による商用サポート

---

## Overview / 概要

UML Workflow v3 は、Claude AI の [Agent Skills](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) 機能を活用した、モデルベースシステムエンジニアリング（MBSE）ワークフローです。自然言語で記述されたビジネスシナリオを入力として、UML図の生成からコード・テストの自動生成まで、10ステップのパイプラインを一貫して実行します。

UML Workflow v3 is a Model-Based Systems Engineering (MBSE) workflow powered by Claude AI [Agent Skills](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview). It takes a natural-language business scenario as input and runs a complete 10-step pipeline — from UML diagram generation through full-stack code and test automation.

### What it does / できること

```
ビジネスシナリオ（自然言語） / Business Scenario (Natural Language)
    ↓
┌──────────────────────────────────────────────────────────────────┐
│  Phase A: Modeling & Validation / モデリング＆バリデーション     │
│                                                                  │
│  Step  1: シナリオ → アクティビティ図 / Scenario → Activity      │
│  Step  2: アクティビティ図 → ユースケース / Activity → Use Cases │
│  Step  3: ユースケース → クラス図 / Use Cases → Class Diagram    │
│  Step  4: クラス図 → ステートマシン図 / Class → State Machine    │
│  Step  5: ユースケース → シーケンス図 / Use Cases → Sequence     │
│  Step  6: モデル横断バリデーション / Cross-Model Validation      │
│  Step  7: OWASP準拠セキュリティ設計 / Security Design            │
├──────────────────────────────────────────────────────────────────┤
│  ✅ Cached → Start new conversation / キャッシュ → 新しい会話へ  │
├──────────────────────────────────────────────────────────────────┤
│  Phase B: Code Generation / コード生成                           │
│                                                                  │
│  Step  8: フルスタックコード生成 / Full-Stack Code Generation    │
│  Step  9: テストコード生成 / Test Code Generation                │
│  Step 10: トレーサビリティマトリクス / Traceability Matrix       │
└──────────────────────────────────────────────────────────────────┘
    ↓
本番品質のアプリケーション + 完全なUMLドキュメント + 追跡可能なエビデンス
Production-Ready Application + Full UML Documentation + Traceable Evidence
```

### Key Features / 主な特長

- **10-Step Pipeline** — シナリオからコード・テストまで一気通貫 / End-to-end automation from scenario to code and tests
- **2-Phase Auto-Split** ⭐ — コンテキストウィンドウ枯渇を自動回避（Phase A → Phase B）/ Automatic context-window split prevents Step 8 failures
- **Bilingual Output** — 日本語・英語の両方に対応（コメント・ドキュメント）/ Japanese and English output supported (comments & docs)
- **Caching System** — 中間成果物を自動キャッシュ、再実行時のトークン消費を最大75%削減 / Auto-caches intermediate artifacts; up to 75% token reduction on reruns
- **Template Lazy Loading** ⭐ — 大規模テンプレートをオンデマンド読込で30%軽量化 / Large templates loaded on demand, 30% reduction in code generation step
- **Flexible Execution** — フル実行、途中再開、単一ステップ実行など複数モード / Full run, resume from step, single-step, and more
- **Security-First** — OWASP Top 10準拠のセキュリティ設計を自動生成 / OWASP Top 10–compliant security design auto-generated at Step 7
- **Full Traceability** — 要件→モデル→コード→テストの双方向追跡マトリクス / Bidirectional traceability matrix: requirements ↔ model ↔ code ↔ tests

---

## Quick Start / クイックスタート

### Prerequisites / 前提条件

- Claude.ai の **Pro** / **Max** / **Team** / **Enterprise** プラン、または Claude Code / Claude.ai **Pro**, **Max**, **Team**, or **Enterprise** plan, or Claude Code
- Claude.ai の場合：「Code execution and file creation」が **有効** / For Claude.ai: "Code execution and file creation" feature **enabled**
- Claude Code の場合：Node.js 18+ がインストール済み / For Claude Code: Node.js 18+ installed

### Installation / インストール

> **📖 公式ドキュメント / Official Documentation**
>
> カスタムスキルの配置方法はプラットフォームごとに異なり、**プラットフォーム間で自動同期されません**。詳細は Anthropic 公式ドキュメントを参照してください。 / Custom Skills installation differs by platform and **does not sync across platforms**. See the official Anthropic documentation:
>
> | Topic / トピック | Link |
> |---|---|
> | スキルの概要・プラットフォーム差異 / Skills overview & platform differences | [Agent Skills Overview](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) |
> | Claude Code でのスキル配置 / Skills in Claude Code | [Extend Claude with Skills (Claude Code)](https://docs.claude.com/en/docs/claude-code/skills) |
> | SKILL.md の書き方・命名規則 / SKILL.md authoring & naming | [Skill Authoring Best Practices](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices) |

#### Option A: Claude Code（CLI）⭐ 推奨 / Recommended

Claude Code ではコンテキストウィンドウの管理が効率的で、`--continue` による再開も可能なため、Step 8 のような大量ファイル生成でも途切れにくくなります。 / Claude Code handles context more efficiently and supports `--continue` for resuming, making it more robust for large code generation steps like Step 8.

**グローバルインストール（全プロジェクト共通）/ Global install (all projects):**

```bash
# リポジトリをクローン / Clone the repository
git clone https://github.com/atanaka/uml-workflow-v3.git

# メインオーケストレーターをコピー / Copy main orchestrator
cp -r uml-workflow-v3/uml-workflow-v3 ~/.claude/skills/uml-workflow-v3

# （任意）スタンドアロンスキルもコピー / (Optional) Copy standalone skills
cp -r uml-workflow-v3/skills/* ~/.claude/skills/
```

**プロジェクト固有インストール / Project-specific install:**

```bash
# プロジェクトルートで実行 / Run at project root
mkdir -p .claude/skills
cp -r /path/to/uml-workflow-v3/uml-workflow-v3 .claude/skills/uml-workflow-v3

# （任意）スタンドアロンスキルもコピー / (Optional) Copy standalone skills
cp -r /path/to/uml-workflow-v3/skills/* .claude/skills/
```

**動作確認 / Verify installation:**

```bash
claude
# Claude Code 内で以下を入力 / Type in Claude Code:
> uml-workflow-v3が使えるか確認して
```

> 💡 Claude Code は `~/.claude/skills/`（個人用）と `.claude/skills/`（プロジェクト用）を自動スキャンします。SKILL.md のフロントマター（name, description）でスキルが自動検出されます。詳細は [Extend Claude with Skills](https://docs.claude.com/en/docs/claude-code/skills) を参照。
>
> 💡 Claude Code auto-scans `~/.claude/skills/` (personal) and `.claude/skills/` (project). Skills are auto-discovered via SKILL.md frontmatter (name, description). See [Extend Claude with Skills](https://docs.claude.com/en/docs/claude-code/skills) for details.

#### Option B: Claude.ai（Web / Desktop / Mobile）

1. [Releases](../../releases) から最新版ZIPをダウンロード / Download the latest ZIP from [Releases](../../releases)
2. ZIP を解凍 / Extract the ZIP
3. Claude.ai → **Customize** → **Skills** セクションを開く / Open Claude.ai → **Customize** → **Skills**
4. 「**Upload skill**」で `uml-workflow-v3/` フォルダをアップロード / Click "**Upload skill**" and upload the `uml-workflow-v3/` folder
5. スキルの**トグルを ON** にする / Toggle the skill **ON**

> これ1つで全10ステップのパイプラインが動作します。/ This single skill runs the full 10-step pipeline.
>
> ⚠️ Claude.ai ではネットワークアクセスの制限やランタイム環境の差異があります。詳細は [Agent Skills Overview — Runtime environments](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) を参照。
>
> ⚠️ Claude.ai has network access limitations and different runtime environments. See [Agent Skills Overview — Runtime environments](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) for details.

詳細は [INSTALL.md](INSTALL.md) を参照。 / See [INSTALL.md](INSTALL.md) for details.

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

Claude が自動的にスキルを認識し、対話的に質問しながら実行します。フルワークフローでは Phase A（Steps 1-7）完了後、Phase B（Steps 8-10）を新しい会話で続行するよう案内されます。 / Claude will automatically recognize the skill, ask configuration questions, and execute all steps. For full workflow, after Phase A (Steps 1-7), Claude instructs you to continue Phase B (Steps 8-10) in a new conversation.

---

## Architecture / アーキテクチャ

### 2-Phase Auto-Split / 2フェーズ自動分割 ⭐

v3.1.0 で導入された自動2フェーズ分割により、コンテキストウィンドウ枯渇によるStep 8停止問題を解消しました。 / The automatic 2-phase split introduced in v3.1.0 eliminates Step 8 failures caused by context window exhaustion.

```
┌─────────────────────────────────────────────────────┐
│  PHASE A: Modeling & Validation (Steps 1-7)         │
│  Token consumption: ~91K ✅ Safe                    │
│                                                     │
│  All artifacts cached → "Start new conversation"    │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│  PHASE B: Code Generation (Steps 8-10)              │
│  Token consumption: ~60K ✅ Safe                    │
│                                                     │
│  Cached artifacts restored → Complete application   │
└─────────────────────────────────────────────────────┘
```

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

`references/` 方式により、Claude の `available_skills` カタログに露出するスキルを最小化。必要なスキルだけが実行時に動的にロードされます。 / The `references/` approach minimizes skills in Claude's `available_skills` catalog. Only required skills are loaded dynamically at runtime.

| 実行シナリオ / Scenario | Token削減率 / Reduction |
|------------------------|------------------------|
| 初回フル実行 / First full run | 0%（基準 / baseline） |
| Phase A のみ（モデルのみ）/ Phase A only (models only) | 35–40% |
| Phase B（コード生成、再開）/ Phase B (code gen, resume) | 45–50% |
| 機能追加（Step 2から再開）/ Add feature (resume from Step 2) | 20–30% |
| モデル調整（Step 3から）/ Model tweak (from Step 3) | 30–40% |
| バリデーションのみ / Validation only | ~95% |
| 最適組合せ（キャッシュ + XMI OFF）/ Optimal combo (cache + XMI OFF) | ~75% |

### Technology Stack / 技術スタック

| Category / カテゴリ | Options / 選択肢 |
|---------------------|------------------|
| **Backend** | TypeScript + Express（推奨）/ NestJS / Python + FastAPI / Java + Spring Boot |
| **Frontend** | React + TypeScript + Vite + Tailwind CSS（推奨）/ Vue 3 + TypeScript / None |
| **Architecture** | Monolith（推奨）/ Microservices / Serverless |
| **Language / 言語** | 日本語 🇯🇵 / English 🇬🇧 / Bilingual 🌏（自動検出 / auto-detect） |

---

## Execution Modes / 実行モード

### 1. Full Workflow / フルワークフロー（2フェーズ自動分割）

```
「uml-workflow-v3で{プロジェクト名}を生成して」
"Generate {project-name} with uml-workflow-v3"
```

Phase A（Steps 1-7）を実行後、自動的にPhase Bの案内を表示。新しい会話で続行。 / Executes Phase A (Steps 1-7), then instructs to continue Phase B (Steps 8-10) in a new conversation.

### 2. Resume from Step / 途中から再開

```
「uml-workflow-v3で{プロジェクト名}のStep 8から再開」
"Resume uml-workflow-v3 for {project-name} from Step 8"
```

指定ステップ以前はキャッシュから復元し、指定ステップ以降を再実行。Phase B の開始にも使用。 / Restores prior steps from cache and re-executes from the specified step onward. Also used to start Phase B.

### 3. Model Only / モデルのみ

```
「{プロジェクト名}のモデルのみ生成して」
"Generate models only for {project-name}"
```

Step 1–7 を実行し、コード生成（Step 8–9）をスキップ。設計フェーズや要件確認に最適。フェーズ分割なし。 / Runs Steps 1–7 and skips code generation (Steps 8–9). Best for design-phase or requirements review. No split needed.

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
{project-name}_statemachine.puml        ← Step 4: PlantUML ステートマシン図 / PlantUML state machine
{project-name}_sequence.puml            ← Step 5: PlantUML シーケンス図 / PlantUML sequence diagrams
{project-name}_validation-report.md     ← Step 6: バリデーションレポート / Validation report
{project-name}_security-design.md       ← Step 7: セキュリティ設計書 / Security design document
{project-name}_security-config.json     ← Step 7: セキュリティ設定 / Security configuration
{project-name}_traceability-matrix.json ← Step 10: トレーサビリティマトリクス / Traceability matrix
{project-name}/                         ← Step 8-9: 生成アプリケーション / Generated application
  ├── backend/
  ├── frontend/
  ├── tests/                            ← Step 9: テストコード / Test code
  ├── docker-compose.yml
  └── README.md
```

---

## Skill Files / スキルファイル一覧

### Required / 必須（1フォルダ / 1 folder）

| # | Skill Folder | Role / 役割 |
|---|-------------|------------|
| 1 | `uml-workflow-v3/` | メインオーケストレーター＋10パイプラインスキル内蔵 / Main orchestrator + 10 built-in pipeline skills |

> `uml-workflow-v3/` のみで10ステップパイプラインは動作します。 / This single skill runs the full 10-step pipeline.

### Optional — Standalone Skills / オプション — スタンドアロンスキル（13フォルダ / 13 folders）

個別利用（単一ステップ実行、モデル手動修正など）向け。フルワークフローには不要。 / For independent use (single-step execution, manual model editing). Not required for the full workflow.

| # | Skill Folder | Role / 役割 |
|---|-------------|------------|
| 2 | `skills/scenario-to-activity-v1/` | シナリオ → アクティビティ図 / Scenario → Activity diagram |
| 3 | `skills/activity-to-usecase-v1/` | アクティビティ図 → ユースケース / Activity → Use cases |
| 4 | `skills/usecase-to-class-v1/` | ユースケース → クラス図 / Use cases → Class diagram |
| 5 | `skills/class-to-statemachine-v1/` | クラス図 → ステートマシン図 / Class → State machines |
| 6 | `skills/usecase-to-sequence-v1/` | ユースケース → シーケンス図 / Use cases → Sequence diagrams |
| 7 | `skills/model-validator-v1/` | モデル横断バリデーション / Cross-model validation |
| 8 | `skills/security-design-v1/` | OWASP準拠セキュリティ設計 / Security design |
| 9 | `skills/usecase-to-code-v1/` | フルスタックコード生成 / Full-stack code generation |
| 10 | `skills/usecase-to-test-v1/` | テストコード生成 / Test code generation |
| 11 | `skills/json-to-models/` | JSON → PlantUML/XMI 再生成 / JSON → PlantUML/XMI regeneration |
| 12 | `skills/usecase-md-to-json/` | UC仕様 Markdown → JSON変換 / UC spec Markdown → JSON converter |
| 13 | `skills/classdiagram-image-to-json/` | 手描きクラス図 → JSON取込 / Hand-drawn class diagram → JSON |
| 14 | `skills/classdiagram-to-crud/` | クラス図 → CRUD HTML生成 / Class diagram → CRUD HTML fragments |

---

## Repository Structure / リポジトリ構造

```
uml-workflow-v3-release/
├── README.md                              ← This file
├── INSTALL.md                             ← インストールガイド / Installation guide
├── CHANGELOG.md                           ← 変更履歴 / Version history
├── CONTRIBUTING.md                        ← コントリビューションガイド / Contribution guide
├── LICENSE                                ← MIT License
├── .gitignore
├── uml-workflow-v3/                       ← メインオーケストレーター / Main orchestrator
│   ├── SKILL.md                           ← 実行仕様 / Execution spec (911 lines)
│   ├── INSTALL.md
│   ├── README.md
│   ├── references/                        ← 内蔵パイプライン / Bundled PIPELINE definitions
│   │   ├── scenario-to-activity-v1/
│   │   ├── activity-to-usecase-v1/
│   │   ├── usecase-to-class-v1/
│   │   ├── class-to-statemachine-v1/
│   │   ├── usecase-to-sequence-v1/
│   │   ├── model-validator-v1/
│   │   ├── security-design-v1/
│   │   ├── usecase-to-code-v1/
│   │   │   └── PIPELINE.md
│   │   ├── usecase-to-test-v1/
│   │   └── traceability-matrix-v1/
│   └── scripts/                           ← Python実行エンジン / Execution engine
└── skills/                                ← スタンドアロンスキル / Standalone skills (13)
    ├── scenario-to-activity-v1/
    ├── activity-to-usecase-v1/
    ├── usecase-to-class-v1/
    ├── class-to-statemachine-v1/
    ├── usecase-to-sequence-v1/
    ├── model-validator-v1/
    ├── security-design-v1/
    ├── usecase-to-code-v1/
    │   ├── SKILL.md
    │   └── templates/                     ← オンデマンド読込 / Lazy-loaded
    ├── usecase-to-test-v1/
    ├── json-to-models/                    ← optional
    ├── usecase-md-to-json/                ← optional
    ├── classdiagram-image-to-json/        ← optional
    └── classdiagram-to-crud/              ← optional
```

---

## Version History / バージョン履歴

| Version | Changes / 変更内容 |
|---------|--------------------|
| **v3.1.0** | 2-Phase Auto-Split（コンテキスト枯渇対策）, Template Lazy Loading（テンプレート遅延読込）, SKILL.md 38%圧縮, PIPELINE.md 30%圧縮, v2-enhanced統合廃止 |
| **v3.0.0** | 10-step pipeline (Step 10 Traceability Matrix追加), references architecture, Claude.ai Skills正式対応 |
| v2.0.0 | 9-step pipeline, caching system / キャッシュシステム, XMI optimization / XMI最適化, security design / セキュリティ設計 |
| v1.0.0 | 4-step basic pipeline（シナリオ→ユースケース→クラス図→コード）/ 4-step basic pipeline (scenario → use cases → class diagram → code) |

詳細は [CHANGELOG.md](CHANGELOG.md) を参照。/ See [CHANGELOG.md](CHANGELOG.md) for full details.

---

## Documentation / ドキュメント

| Document | Description / 説明 |
|----------|--------------------|
| [INSTALL.md](INSTALL.md) | インストール手順 / Installation guide (bilingual) |
| [uml-workflow-v3/README.md](uml-workflow-v3/README.md) | スキル詳細説明 / Skill detail guide |
| [uml-workflow-v3/INSTALL.md](uml-workflow-v3/INSTALL.md) | オーケストレーター説明 / Orchestrator details |
| [CHANGELOG.md](CHANGELOG.md) | 変更履歴 / Change log |
| [CONTRIBUTING.md](CONTRIBUTING.md) | コントリビューションガイド / Contributing guide |

---

## Requirements / 動作環境

| Item / 項目 | Requirement / 要件 |
|-------------|-------------------|
| Platform / プラットフォーム | Claude.ai (Web / Desktop / Mobile) **or** Claude Code (CLI) |
| Plan / プラン | Pro / Max / Team / Enterprise |
| Feature / 機能 | Code execution and file creation: **ON**（Claude.ai の場合 / for Claude.ai） |
| Skills / スキル | Claude.ai: `uml-workflow-v3/` uploaded via Customize > Skills ([手順](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)) |
| | Claude Code: `uml-workflow-v3/` copied to `~/.claude/skills/` or `.claude/skills/` ([手順](https://docs.claude.com/en/docs/claude-code/skills)) |
| Optional / オプション | + 13 standalone skills for independent use / 個別利用向けスタンドアロンスキル13個 |

---

## License / ライセンス

MIT License — see [LICENSE](LICENSE) for details. / 詳細は [LICENSE](LICENSE) を参照。

---

## Contributing / コントリビューション

Issues and Pull Requests are welcome. / Issue・Pull Request 歓迎です。  
See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. / ガイドラインは [CONTRIBUTING.md](CONTRIBUTING.md) を参照。

---

## Acknowledgments / 謝辞

Built with [Claude AI Agent Skills](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) by [Anthropic](https://www.anthropic.com/). / [Anthropic](https://www.anthropic.com/) の [Claude AI Agent Skills](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) を活用して構築。

Methodology based on: **RM-ODP** / **UML 2.5** / **MBSE** / **OWASP Top 10**
