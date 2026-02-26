#!/usr/bin/env python3
"""
Interactive Workflow Executor
段階的実行モードを対話的に設定してワークフローを実行
"""

import sys
import os
from typing import Optional

# スキルのscriptsディレクトリをパスに追加
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# フォールバック
sys.path.append('/mnt/skills/user/uml-workflow-v3/scripts')
sys.path.append('/mnt/user-data/outputs')

from execution_mode_manager import (
    ExecutionPlanner,
    ExecutionConfig,
    SkillStep,
    ExecutionMode,
    print_execution_plan
)

def ask_yes_no(question: str, default: bool = True) -> bool:
    """Yes/No質問"""
    default_str = "Y/n" if default else "y/N"
    response = input(f"{question} ({default_str}): ").strip().lower()
    
    if not response:
        return default
    return response in ['y', 'yes', 'はい']

def ask_choice(question: str, choices: list, default: int = 0) -> int:
    """選択肢から選ぶ"""
    print(f"\n{question}")
    for i, choice in enumerate(choices):
        marker = "→" if i == default else " "
        print(f"  {marker} {i+1}. {choice}")
    
    while True:
        response = input(f"\n選択 (1-{len(choices)}, デフォルト={default+1}): ").strip()
        
        if not response:
            return default
        
        try:
            choice = int(response) - 1
            if 0 <= choice < len(choices):
                return choice
        except ValueError:
            pass
        
        print("❌ 無効な選択です。もう一度入力してください。")

