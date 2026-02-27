---
name: uml-workflow-v3
description: "10-step UML workflow: scenario→activity→usecase→class→state→sequence→validation→security→code→test→traceability. Caching, resume, single-step modes."
---

# UML Workflow v3

完全統合されたtoken効率化UMLワークフロー。キャッシュ管理・段階的実行・XMI最適化をすべて自動化。

## 🎯 Overview / 概要

このスキルは3つの最適化機能を統合：

1. **キャッシュシステム（項目1）**: 中間成果物の自動キャッシュと再利用
2. **段階的実行（項目2）**: 必要なステップのみ実行
3. **XMI最適化（項目3）**: デフォルトでXMI生成OFF（40%高速化）

**最大75%のtoken削減を実現**

---

## 🤖 EXECUTION INSTRUCTIONS FOR CLAUDE / Claude実行指示

**CRITICAL**: When a user requests to use this skill, Claude MUST follow this exact workflow.

### Trigger Patterns / トリガーパターン

Execute this workflow when user says:
- "uml-workflow-v3で〜を生成"
- "uml-workflow-v3を使って〜"
- "token効率化ワークフローで〜"
- Any mention of this skill by name

### Quick Execution Steps / クイック実行手順

```
1. Determine project_name from user's request
2. Ask questions using ask_user_input_v0 tool
3. Execute: bash_tool run_workflow.py with user's answers
4. Read execution plan JSON
5. Call each sub-skill in sequence
6. Present results with present_files
```

**Detail**: See CLAUDE_QUICK_GUIDE.md for concise reference, or follow detailed phases below.

### Execution Workflow (MUST FOLLOW) / 実行ワークフロー

Claude will execute this skill by following these phases in order:

1. **Initialization** - Set up Python environment
2. **User Dialogue** - Ask configuration questions using ask_user_input tool
3. **Configuration** - Build execution config using Python scripts
4. **Execution Plan** - Display plan and get confirmation
5. **Step-by-Step Execution** - Execute each step with cache management
6. **Completion** - Present results and statistics

Each phase is detailed below with exact commands to execute.

### ⚠️ CRITICAL: 2-Phase Auto-Split Architecture / 2フェーズ自動分割

**Problem**: Running all 10 steps in a single conversation exhausts the context window (~200K tokens). Step 8 (code generation) requires reading the largest PIPELINE.md (~14K tokens) plus generating substantial code output, which causes failures around Step 8.

**Solution**: The workflow automatically splits into 2 phases:

| Phase | Steps | Purpose | Context Usage |
|-------|-------|---------|---------------|
| **Phase A** | 1-7 | Modeling & Validation | ~80K tokens |
| **Phase B** | 8-10 | Code Gen, Test Gen, Traceability | ~60K tokens |

**AUTO-SPLIT RULES**:

1. **Full Workflow mode**: After completing Step 7, Claude MUST:
   - Present all Phase A outputs via `present_files`
   - Cache all outputs
   - Inform user: "Phase A (Modeling) complete. Please start a **new conversation** and say: `uml-workflow-v3で{project_name}のStep 8から再開`"
   - **STOP execution.** Do NOT proceed to Step 8 in the same conversation.

2. **Resume from Step 8+ mode**: Claude loads cached artifacts and executes Steps 8-10 in a fresh context.

3. **Models-only mode**: Steps 1-7 only — no split needed.

4. **Exception**: If user explicitly says "continue in this conversation" or "このまま続行", Claude may attempt Steps 8+ but should warn about potential context limits.

---

## 📋 PHASE 0: Initialization / 初期化

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

## 📋 PHASE 1: User Dialogue / ユーザー対話

**Objective**: Collect execution configuration from user

Claude uses the `ask_user_input_v0` tool to ask the following questions:

### Question Set / 質問セット

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

### Follow-up Questions / 追加質問

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

## 📋 PHASE 2: Configuration Build / 設定構築

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

## 📋 PHASE 3: Execution Plan Display / 実行計画の表示

**Objective**: Show the user what will happen

Claude displays the plan to the user:

```
========================================
Execution Plan - {project_name}
========================================
Mode: {execution_mode}
Cache: {enabled/disabled}
XMI Generation: {enabled/disabled}

Phase A (Modeling - Steps 1-7):
  🟢 Step 1: scenario-to-activity-v1
  🟢 Step 2: activity-to-usecase-v1
  💾 Step 3: usecase-to-class-v1 (from cache)
  🟢 Step 4: class-to-statemachine-v1
  🟢 Step 5: usecase-to-sequence-v1
  🟢 Step 6: model-validator-v1
  🟢 Step 7: security-design-v1

Phase B (Code Generation - Steps 8-10):
  → Will execute in a NEW conversation after Phase A
  🟢 Step 8: usecase-to-code-v1
  🟢 Step 9: usecase-to-test-v1
  🟢 Step 10: traceability-matrix-v1

⚠️ Full Workflow = Phase A now → Phase B in new conversation
========================================
```

Claude then proceeds to Phase A execution automatically (no additional confirmation needed).

---

## 📋 PHASE 4: Step-by-Step Execution / ステップ実行

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

> **Sub-skill reference**: Each step's full implementation is in its PIPELINE.md under `references/`.
> Before executing a step, Claude MUST read: `view /mnt/skills/user/uml-workflow-v3/references/{skill-name}/PIPELINE.md`

#### Step 1: scenario-to-activity-v1

**Execution**:

Claude reads `references/scenario-to-activity-v1/PIPELINE.md`, then executes:

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

