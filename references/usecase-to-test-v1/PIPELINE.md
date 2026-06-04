---
name: usecase-to-test-v1
description: Generate comprehensive test code from use case specifications and domain models with multi-language test descriptions (Japanese/English). Creates unit tests, integration tests, and E2E tests with business rule validation. Supports Jest, Vitest, Playwright, and Cypress frameworks. Inherits language settings for test case descriptions. Use after code generation to ensure complete test coverage.
---


# Use Case to Test Code Generator v1

> 🌐 **パスのプレースホルダについて**: 本文の `{SKILL_DIR}` / `{OUTPUT_DIR}` / `{WORK_DIR}` は環境依存。
> uml-workflow-v3 経由なら PHASE 0.0 で解決済みの値を使う。単独起動時は Web=`/mnt/skills/user/uml-workflow-v3`・`/mnt/user-data/outputs`・`/home/claude`、ローカル(Claude Code)=`~/.claude/skills/uml-workflow-v3`・作業ディレクトリ(CWD) に読み替えること。


Generate comprehensive, production-ready test suites from use case specifications and domain models.

## Overview / 概要

This skill automatically generates test code that validates:
- Business logic correctness
- State transitions
- Business rule compliance
- API contract adherence
- End-to-end user flows

**Key capabilities:**
- ✅ Generates unit tests for domain entities
- ✅ Generates integration tests for services
- ✅ Generates E2E tests for user flows
- ✅ Validates business rules (BR-001, BR-002, etc.)
- ✅ Tests state machine transitions
- ✅ Generates test data fixtures
- ✅ Supports multiple test frameworks (Jest, Vitest, Playwright, Cypress)
- ✅ **Multi-language test descriptions (Japanese/English)** ⭐ NEW!

---

## Language Support / 言語サポート ⭐

Generates test code with language-appropriate descriptions. Code identifiers remain in English, but test descriptions (describe/it blocks) follow the configured language.

**Example:**
- Japanese: `describe('商品を注文する', () => { it('在庫ありの場合、注文が完了する', ...) })`
- English: `describe('Place Order', () => { it('should complete order when stock is available', ...) })`

**Configuration inherited from:** domain-model.json metadata.language

---

## Position in Workflow / ワークフロー内の位置

```
Step 1: scenario-to-activity-v1
  ↓
Step 2: activity-to-usecase-v1
  ↓
Step 3: usecase-to-class-v1
  ↓
Step 4: usecase-to-code-v1
  ↓ Source code generated
Step 5: usecase-to-test-v1 ← YOU ARE HERE
  ↓ Test suites
Step 6: security-design-v1
```

---

## Input / 入力

### Required

1. **Use case specifications:** `{project}_usecase-output.json`
2. **Domain model:** `{project}_domain-model.json`
3. **Generated source code:** Backend/Frontend code structure

### Optional

4. **Test configuration:**
   - `test_framework`: 'jest' | 'vitest' (default: 'jest')
   - `e2e_framework`: 'playwright' | 'cypress' (default: 'playwright')
   - `coverage_threshold`: number (default: 80)

---

## Test Generation Strategy / テスト生成戦略

### 1. Unit Tests (Domain Layer)

Generate tests for each domain entity covering:
- Constructor validation
- Business methods
- State transitions
- Business rule enforcement

### 2. Integration Tests (Service Layer)

Generate tests for each use case covering:
- Main success scenario
- Extension scenarios
- Service interactions

### 3. E2E Tests (UI Layer)

Generate tests for critical user flows:
- Complete use case flows
- Error handling scenarios
- User interactions

---

## Output / 出力

### Generated Files

1. **Unit Tests**
   - `tests/unit/domain/entities/{Entity}.test.ts`
   - `tests/unit/domain/services/{Service}.test.ts`

2. **Integration Tests**
   - `tests/integration/services/{Service}.test.ts`
   - `tests/api/{endpoint}.api.test.ts`

3. **E2E Tests**
   - `tests/e2e/{feature}.spec.ts`

4. **Test Fixtures**
   - `tests/fixtures/{entity}.fixture.ts`

5. **Configuration**
   - `jest.config.js` or `vitest.config.ts`
   - `playwright.config.ts` or `cypress.config.ts`

---

## Usage Example / 使用例

```bash
# Generate tests for B2B EC Platform
usecase-to-test-v1 --project b2b-ec-platform

# Generated files:
# ✅ tests/unit/domain/entities/Order.test.ts
# ✅ tests/integration/services/OrderService.test.ts
# ✅ tests/api/orders.api.test.ts
# ✅ tests/e2e/order-flow.spec.ts
# ✅ tests/fixtures/orders.fixture.ts
```

---

## Test Coverage Matrix / テストカバレッジマトリクス

| Layer | Unit | Integration | E2E |
|-------|------|-------------|-----|
| Domain Entities | ✅ All methods | ✅ State transitions | - |
| Services | - | ✅ All use cases | - |
| API | - | ✅ All endpoints | ✅ Critical flows |
| Business Rules | ✅ All rules | ✅ Combinations | - |

Target: 80%+ code coverage

---

## ⚠️ Test Fixture Quality Requirements (MANDATORY)

The following requirements address real-world bugs observed in generated test code (`library-management` project, 2026-05-22). Claude MUST apply these when generating `tests/fixtures/builders.ts` and related helpers.

### Fixture ID generation MUST use real UUIDs

**Why**: Service and API layers validate IDs with `z.string().uuid()` from zod. A custom format like `m-00000001-0000-0000-0000-000000000000` does NOT pass zod's UUID v4 check, causing 7+ integration tests to fail with `Expected: 201 / Received: 400` (validation error). The exact failure observed in `library-management`.

**Required pattern**:

```typescript
// tests/fixtures/builders.ts
import { randomUUID } from 'crypto';

let _counter = 0;

/** Generate a fresh RFC 4122 v4 UUID for fixture IDs. */
export function uid(): string {
  _counter += 1;
  return randomUUID();
}

// Use uid() everywhere fixtures need an ID:
export function buildMember(overrides: Partial<Member> = {}): Member {
  return {
    id: uid(),
    name: 'Test Member',
    // ...
    ...overrides,
  };
}
```

**Do NOT** generate IDs with custom prefixes like `m-`, `o-`, `u-` for fixtures used in code paths that hit zod validation. If a domain-specific identifier is genuinely needed (e.g., a non-PK business code), keep it as a separate field, not the primary `id`.

### Verification

After generating fixtures, confirm UUID usage:

```bash
grep -n "randomUUID" {WORK_DIR}/{project}/backend/tests/fixtures/builders.ts
# Should print at least one match. If absent, fix before running tests.
```

---

*Generated by usecase-to-test-v1*
