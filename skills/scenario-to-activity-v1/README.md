# scenario-to-activity-v1

## 概要

業務シナリオからUMLアクティビティ図を生成するスキルです。

## 主な機能

- 業務概要と業務シナリオから自動的にアクティビティ図を生成
- 一時的なドメインモデルを内部で管理
- クラス図への依存なし（独立して実行可能）

## 出力成果物

1. **PlantUML Activity Diagram** (`{project}_activity.puml`)
2. **Business Scenario Document** (`{project}_business-scenario.md`) - 業務シナリオ文書
3. **Activity Data JSON** (`{project}_activity-data.json`) - 構造化データ
4. **XMI Model** (`{project}_activity-model.xmi`) - UML 2.5.1標準形式

## 使用方法

```
ユーザー: 「このシナリオからアクティビティ図を作成してください」

業務概要:
B2B卸売業向けの受注管理システム

業務シナリオ:
1. 顧客が商品カタログを確認する
2. 顧客が電話で注文する
...
```

## 入力要件

### 必須
- 業務概要
- 業務シナリオ

### オプション（推奨）
- ビジネスルール
- 用語集
- ステークホルダー情報
- 非機能要件

## ワークフローでの位置

```
Step 1: scenario-to-activity-v1 ← このスキル
  ↓
Step 2: activity-to-usecase-v1
  ↓
Step 3: usecase-to-class-v1
  ↓
Step 4: usecase-to-code-v1
```

## バージョン

- **v1.0** (2026-01-24)
  - XMI出力機能追加
  - 業務シナリオ文書生成
  - アクティビティデータJSON生成
  - 構造化されたドメインモデル管理

## 標準準拠

- UML 2.5.1 (OMG)
- XMI 2.5.1
- Eclipse Modeling Framework互換
