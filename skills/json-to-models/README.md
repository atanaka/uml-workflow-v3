# json-to-models / JSON→モデル再生成

**UML Workflow v3 ヘルパースキル / Helper Skill for UML Workflow v3**

`domain-model.json` を編集した後に PlantUML・XMI・Markdown ドキュメントを再生成します。  
`domain-model.json` を編集した後に PlantUML・XMI・Markdown ドキュメントを再生成します。 / Regenerates PlantUML diagrams, XMI, and Markdown documentation after editing `domain-model.json`.

**使い方 / Usage:**
```
「domain-model.json を更新したので、クラス図を再生成してください」
"I've updated domain-model.json. Please regenerate the class diagram."
```

---

## 概要 / Overview

`domain-model.json` を手動で編集した後に、PlantUML・XMI・Markdown ドキュメントをまとめて再生成するスキルです。  
`domain-model.json` を手動で編集した後に、PlantUML・XMI・Markdown ドキュメントをまとめて再生成するスキルです。 / A skill that regenerates PlantUML diagrams, XMI, and Markdown documentation all at once after manually editing `domain-model.json`.

**v1.2 の新機能 / New in v1.2:** XMI 生成の有無を選択可能（最大 40% 高速化）⚡  
**v1.2 の新機能 / New in v1.2:** XMI 生成の有無を選択可能（最大 40% 高速化 / up to 40% faster）⚡

---

## 主な用途 / Primary Use Cases

✅ **モデル修正ワークフロー / Model Editing Workflow**  
レビュー後にドメインモデルを修正し、JSON を編集するだけで全フォーマットを更新します。  
レビュー後にドメインモデルを修正し、JSON を編集するだけで全フォーマットを更新します。 / Edit the domain model after review — just update the JSON and all formats are regenerated.

✅ **プログラマティックなモデル管理 / Programmatic Model Management**  
スクリプトでモデルを一括修正したり、CI/CD パイプラインに組み込んだりできます。 / スクリプトでモデルを一括修正したり、CI/CD パイプラインに組み込んだりできます。 / Batch-edit models via scripts or integrate into CI/CD pipelines.

---

## 実行オプション / Execution Options (v1.2 ⭐)

### パフォーマンス最適化 / Performance Optimization

```
質問 / Question: XMI ファイルを生成しますか？/ Generate XMI file?
  はい / Yes (デフォルト / default): PlantUML + XMI + Markdown
  いいえ / No:                       PlantUML + Markdown のみ（約 40% 高速化 / ~40% faster）
```

**推奨設定 / Recommended settings:**

| シナリオ / Scenario | 推奨 / Recommendation |
|--------------------|----------------------|
| 反復的なモデル修正中 / During iterative editing | **いいえ / No**（素早く確認 / Quick review） |
| 最終成果物として保存 / Saving final artifacts | **はい / Yes**（完全なアーカイブ / Full archive） |
| UML ツール使用時 / When using UML tools | **はい / Yes**（Papyrus 等で編集 / For Papyrus, etc.） |

---

## 使用方法 / How to Use

### 1. domain-model.json を編集 / Edit domain-model.json

```json
{
  "entities": [
    {
      "name": "Order",
      "attributes": [
        {
          "name": "shippingFee",
          "type": "decimal",
          "required": true,
          "default": "0.00",
          "description": "送料 / Shipping fee"
        }
      ]
    }
  ]
}
```

### 2. json-to-models を実行 / Run json-to-models

**パターン A：完全な再生成 / Pattern A: Full regeneration**
```
ユーザー / User: 「json-to-models を使って、この domain-model.json から
                  PlantUML と XMI を再生成してください」
                  "Use json-to-models to regenerate PlantUML and XMI
                   from this domain-model.json"

Claude: XMI ファイルを生成しますか？/ Generate XMI file? (はい / Yes・いいえ / No)
ユーザー / User: はい / Yes

→ PlantUML + XMI + Markdown 生成 / Generated
```

**パターン B：素早い確認 / Pattern B: Quick check**
```
ユーザー / User: 「json-to-models で PlantUML を素早く確認したい」
                  "I want to quickly check the PlantUML with json-to-models"

Claude: XMI ファイルを生成しますか？/ Generate XMI file? (はい / Yes・いいえ / No)
ユーザー / User: いいえ / No

→ PlantUML + Markdown のみ（40% 高速化）/ PlantUML + Markdown only (40% faster)
```

### 3. 生成される成果物 / Generated Artifacts

