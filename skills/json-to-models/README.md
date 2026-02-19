# json-to-models

## 概要

domain-model.jsonを編集した後、PlantUML、XMI、Markdownドキュメントを再生成するスキルです。

**v1.2の新機能:** XMI生成の有無を選択可能（最大40%高速化）⚡

## 主な用途

✅ **モデル修正ワークフロー**
- レビュー後にドメインモデルを修正
- JSONを編集するだけで全フォーマットを更新

✅ **プログラマティックなモデル管理**
- スクリプトでモデルを一括修正
- CI/CDパイプラインに組み込み

## 実行オプション (NEW! v1.2 ⭐)

### パフォーマンス最適化

```
質問: XMIファイルを生成しますか？
  はい (デフォルト): PlantUML + XMI + Markdown
  いいえ: PlantUML + Markdown のみ（約40%高速化）
```

**推奨設定:**
- 反復的なモデル修正中: **いいえ** (素早く確認)
- 最終成果物として保存: **はい** (完全なアーカイブ)
- UMLツール使用時: **はい** (Papyrus等で編集)

## 使用方法

### 1. domain-model.jsonを編集

```json
{
  "entities": [
    {
      "name": "Order",
      "attributes": [
        // 新しい属性を追加
        {
          "name": "shippingFee",
          "type": "decimal",
          "required": true,
          "default": "0.00"
        }
      ]
    }
  ]
}
```

### 2. json-to-modelsを実行

**パターンA: 完全な再生成**
```
ユーザー: json-to-modelsを使って、このdomain-model.jsonから
PlantUMLとXMIを再生成してください

Claude: XMIファイルを生成しますか？ (はい/いいえ)
ユーザー: はい

→ PlantUML + XMI + Markdown 生成
```

**パターンB: 素早い確認**
```
ユーザー: json-to-modelsでPlantUMLを素早く確認したい

Claude: XMIファイルを生成しますか？ (はい/いいえ)
ユーザー: いいえ

→ PlantUML + Markdown のみ（40%高速化）
```

### 3. 生成される成果物

**If XMI生成 = はい:**
- ✅ `{project}_class.puml` - 更新されたクラス図
- ✅ `{project}_class-model.xmi` - 更新されたXMI
- ✅ `{project}_architecture-overview.md` - 更新されたドキュメント

**If XMI生成 = いいえ:**
- ✅ `{project}_class.puml` - 更新されたクラス図
- ⏭️ `{project}_class-model.xmi` - **SKIPPED**
- ✅ `{project}_architecture-overview.md` - 更新されたドキュメント

### 4. コードを再生成（オプション）

```
Claude: usecase-to-code-v1を使って、
更新されたドメインモデルでコードを再生成してください
```

## よくある修正例

### 属性の追加
```json
"attributes": [
  {
    "name": "newAttribute",
    "type": "string",
    "required": false,
    "description": "新しい属性"
  }
]
```

### リレーションシップの変更
```json
"relationships": [
  {
    "type": "has-many",
    "target": "OrderItem",
    "source_multiplicity": "1",
    "target_multiplicity": "1..*"  // 多重度変更
  }
]
```

### エンティティの追加
```json
"entities": [
  {
    "name": "NewEntity",
    "japanese_name": "新規エンティティ",
    "attributes": [...],
    "relationships": [...]
  }
]
```

## ワークフローでの位置

```
uml-workflow-v1
  ↓
domain-model.json生成
  ↓
[手動編集]
  ↓
json-to-models ← このスキル
  ↓
PlantUML/XMI/Markdown更新
  ↓
usecase-to-code-v1
  ↓
コード再生成
```

## ベストプラクティス

1. **編集前にバックアップ**
   ```bash
   cp domain-model.json domain-model.json.bak
   ```

2. **段階的な修正**
   - 一度に大きく変更しない
   - 修正 → 再生成 → 確認を繰り返す

3. **バリデーション**
   - 修正後、必ずバリデーションを実行

4. **バージョン管理**
   - Gitで変更履歴を管理

## トラブルシューティング

### Q: JSONのエラーが出る
**A:** JSONの構文を確認してください
- カンマの位置
- カッコの閉じ忘れ
- 文字列のクォート

### Q: リレーション先が見つからない
**A:** リレーション先のエンティティが存在するか確認

### Q: 生成されたPlantUMLが正しくない
**A:** domain-model.jsonの構造を確認
- 必須フィールドがすべて存在するか
- 型定義が正しいか

## バージョン

- **v1.2** (2026-01-24)
  - ⭐ **NEW**: 実行オプション追加（XMI生成の選択可能）
  - ⚡ 約40%の処理時間短縮（XMI生成なし時）
  - ✅ 完全な後方互換性

- **v1.0** (2026-01-24): 初版リリース
