# uml-workflow-v3 進捗ダッシュボード 計画書

> 本書は設計計画のみを記述する。実装は本計画の承認後に別タスクとして着手する。
> 作成日: 2026-04-09 / 対象スキル: `uml-workflow-v3`

---

## 0. 決定事項サマリ（ユーザー確認済み）

| # | 項目 | 決定 |
|---|------|------|
| 1 | 配置場所 | `~/.claude/skills/uml-workflow-v3/dashboard/`（スキルに同梱） |
| 2 | アーキテクチャ | **Vite のみ**（別プロセスのバックエンドなし）+ ポーリング |
| 3 | ポート | 5173（Vite 既定） |
| 4 | 状態ファイル保存先 | `/mnt/user-data/outputs/`（既存ワークフロー出力と同位置） |
| 5 | 実装有無 | **本計画書のみ。実装はしない** |

---

## 1. 目的

`uml-workflow-v3` の 10 ステップパイプライン（Phase A: 1–7, Phase B: 8–10）の進捗を
リアルタイムに可視化する React アプリを作成する。以下を同時に満たす：

1. ワークフロー本体と **疎結合**（本体の実行フローを壊さない）
2. **Step 1 がスキップされるケースでも可視化できる**（スキップ判断より前に初期化）
3. **ワークフロー未実行でも単体で動作**（過去実行の閲覧・ドライラン）
4. **別プロセスのバックエンドを持たない**（Vite 一本で完結）

---

## 2. アーキテクチャ概要

```
┌──────────────────────┐   writes   ┌──────────────────────┐   reads    ┌─────────────────┐
│ uml-workflow-v3      │ ─────────▶ │ /mnt/user-data/      │ ◀───────── │ Vite Dev Server │
│ (Claude + scripts/)  │            │  outputs/            │  (plugin   │  + React SPA    │
│                      │            │  {proj}_workflow-    │   poll)    │  localhost:5173 │
│                      │            │  status.json         │            │                 │
└──────────────────────┘            └──────────────────────┘            └─────────────────┘
```

### 2.1 責務分担

- **ワークフロー側**：`status_emitter.py` が状態 JSON を atomic に書き出すだけ
- **Vite カスタムプラグイン**：`/mnt/user-data/outputs/` 配下の状態 JSON を読み、
  仮想エンドポイント（例：`/api/projects`, `/api/status/:project`）として配信
- **React SPA**：仮想エンドポイントを **1 秒間隔ポーリング**、差分を描画

> 「別プロセスのバックエンドなし」の定義 = Fastify/Express 等の独立サーバーは置かない。
> Vite 開発サーバーのカスタムミドルウェア（`configureServer`）で完結させる。

### 2.2 状態ファイル保存先とパス解決

既定：`/mnt/user-data/outputs/{project_name}_workflow-status.json`

ただし Claude 実行環境によってこのパスが存在しない場合があるため、
以下の優先順で解決する（`status_emitter.py` と Vite プラグインの両側で共通実装）：

1. 環境変数 `UMLWF_OUTPUT_DIR`（明示指定）
2. `/mnt/user-data/outputs/`（Claude のサンドボックス既定）
3. `~/claude-outputs/`（ローカル実行時のフォールバック）
4. `./outputs/`（カレント相対、最後の保険）

---

## 3. 状態ファイル仕様（契約）

ファイル名：`{project_name}_workflow-status.json`
書き込み規約：**atomic rewrite**（`*.tmp` → `rename`）、1 秒未満の連続更新は合流可。

```jsonc
{
  "schema_version": 1,
  "project_name": "order-system",
  "started_at": "2026-04-09T10:00:00+09:00",
  "updated_at": "2026-04-09T10:03:21+09:00",
  "execution_mode": "full",           // full | resume | models_only | validate_only
  "phase": "A",                       // A | B | completed | failed
  "current_step_id": 3,
  "config": {
    "cache": "yes",                   // yes | no | clear
    "xmi": false,
    "backend": "typescript-express",
    "frontend": "react-vite",
    "architecture": "monolith",
    "tests": true
  },
  "steps": [
    {
      "id": 1,
      "skill": "scenario-to-activity-v1",
      "label_ja": "シナリオ → アクティビティ図",
      "label_en": "Scenario → Activity",
      "phase": "A",
      "status": "skipped",            // pending|running|cached|completed|skipped|failed
      "reason": "user_provided_activity_diagram",
      "started_at": null,
      "ended_at": null,
      "duration_ms": 0,
      "outputs": [],
      "cache_hit": false,
      "error": null
    }
    // ... id: 2..10
  ],
  "token_stats": {
    "saved_estimate": 48000,
    "used": 12400
  },
  "cache_stats": {
    "hits": 2,
    "misses": 1
  },
  "messages": [                       // 任意の追加ログ（最新 N 件）
    { "ts": "2026-04-09T10:01:00+09:00", "level": "info", "text": "Phase A started" }
  ]
}
```

