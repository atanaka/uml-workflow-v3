# Class Diagram Image to JSON Converter / クラス図画像→JSONコンバーター

**UML Workflow v3 ヘルパースキル / Helper Skill for UML Workflow v3**

手描き・UMLツール出力のクラス図画像を `domain-model.json` に変換します。  
手描き・UMLツール出力のクラス図画像を `domain-model.json` に変換します。 / Converts class diagram images (hand-drawn or from UML tools) into `domain-model.json`.

**使い方 / Usage:**
```
「この手描きのクラス図をJSONに変換してください」（画像を添付）
"Please convert this class diagram to domain-model.json" (attach image)
```

変換後は `json-to-models` スキルで PlantUML 図を再生成するか、Step 4 以降のパイプラインを再実行してください。  
変換後は `json-to-models` スキルで PlantUML 図を再生成するか、Step 4 以降のパイプラインを再実行してください。 / After conversion, use the `json-to-models` skill to regenerate PlantUML diagrams, or re-run the pipeline from Step 4.

---

## 概要 / Overview

JPEG・PNG・PDF のクラス図画像を構造化された `domain-model.json` 形式に変換します。uml-workflow-v3 のパイプラインにシームレスに統合できます。  
JPEG・PNG・PDF のクラス図画像を構造化された `domain-model.json` 形式に変換します。uml-workflow-v3 パイプラインにシームレスに統合できます。 / Converts class diagram images in JPEG, PNG, or PDF format into structured `domain-model.json`. Integrates seamlessly into the uml-workflow-v3 pipeline.

---

## クイックスタート / Quick Start

### 基本的な使い方 / Basic Usage

1. **クラス図を作成またはエクスポート / Create or export a class diagram**  
   UMLツール（Eclipse Papyrus、Draw.io、Lucidchart 等）でクラス図を作成し、PNG・JPEG・PDF でエクスポートします。テキストが明確に読めることを確認してください（推奨幅：1200px 以上）。  
   UMLツール（Eclipse Papyrus、Draw.io、Lucidchart 等）でクラス図を作成し、PNG・JPEG・PDF でエクスポートします。テキストが明確に読めることを確認してください（推奨幅：1200px 以上）。 / Create a class diagram in any UML tool and export as PNG, JPEG, or PDF. Recommended width: 1200px+.

2. **Claude にアップロード / Upload to Claude**  
   画像ファイルを会話に添付してスキルを起動します。 /    Attach the image file to the conversation and trigger the skill.

3. **JSON に変換 / Convert to JSON**
   ```
   ユーザー / User: 「このクラス図を domain-model.json に変換してください」
                    "Please convert this class diagram to domain-model.json"
   Claude: [画像を解析して JSON を生成 / Analyzes image and generates JSON]
   ```

### ワークフロー統合 / Workflow Integration

#### シナリオA：ビジュアル図からスタート / Scenario A: Start from Visual Diagram
```
ユーザーがビジュアルツールでクラス図を作成 / User creates class diagram visually
  ↓
Claude: classdiagram-image-to-json
  ↓
domain-model.json 生成 / domain-model.json created
  ↓
Step 5（usecase-to-sequence-v1）以降を継続 / Continue with Step 5 or later steps
```

#### シナリオB：自動生成図を手修正 / Scenario B: Refine Auto-Generated Diagram
```
UML Workflow Step 3 完了（usecase-to-class-v1）/ UML Workflow Step 3 completes
  ↓
ユーザーが図をエクスポートしてモデリングツールで修正 / User exports and edits in modeling tool
  ↓
修正した図をアップロード / Upload refined diagram
  ↓
Claude: classdiagram-image-to-json（マージモード / merge mode）
  ↓
domain-model.json 更新 / domain-model.json updated
  ↓
Step 5 以降を継続 / Continue with Step 5 or later steps
```

---

## 使用例 / Examples

### 例1：シンプルなECモデル / Example 1: Simple E-Commerce Model

**入力図（概念）/ Input Diagram (conceptual):**
```
┌─────────────────┐         ┌─────────────────┐
│    Customer     │         │      Order      │
├─────────────────┤         ├─────────────────┤
│ - customerId    │ 1    0..* │ - orderId      │
│ - name          │─────────>│ - orderDate    │
│ - email         │         │ - totalAmount  │
└─────────────────┘         └─────────────────┘
```

**コマンド / Command:**
```
「このクラス図を domain-model.json に変換してください」
"Please convert this class diagram to domain-model.json"
```

