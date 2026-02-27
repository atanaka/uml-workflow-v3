## Output Structure

### Monolith

```
{project}/
├── README.md
├── docker-compose.yml
├── backend/
│   ├── package.json (or requirements.txt, pom.xml)
│   ├── tsconfig.json (or pyproject.toml, etc.)
│   ├── .env.example
│   ├── prisma/schema.prisma (or equivalent)
│   └── src/
│       ├── types/
│       │   ├── index.ts             # Shared types
│       │   ├── pagination.ts        # PaginatedResult, ListParams ⭐
│       │   └── dto/                 # Create/Update DTOs per entity ⭐
│       ├── domain/
│       ├── services/
│       │   ├── customer.service.ts  # Full CRUD ⭐
│       │   ├── product.service.ts   # Full CRUD ⭐
│       │   ├── shipping-staff.service.ts  # Full CRUD ⭐
│       │   ├── order.service.ts     # CRUD + use-case logic
│       │   └── shipment.service.ts  # CRUD + use-case logic
│       ├── api/
│       │   ├── customers.ts         # CRUD endpoints ⭐
│       │   ├── products.ts          # CRUD endpoints ⭐
│       │   ├── shipping-staffs.ts   # CRUD endpoints ⭐
│       │   ├── orders.ts            # CRUD + use-case endpoints
│       │   └── shipments.ts         # CRUD + use-case endpoints
│       └── index.ts
└── frontend/
    ├── package.json
    ├── vite.config.ts (or webpack.config.js)
    └── src/
        ├── api/
        │   └── client.ts            # API client with ALL entity CRUD ⭐
        ├── components/
        │   └── shared/              # DataTable, Pagination, SearchBar, etc. ⭐
        ├── pages/
        │   ├── DashboardPage.tsx     # Overview dashboard ⭐
        │   ├── customers/            # List, Detail, Form pages ⭐
        │   ├── products/             # List, Detail, Form pages ⭐
        │   ├── shipping-staffs/      # List, Detail, Form pages ⭐
        │   ├── orders/               # List, Detail, Form pages
        │   └── shipments/            # List, Detail, Form pages
        ├── types/
        └── App.tsx                   # Routes + Sidebar navigation ⭐
```

### Microservices

```
{project}/
├── README.md
├── docker-compose.yml (for local dev)
├── kubernetes/
│   ├── order-service.yaml
│   ├── inventory-service.yaml
│   └── ingress.yaml
├── services/
│   ├── order-service/
│   ├── inventory-service/
│   └── shipping-service/
└── frontend/
```

### Serverless

```
{project}/
├── README.md
├── serverless.yml (or SAM template)
├── functions/
│   ├── create-order/
│   ├── get-inventory/
│   └── create-shipment/
├── infrastructure/
│   └── terraform/ (or CloudFormation)
└── frontend/
```

---

## Technology Stack Matrix

### Supported Combinations

| Language | Frameworks | ORMs | Databases |
|----------|-----------|------|-----------|
| TypeScript | Express, NestJS | Prisma, TypeORM | PostgreSQL, MySQL, MongoDB |
| Python | FastAPI, Flask, Django | SQLAlchemy, Django ORM | PostgreSQL, MySQL, MongoDB |
| Java | Spring Boot | Hibernate, JPA | PostgreSQL, MySQL, Oracle |
| Go | Gin, Echo | GORM | PostgreSQL, MySQL |
| C# | ASP.NET Core | Entity Framework | SQL Server, PostgreSQL |

### Frontend Options

| Framework | Build Tools | Styling |
|-----------|------------|---------|
| React | Vite, Next.js, Create React App | Tailwind, styled-components, SCSS |
| Vue | Vite, Nuxt.js | Tailwind, SCSS |
| Angular | Angular CLI | SCSS, CSS |
| Svelte | Vite, SvelteKit | Tailwind, SCSS |

---

## Documentation Output

All generated projects include comprehensive documentation.

### 1. README.md (Enhanced)

**Location:** `{project}/README.md`

**Enhanced contents:**
```markdown
# {Project Name}

## Overview
[System description from business overview]

## Features
- [Feature 1 from use cases]
- [Feature 2 from use cases]

## Architecture
- **Type**: Monolith / Microservices / Serverless
- **Backend**: {Stack}
- **Frontend**: {Stack}
- **Database**: {Database}

## Quick Start

### Prerequisites
- Node.js 18+ (or Python 3.11+, Java 17+, etc.)
- Docker and Docker Compose
- PostgreSQL client (optional)

### Installation

1. Clone the repository
```bash
git clone {repo}
cd {project}
```

2. Install dependencies
```bash
# Backend
cd backend
npm install  # or pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

