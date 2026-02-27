
# Security Design v1

Generate production-grade security architecture and design documents from UML workflow artifacts.

## Overview / 概要

This skill analyzes domain models and use case specifications to generate:
1. **Security Design Document** - Comprehensive security architecture and policies
2. **Security Configuration JSON** - Structured configuration for code generation

**Key capabilities:**
- ✅ Authentication design (JWT, OAuth2, Session-based)
- ✅ Authorization design (RBAC, ABAC, Policy-based)
- ✅ Data protection & encryption policies
- ✅ API security (Rate limiting, CORS, Input validation)
- ✅ OWASP Top 10 countermeasures
- ✅ Role-Permission matrix generation
- ✅ Audit logging design
- ✅ Session management design
- ✅ Security-aware error handling
- ✅ Compliance readiness (GDPR, SOC2, PCI-DSS awareness)
- ✅ **Multi-language security documents (Japanese/English/Bilingual)** ⭐
- ✅ **Inherits language from domain model** ⭐
- ✅ **Structured JSON output for usecase-to-code-v1 integration** ⭐

---

## Language Support / 言語サポート

### Overview / 概要

This skill generates security design documents in multiple languages, inheriting settings from the domain model for consistency with project documentation.

**Supported Languages:**
- **Japanese (日本語)**: Security design documents in Japanese
- **English**: Security design documents in English
- **Bilingual (バイリンガル)**: Dual-language documents for international teams

### Language Scope

**What is localized:**
- ✅ Document headers and sections
- ✅ Design descriptions and rationale
- ✅ Threat descriptions and countermeasures
- ✅ Policy statements and guidelines
- ✅ Summary tables and matrices

**What is NOT localized:**
- ✅ Entity names (always show original)
- ✅ Attribute names (always show original)
- ✅ HTTP headers, status codes, technical terms
- ✅ JSON/code configuration snippets
- ✅ OWASP, CVE, standard identifiers

### Language Inheritance

**Priority Order:**
1. **From domain-model.json** (highest priority)
   - Reads `metadata.language` if present
   - Ensures document matches model language
2. **Manual override** (if specified)
   - Can override via `document_language` parameter
3. **Auto-detection** (fallback)
   - Analyzes entity descriptions
   - Defaults to English if unclear

### Language Configuration

**Parameters:**
```python
language_options = {
    "document_language": "auto",         # auto | ja | en | bilingual
    "inherit_from_domain_model": True,   # Inherit language settings
    "policy_statements": "auto",         # auto | ja | en
    "threat_descriptions": "auto",       # auto | ja | en
    "technical_terms": "preserve"        # preserve | translate
}
```

### Document Language Examples

#### Japanese Document (language="ja")
```markdown
# セキュリティ設計書

**プロジェクト:** order-management
**作成日:** 2026-02-16
**バージョン:** 1.0

## 1. 認証設計 / Authentication Design

### 1.1 認証方式
JWT (JSON Web Token) ベースの認証を採用します。

**選定理由:**
- ステートレスなAPI設計に適合
- マイクロサービス間の認証に対応
- トークンの有効期限管理が容易

### 1.2 認証フロー
1. ユーザーがログインエンドポイントに認証情報を送信
2. サーバーが認証情報を検証
3. 成功時にアクセストークンとリフレッシュトークンを発行
4. クライアントが以降のリクエストにアクセストークンを付与

**トークン設定:**
| 項目 | 値 |
|------|-----|
| アクセストークン有効期限 | 15分 |
| リフレッシュトークン有効期限 | 7日 |
| アルゴリズム | RS256 |
```

#### English Document (language="en")
```markdown
# Security Design Document

**Project:** order-management
**Date:** 2026-02-16
**Version:** 1.0

## 1. Authentication Design / 認証設計

### 1.1 Authentication Method
JWT (JSON Web Token) based authentication is adopted.

**Rationale:**
- Suitable for stateless API design
- Supports authentication between microservices
- Easy token expiration management

### 1.2 Authentication Flow
1. User sends credentials to login endpoint
2. Server validates credentials
3. On success, issues access token and refresh token
4. Client includes access token in subsequent requests

**Token Configuration:**
| Item | Value |
|------|-------|
| Access token expiry | 15 minutes |
| Refresh token expiry | 7 days |
| Algorithm | RS256 |
```

### Language Selection Guide

| Team Type | Document Language | Rationale |
|-----------|-------------------|-----------|
| Japanese-only | ja | Native language for clarity |
| International | en | Standard for global teams |
| Mixed (Japan-based) | bilingual | Accessibility for both groups |
| Offshore handover | bilingual | Documentation continuity |

