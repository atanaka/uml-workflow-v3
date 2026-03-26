
# Use Case to Class Diagram Generator v1

Create formal, comprehensive UML class diagrams by consolidating use case definitions with original business requirements.

## Overview / 概要

This skill generates the **formal class diagram** that serves as the authoritative domain model for code generation. It consolidates:
1. All use cases from activity-to-usecase-v1
2. Inferred domain models from use cases
3. Original business scenario information
4. Business rules and constraints

**Key characteristics:**
- ✅ Creates authoritative domain model
- ✅ Consolidates all available information
- ✅ Production-quality output
- ✅ Foundation for code generation
- ✅ **Multi-language support (Japanese/English/Bilingual)** ⭐ NEW!
- ✅ **Inherits language from use cases** ⭐ NEW!
- ✅ **Complete japanese_name support** ⭐ NEW!

---

## Language Support / 言語サポート ⭐

### Overview / 概要

This skill generates formal class diagrams with multi-language support, inheriting settings from use case specifications to maintain consistency across the workflow.

**Supported Languages:**
- **Japanese (日本語)**: Class diagrams and documentation in Japanese
- **English**: Class diagrams and documentation in English
- **Bilingual (バイリンガル)**: Dual-language output for international teams

### Language Inheritance

**Priority Order:**
1. **From usecase-output.json** (highest priority)
   - Reads existing `language_config` or `domain_model` settings
   - Ensures consistency with use case specifications
2. **Manual override** (if specified)
   - Can override via `language` parameter
3. **Auto-detection** (fallback)
   - Analyzes use case content if no configuration found

**Example inheritance:**
```json
// From activity-to-usecase-v1 output
{
  "domain_model": {
    "entities": [
      {
        "name": "Product",
        "japanese_name": "商品",
        "description": "販売する商品の情報"
      }
    ]
  }
}

// usecase-to-class-v1 preserves and formalizes this structure
```

### Language Configuration

**Parameters:**
```python
language_options = {
    "language": "auto",              # auto | ja | en | bilingual
    "inherit_from_usecases": True,   # Inherit from use case JSON (recommended)
    "entity_naming": "en",           # en (always English for code)
    "include_japanese_name": True,   # Always include japanese_name
    "class_diagram_lang": "auto",    # auto | ja | en (PlantUML comments)
    "documentation_lang": "auto",    # auto | ja | en (architecture-overview.md)
    "json_lang": "auto"              # auto | ja | en (descriptions in JSON)
}
```

### Output Language Control

**1. PlantUML Class Diagram:**
```plantuml
' language="ja"
class Product {
  - productId: String
  - name: String
  - price: Decimal
  --
  + getPrice(): Decimal
  + isAvailable(): Boolean
}

note right of Product
  **ビジネスルール:**
  - 商品価格は正の数である
  - 在庫数は0以上である
end note

' language="en"
class Product {
  - productId: String
  - name: String
  - price: Decimal
  --
  + getPrice(): Decimal
  + isAvailable(): Boolean
}

note right of Product
  **Business Rules:**
  - Product price must be positive
  - Stock quantity must be non-negative
end note

' language="bilingual"
class Product {
  - productId: String
  - name: String
  - price: Decimal
  --
  + getPrice(): Decimal
  + isAvailable(): Boolean
}

note right of Product
  **ビジネスルール / Business Rules:**
  - 商品価格は正の数である
    Product price must be positive
  - 在庫数は0以上である
    Stock quantity must be non-negative
end note
```

**2. Domain Model JSON:**
```json
// language="ja"
{
  "entities": [
    {
      "name": "Product",
      "japanese_name": "商品",
      "description": "販売する商品の情報",
      "attributes": [
        {
          "name": "productId",
          "japanese_name": "商品ID",
          "type": "string",
          "description": "商品の一意識別子"
        }
      ]
    }
  ]
}

// language="en"
{
  "entities": [
    {
      "name": "Product",
      "japanese_name": "Product",
      "description": "Information about products for sale",
      "attributes": [
        {
          "name": "productId",
          "japanese_name": "productId",
          "type": "string",
          "description": "Unique identifier for the product"
        }
      ]
    }
  ]
}

// language="bilingual"
{
  "entities": [
    {
      "name": "Product",
      "japanese_name": "商品",
      "description": "販売する商品の情報 / Information about products for sale",
      "attributes": [
        {
          "name": "productId",
          "japanese_name": "商品ID",
          "type": "string",
          "description": "商品の一意識別子 / Unique identifier for the product"
        }
      ]
    }
  ]
}
```

