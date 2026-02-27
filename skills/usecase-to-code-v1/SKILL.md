---
name: usecase-to-code-v1
description: Generate full-stack applications from use case definitions with customizable technology stacks and multi-language support (Japanese/English code comments). Supports multiple deployment architectures (monolith, microservices, serverless), frameworks (Express, NestJS, FastAPI, Spring Boot), and programming languages (TypeScript, Python, Java, Go). References domain model JSON (Single Source of Truth) for high-quality, type-safe code generation. Inherits language settings for code comments and documentation. Auto-generates full CRUD (Create, Read, Update, Delete) + List pages for ALL entities including master data management and system actor management.
---

# Use Case to Code Generator v1

Generate production-ready, full-stack applications from use case definitions with configurable technology stacks.

## Overview / 概要

This skill generates complete application code based on:
1. Use case definition JSON (from activity-to-usecase-v1)
2. Domain model JSON (from usecase-to-class-v1) - **Single Source of Truth**
3. User-specified technology stack

**Key improvements from original:**
- ✅ Technology stack selection
- ✅ Multiple architecture support
- ✅ Framework flexibility
- ✅ Uses domain-model.json (SSOT) with complete metadata
- ✅ **Multi-language code comments (Japanese/English)** ⭐ NEW!
- ✅ **Inherits language from domain model** ⭐ NEW!
- ✅ **Localized documentation (README, API docs)** ⭐ NEW!
- ✅ **Full CRUD + List for ALL entities (not just use-case-referenced)** ⭐ v1.1!
- ✅ **Entity classification (Master/Transaction/SubEntity/SystemActor)** ⭐ v1.1!
- ✅ **Shared UI components (DataTable, Pagination, SearchBar)** ⭐ v1.1!
- ✅ **Auto-generated sidebar navigation** ⭐ v1.1!

---


## Language Support / 言語サポート ⭐

This skill supports bilingual code generation (Japanese/English).

**Language Detection Priority**: metadata.language → entity descriptions → user request → default "ja"

**IMPORTANT**: Claude MUST read `templates/language-examples.md` for:
- Code comment language patterns (TypeScript/Python ja/en)
- README template patterns
- Language best practices

> ⚠️ Only read templates/language-examples.md when executing this step. Do NOT preload.

## Position in Workflow / ワークフロー内の位置

```
Step 1: scenario-to-activity-v1
  ↓
Step 2: activity-to-usecase-v1
  ↓
Step 3: usecase-to-class-v1
  ↓ Domain model JSON (REQUIRED - SSOT)
Step 4: usecase-to-code-v1 ← YOU ARE HERE
  ↓ Production code
```

---

## Input / 入力

### Required

**1. Use case definition JSON:**
- `{project-name}_usecase-output.json`
- Contains: actors, use cases, domain model reference

**2. Domain model JSON:**
- `{project-name}_domain-model.json`
- From usecase-to-class-v1
- **CRITICAL**: Authoritative domain model (Single Source of Truth)
- Contains: Complete entity definitions, attributes with full metadata, relationships, enumerations, business rules, validation rules, database-specific types

### Optional

**3. Technology stack specification:**
If not provided, interactive selection or defaults apply.

---

## Technology Stack Configuration / 技術スタック設定

### Configuration Format

Users can specify technology choices before code generation:

```yaml
architecture: monolith | microservices | serverless
backend:
  language: typescript | python | java | go | csharp
  framework: express | nestjs | fastapi | spring-boot | gin | aspnet
  database: postgresql | mysql | mongodb | dynamodb
  orm: prisma | typeorm | sqlalchemy | hibernate | gorm
frontend:
  framework: react | vue | angular | svelte
  language: typescript | javascript
  styling: tailwind | scss | styled-components
  build: vite | webpack | nextjs
deployment:
  platform: docker | kubernetes | aws-lambda | vercel | heroku
  infrastructure: terraform | cloudformation | manual
```

### Interactive Selection

If not specified, prompt user:

```
Claude: "Let's configure your technology stack.

Backend Language:
1. TypeScript (recommended for type safety)
2. Python (great for data/ML applications)
3. Java (enterprise-grade)
4. Go (high performance)

Select [1-4] or press Enter for default (1):"
```

Continue for each category.

### Presets

Provide common presets:

**Preset 1: Modern Full-Stack (Default)**
```yaml
architecture: monolith
backend:
  language: typescript
  framework: express
  database: postgresql
  orm: prisma
frontend:
  framework: react
  language: typescript
  styling: tailwind
  build: vite
```

**Preset 2: Python Web App**
```yaml
backend:
  language: python
  framework: fastapi
  database: postgresql
  orm: sqlalchemy
frontend:
  framework: react
  language: typescript
```

**Preset 3: Java Enterprise**
```yaml
backend:
  language: java
  framework: spring-boot
  database: postgresql
  orm: hibernate
frontend:
  framework: angular
  language: typescript
```

**Preset 4: Microservices**
```yaml
architecture: microservices
backend:
  language: typescript
  framework: nestjs
  database: postgresql
deployment:
  platform: kubernetes
```

**Preset 5: Serverless**
```yaml
architecture: serverless
backend:
  language: typescript
  framework: aws-lambda
  database: dynamodb
deployment:
  platform: aws-lambda
```

---

## Workflow / 処理フロー

### Step 0: Language Inheritance and Configuration ⭐ NEW!

**0a. Load domain model JSON:**
```python
domain_model = load_json(f"{project}_domain-model.json")
```

**0b. Extract language configuration:**
```python
# Priority 1: Check metadata.language
if "metadata" in domain_model and "language" in domain_model["metadata"]:
    language = domain_model["metadata"]["language"]

# Priority 2: Infer from entity descriptions
elif "entities" in domain_model and len(domain_model["entities"]) > 0:
    first_entity = domain_model["entities"][0]
    
    # Check description language
    if "description" in first_entity:
        language = detect_language(first_entity["description"])
    else:
        language = "en"
else:
    language = "en"  # Default

# Set code comment language
if language_options.code_comment_language == "auto":
    code_comment_lang = language
else:
    code_comment_lang = language_options.code_comment_language
```

**0c. Apply language configuration:**
```python
lang_config = {
    "code_comments": code_comment_lang,     # ja | en
    "jsdoc": code_comment_lang,             # Follow comments
    "readme": code_comment_lang,            # Follow comments
    "api_docs": code_comment_lang,          # Follow comments
    "error_messages": "en",                 # Always English
    "console_logs": code_comment_lang       # Follow comments
}
```

**0d. Load japanese_name mappings:**
```python
# Extract japanese_name for all entities and attributes
japanese_names = {}
for entity in domain_model["entities"]:
    entity_name = entity["name"]
    japanese_names[entity_name] = entity.get("japanese_name", entity_name)
    
    for attr in entity.get("attributes", []):
        attr_key = f"{entity_name}.{attr['name']}"
        japanese_names[attr_key] = attr.get("japanese_name", attr["name"])
```