---

## Position in Workflow / ワークフロー内の位置

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
Step 7: security-design-v1 ← YOU ARE HERE
  ↓ Security design + config JSON
Step 8: usecase-to-code-v1 (uses security-config.json)
  ↓
Step 9: usecase-to-test-v1 (uses security-config.json for security tests)
```

**Why before code generation:**
- Security must be designed before implementation (Security by Design)
- Generates security-config.json consumed by usecase-to-code-v1
- Ensures authentication/authorization are integrated from the start
- Prevents security as an afterthought

---

## Input / 入力

### Required Models

**1. Domain Model (Single Source of Truth):**
- `{project}_domain-model.json`

**2. Use Case Specifications:**
- `{project}_usecase-output.json`

### Optional Models

**3. Validation Report:**
- `{project}_validation-report.md` (from model-validator-v1)

**4. Sequence Diagrams:**
- `{project}_sequence.puml` (for API endpoint analysis)

**5. State Machine Diagrams:**
- `{project}_statemachine.puml` (for state transition security)

---

## Output / 出力

### 1. Security Design Document

**File:** `{project}_security-design.md`

Comprehensive security architecture document containing:
- Authentication design
- Authorization design (RBAC/ABAC)
- Data protection policies
- API security specifications
- OWASP Top 10 countermeasures
- Role-Permission matrix
- Audit logging design
- Session management
- Error handling policies
- Compliance considerations

### 2. Security Configuration JSON

**File:** `{project}_security-config.json`

Structured configuration consumed by usecase-to-code-v1 and usecase-to-test-v1:

```json
{
  "metadata": {
    "project": "order-management",
    "version": "1.0",
    "generated_by": "security-design-v1",
    "language": "ja"
  },
  "authentication": {
    "method": "jwt",
    "token_config": {
      "access_token_expiry": "15m",
      "refresh_token_expiry": "7d",
      "algorithm": "RS256",
      "issuer": "order-management-api"
    },
    "password_policy": {
      "min_length": 12,
      "require_uppercase": true,
      "require_lowercase": true,
      "require_digits": true,
      "require_special": true,
      "max_age_days": 90,
      "history_count": 5
    },
    "mfa": {
      "enabled": true,
      "methods": ["totp", "email"],
      "required_for_roles": ["admin", "manager"]
    },
    "session": {
      "max_concurrent": 3,
      "idle_timeout": "30m",
      "absolute_timeout": "12h"
    }
  },
  "authorization": {
    "model": "rbac",
    "roles": [
      {
        "name": "admin",
        "description": "System administrator",
        "permissions": ["*"]
      },
      {
        "name": "manager",
        "description": "Department manager",
        "permissions": ["order:*", "product:read", "report:*"]
      },
      {
        "name": "operator",
        "description": "Standard operator",
        "permissions": ["order:create", "order:read", "order:update", "product:read"]
      },
      {
        "name": "viewer",
        "description": "Read-only access",
        "permissions": ["order:read", "product:read"]
      }
    ],
    "permission_matrix": {},
    "resource_policies": []
  },
  "data_protection": {
    "encryption": {
      "at_rest": "AES-256-GCM",
      "in_transit": "TLS 1.3",
      "key_management": "envelope_encryption"
    },
    "pii_fields": [],
    "sensitive_fields": [],
    "data_classification": {
      "public": [],
      "internal": [],
      "confidential": [],
      "restricted": []
    },
    "data_retention": {
      "default_days": 365,
      "audit_logs_days": 730,
      "deleted_data_days": 30
    }
  },
  "api_security": {
    "rate_limiting": {
      "enabled": true,
      "default_rpm": 60,
      "authenticated_rpm": 120,
      "admin_rpm": 300,
      "burst_multiplier": 2
    },
    "cors": {
      "allowed_origins": [],
      "allowed_methods": ["GET", "POST", "PUT", "DELETE", "PATCH"],
      "allowed_headers": ["Content-Type", "Authorization"],
      "max_age": 3600
    },
    "input_validation": {
      "max_body_size": "10mb",
      "sanitize_html": true,
      "validate_content_type": true,
      "reject_unknown_fields": true
    },
    "headers": {
      "strict_transport_security": "max-age=31536000; includeSubDomains",
      "content_security_policy": "default-src 'self'",
      "x_frame_options": "DENY",
      "x_content_type_options": "nosniff",
      "referrer_policy": "strict-origin-when-cross-origin"
    }
  },
  "audit": {
    "enabled": true,
    "events": [
      "auth.login", "auth.logout", "auth.failed",
      "data.create", "data.update", "data.delete",
      "admin.role_change", "admin.config_change",
      "security.permission_denied", "security.rate_limited"
    ],
    "fields": ["timestamp", "user_id", "action", "resource", "ip_address", "user_agent", "result"],
    "storage": "database",
    "retention_days": 730
  },
  "owasp_top10": {
    "A01_broken_access_control": { "status": "mitigated", "measures": [] },
    "A02_cryptographic_failures": { "status": "mitigated", "measures": [] },
    "A03_injection": { "status": "mitigated", "measures": [] },
    "A04_insecure_design": { "status": "mitigated", "measures": [] },
    "A05_security_misconfiguration": { "status": "mitigated", "measures": [] },
    "A06_vulnerable_components": { "status": "mitigated", "measures": [] },
    "A07_auth_failures": { "status": "mitigated", "measures": [] },
    "A08_software_data_integrity": { "status": "mitigated", "measures": [] },
    "A09_logging_monitoring_failures": { "status": "mitigated", "measures": [] },
    "A10_ssrf": { "status": "mitigated", "measures": [] }
  }
}
```

---

## Security Design Workflow / セキュリティ設計フロー

### Step 0: Language Configuration

**0a. Load domain model:**
```python
domain_model = load_json(f'{project}_domain-model.json')
```

**0b. Extract language configuration:**
```python
# Priority 1: Check metadata.language
if "metadata" in domain_model and "language" in domain_model["metadata"]:
    language = domain_model["metadata"]["language"]