**3. Architecture Overview Document:**
```markdown
# language="ja"
# アーキテクチャ概要: 受注管理システム

## ドメインモデル / Domain Model

### エンティティ一覧

#### Product (商品)
販売する商品の情報を管理するエンティティ。

---

# language="en"
# Architecture Overview: Order Management System

## Domain Model / ドメインモデル

### Entity List

#### Product
Entity that manages information about products for sale.

---

# language="bilingual"
# アーキテクチャ概要 / Architecture Overview: 受注管理システム / Order Management System

## ドメインモデル / Domain Model

### エンティティ一覧 / Entity List

#### Product (商品)
販売する商品の情報を管理するエンティティ。
Entity that manages information about products for sale.
```

### Language Selection Guide

**Recommended settings:**
- **Always inherit**: Set `inherit_from_usecases=True` for consistency
- **Domestic projects**: Typically inherits `ja`
- **International projects**: Typically inherits `en`
- **Mixed teams**: Typically inherits `bilingual`

**Best practice:** Never override unless absolutely necessary - consistency is critical for the formal domain model.

---

## Position in Workflow / ワークフロー内の位置

```
Step 1: scenario-to-activity-v1
  Creates: Activity diagram + temporary model
  ↓
Step 2: activity-to-usecase-v1
  Creates: Use cases + inferred domain model
  ↓
Step 3: usecase-to-class-v1 ← YOU ARE HERE
  Creates: Formal class diagram (authoritative)
  ↓
Step 4: usecase-to-code-v1
  Uses: Formal class diagram for code generation
```

---

## Input / 入力

### Required

**Use case definition JSON:**
- `{project-name}_usecase-output.json`
- Contains: actors, use cases, inferred domain model

### Optional (Recommended)

**Original business scenario information:**
- Business overview
- Business rules
- Glossary
- Stakeholder information
- Non-functional requirements

**Why optional context matters:**
- Glossary provides official entity names
- Business rules define constraints
- Non-functional requirements suggest attributes

---

## Workflow / 処理フロー

### Step 0: Language Inheritance and Configuration ⭐ NEW!

**0a. Load use case JSON:**
```python
usecase_data = load_json(f"{project}_usecase-output.json")
```

**0b. Extract language configuration:**
```python
# Priority 1: Check for language_config (if added by activity-to-usecase-v1)
if "language_config" in usecase_data:
    lang_config = usecase_data["language_config"]
    language = lang_config["detected_language"]

# Priority 2: Infer from domain_model entities
elif "domain_model" in usecase_data and usecase_data["domain_model"]["entities"]:
    first_entity = usecase_data["domain_model"]["entities"][0]
    
    # Check if japanese_name differs from name
    if "japanese_name" in first_entity:
        if first_entity["japanese_name"] != first_entity["name"]:
            language = "ja"  # Has Japanese names
        else:
            language = "en"  # English only
    else:
        language = "en"  # No japanese_name field
    
    # Check description language
    if "description" in first_entity:
        lang = detect_language(first_entity["description"])
        if lang == "ja":
            language = "ja"

# Priority 3: Fallback
else:
    language = "en"  # Default to English
```

**0c. Apply language configuration:**
```python
lang_config = {
    "language": language,
    "entity_naming": "en",           # Always English
    "include_japanese_name": True,   # Always include
    "class_diagram_lang": language,
    "documentation_lang": language,
    "json_lang": language
}
```

**0d. Display language decision:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌐 Language Configuration (Inherited)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Source: usecase-output.json
Language: Japanese (日本語)
Entity names: English (for code)
Japanese names: Included
Class diagram: Japanese
Documentation: Japanese
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### Step 1: Gather All Information Sources

**1a. Load use case JSON:**
```json
{
  "actors": [...],
  "usecases": [...],
  "domain_model": {
    "source": "inferred",
    "entities": [...]
  }
}
```

**1b. Load original scenario (if available):**
- Business overview
- Glossary
- Business rules
- Stakeholder definitions

**1c. Identify information gaps:**
What's missing that needs to be added to class diagram?

