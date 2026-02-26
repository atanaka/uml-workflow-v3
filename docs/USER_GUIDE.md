# User Guide / ユーザーガイド

**UML Workflow v3 — 詳細ユーザーガイド / Comprehensive User Guide**

---

## 目次 / Table of Contents

1. [はじめに / Introduction](#はじめに--introduction)
2. [インストール / Installation](#インストール--installation)
3. [最初の実行 / First Run](#最初の実行--first-run)
4. [10ステップ詳細解説 / 10-Step Deep Dive](#10ステップ詳細解説--10-step-deep-dive)
5. [実行モード完全ガイド / Complete Execution Mode Guide](#実行モード完全ガイド--complete-execution-mode-guide)
6. [キャッシュ活用ガイド / Cache Usage Guide](#キャッシュ活用ガイド--cache-usage-guide)
7. [ヘルパースキル活用ガイド / Helper Skills Guide](#ヘルパースキル活用ガイド--helper-skills-guide)
8. [開発フロー別ガイド / Development Flow Guide](#開発フロー別ガイド--development-flow-guide)
9. [出力ファイル完全リファレンス / Output File Reference](#出力ファイル完全リファレンス--output-file-reference)
10. [バイリンガル対応の詳細 / Bilingual Support Details](#バイリンガル対応の詳細--bilingual-support-details)
11. [トラブルシューティング / Troubleshooting](#トラブルシューティング--troubleshooting)
12. [FAQ](#faq)

---

## はじめに / Introduction

UML Workflow v3 は、Claude AI の Skills 機能を使って構築された、モデルベースシステムエンジニアリング（MBSE）ワークフローです。自然言語で書かれたビジネスシナリオを入力とし、UML モデルの生成からフルスタックアプリケーション・テストコード・トレーサビリティマトリクスの生成まで、10ステップを一貫して自動実行します。

UML Workflow v3 is a Model-Based Systems Engineering (MBSE) workflow built on Claude AI's Skills feature. It takes a natural-language business scenario as input and automatically runs a 10-step pipeline — from UML model generation through full-stack application code, test suites, and a complete traceability matrix.

### このガイドの対象読者 / Target Audience

- Claude.ai で初めてこのワークフローを使う方 / First-time users of this workflow on Claude.ai
- 既存の開発プロセスに組み込みたい方 / Developers integrating this into existing processes
- MBSE・アジャイル開発・ユースケース駆動開発の実践者 / Practitioners of MBSE, Agile, or use case–driven development

---

## インストール / Installation

詳細なインストール手順は言語別のガイドを参照してください：

For detailed installation steps, refer to the language-specific guides:

- **日本語 / Japanese**: [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)
- **English**: [INSTALLATION_GUIDE_EN.md](INSTALLATION_GUIDE_EN.md)

### インストールの概要 / Installation Summary

```
1. GitHub Releases から uml-workflow-v3-all-skills.zip をダウンロード
   Download uml-workflow-v3-all-skills.zip from GitHub Releases

2. ZIP を解凍すると 5 つの ZIP が出現
   Extract to reveal 5 ZIP files

3. Claude.ai → Settings → Capabilities → Skills → Upload skill
   各 ZIP を 1 つずつアップロードし、トグルを ON にする
   Upload each ZIP one by one and toggle each ON

4. 新しい会話を開いてテスト実行
   Open a new conversation and run a test
```

### 必要なもの / Requirements

| 項目 / Item | 要件 / Requirement |
|------------|------------------|
| Platform | Claude.ai Web / Desktop / Mobile |
| Plan | Pro / Max / Team / Enterprise |
| Feature | Code execution and file creation: **ON** |
| Install | 5 ZIP ファイルをアップロード / Upload 5 ZIP files |

> **Pro プランについて / About Pro Plan**: メッセージ制限があるため、大規模シナリオでは全10ステップを完走できない場合があります。大規模なプロジェクトには Max プランを推奨します。  
> Pro plan has message limits, which may prevent completing all 10 steps for large scenarios. Max plan is recommended for large projects.

---

## 最初の実行 / First Run

### Step 1: 新しい会話を開く / Open a New Conversation

Claude.ai で新しい会話を開きます。スキルをアップロードした後に開いた会話でのみスキルが認識されます。

Open a new conversation on Claude.ai. The skills are only recognized in conversations opened after uploading them.

### Step 2: リクエストを入力する / Enter Your Request

以下のいずれかの形式でリクエストを入力してください：

Enter your request in one of these forms:

**日本語で / In Japanese:**
```
uml-workflow-v3を使って、以下のビジネスシナリオからアプリケーションを生成してください。

シナリオ：
[ここにビジネスシナリオを記述]
```

**In English:**
```
Use uml-workflow-v3 to generate an application from the following business scenario.

Scenario:
[Describe your business scenario here]
```

### Step 3: Claude の質問に答える / Answer Claude's Questions

Claude が対話形式で以下の質問をします：

Claude will ask the following questions interactively:

| 質問 / Question | 選択肢 / Options | 推奨 / Recommended |
|----------------|----------------|------------------|
| プロジェクト名 / Project name | 自由入力 / Free input | 英小文字とハイフン / lowercase + hyphens (e.g., `order-system`) |
| キャッシュ使用 / Use cache | はい・いいえ / Yes・No | はい / Yes（初回のみ効果なし / No effect on first run）|
| 実行モード / Execution mode | フルワークフロー / Full workflow など | フルワークフロー / Full workflow（初回 / for first run）|
| XMI生成 / XMI output | はい・いいえ / Yes・No | いいえ / No（UMLツール不要なら / unless you use a UML tool）|
| 出力言語 / Output language | 日本語・English・両方 | プロジェクトに合わせて / match your project |
| テスト生成 / Generate tests | はい・いいえ / Yes・No | はい / Yes |

### Step 4: 実行を待つ / Wait for Execution

Claude が 10ステップを順番に自動実行します。各ステップの完了時に進捗が表示されます。

Claude automatically executes all 10 steps in sequence. Progress is shown as each step completes.

所要時間の目安 / Estimated time:
- 小規模シナリオ（UC 3–5個）/ Small scenario (3–5 UCs): 5–15分
- 中規模シナリオ（UC 6–15個）/ Medium scenario (6–15 UCs): 15–40分
- 大規模シナリオ（UC 16個以上）/ Large scenario (16+ UCs): 40–90分

### Step 5: 成果物を受け取る / Receive Outputs

全ステップ完了後、Claude が成果物ファイルを提示します。ダウンロードまたは Google Drive へのアップロードが可能です。

After all steps complete, Claude presents the output files. You can download them or upload to Google Drive.

---

## 10ステップ詳細解説 / 10-Step Deep Dive

### Step 1: シナリオ → アクティビティ図 / Scenario → Activity Diagram

**役割 / Role**: ビジネスシナリオを業務フローとして可視化します。  
**Purpose**: Visualizes the business scenario as a workflow.

**入力 / Input**: 自然言語のビジネスシナリオ / Natural-language business scenario

**出力 / Output**:
- `{project-name}_activity-data.json` — アクティビティ図の構造データ / Activity diagram structure data
- `{project-name}_activity.puml` — PlantUML アクティビティ図 / PlantUML activity diagram

**処理内容 / What it does**:
シナリオのアクター（登場人物）、業務フロー、条件分岐、エラーケースを分析し、スイムレーン形式のアクティビティ図を生成します。

Analyzes actors, business flows, conditional branches, and error cases in the scenario, then generates a swimlane-style activity diagram.

---

### Step 2: アクティビティ図 → ユースケース / Activity → Use Cases

**役割 / Role**: アクティビティ図からシステムのユースケースを抽出します。  
**Purpose**: Extracts system use cases from the activity diagram.

**入力 / Input**: Step 1 の成果物 / Step 1 artifacts

**出力 / Output**:
- `{project-name}_usecase-output.json` — ユースケース定義（全UC）/ Use case definitions (all UCs)
- `{project-name}_usecase-diagram.puml` — PlantUML ユースケース図
- `usecase-specifications/UC-XXX_*.md` — 個別UC仕様（Cockburn形式）/ Individual UC specs (Cockburn format)

**処理内容 / What it does**:
各アクターが実行できる操作をユースケースとして定義し、Cockburn フォーマットの詳細仕様書（前提条件・成功シナリオ・代替フロー）を生成します。

Defines each actor's operations as use cases and generates detailed specs in Cockburn format (preconditions, success scenario, alternative flows).

---

### Step 3: ユースケース → クラス図 / Use Cases → Class Diagram

**役割 / Role**: ドメインモデル（クラス図）を生成します。**このステップが最も重要**です。  
**Purpose**: Generates the domain model (class diagram). **This is the most critical step.**

**入力 / Input**: Step 1, 2 の成果物 / Step 1 & 2 artifacts

**出力 / Output**:
- `{project-name}_domain-model.json` ⭐ — **Single Source of Truth**
- `{project-name}_class.puml` — PlantUML クラス図 / PlantUML class diagram

**処理内容 / What it does**:
ユースケースを分析してエンティティ、属性、関連、多重度を導出し、Step 4以降のすべてのスキルが参照する domain-model.json を生成します。

Analyzes use cases to derive entities, attributes, associations, and multiplicities, then generates domain-model.json — referenced by all subsequent steps.

> ⭐ `domain-model.json` は後続のすべてのステップ（Step 4–10）が参照します。  
> ⭐ `domain-model.json` is referenced by all subsequent steps (4–10).

---

### Step 4: クラス図 → ステートマシン図 / Class → State Machine

**役割 / Role**: 状態を持つエンティティのライフサイクルを図示します。  
**Purpose**: Diagrams the lifecycle of stateful entities.

**入力 / Input**: Step 3 の domain-model.json

**出力 / Output**:
- `{project-name}_statemachine.puml` — ステートマシン図 / State machine diagram

**処理内容 / What it does**:
`domain-model.json` のエンティティの中から `status` 属性を持つものを特定し、状態遷移・ガード条件・アクションを定義したステートマシン図を生成します。

Identifies entities with `status` attributes in `domain-model.json`, then generates state machine diagrams defining transitions, guard conditions, and actions.

---

### Step 5: ユースケース → シーケンス図 / Use Cases → Sequence Diagrams

**役割 / Role**: ユースケースごとのオブジェクト間の相互作用を図示します。  
**Purpose**: Diagrams inter-object interactions for each use case.

**入力 / Input**: Step 2, 3 の成果物

**出力 / Output**:
- `{project-name}_sequence.puml` — シーケンス図（全UC分）/ Sequence diagrams (one per UC)

**処理内容 / What it does**:
各ユースケースについて、アクター・コントローラー・エンティティ間のメッセージフローをシーケンス図として生成します。エラーフローも含みます。

For each use case, generates a sequence diagram showing message flows between actors, controllers, and entities — including error flows.

---

### Step 6: モデル横断バリデーション / Cross-Model Validation

**役割 / Role**: Step 1–5 の成果物を横断的に検証し、不整合を検出します。  
**Purpose**: Cross-validates artifacts from Steps 1–5 to detect inconsistencies.

**入力 / Input**: Step 1–5 の全成果物

**出力 / Output**:
- `{project-name}_validation-report.md` — バリデーションレポート / Validation report

**検証項目 / Validation items**:
- ユースケースとクラス図の整合性 / Consistency between use cases and class diagram
- アクターとロールの一致 / Actor-role alignment
- ステートマシンの到達可能性 / State machine reachability
- シーケンス図に登場するクラスの実在確認 / Existence of classes appearing in sequence diagrams
- 孤立したユースケース・クラスの検出 / Detection of orphan use cases and classes

バリデーションに失敗した場合は、エラー内容をヘルパースキルで修正してから Step 3 以降を再実行してください。

If validation fails, fix the issues using helper skills and re-run from Step 3.

---

### Step 7: セキュリティ設計 / Security Design

**役割 / Role**: OWASP Top 10 に準拠したセキュリティ設計を自動生成します。  
**Purpose**: Automatically generates OWASP Top 10–compliant security design.

**入力 / Input**: Step 3, 6 の成果物

**出力 / Output**:
- `{project-name}_security-config.json` — セキュリティ設計定義 / Security design configuration

**セキュリティ設計の内容 / Security design contents**:
- 認証・認可設計（ロール・権限マトリクス）/ Authentication & authorization design (role-permission matrix)
- API セキュリティ設計 / API security design
- データ保護方針 / Data protection policy
- OWASP Top 10 対策一覧 / OWASP Top 10 countermeasures
- 監査ログ設計 / Audit logging design

---

### Step 8: フルスタックコード生成 / Full-Stack Code Generation

**役割 / Role**: domain-model.json とセキュリティ設計をもとにフルスタックアプリを生成します。  
**Purpose**: Generates a full-stack application from domain-model.json and security design.

**入力 / Input**: Step 3, 7 の成果物

**出力 / Output**:
```
{project-name}/
├── backend/          Express / NestJS / FastAPI / Spring Boot
├── frontend/         React / Vue / Angular
├── docker-compose.yml
└── README.md
```

**対応テクノロジースタック / Supported Technology Stacks**:

| バックエンド / Backend | フロントエンド / Frontend | DB |
|----------------------|--------------------------|-----|
| Express (TypeScript) | React (TypeScript) | PostgreSQL |
| NestJS | Vue.js | MySQL |
| FastAPI (Python) | Angular | SQLite |
| Spring Boot (Java) | — | MongoDB |

実行開始時に Claude が使用するスタックを確認します。

Claude asks which stack to use at the start of execution.

---

### Step 9: テストコード生成 / Test Code Generation

**役割 / Role**: ユースケースベースのテストコードを生成します。  
**Purpose**: Generates use case–based test code.

**入力 / Input**: Step 2, 3, 8 の成果物

**出力 / Output**:
```
tests/
├── unit/       ユニットテスト / Unit tests (Jest / pytest / JUnit)
└── e2e/        E2Eテスト / E2E tests (Playwright / Cypress)
```

**生成されるテスト / Generated tests**:
- 各ユースケースの正常フローテスト / Normal flow tests for each use case
- 代替フロー・エラーフローテスト / Alternative and error flow tests
- エンティティのバリデーションテスト / Entity validation tests
- 認証・認可テスト / Authentication and authorization tests

---

### Step 10: トレーサビリティマトリクス / Traceability Matrix ⭐ NEW in v3

**役割 / Role**: 要件・モデル・コード・テストの対応関係を双方向に追跡します。  
**Purpose**: Bidirectionally traces the relationships between requirements, models, code, and tests.

**入力 / Input**: Step 1–9 の全成果物

**出力 / Output**:
- `{project-name}_traceability-matrix.json` — 機械可読トレーサビリティデータ
- `{project-name}_traceability-matrix.md` — 人が読むMarkdown形式のマトリクス

**マトリクスの構造 / Matrix Structure**:

```
ビジネス要件 (Business Requirement)
  └── ユースケース (Use Case)
        └── クラス / メソッド (Class / Method)
              └── テストケース (Test Case)
```

**活用シーン / Use Cases**:
- 規制対応・コンプライアンス（ISO、IEC、FDA 21 CFR Part 11 等）
- ステークホルダーへの説明責任の証明
- 変更影響範囲の分析（変更の影響が及ぶテストを即座に特定）

- Regulatory compliance (ISO, IEC, FDA 21 CFR Part 11, etc.)
- Demonstrating accountability to stakeholders
- Change impact analysis (instantly identify which tests are affected by a change)

---

## 実行モード完全ガイド / Complete Execution Mode Guide

### モード選択フロー / Mode Selection Flow

```
新規プロジェクト？
/ New project?
    Yes → フルワークフロー / Full Workflow
    No  →
        キャッシュあり？ / Cache exists?
            Yes →
                変更箇所は？ / Where is the change?
                    初期要件 / Initial requirements → Step 1 から再開 / Resume from Step 1
                    UC定義 / UC definitions      → Step 2 から再開 / Resume from Step 2
                    クラス図 / Class diagram      → Step 3 から再開 / Resume from Step 3
                    コードのみ / Code only        → Step 8 から再開 / Resume from Step 8
            No →
                フルワークフロー / Full Workflow
                    または
                モデルのみ（設計フェーズ）/ Model Only (design phase)
```

### モードごとの実行ステップ / Steps per Mode

| モード / Mode | 実行ステップ / Steps | 用途 / Purpose |
|-------------|-------------------|--------------|
| Full Workflow | 1–10 | 初回生成 / Initial generation |
| Resume from Step N | N–10 | 機能追加・修正 / Feature add/fix |
| Model Only | 1–7 | 設計レビュー / Design review |
| Single Step N | N のみ / N only | 特定ステップ再実行 / Rerun specific step |
| Validation Only | 6 のみ / 6 only | バリデーション / Validation |

---

## キャッシュ活用ガイド / Cache Usage Guide

### キャッシュの仕組み / How Cache Works

UML Workflow v3 は各ステップの成果物を自動的にキャッシュします。次回の実行時に「どのステップから実行するか」を指定すると、それ以前のステップの成果物をキャッシュから復元します。

UML Workflow v3 automatically caches each step's artifacts. On the next run, specify "which step to start from," and artifacts from prior steps are restored from cache.

```
キャッシュ保存場所 / Cache location:
/mnt/user-data/outputs/workflow-cache/
├── cache_index.json         ← プロジェクト一覧 / Project registry
└── {project-name}/
    ├── scenario_to_activity_activity-data.json
    ├── scenario_to_activity_activity.puml
    ├── activity_to_usecase_usecase-output.json
    ├── activity_to_usecase_usecase-diagram.puml
    ├── usecase_to_class_domain-model.json
    ├── usecase_to_class_class.puml
    ├── class_to_statemachine_statemachine.puml
    ├── usecase_to_sequence_sequence.puml
    └── model_validator_validation-report.md
```

### キャッシュのライフサイクル / Cache Lifecycle

```
Step 実行完了 / Step completes
  → 自動的にキャッシュ保存 / Auto-saved to cache
  
次回実行 / Next run
  → キャッシュ検出 / Cache detected
  → ユーザー確認 / User confirms
  → 前段ステップを復元 / Restore prior steps
  → 指定ステップから再実行 / Re-run from specified step
  
手動クリア / Manual clear
  「{project-name}のキャッシュをクリアして」
  "Clear cache for {project-name}"
```

### キャッシュを活用した反復開発パターン / Iterative Development Pattern with Cache

```
Phase 1: 初期設計 / Initial design
  → Full Workflow（Step 1–7、Model Only）
  → キャッシュ済み ✅

Phase 2: モデルレビュー → クラス図修正 / Review → Fix class diagram
  → classdiagram-image-to-json でモデル修正
  → Resume from Step 3（Step 1–2 はキャッシュから）
  → Token削減: 約40%

Phase 3: コード生成 / Code generation
  → Resume from Step 8（Step 1–7 はキャッシュから）
  → Token削減: 約50%

Phase 4: 機能追加 / Feature addition
  → Resume from Step 2（Step 1 はキャッシュから）
  → Token削減: 約20%
```

---

## ヘルパースキル活用ガイド / Helper Skills Guide

### usecase-md-to-json

UC仕様書（Markdown）を JSON に変換します。UC仕様を直接編集したいときに使います。

Converts use case spec Markdown to JSON. Use when you want to edit UC specs directly.

```
ワークフロー / Workflow:
  1. usecase-specifications/UC-001_*.md を直接編集
     Directly edit usecase-specifications/UC-001_*.md
  2. 「ユースケース仕様のMarkdownを修正したので、JSONに反映してください」
     "I've edited the UC Markdown specs. Please update the JSON."
  3. usecase-md-to-json が MD → JSON を変換
  4. Step 3 以降を再実行
     Re-run from Step 3
```

### classdiagram-image-to-json

手書き・画像のクラス図を JSON に取り込みます。ホワイトボードや paper のクラス図を使いたいときに使います。

Imports a hand-drawn or image class diagram into JSON. Use when you have a whiteboard or paper class diagram.

```
ワークフロー / Workflow:
  1. クラス図の写真を撮る / Take a photo of the class diagram
  2. 「この手描きのクラス図を取り込んでください」（画像添付）
     "Import this hand-drawn class diagram" (attach image)
  3. classdiagram-image-to-json が画像 → JSON に変換
  4. Step 4 以降を再実行
     Re-run from Step 4
```

### json-to-models

domain-model.json を修正した後、PlantUML 図や XMI を再生成します。

Regenerates PlantUML diagrams or XMI after editing domain-model.json.

```
ワークフロー / Workflow:
  1. domain-model.json をテキストエディタで直接修正
     Directly edit domain-model.json in a text editor
  2. 「domain-model.jsonを更新したので、クラス図とXMIを再生成して」
     "I've updated domain-model.json. Regenerate the class diagram and XMI."
  3. json-to-models が PlantUML / XMI を再生成
  4. Step 4 以降を再実行（任意）/ Re-run from Step 4 (optional)
```

### classdiagram-to-crud

クラス図（domain-model.json）から CRUD 操作用の HTML フラグメントを生成します。プロトタイピングに便利です。

Generates CRUD HTML fragments from the class diagram. Useful for prototyping.

```
ワークフロー / Workflow:
  1. 「{エンティティ名}のCRUD画面を生成して」
     "Generate CRUD screens for {entity name}"
  2. classdiagram-to-crud が HTML フラグメントを生成
  3. 生成された HTML を確認・修正してフロントエンドに組み込む
     Review and integrate the generated HTML into your frontend
```

---

## 開発フロー別ガイド / Development Flow Guide

### フロー 1: スクラム・アジャイル開発 / Scrum / Agile Development

```
Sprint 0: ドメインモデル確定 / Domain model finalization
  1. フルワークフロー（モデルのみ）
     Full Workflow (Model Only, Steps 1–7)
  2. ステークホルダーレビュー
     Stakeholder review
  3. フィードバックをもとにモデル修正（Step 3 から再開）
     Model refinement based on feedback (Resume from Step 3)

Sprint 1: 認証 + コアエンティティ / Auth + core entities
  1. Step 8 から再開（コード生成）
     Resume from Step 8 (code generation)
  2. Step 9（テスト生成）
     Step 9 (test generation)
  3. Step 10（トレーサビリティ確認）
     Step 10 (verify traceability)

Sprint 2+: 機能追加 / Feature additions
  1. 新しいUCをシナリオに追記
     Add new UCs to scenario
  2. Step 2 から再開（30% token 削減）
     Resume from Step 2 (30% token reduction)
```

### フロー 2: ウォーターフォール / Waterfall

```
要件定義フェーズ / Requirements Phase
  → Step 1, 2 のみ実行
  → ユースケース一覧をステークホルダーと確認

設計フェーズ / Design Phase
  → Step 3–7 を実行（モデルのみモード）
  → バリデーションレポートで品質確認
  → セキュリティ設計書をセキュリティチームとレビュー

実装フェーズ / Implementation Phase
  → Step 8, 9 を実行（コード + テスト生成）
  → Step 10 でトレーサビリティマトリクス生成
  → コードレビュー・品質確認

受入テストフェーズ / Acceptance Phase
  → トレーサビリティマトリクスを根拠に受入テスト実施
```

### フロー 3: 規制対応開発 / Regulatory-Compliant Development

```
対象: 医療機器・航空・金融など / Target: Medical, aviation, finance, etc.

1. Full Workflow で全成果物を生成
2. Step 10 のトレーサビリティマトリクスを規制当局提出用ドキュメントとして利用
3. Step 6 のバリデーションレポートを品質証跡として保存
4. Step 7 のセキュリティ設計書をセキュリティ評価の根拠として利用

提出ドキュメント / Submission documents:
  ✅ {project-name}_traceability-matrix.md (要件追跡)
  ✅ {project-name}_validation-report.md  (設計品質証跡)
  ✅ {project-name}_security-config.json  (セキュリティ評価)
  ✅ usecase-specifications/              (機能要件詳細)
```

---

## 出力ファイル完全リファレンス / Output File Reference

### Step別出力ファイル一覧 / Output Files by Step

| Step | ファイル / File | 形式 / Format | 用途 / Purpose |
|------|---------------|-------------|--------------|
| 1 | `*_activity-data.json` | JSON | アクティビティ図構造データ / Activity structure data |
| 1 | `*_activity.puml` | PlantUML | アクティビティ図 / Activity diagram |
| 2 | `*_usecase-output.json` | JSON | ユースケース定義全体 / All UC definitions |
| 2 | `*_usecase-diagram.puml` | PlantUML | ユースケース図 / Use case diagram |
| 2 | `usecase-specifications/UC-*.md` | Markdown | 個別UC仕様（Cockburn形式）/ Individual UC specs |
| 3 | `*_domain-model.json` ⭐ | JSON | ドメインモデル（SoT）/ Domain model (SoT) |
| 3 | `*_class.puml` | PlantUML | クラス図 / Class diagram |
| 4 | `*_statemachine.puml` | PlantUML | ステートマシン図 / State machine diagram |
| 5 | `*_sequence.puml` | PlantUML | シーケンス図 / Sequence diagram |
| 6 | `*_validation-report.md` | Markdown | バリデーションレポート / Validation report |
| 7 | `*_security-config.json` | JSON | セキュリティ設計 / Security design |
| 8 | `{project-name}/` | Directory | 生成アプリ / Generated app |
| 9 | `tests/` | Directory | テストコード / Test code |
| 10 | `*_traceability-matrix.json` | JSON | トレーサビリティ（機械可読）/ Traceability (machine-readable) |
| 10 | `*_traceability-matrix.md` | Markdown | トレーサビリティ（人間可読）/ Traceability (human-readable) |

### PlantUML ファイルの利用 / Using PlantUML Files

生成された `.puml` ファイルは以下の方法で UML 図として表示できます：

Generated `.puml` files can be rendered as UML diagrams in the following ways:

1. **PlantUML オンライン / PlantUML Online**: [plantuml.com](https://plantuml.com)
2. **VS Code 拡張 / VS Code Extension**: "PlantUML" extension
3. **IntelliJ IDEA プラグイン / IntelliJ IDEA Plugin**: PlantUML Integration plugin
4. **Mermaid 変換 / Mermaid conversion**: Claude に変換依頼 / Ask Claude to convert

---

## バイリンガル対応の詳細 / Bilingual Support Details

UML Workflow v3 は、入力シナリオの言語に関わらず、出力を日本語・英語・両方で生成できます。

UML Workflow v3 can generate outputs in Japanese, English, or both — regardless of the input scenario's language.

### 言語の指定方法 / How to Specify Language

実行開始時の質問で選択します：

Select at the start of execution:

| 選択肢 / Option | 効果 / Effect |
|---------------|--------------|
| 日本語 | コード内コメント・ドキュメント・UML図ラベルを日本語で生成 |
| English | Generate code comments, docs, and UML labels in English |
| 両方 / Both | コメントを日英バイリンガルで生成 / Generate bilingual comments |

### バイリンガル出力のサンプル / Bilingual Output Sample

**コードコメント / Code Comments (Both)**:
```typescript
/**
 * 経費申請を作成する / Create an expense report
 * @param input 申請データ / Report input data
 * @returns 作成された申請 / Created expense report
 */
async createExpenseReport(input: CreateExpenseReportInput): Promise<ExpenseReport> {
  // 申請金額の検証 / Validate report amount
  if (input.amount <= 0) {
    throw new ValidationError('金額は0より大きい必要があります / Amount must be greater than 0');
  }
  // ...
}
```

**UML 図のラベル / UML Diagram Labels (Both)**:
```
usecase "経費申請 / Submit Expense Report" as UC001
actor "従業員 / Employee" as EMP
```

---

## トラブルシューティング / Troubleshooting

### スキルが認識されない / Skill Not Recognized

**症状 / Symptom**: "uml-workflow-v3" と入力しても Claude がスキルを認識しない。  
"uml-workflow-v3" is typed but Claude doesn't recognize the skill.

**確認事項 / Check**:
1. Settings > Capabilities で `uml-workflow-v3` のトグルが **ON** か / Toggle is **ON** in Settings > Capabilities
2. 「コード実行とファイル作成」が **ON** か / "Code execution and file creation" is **ON**
3. スキルをアップロード **後** に開いた会話か / Conversation was opened **after** uploading the skills

---

### ステップの途中でエラーが発生した / Error During Step Execution

**症状 / Symptom**: Step N でエラーが発生し、実行が止まった。  
An error occurred at Step N and execution stopped.

**対処 / Solution**:
1. エラーメッセージを確認する / Read the error message
2. Claude に「Step N からやり直してください」と依頼する / Ask Claude to "Retry from Step N"
3. キャッシュが存在する場合、前段の成果物は保持されます / If cache exists, prior artifacts are preserved

---

### バリデーションエラーが多い / Many Validation Errors

**症状 / Symptom**: Step 6 で多くのエラーが報告された。  
Many errors reported at Step 6.

**対処 / Solution**:
1. バリデーションレポートでエラー箇所を確認 / Check error locations in validation report
2. 主なエラーに対してヘルパースキルでモデルを修正 / Fix main errors in model using helper skills
3. Step 3 から再開して修正を反映 / Resume from Step 3 to apply fixes
4. Step 6 を単独実行して再検証 / Run Step 6 alone to re-validate

---

### 生成されたコードにエラーがある / Generated Code Has Errors

**症状 / Symptom**: Step 8 で生成されたコードが型エラーや参照エラーを含む。  
Code generated at Step 8 contains type or reference errors.

**対処 / Solution**:
1. エラーの内容を Claude に伝える / Report the error to Claude
2. domain-model.json の該当エンティティ定義を確認・修正 / Check and fix the relevant entity in domain-model.json
3. json-to-models で図を再生成し、Step 8 から再実行 / Regenerate diagrams with json-to-models and re-run from Step 8

---

## FAQ

**Q: ビジネスシナリオはどれくらい詳細に書けばいいですか？**  
**Q: How detailed should the business scenario be?**

A: 最低限、以下を含めてください / At minimum, include:
- アクター（誰が使うか）/ Actors (who uses it)
- 主な業務フロー（何をするか）/ Main flows (what they do)
- ビジネスルール（制約）/ Business rules (constraints)

詳細であるほど精度が上がります。サンプルは `examples/expense-report.md` を参照してください。

More detail = better accuracy. See `examples/expense-report.md` for a sample.

---

**Q: 1回の実行でどれくらいの規模のシステムに対応できますか？**  
**Q: How large a system can be handled in one run?**

A:
- **Max プラン**: UC 20個、エンティティ 15–20個程度まで快適に動作
- **Pro プラン**: UC 5–10個程度が実用的な上限

- **Max plan**: Works well up to ~20 UCs and 15–20 entities
- **Pro plan**: ~5–10 UCs is a practical limit

---

**Q: 生成されたコードはそのまま本番環境で使えますか？**  
**Q: Can the generated code be used in production as-is?**

A: 生成されたコードはスキャフォールディング（骨格）として機能します。実際の本番投入には以下が必要です / The generated code serves as scaffolding. For production use, you will need:
- ビジネスロジックの具体的な実装 / Concrete business logic implementation
- データベース接続設定 / Database connection configuration
- 環境変数・シークレット管理 / Environment variables and secret management
- CI/CD パイプラインの構築 / CI/CD pipeline setup
- セキュリティ設定の本番向け調整 / Production tuning of security settings

---

**Q: PlantUML の図を編集した後、コードに反映させるには？**  
**Q: After editing a PlantUML diagram, how do I reflect it in the code?**

A: PlantUML ファイルを直接編集しても domain-model.json には反映されません。以下の手順を使ってください / Editing PlantUML directly doesn't update domain-model.json. Use this process:
1. `domain-model.json` をテキストエディタで直接編集 / Directly edit `domain-model.json`
2. `json-to-models` スキルで PlantUML を再生成 / Regenerate PlantUML with `json-to-models`
3. Step 4 以降を再実行 / Re-run from Step 4

---

**Q: 日本語のシナリオを英語のコードに変換できますか？**  
**Q: Can a Japanese scenario be converted to English code?**

A: はい。実行開始時の言語設定で「English」を選択すると、日本語のシナリオから英語のコード・コメント・ドキュメントを生成します。

Yes. Select "English" in the language setting at the start of execution, and Japanese scenarios will produce English code, comments, and documentation.

---

*このガイドに関する質問・提案は [GitHub Issues](../../issues) または [Discussions](../../discussions) でどうぞ。*  
*For questions or suggestions about this guide, use [GitHub Issues](../../issues) or [Discussions](../../discussions).*