3. Configure environment
```bash
cp backend/.env.example backend/.env
# Edit .env with your settings
```

4. Start with Docker Compose
```bash
docker-compose up
```

5. Access the application
- Frontend: http://localhost:5173
- Backend API: http://localhost:3000
- API Docs: http://localhost:3000/api-docs

## Project Structure

[Detailed directory structure]

## API Documentation

See [API-specification.md](./API-specification.md) for detailed API documentation.

## Database Schema

[ERD diagram or schema description]

## Development

### Running tests
```bash
# Backend
cd backend
npm test

# Frontend
cd frontend
npm test
```

### Code formatting
```bash
npm run format
npm run lint
```

## Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for deployment instructions.

## Technology Stack

**Backend:**
- Language: TypeScript
- Framework: Express
- ORM: Prisma
- Validation: Zod

**Frontend:**
- Language: TypeScript
- Framework: React
- UI: Tailwind CSS + shadcn/ui
- State: Context API

**Infrastructure:**
- Database: PostgreSQL
- Cache: Redis (optional)
- Deployment: Docker + Kubernetes

## Use Cases Implemented

- UC-001: {Use case name} ({story points} points)
- UC-002: {Use case name} ({story points} points)

Total: {total story points} story points

## Domain Model

See [architecture-overview.md](../architecture-overview.md) for complete domain model documentation.

## Contributing

[Contribution guidelines]

## License

[License information]

---

*Generated by: usecase-to-code-v1*
*Generation date: {timestamp}*
*Based on: {project}_usecase-output.json, {project}_class.puml*
```

---

### 2. API Specification (NEW!)

**Location:** `{project}/API-specification.md`

**Complete API documentation:**
```markdown
# API仕様書: {Project Name}

## 概要

このドキュメントは {Project Name} のREST API仕様を定義します。

**ベースURL:** `http://localhost:3000/api` (開発環境)

**認証方式:** JWT Bearer Token

---

## エンドポイント一覧

### 受注管理 (Orders)

#### POST /api/orders
**説明:** 新規受注を作成

**認証:** 必要（受注係ロール）

**リクエストヘッダー:**
```
Content-Type: application/json
Authorization: Bearer {token}
```

**リクエストボディ:**
```json
{
  "customerId": "uuid",
  "items": [
    {
      "productId": "uuid",
      "quantity": 10,
      "unitPrice": 1500.00
    }
  ],
  "shippingAddress": {
    "postalCode": "100-0001",
    "prefecture": "東京都",
    "city": "千代田区",
    "addressLine1": "丸の内1-1-1"
  }
}
```

**レスポンス (201 Created):**
```json
{
  "orderId": "uuid",
  "customerId": "uuid",
  "orderDate": "2026-01-24T10:30:00Z",
  "status": "RECEIVED",
  "totalAmount": 15000.00,
  "items": [
    {
      "orderItemId": "uuid",
      "productId": "uuid",
      "productName": "商品A",
      "quantity": 10,
      "unitPrice": 1500.00,
      "subtotal": 15000.00
    }
  ],
  "createdAt": "2026-01-24T10:30:00Z",
  "updatedAt": "2026-01-24T10:30:00Z"
}
```

**エラーレスポンス:**

```json
// 400 Bad Request - バリデーションエラー
{
  "error": "VALIDATION_ERROR",
  "message": "Invalid request data",
  "details": [
    {
      "field": "items[0].quantity",
      "message": "Quantity must be greater than 0"
    }
  ]
}

// 404 Not Found - 顧客が見つからない
{
  "error": "CUSTOMER_NOT_FOUND",
  "message": "Customer with ID {customerId} not found"
}

// 409 Conflict - 在庫不足
{
  "error": "INSUFFICIENT_INVENTORY",
  "message": "Insufficient inventory for product {productId}",
  "details": {
    "productId": "uuid",
    "requestedQuantity": 10,
    "availableQuantity": 5
  }
}

// 500 Internal Server Error
{
  "error": "INTERNAL_ERROR",
  "message": "An unexpected error occurred"
}
```

**バリデーションルール:**
- customerId: 必須、UUID形式
- items: 必須、最低1件
- items[].quantity: 必須、1以上の整数
- items[].unitPrice: 必須、0より大きい数値