**生成される JSON / Generated JSON:**
```json
{
  "entities": [
    {
      "name": "Customer",
      "attributes": [
        { "name": "customerId", "type": "String", "required": true, "unique": true },
        { "name": "name",       "type": "String", "required": true },
        { "name": "email",      "type": "String", "required": true }
      ]
    },
    {
      "name": "Order",
      "attributes": [
        { "name": "orderId",      "type": "String", "required": true, "unique": true },
        { "name": "orderDate",    "type": "Date",   "required": true },
        { "name": "totalAmount",  "type": "Number", "required": true }
      ]
    }
  ],
  "relationships": [
    {
      "type": "association",
      "source": "Customer", "target": "Order",
      "sourceMultiplicity": "1", "targetMultiplicity": "0..*",
      "targetName": "orders"
    }
  ]
}
```

### 例2：マージモード / Example 2: Merge Mode

**シナリオ / Scenario:**  
既存の `domain-model.json` に新しい Product クラスを追加したい場合。  
既存の `domain-model.json` に新しい Product クラスを追加したい場合。 / You have an existing `domain-model.json` and want to add a new Product class.

**コマンド / Command:**
```
「Product クラスを図に追加しました。既存モデルにマージしてください。」
"I've added a Product class to my diagram. Please merge it with the existing model."
```

**Claude の応答 / Claude's Response:**
```
既存の domain-model.json を検出しました。変更をマージしています：
Found existing domain-model.json. Merging changes:

追加 / Added:
- Product エンティティ（productId、name、price、stock 属性）
  Product entity with attributes (productId, name, price, stock)
- Order-Product リレーション（多対多）/ Order-Product relationship (many-to-many)

変更 / Modified:
- Order エンティティ（items 属性を追加）/ Order entity (added items attribute)

保持 / Preserved:
- 既存の Customer エンティティ / Existing Customer entity
- Customer-Order リレーション / Customer-Order relationship

マージ済みモデルを domain-model.json に保存しました。
Merged model saved to domain-model.json.
```

### 例3：継承を含む複雑な図 / Example 3: Complex Diagram with Inheritance

**入力図の特徴 / Input Diagram Features:**
- 抽象クラス：`Payment`（abstract）/ Abstract class: `Payment`
- 具象クラス：`CreditCardPayment`、`PayPalPayment` / Concrete classes: `CreditCardPayment`, `PayPalPayment`
- 汎化（継承）リレーション / Generalization (inheritance) relationships

**コマンド / Command:**
```
「この支払い階層図を JSON に変換してください」
"Convert this payment hierarchy diagram to JSON"
```

**生成される JSON（抜粋）/ Generated JSON (excerpt):**
```json
{
  "entities": [
    {
      "name": "Payment", "isAbstract": true,
      "attributes": [
        { "name": "paymentId", "type": "String", "required": true, "unique": true },
        { "name": "amount",    "type": "Number", "required": true }
      ],
      "methods": [{ "name": "processPayment", "returnType": "Boolean", "parameters": [] }]
    },
    { "name": "CreditCardPayment", "attributes": [{ "name": "cardNumber", "type": "String", "required": true }] },
    { "name": "PayPalPayment",     "attributes": [{ "name": "paypalEmail", "type": "String", "required": true }] }
  ],
  "relationships": [
    { "type": "generalization", "source": "CreditCardPayment", "target": "Payment" },
    { "type": "generalization", "source": "PayPalPayment",     "target": "Payment" }
  ]
}
```

---

## 対応 UML 要素 / Supported UML Elements

### クラス / Classes
- ✅ クラス名 / Class names
- ✅ ステレオタイプ：`<<entity>>`, `<<value object>>`, `<<enumeration>>`, `<<service>>` 等 / Stereotypes
- ✅ 抽象クラス / Abstract classes
- ✅ インターフェース / Interfaces

### 属性 / Attributes
- ✅ 名前と型 / Name and type
- ✅ 可視性：`+` public, `-` private, `#` protected, `~` package
- ✅ 多重度：`[0..1]`, `[0..*]` 等 / Multiplicity
- ✅ デフォルト値 / Default values
- ✅ 制約：`{unique}`, `{required}`, `{id}` / Constraints

### メソッド / Methods
- ✅ 名前と戻り型 / Name and return type
- ✅ パラメータと型 / Parameters with types
- ✅ 可視性 / Visibility
- ✅ ステレオタイプ：`<<constructor>>`, `<<query>>`, `<<command>>`