# Priority 2: Infer from entity descriptions
elif "entities" in domain_model and len(domain_model["entities"]) > 0:
    first_entity = domain_model["entities"][0]
    if "description" in first_entity:
        language = detect_language(first_entity["description"])
    else:
        language = "en"
else:
    language = "en"  # Default
```

**0c. Display configuration:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔒 Security Design Language
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Source: domain-model.json
Document language: Japanese (日本語)
Policy statements: Japanese
Threat descriptions: Japanese
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### Step 1: Analyze Domain Model

**1a. Extract entities and their security-relevant attributes:**
```python
entities = domain_model["entities"]

# Identify actors/users
user_entities = [e for e in entities if is_user_entity(e)]

# Identify sensitive data
sensitive_entities = [e for e in entities if has_sensitive_data(e)]

# Identify entities with status (state transitions = authorization checkpoints)
stateful_entities = [e for e in entities if has_status_field(e)]
```

**1b. Classify data sensitivity:**
```python
for entity in entities:
    for attr in entity["attributes"]:
        classification = classify_attribute(attr)
        # "public", "internal", "confidential", "restricted"
        data_classification[entity["name"]].append({
            "attribute": attr["name"],
            "classification": classification,
            "requires_encryption": classification in ["confidential", "restricted"],
            "is_pii": is_pii(attr)
        })
```

**Classification Rules:**

| Pattern | Classification | Examples |
|---------|---------------|----------|
| password, secret, token | **restricted** | password_hash, api_secret |
| email, phone, address, ssn | **confidential** (PII) | email, phone_number |
| name, birth_date, national_id | **confidential** (PII) | full_name, date_of_birth |
| price, amount, balance | **confidential** | unit_price, total_amount |
| status, type, category | **internal** | order_status, product_type |
| id, created_at, updated_at | **internal** | entity_id, timestamps |
| description, notes | **public** | product_description |

---

### Step 2: Analyze Use Cases for Security Requirements

**2a. Extract actors and their roles:**
```python
usecases = load_json(f'{project}_usecase-output.json')

# Map actors to roles
actors = {}
for uc in usecases["use_cases"]:
    for actor in uc["actors"]:
        if actor not in actors:
            actors[actor] = {
                "use_cases": [],
                "suggested_role": infer_role(actor),
                "permissions": set()
            }
        actors[actor]["use_cases"].append(uc["id"])
        actors[actor]["permissions"].update(extract_permissions(uc))
```

**2b. Build permission matrix:**
```python
# For each use case, determine required permissions
permission_matrix = {}
for uc in usecases["use_cases"]:
    resource = infer_resource(uc)
    actions = infer_actions(uc)
    
    for actor in uc["actors"]:
        role = actors[actor]["suggested_role"]
        if role not in permission_matrix:
            permission_matrix[role] = {}
        if resource not in permission_matrix[role]:
            permission_matrix[role][resource] = set()
        permission_matrix[role][resource].update(actions)
