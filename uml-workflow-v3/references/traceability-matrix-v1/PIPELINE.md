
# Traceability Matrix Generator v1

Generate end-to-end traceability matrices from UML Workflow pipeline artifacts.

## Overview / 概要

This skill reads all artifacts produced by the UML Workflow v2.3 pipeline and generates a consolidated traceability matrix that links:

**Scenario → Activity → Use Case → Entity → Security → Code → Test**

This provides the "evidence artifact" that proves requirements are fully implemented and tested.

## When to Use / 使用タイミング

- **After Step 9 (Test Generation)**: Full forward+backward traceability across all artifacts
- **After Step 6 (Model Validation)**: Pre-code traceability verification (scenario→model only)
- **On demand**: To audit coverage gaps or generate compliance documentation

## Language Support / 言語サポート

Inherits language settings from domain-model.json or usecase-output.json.
Supports Japanese, English, and Bilingual output.

---

## Input Artifacts / 入力成果物

The skill reads the following files from the project output directory.
Not all files are required — the matrix adapts to what is available.

### Required (minimum for useful matrix)

| File | Source Skill | Key Data |
|------|-------------|----------|
| `{project}_usecase-output.json` | activity-to-usecase-v1 | UC IDs, actor refs, domain model refs |
| `usecase-specifications/UC-*.md` | activity-to-usecase-v1 | Traceability sections, related entities |

### Recommended

| File | Source Skill | Key Data |
|------|-------------|----------|
| `{project}_activity.puml` | scenario-to-activity-v1 | Scenario step → activity action mapping |
| `{project}_activity-data.json` | scenario-to-activity-v1 | Structured scenario/activity data |
| `{project}_domain-model.json` | usecase-to-class-v1 | Entity definitions, relationships |
| `{project}_statemachine.puml` | class-to-statemachine-v1 | Entity lifecycle states |
| `{project}_sequence.puml` | usecase-to-sequence-v1 | Object interactions per UC |
| `{project}_validation-report.json` | model-validator-v1 | Existing coverage metrics |
| `{project}_security-config.json` | security-design-v1 | Role-permission, endpoint security |

### Optional (for full code/test traceability)

| File/Directory | Source Skill | Key Data |
|----------------|-------------|----------|
| `src/` directory | usecase-to-code-v1 | Generated source code files |
| `tests/` directory | usecase-to-test-v1 | Generated test files |

---

## Output Artifacts / 出力成果物

### 1. Traceability Matrix JSON (Primary)

**Filename:** `{project}_traceability-matrix.json`

