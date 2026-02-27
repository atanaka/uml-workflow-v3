# usecase-md-to-json

## 概要

Markdown形式のユースケース仕様書（Cockburn形式）をJSON形式に変換するスキルです。

## 主な機能

- Markdownファイルからusecase-output.jsonを生成・更新
- 既存のJSONとマージ（メタデータ保持）
- Markdown編集を自動でJSONに反映
- バリデーションとエラー検出

## 問題を解決

### v1.2以前の問題

```
Markdown編集 ──X──> JSONに反映されない
                    ↓
               Step 3, 4で使われない
                    ↓
               最終コードに反映されない
```

### v1.3以降の解決

```
Markdown編集 ──✓──> usecase-md-to-json
                    ↓
               usecase-output.json更新
                    ↓
               Step 3, 4で使われる
                    ↓
               最終コードに反映される ✅
```

## 入力

```
usecase-specifications/
  ├── UC-001_商品を注文する.md
  ├── UC-002_受注を出荷する.md
  └── UC-003_xxx.md
```

## 出力

```
usecase-output.json (更新済み)
usecase-output.json.backup (バックアップ)
```

## 使用方法

### 基本的な使い方

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

## ワークフローでの位置

```
Step 2: activity-to-usecase-v1.1
  ↓
  ├─→ UC-*.md (Markdown生成)
  └─→ usecase-output.json (JSON生成)
  ↓
[ユーザーがMarkdownを編集]
  ↓
Step 2.5: usecase-md-to-json ← このスキル
  ↓
usecase-output.json (更新)
  ↓
Step 3: usecase-to-class-v1
  ↓
Step 4: usecase-to-code-v1
```

## 解析されるセクション

| Markdownセクション | JSONフィールド |
|------------------|---------------|
| # UC-XXX: [name] | id, name |
| ストーリーポイント | story_points |
| 主成功シナリオ | main_flow |
| 拡張（代替フロー） | extensions |
| API操作 | api_operations |
| 特別要件 | special_requirements |

## 使用例

### 例1: ストーリーポイント変更

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

### 例2: 拡張フロー追加

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

## 特徴

- ✅ **Markdown優先**: 人間が読みやすい形式で管理
- ✅ **自動同期**: 手動でJSONを編集する必要なし
- ✅ **既存データ保持**: メタデータとドメインモデルを保持
- ✅ **バリデーション**: 構造チェックと警告表示
- ✅ **バックアップ**: 既存JSONを自動バックアップ

## 制限事項

### v1.0の制限

1. **一方向同期のみ**
   - Markdown → JSON ✅
   - JSON → Markdown ❌ (将来実装予定)

2. **Cockburn形式必須**
   - activity-to-usecase-v1.1が生成する形式
   - カスタム形式は非対応

3. **自動削除なし**
   - 削除したMarkdownファイルに対応するJSON要素は残る
   - 手動削除が必要

## ベストプラクティス

### 1. バックアップを確認

```bash
# 実行前に自動バックアップが作成される
ls usecase-output.json.backup
```

### 2. Git管理

```bash
git add usecase-specifications/*.md
git add usecase-output.json
git commit -m "docs: UC-001のストーリーポイント変更"
```

### 3. 差分確認

```bash
# 変更内容を確認
git diff usecase-output.json
```

## トラブルシューティング

### 問題: Markdownファイルが見つからない

**原因**: 命名規則に従っていない

**解決策**:
```bash
# 正しい命名: UC-001_name.md
# 間違い: uc-001.md, UC001.md
```

### 問題: ストーリーポイントが更新されない

**原因**: Markdown形式が不正

**確認**:
```markdown
# 正しい形式:
- **ストーリーポイント**: 5

# 間違った形式:
- Story Points: 5
```

## バージョン

- **v1.0** (2026-01-24)
  - 初版リリース
  - Markdown→JSON変換
  - 既存JSONとのマージ
  - 基本バリデーション

## 標準準拠

- Cockburn Use Case Format
- JSON形式はactivity-to-usecase-v1.1互換
- usecase-to-class-v1、usecase-to-code-v1と互換

## 関連スキル

- **activity-to-usecase-v1.1**: Markdownファイルを生成
- **usecase-to-class-v1**: JSONからクラス図を生成
- **usecase-to-code-v1**: JSONからコードを生成
- **json-to-models-v1.2**: ドメインモデルJSONの更新