**0e. Display language decision:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌐 Code Generation Language Config
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Source: domain-model.json
Code comments: Japanese (日本語)
JSDoc/docstrings: Japanese
README.md: Japanese
API documentation: Japanese
Error messages: English (recommended)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### Step 1: Load and Validate Inputs

**1a. Load use case JSON:**
```json
{
  "metadata": {...},
  "usecases": [...],
  "domain_model": {...}
}
```

**1b. Load domain model JSON:**
```bash
Check: {project}_domain-model.json exists
Load: Complete domain model with all metadata
```

**Expected structure:**
```json
{
  "metadata": {
    "source": "usecase-to-class-v1",
    "status": "formal"
  },
  "entities": [
    {
      "name": "Order",
      "attributes": [
        {
          "name": "totalAmount",
          "type": "Decimal",
          "db_type": "Decimal(10, 2)",
          "validation": {"min": 1},
          "is_required": true
        }
      ],
      "business_methods": [...],
      "business_rules": [...]
    }
  ],
  "enumerations": [...],
  "relationships": [...],
  "aggregates": [...],
  "repositories": [...]
}
```

**1c. Validate consistency:**
- ✓ All use case entities exist in domain model
- ✓ Relationships are defined with cardinality
- ✓ Attributes have complete type information (type + db_type)
- ✓ Validation rules are specified
- ✓ Enumerations are defined for status fields

**If domain model missing:**
```
❌ ERROR: Domain model not found.
usecase-to-code-v1 requires domain-model.json from usecase-to-class-v1.
Cannot proceed without it.

Please run: usecase-to-class-v1 first.
```

---

### Step 2: Configure Technology Stack

> ⚠️ **CRITICAL — 呼び出し元の判定（Case A / Case B）**
>
> このスキルは2つの方法で呼び出される。**重複質問は厳禁**。
>
> **Case A: uml-workflow-v3 の Step 8 から呼び出された場合**
> - テックスタックは Phase 1 のユーザー対話で既に収集済み
> - `backend_framework`, `frontend_framework`, `architecture` の値が渡されている
> - **ここで再度ユーザーに質問してはならない（バグになる）**
> - Step 2b〜2d をスキップし、渡された値をそのまま使用する
>
> 判定基準（いずれかを満たせば Case A）:
> - 呼び出しコンテキストに `backend_framework`, `frontend_framework`, `architecture` が含まれる
> - `security-config.json` が `domain-model.json` と一緒に参照されている
> - プロンプト文脈に `uml-workflow-v3` または `Step 8` の記述がある
>
> **Case B: 単体で直接呼び出された場合**
> - `ask_user_input_v0` ツールで以下を質問する（workflow Phase 1 と同じ質問セット）:
>   1. バックエンドフレームワーク: Express(TypeScript) / NestJS / FastAPI / Spring Boot
>   2. フロントエンド: React(TypeScript) / Vue 3 / 生成しない
>   3. アーキテクチャ: Monolith / Microservices / Serverless
>   4. テストコードを生成するか: はい / いいえ
> - 確認プロンプト「コード生成を開始しますか？（yes/no）」を表示する

**2a. Check for user specification (Case B のみ):**
Did user provide tech stack configuration?

**2b. If not specified (Case B のみ):**
- Show interactive selection menu
- OR apply default preset
- OR ask user to choose preset

**2c. Validate compatibility:**
```
Check:
- Framework matches language
- ORM compatible with database
- Build tool matches frontend framework
```

**2d. Display selected stack (Case B のみ):**
```
=== Technology Stack ===
Architecture: Monolith
Backend: TypeScript + Express + Prisma + PostgreSQL
Frontend: React + TypeScript + Tailwind + Vite
Deployment: Docker

Proceed with code generation? (yes/no)
```

---

### Step 3: Generate Project Structure

> ⚠️ **bash brace expansion に関する重要な注意**
>
> bash_tool で `mkdir -p path/{a,b,c}` を実行すると、シェル環境によっては `{a,b,c}` という**リテラル名**のディレクトリが1つ作成され、`a`, `b`, `c` の3ディレクトリが作成されない場合がある。
>
> **必ず個別に `mkdir` を呼び出すこと:**
> ```bash
> # ❌ 危険（環境依存）
> mkdir -p /home/claude/project/src/{components,pages,api}
>
> # ✅ 安全（必ずこちらを使う）
> mkdir -p /home/claude/project/src/components
> mkdir -p /home/claude/project/src/pages
> mkdir -p /home/claude/project/src/api
> ```
> または `create_file` ツールでファイルを直接作成すると、必要なディレクトリも自動作成される。

**3a. Create directory structure based on architecture:**

**Monolith:**
```
{project}/
├── backend/
├── frontend/
└── docker-compose.yml
```

**Microservices:**
```
{project}/
├── services/
│   ├── order-service/
│   ├── inventory-service/
│   └── shipping-service/
├── frontend/
└── kubernetes/
```

**Serverless:**
```
{project}/
├── functions/
│   ├── create-order/
│   ├── get-inventory/
│   └── create-shipment/
├── frontend/
└── infrastructure/
```

**3b. Initialize build configurations:**
- package.json / requirements.txt / pom.xml
- tsconfig.json / pyproject.toml / etc.
- Docker files
- CI/CD configs

---

### Step 4: Generate Database Schema

**4a. Load entities from domain-model.json:**
```json
{
  "entities": [
    {
      "name": "Order",
      "table_name": "orders",
      "attributes": [
        {
          "name": "orderId",
          "type": "String",
          "db_type": "VARCHAR(36)",
          "is_primary_key": true,
          "default_value": "UUID.generate()"
        },
        {
          "name": "orderDate",
          "type": "DateTime",
          "db_type": "TIMESTAMP",
          "is_required": true,
          "default_value": "now()"
        },
        {
          "name": "totalAmount",
          "type": "Decimal",
          "db_type": "Decimal(10, 2)",
          "validation": {"min": 1}
        },
        {
          "name": "status",
          "type": "OrderStatus",
          "is_required": true,
          "default_value": "PENDING"
        }
      ]
    }
  ],
  "enumerations": [
    {
      "name": "OrderStatus",
      "values": [
        {"name": "PENDING"},
        {"name": "CONFIRMED"},
        {"name": "SHIPPED"},
        {"name": "CANCELLED"}
      ]
    }
  ]
}
```

**4b. Generate schema for selected ORM:**

**Prisma (TypeScript):**
```prisma
model Order {
  id          String      @id @default(uuid())
  orderDate   DateTime    @default(now())
  customerId  String
  status      OrderStatus @default(PENDING)
  totalAmount Decimal     @db.Decimal(10, 2)
  
  customer    Customer    @relation(fields: [customerId], references: [id])
  orderItems  OrderItem[]
  
  @@map("orders")
}

enum OrderStatus {
  PENDING
  CONFIRMED
  SHIPPED
  CANCELLED
}
```

