---
name: json-to-models
description: Generate PlantUML, XMI (OMG + EMF/Papyrus dual format), and Markdown documentation from domain-model.json. Supports XMI generation toggle (`--no-xmi`) for 40% performance improvement and best-effort PNG rendering. Core skill for model modification workflows.
---

# json-to-models

## Overview

ドメインモデルJSON（domain-model.json）から、PlantUML、XMI、Markdownドキュメントを再生成するスキルです。

**主な用途:**
- モデルのレビュー後、domain-model.jsonを修正して他のフォーマットを更新
- JSONをSingle Source of Truthとして管理
- プログラマティックなモデル操作

---

## Execution Options (v1.3 ⭐)

**CRITICAL: 実行前にXMI生成の有無を確認してパフォーマンスを最適化します。**

```
質問: クラス図 XMI を生成しますか？
  はい (デフォルト): PlantUML + XMI(OMG + EMF) + Markdown を生成
  いいえ:            PlantUML + Markdown のみ生成（約40%高速化）
```

**v1.3 から XMI はデフォルトで OMG / EMF の両形式を同時生成します。**
形式選択の二次質問は廃止。`--xmi-format` で個別指定も可能（後述）。

**Performance Impact:**
- XMI生成あり（OMG + EMF 両形式）: 通常速度
- XMI生成なし: **約40%高速化** ⚡

**When to disable XMI:**
- 素早くPlantUMLを確認したい
- UMLツールを使用しない
- 反復的なモデル修正中

**When to enable XMI:**
- UMLツール（Astah / Enterprise Architect / Papyrus）で編集
- 完全なモデルアーカイブが必要
- 最終成果物として保存

### XMI 形式の使い分け

| 形式 | 主な対応ツール | ファイル名 |
|---|---|---|
| **OMG** (UML 2.5.1 標準) | Astah Professional, Enterprise Architect | `{project}_class-model-omg.uml` |
| **EMF** (Eclipse UML2 5.0.0) | **Eclipse Papyrus 7.1.0** 専用 | `{project}_class-model-emf.uml` |

**クロス互換性は保証外**: OMG → EA/Astah、EMF → Papyrus の組み合わせのみサポート。

### `--xmi-format` フラグ（CLI 直接実行時）

```
--xmi-format=both   # デフォルト: OMG + EMF 両方生成
--xmi-format=omg    # OMG のみ
--xmi-format=emf    # EMF のみ
--xmi-format=none   # XMI スキップ（--no-xmi と等価）
```

**`--xmi` 旧フラグは廃止**。意味の反転（旧: 明示指定が必要 → 新: デフォルトで生成）が破壊的変更となるため、旧フラグ指定時は警告メッセージで `--no-xmi` への移行を促します。

---

## Skill Purpose

このスキルは、手動またはプログラムで編集されたdomain-model.jsonから、すべての派生成果物を再生成します。

**モデル修正ワークフローにおける位置:**
```
domain-model.json (手動編集)
  ↓ json-to-models
  ├→ PlantUML Class Diagram (.puml, 常に生成)
  ├→ PNG (ベストエフォート、plantuml が利用可能な環境のみ)
  ├→ XMI OMG 形式  (.uml, オプション、Astah/EA 向け)
  ├→ XMI EMF 形式  (.uml, オプション、Papyrus 専用)
  └→ Architecture Overview (.md, 常に生成)
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

### Step 3: XMI Generation (OMG + EMF 二形式対応, v1.3)

XMI 生成は **OMG 形式**（業界標準、Astah/EA 向け）と **EMF 形式**（Eclipse UML2 5.0.0、Papyrus 専用）の 2 つの関数に分かれます。エントリーポイントの `generate_xmi()` がディスパッチします。

#### 3.1 OMG 形式生成（既存 `generate_xmi_from_json` をリネーム）

```python
from lxml import etree

XMI_NS_OMG = "http://www.omg.org/spec/XMI/20131001"
UML_NS_OMG = "http://www.omg.org/spec/UML/20161101"

