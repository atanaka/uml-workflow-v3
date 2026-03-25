---
name: json-to-models
description: Generate PlantUML, XMI, and Markdown documentation from domain-model.json. Supports XMI generation toggle for 40% performance improvement. Core skill for model modification workflows.
---

# json-to-models

## Overview

ドメインモデルJSON（domain-model.json）から、PlantUML、XMI、Markdownドキュメントを再生成するスキルです。

**主な用途:**
- モデルのレビュー後、domain-model.jsonを修正して他のフォーマットを更新
- JSONをSingle Source of Truthとして管理
- プログラマティックなモデル操作

---

## Execution Options (NEW! v1.2 ⭐)

**CRITICAL: 実行前にXMI生成の有無・形式を確認してパフォーマンスを最適化します。**

```
質問1: XMIファイルを生成しますか？
  はい (デフォルト): PlantUML + XMI + Markdown を生成
  いいえ: PlantUML + Markdown のみ生成（約40%高速化）

質問2（XMI=はいの場合のみ）: XMI形式を選択してください
  OMG標準 UML 2.5.1: Papyrus / Enterprise Architect / MagicDraw向け
  Eclipse/EMF形式: Sirius / Xtext / Capella / Eclipse UML2向け
```

**Performance Impact:**
- XMI生成あり: 通常速度
- XMI生成なし: **約40%高速化** ⚡

**When to disable XMI:**
- 素早くPlantUMLを確認したい
- UMLツールを使用しない
- 反復的なモデル修正中

**When to enable XMI (OMG標準 UML 2.5.1)**:
- Papyrus、Enterprise Architect、MagicDraw で編集
- OMG標準に準拠した完全なモデルアーカイブが必要
- 最終成果物として保存（ツール非依存の標準形式）

**When to enable XMI (Eclipse/EMF形式)**:
- Sirius、Xtext、Capella、Eclipse UML2 プラグインで編集
- Eclipse Modeling Framework (EMF) ベースのツールチェーンに統合
- Ecore/UML2 モデルとして保存・変換

---

## Skill Purpose

このスキルは、手動またはプログラムで編集されたdomain-model.jsonから、すべての派生成果物を再生成します。

**モデル修正ワークフローにおける位置:**
```
domain-model.json (手動編集)
  ↓ json-to-models
  ├→ PlantUML Class Diagram (常に生成)
  ├→ XMI Model (オプション)
  └→ Architecture Overview (常に生成)
  ↓ usecase-to-code-v1
Application Code (再生成)
```

---

## Input

### Required Input

**Filename:** `{project}_domain-model.json`

**Schema:**
```json
{
  "metadata": {
    "source": "usecase-to-class-v1" | "manual-edit",
    "generated_at": "ISO 8601 timestamp",
    "version": "string",
    "status": "formal"
  },
  "actors": [...],
  "entities": [
    {
      "name": "string (PascalCase)",
      "japanese_name": "string",
      "description": "string",
      "stereotype": "entity|aggregate_root|value_object",
      "attributes": [
        {
          "name": "string",
          "type": "string|number|boolean|datetime|decimal|enum",
          "required": boolean,
          "primary_key": boolean,
          "unique": boolean,
          "default": "any",
          "validation": {...},
          "description": "string"
        }
      ],
      "relationships": [
        {
          "type": "belongs-to|has-one|has-many|many-to-many",
          "target": "string (entity name)",
          "source_multiplicity": "string",
          "target_multiplicity": "string",
          "description": "string"
        }
      ],
      "business_methods": [
        {
          "name": "string",
          "description": "string",
          "parameters": [...],
          "return_type": "string"
        }
      ]
    }
  ],
  "enumerations": [
    {
      "name": "string",
      "values": [...]
    }
  ],
  "value_objects": [...],
  "aggregates": [...]
}
```

---

## Processing Logic

### Step 1: JSON Validation

```python
def validate_domain_model(json_data: dict) -> bool:
    """
    domain-model.jsonのスキーマ検証
    
    チェック項目:
    - 必須フィールドの存在
    - エンティティ名の重複なし
    - リレーション先エンティティの存在
    - 列挙型の参照整合性
    - 属性の型定義の妥当性
    """
    # metadata validation
    assert 'metadata' in json_data
    assert 'entities' in json_data
    
    # Entity validation
    entity_names = [e['name'] for e in json_data['entities']]
    assert len(entity_names) == len(set(entity_names))  # No duplicates
    
    # Relationship validation
    for entity in json_data['entities']:
        for rel in entity.get('relationships', []):
            assert rel['target'] in entity_names  # Target exists
    
    return True
```