**SQLAlchemy (Python):**
```python
class Order(Base):
    __tablename__ = "orders"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    order_date = Column(DateTime, default=datetime.now)
    customer_id = Column(String, ForeignKey("customers.id"))
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    total_amount = Column(Numeric(10, 2))
    
    customer = relationship("Customer", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")
```

**Hibernate (Java):**
```java
@Entity
@Table(name = "orders")
public class Order {
    @Id
    @GeneratedValue(generator = "uuid")
    private String id;
    
    @Column(name = "order_date")
    private LocalDateTime orderDate;
    
    @Column(name = "customer_id")
    private String customerId;
    
    @Enumerated(EnumType.STRING)
    private OrderStatus status;
    
    @Column(precision = 10, scale = 2)
    private BigDecimal totalAmount;
    
    @ManyToOne
    @JoinColumn(name = "customer_id", insertable = false, updatable = false)
    private Customer customer;
    
    @OneToMany(mappedBy = "order")
    private List<OrderItem> orderItems;
}
```

---

### Step 5: Generate Domain Entities

**5a. Extract business methods from domain-model.json:**
```json
{
  "entities": [
    {
      "name": "Order",
      "business_methods": [
        {
          "name": "create",
          "parameters": [
            {"name": "customerId", "type": "String"},
            {"name": "items", "type": "OrderItem[]"}
          ],
          "return_type": "Order",
          "preconditions": ["顧客IDが有効である", "商品在庫がある"],
          "postconditions": ["注文が登録されている", "在庫が引当られている"]
        },
        {
          "name": "confirm",
          "return_type": "void",
          "preconditions": ["status == PENDING"],
          "postconditions": ["status == CONFIRMED"]
        },
        {
          "name": "cancel",
          "return_type": "void",
          "preconditions": ["status != SHIPPED"],
          "postconditions": ["status == CANCELLED"]
        }
      ],
      "business_rules": [
        "最小注文金額は1円以上",
        "出荷後はキャンセル不可"
      ]
    }
  ]
}
```

**5b. Generate domain entity code:**

**TypeScript:**
```typescript
export class OrderEntity {
  constructor(
    public id: string,
    public orderDate: Date,
    public customerId: string,
    public status: OrderStatus,
    public totalAmount: number
  ) {}
  
  static create(customerId: string, items: OrderItem[]): OrderEntity {
    // Business logic from use case
    // Precondition: 顧客IDが有効である
    // Precondition: 商品在庫がある
    
    const order = new OrderEntity(
      uuidv4(),
      new Date(),
      customerId,
      OrderStatus.PENDING,
      items.reduce((sum, item) => sum + item.total, 0)
    );
    
    // Postcondition: 注文が登録されている
    // Postcondition: 在庫が引当られている
    
    return order;
  }
  
  confirm(): void {
    // Business rule from domain-model.json
    if (this.status !== OrderStatus.PENDING) {
      throw new ValidationError('仮登録状態の受注のみ確定できます');
    }
    this.status = OrderStatus.CONFIRMED;
  }
  
  cancel(): void {
    // Business rule from domain-model.json
    if (this.status === OrderStatus.SHIPPED) {
      throw new ValidationError('出荷済みの受注はキャンセルできません');
    }
    this.status = OrderStatus.CANCELLED;
  }
}
```

**Python:**
```python
class OrderEntity:
    def __init__(self, id: str, order_date: datetime, customer_id: str,
                 status: OrderStatus, total_amount: Decimal):
        self.id = id
        self.order_date = order_date
        self.customer_id = customer_id
        self.status = status
        self.total_amount = total_amount
    
    @staticmethod
    def create(customer_id: str, items: List[OrderItem]) -> 'OrderEntity':
        # Business logic
        pass
    
    def confirm(self) -> None:
        if self.status != OrderStatus.TENTATIVE:
            raise ValidationError('仮登録状態の受注のみ確定できます')
        self.status = OrderStatus.CONFIRMED
```

---

### Step 5.5: Entity CRUD Classification ⭐ NEW!

**CRITICAL RULE: Every entity in domain-model.json MUST have complete CRUD (Create, Read, Update, Delete) + List operations generated, regardless of whether explicit use cases exist for those operations.**

This step classifies each entity and determines what to generate.

**5.5a. Classify entities by role:**

For each entity in domain-model.json, classify as one of:

| Classification | Criteria | CRUD Level |
|---------------|----------|------------|
| **Master Data** | Entities representing people, organizations, products, categories, settings (e.g., Customer, ShippingStaff, Product, Category) | Full CRUD + List + Search |
| **Transaction Data** | Entities representing business events/processes (e.g., Order, Shipment, Payment) | Full CRUD + List + Search + Status filter |
| **Sub-entity / Detail** | Entities that only exist as children of another entity (e.g., OrderItem, ShipmentDetail) | Nested CRUD within parent |
| **System Actor** | Entities representing system users/operators (e.g., ShippingStaff, OrderClerk, Admin) | Full CRUD + List + Role management |

**Classification heuristics:**
```python
def classify_entity(entity, relationships):
    name = entity["name"]
    
    # System Actor: has role/permission attributes or is referenced as an actor
    if has_role_attributes(entity) or is_actor_in_usecases(name):
        return "SYSTEM_ACTOR"
    
    # Sub-entity: only exists as composition child (1..* from parent)
    if is_composition_child_only(name, relationships):
        return "SUB_ENTITY"
    
    # Transaction: has status/date attributes and lifecycle
    if has_status_attribute(entity) and has_date_attributes(entity):
        return "TRANSACTION"
    
    # Default: Master Data
    return "MASTER_DATA"
```

**5.5b. Determine CRUD operations per entity:**

| Operation | Master Data | Transaction | Sub-entity | System Actor |
|-----------|------------|-------------|------------|--------------|
| **Create** | ✅ Form | ✅ Form (from use case) | ✅ Inline in parent | ✅ Form |
| **Read (Detail)** | ✅ Detail page | ✅ Detail page | ✅ Within parent detail | ✅ Detail page |
| **Update** | ✅ Edit form | ✅ Edit form | ✅ Inline edit | ✅ Edit form |
| **Delete** | ✅ Soft delete | ⚠️ Cancel/void only | ✅ Remove from parent | ✅ Deactivate |
| **List** | ✅ Table + pagination | ✅ Table + status filter | ❌ (shown in parent) | ✅ Table + pagination |
| **Search** | ✅ Name/keyword | ✅ Date range + status | ❌ | ✅ Name/role |

**5.5c. Generate CRUD specification:**

