# UML Workflow v3 — Installation Guide

## Prerequisites

- Claude.ai **Pro** / **Max** / **Team** / **Enterprise** plan
- "Code execution and file creation" must be **enabled**

## Installation Steps

### Step 1: Download ZIP Files

Download the following 5 ZIP files from the GitHub [Releases](../../releases) page.

| # | File Name | Size | Role |
|---|-----------|------|------|
| 1 | `uml-workflow-v3.zip` | 154KB | Main orchestrator (10 pipeline skills built-in) |
| 2 | `usecase-md-to-json.zip` | 11KB | Use case Markdown → JSON converter |
| 3 | `classdiagram-image-to-json.zip` | 15KB | Class diagram image → JSON import |
| 4 | `json-to-models.zip` | 12KB | JSON → PlantUML/XMI regeneration |
| 5 | `classdiagram-to-crud.zip` | 6KB | Class diagram → CRUD HTML generation |

> **Note**: Installing all 5 is recommended, but the workflow runs with just `uml-workflow-v3.zip`. The other 4 are helper tools for manual model editing.

### Step 2: Open Claude.ai Settings

1. Log in to [claude.ai](https://claude.ai)
2. Click **Settings** (bottom-left)
3. Open the **"Capabilities"** tab
4. Confirm **"Code execution and file creation"** is **ON**

### Step 3: Upload Skills

1. Scroll to the **Skills** section in the Capabilities page
2. Click **"Upload skill"**
3. Select the downloaded **`uml-workflow-v3-github-repo.zip`** and upload
4. After upload, `uml-workflow-v3` appears in the skill list
5. Toggle the switch to **ON**

6. Repeat the same process for the remaining 4 ZIPs:
   - `usecase-md-to-json.zip`
   - `classdiagram-image-to-json.zip`
   - `json-to-models.zip`
   - `classdiagram-to-crud.zip`

> **Important**: Don't forget to toggle each skill **ON** after uploading. Claude won't recognize the skill if it's toggled off.

### Step 4: Verify Installation

Open a **new conversation** and type:

```
Use uml-workflow-v3 to generate an application from the following business scenario.

Scenario:
Employees submit expense reports. Managers approve or reject them.
The accounting department processes approved expense reports for reimbursement.
```

If Claude recognizes the skill and starts the 10-step workflow, the installation was successful.

## Basic Usage

### Full Workflow

```
Use uml-workflow-v3 to generate an application from the following scenario.
[Your business scenario here]
```

### Execute Specific Step

```
Run Step 6 (model validation) of uml-workflow
```

### Resume from Step

```
Resume uml-workflow from Step 5
```

### Model Editing (Helper Skills)

```
I've edited the use case Markdown specs. Please update the JSON.
```

```
Import this hand-drawn class diagram [attach image]
```

## 10-Step Pipeline

| Step | Function | Output |
|------|----------|--------|
| 1 | Scenario → Activity Diagram | activity-data.json, .puml |
| 2 | Activity → Use Cases | usecase-output.json, .puml |
| 3 | Use Cases → Class Diagram | domain-model.json, .puml |
| 4 | State Machine Generation | statemachine.puml |
| 5 | Sequence Diagram Generation | sequence.puml |
| 6 | Cross-Model Validation | validation-report.md |
| 7 | Security Design | security-config.json |
| 8 | Code Generation | src/ directory |
| 9 | Test Generation | tests/ directory |
| 10 | Traceability Matrix | traceability-matrix.json/.md |

## Updating

To update a skill, upload the new ZIP file using the same process. Skills with the same name are automatically overwritten.

## Troubleshooting

### Skill Not Recognized
- Verify the skill toggle is **ON** in Settings > Capabilities
- Confirm "Code execution and file creation" is enabled
- Open a **new conversation** (skills aren't recognized in conversations that existed before upload)

### Upload Error
- Ensure the ZIP contains a folder with `SKILL.md` inside (correct: `skill-name/SKILL.md`, incorrect: `SKILL.md` at root)
- Ensure the `description` field is under 200 characters

### Cannot Resume from Middle Step
- Files from previous sessions are not carried over
- Re-upload the intermediate files or restart from Step 1

## Recommended Plans

| Plan | Workflow Support | Notes |
|------|-----------------|-------|
| Free | Not supported | Code execution not available |
| Pro | Limited | Message limits apply. Best for small scenarios |
| Max | Recommended | Can complete all 10 steps even for large scenarios |
| Team / Enterprise | Recommended | Best for organizational use |

---

*For the comprehensive user guide, see [USER_GUIDE.md](USER_GUIDE.md).*  
*日本語インストールガイドは [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md) を参照してください。*
