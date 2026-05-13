# クラス図 XMI 二形式出力 実装計画書 v5

**作成日**: 2026-05-13
**バージョン**: v5（Docker PlantUML サーバー対応版）
**対象スキル**: `uml-workflow-v3`, `json-to-models`
**目的**: UMLモデラーがクラス図を編集可能な形式で受け取れるようにする

## 更新履歴

| バージョン | 主な変更 |
|---|---|
| v1 | 初版。デフォルト両方生成＋パラメータで絞る方針 |
| v2 | 高速モード（XMI 一切生成しない）の対話質問を保持 |
| v3 | Papyrus 実機サンプル分析を反映。EMF 形式を Papyrus 専用と明確化、OMG 形式はツール非依存の業界標準として明確に役割分担 |
| v4 | PlantUML→PNG 生成をベストエフォート方式に確定。Python/Node 完全ローカル実装が存在しないことを調査済みの上で、ローカル `plantuml` コマンド検出方式を採用 |
| v5 | **Docker PlantUML サーバー対応を優先順位3として追加**。ModelCraft AI 公式開発環境構想（docker-compose）を将来オプションとして言及 |

---

## 1. 背景と目的

### 1.1 背景

`uml-workflow-v3` の利用者の中に、生成された PlantUML クラス図に満足できず、自分のUMLツールでクラス図を再作成しているモデラーが存在する。クラス図への思い入れが強く、レイアウト・配置に独自のこだわりを持つ。

### 1.2 目的

クラス図のみ、編集可能な XMI 形式で出力することで、モデラーが自分のツールで開いて自由に配置・編集できるようにする。**自動レイアウト品質で人間モデラーを満足させることは不可能** という前提に立ち、構造的に正しいモデルを渡すことに集中する。

### 1.3 スコープ

| 対象 | 含む / 含まない |
|---|---|
| クラス図 OMG 形式 XMI（Astah/EA/MagicDraw 等向け） | ✅ 含む |
| クラス図 EMF 形式 XMI（**Papyrus 専用**） | ✅ 含む |
| クラス図 PNG（参考用） | ✅ 含む（MCP 経由） |
| アクティビティ図 XMI | ❌ 含まない（将来拡張余地） |
| ユースケース図 XMI | ❌ 含まない（将来拡張余地） |
| シーケンス図 XMI | ❌ 含まない（将来拡張余地） |
| 状態機械 XMI | ❌ 含まない（将来拡張余地） |
| レイアウト情報生成（Sirius `.aird` 等） | ❌ 含まない |
| EMF 形式の Papyrus 以外のツールでの動作保証 | ❌ 含まない（設計方針として保証外） |

---

## 2. 設計方針

### 2.0 形式ごとのツール戦略（v3 で確定）

各形式は**想定ツールを明確に固定**し、中途半端な互換性を狙わず特化した出力を提供する。

| 形式 | 想定ツール（固定） | 設計方針 |
|---|---|---|
| **OMG XMI 2.5.1** | Astah, Enterprise Architect, MagicDraw, Visual Paradigm | **OMG 標準厳格準拠、ツール固有拡張なし** |
| **Eclipse UML2 5.0.0** | **Papyrus 専用** | **Papyrus が出力する形式を完全踏襲、eAnnotation 含む Papyrus 固有要素も全て含む** |

この戦略の利点:
- **OMG 形式**: 業界標準準拠を売りに、複数ツールでの読み込み互換性を最優先
- **EMF 形式**: 「Papyrus で開けば即動く」を売りに、Papyrus 上での挙動を最適化

モデラーがどのツールを使うかで明確に使い分けられる。

### 2.1 出力ファイル構成

クラス図ステップの output ディレクトリに以下を生成:

```
output/
├── class-diagram.puml          # 既存（PlantUML ソース） ← 常に生成
├── class-diagram.png           # PNG（参考用） ← plantuml コマンド検出時のみ
├── class-diagram-omg.uml       # 新規：OMG UML 2.5.1 XMI（デフォルト出力）
└── class-diagram-emf.uml       # 新規：Eclipse/EMF XMI（デフォルト出力）
```

各ファイルの生成条件:

| ファイル | 生成条件 |
|---|---|
| `class-diagram.puml` | 常に生成（PlantUML ソース、これが SSoT 的役割） |
| `class-diagram.png` | **`plantuml` コマンドが環境にある場合のみ**（ベストエフォート） |
| `class-diagram-omg.uml` | XMI 生成モード時（デフォルト） |
| `class-diagram-emf.uml` | XMI 生成モード時（デフォルト） |

高速モード（`--no-xmi`）では XMI 2ファイルがスキップされ、`.puml` と（環境にあれば）`.png` のみ生成される。

### 2.2 動作モード

| パラメータ | 動作 | 用途 |
|---|---|---|
| 未指定（デフォルト） | OMG + EMF 両方生成 | 通常運用、モデラーへの納品 |
| `--xmi-format=both` | OMG + EMF 両方生成（明示） | デフォルトと同じ、スクリプトでの明示用 |
| `--xmi-format=omg` | OMG のみ生成 | Astah / EA など OMG 専用環境 |
| `--xmi-format=emf` | EMF のみ生成 | Papyrus 専用環境 |
| `--xmi-format=none` | XMI 生成しない（約40%高速化） | CI、開発中の高速反復 |
| `--no-xmi` | `--xmi-format=none` のエイリアス | 短縮形 |

