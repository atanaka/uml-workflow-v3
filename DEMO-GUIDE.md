# uml-workflow-v3 デモ・利用ガイド

**対象**: 初めて uml-workflow-v3 を試す方、POC を開始する方  
**バージョン**: v3.3.0

---

## 前提条件（最初に確認）

| 必要なもの | 確認方法 |
|---|---|
| **Claude.ai Pro / Team / Enterprise プラン** | claude.ai の設定画面でプランを確認 |
| **uml-workflow-v3 スキルのインストール** | Claude.ai の「スキル」設定にアップロード済みか確認（→ [インストール手順](#インストール手順)) |

> **補足**: uml-workflow-v3 は Claude.ai の有料プランが必要です。  
> 無料プランでは Claude Skills 機能が利用できません。

---

## インストール手順

1. [GitHub リリースページ](https://github.com/YOUR_ORG/uml-workflow-v3/releases) から最新の zip をダウンロード
2. Claude.ai を開き、サイドバーの「スキル」→「スキルを追加」
3. zip ファイルをアップロード
4. 「uml-workflow-v3」が一覧に表示されれば完了

---

## 全体の流れ

```
【Phase A】1つの会話で実行               【Phase B】新しい会話で実行
┌────────────────────────────────┐      ┌────────────────────────────────┐
│ Step 1: シナリオ → アクティビティ図   │      │ Step 8: コード生成                │
│ Step 2: アクティビティ → ユースケース │ ───→ │ Step 9: テストコード生成          │
│ Step 3: ユースケース → クラス図      │      │ Step 10: トレーサビリティ          │
│ Step 4: クラス → ステートマシン図    │      └────────────────────────────────┘
│ Step 5: ユースケース → シーケンス図  │
│ Step 6: モデルバリデーション         │
│ Step 7: セキュリティ設計            │
└────────────────────────────────┘
```

> **なぜ2つの会話に分かれるのか?**  
> 10ステップすべてをコンテキスト内で処理すると Step 8 前後で上限に達します。  
> Phase A の成果物はキャッシュされるため、Phase B で自動的に引き継がれます。

---

## Phase A の実行手順

### Step 1: 会話を開始

Claude.ai の新しい会話を開き、以下のように入力します。

```
uml-workflow-v3で[プロジェクト名]のPhase Aを実行してください。

【業務シナリオ】
（ここに業務の概要を書く。箇条書きでも文章でも可）
例:
- 受注担当者が注文を受け付ける
- 在庫を確認して、不足の場合は発注する
- 出荷指示を作成し、倉庫に送る
```

### Step 2: 設定の選択

Claude から以下の質問が来ます。

| 質問 | 推奨選択 |
|---|---|
| キャッシュを使用しますか？ | **はい（推奨）** |
| 実行モードは？ | **フルワークフロー** |
| XMI ファイルを生成しますか？ | 用途に合わせて選択（後述）|
| テックスタック（バックエンド）| 用途に合わせて選択 |
| テックスタック（フロントエンド）| 用途に合わせて選択 |

#### XMI 形式の選び方 (v1.3 ⭐)

| 選択肢 | 用途 |
|---|---|
| **両形式 (デフォルト)** | OMG (Astah/EA) と EMF (Papyrus) を同時生成。完全なアーカイブを残したい場合 |
| **OMG 形式のみ** | Astah / Enterprise Architect でクラス図を編集する場合 |
| **EMF 形式のみ** | Papyrus 7.1.0 でクラス図を編集する場合 (Papyrus 検証手順は後述) |
| **生成しない** | 反復的なモデル修正中で 40% 高速化したい場合 |

### Step 3: 実行を待つ

Step 1〜7 が順番に実行されます（目安: 15〜30 分）。  
各 Step の完了後にアクティビティ図・ユースケース・クラス図などが表示されます。

### Step 4: Phase A 完了の確認

以下のメッセージが表示されれば Phase A 完了です。

```
✅ PHASE A COMPLETE
Phase A の状態（テックスタック選択）を自動保存しました。
```

成果物のファイルをダウンロードしておくことを推奨します。

---

## Phase B の実行手順（コード生成）

### Step 1: **新しい会話**を開始する

> ⚠️ 同じ会話を続けてはいけません。必ず「新しい会話」を開いてください。

### Step 2: 以下のメッセージを入力

```
uml-workflow-v3で[Phase A と同じプロジェクト名]のStep 8から再開
```

それだけです。Phase A で保存されたテックスタック設定が自動的に読み込まれます。

### Step 3: 実行を待つ

Step 8（コード生成）→ Step 9（テスト）→ Step 10（トレーサビリティ）が実行されます。  
完了後、バックエンド・フロントエンドのコードがダウンロード可能になります。

---

## 生成されるファイル一覧

| ファイル | 内容 |
|---|---|
| `{project}_activity-data.json` | アクティビティ図データ |
| `{project}_usecase-output.json` | ユースケース定義（JSON） |
| `{project}_domain-model.json` | クラス図・ドメインモデル（SSoT） |
| `{project}_class-model-omg.uml` | OMG 形式 XMI (Astah / EA 向け、XMI 生成有効時) |
| `{project}_class-model-emf.uml` | EMF 形式 XMI (Papyrus 7.1.0 向け、XMI 生成有効時) |
| `{project}_class-diagram.png` | クラス図の PNG (PlantUML / plantuml.jar / Docker サーバーで生成) |
| `{project}_validation-report.md` | モデル整合性チェックレポート |
| `{project}_security-design.md` | セキュリティ設計書 |
| `{project}_security-config.json` | セキュリティ設定（コード生成に使用） |
| `{project}/backend/` | バックエンドコード（TypeScript 等） |
| `{project}/frontend/` | フロントエンドコード（React 等） |
| `{project}_traceability-matrix.md` | 要件↔コードのトレーサビリティ |

---

## Papyrus 7.1.0 でクラス図を編集する (NEW! v3.3.0 ⭐)

`{project}_class-model-emf.uml` を Papyrus 7.1.0 で開き、生成されたクラス図を編集・拡張できます。

### 前提条件

- Papyrus-Desktop 7.1.0 以降がインストール済
- XMI 形式選択で「両形式」または「EMF のみ」を指定済（`*_class-model-emf.uml` が生成されている）

### 手順

#### Step 1: ファイルを Papyrus にインポート

1. Papyrus 起動 → ワークスペース選択
2. **File > New > Project** で空のプロジェクト作成（例: `my-uml-project`）
3. `{project}_class-model-emf.uml` を Project Explorer にインポート
   - 方法 ①: OS のファイラからドラッグ&ドロップ
   - 方法 ②: Project Explorer 右クリック > **Import > File System**
4. インポートした `.uml` を右クリック > **Open With > Papyrus Model Editor**

このとき Papyrus が自動的に `.aird` / `.di` / `.notation` の 3 ファイルを補完生成します。

#### Step 2: Model Explorer でモデル要素を確認

左ペインの **Model Explorer** ビューでツリーを展開すると、Class / Enumeration / Association などのモデル要素が表示されます。

#### Step 3: クラス図を新規作成 (⚠️ 重要)

> **必ず Model Explorer から作成すること**。メインエディタタブから新規作成すると、後述の Show Related Links が機能しません。

1. Model Explorer でモデルルート（例: `OrderManagement`）を右クリック
2. **New Diagram > Class Diagram** を選択
3. 図の名前を入力（例: `ClassDiagram_Overview`）

#### Step 4: クラスをキャンバスにドラッグ&ドロップ

Model Explorer から Class や Enumeration をクラス図キャンバスにドラッグ&ドロップで配置します。

#### Step 5: 関連線を描画する（2 通りの方法）

**方法 A: Show Related Links を使う（簡単なモデル向け）**

1. キャンバス上で **Ctrl+A**（Mac は **Cmd+A**）で全選択
2. 右クリック > **Filters > Show Related Links**
3. Generalization と Association が自動描画される

**方法 B: Model Explorer の Association をドラッグする（複雑なモデル向け）**

1. Model Explorer の `A_xxx_xxx` (Association ノード) を、クラス図上にドラッグ&ドロップ
2. 両端のクラスが既にキャンバスにあれば線が描画される

#### Step 6: abstract クラスの確認

`domain-model.json` で `"is_abstract": true` を指定したクラスは、Papyrus 上で **クラス名がイタリック体**で表示されます。

```json
{
  "entities": [
    {
      "name": "Person",
      "is_abstract": true,
      "attributes": [...]
    },
    {
      "name": "Student",
      "extends": "Person",
      "attributes": [...]
    }
  ]
}
```

上記の場合、Person はイタリック体、Student は通常体で描画されます。

### Papyrus トラブルシューティング

| 症状 | 原因 | 対処 |
|---|---|---|
| `.uml` をダブルクリックすると XML テキストが開く | XML Editor で開いている | 右クリック > **Open With > Papyrus Model Editor** |
| Show Related Links が機能しない | クラス図がメインエディタタブから作成された | Model Explorer から作り直す |
| クラス図に関連線が一部しか出ない | 両端のクラスがキャンバスにない | 関連の両端クラスを先にドロップしてから関連をドロップ |
| PrimitiveType が「???」表示 | pathmap 未解決 | **Window > Preferences > UML2 > URI Mappings** を確認 |
| abstract クラスがイタリック体にならない | `is_abstract` が JSON に未設定 | `domain-model.json` の該当 entity に `"is_abstract": true` を追加して再生成 |

---

## よくあるトラブル

### 「キャッシュが見つかりません」と表示される

**原因**: Phase A と Phase B でプロジェクト名が異なっている。  
**対処**: Phase B のメッセージで指定するプロジェクト名を Phase A と完全一致させてください。

```
✅ 正しい例: 「order-management のStep 8から再開」
❌ 間違い例: 「受注管理システムのStep 8から再開」 (Phase A では order-management と指定した場合)
```

### Step 8 でテックスタックを再度聞かれる

**原因**: Phase A 状態ファイルが見つからない（古いバージョンで実行した場合など）。  
**対処**: 以下の形式でテックスタックを明示してください。

```
uml-workflow-v3でorder-managementのStep 8から再開
テックスタック: TypeScript + Express / React + Vite + Tailwind
アーキテクチャ: monolith
テスト生成: あり
```

### コード生成後、TypeScript のコンパイルエラーが出る

**これは正常な動作の範囲内です。** 生成コードは「80% の雛形」として扱い、以下を確認してください。

1. `npm install` の実行
2. `npx tsc --noEmit` でエラー箇所を確認
3. 型エラーは手動修正（主に import パスと型定義の調整）

### 途中でエラーが発生した特定のステップからやり直したい

以下のように指定して再実行できます。

```
uml-workflow-v3でorder-managementのStep 5から再開
```

> **注意**: Step 3（クラス図）を再実行する場合は、Step 4〜7 も再実行が必要です。  
> `domain-model.json` が変わると以降のステップの整合性が崩れるためです。

---

## Claude.ai のコスト感覚

| フェーズ | 目安のトークン使用量 | Pro プランへの影響 |
|---|---|---|
| Phase A（Step 1〜7） | 約 80K トークン | 1 回あたり数分のクレジット消費 |
| Phase B（Step 8〜10） | 約 60K トークン | 同上 |
| 合計（フル実行） | 約 140K トークン | Pro プランで 1 日数回が目安 |

> Pro プランの 1 日あたりメッセージ数に近づくと制限がかかります。  
> 大規模シナリオは複数日に分けて実行することを推奨します。

---

## お問い合わせ

- GitHub Issues: [リポジトリ URL]
- 導入支援・POC 相談: ModelCraft AI（[連絡先]）