```json
{
  "crud_spec": [
    {
      "entity": "Customer",
      "classification": "MASTER_DATA",
      "operations": {
        "create": { "fields": ["name", "email", "phone", "address"], "validation": true },
        "read": { "detail_page": true, "include_relations": ["orders"] },
        "update": { "editable_fields": ["name", "email", "phone", "address"] },
        "delete": { "type": "soft_delete", "field": "isActive" },
        "list": { "columns": ["name", "email", "phone", "createdAt"], "searchable": ["name", "email"], "sortable": true, "pagination": true },
        "search": { "fields": ["name", "email"] }
      }
    },
    {
      "entity": "ShippingStaff",
      "classification": "SYSTEM_ACTOR",
      "operations": {
        "create": { "fields": ["name", "email", "role"], "validation": true },
        "read": { "detail_page": true },
        "update": { "editable_fields": ["name", "email", "role", "isActive"] },
        "delete": { "type": "deactivate", "field": "isActive" },
        "list": { "columns": ["name", "email", "role", "isActive"], "searchable": ["name"], "sortable": true, "pagination": true },
        "search": { "fields": ["name"] }
      }
    },
    {
      "entity": "Order",
      "classification": "TRANSACTION",
      "operations": {
        "create": { "from_usecase": "UC-001", "fields": "from_usecase" },
        "read": { "detail_page": true, "include_relations": ["orderItems", "customer"] },
        "update": { "from_usecase": true },
        "delete": { "type": "cancel", "business_rule": "出荷後はキャンセル不可" },
        "list": { "columns": ["orderId", "customer.name", "orderDate", "status", "totalAmount"], "filterable": ["status", "orderDate"], "sortable": true, "pagination": true },
        "search": { "fields": ["orderId", "customer.name"], "date_range": "orderDate" }
      }
    }
  ]
}
```

**5.5d. Display classification result:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Entity CRUD Classification
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Entity            │ Classification  │ CRUD Level
──────────────────┼────────────────┼───────────
Customer          │ MASTER_DATA    │ Full CRUD + List + Search
ShippingStaff     │ SYSTEM_ACTOR   │ Full CRUD + List + Role Mgmt
Product           │ MASTER_DATA    │ Full CRUD + List + Search
Order             │ TRANSACTION    │ Full CRUD + List + Status Filter
OrderItem         │ SUB_ENTITY     │ Nested in Order
Shipment          │ TRANSACTION    │ Full CRUD + List + Status Filter
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### Step 6: Generate Services

**6a. Map use cases to services:**
```
Use Case: "商品を注文する"
→ Service: OrderService.createOrder()

Use Case: "商品を出荷する"
→ Service: ShipmentService.createShipment()
```

**6b. Generate CRUD services for ALL entities:** ⭐ NEW!

**CRITICAL: For every entity classified in Step 5.5, generate a complete CRUD service with findAll, findById, create, update, delete methods, even if no explicit use case exists.**

**TypeScript + Express (Generic CRUD Service):**
```typescript
// Base CRUD service pattern - generated for EVERY entity
export class CustomerService {
  constructor(private prisma: PrismaClient) {}

  // 一覧取得（ページネーション + 検索）
  async findAll(params: {
    page?: number;
    limit?: number;
    search?: string;
    sortBy?: string;
    sortOrder?: 'asc' | 'desc';
  }): Promise<PaginatedResult<Customer>> {
    const { page = 1, limit = 20, search, sortBy = 'createdAt', sortOrder = 'desc' } = params;
    const where = search ? {
      OR: [
        { name: { contains: search, mode: 'insensitive' } },
        { email: { contains: search, mode: 'insensitive' } },
      ]
    } : {};

    const [data, total] = await Promise.all([
      this.prisma.customer.findMany({
        where,
        skip: (page - 1) * limit,
        take: limit,
        orderBy: { [sortBy]: sortOrder },
      }),
      this.prisma.customer.count({ where }),
    ]);

    return { data, pagination: { page, limit, total, totalPages: Math.ceil(total / limit) } };
  }

  // 詳細取得（関連エンティティ含む）
  async findById(id: string): Promise<Customer | null> {
    return this.prisma.customer.findUnique({
      where: { id },
      include: { orders: { take: 10, orderBy: { createdAt: 'desc' } } },
    });
  }

  // 新規作成
  async create(dto: CreateCustomerDTO): Promise<Customer> {
    return this.prisma.customer.create({ data: dto });
  }

  // 更新
  async update(id: string, dto: UpdateCustomerDTO): Promise<Customer> {
    return this.prisma.customer.update({ where: { id }, data: dto });
  }

  // 削除（ソフトデリート）
  async delete(id: string): Promise<Customer> {
    return this.prisma.customer.update({
      where: { id },
      data: { isActive: false },
    });
  }
}
```

**System Actor service pattern (e.g., ShippingStaff):**
```typescript
export class ShippingStaffService {
  constructor(private prisma: PrismaClient) {}

  async findAll(params: PaginationParams): Promise<PaginatedResult<ShippingStaff>> {
    // Same pattern as Master Data but with role filtering
  }

  async findById(id: string): Promise<ShippingStaff | null> { ... }
  async create(dto: CreateShippingStaffDTO): Promise<ShippingStaff> { ... }
  async update(id: string, dto: UpdateShippingStaffDTO): Promise<ShippingStaff> { ... }
  async deactivate(id: string): Promise<ShippingStaff> {
    return this.prisma.shippingStaff.update({
      where: { id },
      data: { isActive: false },
    });
  }
}
```

**6c. Generate use-case-specific service methods (existing behavior):**

**TypeScript + Express:**
```typescript
export class OrderService {
  constructor(private prisma: PrismaClient) {}
  
  async createOrder(dto: CreateOrderDTO): Promise<OrderWithItems> {
    // Implementation from use case main flow
    return await this.prisma.$transaction(async (tx) => {
      // Step 1: Validate products
      // Step 2: Check inventory
      // Step 3: Create order
      // Step 4: Create order items
    });
  }
  
  async confirmOrder(orderId: string): Promise<Order> {
    // Implementation from use case extension
  }
}
```

**Python + FastAPI:**
```python
class OrderService:
    def __init__(self, db: Session):
        self.db = db
    
    async def create_order(self, dto: CreateOrderDTO) -> OrderWithItems:
        # Implementation
        pass
```

---

### Step 7: Generate API Routes

**7a. Generate CRUD API endpoints for ALL entities:** ⭐ NEW!

**CRITICAL: For every entity classified in Step 5.5, generate standard RESTful CRUD endpoints.**

**Standard CRUD endpoints per entity:**

| Entity Type | Endpoints Generated |
|------------|-------------------|
| Master Data | `GET /api/{entities}` (list+search), `GET /api/{entities}/:id` (detail), `POST /api/{entities}` (create), `PUT /api/{entities}/:id` (update), `DELETE /api/{entities}/:id` (soft-delete) |
| Transaction | Same as above + `PATCH /api/{entities}/:id/status` (status change) |
| System Actor | Same as Master Data + `PATCH /api/{entities}/:id/activate` / `deactivate` |
| Sub-entity | Nested: `GET /api/{parents}/:parentId/{entities}`, `POST /api/{parents}/:parentId/{entities}` etc. |