def configure_execution_interactive() -> ExecutionConfig:
    """対話的に実行設定を構築"""
    
    print("=" * 70)
    print("UML Workflow - 段階的実行モード設定")
    print("=" * 70)
    print()
    
    # 実行モードの選択
    modes = [
        "フルワークフロー（全ステップ実行）",
        "指定ステップから再開",
        "部分実行（開始と終了を指定）",
        "単一スキルのみ実行",
        "モデルのみ生成（コード生成なし）",
        "バリデーションのみ実行"
    ]
    
    mode_choice = ask_choice("実行モードを選択してください:", modes, default=0)
    
    # モードごとの設定
    if mode_choice == 0:  # フルワークフロー
        print("\n✅ フルワークフロー")
        generate_xmi = ask_yes_no(
            "XMIファイルを生成しますか？（いいえ推奨：40%高速化）",
            default=False  # デフォルトはOFF
        )
        generate_code = ask_yes_no("アプリケーションコードを生成しますか？", default=True)
        generate_tests = ask_yes_no("テストコードを生成しますか？", default=True)
        
        return ExecutionPlanner.create_full_workflow(
            generate_xmi=generate_xmi,
            generate_code=generate_code,
            generate_tests=generate_tests
        )
    
    elif mode_choice == 1:  # 指定ステップから再開
        print("\n✅ 指定ステップから再開")
        steps = [
            ("Step 1: シナリオ → アクティビティ図", SkillStep.SCENARIO_TO_ACTIVITY),
            ("Step 2: アクティビティ図 → ユースケース", SkillStep.ACTIVITY_TO_USECASE),
            ("Step 3: ユースケース → クラス図", SkillStep.USECASE_TO_CLASS),
            ("Step 4: クラス図 → ステートマシン図", SkillStep.CLASS_TO_STATEMACHINE),
            ("Step 5: ユースケース → シーケンス図", SkillStep.USECASE_TO_SEQUENCE),
            ("Step 6: モデルバリデーション", SkillStep.MODEL_VALIDATOR),
            ("Step 7: セキュリティ設計", SkillStep.SECURITY_DESIGN),
            ("Step 8: コード生成", SkillStep.USECASE_TO_CODE),
            ("Step 9: テスト生成", SkillStep.USECASE_TO_TEST),
        ]
        
        step_names = [name for name, _ in steps]
        step_choice = ask_choice("どのステップから再開しますか？", step_names, default=0)
        start_step = steps[step_choice][1]
        
        generate_xmi = ask_yes_no(
            "XMIファイルを生成しますか？（いいえ推奨：40%高速化）",
            default=False  # デフォルトはOFF
        )
        generate_code = ask_yes_no("コード生成を含めますか？", default=True)
        
        return ExecutionPlanner.create_resume_from(
            start_step=start_step,
            generate_xmi=generate_xmi,
            generate_code=generate_code
        )
    
    elif mode_choice == 2:  # 部分実行
        print("\n✅ 部分実行")
        steps = [
            ("Step 1: シナリオ → アクティビティ図", SkillStep.SCENARIO_TO_ACTIVITY),
            ("Step 2: アクティビティ図 → ユースケース", SkillStep.ACTIVITY_TO_USECASE),
            ("Step 3: ユースケース → クラス図", SkillStep.USECASE_TO_CLASS),
            ("Step 4: クラス図 → ステートマシン図", SkillStep.CLASS_TO_STATEMACHINE),
            ("Step 5: ユースケース → シーケンス図", SkillStep.USECASE_TO_SEQUENCE),
            ("Step 6: モデルバリデーション", SkillStep.MODEL_VALIDATOR),
            ("Step 7: セキュリティ設計", SkillStep.SECURITY_DESIGN),
        ]
        
        step_names = [name for name, _ in steps]
        
        start_choice = ask_choice("開始ステップを選択:", step_names, default=0)
        end_choice = ask_choice("終了ステップを選択:", step_names, default=len(steps)-1)
        
        start_step = steps[start_choice][1]
        end_step = steps[end_choice][1]
        
        generate_xmi = ask_yes_no(
            "XMIファイルを生成しますか？（いいえ推奨：40%高速化）",
            default=False  # デフォルトはOFF
        )
        
        return ExecutionPlanner.create_partial(
            start_step=start_step,
            end_step=end_step,
            generate_xmi=generate_xmi
        )
    
    elif mode_choice == 3:  # 単一スキル
        print("\n✅ 単一スキル実行")
        skills = [
            ("シナリオ → アクティビティ図", SkillStep.SCENARIO_TO_ACTIVITY),
            ("アクティビティ図 → ユースケース", SkillStep.ACTIVITY_TO_USECASE),
            ("ユースケース → クラス図", SkillStep.USECASE_TO_CLASS),
            ("クラス図 → ステートマシン図", SkillStep.CLASS_TO_STATEMACHINE),
            ("ユースケース → シーケンス図", SkillStep.USECASE_TO_SEQUENCE),
            ("モデルバリデーション", SkillStep.MODEL_VALIDATOR),
            ("セキュリティ設計", SkillStep.SECURITY_DESIGN),
            ("コード生成", SkillStep.USECASE_TO_CODE),
            ("テスト生成", SkillStep.USECASE_TO_TEST),
            ("JSON → モデル変換", SkillStep.JSON_TO_MODELS),
        ]
        
        skill_names = [name for name, _ in skills]
        skill_choice = ask_choice("実行するスキルを選択:", skill_names, default=0)
        skill = skills[skill_choice][1]
        
        generate_xmi = ask_yes_no(
            "XMIファイルを生成しますか？（いいえ推奨：40%高速化）",
            default=False  # デフォルトはOFF
        )
        
        return ExecutionPlanner.create_single_skill(
            skill=skill,
            generate_xmi=generate_xmi
        )
    
    elif mode_choice == 4:  # モデルのみ
        print("\n✅ モデル生成のみ（コード生成なし）")
        include_diagrams = ask_yes_no(
            "追加の図（ステートマシン、シーケンス）を生成しますか？",
            default=True
        )
        
        return ExecutionPlanner.create_models_only(
            include_diagrams=include_diagrams
        )
    
    elif mode_choice == 5:  # バリデーションのみ
        print("\n✅ バリデーションのみ実行")
        return ExecutionPlanner.create_validate_only()
    
    # デフォルト（念のため）
    return ExecutionPlanner.create_full_workflow()