### 関係 / Relationships
- ✅ 関連（単方向・双方向）/ Association (uni/bidirectional)
- ✅ 集約（空きダイヤモンド）/ Aggregation (hollow diamond)
- ✅ コンポジション（塗りつぶしダイヤモンド）/ Composition (filled diamond)
- ✅ 汎化（継承）/ Generalization (inheritance)
- ✅ 実現（インターフェース実装）/ Realization (interface implementation)
- ✅ 両端の多重度 / Multiplicities on both ends
- ✅ ロール名 / Role names

### 値オブジェクトと列挙型 / Value Objects & Enums
- ✅ 値を持つ列挙型 / Enumerations with values
- ✅ 属性を持つ値オブジェクト / Value objects with attributes

---

## ベストプラクティス / Best Practices

### 図の作成時 / For Creating Diagrams

1. **標準 UML 記法を使用 / Use standard UML notation**  
   UML 2.5 の慣例に従い、標準記号と多重度を使用します。  
   UML 2.5 の慣例に従い、標準記号と多重度を使用します。 / Follow UML 2.5 conventions and use standard symbols with multiplicities.

2. **テキストを読みやすく / Make text readable**  
   明確で読みやすいフォント、高コントラスト（暗いテキストに明るい背景）、十分なフォントサイズ（最終エクスポートで 12pt 以上）を使用します。 /    Use clear legible fonts, high contrast (dark text on light background), and adequate font size (12pt+ in final export).

3. **レイアウトを整理 / Organize layout**  
   線の重なりを避け、関連クラスをグループ化し、一貫した間隔を保ちます。 /    Avoid overlapping lines, group related classes, and use consistent spacing.

4. **詳細を記載 / Include details**  
   属性の型、多重度、ステレオタイプを適切に記載します。 /    Add attribute types, specify multiplicities, and use stereotypes appropriately.

5. **エクスポート品質 / Export quality**  
   PNG はロスレス圧縮、JPEG は最高品質設定、PDF はテキストがベクターベースであることを確認します。推奨解像度：幅 1200px 以上。  
   PNG はロスレス圧縮、JPEG は最高品質設定、PDF はテキストがベクターベースであることを確認します。推奨解像度：幅 1200px 以上。 / PNG: lossless compression. JPEG: maximum quality. PDF: vector-based text. Recommended: 1200px+ width.

### マージ時 / For Merging

1. **マージ前に確認 / Review before merging**  
   「変更内容を先に見せてください」とリクエストすると、Claude が適用前に差分を表示します。  
   「変更内容を先に見せてください」とリクエストすると、Claude が適用前に差分を表示します。 / Request "Show me what will change" — Claude will display a diff before applying.

2. **競合の処理 / Handle conflicts**  
   クラス定義が異なる場合、どちらを残すか選択します。Claude が競合について確認を求めます。  
   クラス定義が異なる場合、どちらを残すか選択します。Claude が競合について確認を求めます。 / If class definitions differ, choose which to keep. Claude will ask for clarification on conflicts.

3. **メタデータの保持 / Preserve metadata**  
   既存のノート・ドキュメント・カスタムフィールドは保持されます。 /    Existing notes, documentation, and custom JSON fields are preserved.

---

## より良い結果のためのヒント / Tips for Better Results

### 画像品質 / Image Quality
- ✅ 高解像度（幅 1200px 以上）/ High resolution (1200px+)
- ✅ 良好な照明（写真の場合）/ Good lighting (for photos)
- ✅ 直接スクリーンショット（デジタル図の場合）/ Direct screenshot (for digital diagrams)
- ❌ ぼやけた画像は避ける / Avoid blurry images
- ❌ 過度な圧縮は避ける / Avoid excessive compression

### 図の明瞭さ / Diagram Clarity
- ✅ 明確なクラス名 / Clear class names
- ✅ 型付き属性 / Typed attributes
- ✅ ラベル付きリレーション / Labeled relationships
- ✅ 可視の多重度 / Visible multiplicities
- ❌ 小さすぎるフォントは避ける / Avoid tiny fonts
- ❌ ごちゃごちゃしたレイアウトは避ける / Avoid cluttered layouts

### 記法 / Notation
- ✅ 標準 UML 記号 / Standard UML symbols
- ✅ 一貫したスタイル / Consistent style
- ❌ 独自記法は避ける / Avoid custom notation
- ❌ あいまいな矢印は避ける / Avoid ambiguous arrows

---

## トラブルシューティング / Troubleshooting

### 問題：「属性の型を読み取れない」/ Problem: "Cannot read attribute types"

**原因 / Cause:** テキストが小さすぎるかぼやけている / Text too small or blurry