```json
{
  "metadata": {
    "project": "ec-order-management",
    "generated_at": "2026-02-26T...",
    "tool": "traceability-matrix-v1",
    "version": "1.0",
    "language": "ja",
    "pipeline_steps_detected": [
      "scenario-to-activity-v1",
      "activity-to-usecase-v1",
      "usecase-to-class-v1",
      "class-to-statemachine-v1",
      "usecase-to-sequence-v1",
      "model-validator-v1",
      "security-design-v1",
      "usecase-to-code-v1",
      "usecase-to-test-v1"
    ],
    "artifacts_found": {
      "activity_data": true,
      "usecase_output": true,
      "usecase_specs": true,
      "domain_model": true,
      "statemachine": true,
      "sequence": true,
      "validation_report": true,
      "security_config": true,
      "source_code": true,
      "test_code": true
    }
  },

  "scenario_to_activity": [
    {
      "scenario_id": "S1",
      "scenario_name": "商品注文フロー",
      "activity_actions": ["A1.1", "A1.2", "A1.3", "A1.4", "A1.5"]
    }
  ],

  "activity_to_usecase": [
    {
      "activity_action_id": "A1.1",
      "activity_action_name": "商品カタログを確認する",
      "usecase_ids": ["UC-001"]
    }
  ],

  "usecase_to_entity": [
    {
      "usecase_id": "UC-001",
      "usecase_name": "商品を注文する",
      "primary_actor": "顧客",
      "entities": ["Order", "OrderItem", "Product", "Inventory", "Customer"],
      "story_points": 5
    }
  ],

  "entity_to_statemachine": [
    {
      "entity_name": "Order",
      "has_statemachine": true,
      "states": ["Created", "Confirmed", "Shipped", "Delivered", "Cancelled"],
      "transitions": 8
    }
  ],

  "usecase_to_sequence": [
    {
      "usecase_id": "UC-001",
      "has_sequence_diagram": true,
      "participants": ["Customer", "OrderController", "OrderService", "InventoryService", "OrderRepository"]
    }
  ],

  "usecase_to_security": [
    {
      "usecase_id": "UC-001",
      "required_roles": ["customer", "authenticated"],
      "api_endpoints": [
        {
          "method": "POST",
          "path": "/api/orders",
          "auth_required": true,
          "rate_limited": true
        }
      ],
      "owasp_controls": ["A01:2021", "A02:2021", "A07:2021"]
    }
  ],

  "usecase_to_code": [
    {
      "usecase_id": "UC-001",
      "code_files": {
        "routes": ["src/routes/order.routes.ts"],
        "services": ["src/services/order.service.ts"],
        "models": ["src/models/Order.ts", "src/models/OrderItem.ts"],
        "controllers": ["src/controllers/order.controller.ts"]
      }
    }
  ],

  "usecase_to_test": [
    {
      "usecase_id": "UC-001",
      "test_files": {
        "unit": ["tests/unit/order.service.test.ts"],
        "integration": ["tests/integration/order.api.test.ts"],
        "e2e": ["tests/e2e/order-flow.test.ts"]
      },
      "test_cases": [
        {
          "test_id": "T-UC001-01",
          "description": "正常な注文登録",
          "type": "integration",
          "covers_main_flow": true,
          "covers_step": "主成功シナリオ Step 1-9"
        },
        {
          "test_id": "T-UC001-02",
          "description": "在庫不足時のエラーハンドリング",
          "type": "integration",
          "covers_main_flow": false,
          "covers_step": "拡張 5a"
        }
      ]
    }
  ],

  "full_trace_chains": [
    {
      "chain_id": "TRACE-001",
      "scenario": "S1: 商品注文フロー",
      "scenario_step": "顧客が商品を注文する",
      "activity_action": "A1.1: 商品カタログを確認する",
      "usecase": "UC-001: 商品を注文する",
      "entities": ["Order", "OrderItem", "Product"],
      "security": "認証必須, customer ロール",
      "code_file": "src/services/order.service.ts",
      "test_file": "tests/integration/order.api.test.ts",
      "status": "fully_traced"
    }
  ],

  "coverage_summary": {
    "scenario_to_activity": {
      "total_scenarios": 4,
      "covered": 4,
      "coverage_pct": 100.0
    },
    "activity_to_usecase": {
      "total_actions": 15,
      "covered": 14,
      "coverage_pct": 93.3,
      "gaps": ["A3.5: 売上集計処理（未対応ユースケースなし）"]
    },
    "usecase_to_entity": {
      "total_usecases": 8,
      "covered": 8,
      "coverage_pct": 100.0
    },
    "usecase_to_security": {
      "total_usecases": 8,
      "covered": 8,
      "coverage_pct": 100.0
    },
    "usecase_to_code": {
      "total_usecases": 8,
      "covered": 7,
      "coverage_pct": 87.5,
      "gaps": ["UC-008: 売上レポート生成（コード未生成）"]
    },
    "usecase_to_test": {
      "total_usecases": 8,
      "covered": 7,
      "coverage_pct": 87.5,
      "gaps": ["UC-008: 売上レポート生成（テスト未生成）"]
    },
    "overall_end_to_end": {
      "total_trace_chains": 15,
      "fully_traced": 12,
      "partially_traced": 2,
      "not_traced": 1,
      "coverage_pct": 80.0
    }
  }
}
```

