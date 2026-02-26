# UML Workflow v2 Enhanced - Claude Execution Guide

このドキュメントは、Claudeが uml-workflow-v3 スキルを実行する際の完全な手順書です。

## 🎯 実行トリガー

ユーザーが以下のように言ったとき、このワークフローを実行：
- 「uml-workflow-v3で〜を生成」
- 「uml-workflow-v3を使って〜」
- 「token効率化ワークフローで〜」

## 📋 実行手順（Claudeが従うステップ）

### STEP 1: プロジェクト名の決定

ユーザーのメッセージからプロジェクト名を推測：
- 「受注システム」→ "order-system"
- 「在庫管理」→ "inventory-management"  
- 英語の場合はそのまま kebab-case に変換

不明な場合は直接質問。

### STEP 2: ユーザー対話（ask_user_input ツール使用）

```python
# Claude は ask_user_input_v0 ツールを使用
ask_user_input_v0({
    "questions": [
        {
            "question": "キャッシュを使用しますか？",
            "type": "single_select",
            "options": [
                "はい（推奨）",
                "いいえ",
                "クリア"
            ]
        },
        {
            "question": "実行モードを選択",
            "type": "single_select",
            "options": [
                "フルワークフロー",
                "指定ステップから再開",
                "モデルのみ",
                "バリデーションのみ"
            ]
        },
        {
            "question": "XMI生成しますか？",
            "type": "single_select",
            "options": [
                "いいえ（推奨・40%高速化）",
                "はい"
            ]
        }
    ]
})
```

### STEP 3: 実行計画の作成

bash_tool を使用してPythonスクリプトを実行：

```bash
python3 /mnt/skills/user/uml-workflow-v3/scripts/run_workflow.py \
  <project-name> \
  --cache <yes|no|clear> \
  --mode <full|resume|models_only|validate_only> \
  [--xmi] \
  [--no-tests]
```

例：
```bash
python3 /mnt/skills/user/uml-workflow-v3/scripts/run_workflow.py \
  order-system \
  --cache yes \
  --mode full
```

このスクリプトが出力：
- 実行サマリー
- Token削減予測
- キャッシュ状況
- 実行すべきステップのリスト

### STEP 4: 各サブスキルの実行

スクリプトの出力に基づいて、Claude が各サブスキルを順次呼び出す：

#### Step 1: scenario-to-activity-v1

**キャッシュチェック済みで「実行が必要」と表示された場合：**

```
Claude calls scenario-to-activity-v1 with:
- Input: ユーザーのビジネスシナリオ
- Project name: <project-name>
- Generate XMI: <true|false>（ユーザー設定による）
```

**実行後：**
```bash
# キャッシュに保存（自動）
# → スクリプトが自動的に処理
```

#### Step 2: activity-to-usecase-v1

**前ステップの成果物が必要：**
- `<project>_activity-data.json`

**キャッシュから復元されていない場合：**

```
Claude calls activity-to-usecase-v1 with:
- Input: <project>_activity-data.json
- Generate XMI: <true|false>
```

#### Step 3: usecase-to-class-v1

```
Claude calls usecase-to-class-v1 with:
- Input: <project>_usecase-output.json
- Original scenario: <project>_activity-data.json
- Generate XMI: <true|false>
```

#### Step 4: class-to-statemachine-v1

```
Claude calls class-to-statemachine-v1 with:
- Input: <project>_domain-model.json
```

#### Step 5: usecase-to-sequence-v1

```
Claude calls usecase-to-sequence-v1 with:
- Input: <project>_usecase-output.json
- Domain model: <project>_domain-model.json
```

#### Step 6: model-validator-v1

```
Claude calls model-validator-v1 with:
- Input: All models in /mnt/user-data/outputs/<project>_*
```

#### Step 7: security-design-v1

**セキュリティ設計が有効な場合のみ：**

```
Claude calls security-design-v1 with:
- Input: <project>_domain-model.json, <project>_usecase-output.json
- Validation report: <project>_validation-report.md (optional)
```

#### Step 8: usecase-to-code-v1

**モード設定でコード生成が有効な場合のみ：**

```
Claude calls usecase-to-code-v1 with:
- Input: <project>_domain-model.json, <project>_usecase-output.json
- Security config: <project>_security-config.json (if available)
- Tech stack: ユーザーに確認または default
```

#### Step 9: usecase-to-test-v1

**テスト生成が有効な場合のみ：**