### 3.1 status の遷移規則

```
pending ──▶ running ──▶ completed
   │           │
   │           └─▶ failed
   │
   ├─▶ cached       (run_workflow.py が cache hit と判断した時点で)
   └─▶ skipped      (実行計画から除外された時点で)
```

`skipped` と `cached` は **Step 1 スキップ問題の要**：両者を区別して表示する。

---

## 4. ワークフロー側の差し込み設計（最小侵襲）

### 4.1 新規スクリプト

`~/.claude/skills/uml-workflow-v3/scripts/status_emitter.py`

公開 API：

| 関数 | 呼び出しタイミング | 主なパラメータ |
|------|------------------|----------------|
| `init_status(project_name, config)` | **Phase 0.2 の直後**（Python 環境チェック後） | config 一式。steps は全て `pending` で初期化 |
| `apply_execution_plan(project_name, plan_json_path)` | Phase 2.3（実行計画 JSON パース後） | plan を読み、`skipped` / `cached` をマーク |
| `begin_step(project_name, step_id)` | 各 Step 実行の直前 | `status=running`, `started_at=now` |
| `end_step(project_name, step_id, status, outputs=[], error=None)` | 各 Step 実行の直後 | `completed` / `failed` |
| `set_phase(project_name, phase)` | Phase A→B 境界、最終完了時 | `A` / `B` / `completed` / `failed` |
| `append_message(project_name, level, text)` | 任意の情報ログ | 失敗時の理由など |

すべて **ファイルロックなしの atomic rewrite**。読み手はポーリング時に一貫したスナップショットだけを見る。

### 4.2 SKILL.md への差し込み位置

| 位置 | 挿入する内容 | 備考 |
|------|-------------|------|
| **Phase 0.2 直後** | `init_status(project_name, <最小 config>)` | ← **Step 1 スキップ判断より前**。これが肝 |
| Phase 1 完了時 | `init_status` で渡した config を上書き更新 | ユーザー回答反映 |
| Phase 2.3（計画 JSON 読込直後） | `apply_execution_plan(...)` | skipped/cached のマーク付与 |
| 各 Step（1..10）の実行ブロック冒頭 | `begin_step(project_name, N)` | |
| 各 Step の実行ブロック末尾 | `end_step(project_name, N, "completed", outputs=[...])` | 失敗時は `"failed"` + error |
| Phase A チェックポイント | `set_phase("B")` もしくは `set_phase("completed")` | モード依存 |
| Phase 5 完了 | `set_phase("completed")` | |
| 例外経路 | `append_message(level="error", ...)` + `end_step(status="failed")` | |

差分は **各呼び出しが 1 行の bash ラッパー**で済むよう設計し、既存手順を汚さない。

### 4.3 Step 1 スキップ問題への対処（再掲）

- `init_status` は **プロジェクト名が決まった直後**（Phase 0.2 末尾）で呼ぶ。
- このタイミングでは「入力がアクティビティ図か否か」の判断はまだ行われていない。
- その後、Phase 2.3 で `apply_execution_plan` を呼ぶと、Step 1 が `skipped` にマークされる。
- よって **ダッシュボード上では「Step 1 が存在し、スキップされた理由付きで表示される」** 状態になる。
- もしダッシュボードを Step 1 の内部（PIPELINE.md）に仕込むと、Step 1 自体が実行されずに無視されるため、この配置は採用しない。

---

## 5. ダッシュボード（React SPA）

### 5.1 スタック

- Vite + React 18 + TypeScript
- Tailwind CSS + shadcn/ui
- Zustand（軽量状態管理）
- zod（状態ファイルのランタイムバリデーション）
- date-fns（相対時刻表示）

### 5.2 ディレクトリ構成（予定）

