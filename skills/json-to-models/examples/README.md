# json-to-models - Examples

Papyrus 7.1.0 実機検証で使用した 2 つのサンプル domain-model.json です。

## verify-mini.json

最小限のベースラインモデル（3 クラス + 1 Association）。Papyrus 7.1.0 で
v1.3 / v1.3.1 が動作することの最小確認用。

| 項目 | 値 |
|---|---|
| Class 数 | 3 (Person / Student / OrgUnit) |
| Generalization | 2 (Student→Person, OrgUnit→Person 風の構造) |
| Composition | 1 (OrgUnit ◆━ Party) |
| カバーする v1.3 機能 | 15/15 |

## verify-comprehensive.json

学校管理システムを題材にした、v1.3.1 全機能カバレッジモデル。

| 項目 | 値 |
|---|---|
| Class 数 | 8 (Person / Student / Staff / Teacher / School / Department / Course / Enrollment) |
| Enumeration 数 | 2 (Grade 6 値、Subject 8 値) |
| Association 数 | 7 |
| 多段 Generalization | 3 段 (Person ← Staff ← Teacher) |
| abstract クラス | 2 (Person, Staff) |
| 自己参照 | 1 (Teacher.mentor → Teacher) |
| aggregation 種別 | 3 種 (composite / shared / none) |
| 全 PrimitiveType | 5 種使用 (String / Integer / Boolean / Real / UnlimitedNatural) |
| Operation w/ params + return | 2 件 |
| カバーする v1.3.1 機能 | 26/26 |

## 使い方

各 JSON を `domain-model.json` として配置し、`json-to-models` を実行すれば、
Papyrus 7.1.0 で開ける `*_class-model-emf.uml` が生成されます。

```bash
python3 generate.py verify-mini.json --xmi-format=both
# または
python3 generate.py verify-comprehensive.json --xmi-format=emf
```

詳細は本スキルの README.md と SKILL.md を参照してください。