Claude reads `references/activity-to-usecase-v1/PIPELINE.md`, then executes:

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

Claude reads `references/usecase-to-class-v1/PIPELINE.md`, then executes:

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

Claude reads `references/class-to-statemachine-v1/PIPELINE.md`, then executes:

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

Claude reads `references/usecase-to-sequence-v1/PIPELINE.md`, then executes:

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

Claude reads `references/model-validator-v1/PIPELINE.md`, then executes:

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

Claude reads `references/security-design-v1/PIPELINE.md`, then executes:

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

---

### ⚠️ AUTO-SPLIT CHECKPOINT — After Step 7 / Step 7完了後の自動分割

**CRITICAL**: After Step 7 completes, Claude MUST execute the following:

```
IF execution_mode == "full" AND steps_include(8, 9, 10):
    1. Cache all Step 1-7 outputs (if not already cached)
    2. Present all Phase A files to user via present_files
    3. Display Phase A completion summary:
    
    ========================================
    ✅ PHASE A COMPLETE (Modeling & Validation)
    ========================================
    Project: {project_name}
    Steps completed: 1-7
    
    Generated Artifacts:
      📄 Activity Diagram
      📋 Use Cases (JSON + MD specifications)
      📊 Class Diagram (domain-model.json — SSoT)
      🔄 State Machine Diagrams
      🔀 Sequence Diagrams
      ✅ Validation Report
      🔒 Security Design + Config
    
    All outputs cached for Phase B.
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    📢 NEXT: Start a NEW conversation and say:
    
    「uml-workflow-v3で{project_name}のStep 8から再開」
    
    Tech stack: {selected_backend} + {selected_frontend}
    Architecture: {selected_architecture}
    Tests: {yes/no}
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    4. STOP. Do NOT proceed to Step 8.
    
ELSE IF execution_mode == "models_only":
    → Proceed to PHASE 5 (Completion)
    
ELSE IF execution_mode == "resume" AND start_step >= 8:
    → Proceed to Step 8 directly (Phase B)
```

#### Step 8: usecase-to-code-v1

**Pre-requisites Check**:

```bash
# Needs: domain-model.json AND usecase-output.json AND security-config.json
# These should be in cache from Phase A — restore if needed
python3 -c "
import sys, os
sys.path.append('/mnt/skills/user/uml-workflow-v3/scripts')
from workflow_cache_helper import restore_all_cached_files
restore_all_cached_files('{project_name}')
"
ls /mnt/user-data/outputs/{project_name}_domain-model.json
ls /mnt/user-data/outputs/{project_name}_usecase-output.json
```

**Execution**:

> ⚠️ **IMPORTANT — テックスタックの質問は Phase 1 で実施済み**
>
> Phase B（Step 8から再開）の場合、ユーザーのメッセージからテックスタック情報を取得する。
> Phase A完了時に表示されたテックスタック情報をユーザーがコピーして送ってくるため、
> そこから backend_framework, frontend_framework, architecture を読み取る。
> **Step 8 でユーザーに再度質問してはならない**。

Claude reads `references/usecase-to-code-v1/PIPELINE.md`, then executes:

```
Input: {project_name}_domain-model.json
       {project_name}_usecase-output.json
       {project_name}_security-config.json
Tech stack: {phase1_selected_stack}
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

**もし上記ファイルが存在しない場合は、フロントエンドコードが未生成なので、即座に生成すること。Step 9 に進んではならない。**

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

Claude reads `references/usecase-to-test-v1/PIPELINE.md`, then executes:

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

Claude reads `references/traceability-matrix-v1/PIPELINE.md`, then executes:

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

## 📋 PHASE 5: Completion and Presentation / 完了・成果物提示

**Objective**: Present results to user and provide guidance

### Phase A Completion (Steps 1-7)

If executing Phase A (modeling), follow the AUTO-SPLIT CHECKPOINT above.
Present all model artifacts and instruct user to start Phase B.

### Phase B Completion (Steps 8-10) / Full Completion

Claude collects all generated files:

```bash
ls -la /mnt/user-data/outputs/{project_name}*
ls -la /home/claude/{project_name}/
```

Claude uses the present_files tool and displays:

```
========================================
✅ WORKFLOW COMPLETE
========================================
Project: {project_name}
Phases completed: A + B (Full)

Generated Artifacts:
  📄 UML Models: 8 files
  📊 Diagrams: 5 types
  💻 Application Code: backend + frontend
  🧪 Test Code: unit + integration + E2E
  📊 Traceability Matrix
  
Cache Status: All steps cached for next run.

💡 Next run: 
  - Add features: "uml-workflow-v3で{project_name}に{新機能}を追加"
  - Models only: Select "モデルのみ" mode
  - Validate only: Select "バリデーションのみ" mode
========================================
```

---

## 🚨 ERROR HANDLING / エラーハンドリング

- **Missing pre-requisites**: Auto-restore from cache → if fail, inform user to run from earlier step
- **Sub-skill failure**: Offer retry/skip/abort options via `ask_user_input_v0`
- **Cache corruption**: Clear cache with `clear_project_cache('{project_name}')` and re-run

## ✅ SUCCESS CRITERIA / 成功基準

1. ✅ All selected steps executed without errors
2. ✅ All expected output files generated
3. ✅ Validation report shows no critical issues
4. ✅ Files presented to user via present_files
5. ✅ Cache updated for next run

**This completes the SKILL.md implementation. Claude can now execute this workflow fully automatically.**
