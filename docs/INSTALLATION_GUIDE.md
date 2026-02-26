# UML Workflow v3 — インストールガイド / Installation Guide

このガイドは日本語を主体に記述しています。English guide: [INSTALLATION_GUIDE_EN.md](INSTALLATION_GUIDE_EN.md)

---

## 前提条件 / Prerequisites

| 項目 / Item | 要件 / Requirement |
|------------|------------------|
| プラットフォーム / Platform | Claude.ai（Web / Desktop / Mobile） |
| プラン / Plan | **Pro** / **Max** / **Team** / **Enterprise** |
| 必要な機能 / Required feature | 「コード実行とファイル作成 / Code execution and file creation」が **ON** |

> **Pro プランについて / About Pro plan**: メッセージ制限により、大規模シナリオでは全10ステップを完走できない場合があります。大規模プロジェクトには **Max** プランを推奨します。  
> Pro plan message limits may prevent completing all 10 steps for large scenarios. **Max** plan is recommended for large projects.

---

## インストール手順 / Installation Steps

### Step 1: ZIPファイルのダウンロード / Download ZIP Files

GitHub リポジトリの [Releases](../../releases) ページから以下の5つのZIPファイルをダウンロードしてください。

Download the following 5 ZIP files from the [Releases](../../releases) page.

| # | ファイル名 / File Name | サイズ / Size | 役割 / Role |
|---|----------------------|-------------|------------|
| 1 | `uml-workflow-v3.zip` | 154KB | メイン（10個のパイプラインスキル内蔵）/ Main (10 pipeline skills built-in) |
| 2 | `usecase-md-to-json.zip` | 11KB | UC仕様Markdown→JSON変換 / UC spec Markdown→JSON |
| 3 | `classdiagram-image-to-json.zip` | 15KB | クラス図画像→JSON取込 / Class diagram image→JSON |
| 4 | `json-to-models.zip` | 12KB | JSON→PlantUML/XMI再生成 / JSON→PlantUML/XMI |
| 5 | `classdiagram-to-crud.zip` | 6KB | クラス図→CRUD画面生成 / Class diagram→CRUD HTML |

> **注意 / Note**: 最低限 `uml-workflow-v3.zip` のみでワークフローは動作します。残りの4つはモデル修正時の補助ツールです。  
> The workflow runs with just `uml-workflow-v3.zip`. The other 4 are helper tools for manual model editing.

---

### Step 2: Claude.ai の設定画面を開く / Open Claude.ai Settings

