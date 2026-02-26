# UML Workflow v3

**ビジネスシナリオから本番品質アプリケーションを自動生成する Claude AI スキル**

*A Claude AI Skill that transforms business scenarios into production-ready applications through a 10-step UML pipeline.*

---

## 🎯 これは何？ / What is this?

**uml-workflow-v3** は、自然言語で書かれたビジネスシナリオを入力として、UML設計からフルスタックコード・テスト・トレーサビリティマトリクスまでを自動生成する Claude AI スキルです。

**uml-workflow-v3** is a Claude AI skill that takes a natural-language business scenario and automatically generates UML diagrams, full-stack application code, test suites, and a complete traceability matrix — all in a single 10-step pipeline.

### パイプライン全体像 / Full Pipeline Overview

```
ビジネスシナリオ（自然言語） / Business Scenario (Natural Language)
    ↓
┌─────────────────────────────────────────────────────────────┐
│  Step  1: シナリオ → アクティビティ図 / → Activity Diagram   │
│  Step  2: アクティビティ図 → ユースケース / → Use Cases      │
│  Step  3: ユースケース → クラス図 / → Class Diagram          │
│  Step  4: クラス図 → ステートマシン / → State Machine        │
│  Step  5: ユースケース → シーケンス図 / → Sequence Diagram   │
│  Step  6: モデル横断バリデーション / Cross-Model Validation  │
│  Step  7: OWASP準拠セキュリティ設計 / Security Design        │
│  Step  8: フルスタックコード生成 / Code Generation           │
│  Step  9: テストコード生成 / Test Generation                 │
│  Step 10: トレーサビリティマトリクス / Traceability Matrix    │
└─────────────────────────────────────────────────────────────┘
    ↓
本番品質アプリ + 完全なUMLドキュメント + 追跡可能なエビデンス
Production-Quality App + Full UML Docs + Traceable Evidence
```

---

## ✨ 主な特長 / Key Features

| 特長 / Feature | 詳細 / Details |
|---------------|---------------|
| **10ステップパイプライン** | シナリオ→コード→テスト→追跡マトリクスまで一貫自動実行 |
| **10-Step Pipeline** | Seamlessly automated from scenario to code, tests, and traceability |
| **バイリンガル対応** | 日本語・英語の両出力に対応。コメント・ドキュメントも選択可能 |
| **Bilingual Output** | Japanese and English outputs. Comments and docs in your language |
| **キャッシュシステム** | 中間成果物を自動保存。再実行時のトークン消費を最大75%削減 |
| **Caching System** | Auto-saves intermediate artifacts. Up to 75% token reduction on reruns |
| **柔軟な実行モード** | フル実行・途中再開・単一ステップ・モデルのみなど複数モード |
| **Flexible Execution** | Full run, resume from step, single-step, model-only — your choice |
| **セキュリティファースト** | OWASP Top 10準拠のセキュリティ設計を Step 7 で自動生成 |
| **Security-First** | OWASP Top 10–compliant security design auto-generated at Step 7 |
| **完全なトレーサビリティ** | 要件→モデル→コード→テストを Step 10 で双方向追跡 |
| **Full Traceability** | Requirements ↔ Model ↔ Code ↔ Tests bidirectionally tracked at Step 10 |

---

## 🚀 基本的な使い方 / Basic Usage

### 初回実行 / First Run

Claude の新しい会話を開き、以下のように入力してください：

Open a new Claude conversation and type:

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

Claude が対話的に質問しながら、10ステップを自動実行します。

Claude will ask a few configuration questions, then automatically execute all 10 steps.

### 対話の例 / Sample Dialogue

```
あなた / You: 「uml-workflow-v3で受注管理システムを生成して」

Claude: [対話形式で質問 / interactive questions]
  1. プロジェクト名 / Project name → order-management
  2. キャッシュ使用 / Use cache    → はい / Yes
  3. 実行モード / Execution mode   → フルワークフロー / Full workflow
  4. XMI生成 / XMI output         → いいえ（推奨）/ No (recommended)
  5. 言語 / Language              → 日本語 / Japanese
  6. テスト生成 / Generate tests   → はい / Yes

Claude: [自動実行 / auto-executing]
  ✅ Step  1: アクティビティ図生成 complete
  ✅ Step  2: ユースケース抽出 complete
  ✅ Step  3: クラス図生成 complete
  ✅ Step  4: ステートマシン図生成 complete
  ✅ Step  5: シーケンス図生成 complete
  ✅ Step  6: バリデーション complete
  ✅ Step  7: セキュリティ設計 complete
  ✅ Step  8: コード生成 complete
  ✅ Step  9: テスト生成 complete
  ✅ Step 10: トレーサビリティマトリクス complete
  🎉 完成！ / Done!
```