```

**Permission Inference Rules:**

| Use Case Pattern | Inferred Permissions |
|-----------------|---------------------|
| "〜を登録/作成" or "Create/Register" | resource:create |
| "〜を参照/表示" or "View/List" | resource:read |
| "〜を更新/編集" or "Update/Edit" | resource:update |
| "〜を削除" or "Delete/Remove" | resource:delete |
| "〜を承認" or "Approve" | resource:approve |
| "〜を管理" or "Manage" | resource:* |
| "レポート/集計" or "Report" | resource:report |
| "〜をエクスポート" or "Export" | resource:export |

**2c. Identify security-critical use cases:**
```python
# Use cases that require special security attention
security_critical_ucs = []

for uc in usecases["use_cases"]:
    # Financial transactions
    if involves_money(uc):
        security_critical_ucs.append({"uc": uc, "reason": "financial_transaction"})
    
    # Personal data handling
    if involves_pii(uc):
        security_critical_ucs.append({"uc": uc, "reason": "pii_handling"})
    
    # Admin operations
    if is_admin_operation(uc):
        security_critical_ucs.append({"uc": uc, "reason": "admin_operation"})
    
    # State transitions (approval workflows)
    if involves_state_change(uc):
        security_critical_ucs.append({"uc": uc, "reason": "state_transition"})
    
    # Data deletion
    if involves_deletion(uc):
        security_critical_ucs.append({"uc": uc, "reason": "data_deletion"})
```

---

### Step 3: Design Authentication

**3a. Select authentication method:**

Based on domain analysis:

| Factor | JWT | Session | OAuth2 |
|--------|-----|---------|--------|
| Stateless APIs | ✅ Best | ❌ | ✅ Good |
| Microservices | ✅ Best | ❌ | ✅ Good |
| Browser-only apps | ✅ Good | ✅ Best | ✅ Good |
| Third-party integration | ❌ | ❌ | ✅ Best |
| Mobile apps | ✅ Best | ❌ | ✅ Good |
| Simple monolith | ✅ Good | ✅ Best | ⚠️ Overhead |

**3b. Design password policy:**
```python
password_policy = {
    "min_length": 12,
    "require_uppercase": True,
    "require_lowercase": True,
    "require_digits": True,
    "require_special": True,
    "max_age_days": 90,
    "history_count": 5,
    "lockout_threshold": 5,
    "lockout_duration_minutes": 30,
    "bcrypt_rounds": 12
}
```

**3c. Design MFA (if applicable):**
```python
mfa_config = {
    "enabled": has_admin_roles or has_financial_operations,
    "methods": ["totp"],
    "required_for_roles": [r for r in roles if r.is_privileged],
    "remember_device_days": 30
}
```

**3d. Design token management:**
```python
token_config = {
    "access_token_expiry": "15m",
    "refresh_token_expiry": "7d",
    "algorithm": "RS256",
    "issuer": f"{project}-api",
    "audience": f"{project}-client",
    "claims": ["sub", "role", "permissions", "iat", "exp"],
    "rotation": {
        "refresh_token_rotation": True,
        "revoke_on_reuse": True
    }
}
```

---

### Step 4: Design Authorization

**4a. Build RBAC model from analyzed actors:**

```python
roles = []
for actor_name, actor_info in actors.items():
    role = {
        "name": actor_info["suggested_role"],
        "display_name": actor_name,
        "description": f"Role for {actor_name}",
        "permissions": list(actor_info["permissions"]),
        "is_default": actor_info["suggested_role"] == "viewer",
        "is_admin": actor_info["suggested_role"] == "admin"
    }
    roles.append(role)
```

**4b. Generate permission matrix:**

Example output:

| Resource | admin | manager | operator | viewer |
|----------|-------|---------|----------|--------|
| Order | CRUD + Approve | CRUD + Approve | CRU | R |
| Product | CRUD | R | R | R |
| Customer | CRUD | CR | R | R |
| Report | * | * | R | R |
| User | CRUD | R | - | - |
| Config | CRUD | - | - | - |

**4c. Design resource-level policies:**
```python
resource_policies = []
for entity in stateful_entities:
    # State-transition authorization
    for transition in entity["state_transitions"]:
        policy = {
            "resource": entity["name"],
            "action": f"transition_{transition['from']}_{transition['to']}",
            "allowed_roles": infer_transition_roles(transition),
            "conditions": transition.get("guards", [])
        }
        resource_policies.append(policy)
```

**4d. Design data-level access controls:**
```python
# Owner-based access for personal data
data_policies = []
for entity in entities:
    if has_owner_field(entity):
        data_policies.append({
            "resource": entity["name"],
            "type": "owner_based",
            "rule": "Users can only access their own records",
            "field": "owner_id",
            "exceptions": ["admin", "manager"]
        })