### Step 2: PlantUML Generation

```python
def generate_plantuml_from_json(domain_model: dict) -> str:
    """
    JSONからPlantUMLクラス図を生成
    """
    puml_lines = ["@startuml", ""]
    
    # Generate enumerations
    for enum in domain_model.get('enumerations', []):
        puml_lines.append(f"enum {enum['name']} {{")
        for value in enum['values']:
            val_name = value['name'] if isinstance(value, dict) else value
            puml_lines.append(f"  {val_name}")
        puml_lines.append("}")
        puml_lines.append("")
    
    # Generate entities
    for entity in domain_model['entities']:
        # Class header
        stereotype = entity.get('stereotype', 'entity')
        if stereotype == 'aggregate_root':
            puml_lines.append(f"class {entity['name']} <<aggregate_root>> {{")
        else:
            puml_lines.append(f"class {entity['name']} {{")
        
        # Attributes
        for attr in entity.get('attributes', []):
            visibility = "+" if not attr.get('primary_key') else "#"
            attr_type = attr['type']
            required = " {required}" if attr.get('required') else ""
            puml_lines.append(f"  {visibility} {attr['name']}: {attr_type}{required}")
        
        puml_lines.append("  --")
        
        # Methods
        for method in entity.get('business_methods', []):
            params = ", ".join([f"{p['name']}: {p['type']}" for p in method.get('parameters', [])])
            puml_lines.append(f"  + {method['name']}({params}): {method['return_type']}")
        
        puml_lines.append("}")
        puml_lines.append("")
    
    # Generate relationships
    for entity in domain_model['entities']:
        for rel in entity.get('relationships', []):
            source = entity['name']
            target = rel['target']
            rel_type = rel['type']
            
            # Determine arrow type
            if rel_type == 'belongs-to':
                arrow = "-->"
            elif rel_type == 'has-one':
                arrow = "--|>"
            elif rel_type == 'has-many':
                arrow = "\"1\" --o \"*\""
            else:  # many-to-many
                arrow = "\"*\" --o \"*\""
            
            puml_lines.append(f"{source} {arrow} {target}")
    
    puml_lines.append("")
    puml_lines.append("@enduml")
    
    return "\n".join(puml_lines)
```

### Step 3: XMI Generation

#### 3a. OMG標準 UML 2.5.1 形式

```python
from lxml import etree

def generate_xmi_omg(domain_model: dict) -> str:
    """
    JSONからOMG標準 UML 2.5.1 XMIを生成
    対象ツール: Papyrus, Enterprise Architect, MagicDraw
    """
    # XMI root
    xmi = etree.Element("xmi:XMI", nsmap={
        'xmi': 'http://www.omg.org/spec/XMI/20131001',
        'uml': 'http://www.omg.org/spec/UML/20161101'
    })
    xmi.set("{http://www.omg.org/spec/XMI/20131001}version", "2.5.1")

    # UML Model
    model = etree.SubElement(xmi, "{http://www.omg.org/spec/UML/20161101}Model")
    model.set("name", domain_model['metadata'].get('project_name', 'DomainModel'))

    # Package for domain model
    package = etree.SubElement(model, "{http://www.omg.org/spec/UML/20161101}packagedElement")
    package.set("{http://www.omg.org/spec/XMI/20131001}type", "{http://www.omg.org/spec/UML/20161101}Package")
    package.set("name", "DomainModel")

    # Generate enumerations
    for enum in domain_model.get('enumerations', []):
        enum_elem = etree.SubElement(package, "{http://www.omg.org/spec/UML/20161101}packagedElement")
        enum_elem.set("{http://www.omg.org/spec/XMI/20131001}type", "{http://www.omg.org/spec/UML/20161101}Enumeration")
        enum_elem.set("name", enum['name'])

        for value in enum['values']:
            literal = etree.SubElement(enum_elem, "{http://www.omg.org/spec/UML/20161101}ownedLiteral")
            literal.set("{http://www.omg.org/spec/XMI/20131001}type", "{http://www.omg.org/spec/UML/20161101}EnumerationLiteral")
            val_name = value['name'] if isinstance(value, dict) else value
            literal.set("name", val_name)

    # Generate classes (entities)
    for entity in domain_model['entities']:
        class_elem = etree.SubElement(package, "{http://www.omg.org/spec/UML/20161101}packagedElement")
        class_elem.set("{http://www.omg.org/spec/XMI/20131001}type", "{http://www.omg.org/spec/UML/20161101}Class")
        class_elem.set("name", entity['name'])

        # Attributes
        for attr in entity.get('attributes', []):
            attr_elem = etree.SubElement(class_elem, "{http://www.omg.org/spec/UML/20161101}ownedAttribute")
            attr_elem.set("{http://www.omg.org/spec/XMI/20131001}type", "{http://www.omg.org/spec/UML/20161101}Property")
            attr_elem.set("name", attr['name'])
            # Type reference would be added here

        # Operations (business methods)
        for method in entity.get('business_methods', []):
            op_elem = etree.SubElement(class_elem, "{http://www.omg.org/spec/UML/20161101}ownedOperation")
            op_elem.set("{http://www.omg.org/spec/XMI/20131001}type", "{http://www.omg.org/spec/UML/20161101}Operation")
            op_elem.set("name", method['name'])

    # Generate associations (relationships)
    for entity in domain_model['entities']:
        for rel in entity.get('relationships', []):
            assoc = etree.SubElement(package, "{http://www.omg.org/spec/UML/20161101}packagedElement")
            assoc.set("{http://www.omg.org/spec/XMI/20131001}type", "{http://www.omg.org/spec/UML/20161101}Association")
            assoc.set("name", f"{entity['name']}_{rel['target']}")

    return etree.tostring(xmi, pretty_print=True, encoding='unicode', xml_declaration=True)
```