### 2.3 対話質問の再設計

3月時点の「XMI yes/no」と「OMG/EMF 選択」の2段階質問を、**1問に統合**する。XMI 形式の二次質問は廃止するが、**「高速化のためにスキップする選択肢」は残す**。

```
質問: クラス図のXMIファイルを生成しますか？

  はい（推奨・デフォルト）
    → OMG標準 + Eclipse/EMF の両形式を自動生成
    → UMLツールで編集可能なクラス図データとして利用可能
    
  いいえ（高速モード）
    → PlantUML のみ生成（約40%高速化）
    → 既存ワークフローと同等の速度
```

**変更点まとめ:**

| 項目 | 3月時点 | 今回 |
|---|---|---|
| 対話質問数 | 2問（yes/no → 形式選択） | **1問**（生成するか否か） |
| デフォルト | XMI 生成 OFF | **XMI 生成 ON（両形式）** |
| 形式選択 | ユーザーが二択 | **自動で両形式生成** |
| 高速モード | デフォルト | **明示選択時** |



---

## 3. 実装計画

### Phase 1: `json-to-models` スキル拡張

#### 1.1 既存関数のリネーム

```python
# 変更前
def generate_xmi_from_json(domain_model: dict) -> str: ...

# 変更後
def generate_xmi_omg(domain_model: dict) -> str: ...
```

実体の変更なし、関数名のみ変更。OMG 形式に明示的に名付ける。

#### 1.2 EMF 形式生成関数の新設（Papyrus 実機サンプル準拠）

**Papyrus 実物サンプルの解析結果（2026-05-13 取得）:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<uml:Model xmi:version="20131001"
           xmlns:xmi="http://www.omg.org/spec/XMI/20131001"
           xmlns:ecore="http://www.eclipse.org/emf/2002/Ecore"
           xmlns:uml="http://www.eclipse.org/uml2/5.0.0/UML"
           xmi:id="_8qjE0EBkEfGJ9KxQ0FEvfA" name="TestClass">

  <!-- 必須: UMLPrimitiveTypes ライブラリの import -->
  <packageImport xmi:type="uml:PackageImport" xmi:id="_8vRz0EBkEfGJ9KxQ0FEvfA">
    <importedPackage xmi:type="uml:Model"
                     href="pathmap://UML_LIBRARIES/UMLPrimitiveTypes.library.uml#_0"/>
  </packageImport>

  <!-- Class with Generalization (inheritance) -->
  <packagedElement xmi:type="uml:Class" xmi:id="_FGad4EBlEfGJ9KxQ0FEvfA" name="Person">
    <generalization xmi:type="uml:Generalization"
                    xmi:id="_dxuhEEBlEfGJ9KxQ0FEvfA"
                    general="_-IRAAEBkEfGJ9KxQ0FEvfA"/>
  </packagedElement>

  <!-- Class with composite Aggregation -->
  <packagedElement xmi:type="uml:Class" xmi:id="_G0Sr8EBlEfGJ9KxQ0FEvfA" name="OrgUnit">
    <ownedAttribute xmi:type="uml:Property" xmi:id="_p8-9AkBlEfGJ9KxQ0FEvfA"
                    name="party" type="_-IRAAEBkEfGJ9KxQ0FEvfA"
                    aggregation="composite"
                    association="_p8-V8EBlEfGJ9KxQ0FEvfA">
      <lowerValue xmi:type="uml:LiteralInteger" xmi:id="..." value="1"/>
      <upperValue xmi:type="uml:LiteralUnlimitedNatural" xmi:id="..." value="1"/>
    </ownedAttribute>
  </packagedElement>

  <!-- Class with String property via pathmap -->
  <packagedElement xmi:type="uml:Class" xmi:id="_-IRAAEBkEfGJ9KxQ0FEvfA" name="Party">
    <ownedAttribute xmi:type="uml:Property" xmi:id="_lYcssEEnEfG-jsOk2mburg" name="name">
      <type xmi:type="uml:PrimitiveType"
            href="pathmap://UML_LIBRARIES/UMLPrimitiveTypes.library.uml#String"/>
    </ownedAttribute>
  </packagedElement>

  <!-- Association with eAnnotation (Papyrus-specific) -->
  <packagedElement xmi:type="uml:Association" xmi:id="_p8-V8EBlEfGJ9KxQ0FEvfA"
                   memberEnd="_p8-9AkBlEfGJ9KxQ0FEvfA _p8_kEEBlEfGJ9KxQ0FEvfA">
    <eAnnotations xmi:type="ecore:EAnnotation" xmi:id="_p8-9AEBlEfGJ9KxQ0FEvfA"
                  source="org.eclipse.papyrus">
      <details xmi:type="ecore:EStringToStringMapEntry"
               xmi:id="_p8-9AUBlEfGJ9KxQ0FEvfA"
               key="nature" value="UML_Nature"/>
    </eAnnotations>
    <ownedEnd xmi:type="uml:Property" xmi:id="_p8_kEEBlEfGJ9KxQ0FEvfA"
              name="orgunit" type="_G0Sr8EBlEfGJ9KxQ0FEvfA"
              association="_p8-V8EBlEfGJ9KxQ0FEvfA">
      <lowerValue xmi:type="uml:LiteralInteger" value="0"/>
      <upperValue xmi:type="uml:LiteralUnlimitedNatural" value="*"/>
    </ownedEnd>
  </packagedElement>