```

---

### Step 5: Design Data Protection

**5a. Identify fields requiring encryption:**
```python
encrypted_fields = []
for entity_name, classifications in data_classification.items():
    for field in classifications:
        if field["requires_encryption"]:
            encrypted_fields.append({
                "entity": entity_name,
                "field": field["attribute"],
                "encryption_type": "field_level" if field["is_pii"] else "column_level",
                "algorithm": "AES-256-GCM"
            })
```

**5b. Design PII handling:**
```python
pii_handling = {
    "identified_pii_fields": pii_fields,
    "anonymization_strategy": "pseudonymization",
    "consent_tracking": True,
    "right_to_erasure": True,
    "data_export_format": "json",
    "masking_rules": {
        "email": "j***@***.com",
        "phone": "***-****-1234",
        "name": "J*** D***",
        "address": "[REDACTED]"
    }
}
```

**5c. Design encryption layers:**

| Layer | Method | Scope |
|-------|--------|-------|
| Transport | TLS 1.3 | All HTTP traffic |
| Application | AES-256-GCM | PII and sensitive fields |
| Database | Transparent Data Encryption | Entire database |
| Backup | AES-256 | All backup files |
| Key Management | Envelope Encryption | Encryption keys |

---

### Step 6: Design API Security

**6a. Rate limiting configuration:**
```python
rate_limits = {
    "global": {
        "requests_per_minute": 60,
        "burst": 120
    },
    "authenticated": {
        "requests_per_minute": 120,
        "burst": 240
    },
    "endpoints": {
        "/auth/login": {"requests_per_minute": 10, "burst": 15},
        "/auth/register": {"requests_per_minute": 5, "burst": 10},
        "/auth/password-reset": {"requests_per_minute": 3, "burst": 5}
    }
}
```

**6b. Input validation rules:**
```python
# Generate validation rules from domain model attributes
validation_rules = {}
for entity in entities:
    entity_rules = {}
    for attr in entity["attributes"]:
        rule = {
            "type": map_type_to_validation(attr["type"]),
            "required": not attr.get("optional", False),
            "max_length": infer_max_length(attr),
            "pattern": infer_pattern(attr),
            "sanitize": needs_sanitization(attr)
        }
        entity_rules[attr["name"]] = rule
    validation_rules[entity["name"]] = entity_rules
```

**6c. Security headers:**
```python
security_headers = {
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains; preload",
    "Content-Security-Policy": "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'",
    "X-Frame-Options": "DENY",
    "X-Content-Type-Options": "nosniff",
    "X-XSS-Protection": "0",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
    "Cache-Control": "no-store, no-cache, must-revalidate"
}
```

---

### Step 7: OWASP Top 10 Analysis

For each OWASP Top 10 (2021) category, analyze the domain model and generate countermeasures:

**A01: Broken Access Control**
```python
measures = []
# Check: Every use case has actor restrictions
for uc in usecases:
    if not uc.get("actors"):
        measures.append(f"WARNING: {uc['name']} has no actor restrictions")

# Check: State transitions have role guards
for entity in stateful_entities:
    for transition in entity.get("state_transitions", []):
        if not transition.get("allowed_roles"):
            measures.append(f"WARNING: {entity['name']}.{transition['name']} has no role guard")