### 2回目以降（キャッシュ活用）/ Subsequent Runs (Cache Reuse)

```
あなた / You: 「order-managementに在庫管理機能を追加」

Claude: [キャッシュ検出 / Cache detected]
  💾 Step 1: キャッシュから復元 / Restored from cache
  ⚙️ Step 2-10: 再実行 / Re-executing
  Token削減 / Token reduction: 約 20-30%
```

---

## 📊 トークン削減効果 / Token Efficiency

### シナリオ別削減率 / Reduction by Scenario

| シナリオ / Scenario | 実行内容 / Steps | 削減率 / Reduction |
|--------------------|-----------------|-------------------|
| 初回実行 / First run | 全ステップ / All | 0%（基準 / baseline）|
| 機能追加 / Add feature | Step 2から再開 / Resume from 2 | 20–30% |
| モデル調整 / Model tweak | Step 3から再開 / Resume from 3 | 30–40% |
| モデルのみ / Model only | Step 1–7 のみ | 30–35% |
| バリデーションのみ / Validation only | Step 6 のみ | ~95% |
| 最適組合せ / Optimal combo | Step 3から + モデルのみ | **~75%** |

### XMI生成OFF の追加効果 / Additional Gain from XMI=OFF

全シナリオでXMI生成をOFFにすることで **さらに最大18%削減** できます。

Disabling XMI generation provides an **additional up to 18% reduction** across all scenarios.

```
例 / Example: モデルのみ + XMI OFF / Model only + XMI OFF
  基本削減 / Base reduction:   33%
  XMI無効化 / XMI disabled:   18%
  合計 / Total:             ~50% 削減 / reduction
```

---

## 🎮 実行モード / Execution Modes

### 1. フルワークフロー / Full Workflow（デフォルト / Default）

全10ステップを実行。初回のプロジェクト生成に使用します。

Executes all 10 steps. Use this for initial project generation.

```
「uml-workflow-v3で{プロジェクト名}を生成して」
"Generate {project-name} with uml-workflow-v3"
```

実行されるステップ / Steps executed:

```
Step  1: シナリオ → アクティビティ図 / Scenario → Activity Diagram
Step  2: アクティビティ図 → ユースケース / Activity → Use Cases
Step  3: ユースケース → クラス図 / Use Cases → Class Diagram
Step  4: クラス図 → ステートマシン図 / Class → State Machine
Step  5: ユースケース → シーケンス図 / Use Cases → Sequence Diagrams
Step  6: モデル横断バリデーション / Cross-Model Validation
Step  7: OWASP準拠セキュリティ設計 / OWASP-Compliant Security Design
Step  8: フルスタックコード生成 / Full-Stack Code Generation
Step  9: テストコード生成（ユニット + E2E）/ Test Generation (Unit + E2E)
Step 10: トレーサビリティマトリクス生成 / Traceability Matrix Generation
```

### 2. 指定ステップから再開 / Resume from Step

任意のステップから実行を開始します。それ以前のステップはキャッシュから復元されます。

Starts execution from any step. Prior steps are restored from cache.

```
「uml-workflowをStep 5から再開してください」
"Resume uml-workflow from Step 5"
```

いつ使うか / When to use: 前段のモデルは変更せず、後段のみ再生成したい場合。機能追加など。

Use this when you want to regenerate only later steps without changing earlier models — e.g., when adding features.

### 3. モデルのみ / Model Only

コード生成（Step 8–9）をスキップし、Step 1–7 のみを実行します。

Executes Steps 1–7, skipping code generation (Steps 8–9).

```
「{プロジェクト名}のモデルのみ生成して」
"Generate models only for {project-name}"
```

いつ使うか / When to use: 要件定義・設計フェーズ。ステークホルダーレビュー用のUML図のみ欲しい場合。

Use during requirements or design phase, or when only UML diagrams are needed for stakeholder review.

### 4. 単一ステップ / Single Step

特定のステップのみを実行します。

Executes one specific step in isolation.

```
「uml-workflowのStep 6（モデル検証）を実行してください」
"Run Step 6 (model validation) of uml-workflow"
```

いつ使うか / When to use: モデル手動修正後のバリデーション。特定のUML図の再生成。

Use after manually editing a model, or to regenerate a specific UML diagram.

### 5. バリデーションのみ / Validation Only

```
「{プロジェクト名}のバリデーションを実行して」
"Run validation for {project-name}"
```

Step 6 のみを実行します。トークン削減率は最大約95%。

Runs Step 6 only. Up to ~95% token reduction.

---

## 💾 キャッシュの仕組み / How Caching Works

### 自動キャッシュ / Automatic Caching

各ステップ完了後、Claude が自動的に成果物をキャッシュに保存します。