```
~/.claude/skills/uml-workflow-v3/dashboard/
├── PLAN.md                          # 本書
├── package.json
├── vite.config.ts                   # カスタムプラグインを登録
├── tsconfig.json
├── tailwind.config.ts
├── index.html
├── plugins/
│   └── workflow-status-plugin.ts    # /api/projects, /api/status/:proj を提供
├── src/
│   ├── main.tsx
│   ├── App.tsx
│   ├── routes.tsx
│   ├── pages/
│   │   ├── ProjectList.tsx
│   │   └── ProjectDetail.tsx
│   ├── components/
│   │   ├── PhaseTimeline.tsx
│   │   ├── StepCard.tsx
│   │   ├── StepDetailDrawer.tsx
│   │   ├── ModeBadge.tsx
│   │   ├── ConnectionIndicator.tsx
│   │   ├── TokenSavingsGauge.tsx
│   │   └── CacheStatsPanel.tsx
│   ├── hooks/
│   │   ├── useProjects.ts           # /api/projects を 5s ポーリング
│   │   └── useWorkflowStatus.ts     # /api/status/:proj を 1s ポーリング
│   ├── store/
│   │   └── workflowStore.ts
│   ├── lib/
│   │   ├── schema.ts                # zod スキーマ（状態ファイル仕様）
│   │   └── format.ts                # 時刻・トークン表示
│   └── types/
│       └── status.ts
└── README.md
```

### 5.3 Vite カスタムプラグイン設計

`plugins/workflow-status-plugin.ts`

- `configureServer(server)` で Express 風ミドルウェアを登録
- エンドポイント：
  - `GET /api/projects` → 出力ディレクトリを走査し、`*_workflow-status.json` を列挙
  - `GET /api/status/:project` → 該当ファイルを読み込み JSON を返す
  - `GET /api/dryrun?file=...` → 任意の `workflow_execution_result_*.json` を読み込み、計画プレビュー用に整形
- パス解決は §2.2 の優先順位を使用
- ファイル未存在時は 404 + わかりやすいエラーメッセージ（UI 側で「まだ実行されていません」表示）

> ポーリング方式のため、サーバー側にファイル監視は不要。
> クライアント側では React Query（または SWR）の `refetchInterval: 1000` によって 1 秒ごとに
> `/api/status/:project` を再取得し、`updated_at` が変わったときだけ再描画する。
> ※ 本ポーリングはブラウザ上の React SPA で動作するものであり、Vercel Workflow サンドボックスとは無関係。

### 5.4 画面構成

#### ProjectList（`/`）

- 検出された全プロジェクトのカード一覧
- 各カード：プロジェクト名 / モード / Phase / 進捗率 / 最終更新（相対時刻）
- 「スナップショットを開く」「ドライランをインポート」ボタン

#### ProjectDetail（`/project/:name`）

```
┌─────────────────────────────────────────────────────────┐
│ 📦 order-system           Mode: full  ● Live (1s ago)  │
│ Phase: A   Started: 10:00                               │
├─────────────────────────────────────────────────────────┤
│ Phase A (Modeling)                            [====----]│
│ ┌──┐─┌──┐─┌──┐─┌──┐─┌──┐─┌──┐─┌──┐                    │
│ │⏭1│ │✅2│ │💾3│ │⚙4│ │⏳5│ │⏳6│ │⏳7│                   │
│ └──┘ └──┘ └──┘ └──┘ └──┘ └──┘ └──┘                    │
│   skipped: user_provided_activity_diagram              │
│                                                         │
│ Phase B (Code Gen / Test / Traceability)      [--------]│
│ ┌──┐─┌──┐─┌──┐                                          │
│ │⏳8│ │⏳9│ │⏳10│                                         │
│ └──┘ └──┘ └──┘                                          │
├─────────────────────────────────────────────────────────┤
│ Token Savings: ~48,000 (est.)  │ Cache: 2 hit / 1 miss │
│ [Messages panel: 最新 10 件のログ]                       │
└─────────────────────────────────────────────────────────┘
```

ステップカードをクリックすると Drawer で詳細（出力ファイルリンク / 所要時間 / エラー）。

#### アイコン凡例

| アイコン | 状態 |
|--------|------|
| ⏳ | pending |
| ⚙ | running（アニメーション） |
| ✅ | completed |
| 💾 | cached |
| ⏭ | skipped（理由を tooltip 表示） |
| ❌ | failed |

### 5.5 独立実行モード

ワークフローが動いていないときでも以下が可能：

