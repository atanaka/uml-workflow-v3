---
name: usecase-to-test-v1
description: Generate comprehensive test code from use case specifications and domain models with multi-language test descriptions (Japanese/English). Creates unit tests, integration tests, and E2E tests with business rule validation. Supports Jest, Vitest, Playwright, and Cypress frameworks. Inherits language settings for test case descriptions. Use after code generation to ensure complete test coverage.
---

# Use Case to Test Code Generator v1

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
4. **⭐ Security configuration:** `{project}_security-config.json`
   - **MUST read this file before generating tests**
   - Used to generate: authentication tests, RBAC tests, rate limit tests, input validation tests, audit log tests
   - If file is missing, warn user and skip security test generation

### Optional

5. **Test configuration:**
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

### 4. ⭐ Security Tests (from security-config.json) — MANDATORY

**Claude MUST generate `tests/security/security.test.ts` by reading `{project}_security-config.json`.**

Generate tests covering ALL of the following categories:

#### 4a. Authentication Tests
```typescript
// From security-config.json: authentication section
describe('認証テスト', () => {
  it('未認証リクエストは401を返す')
  it('無効なJWTトークンは401を返す')
  it('期限切れトークンは401を返す')
  it('改ざんされたトークンは401を返す')
})
```

#### 4b. RBAC Tests (Role-Permission Matrix)
```typescript
// From security-config.json: permissions section
// Generate one test per role × resource × operation combination
describe('RBACテスト', () => {
  // For each resource in permissions:
  //   For each role:
  //     For each operation (create/read/update/delete):
  //       it('{role}は{resource}の{operation}を{許可/拒否}される')
})
```

#### 4c. Rate Limit Tests
```typescript
// From security-config.json: api_security.rate_limiting section
describe('レートリミットテスト', () => {
  // For each endpoint in rate_limiting:
  //   it('{endpoint}は{max}回超で429を返す')
})
```

#### 4d. Input Validation Tests
```typescript
describe('入力バリデーションテスト', () => {
  it('SQLインジェクション文字列は400を返す')
  it('XSSペイロードは400を返す')
  it('過大なペイロード（>10MB）は413を返す')
  it('不正なJSON形式は400を返す')
})
```

#### 4e. Audit Log Tests
```typescript
// From security-config.json: audit_logging.events section
describe('監査ログテスト', () => {
  // For each event in audit_logging.events:
  //   it('{event}発生時に監査ログが記録される')
  it('ログにパスワード・トークンが含まれない')
})
```

#### 4f. Data Protection Tests
```typescript
// From security-config.json: data_protection section
describe('データ保護テスト', () => {
  // For each field in sensitive_fields:
  //   it('{field}がレスポンスに平文で含まれない')
  it('パスワードがbcryptでハッシュ化されている')
})
```

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

4. **⭐ Security Tests** (generated from security-config.json)
   - `tests/security/security.test.ts`
   - Covers: Authentication, RBAC, Rate Limiting, Input Validation, Audit Logging, Data Protection

5. **Test Fixtures**
   - `tests/fixtures/{entity}.fixture.ts`

6. **Configuration**
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

| Layer | Unit | Integration | E2E | Security |
|-------|------|-------------|-----|----------|
| Domain Entities | ✅ All methods | ✅ State transitions | - | - |
| Services | - | ✅ All use cases | - | - |
| API | - | ✅ All endpoints | ✅ Critical flows | - |
| Business Rules | ✅ All rules | ✅ Combinations | - | - |
| Authentication | - | - | - | ✅ JWT/Token validation |
| Authorization (RBAC) | - | - | - | ✅ All role×resource combinations |
| Rate Limiting | - | - | - | ✅ All configured limits |
| Input Validation | - | - | - | ✅ Injection, XSS, oversized payloads |
| Audit Logging | - | - | - | ✅ All configured events |
| Data Protection | - | - | - | ✅ Sensitive field masking |

Target: 80%+ code coverage, 100% security-config.json coverage

---

*Generated by usecase-to-test-v1*