countermeasures["A01"] = {
    "status": "mitigated",
    "measures": [
        "RBAC implemented for all endpoints",
        "Resource-level access control for owned data",
        "State transition authorization enforced",
        "Default-deny access policy",
        "CORS configuration restricts origins",
        "JWT claims validated on every request"
    ] + measures
}
```

**A02: Cryptographic Failures**
```python
countermeasures["A02"] = {
    "status": "mitigated",
    "measures": [
        f"TLS 1.3 enforced for all connections",
        f"{len(encrypted_fields)} sensitive fields encrypted with AES-256-GCM",
        "Passwords hashed with bcrypt (cost factor 12)",
        "No sensitive data in URLs or logs",
        "Secure key management with envelope encryption",
        "HSTS header enforced"
    ]
}
```

**A03: Injection**
```python
countermeasures["A03"] = {
    "status": "mitigated",
    "measures": [
        "Parameterized queries for all database operations",
        "Input validation on all API endpoints",
        "HTML sanitization for user-provided content",
        "Content-Type validation",
        "ORM used for database access (no raw SQL)",
        "Output encoding for XSS prevention"
    ]
}
```

**A04: Insecure Design**
```python
countermeasures["A04"] = {
    "status": "mitigated",
    "measures": [
        "Security design review completed (this document)",
        "Threat modeling performed for critical use cases",
        "Business logic validation at domain model level",
        "Rate limiting on authentication endpoints",
        "Account lockout after failed attempts",
        "Principle of least privilege applied"
    ]
}
```

**A05: Security Misconfiguration**
```python
countermeasures["A05"] = {
    "status": "mitigated",
    "measures": [
        "Security headers configured (HSTS, CSP, X-Frame-Options)",
        "Default credentials removed",
        "Error messages do not expose stack traces",
        "Unnecessary HTTP methods disabled",
        "Directory listing disabled",
        "Debug mode disabled in production"
    ]
}
```

**A06: Vulnerable and Outdated Components**
```python
countermeasures["A06"] = {
    "status": "awareness",
    "measures": [
        "Dependency audit recommended (npm audit / pip audit)",
        "Automated vulnerability scanning in CI/CD",
        "Regular dependency updates scheduled",
        "Lock files committed to version control"
    ]
}
```

**A07: Identification and Authentication Failures**
```python
countermeasures["A07"] = {
    "status": "mitigated",
    "measures": [
        f"Password policy enforced (min {password_policy['min_length']} chars, complexity required)",
        f"Account lockout after {password_policy['lockout_threshold']} failed attempts",
        f"MFA {'enabled' if mfa_config['enabled'] else 'available'} for privileged roles",
        "Session management with idle and absolute timeouts",
        "Refresh token rotation with reuse detection",
        "Credential stuffing protection via rate limiting"
    ]
}
```

**A08: Software and Data Integrity Failures**
```python
countermeasures["A08"] = {
    "status": "mitigated",
    "measures": [
        "JWT signature verification on all tokens",
        "CSRF protection for state-changing operations",
        "Subresource Integrity (SRI) for CDN resources",
        "Signed API responses for critical operations"
    ]
}
```

**A09: Security Logging and Monitoring Failures**
```python
countermeasures["A09"] = {
    "status": "mitigated",
    "measures": [
        f"Audit logging for {len(audit_events)} event types",
        "Failed authentication attempts logged",
        "Access control failures logged",
        "Structured logging format (JSON)",
        f"Log retention: {audit_config['retention_days']} days",
        "Alerting recommended for anomalous patterns"
    ]
}
```

**A10: Server-Side Request Forgery (SSRF)**
```python
countermeasures["A10"] = {
    "status": "mitigated",
    "measures": [
        "URL validation for any user-supplied URLs",
        "Allowlist for external service connections",
        "No direct URL fetching from user input",
        "Network segmentation (API server isolated)"
    ]
}
```

---

### Step 8: Design Audit Logging

**8a. Define audit events:**
```python
audit_events = []

# Authentication events
audit_events.extend([
    {"category": "auth", "event": "login", "severity": "info"},
    {"category": "auth", "event": "logout", "severity": "info"},
    {"category": "auth", "event": "login_failed", "severity": "warning"},
    {"category": "auth", "event": "account_locked", "severity": "warning"},
    {"category": "auth", "event": "password_changed", "severity": "info"},
    {"category": "auth", "event": "mfa_enabled", "severity": "info"},
    {"category": "auth", "event": "token_refreshed", "severity": "debug"},
])

# Data events (from domain model entities)
for entity in entities:
    for action in ["create", "update", "delete"]:
        audit_events.append({
            "category": "data",
            "event": f"{entity['name'].lower()}.{action}",
            "severity": "info",
            "fields": ["entity_id", "changed_fields", "old_values", "new_values"]
        })

# Security events
audit_events.extend([
    {"category": "security", "event": "permission_denied", "severity": "warning"},
    {"category": "security", "event": "rate_limited", "severity": "warning"},
    {"category": "security", "event": "invalid_token", "severity": "warning"},
    {"category": "security", "event": "suspicious_activity", "severity": "critical"},
])