After each step completes, Claude automatically saves artifacts to the cache.

```
キャッシュ保存先 / Cache location:
  /mnt/user-data/outputs/workflow-cache/{project-name}/

保存されるファイル例 / Example cached files:
  scenario_to_activity_activity-data.json
  scenario_to_activity_activity.puml
  activity_to_usecase_usecase-output.json
  activity_to_usecase_usecase-diagram.puml
  usecase_to_class_domain-model.json
  usecase_to_class_class.puml
  class_to_statemachine_statemachine.puml
  usecase_to_sequence_sequence.puml
  model_validator_validation-report.md
```

### キャッシュの確認・クリア / Check & Clear Cache

```
「{プロジェクト名}のキャッシュ状況を確認して」
"Check cache status for {project-name}"

「{プロジェクト名}のキャッシュをクリアして」
"Clear cache for {project-name}"
```

### キャッシュの利用条件 / When Cache is Used

キャッシュは次の条件を満たすときに利用されます：

Cache is used when all of the following apply:

1. 同じプロジェクト名のキャッシュが存在する / A cache entry exists for the same project name
2. キャッシュファイルが壊れていない / Cache files are intact
3. 実行開始時に「キャッシュを使用する」を選択した / User selected "Use cache" at startup

---

## ⚡ XMI生成の最適化 / XMI Generation Optimization

### デフォルト: OFF / Default: OFF

XMI生成はすべての実行モードでデフォルト OFF です。効果: 各モデル生成ステップで **最大40%高速化**。

XMI generation is OFF by default in all modes. Effect: **up to 40% faster** per model step.

### XMIが必要なケース / When You Need XMI

| ユースケース / Use Case | 説明 / Description |
|------------------------|-------------------|
| UMLツールへのインポート | Enterprise Architect / Papyrus / MagicDraw |
| ラウンドトリップ | UMLツールで編集後、再インポートする場合 |
| 組織標準要件 | XMI形式が必須要件の場合 |
| Import to UML tool | Enterprise Architect / Papyrus / MagicDraw |
| Round-trip engineering | Re-importing after editing in a UML tool |
| Org standard | When XMI is a mandatory requirement |

---

## 📁 出力ファイル / Output Files

```
/mnt/user-data/outputs/
│
├── {project-name}_activity-data.json     ← Step 1
├── {project-name}_activity.puml          ← Step 1
│
├── {project-name}_usecase-output.json    ← Step 2
├── {project-name}_usecase-diagram.puml   ← Step 2
├── usecase-specifications/               ← Step 2 (Cockburn format)
│   ├── UC-001_*.md
│   └── UC-002_*.md
│
├── {project-name}_domain-model.json  ⭐  ← Step 3 (Single Source of Truth)
├── {project-name}_class.puml             ← Step 3
│
├── {project-name}_statemachine.puml      ← Step 4
├── {project-name}_sequence.puml          ← Step 5
│
├── {project-name}_validation-report.md   ← Step 6
├── {project-name}_security-config.json   ← Step 7
│
├── {project-name}/                        ← Step 8 (Generated application)
│   ├── backend/
│   ├── frontend/
│   ├── docker-compose.yml
│   └── README.md
│
├── tests/                                 ← Step 9
│   ├── unit/
│   └── e2e/
│
└── {project-name}_traceability-matrix.json  ← Step 10
    {project-name}_traceability-matrix.md    ← Step 10
```

> ⭐ `domain-model.json` はすべてのステップが参照する Single Source of Truth です。  
> ⭐ `domain-model.json` is the Single Source of Truth referenced by all subsequent steps.

---

## 🛠️ ヘルパースキル / Helper Skills

メインワークフローに加え、モデルの手動修正を支援するヘルパースキルが4つあります。

Four helper skills support manual model editing alongside the main workflow.

| スキル / Skill | 用途 / Purpose | 使用タイミング / When to Use |
|---------------|---------------|---------------------------|
| `usecase-md-to-json` | UC仕様 Markdown → JSON | UC仕様を直接編集したとき / After editing UC specs |
| `classdiagram-image-to-json` | 手描きクラス図 → JSON | 紙や画像のクラス図取込 / Importing image/paper diagrams |
| `json-to-models` | JSON → PlantUML / XMI | domain-model.json 修正後 / After modifying domain-model.json |
| `classdiagram-to-crud` | クラス図 → CRUD HTML | CRUD画面プロトタイプ生成 / CRUD screen prototyping |

### 使用例 / Usage Examples

```
「この手描きのクラス図を取り込んでください」（画像を添付）
"Import this hand-drawn class diagram" (attach image)

「ユースケース仕様のMarkdownを修正したので、JSONに反映して」
"I've edited the use case Markdown specs. Please update the JSON."

「domain-model.jsonを更新したので、クラス図を再生成して」
"I've updated domain-model.json. Please regenerate the class diagram."
```

