# usecase-md-to-json / ユースケース仕様書Markdown→JSON変換

**UML Workflow v3 ヘルパースキル / Helper Skill for UML Workflow v3**

Markdown 形式のユースケース仕様書（Cockburn 形式）を `usecase-output.json` に変換します。  
Markdown 形式のユースケース仕様書（Cockburn 形式）を `usecase-output.json` に変換します。 / Converts use case specifications in Cockburn-style Markdown to `usecase-output.json`.

**使い方 / Usage:**
```
「ユースケース仕様の Markdown を修正したので、JSON に反映してください」
"I've edited the use case Markdown specs. Please update the JSON."
```

変換後は Step 3 以降のパイプラインを再実行してください。  
変換後は Step 3 以降のパイプラインを再実行してください。 / After conversion, re-run the pipeline from Step 3.

---

## 概要 / Overview

Markdown 形式のユースケース仕様書（Cockburn 形式）を `usecase-output.json` に変換するスキルです。人間が読みやすい Markdown で仕様を管理しながら、パイプラインが必要とする JSON 形式に自動で同期します。  
Markdown 形式のユースケース仕様書（Cockburn 形式）を `usecase-output.json` に変換するスキルです。人間が読みやすい Markdown で仕様を管理しながら、パイプラインが必要とする JSON 形式に自動で同期します。 / A skill that converts Cockburn-format Markdown use case specifications into `usecase-output.json`. Manage specs in human-readable Markdown while automatically syncing to the JSON format required by the pipeline.

---

## 解決する問題 / Problems Solved

### v1.2 以前の問題 / Problems before v1.2

```
Markdown 編集 ──✗──> JSON に反映されない / Changes not reflected in JSON
                          ↓
                     Step 3, 4 で使われない / Not used by Steps 3, 4
                          ↓
                     最終コードに反映されない / Not reflected in final code
```

### v1.3 以降の解決 / Resolution from v1.3

```
Markdown 編集 ──✓──> usecase-md-to-json（このスキル / This skill）
                          ↓
                     usecase-output.json 更新 / Updated
                          ↓
                     Step 3, 4 で使われる / Used by Steps 3, 4
                          ↓
                     最終コードに反映される ✅ / Reflected in final code ✅
```

---

## 主な機能 / Key Features

- ✅ **Markdown 優先 / Markdown-first** — 人間が読みやすい形式で仕様を管理 / Manage specs in a human-readable format
- ✅ **自動同期 / Auto sync** — 手動で JSON を編集する必要なし / No need to manually edit JSON
- ✅ **既存データ保持 / Preserve existing data** — メタデータとドメインモデルを維持 / Maintains metadata and domain model
- ✅ **バリデーション / Validation** — 構造チェックと警告表示 / Structure check and warning display
- ✅ **バックアップ / Backup** — 既存 JSON を自動バックアップ / Auto-backs up existing JSON

---

## 入力・出力 / Input & Output

**入力 / Input:**
```
usecase-specifications/
  ├── UC-001_商品を注文する.md   / "Place an Order"
  ├── UC-002_受注を出荷する.md   / "Ship an Order"
  └── UC-003_xxx.md
```

**出力 / Output:**
```
usecase-output.json         ← 更新済み / Updated
usecase-output.json.backup  ← 自動バックアップ / Auto backup
```

---

## 使用方法 / How to Use

### 基本的な手順 / Basic Steps

```
1. Markdown ファイルを編集 / Edit the Markdown file
   - UC-001_商品を注文する.md を修正
   - ストーリーポイントを 8 から 5 に変更 / Change story points from 8 to 5

2. usecase-md-to-json を実行 / Run usecase-md-to-json
   ユーザー / User: 「usecase-md-to-json を実行してください」
                     "Please run usecase-md-to-json"

3. usecase-output.json が自動更新される / usecase-output.json is automatically updated

4. Step 3, Step 8 を実行 / Run Step 3 and Step 8
   - Step 3: usecase-to-class-v1  （クラス図生成 / Class diagram generation）
   - Step 8: usecase-to-code-v1   （コード生成 / Code generation）
```

---

## ワークフローでの位置 / Position in Workflow

```
Step 2: activity-to-usecase-v1
  ↓
  ├─→ UC-*.md  （Markdown 生成 / Generated）
  └─→ usecase-output.json  （JSON 生成 / Generated）
  ↓
[ユーザーが Markdown を編集 / User edits Markdown]
  ↓
Edit Helper: usecase-md-to-json ← このスキル / This skill
  ↓
usecase-output.json（更新 / Updated）
  ↓
Step 3: usecase-to-class-v1  （クラス図生成 / Class diagram generation）
  ↓
Step 8: usecase-to-code-v1   （コード生成 / Code generation）
```

---

## 解析されるセクション / Parsed Sections