1. **過去実行の閲覧**：`/mnt/user-data/outputs/` に残る完了済み `*_workflow-status.json` を ProjectList に表示
2. **ドライラン表示**：SKILL.md が元々出力する `workflow_execution_result_{proj}.json` を
   `/api/dryrun?file=...` 経由で読み込み、「これから何が走るか」を同じタイムライン UI で表示
3. **手動インポート**：任意の状態 JSON をファイル選択で取り込み（FileReader API でクライアント側処理）
4. **ポーリング ON/OFF トグル**：静的閲覧モードへ切り替え

### 5.6 運用フロー（推奨）

```
# ① ダッシュボード事前起動（ターミナル 1）
cd ~/.claude/skills/uml-workflow-v3/dashboard
npm install
npm run dev
# → http://localhost:5173 で待機

# ② Claude に通常通り依頼（ターミナル 2 または Claude Code）
「uml-workflow-v3 で受注システムを生成」

# ③ ダッシュボードに自動的にプロジェクトが現れる
#    Step 1 がスキップされた場合も可視化される
```

事前起動しておけば、Step 1 スキップ問題と完全に独立して動作する。

---

## 6. 実装タスク一覧（実装フェーズ用の下準備）

本計画書の承認後、以下の順で着手する予定。本書の範囲では実装しない。

| # | タスク | 成果物 |
|---|-------|--------|
| 1 | 状態ファイルスキーマ確定 | `src/lib/schema.ts`（zod）+ JSON Schema |
| 2 | `status_emitter.py` 実装 | scripts 配下に追加、単体テスト付き |
| 3 | SKILL.md 差分パッチ案作成 | ユーザーレビュー前提で diff 形式 |
| 4 | Vite プラグイン `workflow-status-plugin.ts` | /api/* の 3 エンドポイント |
| 5 | React スケルトン（ルーティング + 型取り込み） | ビルドが通る状態 |
| 6 | ProjectList / ProjectDetail / PhaseTimeline | 主要画面 |
| 7 | StepCard / StepDetailDrawer | ステップ詳細 |
| 8 | TokenSavingsGauge / CacheStatsPanel / ConnectionIndicator | サブ情報 |
| 9 | 独立実行モード（スナップショット / ドライラン / 手動インポート） | |
| 10 | E2E 動作確認（full / resume / skip あり / cache hit の 4 パターン） | チェックリスト |
| 11 | README + INSTALL（事前起動の運用を明記） | |

---

## 7. 既存ワークフローへの影響評価

- **実行フロー**：`status_emitter.py` の呼び出しは失敗しても `|| true` でラップし、
  ワークフロー本体を止めない設計にする（ダッシュボードは補助機能）
- **token 使用**：状態ファイルの書き込みは Python 側で完結。Claude のコンテキストには乗らない
- **キャッシュ**：既存の `workflow_cache_helper.py` には一切手を入れない
- **パスの前提**：既存スキルが `/mnt/user-data/outputs/` を前提にしているため踏襲
- **ユーザー対話**：追加の質問は発生させない（起動はダッシュボードを事前起動するだけ）

---

## 8. リスクと緩和策

| リスク | 緩和策 |
|--------|--------|
| `/mnt/user-data/outputs/` がローカル環境に存在しない | §2.2 のパス解決フォールバックで対応 |
| 状態ファイルの atomic write が不完全（部分的な JSON を読む） | `*.tmp → rename` を徹底、読み手側で zod バリデーション失敗時は前回値を保持 |
| ポーリング 1s が重い | `updated_at` の If-None-Match 相当で未更新時は 304 相当の軽レスポンス |
| Step 1 スキップ以外にもスキップされるステップが出る | `apply_execution_plan` が汎用的に対応済（全ステップを `skipped`/`cached`/`pending` に分類） |
| ダッシュボード単体起動時に状態ファイルがない | 「ワークフロー未実行」の空状態 UI + 過去実行リスト |
| Vite プラグイン経由のファイルアクセスがセキュリティ上望ましくない | 読み取り専用・ホワイトリスト（`*_workflow-status.json` と `workflow_execution_result_*.json` のみ）・ローカルホスト限定 |

---

## 9. 次のアクション

1. 本計画書のレビュー
2. 承認後、§6 のタスク 1（スキーマ確定）と タスク 2（`status_emitter.py`）から着手
3. タスク 3（SKILL.md 差分）はユーザーレビューを挟んでから適用

以上。
