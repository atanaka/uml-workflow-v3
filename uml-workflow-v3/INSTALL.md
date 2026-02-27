# uml-workflow-v3 Installation / インストール

## About This Folder / このフォルダについて

This is the **orchestrator skill** that coordinates the entire 10-step pipeline.  
See the root [INSTALL.md](../INSTALL.md) for full package installation instructions.

## Required Sub-skills / 必要なサブスキル

This orchestrator requires the following skills to be installed alongside it:

### Core (9 skills — required)

| Skill | Folder |
|-------|--------|
| scenario-to-activity-v1 | `../skills/scenario-to-activity-v1/` |
| activity-to-usecase-v1 | `../skills/activity-to-usecase-v1/` |
| usecase-to-class-v1 | `../skills/usecase-to-class-v1/` |
| class-to-statemachine-v1 | `../skills/class-to-statemachine-v1/` |
| usecase-to-sequence-v1 | `../skills/usecase-to-sequence-v1/` |
| model-validator-v1 | `../skills/model-validator-v1/` |
| security-design-v1 | `../skills/security-design-v1/` |
| usecase-to-code-v1 | `../skills/usecase-to-code-v1/` |
| usecase-to-test-v1 | `../skills/usecase-to-test-v1/` |

### Optional (3 skills)

| Skill | Folder |
|-------|--------|
| json-to-models | `../skills/json-to-models/` |
| usecase-md-to-json | `../skills/usecase-md-to-json/` |
| classdiagram-image-to-json | `../skills/classdiagram-image-to-json/` |

## Internal Structure / 内部構造

    uml-workflow-v3/
    ├── SKILL.md              ← Main execution specification for Claude
    ├── references/            ← Bundled PIPELINE definitions (read by Claude)
    │   ├── usecase-to-code-v1/
    │   │   ├── PIPELINE.md
    │   │   └── templates/    ← Lazy-loaded (language-examples, doc-templates)
    │   └── ...
    └── scripts/               ← Python utilities (cache, execution mode, etc.)

> **Note**: The `references/` folder contains PIPELINE.md files that the orchestrator reads during execution. These are separate from the standalone skills in `../skills/`.
