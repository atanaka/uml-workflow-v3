# uml-workflow-v3 インストールガイド

## 📦 このパッケージについて

**uml-workflow-v3** は、ビジネスシナリオから本番品質のフルスタックアプリケーションを自動生成するClaude用スキルパッケージです。

このZIPパッケージには、動作に必要な**全13スキル**が同梱されています。別途スキルをダウンロードする必要はありません。

---

## 📁 同梱スキル一覧

### オーケストレーター（1件）
| フォルダ | 役割 |
|---------|------|
| `uml-workflow-v3/` | 全スキルを統括・自動実行するメインスキル |

### メインスキル（9件）
| フォルダ | 役割 |
|---------|------|
| `skills/scenario-to-activity-v1/` | ビジネスシナリオ → アクティビティ図 |
| `skills/activity-to-usecase-v1/` | アクティビティ図 → ユースケース |
| `skills/usecase-to-class-v1/` | ユースケース → クラス図・ドメインモデル |
| `skills/class-to-statemachine-v1/` | クラス図 → ステートマシン図 |
| `skills/usecase-to-sequence-v1/` | ユースケース → シーケンス図 |
| `skills/model-validator-v1/` | モデルバリデーション |
| `skills/security-design-v1/` | セキュリティ設計（OWASP準拠） |
| `skills/usecase-to-code-v1/` | フルスタックコード生成 |
| `skills/usecase-to-test-v1/` | テストコード生成 |

### オプションスキル（3件）
| フォルダ | 役割 |
|---------|------|
| `skills/json-to-models/` | domain-model.json から図・ドキュメントを再生成 |
| `skills/usecase-md-to-json/` | ユースケースMarkdownをJSONに変換 |
| `skills/classdiagram-image-to-json/` | クラス図画像をdomain-model.jsonに変換 |

---

## 🚀 インストール手順

### Step 1: ZIPを展開する

ダウンロードしたZIPを展開してください：

```
uml-workflow-v3-release/
├── README.md
├── uml-workflow-v3/
└── skills/
    ├── scenario-to-activity-v1/
    ├── activity-to-usecase-v1/
    └── ...（12スキル）
```

### Step 2: Claude.ai でSkillsを開く

1. claude.ai にアクセス
2. 左サイドバーの「Skills」をクリック
3. 「+ New Skill」をクリック

### Step 3: 関連スキル12件をアップロード

skills/ フォルダ内の各スキルをアップロードします。
各スキルフォルダを1つずつアップロードしてください。

アップロード順序（推奨）：

```
1.  skills/scenario-to-activity-v1/
2.  skills/activity-to-usecase-v1/
3.  skills/usecase-to-class-v1/
4.  skills/class-to-statemachine-v1/
5.  skills/usecase-to-sequence-v1/
6.  skills/model-validator-v1/
7.  skills/security-design-v1/
8.  skills/usecase-to-code-v1/
9.  skills/usecase-to-test-v1/
10. skills/json-to-models/
11. skills/usecase-md-to-json/
12. skills/classdiagram-image-to-json/
```

### Step 4: uml-workflow-v3 をアップロード

最後にメインオーケストレーターをアップロードします：

```
uml-workflow-v3/
```

> ⚠️ 重要: 関連スキル12件を先にアップロードしてから、uml-workflow-v3 をアップロードしてください。

### Step 5: 動作確認

Claudeとの新しい会話を開始し、以下を入力してください：

```
「uml-workflow-v3が使えるか確認して」
```

Claudeが正常に応答すれば完了です。

---

## 🎯 最初の実行

```
「uml-workflow-v3で簡単な在庫管理システムを生成して」
```

Claudeが対話形式でいくつか質問しますので答えてください（すべてデフォルト選択でOKです）。

---

## ❓ トラブルシューティング

### スキルが認識されない

- Skills画面でスキルが正しくアップロードされているか確認してください
- フォルダ単位でアップロードされているか確認してください（個別ファイルではなくフォルダごと）

### スクリプトが見つからないと言われる

uml-workflow-v3/scripts/ に以下5ファイルが存在することを確認してください：
- run_workflow.py
- workflow_cache_helper.py
- execution_mode_manager.py
- unified_workflow_executor.py
- interactive_workflow_executor.py

### 途中でエラーが発生した場合

キャッシュ機能により、中断したステップから再開できます：

```
「uml-workflow-v3で[プロジェクト名]のStep [N]から再開して」
```

---

## 📚 関連ドキュメント

| ファイル | 内容 |
|---------|------|
| ../README.md | パッケージ全体の説明 |
| README.md | uml-workflow-v3の詳細 |
| SKILL.md | Claude実行仕様（技術者向け） |
| CLAUDE_QUICK_GUIDE.md | Claudeへのクイックリファレンス |
| CHANGELOG.md | バージョン履歴 |