**Express (TypeScript) — auto-generated for every entity:**
```typescript
// Auto-generated: Customer CRUD routes
const customerRouter = Router();

// 一覧取得（検索・ページネーション対応）
customerRouter.get('/', async (req: Request, res: Response) => {
  const { page, limit, search, sortBy, sortOrder } = req.query;
  const result = await customerService.findAll({ page: Number(page), limit: Number(limit), search: String(search || ''), sortBy: String(sortBy || 'createdAt'), sortOrder: (sortOrder as 'asc' | 'desc') || 'desc' });
  res.json({ success: true, ...result });
});

// 詳細取得
customerRouter.get('/:id', async (req: Request, res: Response) => {
  const customer = await customerService.findById(req.params.id);
  if (!customer) return res.status(404).json({ success: false, error: 'Not found' });
  res.json({ success: true, data: customer });
});

// 新規作成
customerRouter.post('/', validateBody(CreateCustomerDTO), async (req: Request, res: Response) => {
  const customer = await customerService.create(req.body);
  res.status(201).json({ success: true, data: customer });
});

// 更新
customerRouter.put('/:id', validateBody(UpdateCustomerDTO), async (req: Request, res: Response) => {
  const customer = await customerService.update(req.params.id, req.body);
  res.json({ success: true, data: customer });
});

// 削除（ソフトデリート）
customerRouter.delete('/:id', async (req: Request, res: Response) => {
  await customerService.delete(req.params.id);
  res.json({ success: true });
});

// Router registration
app.use('/api/customers', customerRouter);
app.use('/api/shipping-staffs', shippingStaffRouter);  // System Actors too!
app.use('/api/products', productRouter);
app.use('/api/orders', orderRouter);
app.use('/api/shipments', shipmentRouter);
```

**7b. Extract additional API endpoints from use case JSON (existing behavior):**
```json
"api_endpoints": [
  {
    "method": "POST",
    "path": "/api/orders",
    "description": "新規受注を作成"
  }
]
```

**7b. Generate route handlers:**

**Express (TypeScript):**
```typescript
router.post('/orders', async (req: Request, res: Response) => {
  try {
    const order = await orderService.createOrder(req.body);
    res.status(201).json({ success: true, data: order });
  } catch (error) {
    // Error handling
  }
});
```

**FastAPI (Python):**
```python
@router.post("/orders", response_model=OrderResponse)
async def create_order(dto: CreateOrderDTO, db: Session = Depends(get_db)):
    service = OrderService(db)
    return await service.create_order(dto)
```

**Spring Boot (Java):**
```java
@PostMapping("/orders")
public ResponseEntity<OrderResponse> createOrder(@RequestBody CreateOrderDTO dto) {
    Order order = orderService.createOrder(dto);
    return ResponseEntity.status(HttpStatus.CREATED).body(order);
}
```

---

### Step 8: Generate Frontend Code

**8a. Generate API client with CRUD methods for ALL entities:** ⭐ ENHANCED!

**CRITICAL: Generate API client methods for every entity, not just those with explicit use cases.**

**⚠️ 型定義とAPIクライアントの必須ルール（SYSTEM_ACTOR / MASTER_DATA）:**

```
以下を必ず守ること:

1. types/index.ts
   - SYSTEM_ACTOR / MASTER_DATA の全エンティティを interface として定義すること
   - AdminPage.tsx 等のページコンポーネントにローカルで型定義してはならない（FORBIDDEN）
   - 登録・更新のリクエスト型（CreateXxxRequest / UpdateXxxRequest）も types/index.ts に定義すること
   - SYSTEM_ACTOR はパスワードフィールドを型から除外すること（APIが返さないため）

2. api/client.ts
   - SYSTEM_ACTOR / MASTER_DATA の全エンティティについて以下の関数を必ず生成すること:
     * fetchXxxList()   — 一覧取得（GET /api/{entities}）
     * fetchXxx(id)     — 詳細取得（GET /api/{entities}/:id）
     * createXxx(data)  — 新規登録（POST /api/{entities}）
     * updateXxx(id, data) — 更新（PUT /api/{entities}/:id）
     * deactivateXxx(id)   — 論理削除（DELETE /api/{entities}/:id）
     * changeXxxPassword(id, password) — パスワード変更（SYSTEM_ACTORのみ）
   - ページコンポーネント内でfetch()を直接呼んではならない（FORBIDDEN）
   - 全てのAPI呼び出しは api/client.ts 経由であること

3. ページコンポーネント（AdminPage.tsx 等）
   - 型は types から import すること
   - API呼び出しは api/client.ts から import すること
   - ローカル型定義（interface / type）やローカルfetch関数は作成してはならない（FORBIDDEN）
```

**TypeScript:**
```typescript
export class ApiClient {
  private baseUrl = '/api';

  // === Auto-generated for EVERY entity ===

  // Customer CRUD
  async getCustomers(params?: ListParams): Promise<PaginatedResult<Customer>> {
    return this.get('/customers', params);
  }
  async getCustomer(id: string): Promise<Customer> {
    return this.get(`/customers/${id}`);
  }
  async createCustomer(dto: CreateCustomerDTO): Promise<Customer> {
    return this.post('/customers', dto);
  }
  async updateCustomer(id: string, dto: UpdateCustomerDTO): Promise<Customer> {
    return this.put(`/customers/${id}`, dto);
  }
  async deleteCustomer(id: string): Promise<void> {
    return this.delete(`/customers/${id}`);
  }

  // ShippingStaff CRUD (System Actor — also gets full CRUD!)
  async getShippingStaffs(params?: ListParams): Promise<PaginatedResult<ShippingStaff>> {
    return this.get('/shipping-staffs', params);
  }
  async getShippingStaff(id: string): Promise<ShippingStaff> {
    return this.get(`/shipping-staffs/${id}`);
  }
  async createShippingStaff(dto: CreateShippingStaffDTO): Promise<ShippingStaff> {
    return this.post('/shipping-staffs', dto);
  }
  async updateShippingStaff(id: string, dto: UpdateShippingStaffDTO): Promise<ShippingStaff> {
    return this.put(`/shipping-staffs/${id}`, dto);
  }

  // ... (repeat for ALL entities: Product, Order, Shipment, etc.)

  // === Use-case-specific methods (from use case JSON) ===
  async createOrder(dto: CreateOrderDTO): Promise<Order> {
    return this.post('/orders', dto);
  }
}
```

**8b. Generate CRUD pages for ALL entities:** ⭐ NEW!

**CRITICAL: For every entity (except sub-entities), generate these 3 page types:**

