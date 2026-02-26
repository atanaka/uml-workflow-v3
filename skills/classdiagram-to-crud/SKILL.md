---
name: classdiagram-to-crud
description: Generate CRUD HTML fragments (Create/Read/Update/Delete) from UML class diagrams. Supports PlantUML, draw.io, XMI, and image inputs.
---

# Class Diagram to CRUD HTML Generator

UMLクラス図を入力として、各クラスにつきCRUD（Create / Read / Update / Delete）用のHTML画面を自動生成する。

## Overview

このスキルは、クラス図に定義されたエンティティの情報（属性名、型、関連）を解析し、各エンティティにつき4つの**HTMLフラグメント**を生成する。

> **フラグメントとは**: `<!DOCTYPE html>` / `<html>` / `<head>` / `<body>` を含まない、単一ルート要素のみのHTMLファイル。crud-composerなどの合成ツールが直接読み込める形式であり、インラインJSイベントハンドラ（onclick等）は使用しない。

**対応する入力形式:**
- PlantUML (.puml)
- draw.io / diagrams.net (.drawio, .xml)
- XMI (.xmi)
- 画像 (PNG, JPEG, PDF) — OCR/目視解析
- テキスト記述（自然言語やマークダウン）
- domain-model.json（uml-workflow 系スキルの出力）

**生成物:**
- 各クラスにつき4つのHTMLファイル
- ファイル名規則: `{クラス名を小文字}_{操作}.html`
  - `x_create.html` — 新規登録フォーム
  - `x_read.html` — 一覧・検索テーブル
  - `x_update.html` — 編集フォーム
  - `x_delete.html` — 削除確認画面

---

## Position in Workflow

```
クラス図（任意の形式）
  ↓ 入力
classdiagram-to-crud ← YOU ARE HERE
  ↓ 出力
{class}_create.html
{class}_read.html
{class}_update.html
{class}_delete.html
```

このスキルは単独でも使用可能。uml-workflow 系のワークフロー内では、
`usecase-to-class-v1` の出力（domain-model.json）を入力として利用できる。

---

## Input

### Required

クラス図の情報。以下のいずれかの形式で提供される:

1. **PlantUML**: `.puml` ファイル
2. **draw.io**: `.drawio` / `.xml` ファイル
3. **XMI**: `.xmi` ファイル
4. **画像**: PNG / JPEG / PDF（クラス図のスクリーンショットや手書き）
5. **テキスト**: 自然言語やマークダウンによるクラス定義
6. **domain-model.json**: uml-workflow 系スキルの出力 JSON

### 入力から抽出する情報

各クラスについて以下を抽出する:

| 項目 | 用途 |
|------|------|
| クラス名（英語） | ファイル名、タイトル |
| クラス名（日本語、あれば） | 画面表示タイトル |
| 属性名 | フォームフィールド、テーブルカラム |
| 属性の型 | 入力コンポーネントの選定 |
| 必須/任意 | バリデーション表示 |
| 主キー (PK) | 読取専用フィールド、自動採番表示 |
| 外部キー (FK) | セレクトボックス（関連エンティティ選択） |
| 列挙型 (Enum) | セレクトボックス / ステータスバッジ |
| クラス間の関連 | FK参照先、関連データの警告表示 |

---

## Output

### ファイル命名規則

クラス名を**小文字**に変換し、`_create`, `_read`, `_update`, `_delete` を付与する。

```
例: Customer, Order, OrderItem の場合

customer_create.html
customer_read.html
customer_update.html
customer_delete.html
order_create.html
order_read.html
order_update.html
order_delete.html
orderitem_create.html
orderitem_read.html
orderitem_update.html
orderitem_delete.html
```

### 各画面の構成

#### Create（新規登録）

- フォーム形式
- PK属性 → `readonly` + 「自動採番」表示
- FK属性 → `<select>` でサンプル選択肢を表示
- Enum属性 → `<select>` で列挙値を表示
- 必須属性 → ラベルに `*` マーク
- 型に応じた入力コンポーネント（後述）
- ボタン: 「登録する」(primary) + 「キャンセル」(outline)

#### Read（参照）

- 検索バー（テキスト入力 + 検索ボタン）を上部に配置（`class="search-bar"`）
- Enum属性がある場合 → 検索バー横にフィルタ用セレクトボックスを追加
- 検索バーの下に詳細ビュー（`class="detail-view" id="detail-view"`）を配置
- Update と同じ項目・同じレイアウトで全フィールドを表示
- 全フィールドは `readonly` 属性を付与し、背景色 `--c-bg-readonly` で参照専用であることを明示
- `<select>` は `<input type="text" readonly>` に置き換え（ドロップダウンが開かないように）
- `<textarea>` は `readonly` + `resize:none` で表示
- 必須マーク（`*`）は表示しない
- ボタン行（submitボタン）は生成しない

#### Update（編集）

- Create と同様のフォーム構成
- PK属性 → `readonly`（変更不可）
- FK属性（親への参照） → 文脈に応じて `readonly` または `<select>`
- 各フィールドにサンプル値をプリセット
- ボタン: 「更新する」(primary) + 「キャンセル」(outline)

