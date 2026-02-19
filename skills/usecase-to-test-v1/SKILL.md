---
name: usecase-to-test-v1
description: Generate comprehensive test code from use case specifications, domain models, and security design with multi-language test descriptions (Japanese/English). Creates unit tests, integration tests, E2E tests, and security tests covering authentication, authorization, rate limiting, and audit logging. Supports Jest, Vitest, Playwright, and Cypress frameworks. Inherits language settings for test case descriptions. Use after code generation to ensure complete test coverage including OWASP-aligned security validation.
---

# Use Case to Test Code Generator v1

Generate comprehensive, production-ready test suites from use case specifications and domain models.

## Overview

This skill automatically generates test code that validates:
- Business logic correctness
- State transitions
- Business rule compliance
- API contract adherence
- End-to-end user flows
- **Security controls (authentication, authorization, rate limiting, audit logging)** ⭐ NEW!

**Key capabilities:**
- ✅ Generates unit tests for domain entities
- ✅ Generates integration tests for services
- ✅ Generates E2E tests for user flows
- ✅ Validates business rules (BR-001, BR-002, etc.)
- ✅ Tests state machine transitions
- ✅ Generates test data fixtures
- ✅ Supports multiple test frameworks (Jest, Vitest, Playwright, Cypress)
- ✅ **Multi-language test descriptions (Japanese/English)** ⭐ NEW!
- ✅ **Security tests from security-config.json (JWT, RBAC, Rate Limit, Audit)** ⭐ NEW!

---

## Language Support ⭐ NEW!

Generates test code with language-appropriate descriptions. Code identifiers remain in English, but test descriptions (describe/it blocks) follow the configured language.

**Example:**
- Japanese: `describe('商品を注文する', () => { it('在庫ありの場合、注文が完了する', ...) })`
- English: `describe('Place Order', () => { it('should complete order when stock is available', ...) })`

**Configuration inherited from:** domain-model.json metadata.language

---

## Position in Workflow

```
Step 1: scenario-to-activity-v1
  ↓
Step 2: activity-to-usecase-v1
  ↓
Step 3: usecase-to-class-v1
  ↓
Step 4: class-to-statemachine-v1
  ↓
Step 5: usecase-to-sequence-v1
  ↓
Step 6: model-validator-v1
  ↓
Step 7: security-design-v1   ← security-config.json generated here
  ↓
Step 8: usecase-to-code-v1   ← source code generated here
  ↓
Step 9: usecase-to-test-v1 ← YOU ARE HERE
         Inputs: usecase-output.json + domain-model.json
                 + security-config.json (Step 7 output) ⭐ NEW!
  ↓ Test suites (business + security)
```

---

## Input

### Required

1. **Use case specifications:** `{project}_usecase-output.json`
2. **Domain model:** `{project}_domain-model.json`
3. **Generated source code:** Backend/Frontend code structure

### Optional

4. **Security configuration:** `{project}_security-config.json` ⭐ NEW!
   - If present: generates `tests/security/` suite automatically
   - Source: output of security-design-v1 (Step 7)
   - Drives tests for: auth, RBAC, rate limiting, encryption, audit logging

5. **Test configuration:**
   - `test_framework`: 'jest' | 'vitest' (default: 'jest')
   - `e2e_framework`: 'playwright' | 'cypress' (default: 'playwright')
   - `coverage_threshold`: number (default: 80)

### Security Config Schema (expected fields)

```json
{
  "auth": {
    "type": "JWT",
    "accessTokenExpiry": "1h",
    "refreshTokenExpiry": "7d",
    "passwordHash": "bcrypt:12"
  },
  "encryption": {
    "fields": ["Entity.field", ...]
  },
  "rateLimit": {
    "login":  { "max": 5,   "windowMs": 60000 },
    "orders": { "max": 60,  "windowMs": 3600000 }
  },
  "cors": { "allowedOrigins": ["https://..."] },
  "audit": { "retention": "7years", "table": "audit_logs" }
}
```

---

## Test Generation Strategy

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

### 4. Security Tests ⭐ NEW! (requires security-config.json)

**Triggered automatically when `{project}_security-config.json` exists.**

Generate tests derived from each section of security-config.json:

#### 4a. Authentication Tests (`auth` section)
- Valid JWT → 200 OK
- Expired access token → 401
- Invalid/tampered token → 401
- Missing Authorization header → 401
- Refresh token rotation works correctly
- Password stored as bcrypt hash (not plaintext)

#### 4b. Authorization / RBAC Tests (`roles` or role matrix in security-design.md)
- Each role can access permitted endpoints → 200
- Each role is denied forbidden endpoints → 403
- Unauthenticated request → 401
- Example: `buyer` cannot POST to `/credit-approvals/:id/approve`

#### 4c. Rate Limiting Tests (`rateLimit` section)
- Under limit → 200
- Exactly at limit → 200
- Over limit → 429 Too Many Requests
- Window reset restores access

#### 4d. Encryption Tests (`encryption` section)
- Encrypted fields are NOT stored as plaintext in DB
- Encrypted fields are NOT exposed in API responses (unless explicitly allowed)
- Decryption produces correct original value

#### 4e. Audit Logging Tests (`audit` section)
- Key actions (login, order create, approval) write to audit_logs table
- Audit log entry contains: userId, action, resource, result, timestamp
- Failed actions are also logged

#### 4f. Security Headers & CORS Tests
- Required security headers present (Content-Security-Policy, X-Frame-Options, etc.)
- CORS rejects requests from non-allowlisted origins
- CORS accepts requests from allowlisted origins

---

## Output

### Generated Files

1. **Unit Tests**
   - `tests/unit/domain/entities/{Entity}.test.ts`
   - `tests/unit/domain/services/{Service}.test.ts`

2. **Integration Tests**
   - `tests/integration/services/{Service}.test.ts`
   - `tests/api/{endpoint}.api.test.ts`

3. **E2E Tests**
   - `tests/e2e/{feature}.spec.ts`

4. **Security Tests** ⭐ NEW! (generated when security-config.json present)
   - `tests/security/auth.test.ts`          — JWT, token expiry, refresh
   - `tests/security/authorization.test.ts` — RBAC, role-based access control
   - `tests/security/rate-limit.test.ts`    — rate limiting per endpoint
   - `tests/security/encryption.test.ts`    — PII field encryption verification
   - `tests/security/audit.test.ts`         — audit log entry validation
   - `tests/security/headers.test.ts`       — HTTP security headers & CORS

5. **Test Fixtures**
   - `tests/fixtures/{entity}.fixture.ts`

6. **Configuration**
   - `jest.config.js` or `vitest.config.ts`
   - `playwright.config.ts` or `cypress.config.ts`

---

## Usage Example

```bash
# Generate tests for B2B EC Platform
usecase-to-test-v1 --project b2b-ec-platform

# Generated files:
# ✅ tests/unit/domain/entities/Order.test.ts
# ✅ tests/integration/services/OrderService.test.ts
# ✅ tests/api/orders.api.test.ts
# ✅ tests/e2e/order-flow.spec.ts
# ✅ tests/fixtures/orders.fixture.ts
#
# Security tests (if security-config.json present):
# ✅ tests/security/auth.test.ts
# ✅ tests/security/authorization.test.ts
# ✅ tests/security/rate-limit.test.ts
# ✅ tests/security/encryption.test.ts
# ✅ tests/security/audit.test.ts
# ✅ tests/security/headers.test.ts
```

---

## Test Coverage Matrix

| Layer | Unit | Integration | E2E |
|-------|------|-------------|-----|
| Domain Entities | ✅ All methods | ✅ State transitions | - |
| Services | - | ✅ All use cases | - |
| API | - | ✅ All endpoints | ✅ Critical flows |
| Business Rules | ✅ All rules | ✅ Combinations | - |
| **Authentication** | - | ✅ JWT / token lifecycle | - |
| **Authorization (RBAC)** | - | ✅ All role × endpoint | - |
| **Rate Limiting** | - | ✅ Limit / over-limit / reset | - |
| **Encryption** | ✅ Field-level | ✅ DB storage / API response | - |
| **Audit Logging** | - | ✅ All key actions logged | - |
| **Security Headers** | - | ✅ Headers / CORS | - |

Target: 80%+ code coverage (business) + 100% coverage of security-config.json rules

---

*Generated by usecase-to-test-v1*