### 2. Traceability Matrix Markdown (Human-Readable)

**Filename:** `{project}_traceability-matrix.md`

Structure:

```markdown
# トレーサビリティマトリクス: {project}

生成日時: {timestamp}
パイプラインステップ検出数: {n}/9

## 1. カバレッジサマリー / Coverage Summary

| 追跡レベル | 総数 | カバー済 | カバレッジ | ステータス |
|-----------|------|---------|----------|----------|
| シナリオ → アクティビティ | 4 | 4 | 100% | ✅ |
| アクティビティ → ユースケース | 15 | 14 | 93.3% | ⚠️ |
| ユースケース → エンティティ | 8 | 8 | 100% | ✅ |
| ユースケース → セキュリティ | 8 | 8 | 100% | ✅ |
| ユースケース → コード | 8 | 7 | 87.5% | ⚠️ |
| ユースケース → テスト | 8 | 7 | 87.5% | ⚠️ |
| **End-to-End 完全追跡** | **15** | **12** | **80.0%** | ⚠️ |

## 2. 完全追跡チェーン / End-to-End Traceability Chain

### UC-001: 商品を注文する

| レイヤー | 成果物 | ステータス |
|---------|-------|----------|
| シナリオ | S1: 商品注文フロー | ✅ |
| アクティビティ | A1.1〜A1.5 | ✅ |
| ユースケース | UC-001 (5 SP) | ✅ |
| エンティティ | Order, OrderItem, Product, Inventory, Customer | ✅ |
| ステートマシン | Order: 5状態, 8遷移 | ✅ |
| シーケンス図 | 5参加者 | ✅ |
| セキュリティ | 認証必須, customer ロール, OWASP A01,A02,A07 | ✅ |
| コード | 4ファイル (routes, service, model, controller) | ✅ |
| テスト | 3ファイル (unit, integration, e2e) | ✅ |

**追跡チェーン**: シナリオ → アクティビティ → ユースケース → エンティティ → セキュリティ → コード → テスト **✅ 完全**

### UC-008: 売上レポート生成

| レイヤー | 成果物 | ステータス |
|---------|-------|----------|
| シナリオ | S4: 管理者レポートフロー | ✅ |
| アクティビティ | A4.1〜A4.3 | ✅ |
| ユースケース | UC-008 (3 SP) | ✅ |
| エンティティ | SalesReport, Order | ✅ |
| コード | — | ❌ 未生成 |
| テスト | — | ❌ 未生成 |

**追跡チェーン**: シナリオ → アクティビティ → ユースケース → エンティティ → **断絶** ⚠️

## 3. カバレッジギャップ一覧 / Coverage Gaps

| ギャップID | レベル | 内容 | 推奨アクション |
|-----------|-------|------|-------------|
| GAP-001 | アクティビティ→UC | A3.5 にユースケースなし | ユースケース追加を検討 |
| GAP-002 | UC→コード | UC-008 のコード未生成 | usecase-to-code-v1 を再実行 |
| GAP-003 | UC→テスト | UC-008 のテスト未生成 | usecase-to-test-v1 を再実行 |

## 4. 逆追跡マトリクス / Reverse Traceability Matrix (Code→Requirements)

| コードファイル | エンティティ | ユースケース | シナリオ |
|--------------|-----------|-----------|---------|
| src/services/order.service.ts | Order | UC-001, UC-004 | S1, S2 |
| src/services/inventory.service.ts | Inventory | UC-001, UC-003 | S1, S3 |
| src/models/Order.ts | Order | UC-001, UC-002, UC-004 | S1, S2 |
```

---

## Execution Procedure / 実行手順

### Step 1: Detect Available Artifacts

