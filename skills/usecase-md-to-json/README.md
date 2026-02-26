# usecase-md-to-json

**UML Workflow v3 ヘルパースキル / Helper Skill for UML Workflow v3**

Markdown形式のユースケース仕様書（Cockburn形式）を `usecase-output.json` に変換します。  
Converts use case specifications in Cockburn-style Markdown to `usecase-output.json`.

**使い方 / Usage:**
```
「ユースケース仕様のMarkdownを修正したので、JSONに反映してください」
"I've edited the use case Markdown specs. Please update the JSON."
```

変換後は Step 3 以降のパイプラインを再実行してください。  
After conversion, re-run the pipeline from Step 3.

---


## 概要 / Overview

Markdown形式のユースケース仕様書（Cockburn形式）をJSON形式に変換するスキルです。

## 主な機能 / Key Features

- Markdownファイルからusecase-output.jsonを生成・更新
- 既存のJSONとマージ（メタデータ保持）
- Markdown編集を自動でJSONに反映
- バリデーションとエラー検出

## 問題を解決 / Problems Solved

### v1.2以前の問題 / Problems before v1.2

```
Markdown編集 ──X──> JSONに反映されない
                    ↓
               Step 3, 4で使われない
                    ↓
               最終コードに反映されない
```

### v1.3以降の解決 / Resolution from v1.3

```
Markdown編集 ──✓──> usecase-md-to-json
                    ↓
               usecase-output.json更新
                    ↓
               Step 3, 4で使われる
                    ↓
               最終コードに反映される ✅
```

## 入力 / Input

```
usecase-specifications/
  ├── UC-001_商品を注文する.md
  ├── UC-002_受注を出荷する.md
  └── UC-003_xxx.md
```

## 出力 / Output

```
usecase-output.json (更新済み)
usecase-output.json.backup (バックアップ)
```

## 使用方法 / How to Use

### 基本的な使い方 / Basic Usage

```
1. Markdownファイルを編集
   - UC-001_商品を注文する.md を修正
   - ストーリーポイントを8から5に変更

2. usecase-md-to-jsonを実行
   ユーザー: 「usecase-md-to-jsonを実行してください」

3. usecase-output.jsonが自動更新される

4. Step 3, 4を実行
   - usecase-to-class-v1
   - usecase-to-code-v1
```

## ワークフローでの位置 / Position in Workflow

```
Step 2: activity-to-usecase-v1.1
  ↓
  ├─→ UC-*.md (Markdown生成)
  └─→ usecase-output.json (JSON生成)
  ↓
[ユーザーがMarkdownを編集]
  ↓
Edit Helper: usecase-md-to-json ← このスキル
  ↓
usecase-output.json (更新)
  ↓
Step 3: usecase-to-class-v1 (クラス図生成)
  ↓
Step 8: usecase-to-code-v1 (コード生成)
```

## 解析されるセクション / Parsed Sections

| Markdownセクション | JSONフィールド |
|------------------|---------------|
| # UC-XXX: [name] | id, name |
| ストーリーポイント | story_points |
| 主成功シナリオ | main_flow |
| 拡張（代替フロー） | extensions |
| API操作 | api_operations |
| 特別要件 | special_requirements |

## 使用例 / Examples

### 例1: ストーリーポイント変更 / Example 1: Changing Story Points

```markdown
# UC-001_商品を注文する.md

- **ストーリーポイント**: 5  ← 8から変更
```

実行後:
```json
{
  "usecases": [
    {
      "id": "UC-001",
      "story_points": 5  // 更新された!
    }
  ]
}
```

### 例2: 拡張フロー追加 / Example 2: Adding Extension Flow

```markdown
## 拡張（代替フロー）

**5a. 商品が在庫切れの場合:**
- 5a1. システムが在庫切れを通知する
- 5a2. ステップ2に戻る
```

実行後:
```json
{
  "extensions": [
    {
      "step": "5a",
      "condition": "商品が在庫切れの場合",
      "actions": [
        "5a1. システムが在庫切れを通知する",
        "5a2. ステップ2に戻る"
      ]
    }
  ]
}
```

## 特徴 / Features

- ✅ **Markdown優先**: 人間が読みやすい形式で管理
- ✅ **自動同期**: 手動でJSONを編集する必要なし
- ✅ **既存データ保持**: メタデータとドメインモデルを保持
- ✅ **バリデーション**: 構造チェックと警告表示
- ✅ **バックアップ**: 既存JSONを自動バックアップ

## 制限事項 / Limitations

### v1.0の制限 / v1.0 Limitations

1. **一方向同期のみ**
   - Markdown → JSON ✅
   - JSON → Markdown ❌ (将来実装予定)

2. **Cockburn形式必須**
   - activity-to-usecase-v1.1が生成する形式
   - カスタム形式は非対応

3. **自動削除なし**
   - 削除したMarkdownファイルに対応するJSON要素は残る
   - 手動削除が必要

## ベストプラクティス / Best Practices

### 1. バックアップを確認 / Check Backup

```bash
# 実行前に自動バックアップが作成される
ls usecase-output.json.backup
```

### 2. Git管理 / Git Management

```bash
git add usecase-specifications/*.md
git add usecase-output.json
git commit -m "docs: UC-001のストーリーポイント変更"
```

### 3. 差分確認 / Check Diff

```bash
# 変更内容を確認
git diff usecase-output.json
```

## トラブルシューティング / Troubleshooting

### 問題: Markdownファイルが見つからない / Problem: Markdown file not found

**原因**: 命名規則に従っていない

**解決策**:
```bash
# 正しい命名: UC-001_name.md
# 間違い: uc-001.md, UC001.md
```

### 問題: ストーリーポイントが更新されない / Problem: Story points not updated

**原因**: Markdown形式が不正

**確認**:
```markdown
# 正しい形式:
- **ストーリーポイント**: 5

# 間違った形式:
- Story Points: 5
```

## バージョン / Version History

- **v1.0** (2026-01-24)
  - 初版リリース
  - Markdown→JSON変換
  - 既存JSONとのマージ
  - 基本バリデーション

## 標準準拠 / Standards Compliance

- Cockburn Use Case Format
- JSON形式はactivity-to-usecase-v1.1互換
- usecase-to-class-v1、usecase-to-code-v1と互換

## 関連スキル / Related Skills

- **activity-to-usecase-v1.1**: Markdownファイルを生成
- **usecase-to-class-v1**: JSONからクラス図を生成
- **usecase-to-code-v1**: JSONからコードを生成
- **json-to-models-v1.2**: ドメインモデルJSONの更新