def estimate_token_savings(config: ExecutionConfig) -> dict:
    """Token削減効果を推定"""
    # 各ステップの推定token消費量（概算）
    step_tokens = {
        SkillStep.SCENARIO_TO_ACTIVITY: 15000,
        SkillStep.ACTIVITY_TO_USECASE: 18000,
        SkillStep.USECASE_TO_CLASS: 12000,
        SkillStep.CLASS_TO_STATEMACHINE: 8000,
        SkillStep.USECASE_TO_SEQUENCE: 10000,
        SkillStep.MODEL_VALIDATOR: 5000,
        SkillStep.SECURITY_DESIGN: 8000,
        SkillStep.USECASE_TO_CODE: 25000,
        SkillStep.USECASE_TO_TEST: 8000,
    }
    
    # XMI生成が影響するステップ
    xmi_affected_steps = [
        SkillStep.SCENARIO_TO_ACTIVITY,
        SkillStep.ACTIVITY_TO_USECASE,
        SkillStep.USECASE_TO_CLASS,
    ]
    
    # フルワークフローの総token数
    full_workflow_tokens = sum(step_tokens.values())
    
    # 実行計画に基づいて実際のtoken数を計算
    plan = config.get_execution_plan()
    actual_tokens = 0
    
    for step in plan:
        base_tokens = step_tokens.get(step, 0)
        
        # XMI生成OFFの場合、影響を受けるステップで40%削減
        if not config.generate_xmi and step in xmi_affected_steps:
            actual_tokens += int(base_tokens * 0.6)  # 40%削減
        else:
            actual_tokens += base_tokens
    
    saved_tokens = full_workflow_tokens - actual_tokens
    savings_percent = (saved_tokens / full_workflow_tokens * 100) if full_workflow_tokens > 0 else 0
    
    # XMI OFFによる追加削減の内訳
    xmi_savings = 0
    if not config.generate_xmi:
        for step in plan:
            if step in xmi_affected_steps:
                xmi_savings += int(step_tokens.get(step, 0) * 0.4)
    
    return {
        "full_workflow_tokens": full_workflow_tokens,
        "actual_tokens": actual_tokens,
        "saved_tokens": saved_tokens,
        "savings_percent": savings_percent,
        "xmi_savings": xmi_savings,
        "xmi_enabled": config.generate_xmi
    }

def main():
    """メイン処理"""
    
    # 対話的に設定を構築
    config = configure_execution_interactive()
    
    # 実行計画を表示
    print()
    print_execution_plan(config)
    
    # Token削減効果を表示
    print()
    print("=" * 70)
    print("推定Token削減効果")
    print("=" * 70)
    
    savings = estimate_token_savings(config)
    print(f"フルワークフロー: {savings['full_workflow_tokens']:,} tokens")
    print(f"この設定での消費: {savings['actual_tokens']:,} tokens")
    print(f"削減量: {savings['saved_tokens']:,} tokens ({savings['savings_percent']:.1f}%削減)")
    
    if savings['xmi_savings'] > 0:
        print(f"  └─ XMI生成OFF効果: {savings['xmi_savings']:,} tokens")
    
    print("=" * 70)
    
    # 確認
    print()
    proceed = ask_yes_no("この設定で実行しますか？", default=True)
    
    if proceed:
        print("\n✅ 実行設定が確定しました")
        print("\n📝 次のステップ:")
        print("   1. この設定をuml-workflowスキルに渡す")
        print("   2. 各ステップで設定に従って実行/スキップを判断")
        print("   3. キャッシュシステムと組み合わせて最大効率化")
        print()
        print("💡 この設定はconfig.jsonとして保存できます")
        
        # 設定をJSON形式で保存（オプション）
        save_config = ask_yes_no("設定をファイルに保存しますか？", default=False)
        if save_config:
            import json
            config_dict = config.get_summary()
            
            output_path = "/mnt/user-data/outputs/workflow_execution_config.json"
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, indent=2, ensure_ascii=False)
            
            print(f"\n✅ 設定を保存しました: {output_path}")
    else:
        print("\n❌ 実行をキャンセルしました")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ 中断されました")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ エラーが発生しました:")
        print(f"   {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