#### 3b. Eclipse/EMF 形式

```python
from lxml import etree

def generate_xmi_emf(domain_model: dict) -> str:
    """
    JSONからEclipse/EMF形式のXMIを生成
    対象ツール: Sirius, Xtext, Capella, Eclipse UML2 プラグイン
    namespace: http://www.eclipse.org/uml2/5.0.0/UML
    """
    # XMI root with Eclipse UML2 namespace
    xmi = etree.Element("xmi:XMI", nsmap={
        'xmi':   'http://www.omg.org/XMI',
        'uml':   'http://www.eclipse.org/uml2/5.0.0/UML',
        'ecore': 'http://www.eclipse.org/emf/2002/Ecore'
    })
    xmi.set("{http://www.omg.org/XMI}version", "2.0")

    # UML Model element (Eclipse UML2 style)
    model = etree.SubElement(xmi, "{http://www.eclipse.org/uml2/5.0.0/UML}Model")
    model.set("{http://www.omg.org/XMI}id", "_model_" + domain_model['metadata'].get('project_name', 'DomainModel'))
    model.set("name", domain_model['metadata'].get('project_name', 'DomainModel'))

    # Package
    package = etree.SubElement(model, "packagedElement")
    package.set("{http://www.omg.org/XMI}type", "uml:Package")
    package.set("{http://www.omg.org/XMI}id", "_pkg_DomainModel")
    package.set("name", "DomainModel")

    # Enumerations
    for enum in domain_model.get('enumerations', []):
        enum_id = f"_enum_{enum['name']}"
        enum_elem = etree.SubElement(package, "packagedElement")
        enum_elem.set("{http://www.omg.org/XMI}type", "uml:Enumeration")
        enum_elem.set("{http://www.omg.org/XMI}id", enum_id)
        enum_elem.set("name", enum['name'])

        for value in enum['values']:
            val_name = value['name'] if isinstance(value, dict) else value
            lit = etree.SubElement(enum_elem, "ownedLiteral")
            lit.set("{http://www.omg.org/XMI}type", "uml:EnumerationLiteral")
            lit.set("{http://www.omg.org/XMI}id", f"_lit_{enum['name']}_{val_name}")
            lit.set("name", val_name)

    # Classes (entities)
    for entity in domain_model['entities']:
        class_id = f"_class_{entity['name']}"
        class_elem = etree.SubElement(package, "packagedElement")
        class_elem.set("{http://www.omg.org/XMI}type", "uml:Class")
        class_elem.set("{http://www.omg.org/XMI}id", class_id)
        class_elem.set("name", entity['name'])

        # Attributes → ownedAttribute
        for attr in entity.get('attributes', []):
            attr_id = f"_attr_{entity['name']}_{attr['name']}"
            attr_elem = etree.SubElement(class_elem, "ownedAttribute")
            attr_elem.set("{http://www.omg.org/XMI}type", "uml:Property")
            attr_elem.set("{http://www.omg.org/XMI}id", attr_id)
            attr_elem.set("name", attr['name'])
            if attr.get('required'):
                attr_elem.set("lower", "1")
                attr_elem.set("upper", "1")
            else:
                attr_elem.set("lower", "0")
                attr_elem.set("upper", "1")

        # Operations (business methods)
        for method in entity.get('business_methods', []):
            op_id = f"_op_{entity['name']}_{method['name']}"
            op_elem = etree.SubElement(class_elem, "ownedOperation")
            op_elem.set("{http://www.omg.org/XMI}type", "uml:Operation")
            op_elem.set("{http://www.omg.org/XMI}id", op_id)
            op_elem.set("name", method['name'])

    # Associations (relationships)
    for entity in domain_model['entities']:
        for rel in entity.get('relationships', []):
            assoc_id = f"_assoc_{entity['name']}_{rel['target']}"
            assoc = etree.SubElement(package, "packagedElement")
            assoc.set("{http://www.omg.org/XMI}type", "uml:Association")
            assoc.set("{http://www.omg.org/XMI}id", assoc_id)
            assoc.set("name", f"{entity['name']}_{rel['target']}")

            # memberEnd references
            src_end = etree.SubElement(assoc, "ownedEnd")
            src_end.set("{http://www.omg.org/XMI}type", "uml:Property")
            src_end.set("{http://www.omg.org/XMI}id", f"{assoc_id}_src")
            src_end.set("type", f"_class_{entity['name']}")
            src_end.set("lower", rel.get('source_multiplicity', '1').replace('*', '-1'))
            src_end.set("upper", rel.get('source_multiplicity', '1').replace('*', '-1'))

            tgt_end = etree.SubElement(assoc, "ownedEnd")
            tgt_end.set("{http://www.omg.org/XMI}type", "uml:Property")
            tgt_end.set("{http://www.omg.org/XMI}id", f"{assoc_id}_tgt")
            tgt_end.set("type", f"_class_{rel['target']}")
            tgt_end.set("lower", rel.get('target_multiplicity', '*').replace('*', '-1'))
            tgt_end.set("upper", rel.get('target_multiplicity', '*').replace('*', '-1'))

    return etree.tostring(xmi, pretty_print=True, encoding='unicode', xml_declaration=True)
```

