# activity-to-usecase-v1

## 概要

UMLアクティビティ図からユースケースを抽出するスキルです。

## 主な機能

- アクティビティ図を解析してユースケースを自動抽出
- **Markdown形式の詳細仕様書を自動生成** ⭐
- ドメインモデルを推論（一時的）
- ストーリーポイント見積もり
- スプリント分割

## 出力成果物

### 必須出力

1. ⭐ **Use Case Specifications (Markdown)** (`usecase-specifications/UC-{ID}_{name}.md`) - Cockburn形式の詳細仕様書
   - **すべてのユースケースが個別のMarkdownファイルとして生成されます**
   - 主成功シナリオ、拡張フロー、特別要件を含む
   - API操作、ストーリーポイント、トレーサビリティ情報

2. **PlantUML Use Case Diagram** (`{project}_usecase-diagram.puml`) - ユースケース図

3. **Structured JSON Output** (`{project}_usecase-output.json`) - 構造化データ（コード生成用）

### オプション出力

4. **XMI Model** (`{project}_usecase-model.xmi`) - UML 2.5.1標準形式（実行オプションで制御）

## 使用方法

```
ユーザー: 「このアクティビティ図からユースケースを抽出してください」
[アクティビティ図をアップロード: PDF/draw.io/XMI]
```

## 入力形式

### 対応ファイル形式
- PDF (アクティビティ図)
- draw.io XML
- UML 2.x XMI

### オプション入力
- 元の業務シナリオ情報（推奨）

## ワークフローでの位置

```
Step 1: scenario-to-activity-v1
  ↓
Step 2: activity-to-usecase-v1 ← このスキル
  ↓
Step 3: usecase-to-class-v1
  ↓
Step 4: usecase-to-code-v1
```

## 特徴

- **クラス図不要**: 独立して実行可能
- **ドメインモデル推論**: アクティビティ図から自動推論
- **アジャイル対応**: スプリント単位でサイジング
- **完全なドキュメント**: Cockburn形式の詳細仕様書を個別Markdownファイルとして生成 ⭐
- **常にMarkdown出力**: すべてのユースケースが必ず.md形式で出力されます

## ユースケース仕様書の構成

各Markdownファイルには以下が含まれます：

1. ユースケース概要（ID、名称、主アクター、ストーリーポイント等）
2. ステークホルダーと関心事
3. 事前条件・事後条件
4. 主成功シナリオ（ステップバイステップ）
5. 拡張フロー（代替シナリオ・エラーハンドリング）
6. 特別な要求事項（性能、セキュリティ等）
7. 技術・データのバリエーション
8. 発生頻度
9. 未解決事項（あれば）
10. 関連ユースケース
11. トレーサビリティ情報
12. API操作（REST エンドポイント）

## バージョン

- **v1.1** (2026-01-24)
  - ⭐ **Markdown形式のユースケース仕様書を常に出力**
  - 個別の.mdファイルとして各ユースケースを生成
  - USECASE_INDEX.md の生成（オプション）
  - より詳細なCockburn形式テンプレート

- **v1.0** (2026-01-24)
  - XMI出力機能追加
  - ユースケース図生成
  - Cockburn形式仕様書生成
  - 推論ドメインモデル管理

## 標準準拠

- UML 2.5.1 (OMG)
- XMI 2.5.1
- Eclipse Modeling Framework互換
