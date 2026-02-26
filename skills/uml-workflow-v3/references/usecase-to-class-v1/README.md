# usecase-to-class-v1

## 概要 / Overview

ユースケース定義から正式なUMLクラス図を生成するスキルです。

## 主な機能 / Key Features

- ユースケースと元の業務要件を統合
- 推論ドメインモデルを正式化
- 完全な属性・リレーション・メソッド定義
- Domain-Driven Design対応

## 出力成果物 / Output Artifacts

1. **PlantUML Class Diagram** (`{project}_class.puml`) - クラス図
2. **Domain Model JSON** (`{project}_domain-model.json`) - ドメインモデル構造化データ
3. **Architecture Overview** (`{project}_architecture-overview.md`) - アーキテクチャ概要文書
4. **XMI Model** (`{project}_class-model.xmi`) - UML 2.5.1標準形式

## 使用方法 / Usage

```
ユーザー: 「このユースケースから正式なクラス図を作成してください」
[usecase-output.jsonを参照]
```

## 入力要件 / Input Requirements

### 必須
- `{project}_usecase-output.json` (activity-to-usecase-v1の出力)

### オプション（推奨）
- 元の業務シナリオ情報
- ビジネスルール
- 用語集

## ワークフローでの位置 / Position in Workflow

```
Step 1: scenario-to-activity-v1
  ↓
Step 2: activity-to-usecase-v1
  ↓
Step 3: usecase-to-class-v1 ← このスキル
  ↓
Step 4: usecase-to-code-v1
```

## 特徴 / Characteristics

- **正式なドメインモデル**: コード生成の基盤となる権威あるモデル
- **完全な定義**: すべての属性・型・リレーションを明示
- **DDD対応**: Aggregate、Repository、Value Objectをサポート
- **包括的ドキュメント**: アーキテクチャ概要を自動生成

## 生成されるドメインモデル / Generated Domain Model

- エンティティ（完全な属性定義）
- 列挙型（ステータス等）
- 値オブジェクト
- リレーション（多重度含む）
- ビジネスメソッド
- 集約（Aggregate）定義

## バージョン / Version History

- **v1.0** (2026-01-24)
  - XMI出力機能追加
  - ドメインモデルJSON生成
  - アーキテクチャ概要文書生成
  - 完全な型定義とリレーション

## 標準準拠 / Standards Compliance

- UML 2.5.1 (OMG)
- XMI 2.5.1
- Eclipse Modeling Framework互換
- Domain-Driven Design原則