```python
import os
import json
import glob

project_dir = "{output_dir}"
project = "{project_name}"

artifacts = {}

# Check each artifact type
checks = {
    "activity_data": f"{project}_activity-data.json",
    "activity_puml": f"{project}_activity.puml",
    "usecase_output": f"{project}_usecase-output.json",
    "domain_model": f"{project}_domain-model.json",
    "statemachine": f"{project}_statemachine.puml",
    "sequence": f"{project}_sequence.puml",
    "validation_report": f"{project}_validation-report.json",
    "security_config": f"{project}_security-config.json",
}

for key, filename in checks.items():
    path = os.path.join(project_dir, filename)
    artifacts[key] = os.path.exists(path)

# Check for use case specification files
uc_specs = glob.glob(os.path.join(project_dir, "usecase-specifications", "UC-*.md"))
artifacts["usecase_specs"] = len(uc_specs) > 0
artifacts["usecase_spec_count"] = len(uc_specs)

# Check for source code
src_dir = os.path.join(project_dir, "src")
artifacts["source_code"] = os.path.exists(src_dir)
if artifacts["source_code"]:
    artifacts["source_files"] = []
    for root, dirs, files in os.walk(src_dir):
        for f in files:
            if f.endswith(('.ts', '.js', '.py', '.java', '.go')):
                artifacts["source_files"].append(os.path.relpath(os.path.join(root, f), project_dir))

# Check for test code
test_dirs = ["tests", "test", "__tests__"]
for td in test_dirs:
    test_dir = os.path.join(project_dir, td)
    if os.path.exists(test_dir):
        artifacts["test_code"] = True
        artifacts["test_files"] = []
        for root, dirs, files in os.walk(test_dir):
            for f in files:
                if f.endswith(('.test.ts', '.test.js', '.spec.ts', '.spec.js', '_test.py', '_test.go', 'Test.java')):
                    artifacts["test_files"].append(os.path.relpath(os.path.join(root, f), project_dir))
        break
else:
    artifacts["test_code"] = False

print(f"Artifacts detected: {json.dumps(artifacts, indent=2)}")
```

### Step 2: Parse Use Case Output JSON

```python
# Load usecase-output.json
with open(f"{project_dir}/{project}_usecase-output.json", "r") as f:
    uc_data = json.load(f)

usecases = uc_data.get("usecases", [])
actors = uc_data.get("actors", [])
domain_entities_inferred = uc_data.get("domain_model", {}).get("entities", [])

# Build UC → entity mapping
uc_entity_map = {}
for uc in usecases:
    uc_id = uc["id"]
    # Collect entity references from UC fields
    entities = set()
    # From domain model cross-references
    for entity in domain_entities_inferred:
        entity_name = entity.get("name", "")
        # Check if entity is referenced in UC description or steps
        if entity_name:
            entities.add(entity_name)
    uc_entity_map[uc_id] = {
        "name": uc.get("name", ""),
        "actor": uc.get("primary_actor", ""),
        "story_points": uc.get("story_points", 0),
        "entities": list(entities)
    }
```

### Step 3: Parse Use Case Markdown Specifications

```python
import re

uc_spec_dir = os.path.join(project_dir, "usecase-specifications")
uc_trace_info = {}

for md_file in sorted(glob.glob(os.path.join(uc_spec_dir, "UC-*.md"))):
    with open(md_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract UC ID
    id_match = re.search(r'\*\*ID\*\*:\s*(UC-\d+)', content)
    if not id_match:
        id_match = re.search(r'#\s*(UC-\d+)', content)
    uc_id = id_match.group(1) if id_match else os.path.basename(md_file).split('_')[0]

    # Extract related entities from traceability section
    entities = []
    trace_match = re.search(r'関連エンティティ[^:]*[:：]\s*(.+)', content)
    if trace_match:
        entities = [e.strip() for e in trace_match.group(1).split(',')]

    # Extract source activity reference
    activity_ref = None
    act_match = re.search(r'派生元アクティビティ図[^:]*[:：]\s*(.+)', content)
    if act_match:
        activity_ref = act_match.group(1).strip()

    # Extract related use cases
    related_ucs = re.findall(r'(UC-\d+)', content.split('関連ユースケース')[-1] if '関連ユースケース' in content else '')

    # Extract main success scenario step count
    main_steps = re.findall(r'^\d+\.\s', content, re.MULTILINE)

    # Extract extensions
    extensions = re.findall(r'\*\*(\d+[a-z])\.\s', content)

    uc_trace_info[uc_id] = {
        "entities": entities,
        "activity_ref": activity_ref,
        "related_ucs": related_ucs,
        "main_flow_steps": len(main_steps),
        "extensions": extensions,
        "file": os.path.basename(md_file)
    }
```