</uml:Model>
```

**実装コード:**

```python
import base64
import os
from lxml import etree

UML_NS = "http://www.eclipse.org/uml2/5.0.0/UML"
XMI_NS = "http://www.omg.org/spec/XMI/20131001"
ECORE_NS = "http://www.eclipse.org/emf/2002/Ecore"

def gen_papyrus_id() -> str:
    """
    Papyrus 互換の 22 文字 Base64 形式 ID を生成
    例: _8qjE0EBkEfGJ9KxQ0FEvfA
    """
    raw = os.urandom(16)
    b64 = base64.urlsafe_b64encode(raw).decode('ascii').rstrip('=')
    return f"_{b64[:22]}"

def generate_xmi_emf(domain_model: dict) -> str:
    """
    JSON から Eclipse UML2 5.0.0 形式 XMI（Papyrus 専用）を生成
    
    重要: ルート要素は <xmi:XMI> ではなく <uml:Model> 直接
    """
    nsmap = {
        'xmi': XMI_NS,
        'ecore': ECORE_NS,
        'uml': UML_NS
    }
    
    # ルートは uml:Model 直接（xmi:XMI ラッパーなし）
    model = etree.Element(f"{{{UML_NS}}}Model", nsmap=nsmap)
    model.set(f"{{{XMI_NS}}}version", "20131001")
    model.set(f"{{{XMI_NS}}}id", gen_papyrus_id())
    model.set("name", domain_model['metadata'].get('project_name', 'DomainModel'))
    
    # 必須: UMLPrimitiveTypes ライブラリ import
    pkg_import = etree.SubElement(model, "packageImport")
    pkg_import.set(f"{{{XMI_NS}}}type", "uml:PackageImport")
    pkg_import.set(f"{{{XMI_NS}}}id", gen_papyrus_id())
    imported = etree.SubElement(pkg_import, "importedPackage")
    imported.set(f"{{{XMI_NS}}}type", "uml:Model")
    imported.set("href", "pathmap://UML_LIBRARIES/UMLPrimitiveTypes.library.uml#_0")
    
    # ID マップ（後で型参照を解決するため）
    class_id_map = {}  # entity_name -> xmi:id
    
    # クラス生成（第1パス: ID 割り当てのみ）
    for entity in domain_model['entities']:
        class_id_map[entity['name']] = gen_papyrus_id()
    
    # クラス生成（第2パス: 構造生成）
    for entity in domain_model['entities']:
        cls = etree.SubElement(model, "packagedElement")
        cls.set(f"{{{XMI_NS}}}type", "uml:Class")
        cls.set(f"{{{XMI_NS}}}id", class_id_map[entity['name']])
        cls.set("name", entity['name'])
        
        # Generalization（継承）
        if entity.get('extends') and entity['extends'] in class_id_map:
            gen = etree.SubElement(cls, "generalization")
            gen.set(f"{{{XMI_NS}}}type", "uml:Generalization")
            gen.set(f"{{{XMI_NS}}}id", gen_papyrus_id())
            gen.set("general", class_id_map[entity['extends']])
        
        # 属性
        for attr in entity.get('attributes', []):
            prop = etree.SubElement(cls, "ownedAttribute")
            prop.set(f"{{{XMI_NS}}}type", "uml:Property")
            prop.set(f"{{{XMI_NS}}}id", gen_papyrus_id())
            prop.set("name", attr['name'])
            
            # 型解決
            if attr.get('type') in PRIMITIVE_TYPE_MAP:
                type_elem = etree.SubElement(prop, "type")
                type_elem.set(f"{{{XMI_NS}}}type", "uml:PrimitiveType")
                type_elem.set(
                    "href",
                    f"pathmap://UML_LIBRARIES/UMLPrimitiveTypes.library.uml#{PRIMITIVE_TYPE_MAP[attr['type']]}"
                )
            elif attr.get('type') in class_id_map:
                # 別クラスへの参照
                prop.set("type", class_id_map[attr['type']])
    
    # Association 生成（省略 - aggregation, multiplicity, ownedEnd, eAnnotation 含む）
    # ...
    
    return etree.tostring(
        model,
        pretty_print=True,
        encoding='unicode',
        xml_declaration=True
    )

