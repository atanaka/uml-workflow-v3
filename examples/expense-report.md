# Example: 経費申請システム / Expense Report Management System

UML Workflow v3 のデモ用シナリオです。Claude.ai で新しい会話を開き、以下のテキストをそのまま貼り付けてください。

This is a demo scenario for UML Workflow v3. Open a new conversation in Claude.ai and paste the text below directly.

---

## 使い方 / How to Use

**日本語で実行する場合 / To run in Japanese:**

```
uml-workflow-v3を使って、以下のビジネスシナリオからアプリケーションを生成してください。
```

その後、下記の「シナリオ（日本語）」セクションの内容を貼り付けてください。  
Then paste the content from the "シナリオ（日本語）" section below.

**To run in English:**

```
Use uml-workflow-v3 to generate an application from the following business scenario.
```

Then paste the content from the "Scenario (English)" section below.

---

## シナリオ（日本語）/ Scenario (Japanese)

### ビジネス概要

中規模企業（従業員200名）の経費精算業務をデジタル化するWebアプリケーションを開発する。現在は紙の申請書で運用しており、承認プロセスに平均5営業日かかっている。これを1営業日以内に短縮することが目標。

### アクター

- **従業員（Employee）**: 経費申請を作成・提出する
- **上長（Manager）**: 部下の経費申請を承認または却下する
- **経理担当（Accountant）**: 承認済み申請の精算処理を行う
- **システム管理者（Admin）**: ユーザー管理、マスタデータ管理を行う

### 業務フロー

1. 従業員が経費申請を作成する（日付、金額、カテゴリ、領収書画像を入力）
2. 申請を提出すると、上長にメール通知が送られる
3. 上長が申請内容を確認し、承認または却下する
   - 却下の場合、理由を記入し従業員に差し戻す
   - 従業員は修正して再提出できる（2回まで）
4. 承認された申請は経理担当に転送される
5. 経理担当が精算処理を行い、振込手続きを完了する
6. 従業員に精算完了の通知が送られる

### ビジネスルール

- 10万円以上の申請は部長承認が追加で必要（二段階承認）
- 申請カテゴリ: 交通費、宿泊費、接待交際費、消耗品費、その他
- 領収書添付は5,000円以上の申請で必須
- 月末締め、翌月15日払い
- 却下後の再提出は2回まで

### 用語集

| 用語 | 説明 |
|------|------|
| 経費申請 | 業務で発生した費用の精算を会社に求める申請 |
| 精算 | 承認された申請に対して実際に金銭を支払う処理 |
| 二段階承認 | 直属の上長に加えて部長の承認も必要な申請フロー |

### 非機能要件

- レスポンシブデザイン（PC・スマートフォン対応）
- 日本語UI（英語への切替は不要）
- ログイン認証（メールアドレス + パスワード）
- 操作ログの記録（監査目的）
- 可用性: 平日業務時間中（9:00–18:00）に99.5%以上

---

## Scenario (English)

### Business Overview

Develop a web application to digitize expense reimbursement operations for a mid-sized company (200 employees). Currently running on paper forms, the approval process takes an average of 5 business days. The goal is to reduce this to within 1 business day.

### Actors

- **Employee**: Creates and submits expense reports
- **Manager**: Approves or rejects subordinates' expense reports
- **Accountant**: Processes approved reports for reimbursement
- **System Administrator (Admin)**: Manages users and master data

### Business Flow

1. An employee creates an expense report (enters date, amount, category, and attaches receipt image)
2. When submitted, the manager receives an email notification
3. The manager reviews the report and either approves or rejects it
   - If rejected, the manager writes a reason and returns it to the employee
   - The employee can revise and resubmit (up to 2 times)
4. Approved reports are forwarded to the accountant
5. The accountant processes the reimbursement and completes the bank transfer
6. The employee receives a reimbursement completion notification

### Business Rules