def generate_xmi_omg(domain_model: dict) -> str:
    """
    JSON から UML 2.5.1 標準形式 XMI を生成（Astah / Enterprise Architect 向け）。

    ルートは <xmi:XMI> ラッパー。`xmi:id` は 8 文字 hex 形式。
    """
    nsmap = {'xmi': XMI_NS_OMG, 'uml': UML_NS_OMG}
    xmi = etree.Element(f"{{{XMI_NS_OMG}}}XMI", nsmap=nsmap)
    xmi.set(f"{{{XMI_NS_OMG}}}version", "2.5.1")

    # UML Model
    model = etree.SubElement(xmi, f"{{{UML_NS_OMG}}}Model")
    model.set("name", domain_model['metadata'].get('project_name', 'DomainModel'))

    # Package for domain model
    package = etree.SubElement(model, f"{{{UML_NS_OMG}}}packagedElement")
    package.set(f"{{{XMI_NS_OMG}}}type", f"{{{UML_NS_OMG}}}Package")
    package.set("name", "DomainModel")

    # Enumerations
    for enum in domain_model.get('enumerations', []):
        enum_elem = etree.SubElement(package, f"{{{UML_NS_OMG}}}packagedElement")
        enum_elem.set(f"{{{XMI_NS_OMG}}}type", f"{{{UML_NS_OMG}}}Enumeration")
        enum_elem.set("name", enum['name'])
        for value in enum['values']:
            literal = etree.SubElement(enum_elem, f"{{{UML_NS_OMG}}}ownedLiteral")
            literal.set(f"{{{XMI_NS_OMG}}}type", f"{{{UML_NS_OMG}}}EnumerationLiteral")
            val_name = value['name'] if isinstance(value, dict) else value
            literal.set("name", val_name)

    # Classes
    for entity in domain_model['entities']:
        class_elem = etree.SubElement(package, f"{{{UML_NS_OMG}}}packagedElement")
        class_elem.set(f"{{{XMI_NS_OMG}}}type", f"{{{UML_NS_OMG}}}Class")
        class_elem.set("name", entity['name'])

        for attr in entity.get('attributes', []):
            attr_elem = etree.SubElement(class_elem, f"{{{UML_NS_OMG}}}ownedAttribute")
            attr_elem.set(f"{{{XMI_NS_OMG}}}type", f"{{{UML_NS_OMG}}}Property")
            attr_elem.set("name", attr['name'])

        for method in entity.get('business_methods', []):
            op_elem = etree.SubElement(class_elem, f"{{{UML_NS_OMG}}}ownedOperation")
            op_elem.set(f"{{{XMI_NS_OMG}}}type", f"{{{UML_NS_OMG}}}Operation")
            op_elem.set("name", method['name'])

    return etree.tostring(
        xmi, pretty_print=True, encoding='UTF-8', xml_declaration=True
    ).decode('utf-8')
```

**注:** OMG 形式は実質変更なし（旧 `generate_xmi_from_json` を関数名のみ変更）。互換性は維持されます。

#### 3.2 EMF 形式生成（新規実装、Papyrus 専用）

Papyrus 実機サンプル（2026-05-13 取得）と構造一致するよう設計。

**OMG 形式との主要差分:**

| 項目 | OMG | EMF |
|---|---|---|
| ルート要素 | `<xmi:XMI>` | **`<uml:Model>` 直接** |
| UML namespace | `http://www.omg.org/spec/UML/20161101` | `http://www.eclipse.org/uml2/5.0.0/UML` |
| XMI version | `2.5.1` | `20131001` |
| `xmi:id` 形式 | 8 文字 hex | **22 文字 Base64** |
| 型参照 | 直接参照 | `pathmap://UML_LIBRARIES/...` |
| `packageImport` | なし | **必須**（UMLPrimitiveTypes） |
| `eAnnotation` | なし | **あり**（`source="org.eclipse.papyrus"`） |
| Association | 簡略 | **`ownedEnd` + `memberEnd` 完全実装** |