| Page Type | Purpose | Route |
|-----------|---------|-------|
| **List Page** | Table with search, sort, pagination | `/{entities}` |
| **Detail Page** | Read-only view with related data | `/{entities}/:id` |
| **Form Page** | Create/Edit form with validation | `/{entities}/new`, `/{entities}/:id/edit` |

**React — List Page (auto-generated for every entity):**
```tsx
// pages/customers/CustomerListPage.tsx
export const CustomerListPage: React.FC = () => {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [pagination, setPagination] = useState<Pagination>({ page: 1, limit: 20, total: 0 });
  const [search, setSearch] = useState('');
  const [sortBy, setSortBy] = useState('createdAt');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');

  useEffect(() => {
    loadData();
  }, [pagination.page, search, sortBy, sortOrder]);

  const loadData = async () => {
    const result = await apiClient.getCustomers({
      page: pagination.page, limit: pagination.limit,
      search, sortBy, sortOrder,
    });
    setCustomers(result.data);
    setPagination(result.pagination);
  };

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">顧客一覧</h1>
        <Link to="/customers/new">
          <Button>新規登録</Button>
        </Link>
      </div>

      {/* 検索バー */}
      <SearchBar value={search} onChange={setSearch} placeholder="名前・メールで検索" />

      {/* テーブル */}
      <DataTable
        columns={[
          { key: 'name', label: '顧客名', sortable: true },
          { key: 'email', label: 'メール', sortable: true },
          { key: 'phone', label: '電話番号' },
          { key: 'createdAt', label: '登録日', sortable: true, format: 'date' },
        ]}
        data={customers}
        sortBy={sortBy}
        sortOrder={sortOrder}
        onSort={(key) => { setSortBy(key); setSortOrder(prev => prev === 'asc' ? 'desc' : 'asc'); }}
        onRowClick={(row) => navigate(`/customers/${row.id}`)}
        actions={(row) => (
          <>
            <Link to={`/customers/${row.id}/edit`}><EditIcon /></Link>
            <DeleteButton onConfirm={() => handleDelete(row.id)} />
          </>
        )}
      />

      {/* ページネーション */}
      <Pagination pagination={pagination} onChange={(page) => setPagination({ ...pagination, page })} />
    </div>
  );
};
```

**React — Detail Page (auto-generated):**
```tsx
// pages/customers/CustomerDetailPage.tsx
export const CustomerDetailPage: React.FC = () => {
  const { id } = useParams();
  const [customer, setCustomer] = useState<Customer | null>(null);

  useEffect(() => {
    apiClient.getCustomer(id!).then(setCustomer);
  }, [id]);

  if (!customer) return <Loading />;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">{customer.name}</h1>

      {/* 基本情報 */}
      <DetailSection title="基本情報">
        <DetailField label="顧客名" value={customer.name} />
        <DetailField label="メール" value={customer.email} />
        <DetailField label="電話番号" value={customer.phone} />
        <DetailField label="住所" value={customer.address} />
        <DetailField label="登録日" value={formatDate(customer.createdAt)} />
      </DetailSection>

      {/* 関連: 注文履歴（関連エンティティ） */}
      <DetailSection title="注文履歴">
        <DataTable
          columns={[
            { key: 'orderId', label: '注文ID' },
            { key: 'orderDate', label: '注文日', format: 'date' },
            { key: 'status', label: 'ステータス', format: 'badge' },
            { key: 'totalAmount', label: '合計金額', format: 'currency' },
          ]}
          data={customer.orders || []}
          onRowClick={(row) => navigate(`/orders/${row.id}`)}
        />
      </DetailSection>

      <div className="flex gap-2 mt-6">
        <Link to={`/customers/${id}/edit`}><Button>編集</Button></Link>
        <Button variant="outline" onClick={() => navigate('/customers')}>戻る</Button>
      </div>
    </div>
  );
};
```

**React — Form Page (auto-generated for create AND edit):**
```tsx
// pages/customers/CustomerFormPage.tsx
export const CustomerFormPage: React.FC = () => {
  const { id } = useParams(); // undefined for create, present for edit
  const isEdit = !!id;
  const [form, setForm] = useState<CustomerFormData>({ name: '', email: '', phone: '', address: '' });
  const [errors, setErrors] = useState<Record<string, string>>({});

  useEffect(() => {
    if (isEdit) {
      apiClient.getCustomer(id!).then(data => setForm(data));
    }
  }, [id]);

  const handleSubmit = async () => {
    const validationErrors = validate(form, customerValidationRules);
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }
    if (isEdit) {
      await apiClient.updateCustomer(id!, form);
    } else {
      await apiClient.createCustomer(form);
    }
    navigate('/customers');
  };

  return (
    <div className="p-6 max-w-2xl">
      <h1 className="text-2xl font-bold mb-6">
        {isEdit ? '顧客編集' : '顧客新規登録'}
      </h1>

      <FormField label="顧客名" required error={errors.name}>
        <Input value={form.name} onChange={v => setForm({ ...form, name: v })} />
      </FormField>

      <FormField label="メールアドレス" required error={errors.email}>
        <Input type="email" value={form.email} onChange={v => setForm({ ...form, email: v })} />
      </FormField>

      <FormField label="電話番号" error={errors.phone}>
        <Input value={form.phone} onChange={v => setForm({ ...form, phone: v })} />
      </FormField>

      <FormField label="住所" error={errors.address}>
        <Textarea value={form.address} onChange={v => setForm({ ...form, address: v })} />
      </FormField>

      <div className="flex gap-2 mt-6">
        <Button onClick={handleSubmit}>{isEdit ? '更新' : '登録'}</Button>
        <Button variant="outline" onClick={() => navigate('/customers')}>キャンセル</Button>
      </div>
    </div>
  );
};
```

**8c. Generate navigation/routing with ALL entity pages:** ⭐ NEW!

