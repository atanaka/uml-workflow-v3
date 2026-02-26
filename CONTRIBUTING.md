# Contributing Guide / コントリビューションガイド

UML Workflow v3 へのコントリビューションを歓迎します。  
We welcome contributions to UML Workflow v3.

---

## How to Contribute / 貢献の方法

### Bug Reports / バグ報告

[Issues](../../issues) からバグ報告を作成してください。以下の情報を含めると大変助かります：

Please create a bug report via [Issues](../../issues). Including the following information helps greatly:

- 使用した Claude.ai のプラン（Pro / Max / Team / Enterprise）  
  The Claude.ai plan used (Pro / Max / Team / Enterprise)
- 実行したステップとステップ番号  
  The step(s) executed and step number(s)
- 入力シナリオの概要（機密情報は除いてください）  
  A summary of the input scenario (omit confidential information)
- エラーメッセージまたは期待と異なった動作の説明  
  Error messages or description of unexpected behavior
- 再現手順  
  Steps to reproduce the issue

### Feature Requests / 機能提案

新しいステップの追加や既存機能の改善提案は Issue として起票してください。  
For new steps or improvements to existing features, please create an Issue.

提案には以下を含めてください / Please include:
- 提案する機能の概要 / Summary of the proposed feature
- ユースケース（どんな場面で役立つか）/ Use case (what problem it solves)
- 実現可能な実装アイデア（あれば）/ Implementation ideas if any

### Pull Requests

1. リポジトリを Fork する / Fork the repository
2. フィーチャーブランチを作成する / Create a feature branch  
   `git checkout -b feature/my-feature`
3. 変更をコミットする / Commit changes  
   `git commit -m "feat: add my feature"`
4. Pull Request を作成する / Create a Pull Request

---

## Development Guidelines / 開発ガイドライン

### Skill Structure / スキル構造

各スキルは以下の構造に従ってください：

Each skill should follow this structure:

```
skill-name/
├── SKILL.md          ← 必須 Required: frontmatter (name, description) + 実行手順 execution instructions
├── references/       ← オプション Optional: 参照スキル referenced sub-skills
├── scripts/          ← オプション Optional: Python スクリプト Python scripts
└── README.md         ← オプション Optional: ユーザー向け説明 user-facing documentation
```

### SKILL.md Frontmatter

```yaml
---
name: skill-name
description: |
  200文字以内の説明（Claude.ai の制約）
  Description within 200 characters (Claude.ai constraint)
---
```

### Key Constraints / 制約事項

| 項目 / Item | 制約 / Constraint |
|------------|-----------------|
| `description` フィールド | **200文字以下** (Claude.ai 制約) / **≤ 200 characters** (Claude.ai constraint) |
| `SKILL.md` ファイルサイズ | 500行以下推奨 / ≤ 500 lines recommended |
| ZIP 構成 | 1 ZIP = 1 スキル。`skill-name/SKILL.md` の形式 / 1 ZIP = 1 skill, format: `skill-name/SKILL.md` |
| 言語対応 | 日本語・英語の**両方**に対応すること / Support **both** Japanese and English |
| references スキル | SKILL.md の description のみ参照される / Only description is referenced from parent SKILL.md |

### Bilingual Requirement / バイリンガル要件

すべてのドキュメント（README.md、CHANGELOG.md、コメント等）は日本語と英語の**両方**を含める必要があります。  
All documentation (README.md, CHANGELOG.md, comments, etc.) must include **both** Japanese and English.

**推奨フォーマット / Recommended format:**

```markdown
## セクションタイトル / Section Title

日本語の説明文をここに書きます。  
Write the English description here.

| 項目 / Item | 値 / Value |
|------------|-----------|
| 日本語 / Japanese | ... |
```

### Commit Message Convention / コミットメッセージ規約

[Conventional Commits](https://www.conventionalcommits.org/) を推奨します：

We recommend [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add Step 11 for deployment generation
fix: correct cache key naming for Step 3
docs: update README bilingual sections
refactor: split SKILL.md into modular references
test: add test scenario for large-scale input
```

### Testing / テスト

スキルの変更後は、以下のシナリオで動作確認をしてください：

After modifying a skill, verify with the following test scenarios:

1. **フルワークフロー / Full workflow** — 新しい会話で Step 1–10 を通しで実行 / Run Steps 1–10 in a new conversation
2. **途中再開 / Resume** — Step 3 からの再開が正常に動作すること / Confirm resume from Step 3 works correctly
3. **単一ステップ / Single step** — Step 6（バリデーション）の単独実行 / Run Step 6 (validation) in isolation
4. **モデルのみ / Model only** — Step 8–9 がスキップされること / Confirm Steps 8–9 are skipped
5. **ヘルパースキル / Helper skills** — 画像取込・Markdown 変換が動作すること / Confirm image import and Markdown conversion work

テストシナリオの詳細は [skills/uml-workflow-v3/TEST_SCENARIOS.md](skills/uml-workflow-v3/TEST_SCENARIOS.md) を参照してください。  
For detailed test scenarios, see [skills/uml-workflow-v3/TEST_SCENARIOS.md](skills/uml-workflow-v3/TEST_SCENARIOS.md).

---

## File Map / ファイルマップ

コントリビューション時に参考にすべきファイル一覧：

Key files to reference when contributing:

```
uml-workflow-v3/
├── README.md                         ← プロジェクト概要 / Project overview (this repo)
├── CHANGELOG.md                      ← 変更履歴 / Change history
├── CONTRIBUTING.md                   ← このファイル / This file
├── LICENSE
│
├── docs/
│   ├── USER_GUIDE.md                 ← 詳細ユーザーガイド / Detailed user guide
│   ├── ARCHITECTURE.md               ← アーキテクチャ / Architecture overview
│   ├── INSTALLATION_GUIDE.md         ← インストール手順（日本語）
│   └── INSTALLATION_GUIDE_EN.md      ← Installation guide (English)
│
├── examples/
│   └── expense-report.md             ← サンプルシナリオ / Sample scenario
│
└── skills/
    ├── uml-workflow-v3/              ← メインスキル / Main skill
    │   ├── SKILL.md                  ← Claude 向け実行仕様 / Claude execution spec
    │   ├── README.md                 ← スキル説明（ユーザー向け）/ Skill docs (user-facing)
    │   ├── INSTALL.md
    │   ├── references/               ← 10個のパイプラインスキル / 10 pipeline skills
    │   └── scripts/                  ← Python 実行エンジン / Python execution engine
    ├── usecase-md-to-json/
    ├── classdiagram-image-to-json/
    ├── json-to-models/
    └── classdiagram-to-crud/
```

---

## Code of Conduct / 行動規範

すべての参加者は、建設的で敬意のあるコミュニケーションを心がけてください。  
All participants are expected to maintain constructive and respectful communication.

- 他者の意見を尊重する / Respect others' opinions
- 建設的なフィードバックを行う / Provide constructive feedback
- 多様な背景を持つコントリビューターを歓迎する / Welcome contributors from diverse backgrounds

---

## Questions? / ご質問は？

GitHub の [Discussions](../../discussions) または [Issues](../../issues) でお気軽にご質問ください。  
Feel free to ask questions in [Discussions](../../discussions) or [Issues](../../issues).