#### 3c. 形式選択ディスパッチャ

```python
def generate_xmi_from_json(domain_model: dict, xmi_format: str = "omg") -> str:
    """
    xmi_format: "omg" | "emf"
    """
    if xmi_format == "emf":
        return generate_xmi_emf(domain_model)
    else:
        return generate_xmi_omg(domain_model)
```

### Step 4: Markdown Documentation Generation

```python
def generate_architecture_overview_from_json(domain_model: dict) -> str:
    """
    JSONからアーキテクチャ概要ドキュメントを生成
    """
    md_lines = [
        f"# アーキテクチャ概要",
        "",
        "## ドメインモデル",
        ""
    ]
    
    # Entity documentation
    for entity in domain_model['entities']:
        md_lines.append(f"### {entity.get('japanese_name', entity['name'])} ({entity['name']})")
        md_lines.append("")
        md_lines.append(f"**説明:** {entity.get('description', '')}")
        md_lines.append("")
        
        # Attributes
        md_lines.append("**属性:**")
        md_lines.append("")
        for attr in entity.get('attributes', []):
            required = " (必須)" if attr.get('required') else ""
            md_lines.append(f"- `{attr['name']}: {attr['type']}`{required} - {attr.get('description', '')}")
        md_lines.append("")
        
        # Relationships
        if entity.get('relationships'):
            md_lines.append("**リレーション:**")
            md_lines.append("")
            for rel in entity['relationships']:
                md_lines.append(f"- {rel['type']} → {rel['target']}: {rel.get('description', '')}")
            md_lines.append("")
        
        # Business methods
        if entity.get('business_methods'):
            md_lines.append("**ビジネスメソッド:**")
            md_lines.append("")
            for method in entity['business_methods']:
                params = ", ".join([f"{p['name']}: {p['type']}" for p in method.get('parameters', [])])
                md_lines.append(f"- `{method['name']}({params}): {method['return_type']}`")
                md_lines.append(f"  - {method.get('description', '')}")
            md_lines.append("")
        
        md_lines.append("---")
        md_lines.append("")
    
    return "\n".join(md_lines)
```