```tsx
// App.tsx — routes auto-generated for ALL entities
const routes = [
  // Dashboard
  { path: '/', element: <DashboardPage /> },

  // Customer (MASTER_DATA) — Full CRUD
  { path: '/customers', element: <CustomerListPage /> },
  { path: '/customers/new', element: <CustomerFormPage /> },
  { path: '/customers/:id', element: <CustomerDetailPage /> },
  { path: '/customers/:id/edit', element: <CustomerFormPage /> },

  // ShippingStaff (SYSTEM_ACTOR) — Full CRUD
  { path: '/shipping-staffs', element: <ShippingStaffListPage /> },
  { path: '/shipping-staffs/new', element: <ShippingStaffFormPage /> },
  { path: '/shipping-staffs/:id', element: <ShippingStaffDetailPage /> },
  { path: '/shipping-staffs/:id/edit', element: <ShippingStaffFormPage /> },

  // Product (MASTER_DATA) — Full CRUD
  { path: '/products', element: <ProductListPage /> },
  { path: '/products/new', element: <ProductFormPage /> },
  { path: '/products/:id', element: <ProductDetailPage /> },
  { path: '/products/:id/edit', element: <ProductFormPage /> },

  // Order (TRANSACTION) — Full CRUD + use-case-specific pages
  { path: '/orders', element: <OrderListPage /> },
  { path: '/orders/new', element: <OrderFormPage /> },
  { path: '/orders/:id', element: <OrderDetailPage /> },
  { path: '/orders/:id/edit', element: <OrderFormPage /> },

  // Shipment (TRANSACTION) — Full CRUD
  { path: '/shipments', element: <ShipmentListPage /> },
  { path: '/shipments/new', element: <ShipmentFormPage /> },
  { path: '/shipments/:id', element: <ShipmentDetailPage /> },
  { path: '/shipments/:id/edit', element: <ShipmentFormPage /> },
];

// Sidebar navigation — auto-generated from entity classification
const navigation = [
  { label: 'ダッシュボード', path: '/', icon: 'Home' },
  { group: 'マスタ管理', items: [
    { label: '顧客管理', path: '/customers', icon: 'Users' },
    { label: '商品管理', path: '/products', icon: 'Package' },
    { label: '出荷担当者管理', path: '/shipping-staffs', icon: 'UserCog' },
  ]},
  { group: 'トランザクション', items: [
    { label: '受注管理', path: '/orders', icon: 'ShoppingCart' },
    { label: '出荷管理', path: '/shipments', icon: 'Truck' },
  ]},
];
```

**8d. Generate shared UI components:** ⭐ NEW!

Generate reusable components used across all CRUD pages:

```
frontend/src/components/shared/
├── DataTable.tsx          # Sortable table with actions column
├── Pagination.tsx         # Page navigation
├── SearchBar.tsx          # Text search input
├── FormField.tsx          # Label + input + error message
├── DetailSection.tsx      # Read-only section with title
├── DetailField.tsx        # Label + value pair
├── DeleteButton.tsx       # Confirm-delete button
├── Loading.tsx            # Loading spinner
├── Badge.tsx              # Status badge (color-coded)
└── Layout/
    ├── Sidebar.tsx        # Navigation sidebar
    └── PageHeader.tsx     # Page title + action buttons
```

**8e. Generate use-case-specific UI components (existing behavior):**

**React:**
```tsx
export const OrderForm: React.FC = () => {
  const [items, setItems] = useState<OrderItem[]>([]);
  
  const handleSubmit = async () => {
    await apiClient.createOrder({ items });
  };
  
  return (
    <form onSubmit={handleSubmit}>
      {/* Form fields */}
    </form>
  );
};
```

**Vue:**
```vue
<template>
  <form @submit.prevent="handleSubmit">
    <!-- Form fields -->
  </form>
</template>

<script setup lang="ts">
import { ref } from 'vue';
const items = ref<OrderItem[]>([]);
</script>
```

---

> ## ✅ Step 8 完了チェックリスト（必須確認）
>
> **`frontend_framework != "none"` の場合、Step 8 を完了と宣言する前に以下を全て確認すること。**
> チェックが通らないファイルは生成してから次に進む。
>
> ### ⚠️ SYSTEM_ACTOR / MASTER_DATA エンティティの CRUD 必須生成（最重要）
>
> **domain-model.json の type が `SYSTEM_ACTOR` または `MASTER_DATA` のエンティティは、**
> **ユースケースに明示されていなくても、必ずバックエンドとフロントエンドの CRUD コードを生成すること。**
>
> 生成前に以下の Python スニペットで対象エンティティを列挙して確認すること：
>
> ```python
> import json
> with open('{project}_domain-model.json') as f:
>     dm = json.load(f)
> targets = [e for e in dm['entities'] if e['type'] in ('SYSTEM_ACTOR', 'MASTER_DATA')]
> for e in targets:
>     print(f"  → {e['name']} ({e['japanese_name']}) / {e['type']} — Service + Routes + Page が必要")
> ```
>
> 列挙したエンティティ全てについて、バックエンドとフロントエンドの両方を生成していない場合は
> **Step 8 完了を宣言してはならない。** 今すぐ生成すること。
>
> **SYSTEM_ACTOR の特別対応:**
> - パスワードは bcrypt(12) でハッシュ化した上で保存
> - `password` フィールドは API レスポンスから除外（`select: { password: false }`）
> - パスワード変更は専用エンドポイント `PATCH /api/{entities}/:id/password` を別途生成
>
> **MASTER_DATA (Customer 等) の特別対応:**
> - 登録時に関連エンティティ（与信枠など）をトランザクション内で自動生成
> - ビジネスルール（BR-001 等）に従った初期値を設定
>
> **フロントエンドの管理画面:**
> - SYSTEM_ACTOR と MASTER_DATA の CRUD ページは `AdminPage.tsx` にまとめるか、
>   または `pages/{EntityName}ManagePage.tsx` として個別生成する
> - `App.tsx` の Role switcher に `ADMIN` ロールを追加し、管理画面へのルーティングを追加する
>
> **⚠️ types/index.ts と api/client.ts の完全性チェック（FORBIDDEN パターン）:**
>
> ```
> 以下は FORBIDDEN（禁止）— 発見した場合は修正してから Step 8 完了を宣言すること:
>
> ❌ ページコンポーネント（AdminPage.tsx 等）内にローカルで interface / type を定義している
>    → types/index.ts に移動すること
>
> ❌ ページコンポーネント内に fetch() を直接呼ぶ関数が定義されている
>    → api/client.ts に移動すること
>
> ❌ api/client.ts に SYSTEM_ACTOR / MASTER_DATA の一覧取得関数（fetchXxxList / fetchXxxs）がない
>    → 追加すること（一覧表示は CRUD の必須機能）
>
> ❌ types/index.ts に SalesRepresentative / ShippingStaff 等の SYSTEM_ACTOR 型が未定義
>    → interface を追加すること
> ```
>
> ```bash
> # ページ内ローカル型定義・fetch 直呼び の検出コマンド
> grep -n "^interface \|^type \|= await fetch(" \
>   /home/claude/{project}/frontend/src/pages/AdminPage.tsx \
>   && echo "❌ FORBIDDEN パターン検出 → types / api/client.ts に移動" \
>   || echo "✅ ローカル定義なし"
>
> # api/client.ts の一覧取得関数の確認
> python3 -c "
> import json
> with open('{project}_domain-model.json') as f: dm=json.load(f)
> targets = [e['name'] for e in dm['entities'] if e['type'] in ('SYSTEM_ACTOR','MASTER_DATA')]
> client = open('/home/claude/{project}/frontend/src/api/client.ts').read()
> types  = open('/home/claude/{project}/frontend/src/types/index.ts').read()
> for name in targets:
>     has_fetch  = f'fetch{name}' in client
>     has_type   = f'interface {name}' in types
>     has_create_type = f'Create{name}' in types
>     ok = has_fetch and has_type and has_create_type
>     print(f\"{'✅' if ok else '❌'} {name}: fetch={has_fetch}, interface={has_type}, CreateType={has_create_type}\")
> "
> ```
>
> ---
>
> ### フロントエンド必須ファイル
>
> | ファイル | 確認 |
> |---------|------|
> | `frontend/src/App.tsx` (または `main.tsx`) | ルートコンポーネント（ADMIN ロール含む） |
> | `frontend/src/types/index.ts` | 全エンティティの型定義 |
> | `frontend/src/api/client.ts` | 全エンドポイントの API クライアント |
> | `frontend/src/hooks/index.ts` | useXxx カスタムフック |
> | UC ごとの Page コンポーネント | 各ユースケースに対応するページ |
> | **SYSTEM_ACTOR/MASTER_DATA の管理ページ** | **AdminPage.tsx または個別 ManagePage** |
> | 共有コンポーネント（Badge, Card 等） | 再利用可能な UI 部品 |
>
> ### バックエンド必須ファイル（再確認）
>
> | ファイル | 確認 |
> |---------|------|
> | `database/schema.prisma` (または同等) | DBスキーマ |
> | `backend/src/domain/{Entity}.ts` | ドメインエンティティ（全エンティティ） |
> | `backend/src/application/{Entity}Service.ts` | **全エンティティ**（SYSTEM_ACTOR/MASTER_DATA 含む） |
> | `backend/src/presentation/{entity}Routes.ts` | **全エンティティ**（SYSTEM_ACTOR/MASTER_DATA 含む） |
> | `README.md` | セットアップ手順 |
>
> ### 自己チェック手順
>
> ```bash
> # フロントエンドファイルが実際に存在するか必ず確認すること
> find /home/claude/{project}/frontend/src -type f | sort
>
> # SYSTEM_ACTOR/MASTER_DATA の Service/Routes が生成されているか確認
> python3 -c "
> import json, os
> with open('{project}_domain-model.json') as f: dm=json.load(f)
> targets = [e['name'] for e in dm['entities'] if e['type'] in ('SYSTEM_ACTOR','MASTER_DATA')]
> base = '/home/claude/{project}/backend/src'
> for name in targets:
>     svc  = os.path.exists(f'{base}/application/{name}Service.ts')
>     route = os.path.exists(f'{base}/presentation/{name[0].lower()}{name[1:]}Routes.ts') or \
>             os.path.exists(f'{base}/presentation/{name}Routes.ts')
>     status = '✅' if svc and route else '❌ 未生成 → 今すぐ生成'
>     print(f'{status} {name}: Service={svc}, Routes={route}')
> "
> ```
>
> ⚠️ **「生成した」と思っていても、bash brace expansion の問題でファイルが存在しないことがある。**
> **`find` コマンドで実際のファイル一覧を確認してから Step 8 完了を宣言すること。**