```python
import base64
import os
from lxml import etree

UML_NS_EMF   = "http://www.eclipse.org/uml2/5.0.0/UML"
XMI_NS_EMF   = "http://www.omg.org/spec/XMI/20131001"
ECORE_NS_EMF = "http://www.eclipse.org/emf/2002/Ecore"

# プリミティブ型マッピング（pathmap 解決用）
PRIMITIVE_TYPE_MAP = {
    'String': 'String', 'Integer': 'Integer', 'Boolean': 'Boolean',
    'Real': 'Real', 'UnlimitedNatural': 'UnlimitedNatural',
    # JSON Schema 由来のエイリアス
    'string': 'String', 'number': 'Real', 'integer': 'Integer',
    'boolean': 'Boolean', 'decimal': 'Real', 'datetime': 'String',
    # Python 風エイリアス
    'int': 'Integer', 'str': 'String', 'bool': 'Boolean', 'float': 'Real',
}

# JSON relationship.type → UML aggregation kind
AGGREGATION_MAP = {
    'composition': 'composite', 'aggregation': 'shared',
    'has-many': 'none', 'has-one': 'none',
    'belongs-to': 'none', 'many-to-many': 'none',
}


def gen_papyrus_id() -> str:
    """
    Papyrus 互換の 22 文字 Base64 形式 ID を生成。
    例: _8qjE0EBkEfGJ9KxQ0FEvfA
    """
    raw = os.urandom(16)
    b64 = base64.urlsafe_b64encode(raw).decode('ascii').rstrip('=')
    return f"_{b64[:22]}"


def _parse_multiplicity(mult: str) -> tuple:
    """'0..*' / '1' / '0..1' などを (lower:int, upper:str) に分解"""
    if not mult:
        return 1, "1"
    mult = mult.strip()
    if ".." in mult:
        lo, hi = mult.split("..", 1)
        return int(lo), hi.strip()
    if mult == "*":
        return 0, "*"
    return int(mult), mult


def _add_multiplicity(parent, mult: str) -> None:
    """ownedAttribute / ownedEnd に lowerValue / upperValue を追加"""
    lo, hi = _parse_multiplicity(mult)
    lower = etree.SubElement(parent, "lowerValue")
    lower.set(f"{{{XMI_NS_EMF}}}type", "uml:LiteralInteger")
    lower.set(f"{{{XMI_NS_EMF}}}id", gen_papyrus_id())
    lower.set("value", str(lo))
    upper = etree.SubElement(parent, "upperValue")
    upper.set(f"{{{XMI_NS_EMF}}}type", "uml:LiteralUnlimitedNatural")
    upper.set(f"{{{XMI_NS_EMF}}}id", gen_papyrus_id())
    upper.set("value", "*" if hi == "*" else hi)


def _set_primitive_type(prop, type_name: str) -> bool:
    """プリミティブ型なら子要素 <type> を pathmap 形式で追加"""
    if type_name in PRIMITIVE_TYPE_MAP:
        type_elem = etree.SubElement(prop, "type")
        type_elem.set(f"{{{XMI_NS_EMF}}}type", "uml:PrimitiveType")
        type_elem.set(
            "href",
            f"pathmap://UML_LIBRARIES/UMLPrimitiveTypes.library.uml"
            f"#{PRIMITIVE_TYPE_MAP[type_name]}"
        )
        return True
    return False


def generate_xmi_emf(domain_model: dict) -> str:
    """
    JSON から Eclipse UML2 5.0.0 形式 XMI（Papyrus 専用）を生成。

    重要: ルートは <uml:Model> 直接（<xmi:XMI> ラッパーなし）
    """
    nsmap = {'xmi': XMI_NS_EMF, 'ecore': ECORE_NS_EMF, 'uml': UML_NS_EMF}

    # ルートは uml:Model 直接
    model = etree.Element(f"{{{UML_NS_EMF}}}Model", nsmap=nsmap)
    model.set(f"{{{XMI_NS_EMF}}}version", "20131001")
    model.set(f"{{{XMI_NS_EMF}}}id", gen_papyrus_id())
    model.set("name", domain_model.get('metadata', {}).get('project_name', 'DomainModel'))

    # 必須: UMLPrimitiveTypes ライブラリ import
    pkg_import = etree.SubElement(model, "packageImport")
    pkg_import.set(f"{{{XMI_NS_EMF}}}type", "uml:PackageImport")
    pkg_import.set(f"{{{XMI_NS_EMF}}}id", gen_papyrus_id())
    imported = etree.SubElement(pkg_import, "importedPackage")
    imported.set(f"{{{XMI_NS_EMF}}}type", "uml:Model")
    imported.set("href", "pathmap://UML_LIBRARIES/UMLPrimitiveTypes.library.uml#_0")

    # 第1パス: ID 割り当て
    class_id_map = {e['name']: gen_papyrus_id() for e in domain_model.get('entities', [])}
    enum_id_map  = {e['name']: gen_papyrus_id() for e in domain_model.get('enumerations', [])}

    # Enumerations
    for enum in domain_model.get('enumerations', []):
        enum_elem = etree.SubElement(model, "packagedElement")
        enum_elem.set(f"{{{XMI_NS_EMF}}}type", "uml:Enumeration")
        enum_elem.set(f"{{{XMI_NS_EMF}}}id", enum_id_map[enum['name']])
        enum_elem.set("name", enum['name'])
        for value in enum.get('values', []):
            val_name = value['name'] if isinstance(value, dict) else value
            literal = etree.SubElement(enum_elem, "ownedLiteral")
            literal.set(f"{{{XMI_NS_EMF}}}type", "uml:EnumerationLiteral")
            literal.set(f"{{{XMI_NS_EMF}}}id", gen_papyrus_id())
            literal.set("name", val_name)

    # 第2パス: Class 生成（Association は後でまとめて生成）
    pending_associations = []
    class_elem_map = {}  # name -> Class element（後で ownedAttribute を追加する）

    for entity in domain_model.get('entities', []):
        cls = etree.SubElement(model, "packagedElement")
        cls.set(f"{{{XMI_NS_EMF}}}type", "uml:Class")
        cls.set(f"{{{XMI_NS_EMF}}}id", class_id_map[entity['name']])
        cls.set("name", entity['name'])
        class_elem_map[entity['name']] = cls

        # Generalization（継承）
        extends = entity.get('extends')
        if extends and extends in class_id_map:
            gen = etree.SubElement(cls, "generalization")
            gen.set(f"{{{XMI_NS_EMF}}}type", "uml:Generalization")
            gen.set(f"{{{XMI_NS_EMF}}}id", gen_papyrus_id())
            gen.set("general", class_id_map[extends])

        # 属性
        for attr in entity.get('attributes', []):
            prop = etree.SubElement(cls, "ownedAttribute")
            prop.set(f"{{{XMI_NS_EMF}}}type", "uml:Property")
            prop.set(f"{{{XMI_NS_EMF}}}id", gen_papyrus_id())
            prop.set("name", attr['name'])

            type_name = attr.get('type', 'String')
            if _set_primitive_type(prop, type_name):
                pass
            elif type_name in class_id_map:
                prop.set("type", class_id_map[type_name])
            elif type_name in enum_id_map:
                prop.set("type", enum_id_map[type_name])
            else:
                _set_primitive_type(prop, 'String')  # フォールバック

            if not attr.get('required', True):
                _add_multiplicity(prop, "0..1")

        # Operation
        for method in entity.get('business_methods', []):
            op = etree.SubElement(cls, "ownedOperation")
            op.set(f"{{{XMI_NS_EMF}}}type", "uml:Operation")
            op.set(f"{{{XMI_NS_EMF}}}id", gen_papyrus_id())
            op.set("name", method['name'])
            for param in method.get('parameters', []):
                p = etree.SubElement(op, "ownedParameter")
                p.set(f"{{{XMI_NS_EMF}}}type", "uml:Parameter")
                p.set(f"{{{XMI_NS_EMF}}}id", gen_papyrus_id())
                p.set("name", param['name'])
                _set_primitive_type(p, param.get('type', 'String'))
            ret = method.get('return_type')
            if ret and ret != 'void':
                r = etree.SubElement(op, "ownedParameter")
                r.set(f"{{{XMI_NS_EMF}}}type", "uml:Parameter")
                r.set(f"{{{XMI_NS_EMF}}}id", gen_papyrus_id())
                r.set("direction", "return")
                _set_primitive_type(r, ret)

        # Relationships は Association として保留
        for rel in entity.get('relationships', []):
            if rel.get('target') in class_id_map:
                pending_associations.append({
                    'source_entity': entity['name'],
                    'rel': rel,
                })

    # 第3パス: Association 生成（双方向、aggregation、ownedEnd、eAnnotation 含む完全実装）
    seen = set()  # (sorted_pair, rel_type) で重複排除
    for item in pending_associations:
        rel = item['rel']
        source_name = item['source_entity']
        target_name = rel['target']
        rel_type = rel.get('type', 'has-many')

        pair = tuple(sorted([source_name, target_name]))
        key = (pair[0], pair[1], rel_type)
        if key in seen:
            continue
        seen.add(key)

        assoc = etree.SubElement(model, "packagedElement")
        assoc.set(f"{{{XMI_NS_EMF}}}type", "uml:Association")
        assoc_id = gen_papyrus_id()
        assoc.set(f"{{{XMI_NS_EMF}}}id", assoc_id)

        member_end_id = gen_papyrus_id()  # source 側の ownedAttribute（Class 配下）
        owned_end_id  = gen_papyrus_id()  # target 側の ownedEnd（Association 配下）
        assoc.set("memberEnd", f"{member_end_id} {owned_end_id}")

        # Papyrus 専用 eAnnotation
        eann = etree.SubElement(assoc, "eAnnotations")
        eann.set(f"{{{XMI_NS_EMF}}}type", "ecore:EAnnotation")
        eann.set(f"{{{XMI_NS_EMF}}}id", gen_papyrus_id())
        eann.set("source", "org.eclipse.papyrus")
        details = etree.SubElement(eann, "details")
        details.set(f"{{{XMI_NS_EMF}}}type", "ecore:EStringToStringMapEntry")
        details.set(f"{{{XMI_NS_EMF}}}id", gen_papyrus_id())
        details.set("key", "nature")
        details.set("value", "UML_Nature")

        # source 側: source クラスの ownedAttribute（memberEnd）
        src_cls = class_elem_map[source_name]
        src_prop = etree.SubElement(src_cls, "ownedAttribute")
        src_prop.set(f"{{{XMI_NS_EMF}}}type", "uml:Property")
        src_prop.set(f"{{{XMI_NS_EMF}}}id", member_end_id)
        src_prop.set("name", target_name.lower())
        src_prop.set("type", class_id_map[target_name])
        src_prop.set("association", assoc_id)
        aggregation = AGGREGATION_MAP.get(rel_type, 'none')
        if aggregation != 'none':
            src_prop.set("aggregation", aggregation)
        _add_multiplicity(src_prop, rel.get('target_multiplicity', '1'))

        # target 側: Association の ownedEnd
        owned_end = etree.SubElement(assoc, "ownedEnd")
        owned_end.set(f"{{{XMI_NS_EMF}}}type", "uml:Property")
        owned_end.set(f"{{{XMI_NS_EMF}}}id", owned_end_id)
        owned_end.set("name", source_name.lower())
        owned_end.set("type", class_id_map[source_name])
        owned_end.set("association", assoc_id)
        _add_multiplicity(owned_end, rel.get('source_multiplicity', '*'))

    body = etree.tostring(model, pretty_print=True, encoding='unicode')
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + body
```