**ビジネスルール:**
- 在庫確認を実施し、不足時はエラー
- 合計金額が最小注文金額（10,000円）以上
- 営業時間外の場合は受付不可

**関連ユースケース:**
- UC-001: 商品を注文する

---

#### GET /api/orders/{orderId}
**説明:** 受注詳細を取得

[同様の詳細仕様]

---

#### PUT /api/orders/{orderId}/confirm
**説明:** 受注を確定する

[同様の詳細仕様]

---

### 在庫管理 (Inventory)

#### GET /api/inventory/{productId}
**説明:** 在庫数を確認

[詳細仕様]

---

### 商品管理 (Products)

#### GET /api/products
**説明:** 商品一覧を取得

[詳細仕様]

---

## データモデル

### Order (受注)
```typescript
interface Order {
  orderId: string;          // UUID
  customerId: string;       // UUID
  orderDate: Date;
  status: OrderStatus;
  totalAmount: number;      // Decimal(10,2)
  items: OrderItem[];
  createdAt: Date;
  updatedAt: Date;
}

enum OrderStatus {
  RECEIVED = 'RECEIVED',
  CONFIRMED = 'CONFIRMED',
  SHIPPED = 'SHIPPED',
  CANCELLED = 'CANCELLED'
}
```

[全データモデルの定義]

---

## エラーハンドリング

### エラーコード一覧

| コード | HTTP Status | 説明 |
|--------|-------------|------|
| VALIDATION_ERROR | 400 | リクエストデータが不正 |
| UNAUTHORIZED | 401 | 認証が必要 |
| FORBIDDEN | 403 | 権限不足 |
| NOT_FOUND | 404 | リソースが見つからない |
| CONFLICT | 409 | 状態の競合 |
| INTERNAL_ERROR | 500 | サーバー内部エラー |

---

## 認証とセキュリティ

### JWT トークン取得
```
POST /api/auth/login
{
  "username": "string",
  "password": "string"
}

→ Response:
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "expiresIn": 3600
}
```

### トークンの使用
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

### ロールベースアクセス制御

| ロール | 権限 |
|--------|------|
| customer | 注文閲覧のみ |
| order_clerk | 注文作成・確認 |
| shipping_staff | 出荷処理 |
| admin | 全操作 |

---

## レート制限

- 認証済みユーザー: 1000リクエスト/時
- 未認証: 100リクエスト/時

超過時: HTTP 429 Too Many Requests

---

## ページネーション

リスト取得APIはページネーション対応:

**リクエストパラメータ:**
- `page`: ページ番号 (デフォルト: 1)
- `limit`: 1ページあたりの件数 (デフォルト: 20、最大: 100)

**レスポンス:**
```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "totalPages": 8
  }
}
```

---

## バージョニング

APIバージョンはURLパスに含む:
```
/api/v1/orders
/api/v2/orders
```

現在のバージョン: v1

---

*生成日時: {timestamp}*
*生成ツール: usecase-to-code-v1*
*バージョン: 1.0*
```

---

### 3. Deployment Guide (NEW!)

**Location:** `{project}/DEPLOYMENT.md`

**Comprehensive deployment documentation:**
```markdown
# デプロイメントガイド: {Project Name}

## 1. デプロイメント概要

### サポートされる環境
- Docker Compose (開発・テスト環境)
- Kubernetes (本番環境推奨)
- AWS (ECS, Lambda)
- Azure (Container Apps)
- Google Cloud (Cloud Run)

---

## 2. Docker Compose デプロイメント

### 2.1 前提条件
- Docker 20.10+
- Docker Compose 2.0+

### 2.2 デプロイ手順

**1. 環境変数の設定**
```bash
cp .env.example .env
# .envを編集
```

**2. ビルドと起動**
```bash
docker-compose up --build -d
```

**3. データベース初期化**
```bash
docker-compose exec backend npm run prisma:migrate
docker-compose exec backend npm run prisma:seed
```

**4. 動作確認**
```bash
curl http://localhost:3000/health
```

### 2.3 サービス構成

```yaml
services:
  backend:
    ports: 3000
  frontend:
    ports: 5173
  database:
    ports: 5432
  redis:
    ports: 6379
```

---

## 3. Kubernetes デプロイメント

### 3.1 前提条件
- Kubernetes 1.25+
- kubectl configured
- Container registry access