1. [claude.ai](https://claude.ai) にログイン / Log in
2. 画面左下の **「Settings（設定）」** をクリック / Click **Settings** (bottom-left)
3. **「Capabilities（機能）」** タブを開く / Open the **Capabilities** tab
4. **「コード実行とファイル作成 / Code execution and file creation」** が **ON** になっていることを確認  
   Confirm **"Code execution and file creation"** is **ON**

---

### Step 3: スキルをアップロード / Upload Skills

1. 「Capabilities」画面の **Skills** セクションまでスクロール / Scroll to the **Skills** section
2. **「Upload skill（スキルをアップロード）」** ボタンをクリック / Click **"Upload skill"**
3. `uml-workflow-v3.zip` を選択してアップロード / Select and upload `uml-workflow-v3.zip`
4. アップロード成功後、スキル一覧に `uml-workflow-v3` が表示される / After upload, `uml-workflow-v3` appears in the list
5. トグルスイッチを **ON** にする / Toggle the switch **ON**

6. 同じ手順を残りの4つのZIPで繰り返す / Repeat for the remaining 4 ZIPs:
   - `usecase-md-to-json.zip`
   - `classdiagram-image-to-json.zip`
   - `json-to-models.zip`
   - `classdiagram-to-crud.zip`

> **重要 / Important**: アップロード後にトグルを **ON** にするのを忘れないでください。ONにしないと Claude がスキルを認識しません。  
> Don't forget to toggle each skill **ON** after uploading. Claude won't recognize the skill if toggled off.

---

### Step 4: 動作確認 / Verify Installation

**新しい会話** を開き、以下のように入力してください：

Open a **new conversation** and type:

**日本語 / Japanese:**
```
uml-workflow-v3を使って、以下のビジネスシナリオからアプリケーションを生成してください。

シナリオ：
従業員が経費申請を提出し、上長が承認・却下する。
経理部門が承認済み申請を精算処理する。
```

**English:**
```
Use uml-workflow-v3 to generate an application from the following business scenario.

Scenario:
Employees submit expense reports. Managers approve or reject them.
The accounting department processes approved expense reports for reimbursement.
```

Claude が自動的にスキルを認識し、10ステップのワークフローを開始すれば成功です。

If Claude recognizes the skill and starts the 10-step workflow, the installation was successful.

---

## パイプラインの10ステップ / 10-Step Pipeline

| Step | 機能 / Function | 出力 / Output |
|------|----------------|-------------|
| 1 | シナリオ→アクティビティ図 / Scenario→Activity | activity-data.json, .puml |
| 2 | アクティビティ図→ユースケース / Activity→Use Cases | usecase-output.json, .puml, UC-*.md |
| 3 | ユースケース→クラス図 / Use Cases→Class Diagram | domain-model.json ⭐, .puml |
| 4 | 状態遷移図生成 / State Machine | statemachine.puml |
| 5 | シーケンス図生成 / Sequence Diagram | sequence.puml |
| 6 | モデル横断検証 / Cross-Model Validation | validation-report.md |
| 7 | セキュリティ設計 / Security Design | security-config.json |
| 8 | コード生成 / Code Generation | {project-name}/ |
| 9 | テスト生成 / Test Generation | tests/ |
| 10 | トレーサビリティマトリクス / Traceability Matrix | traceability-matrix.json, .md |

> ⭐ `domain-model.json` はすべての後続ステップが参照する Single Source of Truth です。  
> ⭐ `domain-model.json` is the Single Source of Truth referenced by all subsequent steps.

---

## 基本的な使い方 / Basic Usage

### フルワークフロー実行 / Full Workflow

```
uml-workflow-v3を使って、以下のビジネスシナリオからアプリケーションを生成してください。
[シナリオをここに記述]
```

### 特定ステップだけ実行 / Single Step

```
uml-workflowのStep 6（モデル検証）を実行してください
Run Step 6 (model validation) of uml-workflow
```

### 途中から再開 / Resume from Step

```
uml-workflowをStep 5から再開してください
Resume uml-workflow from Step 5
```

### ヘルパースキルの使用例 / Helper Skill Examples

```
ユースケース仕様のMarkdownを修正したので、JSONに反映してください
I've edited the use case Markdown specs. Please update the JSON.

この手描きのクラス図を取り込んでください [画像を添付 / attach image]
Import this hand-drawn class diagram [attach image]
```

---

## アップデート方法 / Updating

スキルを更新する場合は、新しいZIPファイルを同じ手順でアップロードしてください。同じ名前のスキルがあれば自動的に上書きされます。

To update a skill, upload the new ZIP using the same process. Skills with the same name are automatically overwritten.

---

## トラブルシューティング / Troubleshooting

### スキルが認識されない / Skill Not Recognized

- Settings > Capabilities でスキルのトグルが **ON** になっているか確認 / Check toggle is **ON**
- 「コード実行とファイル作成」が有効になっているか確認 / Confirm code execution is enabled
- スキルアップロード **後** に開いた **新しい会話** で試す / Try a **new conversation** opened **after** upload

### アップロードエラー / Upload Error

- ZIPの中に直接 `SKILL.md` が入っていないか確認。正しい構造: `skill-name/SKILL.md`（フォルダの中にSKILL.md）  
  Ensure ZIP contains a folder with `SKILL.md` inside, not `SKILL.md` at root: correct format is `skill-name/SKILL.md`
- `description` フィールドが200文字以下か確認 / Ensure `description` is ≤ 200 characters

### 途中から再開できない / Cannot Resume from Middle Step

- 前回のセッションで生成されたファイルはセッション間で引き継がれません  
  Files from previous sessions are not carried over between sessions
- ファイルをアップロードし直すか、Step 1からやり直してください  
  Re-upload the intermediate files or restart from Step 1

---

## 推奨プラン / Recommended Plans

| プラン / Plan | ワークフロー実行 / Workflow | 備考 / Notes |
|--------------|--------------------------|-------------|
| Free | ❌ | コード実行非対応 / Code execution unavailable |
| Pro | ⚠️ 限定的 / Limited | 小規模シナリオ向き / For small scenarios |
| **Max** | ✅ **推奨 / Recommended** | 大規模でも全10ステップ完走可能 |
| Team / Enterprise | ✅ | 組織利用に最適 / Ideal for org-wide use |

---

*詳細なユーザーガイドは [USER_GUIDE.md](USER_GUIDE.md) を参照してください。*  
*For a detailed user guide, see [USER_GUIDE.md](USER_GUIDE.md).*
