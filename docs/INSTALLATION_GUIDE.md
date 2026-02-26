# UML Workflow v3 — インストールガイド

## 前提条件

- Claude.ai の **Pro** / **Max** / **Team** / **Enterprise** プラン
- 「コード実行とファイル作成」が有効であること

## インストール手順

### Step 1: ZIPファイルのダウンロード

GitHubリポジトリから以下の5つのZIPファイルをダウンロードしてください。

| # | ファイル名 | サイズ | 役割 |
|---|-----------|--------|------|
| 1 | `uml-workflow-v3.zip` | 154KB | メイン（パイプライン10スキル内蔵） |
| 2 | `usecase-md-to-json.zip` | 11KB | UC仕様Markdown→JSON変換 |
| 3 | `classdiagram-image-to-json.zip` | 15KB | クラス図画像→JSON取込 |
| 4 | `json-to-models.zip` | 12KB | JSON→PlantUML/XMI再生成 |
| 5 | `classdiagram-to-crud.zip` | 6KB | クラス図→CRUD画面生成 |

> **注意**: 5つすべてをインストールすることを推奨しますが、最低限 `uml-workflow-v3.zip` のみでワークフローは動作します。残りの4つはモデル修正時の補助ツールです。

### Step 2: Claude.aiの設定画面を開く

1. [claude.ai](https://claude.ai) にログイン
2. 画面左下の **Settings（設定）** をクリック
3. **「Capabilities（機能）」** タブを開く
4. **「Code execution and file creation（コード実行とファイル作成）」** が **ON** になっていることを確認

### Step 3: スキルをアップロード

1. 同じ「Capabilities」画面の **Skills** セクションまでスクロール
2. **「Upload skill（スキルをアップロード）」** ボタンをクリック
3. ダウンロードした **`uml-workflow-v3.zip`** を選択してアップロード
4. アップロード成功後、スキル一覧に `uml-workflow-v3` が表示される
5. トグルスイッチを **ON** にする

6. 同じ手順を残りの4つのZIPで繰り返す：
   - `usecase-md-to-json.zip`
   - `classdiagram-image-to-json.zip`
   - `json-to-models.zip`
   - `classdiagram-to-crud.zip`

> **ヒント**: アップロード後にトグルを **ON** にするのを忘れないでください。ONにしないとClaudeがスキルを認識しません。

### Step 4: 動作確認

新しい会話を開き、以下のように話しかけてください：

```
uml-workflow-v3を使って、以下のビジネスシナリオからアプリケーションを生成してください。

シナリオ：
従業員が経費申請を提出し、上長が承認・却下する。
経理部門が承認済み申請を精算処理する。
```

Claudeが自動的にスキルを認識し、10ステップのワークフローを開始すれば成功です。

## 使い方の基本

### フルワークフロー実行

```
uml-workflow-v3を使って、以下のビジネスシナリオから
アプリケーションを生成してください。
[シナリオをここに記述]
```

### 特定ステップだけ実行

```
uml-workflowのStep 6（モデル検証）を実行してください
```

### 途中から再開

```
uml-workflowをStep 5から再開してください
```

### モデル修正（edit-helper使用例）

```
ユースケース仕様のMarkdownを修正したので、JSONに反映してください
```

```
この手描きのクラス図を取り込んでください [画像を添付]
```

## パイプラインの10ステップ

| Step | 機能 | 出力 |
|------|------|------|
| 1 | シナリオ→アクティビティ図 | activity-data.json, .puml |
| 2 | アクティビティ図→ユースケース | usecase-output.json, .puml |
| 3 | ユースケース→クラス図 | domain-model.json, .puml |
| 4 | 状態遷移図生成 | statemachine.puml |
| 5 | シーケンス図生成 | sequence.puml |
| 6 | モデル横断検証 | validation-report.md |
| 7 | セキュリティ設計 | security-config.json |
| 8 | コード生成 | src/ ディレクトリ |
| 9 | テスト生成 | tests/ ディレクトリ |
| 10 | トレーサビリティマトリクス | traceability-matrix.json/.md |

## アップデート方法

スキルを更新する場合は、新しいZIPファイルを同じ手順でアップロードしてください。同じ名前のスキルがあれば自動的に上書きされます。

## トラブルシューティング

### スキルが認識されない
- Settings > Capabilities でスキルのトグルが **ON** であることを確認
- 「コード実行とファイル作成」が有効であることを確認
- 新しい会話を開いてから試してください（アップロード前の会話では認識されません）

### アップロードエラー
- ZIPの中に直接 `SKILL.md` が入っていないか確認。正しい構造は `skill-name/SKILL.md`（フォルダの中にSKILL.md）
- description が200文字以下であることを確認

### 途中から再開できない
- 前回のセッションで生成されたファイルは引き継がれません
- ファイルをアップロードし直すか、Step 1からやり直してください

## 推奨プラン

| プラン | ワークフロー実行 | 備考 |
|--------|-----------------|------|
| Free | ❌ | コード実行非対応 |
| Pro | ⚠️ | メッセージ制限あり。小規模シナリオ向き |
| Max | ✅ | 推奨。大規模シナリオでもステップ10まで完走可能 |
| Team / Enterprise | ✅ | 組織での利用に最適 |
