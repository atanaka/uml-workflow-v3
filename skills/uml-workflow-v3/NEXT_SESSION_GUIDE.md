# 次回セッション作業ガイド

## 📅 セッション情報

**最終更新**: 2026年2月19日  
**ステータス**: uml-workflow-v3 本番稼働中・スキル群継続改善中

---

## ✅ 完成済み（すべて本番稼働中）

### 1. uml-workflow-v3（旧称: uml-workflow-v2-enhanced）

- ✅ 全9ステップの完全自動実行
- ✅ インテリジェントキャッシュシステム
- ✅ 5種類の実行モード（full / resume / models-only / validate-only / single）
- ✅ XMI最適化（デフォルトOFF、40%高速化）
- ✅ security-design-v1 を Step 7 として統合
- ✅ Step 8/9 に security-config.json を渡す記述を追加（2026-02-19）
- ✅ b2b-ec-order プロジェクトで全9ステップ実行・完走確認済み

**ワークフロー構成:**
```
Step 1: scenario-to-activity-v1    ビジネスシナリオ → アクティビティ図
Step 2: activity-to-usecase-v1     アクティビティ図 → ユースケース
Step 3: usecase-to-class-v1        ユースケース → クラス図・ドメインモデル
Step 4: class-to-statemachine-v1   クラス図 → ステートマシン図
Step 5: usecase-to-sequence-v1     ユースケース → シーケンス図
Step 6: model-validator-v1         モデル検証
Step 7: security-design-v1         セキュリティ設計 → security-config.json
Step 8: usecase-to-code-v1         フルスタックコード生成
Step 9: usecase-to-test-v1         テストコード生成
```

---

### 2. サブスキル群（全13件）

| スキル | 状態 | 最終更新 |
|--------|------|---------|
| scenario-to-activity-v1 | ✅ 稼働中 | — |
| activity-to-usecase-v1 | ✅ 稼働中 | — |
| usecase-to-class-v1 | ✅ 稼働中・**改善済み** | 2026-02-19 |
| class-to-statemachine-v1 | ✅ 稼働中 | — |
| usecase-to-sequence-v1 | ✅ 稼働中 | — |
| model-validator-v1 | ✅ 稼働中 | — |
| security-design-v1 | ✅ 稼働中 | — |
| usecase-to-code-v1 | ✅ 稼働中・**改善済み** | 2026-02-19 |
| usecase-to-test-v1 | ✅ 稼働中・**改善済み** | 2026-02-19 |
| json-to-models | ✅ 稼働中 | — |
| usecase-md-to-json | ✅ 稼働中 | — |
| classdiagram-image-to-json | ✅ 稼働中 | — |
| uml-workflow-v1 | ✅ 稼働中（旧版） | — |

---

### 3. 主要スキルの最新仕様

#### usecase-to-code-v1（v1.2）

- **Step 3.5（セキュリティインフラ生成）を追加**
  - `security-config.json` が存在する場合のみ自動実行
  - 生成物:
    - `infrastructure/crypto.ts`（AES-256-GCM暗号化）
    - `infrastructure/AuditLogger.ts`（監査ログ）
    - `presentation/middleware/auth.ts`（JWT認証+RBAC認可）
    - `app.ts`（helmet / CORS / rateLimit 組み込み）
    - `.env.example`（JWT_SECRET, ENCRYPTION_KEY等）

#### usecase-to-test-v1

- **Security Tests セクションを追加**
  - `security-config.json` が存在する場合に `tests/security/` 以下の6ファイルを自動生成
  - auth.test.ts / authorization.test.ts / rate-limit.test.ts
  - encryption.test.ts / audit.test.ts / headers.test.ts

#### usecase-to-class-v1

PlantUMLビューワー互換のため3ルールを追加（2026-02-19）:

| ルール | 内容 |
|--------|------|
| **ルール A** | enum は必ず改行形式（1行スラッシュ/カンマ区切り禁止） |
| **ルール B** | 関連線は標準クラス図記法（カラス足記法禁止）、多重度を両端に明示 |
| **ルール C** | アクターは `class` + `<<actor>>` ステレオタイプ（`actor` キーワード禁止） |

- **日本語版クラス図（`_class_J.puml`）を英語版と同時生成する仕様を追加**
  - ファイル名: `{project}_class_J.puml`
  - クラス名・属性名・メソッド名・enum名/値をすべて `japanese_name` から変換
  - 用途: モデラーによるレビュー専用（コード生成には英語版を使用）

---

### 4. デモプロジェクト（b2b-ec-order）

