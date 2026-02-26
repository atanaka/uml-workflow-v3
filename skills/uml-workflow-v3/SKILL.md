---
name: uml-workflow-v3
description: 10-step UML workflow: scenario→activity→usecase→class→state→sequence→validation→security→code→test→traceability. Caching, resume, single-step modes.
---

# UML Workflow v3

完全統合されたtoken効率化UMLワークフロー。キャッシュ管理・段階的実行・XMI最適化をすべて自動化。

## 🎯 Overview

このスキルは3つの最適化機能を統合：

1. **キャッシュシステム（項目1）**: 中間成果物の自動キャッシュと再利用
2. **段階的実行（項目2）**: 必要なステップのみ実行
3. **XMI最適化（項目3）**: デフォルトでXMI生成OFF（40%高速化）

**最大75%のtoken削減を実現**

---

## 🤖 EXECUTION INSTRUCTIONS FOR CLAUDE

**CRITICAL**: When a user requests to use this skill, Claude MUST follow this exact workflow.

### Trigger Patterns

Execute this workflow when user says:
- "uml-workflow-v3で〜を生成"
- "uml-workflow-v3を使って〜"
- "token効率化ワークフローで〜"
- Any mention of this skill by name

### Quick Execution Steps

```
1. Determine project_name from user's request
2. Ask questions using ask_user_input_v0 tool
3. Execute: bash_tool run_workflow.py with user's answers
4. Read execution plan JSON
5. Call each sub-skill in sequence
6. Present results with present_files
```

**Detail**: See CLAUDE_QUICK_GUIDE.md for concise reference, or follow detailed phases below.

### Execution Workflow (MUST FOLLOW)

Claude will execute this skill by following these phases in order:

1. **Initialization** - Set up Python environment
2. **User Dialogue** - Ask configuration questions using ask_user_input tool
3. **Configuration** - Build execution config using Python scripts
4. **Execution Plan** - Display plan and get confirmation
5. **Step-by-Step Execution** - Execute each step with cache management
6. **Completion** - Present results and statistics

Each phase is detailed below with exact commands to execute.

---

## 📋 PHASE 0: Initialization

**Objective**: Determine project name and set up Python environment

### Step 0.1: Determine Project Name

Claude analyzes the user's request to infer a project name:
- Extract from user's message (e.g., "受注システム" → "order-system")
- Convert to kebab-case (lowercase with hyphens)
- If unclear, ask user directly

**Example**:
```
User: "受注管理システムを生成"
→ project_name = "order-management"

User: "generate an inventory system"
→ project_name = "inventory-system"
```

### Step 0.2: Set Up Python Environment

Claude executes the following bash command to verify Python scripts are accessible:

```bash
ls -la /mnt/skills/user/uml-workflow-v3/scripts/
```

If the directory doesn't exist, try fallback:
```bash
ls -la /mnt/user-data/outputs/uml-workflow-v3-complete/scripts/
```

**Expected output**: 4 Python files should be listed
- workflow_cache_helper.py
- execution_mode_manager.py
- unified_workflow_executor.py
- interactive_workflow_executor.py

If scripts are not found, inform user and suggest re-uploading the skill.

---

## 📋 PHASE 1: User Dialogue

**Objective**: Collect execution configuration from user

Claude uses the `ask_user_input_v0` tool to ask the following questions:

### Question Set

```python
ask_user_input_v0({
    "questions": [
        {
            "question": "キャッシュを使用しますか？",
            "type": "single_select",
            "options": [
                "はい（推奨）- 前回の成果物を再利用してtoken節約",
                "いいえ - すべて新規生成",
                "クリア - キャッシュを削除して新規生成"
            ]
        },
        {
            "question": "実行モードを選択してください",
            "type": "single_select",
            "options": [
                "フルワークフロー（全10ステップ実行）",
                "指定ステップから再開",
                "モデルのみ生成（コード生成なし）",
                "バリデーションのみ実行"
            ]
        },
        {
            "question": "XMIファイルを生成しますか？",
            "type": "single_select",
            "options": [
                "いいえ（推奨）- 40%高速化、18% token削減",
                "はい - UMLツール連携が必要な場合のみ"
            ]
        }
    ]
})
```

### Follow-up Questions

Based on execution mode selection:

**If "指定ステップから再開" selected**:
```python
ask_user_input_v0({
    "questions": [{
        "question": "どのステップから再開しますか？",
        "type": "single_select",
        "options": [
            "Step 2: アクティビティ図 → ユースケース",
            "Step 3: ユースケース → クラス図",
            "Step 4: クラス図 → ステートマシン図",
            "Step 5: ユースケース → シーケンス図",
            "Step 6: モデルバリデーション",
            "Step 7: セキュリティ設計",
            "Step 8: コード生成",
            "Step 9: テスト生成",
            "Step 10: トレーサビリティマトリクス",
            "Step 10: トレーサビリティマトリクス"
        ]
    }]
})
```

**If mode includes code generation**:
```python
ask_user_input_v0({
    "questions": [
        {
            "question": "テストコードを生成しますか？",
            "type": "single_select",
            "options": [
                "はい（推奨）",
                "いいえ"
            ]
        },
        {
            "question": "バックエンドフレームワークを選択してください",
            "type": "single_select",
            "options": [
                "TypeScript + Express（推奨・軽量）",
                "TypeScript + NestJS（大規模向け）",
                "Python + FastAPI",
                "Java + Spring Boot"
            ]
        },
        {
            "question": "フロントエンドフレームワークを選択してください",
            "type": "single_select",
            "options": [
                "React + TypeScript + Vite + Tailwind CSS（推奨）",
                "Vue 3 + TypeScript + Vite",
                "フロントエンドは生成しない"
            ]
        },
        {
            "question": "アーキテクチャを選択してください",
            "type": "single_select",
            "options": [
                "モノリス（推奨・シンプル）",
                "マイクロサービス",
                "サーバーレス"
            ]
        }
    ]
})
```