# Admin events
audit_events.extend([
    {"category": "admin", "event": "role_changed", "severity": "info"},
    {"category": "admin", "event": "config_changed", "severity": "info"},
    {"category": "admin", "event": "user_created", "severity": "info"},
    {"category": "admin", "event": "user_deactivated", "severity": "warning"},
])
```

**8b. Define audit log schema:**
```json
{
  "timestamp": "2026-02-16T10:30:00.000Z",
  "event_id": "uuid",
  "category": "auth|data|security|admin",
  "event": "login|create|permission_denied|...",
  "severity": "debug|info|warning|critical",
  "user_id": "user-uuid",
  "user_role": "admin|manager|operator|viewer",
  "resource_type": "Order|Product|...",
  "resource_id": "entity-uuid",
  "action": "create|read|update|delete|...",
  "result": "success|failure",
  "ip_address": "192.168.1.1",
  "user_agent": "Mozilla/5.0...",
  "details": {},
  "correlation_id": "request-uuid"
}
```

---

### Step 9: Design Error Handling (Security-Aware)

**9a. Error response design:**
```python
error_responses = {
    "authentication": {
        "status": 401,
        "body": {"error": "unauthorized", "message": "Invalid or expired credentials"},
        "note": "Never reveal which part of credential is wrong"
    },
    "authorization": {
        "status": 403,
        "body": {"error": "forbidden", "message": "Insufficient permissions"},
        "note": "Do not reveal what permissions are needed"
    },
    "not_found_or_forbidden": {
        "status": 404,
        "body": {"error": "not_found", "message": "Resource not found"},
        "note": "Return 404 instead of 403 for resources user should not know about"
    },
    "validation": {
        "status": 422,
        "body": {"error": "validation_error", "message": "...", "details": []},
        "note": "Provide helpful validation messages without exposing internals"
    },
    "rate_limited": {
        "status": 429,
        "body": {"error": "rate_limited", "message": "Too many requests"},
        "headers": {"Retry-After": "60"}
    },
    "internal_error": {
        "status": 500,
        "body": {"error": "internal_error", "message": "An unexpected error occurred"},
        "note": "NEVER expose stack traces, SQL errors, or internal paths"
    }
}
```

**Security Error Handling Principles:**
1. **Never leak information** - Error messages must not reveal system internals
2. **Consistent timing** - Authentication checks should take constant time
3. **Log internally, sanitize externally** - Full details in logs, generic messages to clients
4. **Rate limit error endpoints** - Prevent error-based enumeration

---

### Step 10: Generate Output Files

**10a. Generate security-design.md:**

The document follows this structure:
```markdown
# Security Design Document / セキュリティ設計書

## 1. Overview / 概要
## 2. Authentication Design / 認証設計
   2.1 Authentication Method / 認証方式
   2.2 Password Policy / パスワードポリシー
   2.3 Multi-Factor Authentication / 多要素認証
   2.4 Token Management / トークン管理
   2.5 Session Management / セッション管理
## 3. Authorization Design / 認可設計
   3.1 Authorization Model / 認可モデル
   3.2 Role Definitions / ロール定義
   3.3 Permission Matrix / 権限マトリクス
   3.4 Resource-Level Policies / リソースレベルポリシー
   3.5 Data-Level Access Control / データレベルアクセス制御
## 4. Data Protection / データ保護
   4.1 Data Classification / データ分類
   4.2 Encryption Design / 暗号化設計
   4.3 PII Handling / 個人情報取扱い
   4.4 Data Retention / データ保持
## 5. API Security / APIセキュリティ
   5.1 Rate Limiting / レート制限
   5.2 Input Validation / 入力検証
   5.3 Security Headers / セキュリティヘッダー
   5.4 CORS Configuration / CORS設定
## 6. OWASP Top 10 Countermeasures / OWASP Top 10 対策
   6.1 - 6.10 (Each category)
## 7. Audit Logging / 監査ログ
   7.1 Audit Events / 監査イベント
   7.2 Log Schema / ログスキーマ
   7.3 Log Storage & Retention / ログ保管・保持
## 8. Error Handling / エラーハンドリング
   8.1 Error Response Design / エラーレスポンス設計
   8.2 Security Error Principles / セキュリティエラー原則
## 9. Compliance Considerations / コンプライアンス考慮事項
## 10. Security Checklist / セキュリティチェックリスト
```

**10b. Generate security-config.json:**

Create the structured JSON as defined in the Output section above, populated with all analyzed values.

**10c. Copy outputs to /mnt/user-data/outputs/:**
```python
output_dir = "/mnt/user-data/outputs"

# Save security design document
with open(f"{output_dir}/{project}_security-design.md", "w") as f:
    f.write(security_design_markdown)

# Save security configuration JSON
with open(f"{output_dir}/{project}_security-config.json", "w") as f:
    json.dump(security_config, f, indent=2, ensure_ascii=False)
```

---

## Integration with usecase-to-code-v1 / コード生成との連携

The `security-config.json` is designed to be consumed by code generation:

### Authentication Middleware Generation
```python
# Code generator reads authentication config
auth_config = security_config["authentication"]

