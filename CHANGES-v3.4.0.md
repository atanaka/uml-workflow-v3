# uml-workflow-v3 v3.4.0 改修サマリ

**作成日**: 2026-05-24
**改修対象**: `uml-workflow-v3` v3.3.0 → v3.4.0
**起点**: `_handoff_2026-05-22_uml-workflow-v3-improvement-candidates_1.md`

---

## 概要

`library-management` プロジェクトの生成・動作検証で浮上した 10 件の改修候補のうち、優先度「最高」「高」に該当する 6 件（#1, #2, #4, #5, #6, #10）を実装しました。

| # | 改修内容 | 状態 |
|---|---|---|
| #1 | `activity-to-usecase-v1` 出力の完全性検証 | ✅ 実装 |
| #2 | Resume from Step 8+ モード事前条件検証 | ✅ 実装 |
| #4 | `AuditService.ts` テンプレートの Json 型キャスト | ✅ SKILL.md ガイドラインとして記述 |
| #5 | `tests/fixtures/builders.ts` の有効 UUID 生成 | ✅ SKILL.md ガイドラインとして記述 |
| #6 | `rateLimit.ts` テンプレートの `NODE_ENV=test` 対応 | ✅ SKILL.md ガイドラインとして記述 |
| #10 | `backend/package.json` の `prisma.seed` 設定 | ✅ SKILL.md ガイドラインとして記述 |
| #3 | 全 Step 共通の Expected Outputs 検証フレームワーク | ⏸ `verify_step_outputs.py` で土台のみ実装（拡張余地あり） |
| #7, #8, #9 | `json-to-models` 側の v1.4 候補 | ⏸ 別スキル管轄のため今回はスコープ外 |

---

## 変更ファイル一覧

### 新規ファイル

- `scripts/verify_step_outputs.py` (約 380 行)
  - `verify_step2_outputs()`: Step 2 出力完全性検証
  - `verify_phase_a_completeness()`: Phase A 全体完全性検証
  - `assert_step2_complete()` / `assert_phase_a_complete()`: 失敗時 `WorkflowError` 送出版
  - `format_phase_a_report()`: ユーザー表示用レポート整形
  - CLI モード: `python3 verify_step_outputs.py step2 <project>` / `phase_a <project>`
  - `STEP_EXPECTED_OUTPUTS` 辞書で各 Step の Expected Outputs を一元管理（改修 #3 への拡張余地）

- `scripts/test_verify_step_outputs.py` (約 290 行)
  - 13 件の回帰テスト（library-management 実例の再現を含む）
  - `python3 scripts/test_verify_step_outputs.py` で実行可

### 変更ファイル

| ファイル | 変更内容 | 行数増加 |
|---|---|---|
| `SKILL.md` | PHASE 0.5 (Resume Mode Prerequisite Check) 新設、Step 2 末尾検証、Step 8 fail-safe 検証、AUTO-SPLIT CHECKPOINT 内 Resume 分岐に PHASE 0.5 への導線追加 | +95 行 |
| `references/activity-to-usecase-v1/SKILL.md` | Step 7.5 (Verify Output Completeness) 新設 | +40 行 |
| `references/usecase-to-code-v1/SKILL.md` | Step 9.5 (Backend Code Quality Requirements) 新設（9.5a prisma.seed, 9.5b InputJsonValue, 9.5c rateLimit test 対応） | +102 行 |
| `references/usecase-to-test-v1/SKILL.md` | Test Fixture Quality Requirements セクション新設（randomUUID 使用） | +46 行 |

---

## 動作検証

回帰テスト 13/13 すべて pass:

```
$ python3 scripts/test_verify_step_outputs.py
...
Ran 13 tests in 0.026s
OK
```

主要テストケース:
- `test_2_library_management_repro_case`: 12 UC 中 3 .md のみという `library-management` 実例を再現し、9 件の欠落 UC ID（UC-002〜UC-004, UC-007〜UC-012）が正しく検出されることを確認
- `test_5_phase_a_domain_model_missing`: `domain-model.json` 欠落時に正しいステップ名 (`usecase_to_class`) が紐づけられることを確認
- `test_6_phase_a_cross_check_fails`: JSON と spec ディレクトリの UC 数不整合をクロスチェックで検出

---

## ユーザーへの体感的変化

### Phase A 実行時 (Full Workflow / Models-only)

Step 2 完了直後に検証が走り、UC .md ファイル数が JSON と一致しない場合は **即座に停止** します。これまで Phase B まで進んでから気付くしかなかった `library-management` 型の不整合が、その場で発覚するようになります。

### Phase B 実行時 (Resume from Step 8+)

ユーザーが「`uml-workflow-v3 で {project} の Step 8 から再開`」と入力すると、**Step 8 着手前** に PHASE 0.5 が走ります。Phase A 成果物に欠落があれば検証レポートが表示され、