**解決策 / Solution:**  
より高い解像度で再エクスポートする、図を拡大してスクリーンショットを撮る、またはラスター（PNG）の代わりにベクター（PDF）でエクスポートします。  
より高い解像度で再エクスポートする、拡大してスクリーンショットを撮る、またはベクター（PDF）でエクスポートします。 / Re-export at higher resolution, zoom in before screenshotting, or use vector export (PDF) instead of raster (PNG).

### 問題：「リレーションの方向が不明確」/ Problem: "Relationship direction unclear"

**原因 / Cause:** 矢印が見えないか非標準 / Arrow not visible or non-standard

**解決策 / Solution:**  
標準 UML 矢印を使用し、方向ラベルを追加します。  
標準 UML 矢印を使用し、方向ラベルを追加します。 / Use standard UML arrows and add explicit direction labels.

### 問題：「マージで重複が発生した」/ Problem: "Merge created duplicates"

**原因 / Cause:** クラス名が完全に一致していない / Class names don't match exactly

**解決策 / Solution:**  
クラス名が大文字・小文字も含めて完全一致しているか確認し、マージ差分を適用前にレビューします。 / Ensure class names are identical (case-sensitive) and review the merge diff before applying.

### 問題：「一部のクラスが認識されない」/ Problem: "Missing some classes"

**原因 / Cause:** コントラストが低いか要素が重なっている / Low contrast or overlapping elements

**解決策 / Solution:**  
図のコントラストを上げ、重なっている要素を分離し、白い背景で再エクスポートします。 / Increase diagram contrast, separate overlapping elements, and re-export with a white background.

---

## 他スキルとの連携 / Integration with Other Skills

このスキルの後に使えるスキル：/ After this skill, you can use:

1. **json-to-models** — PlantUML 図の再生成、Eclipse Papyrus 用 XMI 作成、Markdown ドキュメント生成 / Regenerate PlantUML diagrams, create XMI for Eclipse Papyrus, generate Markdown documentation
2. **usecase-to-sequence-v1** — ユースケースからシーケンス図を生成（ユースケース定義が必要）/ Generate sequence diagrams from use cases (requires use case definitions)
3. **class-to-statemachine-v1** — エンティティのステートマシンを生成（ステータス属性を持つエンティティが必要）/ Generate state machines for entities (requires entities with status attributes)
4. **model-validator-v1** — モデルの一貫性を検証し、ビジネスルールをチェック / Validate model consistency and check business rules
5. **usecase-to-code-v1** — フルスタックアプリケーションを生成（完全なワークフローコンテキストが必要）/ Generate full-stack application (requires complete workflow context)

---

## 制限事項 / Limitations

1. **手書き図 / Handwritten diagrams** — 精度は手書きの明瞭さに依存します / Accuracy depends on handwriting clarity
2. **複雑なレイアウト / Complex layouts** — 交差する線が抽出を混乱させる場合があります / Crossing lines may confuse extraction
3. **独自記法 / Custom notation** — 非標準 UML は解釈が必要です / Non-standard UML requires interpretation
4. **OCR の限界 / OCR limits** — 非常に小さなテキストは読み取れない場合があります / Very small text may not be readable
5. **色への依存なし / No color dependency** — 色ではなく構造的要素に依存します / Relies on structural elements, not colors

---

## 成功指標 / Success Metrics

- **抽出精度 / Extraction accuracy** — デジタル図で 95% 以上 / 95%+ for digital diagrams
- **時間節約 / Time saved** — 手動 JSON 作成と比べて 80% 削減 / 80% vs. manual JSON writing
- **ワークフロー統合 / Workflow integration** — uml-workflow-v3 パイプラインにシームレスに追加 / Seamless addition to uml-workflow-v3 pipeline

---

## 今後の拡張予定 / Future Enhancements

- [ ] XMI 直接インポートのサポート / Support XMI import directly
- [ ] 複数図のバッチ処理 / Batch processing multiple diagrams
- [ ] インタラクティブな修正インターフェース / Interactive correction interface
- [ ] 一般的なミスの自動修正 / Auto-fix common mistakes

---

## まとめ / Summary

このスキルはビジュアルモデリングツールと自動コード生成の橋渡しをします： / This skill bridges the gap between visual modeling tools and automated code generation:

- **ビジュアルファーストのワークフロー / Visual-first workflow** — 好みのツールで設計 / Design in your preferred tool
- **柔軟性 / Flexibility** — 自動生成と手動修正を組み合わせ / Mix auto-generation with manual refinement
- **統合 / Integration** — uml-workflow-v3 パイプラインにシームレスに組み込み / Seamless uml-workflow-v3 integration
- **生産性 / Productivity** — 手動 JSON 作成の 10 倍高速 / 10× faster than manual JSON creation
