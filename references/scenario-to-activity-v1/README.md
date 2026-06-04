# scenario-to-activity-v1 / シナリオ→アクティビティ図生成

## 概要 / Overview

業務シナリオからUMLアクティビティ図を生成するスキルです。 / A skill that generates UML activity diagrams from business scenarios.

## 主な機能 / Key Features

- 業務概要と業務シナリオから自動的にアクティビティ図を生成 / Automatically generates activity diagrams from a business overview and scenario
- 一時的なドメインモデルを内部で管理 / Manages a temporary domain model internally
- クラス図への依存なし（独立して実行可能）/ No dependency on a class diagram (can run independently)

## 出力成果物 / Output Artifacts

1. **PlantUML Activity Diagram** (`{project}_activity.puml`) — アクティビティ図 / Activity diagram
2. **Business Scenario Document** (`{project}_business-scenario.md`) — 業務シナリオ文書 / Business scenario document
3. **Activity Data JSON** (`{project}_activity-data.json`) — 構造化データ / Structured data
4. **XMI Model** (`{project}_activity-model.xmi`) — UML 2.5.1標準形式 / UML 2.5.1 standard format

## 使用方法 / Usage

```
ユーザー / User: 「このシナリオからアクティビティ図を作成してください」
                "Please create an activity diagram from this scenario"

業務概要 / Business overview:
B2B卸売業向けの受注管理システム / Order management system for B2B wholesale

業務シナリオ / Business scenario:
1. 顧客が商品カタログを確認する / Customer checks the product catalog
2. 顧客が電話で注文する / Customer places an order by phone
...
```

## 入力要件 / Input Requirements

### 必須 / Required

- 業務概要 / Business overview
- 業務シナリオ / Business scenario

### オプション（推奨）/ Optional (Recommended)

- ビジネスルール / Business rules
- 用語集 / Glossary
- ステークホルダー情報 / Stakeholder information
- 非機能要件 / Non-functional requirements

## ワークフローでの位置 / Position in Workflow

```
Step 1: scenario-to-activity-v1 ← このスキル / This skill
  ↓
Step 2: activity-to-usecase-v1
  ↓
Step 3: usecase-to-class-v1
  ↓
Step 8: usecase-to-code-v1
```

## バージョン / Version History

- **v1.0** (2026-01-24)
  - XMI出力機能追加 / Added XMI output
  - 業務シナリオ文書生成 / Business scenario document generation
  - アクティビティデータJSON生成 / Activity data JSON generation
  - 構造化されたドメインモデル管理 / Structured domain model management

## 標準準拠 / Standards Compliance

- UML 2.5.1（OMG標準 / OMG standard）
- XMI 2.5.1（モデル交換形式 / Model interchange format）
- Eclipse Modeling Framework互換 / Eclipse Modeling Framework compatible