#### Delete（削除確認）

- 警告メッセージ（赤背景のアラート）
  - 「この操作は元に戻せません」
  - 関連データがある場合はその影響を明記
- 対象レコードの詳細をラベル・値のグリッドで表示
- ボタン: 「削除を実行」(danger) + 「キャンセル」(outline)

---

## 型からUIコンポーネントへのマッピング

| 属性の型 | Create/Update コンポーネント | Read 表示 |
|----------|---------------------------|-----------|
| String | `<input type="text">` | テキスト |
| Integer | `<input type="number">` | 数値 |
| Decimal / Money | `<input type="number" step="1">` | 通貨フォーマット（右寄せ） |
| Boolean | `<select>` (はい/いいえ) | ○ / × |
| Date | `<input type="date">` | 日付フォーマット |
| DateTime | `<input type="datetime-local">` | 日時フォーマット |
| Text (長文) | `<textarea>` | テキスト |
| Email | `<input type="email">` | テキスト |
| Phone | `<input type="tel">` | テキスト |
| URL | `<input type="url">` | リンク |
| Enum | `<select>` | ステータスバッジ |
| FK (外部キー) | `<select>` (関連エンティティ) | テキスト（参照先名称） |
| PK (主キー) | `<input readonly>` | テキスト |

---

## HTML生成ルール

### フラグメント構造（必須）

各HTMLファイルは**単一のルート要素のみ**を含むフラグメントとする。
`<!DOCTYPE html>` / `<html>` / `<head>` / `<body>` タグは**絶対に含めない**。

| 操作 | ルート要素 | id属性 |
|------|-----------|--------|
| Create | `<form class="crud-form" id="{class}-create-form">` | `{class}-create-form` |
| Read   | `<div class="crud-read" id="{class}-read">` | `{class}-read` |
| Update | `<form class="crud-form" id="{class}-update-form">` | `{class}-update-form` |
| Delete | `<div class="crud-delete" id="{class}-delete">` | `{class}-delete` |

```html
<!-- Create/Update: formがルート要素 -->
<form class="crud-form" id="person-create-form" style="--c-accent:#1a56db; ...">
  ...フォーム内容...
</form>

<!-- Read/Delete: divがルート要素（内部にformを含んでよい） -->
<div class="crud-read" id="person-read" style="--c-accent:#0f766e; ...">
  ...内容...
</div>
```

### インラインJS禁止

`onclick`、`onchange`、`onsubmit`、`onload`、`onfocus`、`onblur` などの
インラインJSイベントハンドラは**使用禁止**。

- キャンセルボタン → `type="button"` のみ（JS不要）
- 削除確認 → `data-confirm="..."` 属性で代替
- 検索ボタン → `type="button" id="search-btn"` のみ

### スタイル方針

外部CSSファイルやグローバルCSSクラスには依存せず、**インラインstyle属性**と
**CSS変数**（`var(--c-accent)` 等）のみでスタイルを完結させる。
CSS変数はルート要素の `style` 属性内で定義する。

操作種別ごとのアクセントカラー:

| 操作 | `--c-accent` |
|------|-------------|
| Create | `#1a56db`（青） |
| Read   | `#0f766e`（緑） |
| Update | `#b45309`（琥珀） |
| Delete | `#dc2626`（赤） |

共通のCSS変数セット（ルート要素のstyle属性に埋め込む）:

```
--c-accent: {操作色};
--c-accent-hover: {操作色の暗め};
--c-surface: #ffffff;
--c-border: #d4d9e1;
--c-text: #1c2536;
--c-text-sub: #5a6578;
--c-bg-input: #f6f7f9;
--c-bg-readonly: #f0f1f4;
font-family: 'Helvetica Neue', 'Noto Sans JP', sans-serif;
color: var(--c-text);
background: var(--c-surface);
border: 1px solid var(--c-border);
border-radius: 10px;
padding: 28px 32px;
```

---

## Execution Steps

### Step 1: 入力の解析

1. 入力形式を判別する
2. クラス定義を抽出する:
   - クラス名（英語、日本語）
   - 属性一覧（名前、型、PK/FK、必須/任意）
   - 列挙型の定義
   - クラス間の関連（1対多、多対多など）

### Step 2: エンティティ分類

各クラスを以下のように分類する（Read画面のサンプルデータ生成に影響）:

| 分類 | 特徴 | 例 |
|------|------|----|
| マスタ | 参照データ、比較的静的 | Product, Category, Customer |
| トランザクション | 業務イベント、ステータス属性あり | Order, Payment, Shipment |
| サブエンティティ | 親に従属、親のFK必須 | OrderItem, Address |

### Step 3: HTML生成

各クラスについて4つのHTMLファイルを生成する。

**生成時のルール:**