### Step 4: Parse Domain Model JSON

```python
entity_details = {}

if artifacts.get("domain_model"):
    with open(f"{project_dir}/{project}_domain-model.json", "r") as f:
        dm = json.load(f)

    for entity in dm.get("entities", []):
        name = entity.get("name", "")
        entity_details[name] = {
            "japanese_name": entity.get("japanese_name", name),
            "attributes": [a.get("name") for a in entity.get("attributes", [])],
            "methods": [m.get("name") for m in entity.get("methods", [])],
            "relationships": [
                {
                    "target": r.get("target", ""),
                    "type": r.get("type", ""),
                    "name": r.get("name", "")
                }
                for r in entity.get("relationships", [])
            ]
        }
```

### Step 5: Parse State Machine Diagrams

```python
entity_statemachines = {}

if artifacts.get("statemachine"):
    with open(f"{project_dir}/{project}_statemachine.puml", "r", encoding="utf-8") as f:
        sm_content = f.read()

    # Parse each state machine block
    sm_blocks = re.findall(r'@startuml\s+(\w+)_statemachine(.*?)@enduml', sm_content, re.DOTALL)
    for entity_name, block in sm_blocks:
        states = set(re.findall(r'state\s+"([^"]+)"', block))
        transitions = re.findall(r'(\w+)\s*-->\s*(\w+)', block)
        entity_statemachines[entity_name] = {
            "states": list(states),
            "state_count": len(states),
            "transitions": len(transitions)
        }
```

### Step 6: Parse Sequence Diagrams

```python
uc_sequences = {}

if artifacts.get("sequence"):
    with open(f"{project_dir}/{project}_sequence.puml", "r", encoding="utf-8") as f:
        seq_content = f.read()

    # Parse sequence diagram titles linked to UCs
    seq_blocks = re.findall(r'@startuml\s+(\S+)(.*?)@enduml', seq_content, re.DOTALL)
    for diagram_id, block in seq_blocks:
        # Extract UC reference from title
        uc_match = re.search(r'title.*?(UC-\d+)', block)
        if uc_match:
            uc_id = uc_match.group(1)
        else:
            uc_id = diagram_id

        participants = re.findall(r'participant\s+"?([^"\n]+)"?\s+as', block)
        if not participants:
            participants = re.findall(r'participant\s+"?([^"\n]+)"?', block)

        uc_sequences[uc_id] = {
            "participants": participants,
            "participant_count": len(participants)
        }
```

### Step 7: Parse Security Configuration

```python
uc_security = {}

if artifacts.get("security_config"):
    with open(f"{project_dir}/{project}_security-config.json", "r") as f:
        sec = json.load(f)

    roles = sec.get("authorization", {}).get("roles", [])
    endpoints = sec.get("api_security", {}).get("endpoints", {})
    owasp = sec.get("owasp_countermeasures", {})

    # Map endpoints to use cases (heuristic: endpoint name → entity → UC)
    for endpoint_path, endpoint_config in endpoints.items() if isinstance(endpoints, dict) else []:
        # Associate with relevant UCs based on entity names in path
        for uc_id, uc_info in uc_entity_map.items():
            for entity in uc_info.get("entities", []):
                if entity.lower() in endpoint_path.lower():
                    if uc_id not in uc_security:
                        uc_security[uc_id] = {
                            "roles": [],
                            "endpoints": [],
                            "owasp_controls": []
                        }
                    uc_security[uc_id]["endpoints"].append({
                        "path": endpoint_path,
                        "methods": endpoint_config.get("methods", []),
                        "auth_required": endpoint_config.get("auth_required", True)
                    })
```