| Markdown セクション / Section | JSON フィールド / Field |
|------------------------------|------------------------|
| `# UC-XXX: [name]`（タイトル行 / title line） | id, name |
| ストーリーポイント / Story Points | story_points         |
| 主成功シナリオ / Main Success Scenario | main_flow      |
| 拡張（代替フロー）/ Extensions (Alternative Flows) | extensions |
| API 操作 / API Operations    | api_operations         |
| 特別要件 / Special Requirements | special_requirements |

---

## 使用例 / Examples

### 例 1：ストーリーポイント変更 / Example 1: Changing Story Points

**Markdown 変更 / Markdown change:**
```markdown
# UC-001_商品を注文する.md / "Place an Order"

- **ストーリーポイント**: 5  ← 8 から変更 / Changed from 8
```

**実行後の JSON / JSON after execution:**
```json
{
  "usecases": [
    {
      "id": "UC-001",
      "story_points": 5
    }
  ]
}
```

### 例 2：拡張フロー追加 / Example 2: Adding an Extension Flow

**Markdown 追加 / Markdown addition:**
```markdown
## 拡張（代替フロー）/ Extensions (Alternative Flows)

**5a. 商品が在庫切れの場合 / If the item is out of stock:**
- 5a1. システムが在庫切れを通知する / System notifies out-of-stock
- 5a2. ステップ 2 に戻る / Return to step 2
```

**実行後の JSON / JSON after execution:**
```json
{
  "extensions": [
    {
      "step": "5a",
      "condition": "商品が在庫切れの場合 / Item is out of stock",
      "actions": [
        "5a1. システムが在庫切れを通知する",
        "5a2. ステップ 2 に戻る"
      ]
    }
  ]
}
```

---

## 制限事項 / Limitations

1. **一方向同期のみ / One-way sync only**  
   Markdown → JSON ✅ / JSON → Markdown ❌（将来実装予定 / Planned for future）

2. **Cockburn 形式必須 / Cockburn format required**  
   `activity-to-usecase-v1` が生成する形式のみ対応。カスタム形式は非対応です。  
   `activity-to-usecase-v1` が生成する形式のみ対応。カスタム形式は非対応です。 / Only the format generated by `activity-to-usecase-v1` is supported. Custom formats are not.

3. **自動削除なし / No auto-deletion**  
   削除した Markdown ファイルに対応する JSON 要素は残ります。手動での削除が必要です。  
   削除した Markdown ファイルに対応する JSON 要素は残ります。手動での削除が必要です。 / JSON entries corresponding to deleted Markdown files remain. Manual deletion is required.

---

## ベストプラクティス / Best Practices

### バックアップを確認 / Check Backup
```bash
# 実行前に自動バックアップが作成される / Auto backup is created before execution
ls usecase-output.json.backup
```

### Git で管理 / Git Management
```bash
git add usecase-specifications/*.md
git add usecase-output.json
git commit -m "docs: UC-001 のストーリーポイント変更 / Update UC-001 story points"
```

### 差分確認 / Check Diff
```bash
# 変更内容を確認 / Review changes
git diff usecase-output.json
```

---

## トラブルシューティング / Troubleshooting

### 問題：Markdown ファイルが見つからない / Problem: Markdown file not found

**原因 / Cause:** 命名規則に従っていない / File does not follow naming convention

**解決策 / Solution:**
```bash
# 正しい命名 / Correct: UC-001_name.md
# 誤った命名 / Wrong:   uc-001.md, UC001.md
```

### 問題：ストーリーポイントが更新されない / Problem: Story points not updated

**原因 / Cause:** Markdown の書式が不正 / Incorrect Markdown format

**確認 / Check:**
```markdown
# 正しい形式 / Correct format:
- **ストーリーポイント**: 5

# 誤った形式 / Wrong format:
- Story Points: 5
```

---

## バージョン / Version History

- **v1.0** (2026-01-24)
  - 初版リリース / Initial release
  - Markdown → JSON 変換 / Markdown → JSON conversion
  - 既存 JSON とのマージ / Merging with existing JSON
  - 基本バリデーション / Basic validation

---

## 標準準拠 / Standards Compliance

- Cockburn Use Case Format（Cockburn ユースケース形式）
- JSON 形式は `activity-to-usecase-v1` 互換 / JSON format compatible with `activity-to-usecase-v1`
- `usecase-to-class-v1`、`usecase-to-code-v1` と互換 / Compatible with `usecase-to-class-v1` and `usecase-to-code-v1`

---

## 関連スキル / Related Skills

| スキル / Skill | 関係 / Relation |
|---------------|----------------|
| `activity-to-usecase-v1` | Markdown ファイルを生成するスキル / Generates the Markdown files |
| `usecase-to-class-v1` | 更新された JSON からクラス図を生成 / Generates class diagrams from the updated JSON |
| `usecase-to-code-v1` | 更新された JSON からコードを生成 / Generates code from the updated JSON |
| `json-to-models` | ドメインモデル JSON を更新した後に使用 / Used after updating domain-model.json |