---

### Step 2: Consolidate Actor Definitions

**2a. Extract actors from all sources:**

From use case JSON:
```json
"actors": [
  {"id": "customer", "name": "顧客"},
  {"id": "order_staff", "name": "受注係"}
]
```

From stakeholder information (if provided):
```
ステークホルダー情報:
- 顧客: 商品を注文する小売業者
- 受注係: 注文を受け付けるスタッフ
```

**2b. Create actor definitions:**
```plantuml
actor 顧客 <<actor>>
actor 受注係 <<actor>>
actor 出荷係 <<actor>>
actor システム <<actor>>
```

**2c. Add actor descriptions (from context):**
Use stakeholder descriptions or use case roles.

---

### Step 3: Consolidate Entity Definitions

**3a. Collect entities from all sources:**

From inferred domain model:
```json
"entities": [
  {"name": "受注", "attributes": [...]}
]
```

From use case flows:
```
"受注を登録する"
"在庫を確認する"
```

From glossary (if provided):
```
用語集:
- 受注: 顧客からの注文を受け付けること
- 出荷指示書: 出荷作業の指示を記載した文書
```

**3b. Deduplicate and merge:**
- Same entity from multiple sources → Merge definitions
- Conflicting definitions → Prefer glossary/official source
- Missing entities → Add from use case analysis

---

### Step 4: Define Complete Attributes

For each entity, define comprehensive attributes:

**4a. From inferred model:**
```
Entity: 受注
Inferred: 受注ID, 受注日時, ステータス
```

**4b. From use case requirements:**
```
Use Case: "商品を注文する"
Needs: 顧客ID, 合計金額, 備考
```

**4c. From business rules:**
```
ビジネスルール: "営業時間内のみ受注可能"
→ Add: 受注日時 (for validation)
```

**4d. Standard attributes:**
Add common attributes:
- ID fields (primary keys)
- Timestamps (createdAt, updatedAt)
- Status/state fields

**Result:**
```
class 受注 {
  - 受注ID: String
  - 受注日時: DateTime
  - 顧客ID: String
  - ステータス: 受注ステータス
  - 合計金額: Decimal
  - 備考: String
  - createdAt: DateTime
  - updatedAt: DateTime
  --
  + 登録する(): void
  + 確定する(): void
  + キャンセルする(): void
}
```

---

### Step 5: Define Relationships

**5a. From inferred relationships:**
```json
"relationships": [
  {"type": "has-many", "target": "受注明細"}
]
```

**5b. From use case flows:**
```
"注文に対して出荷を依頼する"
→ 受注 1 -- 0..1 出荷
```

**5c. From business logic:**
```
"商品ごとに在庫を管理"
→ 商品 1 -- 1 在庫
```

**Result:**
```plantuml
受注 "1" *-- "1..*" 受注明細 : 含む >
受注明細 "0..*" -- "1" 商品 : 対象 >
商品 "1" -- "1" 在庫 : 管理される >
受注 "1" -- "0..1" 出荷 : 出荷される >
```

---

### Step 6: Define Enumerations

**6a. From status fields:**
```
Entity: 受注
Attribute: ステータス
→ enum 受注ステータス {仮登録, 確定, 出荷済, キャンセル}
```

**6b. From business rules:**
```
"在庫状態は3種類: 在庫あり, 在庫不足, 発注中"
→ enum 在庫ステータス {在庫あり, 在庫不足, 発注中}
```

---

### Step 7: Add Business Methods

For each entity, add methods based on use cases:

**From use case actions:**
```
Use Case: "商品を注文する"
Actions: 登録する, 確定する, キャンセルする

→ class 受注 {
    + 登録する(): void
    + 確定する(): void
    + キャンセルする(): void
  }
```

**From business logic:**
```
"在庫引当処理"
→ class 在庫 {
    + 引当する(数量: Integer): Boolean
    + 更新する(増減量: Integer): void
  }
```

---

### Step 8: Add Constraints and Notes

**8a. Business rules as notes:**
```plantuml
note right of 受注
  事前条件: 営業時間内である
  事後条件: 受注が登録され在庫が引当られる
end note
```

**8b. Validation rules:**
```plantuml
note right of 在庫
  在庫確認時:
  - 在庫あり → 出荷可能
  - 在庫なし → 受注不可
end note
```

