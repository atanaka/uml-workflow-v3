# Release v3.0.0 — UML Workflow v3

ビジネスシナリオから本番品質のアプリケーションを自動生成する Claude AI スキル

## Highlights

### 10-Step Pipeline
シナリオ → アクティビティ図 → ユースケース → クラス図 → ステートマシン → シーケンス → バリデーション → セキュリティ設計 → コード生成 → テスト → トレーサビリティマトリクス

### Claude.ai Skills 対応
Settings > Capabilities > Upload skill で簡単インストール。ZIP を5つアップロードするだけで利用開始できます。

### Token 効率の大幅改善
- available_skills カタログ: 16→5 スキル（69%削減）
- トークンコスト: 1,700→600 tokens（65%削減）
- キャッシュ活用時: 最大75%のトークン削減

## Download & Install

### Step 1: ダウンロード
下の **Assets** セクションから `uml-workflow-v3-all-skills.zip` をダウンロード

### Step 2: 解凍
ZIP を解凍すると5つの ZIP ファイルが出現します：

| File | Role |
|------|------|
| `uml-workflow-v3.zip` (154KB) | メインオーケストレーター（必須） |
| `usecase-md-to-json.zip` (11KB) | UC仕様 Markdown→JSON 変換 |
| `classdiagram-image-to-json.zip` (15KB) | 手描きクラス図取込 |
| `json-to-models.zip` (12KB) | JSON→PlantUML/XMI 再生成 |
| `classdiagram-to-crud.zip` (6KB) | クラス図→CRUD HTML 生成 |

### Step 3: アップロード
1. [claude.ai](https://claude.ai) → Settings → Capabilities → Skills
2. 「Upload skill」で各 ZIP を1つずつアップロード
3. 各スキルのトグルを **ON** にする

### Step 4: 動作確認
新しい会話で：
```
uml-workflow-v3を使って、以下のビジネスシナリオからアプリケーションを生成してください。

シナリオ：
従業員が経費申請を提出し、上長が承認・却下する。
経理部門が承認済み申請を精算処理する。
```

詳細は [INSTALLATION_GUIDE.md](docs/INSTALLATION_GUIDE.md) を参照。

## Requirements

- Claude.ai **Pro** / **Max** / **Team** / **Enterprise** プラン
- 「Code execution and file creation」が有効

## What's Changed since v2

- Step 10（トレーサビリティマトリクス）を追加
- 10個のパイプラインスキルを `references/` に統合
- description を200文字以内に最適化（Claude.ai 制約対応）
- インストール対象を15 ZIP → 5 ZIP に削減
- バイリンガルインストールガイドを追加

## Assets

- `uml-workflow-v3-all-skills.zip` — 5つのスキル ZIP を同梱（推奨ダウンロード）
- `uml-workflow-v3.tar.gz` — 開発者向け（install.sh 付き）