**XMI 生成 = はい / XMI = Yes:**
- ✅ `{project}_class.puml` — 更新されたクラス図 / Updated class diagram
- ✅ `{project}_class-model.xmi` — 更新された XMI / Updated XMI
- ✅ `{project}_architecture-overview.md` — 更新されたドキュメント / Updated documentation

**XMI 生成 = いいえ / XMI = No:**
- ✅ `{project}_class.puml` — 更新されたクラス図 / Updated class diagram
- ⏭️ `{project}_class-model.xmi` — **スキップ / SKIPPED**
- ✅ `{project}_architecture-overview.md` — 更新されたドキュメント / Updated documentation

### 4. コードを再生成（オプション）/ Regenerate Code (Optional)

```
「usecase-to-code-v1 を使って、更新されたドメインモデルでコードを再生成してください」
"Use usecase-to-code-v1 to regenerate code with the updated domain model"
```

---

## よくある修正例 / Common Modification Examples

### 属性の追加 / Adding Attributes
```json
"attributes": [
  {
    "name": "newAttribute",
    "type": "string",
    "required": false,
    "description": "新しい属性 / New attribute"
  }
]
```

### リレーションの変更 / Modifying Relationships
```json
"relationships": [
  {
    "type": "has-many",
    "target": "OrderItem",
    "source_multiplicity": "1",
    "target_multiplicity": "1..*"
  }
]
```

### エンティティの追加 / Adding Entities
```json
"entities": [
  {
    "name": "NewEntity",
    "japanese_name": "新規エンティティ",
    "attributes": [],
    "relationships": []
  }
]
```

---

## ワークフローでの位置 / Position in Workflow

```
uml-workflow-v3 Step 3（usecase-to-class-v1）
  ↓
domain-model.json 生成 / generated
  ↓
[手動編集 / Manual editing]
  ↓
json-to-models ← このスキル / This skill
  ↓
PlantUML / XMI / Markdown 更新 / Updated
  ↓
Step 8: usecase-to-code-v1
  ↓
コード再生成 / Code regenerated
```

---

## ベストプラクティス / Best Practices

1. **編集前にバックアップ / Back up before editing**
   ```bash
   cp domain-model.json domain-model.json.bak
   ```

2. **段階的な修正 / Make changes incrementally**  
   一度に大きく変更せず、修正 → 再生成 → 確認を繰り返します。 /    一度に大きく変更せず、修正 → 再生成 → 確認を繰り返します。 / Avoid large changes at once. Repeat: edit → regenerate → verify.

3. **バリデーション / Validate**  
   修正後、必ず `model-validator-v1` でバリデーションを実行します。  
   修正後、必ず `model-validator-v1` でバリデーションを実行します。 / Always run `model-validator-v1` to validate after editing.

4. **バージョン管理 / Version control**  
   Git で変更履歴を管理することを推奨します。  
   Git で変更履歴を管理することを推奨します。 / Use Git to track change history.

---

## トラブルシューティング / Troubleshooting

### Q: JSON のエラーが出る / JSON errors occur
**A:** JSON の構文を確認してください：カンマの位置、閉じカッコ、文字列のクォートなど。  
**A:** JSON の構文を確認してください：カンマの位置、閉じカッコ、文字列のクォートなど。 / Check JSON syntax: comma placement, closing brackets, string quotes, etc.

### Q: リレーション先が見つからない / Relation target not found
**A:** リレーション先のエンティティが `entities` 配列に存在するか確認してください。  
**A:** リレーション先のエンティティが `entities` 配列に存在するか確認してください。 / Verify that the target entity exists in the `entities` array.

### Q: 生成された PlantUML が正しくない / Generated PlantUML is incorrect
**A:** `domain-model.json` の構造を確認してください。必須フィールドが揃っているか、型定義が正しいかチェックします。  
**A:** `domain-model.json` の構造を確認してください。必須フィールドが揃っているか、型定義が正しいかチェックします。 / Check the `domain-model.json` structure. Ensure all required fields are present and type definitions are correct.

---

## バージョン / Version History

- **v1.2** (2026-01-24)
  - ⭐ **NEW**: 実行オプション追加（XMI 生成の選択が可能に）/ Added execution option (XMI generation now selectable)
  - ⚡ 約 40% の処理時間短縮（XMI 生成なし時）/ ~40% faster processing when XMI is skipped
  - ✅ 完全な後方互換性 / Full backward compatibility

- **v1.0** (2026-01-24)
  - 初版リリース / Initial release
