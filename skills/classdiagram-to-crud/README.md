# classdiagram-to-crud / クラス図→CRUD HTML生成

**UML Workflow v3 ヘルパースキル / Helper Skill for UML Workflow v3**

UMLクラス図を入力として、各エンティティの CRUD 操作用 HTML フラグメントを自動生成します。  
UML クラス図を入力として、各エンティティの CRUD 操作用 HTML フラグメントを自動生成します。 / Generates CRUD operation HTML fragments for each entity from a UML class diagram.

**使い方 / Usage:**
```
「{エンティティ名}のCRUD画面を生成してください」
"Generate CRUD screens for {entity name}"

「domain-model.jsonからCRUD HTMLを生成して」
"Generate CRUD HTML from domain-model.json"
```

---

## 概要 / Overview

クラス図（PlantUML・draw.io・XMI・画像・JSON）を入力として、各クラスにつき以下の4つのHTMLフラグメントを生成します。

クラス図（PlantUML・draw.io・XMI・画像・JSON）を入力として、各クラスにつき以下の 4 つの HTML フラグメントを生成します。 / Takes a class diagram (PlantUML, draw.io, XMI, image, or JSON) as input and generates the following 4 HTML fragments for each class.

| ファイル / File | 用途 / Purpose |
|---------------|--------------|
| `{class}_create.html` | 新規登録フォーム / Create form |
| `{class}_read.html` | 一覧・検索テーブル / List / search table |
| `{class}_update.html` | 編集フォーム / Edit form |
| `{class}_delete.html` | 削除確認画面 / Delete confirmation |

> **フラグメントとは / About HTML Fragments**: `<!DOCTYPE html>` / `<html>` / `<head>` / `<body>` を含まない、単一ルート要素のみのHTMLファイル。crud-composer などの合成ツールが直接読み込める形式です。  
> `<!DOCTYPE html>` / `<html>` / `<head>` / `<body>` を含まない単一ルート要素のみの HTML ファイル。crud-composer などの合成ツールが直接読み込める形式です。 / HTML files consisting of a single root element only. Directly loadable by composition tools like crud-composer.

---

## 対応入力形式 / Supported Input Formats

| 形式 / Format | 例 / Example |
|-------------|-------------|
| PlantUML | `.puml` ファイル / file |
| draw.io | `.drawio` / `.xml` ファイル / file |
| XMI | `.xmi` ファイル / file |
| 画像 / Image | PNG, JPEG, PDF |
| JSON | `domain-model.json`（uml-workflow-v3 出力）|
| テキスト / Text | 自然言語やMarkdownでの記述 / Natural language or Markdown |

---

## ワークフロー内の位置 / Position in Workflow

```
uml-workflow-v3 Step 3
  ↓ 出力 / output
domain-model.json
  ↓ 入力 / input
classdiagram-to-crud  ← このスキル / This skill
  ↓ 出力 / output
{class}_create.html
{class}_read.html
{class}_update.html
{class}_delete.html
```

このスキルは単独でも使用できます。uml-workflow-v3 の Step 8（コード生成）とは独立しており、プロトタイプや画面設計の確認用途に最適です。

このスキルは単独でも使用できます。uml-workflow-v3 の Step 8（コード生成）とは独立しており、プロトタイプや画面設計の確認用途に最適です。 / This skill can also be used standalone. It is independent of uml-workflow-v3 Step 8 (code generation) and is ideal for prototyping and UI design review.

---

## 使用例 / Usage Examples

### 例1 / Example 1: domain-model.json から生成 / Generate from domain-model.json

```
「domain-model.jsonをもとに、全エンティティのCRUD HTMLを生成してください」
"Generate CRUD HTML for all entities from domain-model.json"
```

### 例2 / Example 2: 特定エンティティのみ / Specific entities only

```
「ExpenseReport と User のCRUD画面だけ生成してください」
"Generate CRUD screens for ExpenseReport and User only"
```

### 例3 / Example 3: PlantUML から直接生成 / Generate directly from PlantUML

```
「以下のPlantUMLクラス図からCRUD HTMLを生成してください：[PlantUMLを貼り付け]」
"Generate CRUD HTML from this PlantUML class diagram: [paste PlantUML]"
```

---

## 出力の特徴 / Output Characteristics

- **フラグメント形式 / Fragment format** — `<body>` タグなし、単一ルート要素 / No `<body>` tag, single root element
- **インラインJS禁止 / No inline JS** — `onclick` などのインラインイベントハンドラを使わない / No inline event handlers like `onclick`
- **言語対応 / Language support** — ラベルを日本語または英語で生成 / Labels in Japanese or English
- **型マッピング / Type mapping** — JSON型に対応したHTMLコンポーネント（テキスト、日付、数値、選択肢等）/ HTML components mapped from JSON types (text, date, number, select, etc.)

---

## 関連スキル / Related Skills

| スキル / Skill | 関係 / Relation |
|--------------|--------------|
| `uml-workflow-v3` | Step 3の出力（domain-model.json）を本スキルへの入力として利用 / Step 3 output feeds into this skill |
| `json-to-models` | domain-model.jsonの修正後にPlantUMLを再生成する / Regenerates PlantUML after editing domain-model.json |
| `classdiagram-image-to-json` | 画像のクラス図をJSONに変換してから本スキルに渡す / Converts image class diagram to JSON, then feeds this skill |