> ⚠️ **収集したテックスタック選択値は会話コンテキストに記録し、Step 8 で usecase-to-code-v1 を呼び出す際に Case A として渡すこと。Step 8 で再度ユーザーに質問してはならない。**
```

---

## 📋 PHASE 2: Configuration Build

**Objective**: Create execution configuration using Python scripts

### Step 2.1: Map User Responses to Parameters

Based on user's answers, Claude determines:

```python
# Cache setting
cache_param = "yes"  # if user selected "はい（推奨）"
cache_param = "no"   # if user selected "いいえ"
cache_param = "clear" # if user selected "クリア"

# Execution mode
mode_param = "full"          # if "フルワークフロー"
mode_param = "resume"        # if "指定ステップから再開"
mode_param = "models_only"   # if "モデルのみ生成"
mode_param = "validate_only" # if "バリデーションのみ"

# Start step (if resume mode)
start_step = 2  # if user selected "Step 2: アクティビティ図 → ユースケース"
start_step = 3  # if user selected "Step 3: ユースケース → クラス図"
# ... up to step 9

# XMI generation
xmi_flag = ""        # if user selected "いいえ（推奨）"
xmi_flag = "--xmi"   # if user selected "はい"

# Test generation
test_flag = ""          # if user selected "はい（推奨）"
test_flag = "--no-tests" # if user selected "いいえ"
```

### Step 2.2: Execute Configuration Script

Claude executes the run_workflow.py script using bash_tool:

```bash
python3 /mnt/skills/user/uml-workflow-v3/scripts/run_workflow.py \
  {project_name} \
  --cache {cache_param} \
  --mode {mode_param} \
  [--start-step {start_step}] \
  [{xmi_flag}] \
  [{test_flag}]
```

**Example**:
```bash
python3 /mnt/skills/user/uml-workflow-v3/scripts/run_workflow.py \
  order-system \
  --cache yes \
  --mode full
```

**Important**: If the scripts directory is not found at `/mnt/skills/user/uml-workflow-v3/scripts/`, try the fallback location:
```bash
python3 /mnt/user-data/outputs/uml-workflow-v3-complete/scripts/run_workflow.py \
  {project_name} ...
```

### Step 2.3: Parse Script Output

The script outputs:

1. **Cache Status** - Shows which steps have cached data
2. **Execution Summary** - Lists steps that will be executed
3. **Token Savings Estimate** - Predicted token reduction
4. **Execution Plan JSON** - Saved to `/mnt/user-data/outputs/workflow_execution_result_{project_name}.json`

Claude reads this output and extracts:
- List of steps to execute
- List of steps to skip (cached)
- Token savings estimate

---

## 📋 PHASE 3: Execution Plan Display

**Objective**: Show the user what will happen

Claude displays the plan to the user:

```
========================================
Execution Plan - {project_name}
========================================
Mode: {execution_mode}
Cache: {enabled/disabled}
XMI Generation: {enabled/disabled}

Steps to Execute:
  🟢 Step 1: scenario-to-activity-v1
  🟢 Step 2: activity-to-usecase-v1
  💾 Step 3: usecase-to-class-v1 (from cache)
  🟢 Step 4: class-to-statemachine-v1
  ...

Estimated Token Savings: XX%
========================================
```

Claude then proceeds to execution automatically (no additional confirmation needed).

---

## 📋 PHASE 4: Step-by-Step Execution

**Objective**: Execute each step with cache management

### Step 4.1: Load Execution Plan

Claude reads the execution plan from the JSON file:

```python
import json

with open(f'/mnt/user-data/outputs/workflow_execution_result_{project_name}.json') as f:
    plan = json.load(f)

steps_to_execute = plan['steps_executed']
steps_from_cache = plan['steps_from_cache']
```

### Step 4.2: Execute Each Step

For each step in the workflow:

#### General Pattern

```python
for step_name in workflow_steps:
    
    # Check if step should be executed
    if step_name in steps_to_skip:
        print(f"⏭️ Step skipped: {step_name}")
        continue
    
    # Check if cached
    if step_name in steps_from_cache:
        print(f"💾 Using cached: {step_name}")
        # Cache already restored by run_workflow.py
        continue
    
    # Execute the step
    print(f"⚙️ Executing: {step_name}")
    execute_sub_skill(step_name, project_name, config)
    
    # Cache the output
    cache_step_outputs(step_name, project_name)
```

> **Sub-skill reference**: Each step's full implementation is in its SKILL.md under `references/`.
> Before executing a step, Claude MUST read: `view /mnt/skills/user/uml-workflow-v3/references/{skill-name}/SKILL.md`

#### Step 1: scenario-to-activity-v1

**Execution**:

Claude reads `references/scenario-to-activity-v1/SKILL.md`, then executes:

```
Input: User's business scenario (from initial request)
Project name: {project_name}
Language: Auto-detect (Japanese/English)
Generate XMI: {config.generate_xmi}
Output directory: /mnt/user-data/outputs
```

**Expected Outputs**:
- `{project_name}_activity-data.json`
- `{project_name}_activity.puml`
- `{project_name}_activity-model.xmi` (if XMI enabled)

**Cache Storage** (automatic via run_workflow.py or manual):

```bash
python3 -c "
import sys
sys.path.append('/mnt/skills/user/uml-workflow-v3/scripts')
from workflow_cache_helper import cache_file

