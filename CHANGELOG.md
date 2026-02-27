# Changelog

All notable changes to this project will be documented in this file.

## [3.1.0] - 2026-02-27

### Added
- **2-Phase Auto-Split Architecture**: Full workflow automatically splits into Phase A (Steps 1-7) and Phase B (Steps 8-10) across separate conversations to prevent context window exhaustion
- **Template Lazy Loading**: `usecase-to-code-v1` templates (language examples, documentation templates) extracted to separate files and loaded on demand
- **AUTO-SPLIT CHECKPOINT**: Explicit checkpoint after Step 7 with Phase B instructions for user

### Changed
- **SKILL.md**: Reduced from 1,552 to 911 lines (38% reduction, ~4K tokens saved)
- **usecase-to-code-v1 PIPELINE.md**: Reduced from 2,826 to 1,678 lines (30% reduction, ~6K tokens saved)
- **Standalone usecase-to-code-v1**: Same template split applied for consistency
- Execution plan display now shows Phase A/B split

### Removed
- Duplicate Python pseudocode section in SKILL.md (was redundant with PHASE 4)
- Verbose Usage Examples, Best Practices, Cache Management sections (compressed to tables)
- `uml-workflow-v2-enhanced` — consolidated into v3

### Fixed
- **Context window exhaustion at Step 8**: Root cause was ~120K tokens consumed before Step 8 PIPELINE load. Now Phase A uses ~91K and Phase B uses ~60K, both safely within 200K limit

## [3.0.0] - 2026-02-19

### Added
- Renamed from `uml-workflow-v2-enhanced` to `uml-workflow-v3`
- Security-first 10-step pipeline (was 9 steps in v2)
- `security-design-v1` integrated as Step 7
- `traceability-matrix-v1` added as Step 10
- Bilingual support (Japanese/English) across all skills
- Cache system for intermediate artifacts
- XMI generation toggle (OFF by default for 40% speedup)

### Skills Included
1. scenario-to-activity-v1
2. activity-to-usecase-v1
3. usecase-to-class-v1
4. class-to-statemachine-v1
5. usecase-to-sequence-v1
6. model-validator-v1
7. security-design-v1
8. usecase-to-code-v1
9. usecase-to-test-v1
10. json-to-models (optional)
11. usecase-md-to-json (optional)
12. classdiagram-image-to-json (optional)