# プリミティブ型マッピング（pathmap 解決用）
PRIMITIVE_TYPE_MAP = {
    'String': 'String',
    'Integer': 'Integer',
    'Boolean': 'Boolean',
    'Real': 'Real',
    'UnlimitedNatural': 'UnlimitedNatural',
    # ドメインモデル固有の型エイリアス
    'int': 'Integer',
    'str': 'String',
    'bool': 'Boolean',
    'float': 'Real',
}
```

**OMG 版との差分の核心（v3 で確定）:**

| 項目 | OMG | EMF（Papyrus 実機準拠） |
|---|---|---|
| ルート要素 | `<xmi:XMI>` | **`<uml:Model>` 直接** |
| UML namespace | `http://www.omg.org/spec/UML/20161101` | `http://www.eclipse.org/uml2/5.0.0/UML` |
| XMI version | `2.5.1` | `20131001` |
| `xmi:id` 形式 | `_<prefix>_<8桁hex>` | **22文字 Base64**（Papyrus 互換） |
| `xsi:schemaLocation` | なし | **なし**（Papyrus 実物には不要） |
| 型参照 | 直接参照 | `pathmap://UML_LIBRARIES/...` |
| `packageImport` | なし | **必須**（UMLPrimitiveTypes） |
| eAnnotation | なし | **あり**（`source="org.eclipse.papyrus"`） |
| ecore namespace | なし | あり |

#### 1.3 ディスパッチャー関数

```python
def generate_xmi(domain_model: dict, format: str = "both") -> dict:
    """
    XMI 生成のエントリーポイント

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
```

#### 1.4 ファイル出力ロジック

```python
xmi_outputs = generate_xmi(domain_model, format=xmi_format)
if xmi_outputs["omg"]:
    write_file(f"{project}_class-model-omg.uml", xmi_outputs["omg"])
if xmi_outputs["emf"]:
    write_file(f"{project}_class-model-emf.uml", xmi_outputs["emf"])
```

### Phase 2: `uml-workflow-v3` フロー改修

#### 2.1 対話質問の再設計

`SKILL.md` 161行目付近の XMI yes/no 質問は**残すが選択肢の意味を変更**する。

**変更前（3月時点）:**
```python
{
    "question": "XMIファイルを生成しますか？",
    "options": [
        "いいえ（推奨・デフォルト）",  # 高速モード
        "はい"                       # → さらに OMG/EMF 二次質問へ
    ]
}
# はい選択時の二次質問
{
    "question": "XMI形式を選択してください",
    "options": ["OMG標準 UML 2.5.1", "Eclipse/EMF形式"]
}
```

**変更後:**
```python
{
    "question": "クラス図のXMIファイルを生成しますか？",
    "options": [
        "はい（推奨・デフォルト）：OMG + EMF 両形式を自動生成",
        "いいえ（高速モード）：PlantUML のみ生成、約40%高速化"
    ]
}
# 二次質問は削除
```

ポイント:
- **デフォルトが反転**: 「いいえ」→ 「はい」
- **二次質問は廃止**: 形式選択は自動化
- **高速モードは選択可能**: 既存利用者の高速ワークフローを温存

#### 2.2 パラメータ追加

```bash
python3 run_workflow.py {project_name} \
  --cache {cache_param} \
  --mode {mode_param} \
  [--xmi-format=both|omg|emf|none]  # デフォルト: both
```

#### 2.3 `xmi_flag` ロジックの更新

```python
# 変更前
xmi_flag = ""        # XMI なし
xmi_flag = "--xmi"   # XMI あり

# 変更後（対話結果からマッピング）
if user_answer == "はい":
    xmi_format = "both"
elif user_answer == "いいえ":
    xmi_format = "none"

# パラメータで上書き可能（CLI 直接実行時）
xmi_flag = f"--xmi-format={xmi_format}"
```

CLI 直接実行時はユーザーが `--xmi-format=omg` 等を指定でき、対話モードでは「両方」または「なし」の二択になる（OMG/EMF 単独はパワーユーザー向けの隠し機能）。

### Phase 3: PNG 生成（ベストエフォート方式）

#### 3.1 設計判断の背景（v4 で確定）

調査結果から、以下の事実が判明:

- **Python に完全ローカルレンダリングできるパッケージは存在しない**（すべて PlantUML サーバーへの HTTP クライアントか、Java + plantuml.jar のラッパー）
- **Node.js も同様**（`node-plantuml` は Java を呼ぶラッパー、`plantuml.js`/`plantuml-core` は CheerpJ ベースでブラウザ動作前提、実用段階にない）
- PlantUML 本体は Java 製で、レイアウトエンジンの GraphViz にも依存している
- **どの言語でも結局 plantuml.jar または PlantUML サーバーが必要**
- **Claude.ai サンドボックス**は Java 21 が入っているが `plantuml.com` および GitHub Releases アセットへのアクセスが許可リストにないため、jar の入手も実行も困難

#### 3.2 採用方針: ベストエフォート方式（3段階フォールバック）

**「PlantUML が利用可能な何らかの手段があれば PNG を生成、なければ `.puml` のみ提供」**

3段階のフォールバック:
1. **`plantuml` コマンド**（最も手軽、個人開発者向け）
2. **`java -jar plantuml.jar`**（jar 配置済み環境向け）
3. **PlantUML サーバー HTTP**（Docker または独自ホスト、チーム・企業向け）