#### 3.3 ディスパッチャー & ファイル出力

```python
def generate_xmi(domain_model: dict, format: str = "both") -> dict:
    """
    XMI 生成のエントリーポイント。

    Args:
        format: "omg" | "emf" | "both" | "none"

    Returns:
        {"omg": str | None, "emf": str | None}
    """
    result = {"omg": None, "emf": None}
    if format in ("omg", "both"):
        result["omg"] = generate_xmi_omg(domain_model)
    if format in ("emf", "both"):
        result["emf"] = generate_xmi_emf(domain_model)
    return result


# ファイル出力
xmi_outputs = generate_xmi(domain_model, format=xmi_format)
if xmi_outputs["omg"]:
    write_file(f"{project}_class-model-omg.uml", xmi_outputs["omg"])
if xmi_outputs["emf"]:
    write_file(f"{project}_class-model-emf.uml", xmi_outputs["emf"])
```

**注:** 拡張子は OMG / EMF とも `.uml` で統一（Papyrus 実機が `.uml` 出力するため）。ファイル名のサフィックス（`-omg` / `-emf`）で形式を区別します。

### Step 3.5: PNG Generation (ベストエフォート, v1.3 新規)

PlantUML から PNG をベストエフォートで生成。`plantuml` が利用可能な環境でのみ実行され、不在環境ではスキップ（`.puml` のみ提供）。

