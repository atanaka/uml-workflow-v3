# AI-Assisted UML Workflow v3 - Complete Package

ビジネスシナリオから本番品質のフルスタックアプリケーションを自動生成する、Claude用スキルパッケージです。

---

## 🎯 このパッケージでできること

自然言語で書いたビジネスシナリオを入力するだけで、以下を自動生成します：

```
ビジネスシナリオ（自然言語）
  ↓ 自動生成
  ├── UMLモデル一式
  │     ├── アクティビティ図
  │     ├── ユースケース図 + 仕様書
  │     ├── クラス図（ドメインモデル）
  │     ├── ステートマシン図
  │     └── シーケンス図
  ├── バリデーションレポート
  ├── セキュリティ設計書（OWASP準拠）
  ├── フルスタックアプリケーションコード
  │     ├── Backend（TypeScript/Python/Java/Go）
  │     └── Frontend（React/Vue）
  └── テストコード（Unit / Integration / E2E）
```

**最大75%のトークン削減**を実現するキャッシュシステム・段階的実行・XMI最適化を搭載しています。

---

## 📁 パッケージ構成

```
uml-workflow-v3/              ← メインオーケストレーター
└── （詳細は下記）

skills/                       ← 関連スキル12件（全量収録）
  ├── [メインスキル 9件]
  │   ├── scenario-to-activity-v1/
  │   ├── activity-to-usecase-v1/
  │   ├── usecase-to-class-v1/
  │   ├── class-to-statemachine-v1/
  │   ├── usecase-to-sequence-v1/
  │   ├── model-validator-v1/
  │   ├── security-design-v1/
  │   ├── usecase-to-code-v1/
  │   └── usecase-to-test-v1/
  └── [オプションスキル 3件]
      ├── json-to-models/
      ├── usecase-md-to-json/
      └── classdiagram-image-to-json/
```

---

## 🚀 セットアップ手順（初めての方）

### 必要なもの

- Claude.ai アカウント（Pro または Team プラン推奨）
- このパッケージのZIPファイル

### Step 1: スキルフォルダを準備する

ZIPを展開すると以下の構成になります：

```
uml-workflow-v3-release/
├── README.md              ← このファイル
├── uml-workflow-v3/       ← メインオーケストレーター
└── skills/                ← 関連スキル12件
```

### Step 2: Claude にスキルをアップロードする

Claude.ai の **Skills** 機能を使って、以下のフォルダをすべてアップロードします。

**アップロード順序（推奨）:**

まず関連スキルを先にアップロードしてください：

```
skills/scenario-to-activity-v1/
skills/activity-to-usecase-v1/
skills/usecase-to-class-v1/
skills/class-to-statemachine-v1/
skills/usecase-to-sequence-v1/
skills/model-validator-v1/
skills/security-design-v1/
skills/usecase-to-code-v1/
skills/usecase-to-test-v1/
skills/json-to-models/
skills/usecase-md-to-json/
skills/classdiagram-image-to-json/
```

次にメインオーケストレーターをアップロードします：

```
uml-workflow-v3/
```

### Step 3: 動作確認

Claudeとの会話で以下のように話しかけてください：

```
「uml-workflow-v3が使えるか確認して」
```

正常に認識されたら、以下で実行できます：

```
「uml-workflow-v3で受注管理システムを生成して」
```

---

## 💬 使い方

### 基本的な使い方

```
あなた: 「uml-workflow-v3で[システム名]を生成して」

Claude: いくつか確認させてください。
  1. キャッシュを使用しますか？ → はい（推奨）
  2. 実行モードは？ → フルワークフロー
  3. XMI生成は？ → いいえ（推奨・40%高速化）
  4. テスト生成は？ → はい
  5. バックエンドは？ → TypeScript + Express
  6. フロントエンドは？ → React + TypeScript
  7. アーキテクチャは？ → モノリス

Claude: [Step 1〜9 を自動実行]
  ✅ アクティビティ図
  ✅ ユースケース
  ✅ クラス図
  ✅ ステートマシン図
  ✅ シーケンス図
  ✅ バリデーション
  ✅ セキュリティ設計
  ✅ アプリケーションコード
  ✅ テストコード
```