---

### Step 9: Generate Configuration Files

**9a. Environment configuration:**
```env
# .env.example
DATABASE_URL=postgresql://user:pass@localhost:5432/db
PORT=3000
NODE_ENV=development
```

**9b. Docker configuration:**
```dockerfile
# Dockerfile (backend)
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
CMD ["npm", "start"]
```

**9c. Docker Compose (monolith):**
```yaml
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: ${DB_NAME}
  backend:
    build: ./backend
    ports:
      - "3000:3000"
    depends_on:
      - postgres
  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
```

**9d. Kubernetes manifests (microservices):**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: order-service
        image: order-service:latest
        ports:
        - containerPort: 3000
```

---

### Step 10: Generate Documentation

**10a. README.md:**
```markdown
# {Project Name}

## Technology Stack / 技術スタック
- Backend: {language} + {framework}
- Frontend: {frontend framework}
- Database: {database}
- Architecture: {architecture}

## Setup / セットアップ
[Installation instructions based on stack]

## API Documentation / API仕様
[Generated from use cases]
```

**10b. API documentation:**
- OpenAPI/Swagger spec
- Endpoint descriptions from use cases
- Request/response examples

---


## Output Structure & Documentation Templates

For output directory structure and documentation templates (README, API docs, deployment guide), read:
- `templates/doc-templates.md`

> ⚠️ Only read templates/doc-templates.md AFTER code generation is complete, when generating documentation files.

## Best Practices / ベストプラクティス

### CRUD Generation ⭐ NEW!

1. **Every entity gets CRUD**: No entity in domain-model.json should lack basic CRUD operations. Even if a use case only mentions "register customer", the generated app must also include list, detail, edit, and delete pages for customers.
2. **System actors need management**: If an actor (e.g., ShippingStaff, OrderClerk) is modeled as an entity, generate a full management UI — registration, list, edit, deactivate. Users should never need to type actor names manually during operations.
3. **Shared components first**: Generate reusable DataTable, Pagination, SearchBar, FormField components before individual entity pages to ensure consistency.
4. **Sidebar navigation**: Auto-generate sidebar with grouped navigation (Master Data, Transactions) so users can access all entity management screens.
5. **Consistent patterns**: All list pages use DataTable + SearchBar + Pagination. All form pages use FormField with validation. All detail pages use DetailSection + DetailField.

### Code Quality

1. **Type safety**: Generate with types from class diagram
2. **Error handling**: Comprehensive try-catch blocks
3. **Validation**: DTOs with validation decorators
4. **Testing**: Unit test stubs for services
5. **Documentation**: Inline comments from use cases

### Architecture / アーキテクチャ

1. **Separation of concerns**: Domain, services, API layers
2. **Dependency injection**: Framework-appropriate patterns
3. **Configuration**: Environment-based settings
4. **Logging**: Structured logging setup
5. **Monitoring**: Health check endpoints

### Deployment / デプロイメント

1. **Containerization**: Docker for consistency
2. **Orchestration**: Kubernetes for microservices
3. **Infrastructure as code**: Terraform/CloudFormation
4. **CI/CD**: GitHub Actions/GitLab CI templates
5. **Environment parity**: Dev/staging/prod configs

---

## Version History / バージョン履歴

- **v1.1** (2026-02-18): Entity CRUD auto-generation ⭐
  - Step 5.5: Entity CRUD classification (Master Data, Transaction, Sub-entity, System Actor)
  - Step 6: CRUD services for ALL entities (not just use-case-referenced)
  - Step 7: RESTful CRUD API endpoints for ALL entities
  - Step 8: List, Detail, Form pages for ALL entities + shared UI components + sidebar navigation
  - Fixes: System actors (e.g., ShippingStaff) now get full management UI
  - Fixes: Entities with create operations now always include list pages
- **v1.0** (2026-01-22): Initial version
  - Technology stack selection
  - Multiple architecture support
  - Framework flexibility
  - Mandatory class diagram reference