- (a) 不足分をアップロード
- (b) 該当 Phase A ステップを再実行
- (c) 警告ありで強行

の選択肢が提示されます。これまでは不完全アップロードのまま Step 8 が走り、後から SSoT 不整合に気付いていた事象が予防されます。

### Step 8/9 (コード・テスト生成)

SKILL.md の Step 9.5 / Test Fixture Quality Requirements が、Claude が生成時に必ず読む位置（Step 9 と Step 10 の間／SKILL.md 末尾）に明示されています。これにより:

- 初回 `npm run build` で TS2322（AuditService の JSON 型エラー）が出なくなる
- 初回 `npm test` で 429 Too Many Requests が出なくなる
- zod uuid バリデーションで 7 件のテストが落ちる事象が出なくなる
- `npx prisma migrate reset --force` の自動 seed が動くようになる

---

## デモ動画録画前のチェックリスト

修正後の動作を確認するため、以下を推奨します:

1. ✅ `scripts/test_verify_step_outputs.py` を実行して 13/13 pass を確認（済）
2. ⏭ 修正版 `uml-workflow-v3` を `/mnt/skills/user/` に展開
3. ⏭ 小規模なテストプロジェクト（例: 3〜5 UC のシナリオ）で Phase A → Phase B をひと通り通し、
   - Step 2 完了時に「✅ Step 2 verified: all UCs have spec files」が表示されること
   - Phase B 開始時に「✅ Phase A artifacts complete」が表示されること
   - 生成された `backend/package.json` に `prisma.seed` キーがあること
   - 生成された `rateLimit.ts` に `NODE_ENV === 'test'` 分岐があること
   - 生成された `builders.ts` で `randomUUID` が使われていること
   - `npm test` がレート制限失敗・UUID バリデーション失敗なく走ること
4. ⏭ わざと `usecase-output.json` の UC を 1 件増やした状態で Step 7.5 が落ちることを確認（負例）
5. ⏭ デモ動画を録画

---

## 今後の改修（v3.5 / v1.4 候補）

今回スコープ外とした項目:

- **#3**: 全 Step 共通の Expected Outputs 検証フレームワーク
  - `STEP_EXPECTED_OUTPUTS` 辞書と `verify_step()` 汎用関数の骨格は既に `verify_step_outputs.py` 内に用意済み
  - 今回は Step 2 と Phase A 全体の 2 用途のみで運用、必要に応じて他 Step (Step 3 〜 7) にも展開可能
- **#7**: `role_name` フィールド対応（`json-to-models` v1.4）
- **#8**: `is_abstract` 対応強化（PlantUML 出力で `abstract class X` 表示）
- **#9**: DEMO-GUIDE.md のクラス図作成手順記述

これらは `json-to-models` および DEMO-GUIDE.md 側の改修であり、本セッションのスコープからは除外しました。

---

## 補足: 本体コード版 / Release 版の作り分け

このセッションで生成した成果物は **本体コード版（GitHub 公開用）** です。すべてのスキルファイルは `SKILL.md` の名前で統一されており、親 SKILL.md からの参照もすべて `references/{skill-name}/SKILL.md` を指しています。

### YAML frontmatter について

各サブスキルの `SKILL.md` は Claude Skills が認識できるよう、必ず YAML frontmatter を先頭に持つ必要があります（`SKILL.md must start with YAML frontmatter` エラー回避のため）。本セッションでは `references/*/SKILL.md` 全 10 ファイルに frontmatter を確認・追加しました。

- 9 ファイル (`activity-to-usecase-v1` `usecase-to-code-v1` `usecase-to-test-v1` `scenario-to-activity-v1` `usecase-to-class-v1` `class-to-statemachine-v1` `usecase-to-sequence-v1` `model-validator-v1` `security-design-v1`): 独立スキル版から `name` / `description` を移植
- 1 ファイル (`traceability-matrix-v1`): 独立スキル版が無いため frontmatter を新規作成

### Release 版（Claude.ai アップロード用）への変換手順

GitHub の本体コード版を Claude.ai にアップロードする際は、Claude Skills がネスト構造を受け入れない制約により、以下の変換を行う必要があります:

1. 全 `references/*/SKILL.md` を `references/*/PIPELINE.md` にリネーム
2. リネーム後の `PIPELINE.md` は frontmatter が不要になる（参照ドキュメント扱いになるため）。残しておいても害はないが、整理のため削除も可
3. 親 `SKILL.md` 内の `references/{skill-name}/SKILL.md` への参照をすべて `references/{skill-name}/PIPELINE.md` に書き換え
4. `scripts/verify_step_outputs.py` の docstring 内の参照テキストもあわせて更新

この変換は次セッション以降で実施予定。
