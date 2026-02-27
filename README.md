# UML Workflow v3 — AI-Assisted Model-Based Software Development

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Claude Skills](https://img.shields.io/badge/Claude-Skills-blueviolet)](https://claude.ai)
[![Skills Count](https://img.shields.io/badge/Skills-13-green)]()

> **Generative AI × MBSE**: Business scenario → Production-ready full-stack application, fully automated.
>
> **生成AI × MBSE**: ビジネスシナリオ → 本番品質のフルスタックアプリケーションを完全自動生成。

---

## 🎯 What is this? / これは何？

**UML Workflow v3** is a comprehensive Claude skill suite that automates the entire software development lifecycle using UML-based modeling. Starting from a plain-text business scenario, it generates:

- 📊 UML diagrams (Activity, Use Case, Class, State Machine, Sequence)
- ✅ Model validation reports
- 🔒 Security design (OWASP Top 10 compliant)
- 💻 Full-stack application code (Backend + Frontend)
- 🧪 Comprehensive test suites (Unit / Integration / E2E)
- 📋 Traceability matrix

All from a **single natural language input**.

**UML Workflow v3** は、UMLベースのモデリングでソフトウェア開発ライフサイクル全体を自動化するClaudeスキルスイートです。自然言語のビジネスシナリオから、UML図、セキュリティ設計、フルスタックコード、テストコードまでを一括生成します。

---

## 🏗️ Architecture / アーキテクチャ

### 2-Phase Execution / 2フェーズ実行

v3 uses an automatic 2-phase split to prevent context window exhaustion:

v3はコンテキストウィンドウ枯渇を防ぐため、自動2フェーズ分割を採用しています：

```
┌─────────────────────────────────────────────────────┐
│  PHASE A: Modeling & Validation (Steps 1-7)         │
│                                                     │
│  Business Scenario                                  │
│    → Step 1: Activity Diagram                       │
│    → Step 2: Use Cases                              │
│    → Step 3: Class Diagram (Domain Model — SSoT)    │
│    → Step 4: State Machine Diagrams                 │
│    → Step 5: Sequence Diagrams                      │
│    → Step 6: Model Validation                       │
│    → Step 7: Security Design                        │
│                                                     │
│  ✅ All artifacts cached → Start new conversation   │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│  PHASE B: Code Generation (Steps 8-10)              │
│                                                     │
│  Cached Artifacts                                   │
│    → Step 8: Full-Stack Code Generation             │
│    → Step 9: Test Code Generation                   │
│    → Step 10: Traceability Matrix                   │
│                                                     │
│  ✅ Complete application ready                      │
└─────────────────────────────────────────────────────┘
```

### 10-Step Pipeline / 10ステップパイプライン

| Step | Skill | Output |
|------|-------|--------|
| 1 | scenario-to-activity-v1 | Activity diagram + business analysis |
| 2 | activity-to-usecase-v1 | Use case specifications (Cockburn format) |
| 3 | usecase-to-class-v1 | Class diagram + domain-model.json (SSoT) |
| 4 | class-to-statemachine-v1 | State machine diagrams |
| 5 | usecase-to-sequence-v1 | Sequence diagrams |
| 6 | model-validator-v1 | Cross-model validation report |
| 7 | security-design-v1 | Security design + OWASP compliance |
| 8 | usecase-to-code-v1 | Full-stack application |
| 9 | usecase-to-test-v1 | Unit / Integration / E2E tests |
| 10 | traceability-matrix | Requirements traceability |

---

## 📦 Package Contents / パッケージ構成 (13 Skills)

### Orchestrator (1)

| Folder | Role |
|--------|------|
| `uml-workflow-v3/` | Main orchestrator — coordinates all 10 steps |

### Core Pipeline Skills (9)

| Folder | Role |
|--------|------|
| `skills/scenario-to-activity-v1/` | Business scenario → Activity diagram |
| `skills/activity-to-usecase-v1/` | Activity diagram → Use cases |
| `skills/usecase-to-class-v1/` | Use cases → Class diagram / Domain model |
| `skills/class-to-statemachine-v1/` | Class diagram → State machine diagrams |
| `skills/usecase-to-sequence-v1/` | Use cases → Sequence diagrams |
| `skills/model-validator-v1/` | Cross-model validation |
| `skills/security-design-v1/` | Security design (OWASP Top 10) |
| `skills/usecase-to-code-v1/` | Full-stack code generation |
| `skills/usecase-to-test-v1/` | Test code generation |

### Optional Utility Skills (3)

| Folder | Role |
|--------|------|
| `skills/json-to-models/` | JSON → PlantUML / XMI / Markdown regeneration |
| `skills/usecase-md-to-json/` | Markdown use cases → JSON + diagram update |
| `skills/classdiagram-image-to-json/` | Hand-drawn / tool diagrams → domain-model.json |

---

## 🚀 Quick Start / クイックスタート

### Installation / インストール

See [INSTALL.md](INSTALL.md) for detailed instructions.

1. Download this repository
2. Upload all skill folders to Claude.ai (Settings → Skills)
3. Start using!

### Usage / 使い方

```
You:   「uml-workflow-v3で受注管理システムを生成して」
Claude: Configuration questions → Automatic 10-step execution
```

### Execution Modes / 実行モード

| Mode | Steps | Use Case |
|------|-------|----------|
| Full Workflow | 1-7 → 8-10 | Complete generation (2-phase) |
| Models Only | 1-7 | Design review, no code |
| Resume from Step N | N-10 | Iterative development |
| Validation Only | 6 | Quick model check |

---

## 🛠️ Technology Stack Support / 技術スタック

### Backend
- TypeScript + Express (recommended, lightweight)
- TypeScript + NestJS (enterprise-scale)
- Python + FastAPI
- Java + Spring Boot

### Frontend
- React + TypeScript + Vite + Tailwind CSS (recommended)
- Vue 3 + TypeScript + Vite
- None (API-only)

### Architecture
- Monolith (recommended, simple)
- Microservices
- Serverless

---

## 🌐 Language Support / 言語サポート

All skills support bilingual output:
- 🇯🇵 Japanese (日本語)
- 🇬🇧 English
- 🌏 Bilingual (both)

Language is auto-detected from input or configurable per step.

---

## 📊 Performance / パフォーマンス

### Token Optimization

| Feature | Token Reduction |
|---------|----------------|
| 2-Phase Split | Prevents context overflow |
| Cache System | ~30% on subsequent runs |
| XMI OFF (default) | ~18% per run |
| Models-only Mode | ~53% vs full |
| Template Lazy Loading | ~30% on code generation |

### Estimated Token Consumption

| Phase | Tokens | Context Safety |
|-------|--------|---------------|
| Phase A (Steps 1-7) | ~91K | ✅ Safe |
| Phase B (Steps 8-10) | ~60K | ✅ Safe |

---

## 📁 Repository Structure / リポジトリ構造

```
uml-workflow-v3-release/
├── README.md                              ← This file
├── INSTALL.md                             ← Installation guide
├── CHANGELOG.md                           ← Version history
├── CONTRIBUTING.md                        ← Contribution guide
├── LICENSE                                ← MIT License
├── .gitignore
├── uml-workflow-v3/                       ← Orchestrator
│   ├── SKILL.md                           ← Main execution spec
│   ├── INSTALL.md
│   ├── README.md
│   ├── references/                        ← Bundled PIPELINE definitions
│   │   ├── scenario-to-activity-v1/
│   │   ├── activity-to-usecase-v1/
│   │   ├── usecase-to-class-v1/
│   │   ├── class-to-statemachine-v1/
│   │   ├── usecase-to-sequence-v1/
│   │   ├── model-validator-v1/
│   │   ├── security-design-v1/
│   │   ├── usecase-to-code-v1/
│   │   │   ├── PIPELINE.md
│   │   │   └── templates/               ← Lazy-loaded templates
│   │   ├── usecase-to-test-v1/
│   │   └── traceability-matrix-v1/
│   └── scripts/                           ← Python utilities
│       ├── run_workflow.py
│       ├── workflow_cache_helper.py
│       ├── execution_mode_manager.py
│       ├── unified_workflow_executor.py
│       └── interactive_workflow_executor.py
└── skills/                                ← Standalone skills (12)
    ├── scenario-to-activity-v1/
    ├── activity-to-usecase-v1/
    ├── usecase-to-class-v1/
    ├── class-to-statemachine-v1/
    ├── usecase-to-sequence-v1/
    ├── model-validator-v1/
    ├── security-design-v1/
    ├── usecase-to-code-v1/
    │   ├── SKILL.md
    │   └── templates/                     ← Lazy-loaded templates
    ├── usecase-to-test-v1/
    ├── json-to-models/
    ├── usecase-md-to-json/
    └── classdiagram-image-to-json/
```

---

## 🔗 Related / 関連

- [UML Workflow v2 (monorepo)](https://github.com/yourusername/uml-workflow-v2) — Previous version (8-step, still maintained on GitHub)

---

## 📄 License

MIT License — See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

Built with [Claude](https://claude.ai) by [Anthropic](https://anthropic.com).

Methodology based on:
- **RM-ODP** (Reference Model of Open Distributed Processing)
- **UML 2.5** (Unified Modeling Language)
- **MBSE** (Model-Based Systems Engineering)
- **OWASP Top 10** (Security Design)