cache_file('{project_name}', 'scenario_to_activity', 'activity-data',
           '/mnt/user-data/outputs/{project_name}_activity-data.json')
cache_file('{project_name}', 'scenario_to_activity', 'activity-puml',
           '/mnt/user-data/outputs/{project_name}_activity.puml')
"
```

#### Step 2: activity-to-usecase-v1

**Pre-requisites Check**:

```bash
# Check if activity-data.json exists
if [ ! -f "/mnt/user-data/outputs/{project_name}_activity-data.json" ]; then
    # Try to restore from cache
    python3 -c "
import sys
sys.path.append('/mnt/skills/user/uml-workflow-v3/scripts')
from unified_workflow_executor import UnifiedWorkflowExecutor
executor = UnifiedWorkflowExecutor('{project_name}')
from execution_mode_manager import SkillStep
executor.restore_from_cache(SkillStep.SCENARIO_TO_ACTIVITY)
"
fi
```

**Execution**:

Claude reads `references/activity-to-usecase-v1/SKILL.md`, then executes:

```
Input: {project_name}_activity-data.json
Generate XMI: {config.generate_xmi}
```

**Expected Outputs**:
- `{project_name}_usecase-output.json`
- `{project_name}_usecase-diagram.puml`
- `usecase-specifications/*.md` (individual use case files)
- `{project_name}_usecase-model.xmi` (if XMI enabled)

**Cache Storage**:

```bash
python3 -c "
import sys
sys.path.append('/mnt/skills/user/uml-workflow-v3/scripts')
from workflow_cache_helper import cache_file

cache_file('{project_name}', 'activity_to_usecase', 'usecase-output',
           '/mnt/user-data/outputs/{project_name}_usecase-output.json')
cache_file('{project_name}', 'activity_to_usecase', 'usecase-diagram',
           '/mnt/user-data/outputs/{project_name}_usecase-diagram.puml')
"
```

#### Step 3: usecase-to-class-v1

**Pre-requisites Check**:

```bash
# Needs: usecase-output.json AND activity-data.json (for original scenario)
```

**Execution**:

Claude reads `references/usecase-to-class-v1/SKILL.md`, then executes:

```
Input: {project_name}_usecase-output.json
Original scenario: {project_name}_activity-data.json
Generate XMI: {config.generate_xmi}
```

**Expected Outputs**:
- `{project_name}_domain-model.json` ⭐ **CRITICAL - Single Source of Truth**
- `{project_name}_class.puml`
- `{project_name}_architecture-overview.md`
- `{project_name}_class-model.xmi` (if XMI enabled)

**Cache Storage**:

```bash
python3 -c "
import sys
sys.path.append('/mnt/skills/user/uml-workflow-v3/scripts')
from workflow_cache_helper import cache_file

cache_file('{project_name}', 'usecase_to_class', 'domain-model',
           '/mnt/user-data/outputs/{project_name}_domain-model.json')
cache_file('{project_name}', 'usecase_to_class', 'class-puml',
           '/mnt/user-data/outputs/{project_name}_class.puml')
"
```

#### Step 4: class-to-statemachine-v1

**Pre-requisites Check**:

```bash
# Needs: domain-model.json
```

**Execution**:

Claude reads `references/class-to-statemachine-v1/SKILL.md`, then executes:

```
Input: {project_name}_domain-model.json
Language: Inherit from domain model
```

**Expected Outputs**:
- `{project_name}_statemachine.puml` (all state machines)
- `{project_name}_statemachine-{EntityName}.puml` (individual entities)

**Cache Storage**:

```bash
python3 -c "
import sys
sys.path.append('/mnt/skills/user/uml-workflow-v3/scripts')
from workflow_cache_helper import cache_file

cache_file('{project_name}', 'class_to_statemachine', 'statemachine-puml',
           '/mnt/user-data/outputs/{project_name}_statemachine.puml')
"
```

#### Step 5: usecase-to-sequence-v1

**Pre-requisites Check**:

```bash
# Needs: usecase-output.json AND domain-model.json
```

**Execution**:

Claude reads `references/usecase-to-sequence-v1/SKILL.md`, then executes:

```
Input: {project_name}_usecase-output.json
Domain model: {project_name}_domain-model.json
Language: Inherit from use cases
```

**Expected Outputs**:
- `{project_name}_sequence.puml` (all sequences)
- `{project_name}_sequence-{UC-ID}.puml` (per use case)

**Cache Storage**:

```bash
python3 -c "
import sys
sys.path.append('/mnt/skills/user/uml-workflow-v3/scripts')
from workflow_cache_helper import cache_file

cache_file('{project_name}', 'usecase_to_sequence', 'sequence-puml',
           '/mnt/user-data/outputs/{project_name}_sequence.puml')
"
```

#### Step 6: model-validator-v1

**Pre-requisites Check**:

```bash
# Needs: All models in /mnt/user-data/outputs/{project_name}_*
```

**Execution**:

Claude reads `references/model-validator-v1/SKILL.md`, then executes:

```
Input: All generated models
Language: Inherit from models
```

**Expected Outputs**:
- `{project_name}_validation-report.md`
- `{project_name}_validation-summary.json`

**Cache Storage**:

```bash
python3 -c "
import sys
sys.path.append('/mnt/skills/user/uml-workflow-v3/scripts')
from workflow_cache_helper import cache_file

cache_file('{project_name}', 'model_validator', 'validation-report',
           '/mnt/user-data/outputs/{project_name}_validation-report.md')
"
```

#### Step 7: security-design-v1

**Pre-requisites Check**:

```bash
# Needs: domain-model.json AND usecase-output.json AND validation-report.md
```

**Execution**:

Claude reads `references/security-design-v1/SKILL.md`, then executes:

```
Input: {project_name}_domain-model.json
       {project_name}_usecase-output.json
       {project_name}_validation-report.md (optional)
Language: Inherit from models
```

**Expected Outputs**:
- `{project_name}_security-design.md` (セキュリティ設計書)
- `{project_name}_security-config.json` (セキュリティ設定)

**Cache Storage**:

```bash
python3 -c "
import sys
sys.path.append('/mnt/skills/user/uml-workflow-v3/scripts')
from workflow_cache_helper import cache_file

cache_file('{project_name}', 'security_design', 'security-design',
           '/mnt/user-data/outputs/{project_name}_security-design.md')
cache_file('{project_name}', 'security_design', 'security-config',
           '/mnt/user-data/outputs/{project_name}_security-config.json')
"
```

**Security Design Scope**:
- 認証・認可設計（Authentication & Authorization）
- データ保護・暗号化方針
- API セキュリティ（Rate limiting, CORS, Input validation）
- OWASP Top 10 対策
- セキュリティロール・権限マトリクス
- 監査ログ設計

#### Step 8: usecase-to-code-v1

**Pre-requisites Check**:

```bash
# Needs: domain-model.json AND usecase-output.json
```

**Execution**:

> ⚠️ **IMPORTANT — テックスタックの質問は Phase 1 で実施済み**
>
> このワークフローでは Phase 1（起動時）でユーザーから `backend_framework`, `frontend_framework`, `architecture`, テスト要否 を収集している。**Step 8 でユーザーに再度質問してはならない**。usecase-to-code-v1 の Step 2 はすでに決定済みの値を使用する（Case A）。

Claude reads `references/usecase-to-code-v1/SKILL.md`, then executes with the tech stack already selected in Phase 1:

```
Input: {project_name}_domain-model.json
       {project_name}_usecase-output.json
Tech stack: {phase1_selected_stack}   ← Phase 1 の選択値をそのまま渡す
Architecture: {phase1_architecture}
```

**⚠️ フロントエンド生成の必須確認（最重要）**

`frontend_framework != "none"` の場合、コード生成後に以下を**必ず実行**して実際のファイル存在を確認すること:

```bash
find /home/claude/{project_name}/frontend/src -type f | sort
```

期待される最低限のファイル:
- `frontend/src/App.tsx` (または同等)
- `frontend/src/types/index.ts`
- `frontend/src/api/client.ts`
- `frontend/src/pages/` 以下に各ユースケース対応ページ

**もし上記ファイルが存在しない、または `{components,pages,api}` という名前のディレクトリのみが存在する場合は、フロントエンドコードが未生成（bash brace expansion 問題）なので、即座に生成すること。Step 9 に進んではならない。**

**Expected Outputs**:
- Complete application in `{project_name}/` directory
  - `backend/` — ドメイン・サービス・ルート
  - `frontend/` — UI コンポーネント・ページ・API クライアント
  - `README.md`
  - `docker-compose.yml`

**Note**: Code generation outputs are typically NOT cached (too large and frequently modified)

#### Step 9: usecase-to-test-v1

**Pre-requisites Check**:

```bash
# Needs: domain-model.json AND usecase-output.json
```

**Execution**:

Claude reads `references/usecase-to-test-v1/SKILL.md`, then executes:

```
Input: {project_name}_domain-model.json
       {project_name}_usecase-output.json
Test frameworks: Jest/Vitest/Playwright/Cypress (auto-selected based on tech stack)
```

**Expected Outputs**:
- Unit tests
- Integration tests
- E2E tests
- Test documentation

---

#### Step 10: traceability-matrix-v1

**Pre-requisites Check**:

```bash
# Needs: usecase-output.json (required)
# Recommended: domain-model.json, security-config.json, src/, tests/
```

**Execution**:

Claude reads `references/traceability-matrix-v1/SKILL.md`, then executes:

```
Input: All pipeline artifacts in output directory
       {project_name}_usecase-output.json (required)
       usecase-specifications/UC-*.md (required)
       {project_name}_domain-model.json (recommended)
       {project_name}_security-config.json (recommended)
       src/ directory (if code generated)
       tests/ directory (if tests generated)
```

**Expected Outputs**:
- `{project_name}_traceability-matrix.json` (machine-readable full matrix)
- `{project_name}_traceability-matrix.md` (human-readable report with gap analysis)

**Note**: This step reads all previously generated artifacts. It does not participate in caching since it aggregates from other cached outputs.

---

## 📋 PHASE 5: Completion and Presentation

**Objective**: Present results to user and provide guidance

### Step 5.1: Collect All Outputs

Claude collects all generated files:

```bash
ls -la /mnt/user-data/outputs/{project_name}*
```

### Step 5.2: Present Files to User

Claude uses the present_files tool to make files available:

```python
present_files([
    "/mnt/user-data/outputs/{project_name}_domain-model.json",
    "/mnt/user-data/outputs/{project_name}_class.puml",
    "/mnt/user-data/outputs/{project_name}_validation-report.md",
    # ... other key files
])
```

### Step 5.3: Display Completion Summary

Claude displays:

```
========================================
✅ WORKFLOW COMPLETE
========================================
Project: {project_name}
Mode: {execution_mode}

Generated Artifacts:
  📄 UML Models: 8 files
  📊 Diagrams: 5 types
  💻 Application Code: {if generated}
  🧪 Test Code: {if generated}
  
Token Usage:
  Full workflow: 101,000 tokens
  This execution: {actual_tokens} tokens
  Savings: {savings_percent}% ({saved_tokens} tokens)
  
Cache Status:
  Cached steps: {cached_count}
  New executions: {executed_count}
  
Next Steps:
  - Review validation report
  - Test generated application
  - Next run will use cache for {cache_percent}% more savings
========================================
```

### Step 5.4: Provide Next Run Guidance

Claude informs the user:

```
💡 For your next execution:

1. To add features:
   "uml-workflow-v3で{project_name}に{新機能}を追加"
   → Will use cache for unchanged steps (~30% token savings)

2. To regenerate models only:
   Select "モデルのみ" mode
   → Skips code generation (~33% token savings)

3. To validate only:
   Select "バリデーションのみ" mode
   → Fastest check (~95% token savings)

Cache is ready for next run! 💾
```

---

## 🚨 ERROR HANDLING

### Missing Pre-requisites

If a step's required input files are missing:

```python
if not file_exists(required_file):
    print(f"❌ Error: Missing required file: {required_file}")
    print(f"   Required for: {current_step}")
    print(f"   ")
    print(f"   Attempting to restore from cache...")
    
    if restore_from_cache_successful:
        print(f"   ✅ Restored from cache")
        continue
    else:
        print(f"   ❌ Not in cache")
        print(f"   ")
        print(f"   Please run from an earlier step:")
        print(f"   - Use 'resume from Step X' mode")
        print(f"   - Or use 'full workflow' mode")
        return ERROR
```

### Sub-skill Execution Failure

If a sub-skill fails:

```python
try:
    execute_sub_skill(step_name)
except Exception as e:
    print(f"❌ Error executing {step_name}: {e}")
    print(f"   ")
    print(f"   Options:")
    print(f"   1. Retry this step")
    print(f"   2. Skip and continue")
    print(f"   3. Abort workflow")
    
    # Claude asks user what to do
    user_choice = ask_user_input(...)
    
    if user_choice == "retry":
        # Retry
    elif user_choice == "skip":
        continue
    else:
        return ERROR
```

### Cache Corruption

If cache appears corrupted:

```bash
python3 -c "
from workflow_cache_helper import clear_project_cache
clear_project_cache('{project_name}')
print('Cache cleared. Please re-run workflow.')
"
```

---

## 📊 TOKEN OPTIMIZATION IN ACTION

### Example Execution Flows

#### First Run (No Cache)

```
User: "uml-workflow-v3で受注システムを生成"

Tokens consumed:
  - XMI OFF: 83,000 tokens (18% savings vs baseline)
  
Files cached: All intermediate outputs
```

#### Second Run (With Cache - Feature Addition)

```
User: "order-systemに在庫管理機能を追加"
Mode: Resume from Step 2

Tokens consumed:
  - Step 1: 0 (from cache)
  - Step 2-9: 77,000 tokens
  - XMI OFF savings: -12,000
  - Total: 69,000 tokens (32% savings)
```

#### Third Run (Model Refinement)

```
User: "order-systemのクラス図を調整"
Mode: Resume from Step 3, Models only

Tokens consumed:
  - Step 1-2: 0 (from cache)
  - Step 3-7: 38,200 tokens (models only)
  - Total: 30,200 tokens (70% savings)
```

---

## ✅ SUCCESS CRITERIA

Workflow is considered successfully complete when:

1. ✅ All selected steps executed without errors
2. ✅ All expected output files are generated
3. ✅ Validation report shows no critical issues
4. ✅ Files are presented to user via present_files
5. ✅ Cache is updated for next run
6. ✅ Token savings are calculated and displayed

---

**This completes the SKILL.md implementation. Claude can now execute this workflow fully automatically.**

## 🔧 Step-by-Step Execution Details

### Step 1: scenario-to-activity-v1

```python
def execute_step_1(project_name, config, business_scenario):
    """Step 1: シナリオからアクティビティ図を生成"""
    
    print(f"📝 ビジネスシナリオを分析してアクティビティ図を生成...")
    
    # scenario-to-activity-v1を実行
    # （実際のスキル呼び出しはClaude側で実行）
    
    # 重要: generate_xmi設定を渡す
    # このスキルは内部でjson-to-modelsを呼び出すため
    
    """
    # Read: references/scenario-to-activity-v1/SKILL.md
    Claude calls scenario-to-activity-v1 with:
    - Input: business_scenario
    - Language: auto-detect or user-specified
    - XMI generation: config.generate_xmi (デフォルトFalse)
    
    Output files:
    - {project_name}_activity-data.json
    - {project_name}_activity.puml
    - {project_name}_activity-model.xmi (if generate_xmi=True)
    """
    
    print(f"✅ Step 1 完了")
```

### Step 2: activity-to-usecase-v1

```python
def execute_step_2(project_name, config):
    """Step 2: アクティビティ図からユースケースを抽出"""
    
    # 依存ファイルチェック
    activity_data = f"/mnt/user-data/outputs/{project_name}_activity-data.json"
    
    if not os.path.exists(activity_data):
        # キャッシュから復元を試みる
        cached = executor.get_cached_file(
            project_name,
            "scenario_to_activity",
            "activity-data"
        )
        if cached:
            import shutil
            shutil.copy2(cached, activity_data)
        else:
            print(f"❌ 必須ファイルが見つかりません: {activity_data}")
            print(f"   Step 1を先に実行してください")
            return False
    
    print(f"📝 アクティビティ図からユースケースを抽出...")
    
    """
    # Read: references/activity-to-usecase-v1/SKILL.md
    Claude calls activity-to-usecase-v1 with:
    - Input: {project_name}_activity-data.json
    - XMI generation: config.generate_xmi
    
    Output files:
    - {project_name}_usecase-output.json
    - {project_name}_usecase-diagram.puml
    - usecase-specifications/*.md (個別ユースケース仕様)
    - {project_name}_usecase-model.xmi (if generate_xmi=True)
    """
    
    print(f"✅ Step 2 完了")
    return True
```

### Step 3: usecase-to-class-v1

```python
def execute_step_3(project_name, config):
    """Step 3: ユースケースからクラス図を生成"""
    
    # 依存ファイルチェック
    usecase_output = f"/mnt/user-data/outputs/{project_name}_usecase-output.json"
    
    if not os.path.exists(usecase_output):
        # キャッシュから復元
        cached = executor.get_cached_file(
            project_name,
            "activity_to_usecase",
            "usecase-output"
        )
        if cached:
            import shutil
            shutil.copy2(cached, usecase_output)
        else:
            print(f"❌ 必須ファイルが見つかりません: {usecase_output}")
            return False
    
    # 元のシナリオ情報も必要
    activity_data = f"/mnt/user-data/outputs/{project_name}_activity-data.json"
    if not os.path.exists(activity_data):
        cached = executor.get_cached_file(
            project_name,
            "scenario_to_activity",
            "activity-data"
        )
        if cached:
            import shutil
            shutil.copy2(cached, activity_data)
    
    print(f"📝 ユースケースからクラス図を生成...")
    
    """
    # Read: references/usecase-to-class-v1/SKILL.md
    Claude calls usecase-to-class-v1 with:
    - Input: {project_name}_usecase-output.json
    - Original scenario: {project_name}_activity-data.json
    - XMI generation: config.generate_xmi
    
    Output files:
    - {project_name}_domain-model.json (⭐ Single Source of Truth)
    - {project_name}_class.puml
    - {project_name}_architecture-overview.md
    - {project_name}_class-model.xmi (if generate_xmi=True)
    """
    
    print(f"✅ Step 3 完了")
    print(f"⭐ domain-model.json生成 - これ以降のすべてのステップの基準")
    return True
```

### Step 4: class-to-statemachine-v1

```python
def execute_step_4(project_name, config):
    """Step 4: クラス図からステートマシン図を生成"""
    
    # 依存ファイル
    domain_model = f"/mnt/user-data/outputs/{project_name}_domain-model.json"
    
    if not os.path.exists(domain_model):
        cached = executor.get_cached_file(
            project_name,
            "usecase_to_class",
            "domain-model"
        )
        if cached:
            import shutil
            shutil.copy2(cached, domain_model)
        else:
            print(f"❌ 必須ファイルが見つかりません: {domain_model}")
            return False
    
    print(f"📝 ステータス属性を持つエンティティのステートマシン図を生成...")
    
    """
    # Read: references/class-to-statemachine-v1/SKILL.md
    Claude calls class-to-statemachine-v1 with:
    - Input: {project_name}_domain-model.json
    - Language: inherit from domain model
    
    Output files:
    - {project_name}_statemachine.puml (すべてのステートマシン)
    - {project_name}_statemachine-{EntityName}.puml (個別エンティティ)
    """
    
    print(f"✅ Step 4 完了")
    return True
```

### Step 5: usecase-to-sequence-v1

```python
def execute_step_5(project_name, config):
    """Step 5: ユースケースからシーケンス図を生成"""
    
    # 依存ファイル
    usecase_output = f"/mnt/user-data/outputs/{project_name}_usecase-output.json"
    domain_model = f"/mnt/user-data/outputs/{project_name}_domain-model.json"
    
    # キャッシュから復元（必要に応じて）
    # ... (Step 3と同様)
    
    print(f"📝 各ユースケースのシーケンス図を生成...")
    
    """
    # Read: references/usecase-to-sequence-v1/SKILL.md
    Claude calls usecase-to-sequence-v1 with:
    - Input: {project_name}_usecase-output.json, {project_name}_domain-model.json
    - Language: inherit from use cases
    
    Output files:
    - {project_name}_sequence.puml (すべてのシーケンス図)
    - {project_name}_sequence-{UC-ID}.puml (ユースケース別)
    """
    
    print(f"✅ Step 5 完了")
    return True
```

### Step 6: model-validator-v1

```python
def execute_step_6(project_name, config):
    """Step 6: モデルバリデーション"""
    
    print(f"🔍 UMLモデルの検証を実行...")
    
    """
    # Read: references/model-validator-v1/SKILL.md
    Claude calls model-validator-v1 with:
    - Input: all generated models in /mnt/user-data/outputs/{project_name}_*
    - Language: inherit from models
    
    Validation includes:
    - Cross-model consistency
    - Business rule compliance
    - Traceability verification
    - Quality metrics
    
    Output files:
    - {project_name}_validation-report.md
    - {project_name}_validation-summary.json
    """
    
    print(f"✅ Step 6 完了 - バリデーションレポート生成")
    return True
```

### Step 7: security-design-v1

```python
def execute_step_7(project_name, config):
    """Step 7: セキュリティ設計"""
    
    if not config.run_security:
        print(f"⏭️ Step 7 SKIP - セキュリティ設計が無効")
        return True
    
    # 依存ファイル
    domain_model = f"/mnt/user-data/outputs/{project_name}_domain-model.json"
    usecase_output = f"/mnt/user-data/outputs/{project_name}_usecase-output.json"
    
    # キャッシュから復元（必要に応じて）
    # ...
    
    print(f"🔒 セキュリティ設計を生成...")
    
    """
    # Read: references/security-design-v1/SKILL.md
    Claude calls security-design-v1 with:
    - Input: {project_name}_domain-model.json, {project_name}_usecase-output.json
    - Validation report: {project_name}_validation-report.md (optional)
    - Language: inherit from models
    
    Security design includes:
    - 認証・認可設計 (Authentication & Authorization)
    - データ保護・暗号化方針
    - API セキュリティ (Rate limiting, CORS, Input validation)
    - OWASP Top 10 対策
    - セキュリティロール・権限マトリクス
    - 監査ログ設計
    
    Output files:
    - {project_name}_security-design.md (セキュリティ設計書)
    - {project_name}_security-config.json (セキュリティ設定)
    """
    
    print(f"✅ Step 7 完了 - セキュリティ設計生成")
    return True
```

### Step 8: usecase-to-code-v1

```python
def execute_step_8(project_name, config):
    """Step 8: コード生成"""
    
    if not config.generate_code:
        print(f"⏭️ Step 8 SKIP - コード生成が無効")
        return True
    
    # 依存ファイル
    domain_model = f"/mnt/user-data/outputs/{project_name}_domain-model.json"
    usecase_output = f"/mnt/user-data/outputs/{project_name}_usecase-output.json"
    
    # キャッシュから復元（必要に応じて）
    # ...
    
    print(f"💻 フルスタックアプリケーションを生成...")
    
    # 技術スタック選択（対話的またはデフォルト）
    tech_stack = select_tech_stack()  # ユーザーに確認
    
    """
    # Read: references/usecase-to-code-v1/SKILL.md
    Claude calls usecase-to-code-v1 with:
    - Input: {project_name}_domain-model.json, {project_name}_usecase-output.json
    - Tech stack: selected by user or default
    - Architecture: monolith/microservices/serverless
    
    Output:
    - Complete application in {project_name}/ directory
    - Backend + Frontend + Infrastructure
    - Docker configuration
    - Documentation
    """
    
    print(f"✅ Step 8 完了 - アプリケーション生成")
    return True
```

### Step 9: usecase-to-test-v1

```python
def execute_step_9(project_name, config):
    """Step 9: テスト生成"""
    
    if not config.generate_tests:
        print(f"⏭️ Step 9 SKIP - テスト生成が無効")
        return True
    
    print(f"🧪 テストコードを生成...")
    
    """
    # Read: references/usecase-to-test-v1/SKILL.md
    Claude calls usecase-to-test-v1 with:
    - Input: {project_name}_domain-model.json, {project_name}_usecase-output.json
    - Security config: {project_name}_security-config.json (if available)
    - Test frameworks: Jest/Vitest/Playwright/Cypress
    
    Output:
    - Unit tests
    - Integration tests
    - E2E tests
    - Test documentation
    """
    
    print(f"✅ Step 9 完了 - テスト生成")
    return True
```

### Step 10: traceability-matrix-v1

```python
def execute_step_10(project_name, config):
    """Step 10: トレーサビリティマトリクス生成"""
    
    print(f"📊 トレーサビリティマトリクスを生成...")
    
    """
    # Read: references/traceability-matrix-v1/SKILL.md
    Claude calls traceability-matrix-v1 with:
    - Input: All artifacts in project output directory
    - Required: {project_name}_usecase-output.json, usecase-specifications/UC-*.md
    - Recommended: domain-model.json, security-config.json, src/, tests/
    
    Output:
    - {project_name}_traceability-matrix.json
    - {project_name}_traceability-matrix.md
    """
    
    print(f"✅ Step 10 完了 - トレーサビリティマトリクス生成")
    return True
```

## 📊 Token Optimization Summary

### Individual Optimizations

| 機能 | 削減率 | 削減量（概算） |
|-----|-------|--------------|
| キャッシュ（Step 1-2スキップ） | 30% | 33,000 tokens |
| 段階的実行（モデルのみ） | 30% | 33,000 tokens |
| XMI生成OFF | 16% | 18,000 tokens |
| セキュリティ設計スキップ | 7% | 8,000 tokens |

### Combined Optimizations

**最適シナリオ**: Step 3から再開 + XMI OFF + キャッシュ

```
フルワークフロー（XMI ON）: 109,000 tokens

最適化後:
  Step 1-2: キャッシュから復元 → 0 tokens
  Step 3: 再生成（XMI OFF） → 7,200 tokens
  Step 4-7: 実行 → 31,000 tokens
  Step 8-9: スキップ → 0 tokens
  
合計: 38,200 tokens

削減: 70,800 tokens (65%削減)

さらにコード生成を含める場合:
  Step 8-9: 実行 → 33,000 tokens
  合計: 71,200 tokens (35%削減)
```

## 🎯 Usage Examples

### Example 1: First-Time Full Generation

```
User: "受注管理システムのビジネスシナリオから完全なアプリを生成して"

Claude:
  質問1: プロジェクト名 → "order-management"
  質問2: キャッシュ使用 → はい
  質問3: 実行モード → フルワークフロー
  質問4: XMI生成 → いいえ（推奨）
  質問5: テスト生成 → はい
  
実行:
  Step 1-9 すべて実行
  すべてキャッシュに保存
  
Result: 完全なアプリケーション + すべてキャッシュ済み
```

### Example 2: Iterative Development

```
User: "order-managementに在庫管理機能を追加"

Claude:
  質問1: プロジェクト名 → "order-management"（既存）
  質問2: キャッシュ使用 → はい
  質問3: 実行モード → Step 2から再開（アクティビティ図は変わらない）
  質問4: XMI生成 → いいえ
  
実行:
  Step 1: キャッシュから復元（ユーザー確認）
  Step 2-9: 再生成
  
Token削減: 約20-30%
```

### Example 3: Model Refinement Only

```
User: "クラス図だけ再生成して確認したい"

Claude:
  質問1: プロジェクト名 → "order-management"
  質問2: キャッシュ使用 → はい
  質問3: 実行モード → モデルのみ（コード生成なし）
  質問4: XMI生成 → いいえ
  
実行:
  Step 1-2: キャッシュから復元
  Step 3-7: 実行
  Step 8-9: スキップ
  
Token削減: 約75%
```

### Example 4: Validation Check

```
User: "モデルのバリデーションだけ実行"

Claude:
  質問3: 実行モード → バリデーションのみ
  
実行:
  Step 6のみ実行
  
Token削減: 約95%
```

## ⚙️ Configuration Options

### Execution Modes

1. **フルワークフロー**: すべてのステップを実行（10ステップ）
2. **指定ステップから再開**: Step 1-9から開始点を選択
3. **モデルのみ生成**: Step 1-7（コード生成なし）
4. **単一スキル**: 1つのステップのみ実行
5. **バリデーションのみ**: Step 6のみ

### Cache Management

- **使用**: 前回の成果物を再利用（推奨）
- **不使用**: すべて新規生成
- **クリア**: キャッシュを削除して新規生成

### XMI Generation

- **OFF（推奨）**: PlantUML + JSONのみ、40%高速化
- **ON**: UMLツール連携が必要な場合のみ

### Test Generation

- **ON（デフォルト）**: 包括的なテストコード生成
- **OFF**: テスト生成スキップ

## 🔍 Cache Management Commands

### View Cache Status

```python
from workflow_cache_helper import get_project_cache_summary, list_cached_projects

# すべてのキャッシュプロジェクト
projects = list_cached_projects()
print(f"キャッシュされているプロジェクト: {projects}")

# 特定プロジェクトの詳細
summary = get_project_cache_summary("order-management")
for step in summary['steps']:
    print(f"{step['step_name']}: {len(step['files'])} files")
```

### Clear Cache

```python
from workflow_cache_helper import clear_project_cache

# プロジェクト全体をクリア
clear_project_cache("order-management")
```

## 🚨 Error Handling

### Missing Dependencies

```
ステップ実行時に必須ファイルが見つからない場合:
1. キャッシュから自動復元を試みる
2. 復元できない場合、エラーメッセージ表示
3. 必要なステップを先に実行するよう案内
```

### Cache Corruption

```
キャッシュが破損している場合:
1. キャッシュをクリア
2. 該当ステップを再実行
```

### Disk Space

```
キャッシュがディスク容量を圧迫する場合:
1. 古いプロジェクトのキャッシュを削除
2. 使用頻度の低いプロジェクトを整理
```

## 📋 Best Practices

### For Maximum Efficiency

1. **初回は必ずキャッシュ有効**: 次回以降の効率化
2. **変更のない部分は再利用**: キャッシュを積極的に活用
3. **XMIは必要時のみ**: デフォルトOFFを維持
4. **段階的な開発**: 小さい変更を繰り返す

### For Quality

1. **定期的にバリデーション実行**: Step 6単独実行
2. **大きな変更時はフル再生成**: キャッシュクリアして実行
3. **コード生成前にモデル確認**: モデルのみモードで検証

### For Cost Optimization

1. **開発フェーズ**: モデルのみ（Step 1-7）
2. **検証フェーズ**: バリデーションのみ（Step 6）
3. **最終フェーズ**: コード生成（Step 8-9）

## 📚 Related Files

このスキルは以下のPythonモジュールを利用：

- `workflow_cache_helper.py` - キャッシュ管理
- `execution_mode_manager.py` - 実行モード管理
- `unified_workflow_executor.py` - 統合実行管理
- `interactive_workflow_executor.py` - Token推定

これらは `/mnt/user-data/outputs/` に配置。

## 🎉 Success Criteria

ワークフロー実行完了時、以下が達成されていること：

1. ✅ すべての必要なモデルが生成されている
2. ✅ バリデーションをパスしている
3. ✅ （コード生成の場合）実行可能なアプリケーションがある
4. ✅ すべての成果物がキャッシュされている
5. ✅ Token消費が最適化されている

---

**このスキルで、uml-workflow-v2の完全なtoken最適化版が実現されます。**