### Step 8: Map Code Files to Use Cases

```python
uc_code_map = {}

if artifacts.get("source_code"):
    source_files = artifacts.get("source_files", [])

    for uc_id, uc_info in uc_entity_map.items():
        code_files = {"routes": [], "services": [], "models": [], "controllers": []}

        for src_file in source_files:
            src_lower = src_file.lower()
            for entity in uc_info.get("entities", []):
                entity_lower = entity.lower()
                # Match entity name in filename
                if entity_lower in src_lower:
                    if "route" in src_lower:
                        code_files["routes"].append(src_file)
                    elif "service" in src_lower:
                        code_files["services"].append(src_file)
                    elif "model" in src_lower or "entity" in src_lower:
                        code_files["models"].append(src_file)
                    elif "controller" in src_lower or "handler" in src_lower:
                        code_files["controllers"].append(src_file)

        # Deduplicate
        for k in code_files:
            code_files[k] = sorted(set(code_files[k]))

        if any(code_files.values()):
            uc_code_map[uc_id] = code_files
```

### Step 9: Map Test Files to Use Cases

```python
uc_test_map = {}

if artifacts.get("test_code"):
    test_files = artifacts.get("test_files", [])

    for uc_id, uc_info in uc_entity_map.items():
        tests = {"unit": [], "integration": [], "e2e": []}

        for test_file in test_files:
            test_lower = test_file.lower()
            for entity in uc_info.get("entities", []):
                entity_lower = entity.lower()
                if entity_lower in test_lower:
                    if "unit" in test_lower:
                        tests["unit"].append(test_file)
                    elif "e2e" in test_lower or "playwright" in test_lower or "cypress" in test_lower:
                        tests["e2e"].append(test_file)
                    elif "integration" in test_lower or "api" in test_lower:
                        tests["integration"].append(test_file)
                    else:
                        tests["unit"].append(test_file)

        for k in tests:
            tests[k] = sorted(set(tests[k]))

        if any(tests.values()):
            uc_test_map[uc_id] = tests
```

### Step 10: Build Full Trace Chains

```python
full_chains = []
chain_id = 0

for uc_id, uc_info in uc_entity_map.items():
    chain_id += 1
    trace_info = uc_trace_info.get(uc_id, {})

    chain = {
        "chain_id": f"TRACE-{chain_id:03d}",
        "usecase_id": uc_id,
        "usecase_name": uc_info.get("name", ""),
        "primary_actor": uc_info.get("actor", ""),
        "story_points": uc_info.get("story_points", 0),
        "layers": {}
    }

    # Scenario layer
    chain["layers"]["scenario"] = {
        "status": "traced" if trace_info.get("activity_ref") else "unknown",
        "ref": trace_info.get("activity_ref", "N/A")
    }

    # Entity layer
    entities = trace_info.get("entities", []) or uc_info.get("entities", [])
    chain["layers"]["entities"] = {
        "status": "traced" if entities else "gap",
        "items": entities
    }

    # State machine layer
    has_sm = any(e in entity_statemachines for e in entities)
    chain["layers"]["statemachine"] = {
        "status": "traced" if has_sm else "not_applicable",
        "entities_with_sm": [e for e in entities if e in entity_statemachines]
    }

    # Sequence diagram layer
    chain["layers"]["sequence"] = {
        "status": "traced" if uc_id in uc_sequences else "gap",
        "participants": uc_sequences.get(uc_id, {}).get("participants", [])
    }

    # Security layer
    chain["layers"]["security"] = {
        "status": "traced" if uc_id in uc_security else "gap",
        "details": uc_security.get(uc_id, {})
    }

    # Code layer
    chain["layers"]["code"] = {
        "status": "traced" if uc_id in uc_code_map else "gap",
        "files": uc_code_map.get(uc_id, {})
    }

    # Test layer
    chain["layers"]["test"] = {
        "status": "traced" if uc_id in uc_test_map else "gap",
        "files": uc_test_map.get(uc_id, {})
    }

    # Determine overall status
    statuses = [v.get("status") for k, v in chain["layers"].items()
                if v.get("status") != "not_applicable"]
    if all(s == "traced" for s in statuses):
        chain["overall_status"] = "fully_traced"
    elif any(s == "gap" for s in statuses):
        chain["overall_status"] = "partially_traced"
    else:
        chain["overall_status"] = "unknown"

    full_chains.append(chain)
```