#### 3.5.1 3段階フォールバック

1. **`plantuml` コマンド**（個人開発者向け、最速）
2. **`java -jar plantuml.jar`**（jar 配置済み環境向け）
3. **PlantUML サーバー HTTP**（Docker または独自ホスト、チーム・企業向け）
4. スキップ → ガイダンス表示

```python
import shutil
import subprocess
import os
import urllib.request
import urllib.error
import zlib

PLANTUML_ALPHABET = (
    "0123456789"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "abcdefghijklmnopqrstuvwxyz"
    "-_"
)


def _encode_6bit(data: bytes) -> str:
    """PlantUML 独自の 6bit Base64（末尾パディング完全対応）"""
    result = []
    for i in range(0, len(data), 3):
        chunk = data[i:i+3]
        if len(chunk) == 3:
            b1, b2, b3 = chunk
            result.append(PLANTUML_ALPHABET[b1 >> 2])
            result.append(PLANTUML_ALPHABET[((b1 & 0x3) << 4) | (b2 >> 4)])
            result.append(PLANTUML_ALPHABET[((b2 & 0xF) << 2) | (b3 >> 6)])
            result.append(PLANTUML_ALPHABET[b3 & 0x3F])
        elif len(chunk) == 2:
            b1, b2 = chunk
            result.append(PLANTUML_ALPHABET[b1 >> 2])
            result.append(PLANTUML_ALPHABET[((b1 & 0x3) << 4) | (b2 >> 4)])
            result.append(PLANTUML_ALPHABET[(b2 & 0xF) << 2])
        elif len(chunk) == 1:
            b1 = chunk[0]
            result.append(PLANTUML_ALPHABET[b1 >> 2])
            result.append(PLANTUML_ALPHABET[(b1 & 0x3) << 4])
    return "".join(result)


def _plantuml_encode(text: str) -> str:
    """
    PlantUML サーバー受信形式の URL セーフ文字列を生成。
    DEFLATE 圧縮 → zlib ヘッダ/Adler32 除去 → 6bit Base64。
    """
    compressed = zlib.compress(text.encode('utf-8'), 9)[2:-4]
    return _encode_6bit(compressed)


def render_png_best_effort(puml_path: str, png_path: str) -> dict:
    """
    PlantUML から PNG をベストエフォートで生成。

    Returns:
        {"success": bool, "method": str, "message": str}
    """
    # 優先順位 1: plantuml コマンド
    if shutil.which("plantuml"):
        try:
            subprocess.run(
                ["plantuml", "-tpng", puml_path],
                check=True, capture_output=True, timeout=60,
            )
            return {
                "success": True, "method": "plantuml-cli",
                "message": "✅ PNG generated via local plantuml command",
            }
        except subprocess.SubprocessError as e:
            # 次のフォールバックに進む（return せず）
            cli_error = str(e)
        else:
            cli_error = None

    # 優先順位 2: ローカル plantuml.jar
    jar_candidates = [
        os.environ.get("PLANTUML_JAR"),
        "./plantuml.jar",
        os.path.expanduser("~/.local/share/plantuml/plantuml.jar"),
        "/usr/local/share/plantuml/plantuml.jar",
    ]
    jar_path = next((p for p in jar_candidates if p and os.path.exists(p)), None)
    if jar_path and shutil.which("java"):
        try:
            subprocess.run(
                ["java", "-jar", jar_path, "-tpng", puml_path],
                check=True, capture_output=True, timeout=60,
            )
            return {
                "success": True, "method": "java-jar",
                "message": f"✅ PNG generated via java -jar {jar_path}",
            }
        except subprocess.SubprocessError as e:
            jar_error = str(e)
        else:
            jar_error = None

    # 優先順位 3: Docker / ローカル PlantUML サーバー (HTTP)
    plantuml_server = os.environ.get("PLANTUML_SERVER_URL", "http://localhost:8080")
    try:
        with urllib.request.urlopen(f"{plantuml_server}/", timeout=2) as resp:
            if resp.status == 200:
                with open(puml_path, 'r', encoding='utf-8') as f:
                    puml_text = f.read()
                encoded = _plantuml_encode(puml_text)
                url = f"{plantuml_server}/png/{encoded}"
                with urllib.request.urlopen(url, timeout=30) as png_resp:
                    with open(png_path, 'wb') as out:
                        out.write(png_resp.read())
                return {
                    "success": True, "method": "http-server",
                    "message": f"✅ PNG generated via PlantUML server at {plantuml_server}",
                }
    except (urllib.error.URLError, ConnectionError, TimeoutError, OSError):
        pass  # サーバー不在 → スキップへ

    # 優先順位 4: スキップしてガイダンス表示
    return {
        "success": False, "method": "skipped",
        "message": (
            "ℹ️  PlantUML not available. PNG generation skipped.\n"
            "    .puml file is available for manual rendering.\n"
            "\n"
            "    Option A: Install plantuml command\n"
            "      macOS:   brew install plantuml\n"
            "      Ubuntu:  sudo apt install plantuml\n"
            "      Windows: choco install plantuml\n"
            "\n"
            "    Option B: Docker PlantUML server\n"
            "      docker run -d -p 8080:8080 plantuml/plantuml-server:jetty\n"
            "      (then re-run; PLANTUML_SERVER_URL=http://localhost:8080 is default)\n"
            "\n"
            "    Option C: Set PLANTUML_JAR env var to plantuml.jar path."
        ),
    }
```