---

### Step 9: Generate Complete PlantUML Class Diagram

**Structure:**
```plantuml
@startuml {project}_class

' Actors
actor 顧客 <<actor>>
actor 受注係 <<actor>>
...

' Enumerations
enum 受注ステータス { ... }
enum 在庫ステータス { ... }

' Core Entities
class 受注 {
  - attributes
  --
  + methods
}

class 在庫 {
  ...
}

' Relationships
受注 "1" *-- "1..*" 受注明細
...

' Notes
note right of 受注
  Business rules
end note

@enduml
```

---

### Step 10: Validate Completeness

**10a. Check coverage:**
- ✓ All actors from use cases represented
- ✓ All entities from use cases included
- ✓ All relationships captured
- ✓ Business rules documented

**10b. Check consistency:**
- ✓ Entity names consistent with glossary
- ✓ Attribute types appropriate
- ✓ Relationships make sense

**10c. Check quality:**
- ✓ All entities have IDs
- ✓ Timestamps included
- ✓ Enums defined for status fields
- ✓ Methods align with use cases

---

## Output / 出力

### 1. PlantUML Class Diagram

**Filename:** `{project-name}_class.puml`

**Contents:**
- Complete PlantUML class diagram
- All actors with <<actor>> stereotype
- All entities with full attributes
- All relationships (associations, compositions, aggregations)
- Enumerations with all values
- Business methods for each entity
- Notes with business rules and constraints

**Quality markers:**
- Complete attribute definitions (no TBD)
- Proper relationship multiplicities
- Enumeration types for status fields
- Business logic methods included

---

### 2. Domain Model JSON (NEW!)

**Filename:** `{project}_domain-model.json`

Machine-readable, authoritative domain model specification.

**Schema:**
```json
{
  "metadata": {
    "source": "usecase-to-class-v1",
    "generated_at": "ISO 8601 timestamp",
    "version": "1.0",
    "status": "formal",
    "note": "This is the authoritative domain model for code generation."
  },
  "actors": [
    {
      "id": "string (snake_case)",
      "name": "string",
      "japanese_name": "string",
      "type": "primary|secondary|system",
      "description": "string",
      "responsibilities": ["string"]
    }
  ],
  "entities": [
    {
      "name": "string (PascalCase)",
      "japanese_name": "string",
      "description": "string",
      "stereotype": "entity|aggregate_root|value_object",
      "table_name": "string (snake_case)",
      "attributes": [
        {
          "name": "string (camelCase)",
          "japanese_name": "string",
          "type": "string|number|boolean|datetime|date|enum|decimal",
          "required": boolean,
          "primary_key": boolean,
          "unique": boolean,
          "indexed": boolean,
          "default": "any",
          "validation": {
            "min": number,
            "max": number,
            "pattern": "regex",
            "custom": "string"
          },
          "description": "string"
        }
      ],
      "relationships": [
        {
          "name": "string",
          "type": "belongs-to|has-one|has-many|many-to-many",
          "target": "string (target entity)",
          "source_multiplicity": "0..1|1|*|0..*",
          "target_multiplicity": "0..1|1|*|0..*",
          "foreign_key": "string",
          "inverse_of": "string",
          "description": "string"
        }
      ],
      "business_methods": [
        {
          "name": "string (camelCase)",
          "description": "string",
          "parameters": [
            {
              "name": "string",
              "type": "string",
              "required": boolean
            }
          ],
          "return_type": "string",
          "visibility": "public|private|protected",
          "validation_rules": ["string"],
          "side_effects": ["string"]
        }
      ],
      "invariants": [
        {
          "description": "string",
          "rule": "string"
        }
      ]
    }
  ],
  "enumerations": [
    {
      "name": "string",
      "description": "string",
      "values": [
        {
          "name": "string",
          "value": "string|number",
          "description": "string"
        }
      ]
    }
  ],
  "value_objects": [
    {
      "name": "string",
      "description": "string",
      "properties": [
        {
          "name": "string",
          "type": "string",
          "required": boolean
        }
      ],
      "validation": "string"
    }
  ],
  "aggregates": [
    {
      "root": "string (entity name)",
      "members": ["string (entity names)"],
      "description": "string"
    }
  ],
  "business_rules": [
    {
      "id": "string",
      "description": "string",
      "type": "constraint|validation|invariant|policy",
      "applies_to": ["entity names"],
      "rule_expression": "string"
    }
  ]
}
```