```
Claude calls usecase-to-test-v1 with:
- Input: <project>_domain-model.json, <project>_usecase-output.json
- Security config: <project>_security-config.json (if available)
```

### STEP 5: 各ステップ後のキャッシュ保存

各サブスキル実行後、以下のbashコマンドでキャッシュ保存：

```bash
python3 -c "
import sys
sys.path.append('/mnt/skills/user/uml-workflow-v3/scripts')
from workflow_cache_helper import cache_file

# 例: Step 1の成果物をキャッシュ
cache_file(
    '<project-name>',
    'scenario_to_activity',
    'activity-data',
    '/mnt/user-data/outputs/<project>_activity-data.json'
)
"
```

**または、自動化スクリプト利用可能**

### STEP 6: 完了サマリー

すべてのステップ完了後：

1. 成果物一覧を表示
2. Token削減実績を表示
3. 次回のキャッシュ利用を案内

## 🔍 具体例：フルワークフロー実行

```
ユーザー: 「uml-workflow-v3で受注システムを生成」

Claude:
  1. プロジェクト名推測: "order-system"
  2. ask_user_input で質問
  3. python run_workflow.py order-system --cache yes --mode full
  4. 出力確認：Step 1-9 すべて実行が必要
  5. scenario-to-activity-v1 を呼び出し
  6. activity-to-usecase-v1 を呼び出し
  7. usecase-to-class-v1 を呼び出し
  8. class-to-statemachine-v1 を呼び出し
  9. usecase-to-sequence-v1 を呼び出し
  10. model-validator-v1 を呼び出し
  11. security-design-v1 を呼び出し
  12. usecase-to-code-v1 を呼び出し（技術スタック確認）
  13. usecase-to-test-v1 を呼び出し
  14. 完了サマリー表示

完成！
```

## 🔍 具体例：キャッシュ活用（2回目）

```
ユーザー: 「order-systemに在庫管理機能を追加」

Claude:
  1. プロジェクト名: "order-system"（既存）
  2. ask_user_input で質問（キャッシュ: はい、モード: Step 2から再開）
  3. python run_workflow.py order-system --cache yes --mode resume --start-step 2
  4. 出力確認：
     - Step 1: キャッシュから復元 ✅
     - Step 2-8: 実行が必要
  5. Step 1 はスキップ（キャッシュ使用）
  6. activity-to-usecase-v1 から実行開始
  7. 以降のステップを実行

Token削減: 約20-30%
```

## ⚠️ 重要な注意事項

### Claudeがやるべきこと

1. **ユーザー対話**: ask_user_input ツールで設定収集
2. **実行計画**: run_workflow.py で計画作成
3. **サブスキル呼び出し**: 各ステップでサブスキルを実際に実行
4. **キャッシュ管理**: Pythonスクリプトが自動処理

### Pythonスクリプトがやること

1. **実行計画作成**
2. **キャッシュ管理**
3. **Token推定**
4. **サマリー表示**

### Pythonスクリプトができないこと

- サブスキルの直接呼び出し（これはClaude側の機能）
- ユーザーとの対話（これもClaude側の機能）

## 📊 フローチャート

```
User Request
    ↓
[Claude] プロジェクト名推測
    ↓
[Claude] ask_user_input でユーザー対話
    ↓
[Claude] bash_tool: run_workflow.py 実行
    ↓
[Python] 実行計画作成・キャッシュチェック・Token推定
    ↓
[Python] 実行すべきステップリストを出力
    ↓
[Claude] 出力を読み取る
    ↓
[Claude] For each step in list:
    ├─ キャッシュあり？ → 復元して次へ
    └─ キャッシュなし → サブスキル呼び出し
                      → 成果物をキャッシュ保存
    ↓
[Claude] 完了サマリー表示
```

## ✅ チェックリスト（Claudeが確認すべきこと）

実行前：
- [ ] プロジェクト名を決定済み
- [ ] ユーザー設定を収集済み
- [ ] run_workflow.py が正常実行
- [ ] 実行計画を確認済み

実行中（各ステップ）：
- [ ] キャッシュチェック実施
- [ ] キャッシュがあれば復元試行
- [ ] サブスキル呼び出し成功
- [ ] 成果物の生成確認
- [ ] キャッシュ保存実施

実行後：
- [ ] すべてのステップ完了
- [ ] 成果物を present_files
- [ ] Token削減実績を表示
- [ ] 次回実行のヒント提供

---

**このガイドに従うことで、Claudeは完全に自動化されたワークフローを実行できます。**
