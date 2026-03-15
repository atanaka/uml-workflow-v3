# usecase-to-class-v1 / ユースケース→クラス図生成

## 概要 / Overview

ユースケース定義から正式なUMLクラス図を生成するスキルです。 / A skill that generates formal UML class diagrams from use case definitions.

## 主な機能 / Key Features

- ユースケースと元の業務要件を統合 / Integrates use cases with original business requirements
- 推論ドメインモデルを正式化 / Formalizes the inferred domain model
- 完全な属性・リレーション・メソッド定義 / Complete attribute, relationship, and method definitions
- Domain-Driven Design対応 / Domain-Driven Design support

## 出力成果物 / Output Artifacts

1. **PlantUML Class Diagram** (`{project}_class.puml`) — クラス図 / Class diagram
2. **Domain Model JSON** (`{project}_domain-model.json`) — ドメインモデル構造化データ / Structured domain model data
3. **Architecture Overview** (`{project}_architecture-overview.md`) — アーキテクチャ概要文書 / Architecture overview document
4. **XMI Model** (`{project}_class-model.xmi`) — UML 2.5.1標準形式 / UML 2.5.1 standard format

## 使用方法 / Usage

```
ユーザー / User: 「このユースケースから正式なクラス図を作成してください」
                "Please create a formal class diagram from these use cases"
[usecase-output.jsonを参照 / Referencing usecase-output.json]
```

## 入力要件 / Input Requirements

### 必須 / Required

- `{project}_usecase-output.json` — activity-to-usecase-v1の出力 / Output of activity-to-usecase-v1

### オプション（推奨）/ Optional (Recommended)

- 元の業務シナリオ情報 / Original business scenario information
- ビジネスルール / Business rules
- 用語集 / Glossary

## ワークフローでの位置 / Position in Workflow

```
Step 1: scenario-to-activity-v1
  ↓
Step 2: activity-to-usecase-v1
  ↓
Step 3: usecase-to-class-v1 ← このスキル / This skill
  ↓
Step 8: usecase-to-code-v1
```

## 特徴 / Characteristics

- **正式なドメインモデル**: コード生成の基盤となる権威あるモデル / **Formal domain model**: The authoritative model underlying code generation
- **完全な定義**: すべての属性・型・リレーションを明示 / **Complete definitions**: All attributes, types, and relationships are explicit
- **DDD対応**: Aggregate、Repository、Value Objectをサポート / **DDD support**: Supports Aggregate, Repository, and Value Object patterns
- **包括的ドキュメント**: アーキテクチャ概要を自動生成 / **Comprehensive documentation**: Architecture overview auto-generated

## 生成されるドメインモデル / Generated Domain Model

- エンティティ（完全な属性定義）/ Entities (complete attribute definitions)
- 列挙型（ステータス等）/ Enumerations (statuses, etc.)
- 値オブジェクト / Value objects
- リレーション（多重度含む）/ Relationships (including multiplicity)
- ビジネスメソッド / Business methods
- 集約（Aggregate）定義 / Aggregate definitions

## バージョン / Version History

- **v1.0** (2026-01-24)
  - XMI出力機能追加 / Added XMI output
  - ドメインモデルJSON生成 / Domain model JSON generation
  - アーキテクチャ概要文書生成 / Architecture overview document generation
  - 完全な型定義とリレーション / Complete type definitions and relationships

## 標準準拠 / Standards Compliance

- UML 2.5.1（OMG標準 / OMG standard）
- XMI 2.5.1（モデル交換形式 / Model interchange format）
- Eclipse Modeling Framework互換 / Eclipse Modeling Framework compatible
- Domain-Driven Design原則 / Domain-Driven Design principles