### 途中から再実行する場合

```
「uml-workflow-v3で[プロジェクト名]のStep 3から再開して」
```

### モデルだけ生成する場合（コード生成なし）

```
「uml-workflow-v3でモデルのみ生成して」
```

### バリデーションだけ実行する場合

```
「uml-workflow-v3でバリデーションのみ実行して」
```

---

## 📋 スキル一覧と役割

### メインスキル（Step 1〜9）

| Step | スキル名 | 入力 | 出力 |
|------|---------|------|------|
| 1 | scenario-to-activity-v1 | ビジネスシナリオ（自然言語） | アクティビティ図 |
| 2 | activity-to-usecase-v1 | アクティビティ図 | ユースケース図・仕様書 |
| 3 | usecase-to-class-v1 | ユースケース | クラス図・ドメインモデル |
| 4 | class-to-statemachine-v1 | クラス図 | ステートマシン図 |
| 5 | usecase-to-sequence-v1 | ユースケース・クラス図 | シーケンス図 |
| 6 | model-validator-v1 | 全モデル | バリデーションレポート |
| 7 | security-design-v1 | ドメインモデル・ユースケース | セキュリティ設計書 |
| 8 | usecase-to-code-v1 | ドメインモデル・ユースケース | フルスタックアプリ |
| 9 | usecase-to-test-v1 | ドメインモデル・ユースケース | テストコード |

### オプションスキル

| スキル名 | 使う場面 |
|---------|---------|
| json-to-models | domain-model.json を手動編集後、PlantUML/XMIを再生成したい場合 |
| usecase-md-to-json | ユースケース仕様（Markdown）を手動編集後、JSONに反映したい場合 |
| classdiagram-image-to-json | 手描き・ツール作成のクラス図画像をワークフローに取り込みたい場合 |

---

## ⚙️ 対応技術スタック

**バックエンド**
- TypeScript + Express（推奨・軽量）
- TypeScript + NestJS（大規模向け）
- Python + FastAPI
- Java + Spring Boot

**フロントエンド**
- React + TypeScript + Vite + Tailwind CSS（推奨）
- Vue 3 + TypeScript + Vite

**アーキテクチャ**
- モノリス（推奨・シンプル）
- マイクロサービス
- サーバーレス

**対応言語**
- 日本語・英語・バイリンガル（自動検出）

---

## 🔧 トラブルシューティング

### スキルが認識されない

```
「uml-workflow-v3のSKILL.mdを確認して」
```
と伝えて、Claudeにスキルの読み込みを確認させてください。

### スクリプトが見つからない

`uml-workflow-v3/scripts/` にPythonファイルが5つ存在することを確認してください：
- `run_workflow.py`
- `workflow_cache_helper.py`
- `execution_mode_manager.py`
- `unified_workflow_executor.py`
- `interactive_workflow_executor.py`

### 途中でエラーが発生した場合

```
「uml-workflow-v3で[プロジェクト名]のStep [N]から再開して」
```
キャッシュが保存されているため、エラーが発生したステップから再実行できます。

---

## 📚 詳細ドキュメント

| ファイル | 内容 |
|---------|------|
| `uml-workflow-v3/README.md` | オーケストレーターの詳細説明 |
| `uml-workflow-v3/INSTALL.md` | インストールの詳細手順 |
| `uml-workflow-v3/SKILL.md` | Claude実行仕様（技術者向け） |
| `uml-workflow-v3/CHANGELOG.md` | バージョン履歴 |
| `skills/[スキル名]/README.md` | 各スキルの個別説明 |

---

## 🌐 GitHub

https://github.com/atanaka/uml-workflow-v3

---

*このパッケージは Claude + MBSE（モデルベースシステムズエンジニアリング）の統合を目的として開発されました。*