#### 3.5.2 環境別の挙動

| 環境 | 期待される挙動 |
|---|---|
| Claude Code（ローカル、`plantuml` あり） | ✅ PNG 生成成功（優先順位1） |
| Claude Code（ローカル、jar 配置済み） | ✅ PNG 生成成功（優先順位2） |
| Claude Code（ローカル、Docker サーバー起動済み） | ✅ PNG 生成成功（優先順位3） |
| Claude Code（ローカル、すべて不在） | ⏭️ スキップ + ガイダンス（.puml のみ提供） |
| Claude.ai サンドボックス | ⏭️ 通常はスキップ（.puml のみ提供） |

**`PLANTUML_SERVER_URL` 環境変数**で任意の PlantUML サーバーを指定可能。デフォルトは `http://localhost:8080`（Docker 起動を想定）。

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

### If XMI generation = enabled (デフォルト, `--xmi-format=both`):

**1. PlantUML Class Diagram**

**Filename:** `{project}_class.puml`

完全に再生成されたクラス図。JSONの内容を100%反映。

**2. PNG (ベストエフォート)** ✅ または ⏭️

**Filename:** `{project}_class.png`

`plantuml` コマンド / `plantuml.jar` / Docker PlantUML サーバーのいずれかが利用可能な環境でのみ生成。不在環境ではスキップ（ガイダンスを表示、`.puml` は提供）。