---

## ⚠️ 注意事項 / Notes

### ステップ間の依存関係 / Step Dependencies

```
Step  2 → Step 1 の成果物が必要 / Requires Step 1 artifacts
Step  3 → Step 2 の成果物が必要 / Requires Step 2 artifacts
Step  4 → Step 3 の domain-model.json が必要
Step  5 → Step 2, 3 の成果物が必要
Step  6 → Step 1–5 の成果物を参照
Step  7 → Step 3, 6 の成果物が必要
Step  8 → Step 3, 7 の成果物が必要
Step  9 → Step 2, 3, 8 の成果物が必要
Step 10 → Step 1–9 全ての成果物を参照
```

途中のステップから開始する場合、必要な成果物がキャッシュにあることを確認してください。

When resuming from a middle step, ensure all required prior artifacts exist in cache.

### 推奨プラン / Recommended Plans

| プラン / Plan | サポート / Support | 備考 / Notes |
|--------------|------------------|-------------|
| Free | ❌ | コード実行非対応 / No code execution |
| Pro | ⚠️ | 小規模シナリオ向き / For small scenarios |
| **Max** | ✅ **推奨 / Recommended** | 大規模でも全10ステップ完走可能 / Completes all 10 steps even for large scenarios |
| Team / Enterprise | ✅ | 組織利用に最適 / Ideal for org-wide use |

---

## 🆚 バージョン比較 / Version Comparison

| 機能 / Feature | v1 | v2 Enhanced | **v3** |
|---------------|----|-------------|--------|
| パイプラインステップ / Pipeline steps | 4 | 9 | **10** |
| トレーサビリティ / Traceability | ❌ | ❌ | **✅ Step 10** |
| キャッシュシステム / Caching | ❌ | ✅ | ✅ |
| セキュリティ設計 / Security design | ❌ | ✅ | ✅ |
| references方式 / References | ❌ | ❌ | **✅ (69%削減 / reduction)** |
| Claude.ai Skills 正式対応 | ❌ | ❌ | **✅** |
| インストール用ZIP / Install ZIPs | 15 | 15 | **5** |
| Token効率 / Token efficiency | baseline | max 75% | max 75% |

---

## 🔧 トラブルシューティング / Troubleshooting

**Q: スキルが認識されない / Skill not recognized**

Settings > Capabilities でスキルのトグルが ON か確認してください。スキルをアップロードした後に開いた新しい会話を使ってください。

Check the toggle is ON in Settings > Capabilities. Use a new conversation opened after uploading the skill.

---

**Q: キャッシュが見つからない / Cache not found**

プロジェクト名が前回と同じか確認してください。過去に同じプロジェクト名で実行したことが必要です。

Verify the project name matches the previous session. The cache requires a prior run with the same project name.

---

**Q: Token削減効果が想定より低い / Token reduction lower than expected**

XMI生成がOFFになっているか確認してください。また、フルワークフローではなく「途中から再開」や「モデルのみ」を活用してください。

Confirm XMI generation is OFF. Also, use "Resume from step" or "Model only" instead of the full workflow when possible.

---

**Q: バリデーションエラーが出る / Validation errors**

Step 6 のエラーはモデルの不整合を示します。ヘルパースキルでモデルを修正してから Step 3 以降を再実行してください。

Step 6 errors indicate model inconsistencies. Edit the model using helper skills, then resume from Step 3.

---

## 📚 関連ドキュメント / Related Documentation

| ドキュメント / Document | 内容 / Content |
|------------------------|---------------|
| [SKILL.md](SKILL.md) | Claude 向け実行仕様 / Execution spec for Claude |
| [INSTALL.md](INSTALL.md) | インストール手順 / Install steps |
| [../../docs/USER_GUIDE.md](../../docs/USER_GUIDE.md) | 詳細ユーザーガイド / Comprehensive user guide |
| [../../docs/ARCHITECTURE.md](../../docs/ARCHITECTURE.md) | アーキテクチャ説明 / Architecture overview |
| [../../docs/INSTALLATION_GUIDE.md](../../docs/INSTALLATION_GUIDE.md) | インストールガイド（日本語）|
| [../../docs/INSTALLATION_GUIDE_EN.md](../../docs/INSTALLATION_GUIDE_EN.md) | Installation Guide (English) |
| [../../examples/expense-report.md](../../examples/expense-report.md) | サンプルシナリオ / Sample scenario |
| [../../CHANGELOG.md](../../CHANGELOG.md) | 変更履歴 / Change log |

---

**Happy modeling! 🚀 モデリングを楽しんでください！**