### Step 11: Calculate Coverage Summary

```python
def calc_coverage(items, check_fn):
    total = len(items)
    covered = sum(1 for item in items if check_fn(item))
    gaps = [item for item in items if not check_fn(item)]
    return {
        "total": total,
        "covered": covered,
        "coverage_pct": round(covered / total * 100, 1) if total > 0 else 0.0,
        "gaps": gaps
    }

coverage = {
    "usecase_to_entity": calc_coverage(
        list(uc_entity_map.keys()),
        lambda uc_id: bool(uc_trace_info.get(uc_id, {}).get("entities"))
    ),
    "usecase_to_code": calc_coverage(
        list(uc_entity_map.keys()),
        lambda uc_id: uc_id in uc_code_map
    ),
    "usecase_to_test": calc_coverage(
        list(uc_entity_map.keys()),
        lambda uc_id: uc_id in uc_test_map
    ),
    "overall_end_to_end": {
        "total": len(full_chains),
        "fully_traced": sum(1 for c in full_chains if c["overall_status"] == "fully_traced"),
        "partially_traced": sum(1 for c in full_chains if c["overall_status"] == "partially_traced"),
        "not_traced": sum(1 for c in full_chains if c["overall_status"] == "unknown"),
    }
}
coverage["overall_end_to_end"]["coverage_pct"] = round(
    coverage["overall_end_to_end"]["fully_traced"] / len(full_chains) * 100, 1
) if full_chains else 0.0
```

### Step 12: Generate JSON Output

```python
matrix_json = {
    "metadata": {
        "project": project,
        "generated_at": datetime.now().isoformat(),
        "tool": "traceability-matrix-v1",
        "version": "1.0",
        "artifacts_found": artifacts
    },
    "usecase_to_entity": [
        {
            "usecase_id": uc_id,
            "usecase_name": info.get("name", ""),
            "entities": info.get("entities", [])
        }
        for uc_id, info in uc_entity_map.items()
    ],
    "entity_to_statemachine": [
        {
            "entity_name": name,
            "has_statemachine": True,
            **details
        }
        for name, details in entity_statemachines.items()
    ],
    "usecase_to_sequence": [
        {"usecase_id": uc_id, **details}
        for uc_id, details in uc_sequences.items()
    ],
    "usecase_to_security": [
        {"usecase_id": uc_id, **details}
        for uc_id, details in uc_security.items()
    ],
    "usecase_to_code": [
        {"usecase_id": uc_id, "code_files": files}
        for uc_id, files in uc_code_map.items()
    ],
    "usecase_to_test": [
        {"usecase_id": uc_id, "test_files": files}
        for uc_id, files in uc_test_map.items()
    ],
    "full_trace_chains": full_chains,
    "coverage_summary": coverage
}

output_path = f"{project_dir}/{project}_traceability-matrix.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(matrix_json, f, indent=2, ensure_ascii=False)

print(f"Traceability matrix JSON saved: {output_path}")
```

