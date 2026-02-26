# Release v3.0.0 — UML Workflow v3 / UMLワークフロー v3

ビジネスシナリオから本番品質のアプリケーションを自動生成する Claude AI スキル  


---

## Highlights / ハイライト

### 10-Step Pipeline / 10ステップパイプライン

シナリオ → アクティビティ図 → ユースケース → クラス図 → ステートマシン → シーケンス → バリデーション → セキュリティ設計 → コード生成 → テスト → トレーサビリティマトリクス / Scenario → Activity Diagram → Use Cases → Class Diagram → State Machine → Sequence → Validation → Security Design → Code Generation → Tests → Traceability Matrix

### Claude.ai Skills 対応 / Claude.ai Skills Support

Settings > Capabilities > Upload skill で簡単インストール。ZIP を5つアップロードするだけで利用開始できます。  


### Token 効率の大幅改善 / Significant Token Efficiency Improvement

- `available_skills` カタログ：16 → 5 スキル（69% 削減）/ `available_skills` catalog: 16 → 5 skills (69% reduction)
- トークンコスト：1,700 → 600 tokens（65% 削減）/ Token cost: 1,700 → 600 tokens (65% reduction)
- キャッシュ活用時：最大 75% のトークン削減 / With cache: up to 75% token reduction

---

## Download & Install / ダウンロード・インストール

### Step 1: ダウンロード / Download

下の **Assets** セクションから `uml-workflow-v3-all-skills.zip` をダウンロードしてください。  


### Step 2: 解凍 / Extract

ZIP を解凍すると5つの ZIP ファイルが出現します：  


| ファイル / File | 役割 / Role |
|----------------|------------|
| `uml-workflow-v3.zip` (150KB) | メインオーケストレーター（必須）/ Main orchestrator (required) |
| `usecase-md-to-json.zip` (13KB) | UC仕様 Markdown→JSON 変換 / UC spec Markdown→JSON converter |
| `classdiagram-image-to-json.zip` (19KB) | 手描きクラス図取込 / Hand-drawn class diagram importer |
| `json-to-models.zip` (14KB) | JSON→PlantUML/XMI 再生成 / JSON→PlantUML/XMI regenerator |
| `classdiagram-to-crud.zip` (9KB) | クラス図→CRUD HTML 生成 / Class diagram→CRUD HTML generator |

### Step 3: アップロード / Upload

1. [claude.ai](https://claude.ai) → **Settings** → **Capabilities** → **Skills**（共通 / same for all）
2. 「Upload skill」で各 ZIP を1つずつアップロード / Click "Upload skill" and upload each ZIP one by one
3. 各スキルのトグルを **ON** にする / Toggle each skill **ON**

### Step 4: 動作確認 / Verify

新しい会話を開き、以下のように入力してください：/ Open a new conversation and type:

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

詳細は [docs/INSTALLATION_GUIDE.md](docs/INSTALLATION_GUIDE.md) | [English guide](docs/INSTALLATION_GUIDE_EN.md)

---

## Requirements / 動作要件

- Claude.ai **Pro** / **Max** / **Team** / **Enterprise** プラン / plan
- 「Code execution and file creation」が有効 / enabled

---

## What's Changed since v2 / v2 からの変更点

- Step 10（トレーサビリティマトリクス）を追加 / Added Step 10 (Traceability Matrix)
- 10 個のパイプラインスキルを `references/` に統合 / Bundled all 10 pipeline skills into `references/`
- description を 200 文字以内に最適化（Claude.ai 制約対応）/ Optimized descriptions to ≤200 chars (Claude.ai constraint)
- インストール対象を 15 ZIP → 5 ZIP に削減 / Reduced install package count from 15 ZIPs to 5
- バイリンガルインストールガイドを追加 / Added bilingual installation guide

---

## Assets / 配布物

- `uml-workflow-v3-all-skills.zip` — 5 つのスキル ZIP を同梱（推奨ダウンロード）/ Bundles all 5 skill ZIPs (recommended download)
- `uml-workflow-v3.tar.gz` — 開発者向け（install.sh 付き）/ For developers (includes install.sh)
