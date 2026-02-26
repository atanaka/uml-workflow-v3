# Contributing / コントリビューションガイド

UML Workflow v3 へのコントリビューションを歓迎します。

## How to Contribute / 貢献の方法

### Bug Reports / バグ報告

[Issues](../../issues) からバグ報告を作成してください。以下の情報を含めていただけると助かります：

- 使用した Claude.ai のプラン（Pro / Max / Team / Enterprise）
- 実行したステップと入力シナリオの概要
- エラーメッセージまたは期待と異なった動作の説明
- 再現手順

### Feature Requests / 機能提案

新しいステップの追加や既存機能の改善提案は、Issue として起票してください。

### Pull Requests

1. リポジトリを Fork
2. フィーチャーブランチを作成（`git checkout -b feature/my-feature`）
3. 変更をコミット
4. Pull Request を作成

## Development Guidelines / 開発ガイドライン

### Skill Structure / スキル構造

各スキルは以下の構造に従ってください：

```
skill-name/
├── SKILL.md          ← 必須: frontmatter (name, description) + 実行手順
├── references/       ← オプション: 参照スキル
├── scripts/          ← オプション: Python スクリプト
└── README.md         ← オプション: ユーザー向け説明
```

### SKILL.md Frontmatter

```yaml
---
name: skill-name
description: 200文字以内の説明（Claude.ai の制約）
---
```

### Key Constraints / 制約事項

| Item | Constraint |
|------|-----------|
| `description` | 200文字以下（Claude.ai） |
| `SKILL.md` | 500行以下推奨 |
| ZIP 構成 | 1 ZIP = 1 スキル（フォルダ直下に SKILL.md） |
| 言語 | 日本語・英語の両方に対応すること |

### Testing / テスト

スキルの変更後は、以下のシナリオで動作確認をしてください：

1. **フルワークフロー** — 新しい会話で Step 1-10 を通しで実行
2. **途中再開** — Step 3 からの再開が正常に動作すること
3. **単一ステップ** — Step 6（バリデーション）の単独実行
4. **ヘルパースキル** — 画像取込・Markdown 変換が動作すること

## Code of Conduct

すべての参加者は、建設的で敬意のあるコミュニケーションを心がけてください。
