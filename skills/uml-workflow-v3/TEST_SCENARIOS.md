# Execution Flow Test Scenarios

このドキュメントは、uml-workflow-v3の完全な実行フローをテストするためのシナリオです。

## 🧪 Test Scenario 1: First-Time Full Workflow / 初回フルワークフロー

### User Input
```
ユーザー: 「uml-workflow-v3で簡単な商品管理システムを生成」
```

### Expected Claude Actions

#### Step 1: Project Name Inference
```
Claude determines: project_name = "product-management"
```

#### Step 2: User Questions
```javascript
Claude calls: ask_user_input_v0({
  questions: [
    {question: "キャッシュを使用しますか？", options: ["はい（推奨）", "いいえ", "クリア"]},
    {question: "実行モードを選択", options: ["フルワークフロー", ...]},
    {question: "XMI生成しますか？", options: ["いいえ（推奨）", "はい"]}
  ]
})

User selects:
- はい（推奨）
- フルワークフロー
- いいえ（推奨）
```

#### Step 3: Execute run_workflow.py
```bash
Claude executes via bash_tool:

python3 /mnt/skills/user/uml-workflow-v3/scripts/run_workflow.py \
  product-management \
  --cache yes \
  --mode full

Output shows:
  - Execution summary
  - Token savings: 18% (XMI OFF only, no cache on first run)
  - Steps to execute: all 9 steps
```

#### Step 4: Execute Each Step

**Step 1: scenario-to-activity-v1**
```
Claude calls: scenario-to-activity-v1
Input: User's business scenario about product management
Output: 
  - product-management_activity-data.json
  - product-management_activity.puml
```

**Step 2: activity-to-usecase-v1**
```
Claude calls: activity-to-usecase-v1
Input: product-management_activity-data.json
Output:
  - product-management_usecase-output.json
  - product-management_usecase-diagram.puml
```

**Step 3-8: Continue similarly...**

#### Step 5: Present Results
```
Claude calls: present_files([
  "product-management_domain-model.json",
  "product-management_class.puml",
  "product-management_validation-report.md",
  ...
])

Claude displays:
  ========================================
  ✅ WORKFLOW COMPLETE
  ========================================
  Token savings: 18% (83,000 vs 101,000)
  All artifacts cached for next run
  ========================================
```

### ✅ Success Criteria
- [ ] All 9 steps executed
- [ ] All output files generated
- [ ] Files presented to user
- [ ] Cache populated
- [ ] Token savings displayed

---

## 🧪 Test Scenario 2: Second Run with Cache / キャッシュ活用2回目

### User Input
```
ユーザー: 「product-managementに在庫追跡機能を追加」
```

### Expected Claude Actions

#### Step 1: Recognize Existing Project
```
Claude recognizes: project_name = "product-management" (existing)
```

#### Step 2: User Questions
```
User selects:
- はい（推奨）← cache
- 指定ステップから再開 → Step 2
- いいえ（推奨）← XMI
```

#### Step 3: Execute run_workflow.py
```bash
python3 /mnt/skills/user/uml-workflow-v3/scripts/run_workflow.py \
  product-management \
  --cache yes \
  --mode resume \
  --start-step 2

Output shows:
  - Step 1: 💾 from cache
  - Step 2-8: 🟢 will execute
  - Token savings: 32% estimated
```

#### Step 4: Cache Restoration
```
Claude sees:
  - Step 1: Cached (automatic restoration)
  - Step 2-8: Execute
  
Actual execution:
  - Step 1: SKIP (cache)
  - Step 2: activity-to-usecase-v1 (execute)
  - Step 3-8: Continue
```

#### Step 5: Present Results
```
Token savings: 32% (69,000 vs 101,000)
Cache used for Step 1
```

### ✅ Success Criteria
- [ ] Step 1 skipped (cached)
- [ ] Steps 2-8 executed
- [ ] Token savings ~32%
- [ ] New artifacts cached

---

## 🧪 Test Scenario 3: Models-Only Mode / モデルのみモード