if auth_config["method"] == "jwt":
    generate_jwt_middleware(auth_config["token_config"])
    generate_jwt_auth_routes(auth_config)

if auth_config["mfa"]["enabled"]:
    generate_mfa_middleware(auth_config["mfa"])
```

### Authorization Middleware Generation
```python
# Code generator reads authorization config
authz_config = security_config["authorization"]

for role in authz_config["roles"]:
    generate_role_guard(role)

generate_permission_middleware(authz_config["permission_matrix"])
```

### Security Headers Middleware
```python
# Code generator adds security headers
headers = security_config["api_security"]["headers"]
generate_security_headers_middleware(headers)
```

### Audit Logging Generation
```python
# Code generator creates audit service
audit_config = security_config["audit"]
generate_audit_service(audit_config)
generate_audit_middleware(audit_config["events"])
```

---

## Integration with usecase-to-test-v1 / テスト生成との連携

The `security-config.json` is also consumed by test generation:

### Security Test Generation
```python
# Test generator reads security config
security_tests = []

# Authentication tests
security_tests.extend([
    "should reject requests without authentication",
    "should reject expired tokens",
    "should reject invalid tokens",
    "should enforce password policy",
    "should lock account after failed attempts",
])

# Authorization tests
for role in security_config["authorization"]["roles"]:
    for resource, permissions in permission_matrix[role["name"]].items():
        security_tests.extend([
            f"should allow {role['name']} to {perm} {resource}"
            for perm in permissions
        ])
        
        # Negative tests
        denied_perms = all_permissions - permissions
        security_tests.extend([
            f"should deny {role['name']} to {perm} {resource}"
            for perm in denied_perms
        ])

# OWASP tests
security_tests.extend([
    "should prevent SQL injection",
    "should prevent XSS",
    "should enforce rate limiting",
    "should return proper security headers",
    "should not expose stack traces",
])
```

---

## Execution Summary / 実行サマリー

### Token Estimates

| Component | Estimated Tokens |
|-----------|-----------------|
| Domain model analysis | 1,500 |
| Use case security analysis | 2,000 |
| Authentication design | 1,000 |
| Authorization design | 1,500 |
| Data protection design | 800 |
| API security design | 700 |
| OWASP Top 10 analysis | 1,500 |
| Audit logging design | 500 |
| Document generation | 2,000 |
| JSON generation | 500 |
| **Total** | **~8,000** |

### Expected Output Files

| File | Size (est.) | Description |
|------|-------------|-------------|
| `{project}_security-design.md` | 15-25 KB | Comprehensive security document |
| `{project}_security-config.json` | 5-10 KB | Structured config for code gen |

---

## Error Handling / エラーハンドリング

### Missing Domain Model
```
❌ Error: {project}_domain-model.json not found
   Required for: security-design-v1
   
   Please run usecase-to-class-v1 first (Step 3)
```

### Missing Use Case Output
```
❌ Error: {project}_usecase-output.json not found
   Required for: security-design-v1
   
   Please run activity-to-usecase-v1 first (Step 2)
```

### No User Entities Found
```
⚠️ Warning: No user/actor entities detected in domain model
   Security design will use default role-based configuration
   
   Recommendation: Ensure domain model includes user-related entities
```

---

## Best Practices / ベストプラクティス

### For Maximum Security
1. **Always run security design** before code generation
2. **Review permission matrix** with stakeholders
3. **Customize password policy** for your compliance requirements
4. **Enable MFA** for all privileged roles
5. **Review OWASP countermeasures** for completeness

### For Compliance
1. **GDPR**: Ensure PII handling and right-to-erasure are configured
2. **SOC2**: Review audit logging completeness
3. **PCI-DSS**: Ensure encryption meets requirements for payment data
4. **HIPAA**: Additional encryption for health data (if applicable)

### For Development Efficiency
1. **Use security-config.json** as input to code generation
2. **Generate security tests** from the configuration
3. **Iterate on roles and permissions** before finalizing code
4. **Keep security design in sync** with domain model changes

---

## Success Criteria / 成功基準

Security design is complete when:

1. ✅ All entities analyzed for data sensitivity
2. ✅ All actors mapped to roles with permissions
3. ✅ Authentication method selected and configured
4. ✅ RBAC/permission matrix generated
5. ✅ OWASP Top 10 countermeasures documented
6. ✅ Audit logging events defined
7. ✅ security-design.md generated
8. ✅ security-config.json generated and valid
9. ✅ Files copied to /mnt/user-data/outputs/

---

**This skill ensures security is designed before implementation, following the "Security by Design" principle.**