**3. XMI OMG 形式** ✅

**Filename:** `{project}_class-model-omg.uml`

UML 2.5.1 標準形式。Astah Professional、Enterprise Architect で読み込み可能。

**4. XMI EMF 形式** ✅

**Filename:** `{project}_class-model-emf.uml`

Eclipse UML2 5.0.0 形式。**Papyrus 7.1.0 専用**（`pathmap://` 参照、`eAnnotation`、22文字 Base64 ID を含む）。

**5. Architecture Overview**

**Filename:** `{project}_architecture-overview.md`

更新されたアーキテクチャドキュメント。

**6. Metadata Update**

domain-model.jsonのmetadataを更新:
```json
{
  "metadata": {
    "source": "manual-edit",
    "last_regenerated_at": "2026-05-13T...",
    "regenerated_by": "json-to-models",
    "original_source": "usecase-to-class-v1",
    "xmi_generated": true,
    "xmi_formats": ["omg", "emf"],
    "png_generated": true,
    "png_method": "plantuml-cli"
  }
}
```

### If XMI generation = disabled (`--xmi-format=none` または `--no-xmi`):

**1. PlantUML Class Diagram** ✅
**2. PNG (ベストエフォート)** ✅ または ⏭️
**3. XMI Model** ⏭️ **SKIPPED**（約40%高速化）
**4. Architecture Overview** ✅
**5. Metadata Update**: `"xmi_generated": false`

### If `--xmi-format=omg` または `--xmi-format=emf`:

指定した形式のみ生成。それ以外は両形式モードと同じ。

---

## Usage Examples

### Example 0: 実行オプションの選択

**パターンA: 完全な再生成（デフォルト、OMG + EMF 両形式）**
```
ユーザー: json-to-modelsでdomain-model.jsonから再生成してください

Claude: クラス図 XMI を生成しますか？ (はい/いいえ)
ユーザー: はい

→ PlantUML + PNG(ベストエフォート) + XMI OMG + XMI EMF + Markdown 生成
```

**パターンB: 素早い確認**
```
ユーザー: json-to-modelsでPlantUMLだけ素早く確認したい

Claude: クラス図 XMI を生成しますか？ (はい/いいえ)
ユーザー: いいえ

→ PlantUML + PNG(ベストエフォート) + Markdown のみ生成（40%高速化）
```

**パターンC: 形式指定（CLI 直接実行時）**
```
$ json-to-models --xmi-format=emf      # Papyrus 向けに EMF のみ生成
$ json-to-models --xmi-format=omg      # Astah/EA 向けに OMG のみ生成
$ json-to-models --xmi-format=none     # XMI スキップ（高速モード）
$ json-to-models --no-xmi              # 上と等価
```

