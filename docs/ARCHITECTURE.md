# Architecture / アーキテクチャ

**UML Workflow v3 — アーキテクチャドキュメント / Architecture Document**

---

## 目次 / Table of Contents

1. [システム概要 / System Overview](#システム概要--system-overview)
2. [スキル構成 / Skill Composition](#スキル構成--skill-composition)
3. [データフロー / Data Flow](#データフロー--data-flow)
4. [キャッシュアーキテクチャ / Cache Architecture](#キャッシュアーキテクチャ--cache-architecture)
5. [references 方式 / References Approach](#references-方式--references-approach)
6. [設計判断と根拠 / Design Decisions & Rationale](#設計判断と根拠--design-decisions--rationale)

---

## システム概要 / System Overview

UML Workflow v3 は、Claude AI の Skills 機能を使って構築された **10ステップ MBSE パイプライン** です。ビジネスシナリオを入力として、UML モデル・アプリケーションコード・テスト・トレーサビリティマトリクスを段階的に生成します。

UML Workflow v3 is a **10-step MBSE pipeline** built on Claude AI's Skills feature. It takes a business scenario as input and progressively generates UML models, application code, tests, and a traceability matrix.

### 設計原則 / Design Principles

1. **Single Source of Truth** — `domain-model.json` が全ステップの共通データモデル  
   `domain-model.json` serves as the shared data model for all steps

2. **段階的洗練 / Progressive Refinement** — 各ステップが前ステップの成果物を精緻化  
   Each step refines artifacts from prior steps

3. **キャッシュファースト / Cache-First** — 中間成果物を自動保存し、再実行コストを最小化  
   Auto-save intermediate artifacts to minimize re-run costs

4. **references方式 / References Approach** — サブスキルをメインスキルに内蔵し、カタログ露出を削減  
   Sub-skills embedded in main skill to reduce catalog exposure

5. **バイリンガル / Bilingual** — 入出力・コメント・ドキュメントを日英両対応  
   Input/output, comments, and docs support both Japanese and English

---

## スキル構成 / Skill Composition

### Claude.ai での構成 / Composition in Claude.ai

```
Claude.ai Skills Catalog (5スキル公開 / 5 skills exposed)
│
├── uml-workflow-v3          ← メインオーケストレーター / Main orchestrator
│                               + 10個のパイプラインスキルを内蔵
│                               + 10 pipeline skills embedded as references
│
├── usecase-md-to-json       ← ヘルパー / Helper: UC MD → JSON
├── classdiagram-image-to-json ← ヘルパー / Helper: Image → JSON
├── json-to-models           ← ヘルパー / Helper: JSON → PlantUML/XMI
└── classdiagram-to-crud     ← ヘルパー / Helper: Class → CRUD HTML
```

### ファイルシステム構造 / File System Structure

```
uml-workflow-v3/
├── SKILL.md                           ← Claude 向け実行仕様 / Claude execution spec
├── README.md                          ← ユーザー向け説明 / User-facing docs
├── INSTALL.md                         ← インストール手順 / Install steps
│
├── references/                        ← パイプラインスキル（内蔵）/ Pipeline skills (embedded)
│   ├── scenario-to-activity-v1/
│   │   └── SKILL.md                   ← Step 1 の実行仕様
│   ├── activity-to-usecase-v1/
│   │   └── SKILL.md                   ← Step 2
│   ├── usecase-to-class-v1/
│   │   └── SKILL.md                   ← Step 3 (SoT生成)
│   ├── class-to-statemachine-v1/
│   │   └── SKILL.md                   ← Step 4
│   ├── usecase-to-sequence-v1/
│   │   └── SKILL.md                   ← Step 5
│   ├── model-validator-v1/
│   │   └── SKILL.md                   ← Step 6
│   ├── security-design-v1/
│   │   └── SKILL.md                   ← Step 7
│   ├── usecase-to-code-v1/
│   │   └── SKILL.md                   ← Step 8
│   ├── usecase-to-test-v1/
│   │   └── SKILL.md                   ← Step 9
│   └── traceability-matrix-v1/
│       └── SKILL.md                   ← Step 10
│
└── scripts/                           ← Python 実行エンジン / Python execution engine
    ├── run_workflow.py                ← エントリポイント / Entry point
    ├── unified_workflow_executor.py   ← 統合実行エンジン / Unified executor
    ├── interactive_workflow_executor.py ← 対話型実行 / Interactive execution
    ├── execution_mode_manager.py      ← モード管理 / Mode manager
    └── workflow_cache_helper.py       ← キャッシュ管理 / Cache manager
```

---

## データフロー / Data Flow

### パイプラインのデータフロー / Pipeline Data Flow

```
Input: Business Scenario (Natural Language / 自然言語)
       ↓
Step 1: scenario-to-activity-v1
       Input:  business scenario text
       Output: activity-data.json ──────────────────────┐
               activity.puml                            │
       ↓                                                │
Step 2: activity-to-usecase-v1                          │
       Input:  activity-data.json ◄─────────────────────┘
       Output: usecase-output.json ───────────────────────┐
               usecase-diagram.puml                       │
               usecase-specifications/UC-*.md             │
       ↓                                                  │
Step 3: usecase-to-class-v1                              │
       Input:  usecase-output.json ◄─────────────────────┘
               usecase-specifications/
       Output: domain-model.json ⭐ (SoT) ───────────────────────────────┐
               class.puml                                                 │
       ↓                                                                  │
Step 4: class-to-statemachine-v1                                         │
       Input:  domain-model.json ◄───────────────────────────────────────┤
       Output: statemachine.puml                                          │
       ↓                                                                  │
Step 5: usecase-to-sequence-v1                                           │
       Input:  usecase-output.json + domain-model.json ◄─────────────────┤
       Output: sequence.puml                                              │
       ↓                                                                  │
Step 6: model-validator-v1                                               │
       Input:  All Step 1-5 artifacts                                    │
       Output: validation-report.md                                       │
       ↓                                                                  │
Step 7: security-design-v1                                               │
       Input:  domain-model.json ◄───────────────────────────────────────┤
               validation-report.md                                       │
       Output: security-config.json                                       │
       ↓                                                                  │
Step 8: usecase-to-code-v1                                               │
       Input:  domain-model.json ◄───────────────────────────────────────┤
               security-config.json                                       │
       Output: {project-name}/ (application code)                        │
       ↓                                                                  │
Step 9: usecase-to-test-v1                                               │
       Input:  usecase-output.json + domain-model.json ◄─────────────────┤
               {project-name}/                                            │
       Output: tests/ (unit + e2e)                                       │
       ↓                                                                  │
Step 10: traceability-matrix-v1                                          │
       Input:  All Step 1-9 artifacts                                    │
       Output: traceability-matrix.json                                  │
               traceability-matrix.md                                    │
       ↓                                                                 ↓
Output: Production App + UML Docs + Test Suite + Traceability Matrix
```

### domain-model.json の構造 / domain-model.json Structure

```json
{
  "project": {
    "name": "expense-management",
    "version": "1.0.0",
    "language": "ja"
  },
  "entities": [
    {
      "name": "ExpenseReport",
      "nameJa": "経費申請",
      "attributes": [
        { "name": "id", "type": "UUID", "required": true },
        { "name": "amount", "type": "Decimal", "required": true },
        { "name": "status", "type": "ExpenseStatus", "required": true }
      ],
      "methods": [
        { "name": "submit", "returnType": "void" },
        { "name": "approve", "parameters": [{"name": "approver", "type": "User"}] }
      ]
    }
  ],
  "enums": [
    {
      "name": "ExpenseStatus",
      "values": ["DRAFT", "SUBMITTED", "APPROVED", "REJECTED", "SETTLED"]
    }
  ],
  "associations": [
    {
      "from": "User",
      "to": "ExpenseReport",
      "type": "ONE_TO_MANY",
      "role": "submits"
    }
  ]
}
```

---

## キャッシュアーキテクチャ / Cache Architecture

### キャッシュの設計 / Cache Design

```
/mnt/user-data/outputs/
└── workflow-cache/
    ├── cache_index.json          ← プロジェクト管理 / Project registry
    └── {project-name}/
        ├── step1_activity-data.json
        ├── step1_activity.puml
        ├── step2_usecase-output.json
        ├── step2_usecase-diagram.puml
        ├── step3_domain-model.json      ← SoT のキャッシュ / SoT cache
        ├── step3_class.puml
        ├── step4_statemachine.puml
        ├── step5_sequence.puml
        ├── step6_validation-report.md
        ├── step7_security-config.json
        └── cache_metadata.json          ← キャッシュメタデータ / Cache metadata
```

### cache_index.json の構造 / cache_index.json Structure

```json
{
  "version": "3.0.0",
  "projects": {
    "expense-management": {
      "lastModified": "2026-02-26T10:00:00Z",
      "completedSteps": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
      "language": "ja",
      "techStack": "express-react"
    }
  }
}
```

### キャッシュの再利用戦略 / Cache Reuse Strategy

```
実行開始 / Execution starts
  ↓
プロジェクト名を確認 / Check project name
  ↓
cache_index.json にエントリがあるか？ / Entry in cache_index.json?
  Yes →
    ユーザーに確認 / Ask user:
    「{project-name}のキャッシュが見つかりました。使用しますか？」
    "Cache found for {project-name}. Use it?"
      Yes →
        指定ステップ N より前のステップのキャッシュを読み込む
        Load cache for steps before N
        Step N から実行開始 / Start execution from Step N
      No →
        キャッシュを無視してStep 1 から実行
        Ignore cache, start from Step 1
  No →
    Step 1 から実行 / Start from Step 1
```

---

## references 方式 / References Approach

### 課題と解決策 / Problem and Solution

**課題 / Problem**:  
v2 では 10個のパイプラインスキルすべてをユーザーが個別にインストールする必要がありました（15 ZIP）。Claude の `available_skills` カタログに15スキルが露出し、毎回のコンテキストで 1,700 tokens を消費していました。

In v2, users had to install all 10 pipeline skills individually (15 ZIPs). All 15 skills were exposed in Claude's `available_skills` catalog, consuming 1,700 tokens in every context.

**解決策 / Solution**:  
メインスキル `uml-workflow-v3` の `references/` ディレクトリに10個のパイプラインスキルを内蔵しました。Claude の `available_skills` に露出するのはメインスキルのみとなり、サブスキルは実行時に動的にロードされます。

Embedded all 10 pipeline skills in the `references/` directory of the main skill `uml-workflow-v3`. Only the main skill is exposed in Claude's `available_skills`; sub-skills are dynamically loaded at runtime.

```
Before v3 (v2):                    After v3:
available_skills:                  available_skills:
  - uml-workflow-v2-enhanced         - uml-workflow-v3          ← メイン
  - scenario-to-activity-v1          - usecase-md-to-json       ← ヘルパー
  - activity-to-usecase-v1           - classdiagram-image-to-json
  - usecase-to-class-v1              - json-to-models
  - class-to-statemachine-v1         - classdiagram-to-crud
  - usecase-to-sequence-v1
  - model-validator-v1             合計 / Total: 5スキル
  - security-design-v1             Token消費 / Token cost: ~600
  - usecase-to-code-v1
  - usecase-to-test-v1             削減 / Reduction:
  - traceability-matrix-v1           スキル数: 16 → 5 (69%減)
  - usecase-md-to-json               Token: 1,700 → 600 (65%減)
  - classdiagram-image-to-json
  - json-to-models
  - classdiagram-to-crud
合計 / Total: 16スキル
Token消費 / Token cost: ~1,700
```

### references の仕組み / How References Work

Claude は `uml-workflow-v3/SKILL.md` を読み込む際、`references/` ディレクトリの各スキルの `SKILL.md` も自動的に読み込みます。実行時にサブスキルが動的に参照され、パイプラインの各ステップが実行されます。

When Claude loads `uml-workflow-v3/SKILL.md`, it automatically loads the `SKILL.md` of each skill in `references/`. At runtime, sub-skills are dynamically referenced, executing each pipeline step.

---

## 設計判断と根拠 / Design Decisions & Rationale

### 1. domain-model.json を Single Source of Truth にした理由 / Why domain-model.json as SoT

**判断 / Decision**: Step 3 で生成した `domain-model.json` を全後続ステップで共有する  
**Rationale**: 

- PlantUML はテキストとして直接編集できるが、後続ステップが参照するには JSON が適している
- JSON は型安全で機械可読、かつ人間にも読みやすい
- ヘルパースキルが JSON を更新することで、全ステップへの変更伝播が一元化される

- PlantUML can be edited directly, but JSON is better for downstream steps to reference
- JSON is type-safe, machine-readable, and human-readable
- Helper skills update JSON, centralizing change propagation to all steps

### 2. キャッシュをファイルシステムに保存する理由 / Why File-System Cache

**判断 / Decision**: キャッシュを `/mnt/user-data/outputs/workflow-cache/` に保存する  
**Rationale**:

- Claude.ai の会話メモリはセッション間で保持されないため、永続的なファイルシステムを使用する必要がある
- `/mnt/user-data/outputs/` は Claude.ai の Code execution で書き込み可能な唯一の永続パス

- Claude.ai conversation memory doesn't persist across sessions, so persistent file system storage is needed
- `/mnt/user-data/outputs/` is the only writable persistent path in Claude.ai code execution

### 3. XMI生成をデフォルト OFF にした理由 / Why XMI Off by Default

**判断 / Decision**: XMI 生成を全モードでデフォルト OFF にする  
**Rationale**:

- XMI は主に Enterprise Architect などの外部 UML ツールへの入力に使われる
- 多くのユーザーはUMLツールとの連携を必要としない
- XMI 生成は各ステップで最大40%の処理時間を追加する

- XMI is primarily used as input for external UML tools like Enterprise Architect
- Most users don't need UML tool integration
- XMI generation adds up to 40% processing time per step

### 4. Step 10 をトレーサビリティマトリクスにした理由 / Why Step 10 for Traceability

**判断 / Decision**: v3 で Step 10 としてトレーサビリティマトリクスを追加する  
**Rationale**:

- 要件→モデル→コード→テストの対応関係を証明できるドキュメントは規制産業（医療・航空・金融）で必須
- Step 1–9 が完了した後に全成果物を参照して生成するため、最終ステップが適切
- JSON 形式で出力することで、外部ツール（CI/CD、品質管理システム）との連携が可能

- Documents proving requirements→model→code→test mapping are mandatory in regulated industries
- Generating after Steps 1–9 complete allows referencing all artifacts — making it the natural final step
- JSON output enables integration with external tools (CI/CD, quality management systems)

### 5. Python スクリプトを使う理由 / Why Python Scripts

**判断 / Decision**: ワークフロー実行ロジックを Python スクリプトとして実装する  
**Rationale**:

- Claude の Code execution 機能で Python が実行可能
- キャッシュ管理・ファイル I/O・実行計画の生成など、複雑なロジックを Claude の Markdown 指示より Python でより確実に実装できる
- スクリプトがバージョン管理可能で、バグ修正がデプロイしやすい

- Python is executable in Claude's Code execution feature
- Complex logic (cache management, file I/O, execution planning) is more reliably implemented in Python than Claude markdown instructions
- Scripts are version-controllable and fixes are easy to deploy

---

## パフォーマンス特性 / Performance Characteristics

### トークン消費の内訳 / Token Consumption Breakdown

| 項目 / Item | v2 | v3 | 削減率 / Reduction |
|------------|-----|-----|-----------------|
| `available_skills` | ~1,700 | ~600 | 65% |
| 各ステップの system prompt | 変わらず / unchanged | 変わらず | — |
| キャッシュ活用時の削減 | 最大75% | 最大75% | — |

### 実行時間の目安 / Estimated Execution Times

| シナリオ規模 / Scenario size | ステップ数 / Steps | 目安時間 / Est. time |
|-----------------------------|-------------------|---------------------|
| 小（UC 3–5個）/ Small | Full (1–10) | 5–15 分 / min |
| 中（UC 6–15個）/ Medium | Full (1–10) | 15–40 分 / min |
| 大（UC 16個以上）/ Large | Full (1–10) | 40–90 分 / min |
| 機能追加 / Add feature | Resume from 2 | 3–10 分 / min |
| バリデーションのみ / Validation | Step 6 only | 1–3 分 / min |

---

*このアーキテクチャドキュメントに関する質問・提案は [GitHub Issues](../../issues) でどうぞ。*  
*For questions or suggestions about this architecture document, use [GitHub Issues](../../issues).*