- Reports over ¥100,000 require additional approval from the department head (two-level approval)
- Expense categories: Transportation, Accommodation, Entertainment, Supplies, Other
- Receipt attachment is required for reports over ¥5,000
- Monthly cutoff; payment on the 15th of the following month
- Resubmission after rejection is allowed up to 2 times

### Glossary

| Term | Definition |
|------|-----------|
| Expense Report | A request to the company to reimburse costs incurred for business purposes |
| Reimbursement | The process of actually paying money against an approved expense report |
| Two-level approval | An approval flow requiring both the direct manager and department head to approve |

### Non-Functional Requirements

- Responsive design (PC and smartphone support)
- English UI
- Login authentication (email address + password)
- Operation logging (for audit purposes)
- Availability: ≥99.5% during business hours (9:00–18:00) on weekdays

---

## 期待される出力 / Expected Outputs

ワークフローが完了すると、以下が生成されます：

When the workflow completes, the following will be generated:

| # | 出力 / Output | 形式 / Format | ステップ / Step |
|---|--------------|-------------|--------------|
| 1 | アクティビティ図 / Activity diagram | PlantUML | Step 1 |
| 2 | ユースケース図 + 仕様書 / Use case diagram + specs | PlantUML + Markdown | Step 2 |
| 3 | クラス図（ドメインモデル）/ Class diagram (domain model) | PlantUML + JSON | Step 3 |
| 4 | ステートマシン図 / State machine diagram | PlantUML | Step 4 |
| 5 | シーケンス図 / Sequence diagram | PlantUML | Step 5 |
| 6 | バリデーションレポート / Validation report | Markdown | Step 6 |
| 7 | セキュリティ設計 / Security design | JSON | Step 7 |
| 8 | アプリケーションコード / Application code | TypeScript/React | Step 8 |
| 9 | テストコード / Test code | Jest + Playwright | Step 9 |
| 10 | トレーサビリティマトリクス / Traceability matrix | JSON + Markdown | Step 10 |

---

## 推奨オプション / Recommended Options

このシナリオを使う際の推奨設定：

Recommended settings for this scenario:

| 設定 / Setting | 推奨値 / Recommended Value |
|--------------|--------------------------|
| プロジェクト名 / Project name | `expense-management` |
| 実行モード / Execution mode | フルワークフロー / Full workflow |
| XMI生成 / XMI output | いいえ / No |
| 出力言語 / Output language | 日本語 または English |
| テスト生成 / Generate tests | はい / Yes |
| テックスタック / Tech stack | Express + React（デフォルト / default）|

---

## このシナリオの学習ポイント / Learning Points from this Scenario

このサンプルシナリオを実行することで、以下の機能を体験できます：

Running this sample scenario lets you experience the following features:

- **多アクターのシステム** — 4つのアクターがどのようにユースケースに分解されるかを確認できます  
  **Multi-actor system** — See how 4 actors decompose into use cases

- **条件付きフロー** — 「却下 → 差し戻し → 再提出」という代替フローがシーケンス図でどう表現されるかを確認できます  
  **Conditional flows** — See how the "Reject → Return → Resubmit" alternative flow appears in sequence diagrams

- **二段階承認** — ビジネスルールがステートマシン図・コード・テストにどのように反映されるかを確認できます  
  **Two-level approval** — See how a business rule is reflected in state machine, code, and tests

- **ステータス管理** — ExpenseReport エンティティの状態遷移（DRAFT → SUBMITTED → APPROVED / REJECTED → SETTLED）がステートマシン図でどう表現されるかを確認できます  
  **Status management** — See the state transitions (DRAFT → SUBMITTED → APPROVED / REJECTED → SETTLED) in the state machine diagram

- **トレーサビリティ** — 「10万円以上の申請には部長承認が必要」というルールが、どのユースケース・クラス・テストと結びついているかをマトリクスで確認できます  
  **Traceability** — In the matrix, see which use cases, classes, and tests are linked to the rule "reports over ¥100,000 require department head approval"