**Purpose:**
- Single source of truth for domain model
- Input for code generation
- Database schema generation
- API specification generation
- Type definition generation

---

### 3. Architecture Overview (NEW!)

**Filename:** `{project}_architecture-overview.md`

Comprehensive architecture documentation in Markdown format.

**Contents:**
```markdown
# アーキテクチャ概要: {System Name}

## 1. システム概要 / System Overview

### 目的
[システムが解決する課題と提供する価値]

### スコープ
[システムの境界と責任範囲]

### 主要機能
- [機能1]: [説明]
- [機能2]: [説明]

---

## 2. ドメインモデル / Domain Model

### 2.1 ドメインエンティティ

#### 受注 (Order) - Aggregate Root
**説明:** 顧客からの注文を表すエンティティ

**主要属性:**
- `orderId: String` - 受注ID (主キー)
- `customerId: String` - 顧客ID (外部キー)
- `orderDate: DateTime` - 受注日時
- `status: OrderStatus` - 受注ステータス
- `totalAmount: Decimal` - 合計金額

**リレーション:**
- Customer (多対1) - 1つの受注は1人の顧客に属する
- OrderItem (1対多) - 1つの受注は複数の明細を持つ
- Shipment (1対1) - 1つの受注は1つの出荷に対応

**ビジネスメソッド:**
- `confirm()` - 受注を確定する
- `cancel()` - 受注をキャンセルする
- `calculateTotal()` - 合計金額を計算する

**ビジネスルール:**
- 受注確定後は商品変更不可
- キャンセルは出荷前のみ可能
- 合計金額は明細の合計と一致する必要がある

[全エンティティについて同様に記載]

### 2.2 値オブジェクト

#### Address (住所)
**プロパティ:**
- postalCode: String
- prefecture: String
- city: String
- addressLine1: String
- addressLine2: String

**バリデーション:**
- 郵便番号は7桁の数字
- 都道府県は日本の47都道府県のいずれか

### 2.3 列挙型

#### OrderStatus (受注ステータス)
- `RECEIVED` - 受付済み
- `CONFIRMED` - 確定済み
- `SHIPPED` - 出荷済み
- `CANCELLED` - キャンセル済み

---

## 3. アーキテクチャパターン / Architecture Patterns

### 3.1 レイヤーアーキテクチャ

```
┌─────────────────────────────────┐
│   Presentation Layer            │  UI, API Endpoints
├─────────────────────────────────┤
│   Application Layer             │  Use Case Services
├─────────────────────────────────┤
│   Domain Layer                  │  Entities, Value Objects
├─────────────────────────────────┤
│   Infrastructure Layer          │  Database, External APIs
└─────────────────────────────────┘
```

### 3.2 Domain-Driven Design (DDD)

**Aggregates:**
- Order Aggregate
  - Root: Order
  - Members: OrderItem

**Repositories:**
- OrderRepository
- CustomerRepository
- ProductRepository

**Domain Services:**
- InventoryService
- ShippingService

---

## 4. データモデル / Data Model

### 4.1 エンティティ関係図 (ERD)

```
Customer ||--o{ Order : places
Order ||--|{ OrderItem : contains
Order ||--|| Shipment : has
Product ||--o{ OrderItem : included_in
Product ||--|| Inventory : has
```

### 4.2 主要テーブル

**orders**
- order_id (PK)
- customer_id (FK → customers)
- order_date
- status
- total_amount
- created_at
- updated_at

[全テーブルの定義]

---

## 5. ビジネスルールと制約 / Business Rules and Constraints

### 5.1 在庫管理ルール
- 在庫引当は受注確定時に実施
- 在庫不足時は受注不可
- 在庫数はリアルタイムで更新

### 5.2 受注処理ルール
- 営業時間外の受注は翌営業日処理
- 最小注文金額: 10,000円
- キャンセルは出荷前のみ可能

---

## 6. 非機能要件 / Non-Functional Requirements

### 6.1 性能要件
- 在庫確認: 1秒以内
- 注文登録: 3秒以内
- 同時接続数: 50ユーザー

### 6.2 セキュリティ要件
- 顧客情報の暗号化
- SSL/TLS通信
- ロールベースアクセス制御 (RBAC)

### 6.3 可用性要件
- システム稼働率: 99.9%
- データバックアップ: 1日1回
- 障害復旧時間: 1時間以内

---

## 7. 技術スタック / Technology Stack

### バックエンド
- 言語: TypeScript
- フレームワーク: Express
- ORM: Prisma
- データベース: PostgreSQL

### フロントエンド
- 言語: TypeScript
- フレームワーク: React
- UI: Tailwind CSS + shadcn/ui
- ビルドツール: Vite

---

## 8. デプロイメントアーキテクチャ / Deployment Architecture

### 開発環境
- Docker Compose
- ローカルPostgreSQL

### 本番環境
- Kubernetes
- Managed PostgreSQL
- CDN (静的ファイル)

---

## 9. 今後の拡張性 / Future Extensibility

### フェーズ2機能候補
- 複数配送先対応
- 定期注文機能
- 在庫自動発注

### スケーラビリティ考慮事項
- マイクロサービス化の可能性
- キャッシュレイヤーの追加
- 読み取り専用レプリカ

---

*生成日時: {timestamp}*
*生成ツール: usecase-to-class-v1*
*ドメインモデルバージョン: 1.0 (Formal)*
```

**Purpose:**
- Complete system documentation
- Onboarding for new developers
- Design decision record
- Stakeholder communication

---

### 4. XMI Model (NEW!)

**Filename:** `{project}_class-model.xmi`

UML 2.5.1 Class Diagram in standard XMI 2.5.1 format.

**Contents:**
- Complete class model
- All entities as classes
- All attributes with types
- All relationships with multiplicities
- Enumerations
- Business methods (operations)
- Constraints and invariants

**Compliance:**
- UML 2.5.1 specification (OMG)
- XMI 2.5.1 format
- Eclipse Modeling Framework compatible
- Supports round-trip engineering

**XMI Structure:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<xmi:XMI xmi:version="2.5.1" 
         xmlns:xmi="http://www.omg.org/spec/XMI/20131001"
         xmlns:uml="http://www.omg.org/spec/UML/20161101">
  <uml:Model xmi:type="uml:Model" name="{project}">
    <packagedElement xmi:type="uml:Package" name="DomainModel">
      
      <!-- Classes (Entities) -->
      <packagedElement xmi:type="uml:Class" name="Order">
        <ownedAttribute xmi:type="uml:Property" name="orderId" type="String"/>
        <ownedAttribute xmi:type="uml:Property" name="status" type="OrderStatus"/>
        <ownedOperation xmi:type="uml:Operation" name="confirm">
          <ownedParameter xmi:type="uml:Parameter" direction="return" type="void"/>
        </ownedOperation>
      </packagedElement>
      
      <!-- Associations -->
      <packagedElement xmi:type="uml:Association">
        <memberEnd xmi:idref="order_customer"/>
        <ownedEnd xmi:type="uml:Property" name="customer" type="Customer">
          <lowerValue xmi:type="uml:LiteralInteger" value="1"/>
          <upperValue xmi:type="uml:LiteralUnlimitedNatural" value="1"/>
        </ownedEnd>
      </packagedElement>
      
      <!-- Enumerations -->
      <packagedElement xmi:type="uml:Enumeration" name="OrderStatus">
        <ownedLiteral xmi:type="uml:EnumerationLiteral" name="RECEIVED"/>
        <ownedLiteral xmi:type="uml:EnumerationLiteral" name="CONFIRMED"/>
        <ownedLiteral xmi:type="uml:EnumerationLiteral" name="SHIPPED"/>
        <ownedLiteral xmi:type="uml:EnumerationLiteral" name="CANCELLED"/>
      </packagedElement>
      
    </packagedElement>
  </uml:Model>
</xmi:XMI>
```

**Purpose:**
- Standard UML tool interoperability
- Import into Enterprise Architect, MagicDraw, Papyrus
- Code generation with UML tools
- Model versioning and comparison

---

### 5. Summary Display (Console Output)

Display to user:
```
=== usecase-to-class-v1 完了 ===

✅ Generated Files:
1. {project}_class.puml (PlantUML)
2. {project}_domain-model.json (JSON)
3. {project}_architecture-overview.md (Markdown)
4. {project}_class-model.xmi (XMI)

=== Formal Class Diagram Generated ===

✅ Domain Model Source: FORMAL (production-ready)

Actors: 4
- 顧客, 受注係, 出荷係, システム

Entities: 7
- 受注, 受注明細, 商品, 在庫, 出荷, 出荷指示書, カタログ

Enumerations: 2
- 受注ステータス (4 values)
- 在庫ステータス (3 values)

Relationships: 12
- belongs-to: 5
- has-many: 4
- has-one: 3

Business Methods: 18

Aggregates: 2
- Order Aggregate (root: Order, members: OrderItem)
- Shipment Aggregate (root: Shipment)

This class diagram is now the authoritative domain model.
Next: Use usecase-to-code-v1 for code generation.
```

---

## Information Consolidation Strategy / 情報統合戦略

### Priority Order

When information conflicts, use this priority:

1. **Glossary** (highest) - Official terminology
2. **Business rules** - Explicit constraints
3. **Use case flows** - Functional requirements
4. **Inferred model** - Educated guesses
5. **Domain patterns** (lowest) - Generic conventions

### Example

```
Glossary says: "受注 = 顧客からの注文"
Inferred model says: "Order"
→ Use "受注" (glossary wins)

Business rule says: "ステータスは4種類"
Inferred model says: "status: string"
→ Use enum with 4 values (business rule wins)
```

---

## Entity Attribute Patterns / エンティティ属性パターン

### Mandatory Attributes (All Entities)

```
- [EntityName]ID: String (UUID)
- createdAt: DateTime
- updatedAt: DateTime
```

### Status-Bearing Entities

```
- status: EnumType
- statusChangedAt: DateTime
```

### Financial Entities

```
- amount: Decimal (never float!)
- currency: String (default: JPY)
```

### Temporal Entities

```
- validFrom: Date
- validTo: Date
```

---

## Relationship Patterns / リレーションシップパターン

### Composition (Strong)

```
受注 "1" *-- "1..*" 受注明細
(Order items cannot exist without Order)
```

### Aggregation (Weak)

```
カタログ "1" o-- "0..*" 商品
(Products can exist independently)
```

### Association

```
商品 "1" -- "1" 在庫
(Product has Inventory)
```

### Dependency

```
受注 ..> 在庫 : checks >
(Order checks Inventory)
```

---

## Best Practices / ベストプラクティス

### For Quality

1. **Use all available information**: Don't ignore glossary/business rules
2. **Be comprehensive**: Include all entities from use cases
3. **Define relationships clearly**: Specify cardinality
4. **Add business methods**: Not just data structure
5. **Document constraints**: Use notes for business rules

### For Maintainability

1. **Consistent naming**: Follow glossary terminology
2. **Clear types**: Use Decimal for money, DateTime for timestamps
3. **Enums for states**: Don't use string for status
4. **Meaningful methods**: Based on actual use cases

### For Code Generation

1. **Complete attributes**: Code generator needs all fields
2. **Proper types**: Enable type-safe code generation
3. **Full relationships**: Generate correct foreign keys
4. **Business logic**: Methods become service operations

---

## Common Pitfalls / よくある落とし穴

### ❌ Don't

- ❌ Ignore glossary in favor of inferred names
- ❌ Skip attributes because they seem "obvious"
- ❌ Use generic "status: string" instead of enums
- ❌ Omit relationships between entities
- ❌ Forget actor definitions

### ✅ Do

- ✅ Consolidate all information sources
- ✅ Define complete attribute sets
- ✅ Use strong types (enums, decimals)
- ✅ Specify relationship cardinality
- ✅ Include all actors with stereotypes

---

## Integration with Workflow / ワークフロー連携

**What feeds into this step:**
- Use case JSON (required)
- Original scenario (optional but recommended)

**What depends on this output:**
- usecase-to-code-v1 (critical dependency)
- All code generation quality depends on this class diagram

**Quality impact:**
- Good class diagram → High-quality code
- Incomplete class diagram → Missing functionality
- Wrong types → Runtime errors

---

## Version History / バージョン履歴

- **v1.0** (2026-01-22): Initial version
  - Consolidates use cases + original scenario
  - Creates formal, authoritative class diagram
  - Production-quality output
  - Designed for uml-workflow-v1
