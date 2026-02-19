# Migration Guide（既存ユーザー向け）

> **初めてインストールする方はこのファイルは不要です。**
> `INSTALL.md` を参照してください。

---

## uml-workflow-v2-enhanced → uml-workflow-v3 への移行手順

### 変更の概要

uml-workflow-v2-enhanced を **uml-workflow-v3** に改称しました。
機能的な変更はなく、名称のシンプル化が目的です。

### スキルフォルダの変更

| 変更前 | 変更後 |
|--------|--------|
| `uml-workflow-v2-enhanced/` | `uml-workflow-v3/` |

### Claude への呼び出し方

| 変更前 | 変更後 |
|--------|--------|
| `uml-workflow-v2-enhancedで〜` | `uml-workflow-v3で〜` |

### 関連スキルの更新

以下のスキルファイルを、このパッケージ同梱の最新版に差し替えてください：

| スキル | 変更内容 |
|--------|---------|
| `usecase-to-code-v1/SKILL.md` | `uml-workflow-v2-enhanced` → `uml-workflow-v3` |
| `classdiagram-image-to-json/SKILL.md` | `uml-workflow-v2` → `uml-workflow-v3` |
| `classdiagram-image-to-json/README.md` | `uml-workflow-v2` → `uml-workflow-v3` |
| `scenario-to-activity-v1/SKILL.md` | `uml-workflow-v2` → `uml-workflow-v3` |

最新版はこのパッケージの `skills/` フォルダに含まれています。

### キャッシュについて

既存のキャッシュはそのまま利用できます。
キャッシュはプロジェクト名ベースで管理されているため、スキル名変更の影響を受けません。