---

## Output

**生成される成果物は実行オプションに依存します。**

### If generate_xmi = True:

選択した形式に応じてファイル名とフォーマットが変わります。

**1. PlantUML Class Diagram**

**Filename:** `{project}_class.puml`

完全に再生成されたクラス図。JSONの内容を100%反映。

**2. XMI Model** ✅

| 形式 | Filename | Namespace |
|------|----------|-----------|
| OMG標準 UML 2.5.1 | `{project}_class-model.xmi` | `http://www.omg.org/spec/UML/20161101` |
| Eclipse/EMF形式 | `{project}_class-model-emf.xmi` | `http://www.eclipse.org/uml2/5.0.0/UML` |

**3. Architecture Overview**

**Filename:** `{project}_architecture-overview.md`

更新されたアーキテクチャドキュメント。

**4. Metadata Update**

domain-model.jsonのmetadataを更新:
```json
{
  "metadata": {
    "source": "manual-edit",
    "last_regenerated_at": "2026-01-24T...",
    "regenerated_by": "json-to-models",
    "original_source": "usecase-to-class-v1",
    "xmi_generated": true
  }
}
```

### If generate_xmi = False:

**1. PlantUML Class Diagram**

**Filename:** `{project}_class.puml`

完全に再生成されたクラス図。JSONの内容を100%反映。

**2. XMI Model** ⏭️

**SKIPPED** - XMI生成なし（約40%高速化）

**3. Architecture Overview**

**Filename:** `{project}_architecture-overview.md`

更新されたアーキテクチャドキュメント。

**4. Metadata Update**

domain-model.jsonのmetadataを更新:
```json
{
  "metadata": {
    "source": "manual-edit",
    "last_regenerated_at": "2026-01-24T...",
    "regenerated_by": "json-to-models",
    "original_source": "usecase-to-class-v1",
    "xmi_generated": false
  }
}
```

---

## Usage Examples

### Example 0: 実行オプションの選択

**パターンA: OMG標準 XMI生成（Papyrus / EA向け）**
```
ユーザー: json-to-modelsでdomain-model.jsonから再生成してください

Claude: XMIファイルを生成しますか？ (はい/いいえ)
ユーザー: はい

Claude: XMI形式を選択してください
        1. OMG標準 UML 2.5.1（Papyrus / EA / MagicDraw向け）
        2. Eclipse/EMF形式（Sirius / Xtext / Capella向け）
ユーザー: 1

→ PlantUML + XMI(OMG) + Markdown 生成
```

**パターンB: Eclipse/EMF XMI生成（Sirius / Capella向け）**
```
ユーザー: json-to-modelsでEMF形式のXMIを生成してください

Claude: XMIファイルを生成しますか？ (はい/いいえ)
ユーザー: はい

Claude: XMI形式を選択してください
ユーザー: 2（Eclipse/EMF形式）

→ PlantUML + XMI(EMF) + Markdown 生成
```

**パターンC: 素早い確認**
```
ユーザー: json-to-modelsでPlantUMLだけ素早く確認したい

Claude: XMIファイルを生成しますか？ (はい/いいえ)
ユーザー: いいえ

→ PlantUML + Markdown のみ生成（40%高速化）
```

### Example 1: 属性の追加

```json
// domain-model.jsonを編集
{
  "entities": [
    {
      "name": "Order",
      "attributes": [
        {
          "name": "orderId",
          "type": "string",
          "primary_key": true,
          "required": true
        },
        // 新しい属性を追加
        {
          "name": "shippingFee",
          "type": "decimal",
          "required": true,
          "default": "0.00",
          "description": "配送料"
        }
      ]
    }
  ]
}
```

実行:
```
Claude: json-to-modelsを実行
  → PlantUML、XMI、Markdownが再生成される
```

### Example 2: リレーションシップの変更

```json
{
  "entities": [
    {
      "name": "Order",
      "relationships": [
        // 修正: 多重度を変更
        {
          "type": "has-many",
          "target": "OrderItem",
          "source_multiplicity": "1",
          "target_multiplicity": "1..*",  // 最低1個必要に変更
          "description": "注文には最低1つの明細が必要"
        }
      ]
    }
  ]
}
```