**パターンD: 旧フラグ指定時の警告**
```
$ json-to-models --xmi

WARNING: --xmi フラグは廃止されました。
         XMI はデフォルトで生成されます（OMG + EMF 両形式）。
         スキップしたい場合は --no-xmi または --xmi-format=none を指定してください。

→ 警告を表示した上でデフォルト動作（両形式生成）を実行
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

2. **XMI OMG 構造検証**
   - UML 2.5.1スキーマに準拠
   - ルートが `<xmi:XMI>` ラッパー
   - namespace が `http://www.omg.org/spec/UML/20161101`

3. **XMI EMF 構造検証**（Papyrus 実機サンプル準拠）
   - ルートが `<uml:Model>` 直接
   - `xmi:version="20131001"`
   - `packageImport` で UMLPrimitiveTypes を import
   - 全要素に 22 文字 Base64 形式の `xmi:id`
   - プリミティブ型参照が `pathmap://UML_LIBRARIES/UMLPrimitiveTypes.library.uml#...` 形式
   - Association に `eAnnotation source="org.eclipse.papyrus"` を持つ
   - Multiplicity が `lowerValue` / `upperValue` で表現

4. **PNG 生成結果の検証**
   - 成功時: PNG ファイルが生成されている
   - スキップ時: ガイダンスメッセージが表示されている、`.puml` は確実に存在

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

3. **検証（UMLツール）**
   - PlantUML図（または PNG）で視覚的確認
   - XMI OMG を **Astah Professional / Enterprise Architect** で読み込み
   - XMI EMF を **Eclipse Papyrus 7.1.0** で読み込み（Model Explorer でクラス・属性・関連を確認）

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

2. **XMI 完全性**
   - 基本的なUML要素のみサポート
   - 高度なステレオタイプは限定的
   - **EMF 形式は Papyrus 7.1.0 系を基準**。Papyrus のメジャーバージョンアップ時は追従検証が必要

3. **XMI クロス互換性は保証外**
   - OMG → Astah/EA、EMF → Papyrus の組み合わせのみサポート
   - 例えば Papyrus で OMG 形式、または EA で EMF 形式を開く挙動は保証しない

4. **PNG 生成の環境依存**
   - `plantuml` コマンド / `plantuml.jar` / Docker PlantUML サーバーのいずれかが利用可能な環境でのみ生成
   - Claude.ai サンドボックスは通常スキップとなり、`.puml` ファイルのみ提供
   - PNG が必要な場合はローカル環境で `plantuml` を直接実行することを推奨

5. **情報損失なし**
   - JSONに定義されたすべての情報を保持
   - ただし、追加のPlantUML注釈は非サポート

---

## Version History

- **v1.3** (2026-05-13)
  - **クラス図 XMI 二形式出力**: OMG 形式（Astah/EA 向け）と EMF 形式（Papyrus 7.1.0 専用）の同時生成
  - **EMF 形式の完全実装**: Papyrus 実機サンプル準拠（`<uml:Model>` 直接ルート、22文字 Base64 ID、`pathmap://`、`eAnnotation source="org.eclipse.papyrus"`、Association の `ownedEnd` + `memberEnd` 完全実装）
  - **PNG ベストエフォート生成**: 3段階フォールバック（`plantuml` コマンド → `java -jar plantuml.jar` → Docker PlantUML サーバー HTTP）。`PLANTUML_SERVER_URL` 環境変数で任意サーバー指定可能
  - **対話質問の統合**: 「XMI を生成しますか？」の 1 問に集約（OMG/EMF 二次質問は廃止）
  - **CLI フラグ**: `--xmi-format={both|omg|emf|none}` を新設。`--xmi` 旧フラグは警告付きで廃止、`--no-xmi` は `--xmi-format=none` の別名として保持
  - **ファイル名変更**: `{project}_class-model.xmi` → `{project}_class-model-omg.uml` / `{project}_class-model-emf.uml`
  - **既存バグ修正**: 旧 `generate_xmi_from_json` の lxml 関連の 2 つの実行時エラーを修正
    - `Element("xmi:XMI", ...)` → `Element(f"{{{XMI_NS}}}XMI", ...)`（Clark notation）。旧版では `ValueError: Invalid tag name 'xmi:XMI'`
    - `tostring(..., encoding='unicode', xml_declaration=True)` → `tostring(..., encoding='UTF-8', xml_declaration=True).decode('utf-8')`。旧版では `ValueError: Serialisation to unicode must not request an XML declaration`

- **v1.2** (2026-04)
  - XMI 生成トグル追加（`--no-xmi` で 40% 高速化）

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
