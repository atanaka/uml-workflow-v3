# Installation Guide / インストールガイド

## 📖 公式ドキュメント / Official Documentation

カスタムスキルの配置方法はプラットフォームごとに異なり、**プラットフォーム間で自動同期されません**。  
Custom Skills installation differs by platform and **does not sync across platforms**.

| Topic / トピック | Link |
|---|---|
| スキルの概要・プラットフォーム差異 / Skills overview & platform differences | [Agent Skills Overview](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) |
| Claude Code でのスキル配置 / Skills in Claude Code | [Extend Claude with Skills](https://docs.claude.com/en/docs/claude-code/skills) |
| SKILL.md の書き方・命名規則 / SKILL.md authoring & naming | [Skill Authoring Best Practices](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices) |
| Claude Code のセットアップ / Claude Code setup | [Advanced Setup](https://docs.claude.com/en/docs/claude-code/setup) |

---

## 📦 Package Overview / パッケージ概要

This package contains **14 skills** (1 orchestrator + 9 core + 4 optional). All skills are included — no additional downloads required.

このパッケージには**14スキル**（オーケストレーター1 + コア9 + オプション4）が含まれています。追加ダウンロードは不要です。

### Required (1 folder) / 必須（1フォルダ）

| # | Folder | Description |
|---|--------|-------------|
| 1 | `uml-workflow-v3/` | メインオーケストレーター（10ステップパイプライン内蔵）/ Main orchestrator (all 10 pipeline steps built-in) |

> `uml-workflow-v3/` alone is sufficient to run the full 10-step pipeline. / これ1つで全10ステップが動作します。

### Optional — Standalone Skills (13 folders) / オプション（13フォルダ）

以下は個別利用（単一ステップ実行、モデル手動修正など）向けです。フルワークフローには不要です。  
These are for independent use (single-step execution, manual model editing, etc.). Not required for the full workflow.

| # | Folder | Description |
|---|--------|-------------|
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

---

## 🚀 Option A: Claude Code（CLI）⭐ 推奨 / Recommended

Claude Code ではコンテキストウィンドウの管理が効率的で、`--continue` による再開も可能なため、Step 8 のような大量ファイル生成でも途切れにくくなります。  
Claude Code handles context more efficiently and supports `--continue` for resuming, making it more robust for large code generation steps like Step 8.

### Prerequisites / 前提条件

- Claude Pro / Max / Team / Enterprise プラン
- Claude Code がインストール済み（[セットアップ手順](https://docs.claude.com/en/docs/claude-code/setup)）

### A-1. Download / ダウンロード

**方法1: Git Clone**

```bash
git clone https://github.com/atanaka/uml-workflow-v3.git
```

**方法2: Release ZIP**

[Releases](../../releases) から最新版ZIPをダウンロードし、解凍します。  
Download the latest ZIP from [Releases](../../releases) and extract it.

### A-2. Install / インストール

**グローバルインストール（全プロジェクト共通）/ Global install (all projects):**

```bash
# メインオーケストレーターをコピー / Copy main orchestrator
cp -r uml-workflow-v3/uml-workflow-v3 ~/.claude/skills/uml-workflow-v3

# （任意）スタンドアロンスキルもコピー / (Optional) Copy standalone skills
cp -r uml-workflow-v3/skills/* ~/.claude/skills/
```

**プロジェクト固有インストール / Project-specific install:**

```bash
# プロジェクトルートで実行 / Run at project root
mkdir -p .claude/skills
cp -r /path/to/uml-workflow-v3/uml-workflow-v3 .claude/skills/uml-workflow-v3

# （任意）スタンドアロンスキルもコピー / (Optional) Copy standalone skills
cp -r /path/to/uml-workflow-v3/skills/* .claude/skills/
```

> 💡 **スキル配置ディレクトリ** ([公式ドキュメント](https://docs.claude.com/en/docs/claude-code/skills)):
> - `~/.claude/skills/` — 個人用（全プロジェクト共通） / Personal (all projects)
> - `.claude/skills/` — プロジェクト固有 / Project-specific
>
> Claude Code は両ディレクトリを自動スキャンし、SKILL.md のフロントマター（name, description）でスキルを自動検出します。  
> Claude Code auto-scans both directories and discovers skills via SKILL.md frontmatter.

### A-3. Verify / 動作確認

```bash
claude
# Claude Code 内で以下を入力 / Type in Claude Code:
> uml-workflow-v3が使えるか確認して
```

### A-4. Update / 更新

**Git Clone で入手した場合:**

```bash
cd uml-workflow-v3
git pull origin main
```

**Release ZIP で入手した場合:**

[Releases](../../releases) から最新版ZIPをダウンロードし、解凍して既存フォルダを上書きします。  
Download the latest ZIP from [Releases](../../releases), extract, and overwrite the existing folder.

**インストール先へ反映 / Apply to install location:**

```bash
# グローバルの場合 / For global install:
cp -r uml-workflow-v3 ~/.claude/skills/uml-workflow-v3

# プロジェクト固有の場合 / For project-specific:
cp -r uml-workflow-v3 .claude/skills/uml-workflow-v3
```

---

## 🌐 Option B: Claude.ai（Web / Desktop / Mobile）

### Prerequisites / 前提条件

- Claude Pro / Max / Team / Enterprise プラン
- 「Code execution and file creation」が **有効** / "Code execution and file creation" feature **enabled**

### B-1. Download / ダウンロード

[Releases](../../releases) から最新版ZIPをダウンロードし、解凍します。  
Download the latest ZIP from [Releases](../../releases) and extract it.

### B-2. Upload / アップロード

1. Claude.ai → **Customize** → **Skills** セクションを開く / Open Claude.ai → **Customize** → **Skills**
2. 「**Upload skill**」をクリック / Click "**Upload skill**"
3. `uml-workflow-v3/` **フォルダごと**アップロード / Upload the `uml-workflow-v3/` **folder**
4. スキルの**トグルを ON** にする / Toggle the skill **ON**
5. （任意）スタンドアロンスキルも同様にアップロード / (Optional) Upload standalone skills similarly

> ⚠️ **フォルダ単位でアップロードしてください**（個別ファイルではなく）。各フォルダには `SKILL.md` と `templates/` サブディレクトリが必要です。  
> ⚠️ Upload the **entire folder** (not individual files). Each folder must include its `SKILL.md` and any `templates/` subdirectory.

### B-3. Verify / 動作確認

新しい会話を開き、以下を入力 / Start a new conversation and type:

```
uml-workflow-v3で簡単なTodoアプリを生成して
```

Claude が設定質問を返してきたら、インストール成功です。  
If Claude responds with configuration questions, installation is successful!

### B-4. Update / 更新

> ⚠️ **スキルの更新時は「削除 → 新規アップロード」を推奨します。**  
> Claude.ai の「スキルを置き換え」機能は Internal server error になる場合があります。  
> ⚠️ **When updating, use "Delete → Upload new" instead of "Replace".**  
> The "Replace skill" feature in Claude.ai may cause Internal server errors.

1. **Settings → Skills** を開く / Open **Settings → Skills**
2. 既存スキルを **削除** / **Delete** the existing skill
3. 新版を **新規アップロード** / **Upload** the new version

### ⚠️ Claude.ai 固有の制約 / Claude.ai-Specific Limitations

Claude.ai のランタイム環境は Claude Code と異なります（[公式ドキュメント](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)）。  
The Claude.ai runtime environment differs from Claude Code ([official docs](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)).

| 項目 / Item | Claude Code | Claude.ai |
|---|---|---|
| ネットワーク / Network | フルアクセス / Full access | 制限あり / Limited |
| パッケージ追加 / Package install | 自由 / Unrestricted | npm, PyPI, GitHub のみ / npm, PyPI, GitHub only |
| ファイル出力 / File output | ローカルファイルシステム / Local filesystem | ダウンロード経由 / Via download |
| 中断からの再開 / Resume | `--continue` で再開可能 / `--continue` supported | 新しい会話で手動再開 / Manual resume in new conversation |
| コンテキスト管理 / Context | 効率的 / Efficient | 中断・やり直しが発生しやすい / Interruptions more likely |

---

## ⚙️ How It Works / 動作の仕組み

### 2-Phase Execution / 2フェーズ実行

フルワークフローはコンテキストウィンドウ枯渇を防ぐため、自動的に2つの会話に分割されます。  
Full workflow execution is automatically split into two conversations to prevent context window exhaustion.

1. **Phase A** (Steps 1-7): モデリング＆バリデーション → 全成果物をキャッシュ / Modeling & Validation → All artifacts cached
2. **Phase B** (Steps 8-10): コード生成 → Phase A のキャッシュを使用 / Code Generation → Uses cached artifacts from Phase A

Phase A 完了後、Claude が新しい会話で Phase B を開始するよう案内します。  
After Phase A completes, Claude will instruct you to start a new conversation for Phase B.

### Execution Modes / 実行モード

| Mode / モード | Command Example / コマンド例 |
|------|----------------|
| フルワークフロー / Full workflow | `uml-workflow-v3で受注管理システムを生成` |
| モデルのみ / Models only | `uml-workflow-v3で在庫管理のモデルのみ生成` |
| ステップ指定再開 / Resume from step | `uml-workflow-v3でproject-nameのStep 8から再開` |
| バリデーションのみ / Validation only | `uml-workflow-v3でproject-nameのバリデーションのみ` |

---

## 🔧 Troubleshooting / トラブルシューティング

### スキルが認識されない / Skill not detected

**Claude Code の場合:**

- `~/.claude/skills/uml-workflow-v3/SKILL.md` が存在するか確認 / Verify the file exists
- SKILL.md のフロントマター（`name`, `description`）が正しいか確認 / Check frontmatter is valid
- `name` フィールドは小文字・数字・ハイフンのみ（[命名規則](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices)）/ `name` must be lowercase, numbers, hyphens only

```bash
# 確認コマンド / Verification
ls ~/.claude/skills/uml-workflow-v3/SKILL.md
head -10 ~/.claude/skills/uml-workflow-v3/SKILL.md
```

**Claude.ai の場合:**

- Settings → Skills でスキルが表示されているか確認 / Check if skill appears in Settings → Skills
- トグルが ON になっているか確認 / Verify toggle is ON
- 「Code execution and file creation」が有効か確認 / Verify "Code execution and file creation" is enabled

### "Internal server error" on skill upload（Claude.ai）

Claude.ai の「スキルを置き換え」機能でこのエラーが発生することがあります。  
The "Replace skill" feature in Claude.ai may cause this error.

**対処法 / Workaround:**
1. **Settings → Skills** を開く
2. 既存スキルを **削除** / **Delete** the existing skill
3. 新版を **新規アップロード** / **Upload** the new version

### "Scripts not found"

`uml-workflow-v3/scripts/` に以下の5つの Python ファイルが含まれているか確認してください。  
Ensure `uml-workflow-v3/scripts/` contains these 5 Python files:

- `run_workflow.py`
- `workflow_cache_helper.py`
- `execution_mode_manager.py`
- `unified_workflow_executor.py`
- `interactive_workflow_executor.py`

### ワークフローが途中で停止 / Workflow stops mid-execution

キャッシュベースの再開を使用してください。  
Use cache-based resume:

```
uml-workflow-v3で[project-name]のStep [N]から再開して
```

Claude Code の場合は `--continue` も使えます。  
For Claude Code, you can also use `--continue`.

### Phase B でキャッシュが見つからない / Phase B fails to find cached artifacts

Phase A が正常に完了し、全成果物がキャッシュされていることを確認してください。必要に応じて Phase A を再実行します。  
Ensure Phase A completed successfully and all artifacts were cached. Re-run Phase A if needed.

---

## 📋 Upgrading from v2-enhanced / v2-enhanced からの移行

v2-enhanced から移行する場合 / If you previously used `uml-workflow-v2-enhanced`:

### Claude Code の場合

```bash
# 旧スキルを削除 / Remove old skills
rm -rf ~/.claude/skills/uml-workflow-v2-enhanced
rm -rf ~/.claude/skills/usecase-to-code-v1  # 旧版を削除

# 新スキルをインストール / Install new skills
cp -r uml-workflow-v3/uml-workflow-v3 ~/.claude/skills/uml-workflow-v3
cp -r uml-workflow-v3/skills/* ~/.claude/skills/
```

### Claude.ai の場合

1. **Settings → Skills** から `uml-workflow-v2-enhanced` を **削除** / **Delete** from Skills
2. 古い `usecase-to-code-v1` を **削除** / **Delete** old version
3. `uml-workflow-v3/` を**新規アップロード** / **Upload** new orchestrator
4. `skills/usecase-to-code-v1/`（templates/ 付き新版）を**アップロード** / **Upload** new version with `templates/`

> ✅ 既存のキャッシュ済み成果物は v3 と互換性があります。  
> ✅ Existing cached artifacts remain compatible with v3.
>
> ⚠️ 「スキルを置き換え」は使わず、必ず削除→新規アップロードしてください。  
> ⚠️ Do NOT use "Replace skill". Always delete first, then upload new.