理由:
- ユーザーが Python/Node ラッパーをインストールしても、結局裏で Java が必要 → 中間層を増やしてもメリットなし
- モデラーは XMI を使うので PNG は二次的優先度
- PNG が必要な場面（仕様書添付など）では、ユーザーが自分の環境で `plantuml` を直接使う方が早い
- **Docker 対応により、ModelCraft AI の顧客企業（オフライン要件・環境統一要件あり）にも対応可能**

#### 3.3 検出ロジック

```python
import shutil
import subprocess
import os
import urllib.request
import urllib.error
import base64
import zlib

def render_png_best_effort(puml_path: str, png_path: str) -> dict:
    """
    PlantUML から PNG をベストエフォートで生成
    
    優先順位:
      1. plantuml コマンド（最速、最小依存）
      2. ローカル plantuml.jar (java -jar)
      3. Docker / ローカル PlantUML サーバー (HTTP)
      4. スキップしてガイダンス表示
    
    Returns:
        {"success": bool, "method": str, "message": str}
    """
    # 優先順位 1: plantuml コマンド
    if shutil.which("plantuml"):
        try:
            subprocess.run(
                ["plantuml", "-tpng", puml_path],
                check=True,
                capture_output=True,
                timeout=60
            )
            return {
                "success": True,
                "method": "plantuml-cli",
                "message": "✅ PNG generated via local plantuml command"
            }
        except subprocess.SubprocessError as e:
            return {
                "success": False,
                "method": "plantuml-cli",
                "message": f"⚠️ plantuml command failed: {e}"
            }
    
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
                check=True,
                capture_output=True,
                timeout=60
            )
            return {
                "success": True,
                "method": "java-jar",
                "message": f"✅ PNG generated via java -jar {jar_path}"
            }
        except subprocess.SubprocessError as e:
            return {
                "success": False,
                "method": "java-jar",
                "message": f"⚠️ java -jar plantuml.jar failed: {e}"
            }
    
    # 優先順位 3: Docker / ローカル PlantUML サーバー (HTTP)
    plantuml_server = os.environ.get(
        "PLANTUML_SERVER_URL",
        # デフォルト: Docker plantuml/plantuml-server のローカル起動を試行
        "http://localhost:8080"
    )
    
    if plantuml_server:
        try:
            # サーバー疎通確認（短いタイムアウト）
            with urllib.request.urlopen(f"{plantuml_server}/", timeout=2) as resp:
                if resp.status == 200:
                    # PlantUML テキストを読み込み、独自エンコード
                    with open(puml_path, 'r', encoding='utf-8') as f:
                        puml_text = f.read()
                    
                    encoded = _plantuml_encode(puml_text)
                    url = f"{plantuml_server}/png/{encoded}"
                    
                    with urllib.request.urlopen(url, timeout=30) as png_resp:
                        with open(png_path, 'wb') as out:
                            out.write(png_resp.read())
                    
                    return {
                        "success": True,
                        "method": "http-server",
                        "message": f"✅ PNG generated via PlantUML server at {plantuml_server}"
                    }
        except (urllib.error.URLError, ConnectionError, TimeoutError):
            # サーバーが起動していない、または到達不能 → 次へ
            pass
        except Exception as e:
            return {
                "success": False,
                "method": "http-server",
                "message": f"⚠️ PlantUML server error: {e}"
            }
    
    # 優先順位 4: スキップしてガイダンス表示
    return {
        "success": False,
        "method": "skipped",
        "message": (
            "ℹ️  PlantUML not available. PNG generation skipped.\n"
            "    .puml file is available for manual rendering.\n"
            "\n"
            "    Option A: Install plantuml command\n"
            "      macOS:   brew install plantuml\n"
            "      Ubuntu:  sudo apt install plantuml\n"
            "      Windows: choco install plantuml\n"
            "\n"
            "    Option B: Use Docker PlantUML server\n"
            "      docker run -d -p 8080:8080 plantuml/plantuml-server\n"
            "      (then re-run with PLANTUML_SERVER_URL=http://localhost:8080)\n"
            "\n"
            "    Option C: Set PLANTUML_JAR environment variable to plantuml.jar path."
        )
    }


def _plantuml_encode(text: str) -> str:
    """
    PlantUML 独自の URL エンコード（DEFLATE + 独自 Base64）
    PlantUML サーバーが受け付ける形式に変換する
    """
    compressed = zlib.compress(text.encode('utf-8'))[2:-4]  # zlib ヘッダ/フッタ除去
    return _encode_6bit(compressed)


def _encode_6bit(data: bytes) -> str:
    """PlantUML 独自の 6bit エンコーディング"""
    PLANTUML_ALPHABET = (
        "0123456789"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "abcdefghijklmnopqrstuvwxyz"
        "-_"
    )
    result = []
    for i in range(0, len(data), 3):
        chunk = data[i:i+3]
        if len(chunk) == 3:
            b1, b2, b3 = chunk
            result.append(PLANTUML_ALPHABET[b1 >> 2])
            result.append(PLANTUML_ALPHABET[((b1 & 0x3) << 4) | (b2 >> 4)])
            result.append(PLANTUML_ALPHABET[((b2 & 0xF) << 2) | (b3 >> 6)])
            result.append(PLANTUML_ALPHABET[b3 & 0x3F])
        # （末尾のパディング処理は省略）
    return "".join(result)
```