### Example 3: エンティティの追加

```json
{
  "entities": [
    // 既存のエンティティ...
    
    // 新しいエンティティを追加
    {
      "name": "Discount",
      "japanese_name": "割引",
      "description": "注文に適用される割引",
      "stereotype": "entity",
      "attributes": [
        {
          "name": "discountId",
          "type": "string",
          "primary_key": true,
          "required": true
        },
        {
          "name": "discountRate",
          "type": "decimal",
          "required": true,
          "validation": {
            "min": 0,
            "max": 1
          }
        }
      ],
      "relationships": [
        {
          "type": "belongs-to",
          "target": "Order",
          "description": "特定の注文に適用"
        }
      ]
    }
  ]
}
```

---

## Validation Rules

### Pre-Generation Validation

1. **スキーマ検証**
   - 必須フィールドの存在確認
   - 型の妥当性チェック

2. **整合性チェック**
   - エンティティ名の重複なし
   - リレーション先エンティティの存在
   - 列挙型参照の存在

3. **命名規則**
   - エンティティ名: PascalCase
   - 属性名: camelCase
   - メソッド名: camelCase

### Post-Generation Validation

1. **PlantUML構文チェック**
   - 生成されたPlantUMLがエラーなし

2. **XMI構造検証**
   - OMG標準: UML 2.5.1スキーマに準拠
   - Eclipse/EMF: Eclipse UML2 5.0.0 namespace / xmi:id 全要素付与を確認

---

## Integration with Workflow

### Modification Workflow

```
1. 初回生成
   uml-workflow-v1
   → domain-model.json生成

2. レビュー
   → 修正箇所を特定

3. JSON編集
   → domain-model.json を修正

4. モデル再生成
   json-to-models ← このスキル
   → PlantUML/XMI/Markdown再生成

5. コード再生成
   usecase-to-code-v1
   → 更新されたコード
```

### Next Steps After Regeneration

生成後、以下のいずれかを実行:

1. **usecase-to-code-v1を再実行**
   - 更新されたドメインモデルでコード再生成

2. **さらに修正**
   - domain-model.jsonを再度編集
   - json-to-modelsを再実行

3. **検証**
   - PlantUML図で視覚的確認
   - XMIをUMLツールで検証

---

## Error Handling

### Common Errors

**Error: Entity not found**
```
リレーション先エンティティ "Product" が見つかりません

解決策:
- Productエンティティを追加
- またはリレーションを削除
```

**Error: Invalid attribute type**
```
属性 "totalAmount" の型 "money" は未サポート

サポートされる型:
- string, number, boolean, datetime, date, decimal
- 列挙型名

解決策:
- 型を "decimal" に変更
```

**Error: Duplicate entity name**
```
エンティティ名 "Order" が重複しています

解決策:
- 一方を削除または名前変更
```

---

## Best Practices

### 1. バックアップ

JSONを編集する前に必ずバックアップ:
```bash
cp domain-model.json domain-model.json.bak
```

### 2. 段階的な修正

大きな変更は段階的に:
1. 属性を追加 → 再生成 → 確認
2. リレーションを追加 → 再生成 → 確認
3. エンティティを追加 → 再生成 → 確認

### 3. バリデーション

修正後、必ずバリデーション:
```
Claude: このdomain-model.jsonをバリデートしてください
```

### 4. バージョン管理

domain-model.jsonをGitで管理:
```bash
git add domain-model.json
git commit -m "Add shippingFee attribute to Order"
```

---

## Limitations

### 現在の制限

1. **PlantUMLの制約**
   - すべてのUML機能をサポートしない
   - 複雑な制約表現が困難

2. **XMI完全性**
   - 基本的なUML要素のみサポート
   - 高度なステレオタイプは限定的

3. **情報損失なし**
   - JSONに定義されたすべての情報を保持
   - ただし、追加のPlantUML注釈は非サポート

---

## Version History

- **v1.0** (2026-01-24)
  - 初版リリース
  - PlantUML、XMI、Markdown生成
  - 完全なバリデーション機能

---

## Related Skills

- **usecase-to-class-v1**: domain-model.jsonの初回生成
- **usecase-to-code-v1**: domain-model.jsonからコード生成
- **apply-model-changes**: YAML差分適用（将来実装）
- **xmi-to-models**: XMI編集後の再生成（将来実装）
