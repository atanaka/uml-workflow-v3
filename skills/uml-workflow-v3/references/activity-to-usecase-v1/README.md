# activity-to-usecase-v1 / アクティビティ図→ユースケース変換

## 概要 / Overview

UMLアクティビティ図からユースケースを抽出するスキルです。 / A skill that extracts use cases from UML activity diagrams.

## 主な機能 / Key Features

- アクティビティ図を解析してユースケースを自動抽出 / Automatically extracts use cases by analyzing activity diagrams
- **Markdown形式の詳細仕様書を自動生成** ⭐ / **Auto-generates detailed specs in Markdown format** ⭐
- ドメインモデルを推論（一時的）/ Infers a temporary domain model
- ストーリーポイント見積もり / Story point estimation
- スプリント分割 / Sprint-based sizing

## 出力成果物 / Output Artifacts

### 必須出力 / Required Outputs

1. ⭐ **Use Case Specifications (Markdown)** (`usecase-specifications/UC-{ID}_{name}.md`) — Cockburn形式の詳細仕様書 / Cockburn-format detailed spec
   - **すべてのユースケースが個別のMarkdownファイルとして生成されます** / **Each use case is generated as an individual Markdown file**
   - 主成功シナリオ、拡張フロー、特別要件を含む / Includes main success scenario, extension flows, and special requirements
   - API操作、ストーリーポイント、トレーサビリティ情報 / API operations, story points, and traceability info

2. **PlantUML Use Case Diagram** (`{project}_usecase-diagram.puml`) — ユースケース図 / Use case diagram

3. **Structured JSON Output** (`{project}_usecase-output.json`) — 構造化データ（コード生成用）/ Structured data for code generation

### オプション出力 / Optional Outputs

4. **XMI Model** (`{project}_usecase-model.xmi`) — UML 2.5.1標準形式（実行オプションで制御）/ UML 2.5.1 standard format (controlled via execution option)

## 使用方法 / Usage

```
ユーザー / User: 「このアクティビティ図からユースケースを抽出してください」
                "Please extract use cases from this activity diagram"
[アクティビティ図をアップロード / Upload activity diagram: PDF / draw.io / XMI]
```

## 入力形式 / Input Format

### 対応ファイル形式 / Supported File Formats

- PDF（アクティビティ図 / activity diagram）
- draw.io XML（ダイアグラム形式 / diagram format）
- UML 2.x XMI（モデル形式 / model format）

### オプション入力 / Optional Input

- 元の業務シナリオ情報（推奨）/ Original business scenario information (recommended)

## ワークフローでの位置 / Position in Workflow

```
Step 1: scenario-to-activity-v1
  ↓
Step 2: activity-to-usecase-v1 ← このスキル / This skill
  ↓
Step 3: usecase-to-class-v1
  ↓
Step 8: usecase-to-code-v1
```

## 特徴 / Characteristics

- **クラス図不要**: 独立して実行可能 / **No class diagram needed**: Runs independently
- **ドメインモデル推論**: アクティビティ図から自動推論 / **Domain model inference**: Auto-inferred from the activity diagram
- **アジャイル対応**: スプリント単位でサイジング / **Agile-ready**: Sized by sprint
- **完全なドキュメント**: Cockburn形式の詳細仕様書を個別Markdownファイルとして生成 ⭐ / **Complete documentation**: Detailed Cockburn-format specs generated as individual Markdown files ⭐
- **常にMarkdown出力**: すべてのユースケースが必ず.md形式で出力されます / **Always Markdown output**: Every use case is always emitted as a .md file

## ユースケース仕様書の構成 / Use Case Spec Structure

各Markdownファイルには以下が含まれます：/ Each Markdown file contains the following:

1. ユースケース概要（ID、名称、主アクター、ストーリーポイント等）/ Use case overview (ID, name, primary actor, story points, etc.)
2. ステークホルダーと関心事 / Stakeholders and interests
3. 事前条件・事後条件 / Pre- and postconditions
4. 主成功シナリオ（ステップバイステップ）/ Main success scenario (step-by-step)
5. 拡張フロー（代替シナリオ・エラーハンドリング）/ Extension flows (alternative scenarios & error handling)
6. 特別な要求事項（性能、セキュリティ等）/ Special requirements (performance, security, etc.)
7. 技術・データのバリエーション / Technology and data variations
8. 発生頻度 / Frequency of occurrence
9. 未解決事項（あれば）/ Open issues (if any)
10. 関連ユースケース / Related use cases
11. トレーサビリティ情報 / Traceability information
12. API操作（REST エンドポイント）/ API operations (REST endpoints)

## バージョン / Version History

- **v1.1** (2026-01-24)
  - ⭐ **Markdown形式のユースケース仕様書を常に出力 / Always outputs Markdown use case specs**
  - 個別の.mdファイルとして各ユースケースを生成 / Each use case generated as an individual .md file
  - USECASE_INDEX.md の生成（オプション）/ USECASE_INDEX.md generation (optional)
  - より詳細なCockburn形式テンプレート / More detailed Cockburn-format template

- **v1.0** (2026-01-24)
  - XMI出力機能追加 / Added XMI output
  - ユースケース図生成 / Use case diagram generation
  - Cockburn形式仕様書生成 / Cockburn-format spec generation
  - 推論ドメインモデル管理 / Inferred domain model management

## 標準準拠 / Standards Compliance

- UML 2.5.1（OMG標準 / OMG standard）
- XMI 2.5.1（モデル交換形式 / Model interchange format）
- Eclipse Modeling Framework互換 / Eclipse Modeling Framework compatible