### 3.2 デプロイ手順

**1. イメージビルドとプッシュ**
```bash
# Backend
docker build -t {registry}/backend:v1.0.0 ./backend
docker push {registry}/backend:v1.0.0

# Frontend
docker build -t {registry}/frontend:v1.0.0 ./frontend
docker push {registry}/frontend:v1.0.0
```

**2. Secretsの作成**
```bash
kubectl create secret generic app-secrets \
  --from-literal=DATABASE_URL='postgresql://...' \
  --from-literal=JWT_SECRET='...'
```

**3. デプロイ**
```bash
kubectl apply -f kubernetes/
```

**4. 動作確認**
```bash
kubectl get pods
kubectl get services
```

### 3.3 Kubernetes マニフェスト構成

```
kubernetes/
├── namespace.yaml
├── configmap.yaml
├── secrets.yaml
├── backend-deployment.yaml
├── backend-service.yaml
├── frontend-deployment.yaml
├── frontend-service.yaml
├── database-statefulset.yaml
├── database-service.yaml
├── ingress.yaml
└── hpa.yaml (Horizontal Pod Autoscaler)
```

---

## 4. AWS デプロイメント

### 4.1 ECS (Elastic Container Service)

[詳細手順]

### 4.2 Lambda + API Gateway (Serverless)

[詳細手順]

---

## 5. 環境変数

### Backend環境変数

| 変数名 | 説明 | デフォルト | 必須 |
|--------|------|------------|------|
| DATABASE_URL | PostgreSQL接続文字列 | - | ✓ |
| JWT_SECRET | JWT署名用秘密鍵 | - | ✓ |
| PORT | APIサーバーポート | 3000 | |
| NODE_ENV | 実行環境 | development | |
| LOG_LEVEL | ログレベル | info | |

### Frontend環境変数

| 変数名 | 説明 | デフォルト | 必須 |
|--------|------|------------|------|
| VITE_API_URL | APIベースURL | http://localhost:3000 | ✓ |
| VITE_APP_NAME | アプリ名 | - | |

---

## 6. データベース

### 6.1 マイグレーション実行

**開発環境:**
```bash
npm run prisma:migrate:dev
```

**本番環境:**
```bash
npm run prisma:migrate:deploy
```

### 6.2 バックアップ

**手動バックアップ:**
```bash
pg_dump -h localhost -U postgres -d {dbname} > backup.sql
```

**自動バックアップ (Kubernetes CronJob):**
```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: db-backup
spec:
  schedule: "0 2 * * *"  # 毎日2時
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: postgres:15
            command: ["/bin/sh", "-c"]
            args:
            - pg_dump ... | gzip > /backup/$(date +\%Y\%m\%d).sql.gz
```

---

## 7. モニタリングとログ

### 7.1 ヘルスチェック

**Backend:**
```
GET /health
→ { "status": "ok", "database": "connected" }
```

**Kubernetes Liveness Probe:**
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 3000
  initialDelaySeconds: 30
  periodSeconds: 10
```

### 7.2 ログ収集

**Docker Compose:**
```bash
docker-compose logs -f backend
```

**Kubernetes:**
```bash
kubectl logs -f deployment/backend
```

**集約ログ (推奨):**
- ELK Stack (Elasticsearch, Logstash, Kibana)
- AWS CloudWatch Logs
- Google Cloud Logging

---

## 8. スケーリング

### 8.1 水平スケーリング (Kubernetes HPA)

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: backend-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: backend
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

---

## 9. セキュリティ

### 9.1 SSL/TLS設定

**Let's Encrypt (Kubernetes Ingress):**
```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: app-tls
spec:
  secretName: app-tls-secret
  issuerRef:
    name: letsencrypt-prod
    kind: ClusterIssuer
  dnsNames:
  - {domain}
```

### 9.2 ネットワークポリシー

[Kubernetes NetworkPolicy設定]

---

## 10. トラブルシューティング

### よくある問題

**問題: データベース接続エラー**
```
解決策:
1. DATABASE_URLが正しいか確認
2. データベースが起動しているか確認
3. ネットワーク接続を確認
```

**問題: フロントエンドがAPIにアクセスできない**
```
解決策:
1. VITE_API_URLが正しいか確認
2. CORSポリシーを確認
3. ネットワーク設定を確認
```

---

*生成日時: {timestamp}*
*生成ツール: usecase-to-code-v1*
*バージョン: 1.0*
```

---