### User Input
```
ユーザー: 「product-managementのモデルだけ確認したい」
```

### Expected Claude Actions

#### User Selects
```
- はい（推奨）← cache
- モデルのみ
- いいえ（推奨）← XMI
```

#### Execute run_workflow.py
```bash
python3 .../run_workflow.py \
  product-management \
  --cache yes \
  --mode models_only

Output shows:
  - Steps 1-6: Execute/Cache
  - Steps 7-8: SKIP (no code generation)
  - Token savings: ~65% estimated
```

#### Execution
```
Steps 1-2: From cache
Steps 3-6: Execute
Steps 7-8: Skip

Token savings: 65%+
```

### ✅ Success Criteria
- [ ] Code generation skipped
- [ ] Models generated
- [ ] High token savings

---

## 🧪 Test Scenario 4: Validation Only / バリデーションのみ

### User Input
```
ユーザー: 「product-managementのバリデーションだけ実行」
```

### Expected Claude Actions

#### User Selects
```
- バリデーションのみ
```

#### Execute run_workflow.py
```bash
python3 .../run_workflow.py \
  product-management \
  --cache yes \
  --mode validate_only

Output shows:
  - Step 6 only
  - Token savings: 95%
```

#### Execution
```
Step 6: model-validator-v1

Token consumed: ~5,000 (vs 101,000 for full)
```

### ✅ Success Criteria
- [ ] Only validation executed
- [ ] Very high token savings (95%)
- [ ] Quick execution

---

## 🔍 Error Handling Tests / エラーハンドリングテスト

### Test: Missing Sub-Skill

```
Scenario: User hasn't uploaded scenario-to-activity-v1

Expected:
  Claude displays:
  "❌ Error: scenario-to-activity-v1 skill not found
   Please upload the required sub-skills first"
```

### Test: Missing Input File

```
Scenario: Step 2 needs activity-data.json but it's missing

Expected:
  Claude tries cache restoration:
  "⚠️ Missing: activity-data.json
   💾 Attempting cache restoration...
   ✅ Restored from cache" 
   
  OR if not in cache:
  "❌ Not in cache. Please run from Step 1."
```

### Test: Cache Corruption

```
Scenario: Cache file is corrupted

Expected:
  Claude detects error and suggests:
  "⚠️ Cache appears corrupted
   Clearing cache...
   Please re-run workflow"
```

---

## 📊 Token Savings Verification / トークン削減効果の確認

### First Run
```
Expected: ~83,000 tokens (18% savings from XMI OFF)
```

### Second Run (Step 2+)
```
Expected: ~69,000 tokens (32% savings)
```

### Models Only
```
Expected: ~30,000-40,000 tokens (60-70% savings)
```

### Validation Only
```
Expected: ~5,000 tokens (95% savings)
```

---

## ✅ Complete Test Checklist / テストチェックリスト

### Basic Functionality
- [ ] Project name inference works
- [ ] ask_user_input_v0 displays questions
- [ ] run_workflow.py executes successfully
- [ ] Execution plan is displayed
- [ ] All sub-skills are called correctly
- [ ] Output files are generated
- [ ] present_files works

### Cache System
- [ ] First run populates cache
- [ ] Second run uses cache
- [ ] Cache restoration works
- [ ] Cache clearing works
- [ ] Cache status is displayed correctly

### Token Optimization
- [ ] XMI OFF reduces tokens (~18%)
- [ ] Cache reduces tokens (up to 80%)
- [ ] Staged execution reduces tokens (up to 95%)
- [ ] Combined optimization works (up to 75%)

### Error Handling
- [ ] Missing sub-skills detected
- [ ] Missing files handled
- [ ] Cache corruption handled
- [ ] Clear error messages displayed

### User Experience
- [ ] No manual Python execution required
- [ ] Questions are clear
- [ ] Process is automatic
- [ ] Results are well-presented

---

**すべてのテストがパスすれば、完全自動化が実現！**
