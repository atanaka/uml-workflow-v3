## Language Support / 言語サポート ⭐

### Overview / 概要

This skill generates code with language-appropriate comments and documentation, inheriting settings from the domain model to ensure consistency with modeling artifacts.

**Supported Languages:**
- **Japanese (日本語)**: Code comments, JSDoc, and documentation in Japanese
- **English**: Code comments, JSDoc, and documentation in English
- **Note**: Code identifiers (class names, method names) are ALWAYS in English for international compatibility

### Language Scope

**What is localized:**
- ✅ Code comments (`//` and `/* */`)
- ✅ JSDoc/docstrings
- ✅ README.md and documentation files
- ✅ API documentation
- ✅ Error messages (where appropriate)
- ✅ Console log messages (where appropriate)

**What is NOT localized:**
- ✅ Class names (always English)
- ✅ Method names (always English)
- ✅ Variable names (always English)
- ✅ API endpoint paths (always English)

### Language Inheritance

**Priority Order:**
1. **From domain-model.json** (highest priority)
   - Reads `language_config` if present
   - Or infers from entity descriptions
2. **Manual override** (if specified)
   - Can override via `code_comment_language` parameter
3. **Default** (fallback)
   - English for international compatibility

**Example inheritance:**
```json
// From usecase-to-class-v1 output (domain-model.json)
{
  "metadata": {
    "language": "ja"
  },
  "entities": [
    {
      "name": "Product",
      "japanese_name": "商品",
      "description": "販売する商品の情報"
    }
  ]
}

// usecase-to-code-v1 generates:
/**
 * 商品エンティティ
 * 販売する商品の情報を管理する
 */
export class Product {
  // 商品ID（一意識別子）
  private productId: string;
  
  /**
   * 価格を取得
   * @returns 商品の価格
   */
  public getPrice(): Decimal {
    return this.price;
  }
}
```

### Language Configuration

**Parameters:**
```python
language_options = {
    "code_comment_language": "auto",    # auto | ja | en
    "inherit_from_domain_model": True,  # Inherit from domain-model.json
    "jsdoc_language": "auto",           # auto | ja | en (follows code_comment_language)
    "readme_language": "auto",          # auto | ja | en (follows code_comment_language)
    "api_doc_language": "auto",         # auto | ja | en
    "error_messages": "en",             # en (recommended for stack traces)
    "console_logs": "auto"              # auto | ja | en
}
```

### Code Comment Examples

#### TypeScript (language="ja")
```typescript
/**
 * 受注エンティティ
 * システムに登録された受注情報を管理する
 */
export class ReceivedOrder {
  // 受注ID（主キー）
  private receivedOrderId: string;
  
  // 顧客ID（外部キー）
  private customerId: string;
  
  // 受注ステータス
  private status: OrderStatus;
  
  /**
   * 受注を確定する
   * ステータスをPENDINGからCONFIRMEDに変更
   * @throws {InvalidStatusError} 既に確定済みの場合
   */
  public confirm(): void {
    if (this.status !== OrderStatus.PENDING) {
      throw new InvalidStatusError('受注は既に確定済みです');
    }
    this.status = OrderStatus.CONFIRMED;
    this.updatedAt = new Date();
  }
}
```

#### TypeScript (language="en")
```typescript
/**
 * ReceivedOrder Entity
 * Manages received order information registered in the system
 */
export class ReceivedOrder {
  // Received order ID (primary key)
  private receivedOrderId: string;
  
  // Customer ID (foreign key)
  private customerId: string;
  
  // Order status
  private status: OrderStatus;
  
  /**
   * Confirm the order
   * Changes status from PENDING to CONFIRMED
   * @throws {InvalidStatusError} If already confirmed
   */
  public confirm(): void {
    if (this.status !== OrderStatus.PENDING) {
      throw new InvalidStatusError('Order is already confirmed');
    }
    this.status = OrderStatus.CONFIRMED;
    this.updatedAt = new Date();
  }
}
```

#### Python (language="ja")
```python
class ReceivedOrder:
    """
    受注エンティティ
    システムに登録された受注情報を管理する
    """
    
    def __init__(self, received_order_id: str, customer_id: str):
        # 受注ID（主キー）
        self.received_order_id = received_order_id
        
        # 顧客ID（外部キー）
        self.customer_id = customer_id
        
        # 受注ステータス
        self.status = OrderStatus.PENDING
    
    def confirm(self) -> None:
        """
        受注を確定する
        ステータスをPENDINGからCONFIRMEDに変更
        
        Raises:
            InvalidStatusError: 既に確定済みの場合
        """
        if self.status != OrderStatus.PENDING:
            raise InvalidStatusError("受注は既に確定済みです")
        self.status = OrderStatus.CONFIRMED
        self.updated_at = datetime.now()
```

### Documentation Examples

#### README.md (language="ja")
```markdown
# 受注管理システム

## 概要 / Overview

Eコマースサイトにおける受注・出荷管理システム。

## 機能 / Features

- 商品注文機能
- 受注確認機能
- 出荷管理機能

## セットアップ / Setup

### 必要要件

- Node.js 20.x以降
- PostgreSQL 15.x以降

### インストール

\`\`\`bash
npm install
\`\`\`

### データベース設定

\`\`\`bash
npm run db:migrate
\`\`\`

## 実行 / Running

\`\`\`bash
npm run dev
\`\`\`

## API仕様 / API Documentation

詳細は `docs/api.md` を参照してください。
```

#### README.md (language="en")
```markdown
# Order Management System

## Overview / 概要

Order and shipping management system for e-commerce platform.

## Features / 機能

- Product ordering functionality
- Order confirmation functionality
- Shipping management functionality

## Setup / セットアップ

### Requirements

- Node.js 20.x or later
- PostgreSQL 15.x or later

### Installation

\`\`\`bash
npm install
\`\`\`

### Database Setup

\`\`\`bash
npm run db:migrate
\`\`\`

## Running / 実行

\`\`\`bash
npm run dev
\`\`\`

## API Documentation / API仕様

See `docs/api.md` for details.
```

### Best Practices / ベストプラクティス

**Recommended settings:**
1. **Domestic projects**: `code_comment_language="ja"`
   - Team communication in Japanese
   - Easier code review for Japanese developers
   
2. **International projects**: `code_comment_language="en"`
   - Global team collaboration
   - Standard for open source

3. **Error messages**: Always `"en"`
   - Better for debugging (stack traces, logs)
   - Easier to search for solutions online

4. **Mixed teams**: Consider English comments with Japanese documentation
   ```python
   code_comment_language = "en"
   readme_language = "ja"
   ```

### Language Selection Guide

| Team Type | Code Comments | README | API Docs |
|-----------|--------------|---------|----------|
| Japanese-only | ja | ja | ja |
| International | en | en | en |
| Mixed (Japan-based) | en | ja | ja |
| Mixed (global) | en | en | en |

---