#### 3.4 環境別の挙動

| 環境 | 期待される挙動 |
|---|---|
| **Claude Code（ローカル、`plantuml` あり）** | ✅ PNG 生成成功（優先順位1） |
| **Claude Code（ローカル、jar 配置済み）** | ✅ PNG 生成成功（優先順位2） |
| **Claude Code（ローカル、Docker サーバー起動済み）** | ✅ PNG 生成成功（優先順位3） |
| **Claude Code（ローカル、何もない）** | ℹ️ スキップ + 3択ガイダンス表示 |
| **Claude.ai サンドボックス** | ℹ️ スキップ（plantuml なし、Docker 不可、外部到達不可） |
| **API 経由・コンテナ環境** | Docker 内 PlantUML サーバーと組み合わせて利用可 |

#### 3.5 ユーザー向けガイダンス

`uml-workflow-v3` の README に以下を追記:

```markdown
## PNG 生成について

クラス図 PNG は **PlantUML が利用可能な環境でのみ生成されます**。
未対応環境では `.puml` ファイルのみ提供します。

PNG 生成は以下の優先順位でベストエフォート的に試行されます:

### Option A: `plantuml` コマンドのインストール（推奨、最も手軽）

- macOS:   `brew install plantuml`
- Ubuntu/Debian: `sudo apt install plantuml`
- Windows: `choco install plantuml`

### Option B: Docker PlantUML サーバー（チーム利用に最適）

完全オフラインで動作し、Java/Graphviz の OS 差異を完全に排除できます。

\`\`\`bash
docker run -d -p 8080:8080 plantuml/plantuml-server
\`\`\`

起動後、環境変数を設定（デフォルトの `http://localhost:8080` で自動検出されます）:

\`\`\`bash
export PLANTUML_SERVER_URL=http://localhost:8080
\`\`\`

**Docker 案の利点:**
- 顧客データを外部に送信しない（オフライン動作）
- 環境差異を完全排除
- チーム全員が同じバージョンの PlantUML を使える
- CI/CD への統合が容易

### Option C: plantuml.jar の配置

\`\`\`bash
export PLANTUML_JAR=/path/to/plantuml.jar
\`\`\`

### Claude.ai 上での利用

Claude.ai のサンドボックス環境では PlantUML が利用できないため、PNG は
生成されません。`.puml` ファイルをダウンロードし、お手元の以下の方法で
描画してください:

- VSCode PlantUML 拡張
- IntelliJ IDEA PlantUML プラグイン
- PlantUML Web Server (https://www.plantuml.com/plantuml/uml/)
- ローカル PlantUML サーバー (Docker)
```

#### 3.6 将来オプション（v5 では実装しない）

| オプション | 状況 | 備考 |
|---|---|---|
| **ModelCraft AI 公式開発環境（docker-compose）** | 構想段階 | PlantUML + 将来は Papyrus-Web 等を統合した一括起動環境。顧客への配布で差別化要素になり得る。**本格設計は別セッション** |
| MCP サーバー対応（独自ホスト） | 保留 | 顧客データを外部送信するリスクで保留 |
| MCP サーバー対応（サードパーティ） | 様子見 | 信頼できる実装が成熟したら検討 |
| SVG 出力 | 検討 | PlantUML は `-tsvg` で簡単に対応可能、要望次第で追加 |
| キャッシュ機構 | 検討 | 同じドメインモデルから何度も PNG を生成しないための最適化 |

##### ModelCraft AI 公式開発環境構想（言及のみ）

将来的に、ModelCraft AI が顧客に提供する開発環境セットとして以下のような
`docker-compose.yml` を整備する構想がある。本計画書のスコープ外だが、
本実装で `PLANTUML_SERVER_URL` 環境変数を導入することで、将来の統合への
道筋が開ける。

```yaml
# 将来構想: modelcraft-dev-environment/docker-compose.yml
services:
  plantuml:
    image: plantuml/plantuml-server:jetty
    ports:
      - "8080:8080"
  
  # 将来追加候補
  # papyrus-web:
  #   image: eclipsesource/papyrus-web
  #   ports:
  #     - "8081:8080"
```

これにより顧客は `docker compose up` 一発でフル開発環境を起動でき、
ModelCraft AI ブランドのインフラ提供として位置付けられる。本格設計は
別途実施。

---

## 4. 影響範囲と互換性

### 4.1 後方互換性

**`--xmi` フラグの扱い:**

| 旧 | 新 | 動作変化 |
|---|---|---|
| `--xmi` 指定 | 廃止 → 不要 | 旧: XMI 生成あり / 新: デフォルトで両形式生成されるので指定不要 |
| `--xmi` 未指定 | `--no-xmi` で代替可能 | 旧: XMI なし（デフォルト） / 新: デフォルトが「生成」に反転したので、明示的に `--no-xmi` 指定 |

**意味の反転**が破壊的変更となるため、移行措置として警告メッセージを表示:

```
WARNING: --xmi フラグは廃止されました。
         XMI はデフォルトで生成されます（OMG + EMF 両形式）。
         スキップしたい場合は --no-xmi または --xmi-format=none を指定してください。
```

**ファイル名の変更:**

- 既存出力ファイル名 `{project}_class-model.xmi` は廃止
- 新ファイル名: `{project}_class-model-omg.uml` / `{project}_class-model-emf.uml`
- 既存ファイル名を期待するダウンストリームスクリプトがある場合は要確認

### 4.2 ドキュメント更新

- `uml-workflow-v3/SKILL.md`: 対話フロー記述、CLI 仕様
- `json-to-models/SKILL.md`: Step 3 を OMG/EMF 両対応に書き換え
- `json-to-models/README.md`: 出力ファイル一覧の更新
- `uml-workflow-v3/PIPELINE.md`: Step 4 のクラス図出力仕様更新
- ZIPリリース時の DEMO-GUIDE.md: クラス図XMI出力の説明追加

### 4.3 関連スキルへの影響

- `domain-model-to-papyrus`: 当面そのまま（再評価は別途）
- `classdiagram-image-to-json`: 影響なし（入力側スキル）
- `rmodp-to-domain-model`: 影響なし（domain-model.json を生成する側）
- `model-validator-v1`: 影響なし

---

## 5. テスト計画

### 5.1 単体テスト

- `generate_xmi_omg()`: 既存と同じ出力であること（リネームのみ）
- `generate_xmi_emf()`: 新規実装。以下を検証
  - 全要素に `xmi:id` が付与されること
  - namespace が Eclipse UML2 5.0.0 であること
  - `schemaLocation` が含まれること

### 5.2 統合テスト：実機ツールで開く

各形式は**専用ツール**で動作確認:

| 形式 | 検証ツール | 重点確認項目 |
|---|---|---|
| **OMG** | Astah Professional, Enterprise Architect | Model Explorer にクラス・属性・関連が表示される、業界標準として読み込めること |
| **EMF** | **Eclipse Papyrus 7.1.0** | Papyrus が生成する形式と構造一致、`packageImport` / `pathmap://` / `eAnnotation` が正しく解釈される |

**EMF 形式の参照サンプル**:
2026-05-13 取得の Papyrus 実機サンプル（Section 3.1.2 に掲載）を参照基準とする。生成された XMI が以下の構造的特徴を持つことを確認:

1. ルートが `<uml:Model>` 直接
2. `xmi:version="20131001"`
3. `packageImport` で UMLPrimitiveTypes を import
4. プリミティブ型参照が `pathmap://UML_LIBRARIES/UMLPrimitiveTypes.library.uml#...` 形式
5. 全要素に 22 文字 Base64 形式の `xmi:id`
6. Association に `eAnnotation source="org.eclipse.papyrus"` を持つ
7. Multiplicity が `lowerValue` / `upperValue` で表現

最低限「Model Explorer にクラス・属性・関連が表示される」ことが基準。クラス図ダイアグラム自体は表示されなくてよい（モデラーが手で並べる）。

**OMG/EMF クロステスト（参考）:**
原則として OMG → EA/Astah、EMF → Papyrus の組み合わせのみサポート。Papyrus で OMG 形式を開いたり、EA で EMF 形式を開く場合の挙動は**保証外**とする。これは「Papyrus 専用 EMF」「ツール非依存 OMG」の設計方針による意図的な制限。

### 5.3 後方互換性テスト

- `--xmi-format=none` または `--no-xmi` で従来の高速モード（PlantUML のみ）が動くこと
- 対話モードで「いいえ」選択時に高速モードに入ること
- `--xmi` 旧フラグ指定時に警告メッセージが表示されること
- 既存の `_cache/` チェックポイントが新フォーマット（OMG + EMF）に移行できること

---

## 6. 実装順序

1. **設計レビュー**（本ドキュメントの確認）← **現在地**
2. `json-to-models/SKILL.md` への EMF 形式実装追記
3. `json-to-models` の Step 3 関数群書き換え（OMG/EMF 両対応）
4. PNG ベストエフォート検出ロジック実装（`json-to-models` 内）
   - 4a. 優先順位1: `plantuml` コマンド
   - 4b. 優先順位2: `java -jar plantuml.jar`
   - 4c. **優先順位3: Docker / HTTP サーバー（`_plantuml_encode` 含む）**
5. `uml-workflow-v3/SKILL.md` の対話フロー改修
6. `uml-workflow-v3/scripts/run_workflow.py` の CLI パラメータ追加
7. Astah / Papyrus での実機検証（XMI 出力）
8. 環境別 PNG 生成テスト
   - 8a. plantuml コマンドあり環境
   - 8b. jar 配置済み環境
   - 8c. **Docker サーバー起動済み環境**
   - 8d. すべて無い環境（スキップ確認）
9. PIPELINE.md / README.md 更新（PlantUML 3 方式インストールガイド含む）
10. ZIPリリース（v3.3.0 候補）
11. ~~PlantUML MCP 統合~~（v5 でスコープ外、将来オプション）
12. ~~ModelCraft AI 公式開発環境（docker-compose）~~（v5 でスコープ外、別タスクとして言及のみ）

