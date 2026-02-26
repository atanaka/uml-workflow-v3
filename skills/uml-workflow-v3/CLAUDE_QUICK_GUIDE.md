# Claude Quick Execution Cheatsheet

**このスキル実行時にClaude が従うべき簡潔な手順**

## 🚀 実行フロー（5ステップ）/ Execution Flow (5 Steps)

### 1. プロジェクト名決定
```
ユーザーのメッセージから推測：
「受注システム」→ "order-system"
「inventory management」→ "inventory-management"
```

### 2. ユーザーに質問（ask_user_input_v0使用）
```javascript
ask_user_input_v0({
  "questions": [
    {
      "question": "キャッシュを使用しますか？",
      "type": "single_select",
      "options": ["はい（推奨）", "いいえ", "クリア"]
    },
    {
      "question": "実行モードを選択",
      "type": "single_select",
      "options": ["フルワークフロー", "指定ステップから再開", "モデルのみ", "バリデーションのみ"]
    },
    {
      "question": "XMI生成しますか？",
      "type": "single_select",
      "options": ["いいえ（推奨・40%高速化）", "はい"]
    }
  ]
})
```

### 3. run_workflow.py実行（bash_toolで自動）
```bash
python3 /mnt/skills/user/uml-workflow-v3/scripts/run_workflow.py \
  {project-name} \
  --cache {yes/no/clear} \
  --mode {full/resume/models_only/validate_only} \
  [--start-step {2-9}] \
  [--xmi] \
  [--no-tests] \
  [--no-security]
```

### 4. 実行計画JSONを読み取る
```bash
cat /mnt/user-data/outputs/workflow_execution_result_{project_name}.json
```

### 5. 各サブスキルを順次呼び出し
```
For each step in execution plan:
  - キャッシュあり → スキップ
  - キャッシュなし → サブスキル呼び出し
    
サブスキル一覧:
  Step 1: scenario-to-activity-v1
  Step 2: activity-to-usecase-v1
  Step 3: usecase-to-class-v1
  Step 4: class-to-statemachine-v1
  Step 5: usecase-to-sequence-v1
  Step 6: model-validator-v1
  Step 7: security-design-v1
  Step 8: usecase-to-code-v1
  Step 9: usecase-to-test-v1
```

## 📝 具体例 / Examples

### ユーザー: "uml-workflow-v3で受注システムを生成"

```
Claude実行手順:

1. project_name = "order-system"

2. ask_user_input_v0(...) → 回答取得

3. bash_tool:
   python3 /mnt/skills/user/uml-workflow-v3/scripts/run_workflow.py \
     order-system --cache yes --mode full

4. 出力確認:
   「Steps executed: scenario-to-activity-v1, activity-to-usecase-v1, ...」

5. 各サブスキル呼び出し:
   Claude calls scenario-to-activity-v1 with business scenario
   Claude calls activity-to-usecase-v1 with activity-data.json
   Claude calls usecase-to-class-v1 with usecase-output.json
   ...

6. present_files で成果物提示

完了！
```

## ⚠️ 重要 / Important

- **ユーザーはPythonコードを一切実行しない**
- **すべてClaudeがbash_toolで自動実行**
- **ユーザーは質問に答えるだけ**

## 🔍 トラブルシューティング / Troubleshooting

### scripts/が見つからない場合:
```bash
# フォールバック先を試す
python3 /mnt/user-data/outputs/uml-workflow-v3-complete/scripts/run_workflow.py ...
```

### サブスキルが見つからない場合:
```
「{スキル名}が見つかりません。スキルをアップロードしてください」と案内
```

---

**これだけ！簡単！**
