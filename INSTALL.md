# Installation Guide / インストールガイド

## 📦 Package Overview / パッケージ概要

This package contains **14 skills** (1 orchestrator + 9 core + 4 optional). All skills are included — no additional downloads required.

このパッケージには**14スキル**（オーケストレーター1 + コア9 + オプション4）が含まれています。追加ダウンロードは不要です。

---

## 🚀 Installation / インストール手順

### Step 1: Download / ダウンロード

Download or clone this repository.

### Step 2: Upload to Claude.ai / Claude.aiにアップロード

1. Open [claude.ai](https://claude.ai)
2. Go to **Settings → Skills**
3. Upload skill folders:

**Required (1 folder) / 必須（1フォルダ）:**

| # | Folder to Upload | Description |
|---|-----------------|-------------|
| 1 | `uml-workflow-v3/` | Main orchestrator（10ステップパイプライン内蔵）/ Main orchestrator (all 10 pipeline steps built-in) |

> `uml-workflow-v3/` alone is sufficient to run the full 10-step pipeline. / これ1つで全10ステップが動作します。

**Optional — standalone skills (13 folders) / オプション — スタンドアロンスキル（13フォルダ）:**

以下は個別利用（単一ステップ実行、モデル手動修正など）向けです。フルワークフローには不要です。 / These are for independent use (single-step execution, manual model editing, etc.). Not required for the full workflow.

| # | Folder to Upload | Description |
|---|-----------------|-------------|
| 2 | `skills/scenario-to-activity-v1/` | シナリオ → アクティビティ図 |
| 3 | `skills/activity-to-usecase-v1/` | アクティビティ図 → ユースケース |
| 4 | `skills/usecase-to-class-v1/` | ユースケース → クラス図 |
| 5 | `skills/class-to-statemachine-v1/` | クラス図 → ステートマシン図 |
| 6 | `skills/usecase-to-sequence-v1/` | ユースケース → シーケンス図 |
| 7 | `skills/model-validator-v1/` | モデル横断バリデーション |
| 8 | `skills/security-design-v1/` | OWASP準拠セキュリティ設計 |
| 9 | `skills/usecase-to-code-v1/` | フルスタックコード生成 |
| 10 | `skills/usecase-to-test-v1/` | テストコード生成 |
| 11 | `skills/json-to-models/` | JSON → PlantUML/XMI 再生成 |
| 12 | `skills/usecase-md-to-json/` | UC仕様 Markdown → JSON変換 |
| 13 | `skills/classdiagram-image-to-json/` | 手描きクラス図 → JSON取込 |
| 14 | `skills/classdiagram-to-crud/` | クラス図 → CRUD HTML生成 |

> ⚠️ Upload the **entire folder** (not individual files). Each folder must include its `SKILL.md` and any `templates/` subdirectory.
>
> ⚠️ **既存スキルの更新時は「置き換え」ではなく「削除→新規アップロード」を推奨します。** Claude.ai の「スキルを置き換え」機能は Internal server error になる場合があります。必ず既存スキルを削除してから新規アップロードしてください。
>
> ⚠️ **When updating existing skills, use "Delete → Upload new" instead of "Replace".** The "Replace skill" feature in Claude.ai may cause Internal server errors. Always delete the existing skill first, then upload the new version.

### Step 3: Verify / 確認

Start a new conversation and type:

```
uml-workflow-v3で簡単なTodoアプリを生成して
```

If Claude responds with configuration questions, installation is successful!

---

## ⚙️ How It Works / 動作の仕組み

### 2-Phase Execution / 2フェーズ実行

Full workflow execution is automatically split into two conversations to prevent context window exhaustion:

1. **Phase A** (Steps 1-7): Modeling & Validation → All artifacts cached
2. **Phase B** (Steps 8-10): Code Generation → Uses cached artifacts from Phase A

After Phase A completes, Claude will instruct you to start a new conversation for Phase B.

### Execution Modes / 実行モード

| Mode | Command Example |
|------|----------------|
| Full workflow | `uml-workflow-v3で受注管理システムを生成` |
| Models only | `uml-workflow-v3で在庫管理のモデルのみ生成` |
| Resume from step | `uml-workflow-v3でproject-nameのStep 8から再開` |
| Validation only | `uml-workflow-v3でproject-nameのバリデーションのみ` |

---

## 🔧 Troubleshooting / トラブルシューティング

### "Internal server error" on skill upload / スキルアップロード時のエラー

The "Replace skill" feature in Claude.ai may cause this error. Use the following workaround:

Claude.ai の「スキルを置き換え」機能でこのエラーが発生することがあります。以下の手順で回避してください：

1. Go to **Settings → Skills** / **Settings → Skills** を開く
2. **Delete** the existing skill / 既存スキルを**削除**
3. **Upload** the new version as a fresh skill / 新版を**新規アップロード**

### "Scripts not found"

Ensure `uml-workflow-v3/scripts/` contains these 5 Python files:
- `run_workflow.py`
- `workflow_cache_helper.py`
- `execution_mode_manager.py`
- `unified_workflow_executor.py`
- `interactive_workflow_executor.py`

### Workflow stops mid-execution

Use cache-based resume:
```
uml-workflow-v3で[project-name]のStep [N]から再開して
```

### Phase B fails to find cached artifacts

Ensure Phase A completed successfully and all artifacts were cached. Re-run Phase A if needed.

---

## 📋 Upgrading from v2-enhanced / v2-enhancedからの移行

If you previously used `uml-workflow-v2-enhanced`:

1. **Delete** `uml-workflow-v2-enhanced` from Claude.ai Skills / Claude.ai Skills から削除
2. **Delete** the old `usecase-to-code-v1` / 古い `usecase-to-code-v1` を削除
3. **Upload** `uml-workflow-v3/` as the new orchestrator / 新オーケストレーターをアップロード
4. **Upload** `skills/usecase-to-code-v1/` (new version with `templates/`) / 新版をアップロード
5. Existing cached artifacts remain compatible / 既存キャッシュは互換性あり

> ⚠️ Do NOT use "Replace skill". Always delete first, then upload new. / 「スキルを置き換え」は使わず、必ず削除→新規アップロードしてください。