---

## 7. 未確定事項・要確認

### 7.1 v3〜v5 で解決済み

| 項目 | 解決バージョン | 解決内容 |
|---|---|---|
| EMF 形式の `pathmap://` 解決 | v3 | Papyrus 実機サンプルで確認、`pathmap://UML_LIBRARIES/UMLPrimitiveTypes.library.uml#<TypeName>` を直書きで OK |
| `xsi:schemaLocation` の要否 | v3 | Papyrus 実物には**ない**ことを確認、出力に含めない |
| EMF ルート要素 | v3 | `<uml:Model>` 直接（`<xmi:XMI>` ラッパーなし） |
| eAnnotation の扱い | v3 | EMF（Papyrus 専用）には**含める** |
| OMG/EMF クロス互換性 | v3 | **保証しない**方針で確定。OMG → EA/Astah、EMF → Papyrus のみサポート |
| `xmi:id` 形式 | v3 | EMF: 22文字 Base64、OMG: 8文字 hex |
| PNG 生成方式 | v4 | ベストエフォート方式（`plantuml` コマンド検出時のみ） |
| PNG 生成環境依存の扱い | v4 | Claude.ai サンドボックスでは PNG なし、ローカル環境では plantuml 検出次第 |
| MCP サーバー依存 | v4 | 本実装からは外す、将来オプション |
| **Docker PlantUML サーバー対応** | **v5** | **優先順位3として実装、`PLANTUML_SERVER_URL` 環境変数で制御** |
| **企業・チーム利用の経路** | **v5** | **Docker サーバー方式により、オフライン要件・環境統一要件にも対応** |
| **ModelCraft AI 公式開発環境構想** | **v5** | **言及のみ。本格設計は別セッション。本実装の `PLANTUML_SERVER_URL` で将来統合への道筋は確保** |

### 7.2 残課題

1. **ファイル拡張子**: `.uml` 二本立てか、`.xmi` 拡張子も併用するか（Papyrus 実機は `.uml` 出力なので EMF は `.uml` 推奨、OMG は `.xmi` でも可）
2. **既存ユーザーへのアナウンス**: `--xmi` フラグ廃止の周知方法
3. **Association の完全実装**: 双方向関連・aggregation・composition を `ownedEnd` + `memberEnd` パターンで完全実装する必要がある（Section 3.1.2 のコードは簡略版）
4. **PLANTUML_JAR 環境変数の標準化**: 業界標準があれば踏襲、なければ ModelCraft AI 独自で定義
5. **PlantUML サーバーへの HTTP エンコーディング実装**: `_plantuml_encode` 関数の末尾パディング処理が簡略版なので、本実装時に PlantUML 公式仕様（DEFLATE + 独自 Base64）に完全準拠させる必要あり

---

## 8. リスクと対策

| リスク | 影響度 | 対策 |
|---|---|---|
| ~~EMF 形式の `pathmap://` が Papyrus で解決できない~~ | ~~中~~ | ✅ **v3 で解消**: Papyrus 実物サンプルで `pathmap://` がそのまま使えることを確認 |
| ~~MCP サーバー依存による移植性低下~~ | ~~中~~ | ✅ **v4 で解消**: MCP は実装スコープから外し、ローカル `plantuml` コマンド検出方式に変更 |
| ~~企業ユーザーの「PlantUML をインストールできない」制約~~ | ~~中~~ | ✅ **v5 で解消**: Docker PlantUML サーバー対応により、ホスト OS への直接インストール不要に |
| 既存利用者の `--xmi` フラグ破壊的変更 | 低 | デフォルトで XMI 生成、`--no-xmi` で旧挙動再現、警告メッセージで誘導 |
| `xmi:id` 衝突 | 低 | UUID/16バイトランダム使用で衝突確率は実質ゼロ |
| Papyrus 以外のツール（EA/Astah）で EMF 形式を開くユーザー | 低 | 設計方針として保証外、ドキュメントに明記 |
| Papyrus がバージョンアップで XMI 形式を変更する | 中 | Papyrus 7.1.0 系を基準に実装、メジャーバージョンアップ時に追従検証 |
| Association の双方向参照実装の複雑さ | 中 | 実装フェーズで Papyrus 実物サンプルを参照しながら段階的に実装 |
| Claude.ai ユーザーに PNG が提供されない | 中 | README で明示、VSCode 拡張等の代替手段を案内、`.puml` ファイルは確実に提供 |
| ローカル plantuml コマンドの仕様差異（macOS/Linux/Windows） | 低 | 検出ロジックで `shutil.which()` を使い、失敗時は次の優先順位に進む |
| **Docker Desktop 商用利用ライセンス問題** | **低〜中** | **企業ユーザーの一部に影響。Rancher Desktop や Podman 等の代替案を README で案内** |
| **PlantUML サーバーのバージョン差異** | **低** | **公式 `plantuml/plantuml-server` イメージを推奨、特定のタグを明示してドキュメント化** |
| **PlantUML HTTP エンコーディングのエッジケース** | **中** | **本実装で公式仕様に準拠した完全版を実装、テストケースで境界値を検証** |