### Step 13: Generate Markdown Report

Generate the human-readable Markdown report following the format shown in Section "2. Traceability Matrix Markdown".

**Key sections to include:**
1. Coverage summary table with ✅/⚠️/❌ status indicators
2. Per-UC trace chain tables (one table per UC showing all layers)
3. Gap analysis table with recommended actions
4. Reverse traceability matrix (code file → entity → UC → scenario)

**Status indicators:**
- ✅ = 100% coverage
- ⚠️ = 80-99% coverage
- ❌ = <80% coverage

**Gap recommendations:**
- Missing UC for activity action → "ユースケース追加を検討"
- Missing code for UC → "usecase-to-code-v1 を再実行"
- Missing test for UC → "usecase-to-test-v1 を再実行"
- Missing security for UC → "security-design-v1 を再実行"

```python
md_output_path = f"{project_dir}/{project}_traceability-matrix.md"
with open(md_output_path, "w", encoding="utf-8") as f:
    f.write(md_content)

print(f"Traceability matrix Markdown saved: {md_output_path}")
```

---

## Integration with UML Workflow v3 / UMLワークフローとの連携

### As Step 10 (New)

This skill is designed to be the **final step** in the UML Workflow pipeline:

```
Step 1: scenario-to-activity-v1
Step 2: activity-to-usecase-v1
Step 3: usecase-to-class-v1
Step 4: class-to-statemachine-v1
Step 5: usecase-to-sequence-v1
Step 6: model-validator-v1
Step 7: security-design-v1
Step 8: usecase-to-code-v1
Step 9: usecase-to-test-v1
Step 10: traceability-matrix-v1  ← NEW
```

### Pre-Code Verification (After Step 6)

Can also run after model validation to verify model-level traceability before committing to code generation. In this mode, code and test layers are skipped.

### Cache Integration

The traceability matrix should be regenerated whenever any upstream artifact changes. It does not participate in the caching system since it reads from all other cached outputs.

---

## Quality Criteria / 品質基準

### Minimum Acceptable Coverage

| Level | Threshold | Action if Below |
|-------|-----------|-----------------|
| UC → Entity | 100% | Block code generation |
| UC → Security | 100% | Block code generation |
| UC → Code | 90% | Warning, allow proceed |
| UC → Test | 80% | Warning, allow proceed |
| End-to-End | 80% | Warning in report |

### Validation Rules

1. Every UC must reference at least one entity
2. Every entity in domain model must be referenced by at least one UC
3. Every UC with side effects must have security requirements
4. Every generated code file must trace back to at least one UC
5. Every test file must trace back to at least one UC

---

## Output File Summary / 出力ファイルまとめ

| File | Size | Description |
|------|------|-------------|
| `{project}_traceability-matrix.json` | 10-30 KB | Machine-readable full matrix |
| `{project}_traceability-matrix.md` | 5-15 KB | Human-readable report with gap analysis |

---

## Limitations and Future Enhancements / 制限事項と今後の拡張

### Current Limitations

1. **Code mapping is heuristic-based**: Uses filename/entity name matching, not AST analysis
2. **Test case granularity**: Maps at file level, not individual test case level
3. **Activity→UC mapping**: Relies on UC spec traceability sections, not formal IDs
4. **No formal requirement IDs**: Scenarios don't have structured requirement IDs yet

### Planned Enhancements (v2)

1. **Formal Requirement IDs**: Introduce REQ-{nnn} in scenario input, propagate through pipeline
2. **AST-based code analysis**: Parse generated code to find entity/UC references in comments
3. **Test case extraction**: Parse test files to extract individual test case descriptions
4. **Interactive HTML report**: Generate browsable HTML with clickable cross-references
5. **Diff mode**: Compare two matrices to show what changed between iterations