1. **PK属性**: Create では `readonly` + 「(自動採番)」、Update/Read/Delete では `readonly` + 実値
2. **FK属性**: Create/Update では `<select>` に参照先のサンプルデータを選択肢として表示、Read では `<input type="text" readonly>` で表示
3. **Enum属性**: Create/Update では `<select>` に列挙値を表示、Read では `<input type="text" readonly>` で表示（ラベル文字列）
4. **必須属性**: Create/Update のラベルに `<span style="color:#dc2626;">*</span>` を付与、`required` 属性を追加。Read では必須マークを表示しない
5. **Read のフィールド**: 全フィールドに `readonly` を付与、背景色は `--c-bg-readonly`、`cursor:default`。textareaは `resize:none`
6. **サンプルデータ**: Update/Read/Delete 画面のフィールドにリアルなサンプル値をプリセット（日本語の人名・日付等）
7. **関連データの警告**: Delete 画面で子エンティティがある場合、影響範囲を警告ボックスに明記
8. **submitボタン**: Read 画面にはボタン行を生成しない
9. **インラインJS禁止**: onclick 等のイベントハンドラは使用しない。削除確認ボタンは `data-confirm="..."` 属性で代替

### Step 4: 出力

1. 全HTMLファイルを生成
2. ZIPにまとめて `/mnt/user-data/outputs/` に配置
3. 代表的な画面（例: Read画面）をプレビュー用に個別配置
4. `present_files` ツールでユーザーに提示

---

## Language Support

### 画面ラベルの言語

- 入力のクラス図に日本語名がある場合 → 日本語をタイトル・ラベルに使用
- 日本語名がない場合 → 英語のクラス名・属性名をそのまま使用
- `domain-model.json` の `japanese_name` フィールドがある場合はそれを優先

### ボタンラベル

| 操作 | 日本語 | English |
|------|--------|---------|
| Create submit | 登録する | Register |
| Update submit | 更新する | Update |
| Delete submit | 削除を実行 | Delete |
| Cancel | キャンセル | Cancel |
| Search | 検索 | Search |

言語は入力のクラス図の言語設定、または `domain-model.json` の `metadata.language` に従う。
デフォルトは日本語。

---

## Examples

### 入力例: テキスト記述

```
Customer: customerId(PK), name, email, phone, address
Order: orderId(PK), orderDate, totalAmount, status(Enum: PENDING/CONFIRMED/SHIPPED), customerId(FK→Customer)
OrderItem: orderItemId(PK), orderId(FK→Order), productName, quantity, unitPrice
```

### 出力ファイル

```
customer_create.html  — 顧客の新規登録フォーム
customer_read.html    — 顧客の一覧テーブル（4件のサンプルデータ）
customer_update.html  — 顧客の編集フォーム（CUST-001のデータ）
customer_delete.html  — 顧客の削除確認（関連受注データの警告付き）
order_create.html     — 受注の新規登録（顧客セレクト + ステータスセレクト）
order_read.html       — 受注一覧（ステータスフィルタ + ステータスバッジ表示）
order_update.html     — 受注の編集
order_delete.html     — 受注の削除確認（関連明細データの警告付き）
orderitem_create.html — 明細の新規登録（受注セレクト）
orderitem_read.html   — 明細一覧（小計の計算列あり）
orderitem_update.html — 明細の編集（受注IDはreadonly）
orderitem_delete.html — 明細の削除確認（受注合計への影響警告）
```

---

## Best Practices

1. **フラグメント厳守**: ルート要素は必ず1つ。DOCTYPE/html/head/bodyは絶対に出力しない
2. **インラインJS禁止**: onclick等のイベントハンドラを一切使用しない。代わりに `type="button"` や `data-confirm` 属性を使う
3. **スタイルはインライン完結**: 外部CSS/クラスに依存せず、style属性とCSS変数のみでスタイルを定義する
4. **サンプルデータはリアルに**: 日本語の人名・住所・商品名を使い、実際の業務データに近い内容にする
5. **FK参照は分かりやすく**: セレクトボックスには `ID : 名前` の形式で表示する
6. **Delete の警告は具体的に**: 「N件の関連データも削除されます」など影響範囲を明示する
7. **Read は参照専用を徹底**: readonly + カーソルdefault + ボタンなし で編集不可を明示する

---

## Version History

- **v1.1** (2026-02-22): フラグメント出力に変更
  - フルHTML文書（DOCTYPE/html/head/body）→ 単一ルート要素フラグメントに変更
  - インラインJSイベントハンドラ（onclick等）を全廃
  - Read画面をデータテーブル → 検索バー＋参照詳細ビュー（readonly）に変更
  - crud-composerなど合成ツールとの互換性を確保
  - CSS変数をルート要素のstyle属性内で定義するインライン完結スタイルに変更

- **v1.0** (2026-02-22): Initial version
  - クラス図からCRUD HTML自動生成
  - PlantUML / draw.io / XMI / 画像 / テキスト / JSON 入力対応
  - スタンドアロンHTML（サイドバーなし、コンテンツのみ）
  - 日本語/英語ラベル対応
  - 型→UIコンポーネント自動マッピング
