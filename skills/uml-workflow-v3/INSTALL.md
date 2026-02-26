# UML Workflow v3 インストールガイド

## クイックインストール（推奨）/ Quick Install (Recommended)

```bash
# 1. アーカイブを展開
mkdir -p /tmp/uml-workflow && tar xzf uml-workflow-v3.tar.gz -C /tmp/uml-workflow

# 2. インストール実行
cd /tmp/uml-workflow && bash install.sh

# 3. 確認
ls /mnt/skills/user/uml-workflow-v3/ /mnt/skills/user/usecase-md-to-json/ /mnt/skills/user/classdiagram-image-to-json/ /mnt/skills/user/json-to-models/ /mnt/skills/user/classdiagram-to-crud/
```

5ディレクトリが `/mnt/skills/user/` にインストールされます。

## パッケージ構成 / Package Contents

### オーケストレーター（パイプライン内蔵）
- **uml-workflow-v3** — 10ステップのワークフロー全体制御
  - `references/` 配下にパイプラインスキル10個を同梱
  - `single_skill` / `resume` / `partial` モードで任意ステップを実行可能

| Step | 内蔵スキル | 機能 |
|------|-----------|------|
| 1 | scenario-to-activity-v1 | シナリオ→アクティビティ図 |
| 2 | activity-to-usecase-v1 | アクティビティ図→ユースケース抽出 |
| 3 | usecase-to-class-v1 | ユースケース→クラス図 |
| 4 | class-to-statemachine-v1 | 状態遷移図生成 |
| 5 | usecase-to-sequence-v1 | シーケンス図生成 |
| 6 | model-validator-v1 | モデル横断検証 |
| 7 | security-design-v1 | セキュリティ設計 |
| 8 | usecase-to-code-v1 | コード生成 |
| 9 | usecase-to-test-v1 | テスト生成 |
| 10 | traceability-matrix-v1 | トレーサビリティマトリクス |

### 独立スキル（edit-helper）
ワークフロー外で直接使用するスキル：

- **usecase-md-to-json** — UC仕様のMarkdown手動編集後にJSON/図を再同期
- **classdiagram-image-to-json** — 手描き/ツール作成のクラス図をJSON取込
- **json-to-models** — domain-model.json直接編集後に図/ドキュメント再生成
- **classdiagram-to-crud** — クラス図からCRUD画面フラグメント生成

## インストール後のディレクトリ構造 / Directory Structure After Install

```
/mnt/skills/user/
├── uml-workflow-v3/              ← オーケストレーター
│   ├── SKILL.md
│   ├── scripts/
│   └── references/               ← パイプライン10スキル同梱
│       ├── scenario-to-activity-v1/
│       ├── activity-to-usecase-v1/
│       └── ...
├── usecase-md-to-json/           ← 独立edit-helper
├── classdiagram-image-to-json/
├── json-to-models/
└── classdiagram-to-crud/
```

## 使い方 / Usage

```
# フルワークフロー実行
「uml-workflow-v3を使って、以下のビジネスシナリオからアプリケーションを生成してください」

# 特定ステップだけ実行（single_skillモード）
「uml-workflowのStep 3を実行してください」
「uml-workflowのStep 6（モデル検証）を実行してください」

# 途中から再開（resumeモード）
「uml-workflowをStep 5から再開してください」

# 範囲指定（partialモード）
「uml-workflowのStep 3〜6を実行してください」
```

## アップデート / Updates

既存インストールがある場合、install.sh は差分更新（上書き）を行います。
既存の作業ファイル（`/mnt/user-data/outputs/` 配下）には影響しません。