全9ステップ実行済み。最新パッケージ: `b2b-ec-order-complete-v4.zip`（112KB / 66ファイル）

**UMLモデル:**
```
b2b-ec-order_activity-data.json
b2b-ec-order_activity.puml
b2b-ec-order_usecase-output.json
b2b-ec-order_usecase-diagram.puml
b2b-ec-order_domain-model.json
b2b-ec-order_class.puml          ← ルールA/B/C適用済み
b2b-ec-order_class_J.puml        ← 日本語版（新規追加）
b2b-ec-order_statemachine.puml
b2b-ec-order_sequence.puml
b2b-ec-order_validation-report.md
b2b-ec-order_security-design.md
b2b-ec-order_security-config.json
usecase-specifications/（UC-001〜UC-004）
```

**バックエンド実装:**
```
backend/src/
├── app.ts                              # helmet/CORS/rateLimit
├── domain/entities/Order.ts
├── application/usecases/
│   ├── PlaceOrderUseCase.ts
│   └── ApproveCreditOverrunUseCase.ts
├── infrastructure/
│   ├── crypto.ts                       # AES-256-GCM
│   └── AuditLogger.ts
└── presentation/
    ├── middleware/auth.ts              # JWT+RBAC
    └── routes/routes.ts
```

**テスト（テストバグ3件修正済み）:**
```
tests/unit/domain.test.ts
tests/integration/usecases.test.ts
tests/security/auth.test.ts
tests/security/authorization.test.ts
tests/security/rate-limit.test.ts
tests/security/encryption.test.ts      ← import先をcrypto.tsに修正済み
tests/security/audit.test.ts           ← createdAt不整合修正済み
tests/security/headers.test.ts         ← beforeAllインポート追加済み
tests/e2e/order-flow.spec.ts
```

---

## 🔄 GitHubへの反映待ち（要対応）

以下の4ファイルを `/mnt/user-data/outputs/github-update/` に準備済み。
GitHubリポジトリの対応パスに上書きアップロードすること。

| ダウンロードファイル | GitHub上のパス |
|--------------------|---------------|
| `uml-workflow-v3_SKILL.md` | `uml-workflow-v3/SKILL.md` |
| `usecase-to-code-v1_SKILL.md` | `skills/usecase-to-code-v1/SKILL.md` |
| `usecase-to-test-v1_SKILL.md` | `skills/usecase-to-test-v1/SKILL.md` |
| `usecase-to-class-v1_SKILL.md` | `skills/usecase-to-class-v1/SKILL.md` |

---

## 🎯 今後の改善候補

### 優先度：高

- **他のPumlファイルのビューワー互換性確認**
  - statemachine.puml / sequence.puml / activity.puml で同様のエラーが出る可能性
  - 各スキルに同様のルールを追加する必要が生じる可能性あり

- **usecase-to-class-v1 再実行時のdownstream影響範囲の定義**
  - class.puml / domain-model.json が変わった場合、どのステップまで再実行が必要かをSKILL.mdに明記

### 優先度：中

- **日本語版pumlの他スキルへの展開**
  - statemachine / sequence / activity でも `_J.puml` を生成する需要があるか確認

- **b2b-ec-order フロントエンド確認**
  - `frontend/src/` 以下が brace expansion 問題で未生成の可能性（要確認）

### 優先度：低

- **GitHub公開用 README の更新**
  - security-design-v1 統合、usecase-to-class-v1 の3ルール追加、`_class_J.puml` を反映

---

## 📋 次回セッション開始時のチェックリスト

```
□ /mnt/user-data/outputs/github-update/ の4ファイルをGitHubにアップロード済みか確認
□ b2b-ec-order-complete-v4.zip が最新か確認
□ 新しい改善要望があれば該当スキルのSKILL.mdを修正後、github-update/ にコピー
```

---

## 📦 重要ファイルの場所

```
Claudeインストール済みスキル（/mnt/skills/user/）:
  uml-workflow-v2-enhanced/SKILL.md   ← v3本体（Claude内スキル名はv2-enhanced）
  usecase-to-class-v1/SKILL.md
  usecase-to-code-v1/SKILL.md
  usecase-to-test-v1/SKILL.md

GitHub更新用（ダウンロード可能）:
  /mnt/user-data/outputs/github-update/（4ファイル）

デモプロジェクト:
  /home/claude/b2b-ec-order/
  /mnt/user-data/outputs/b2b-ec-order-complete-v4.zip
  /mnt/user-data/outputs/b2b-ec-order/（個別ファイル）
```
