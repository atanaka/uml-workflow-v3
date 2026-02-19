#!/usr/bin/env python3
"""
Executable Workflow Runner
Claude用の完全自動実行スクリプト
"""

import sys
import os

# パス設定
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# フォールバック
sys.path.append('/mnt/skills/user/uml-workflow-v3/scripts')
sys.path.append('/mnt/user-data/outputs/uml-workflow-v3-complete/scripts')

from execution_mode_manager import ExecutionPlanner, SkillStep
from unified_workflow_executor import UnifiedWorkflowExecutor
import json

def run_workflow(
    project_name: str,
    use_cache: str = "yes",  # "yes", "no", "clear"
    execution_mode: str = "full",  # "full", "resume", "models_only", "validate_only"
    start_step: int = 1,  # 1-9
    generate_xmi: bool = False,
    generate_tests: bool = True,
    run_security: bool = True,
    business_scenario: str = ""
):
    """
    ワークフローを実行
    
    Args:
        project_name: プロジェクト名
        use_cache: キャッシュ使用 ("yes", "no", "clear")
        execution_mode: 実行モード
        start_step: 開始ステップ（resume時）
        generate_xmi: XMI生成
        generate_tests: テスト生成
        business_scenario: ビジネスシナリオ（Step 1用）
    """
    
    print("=" * 80)
    print(f"UML Workflow v3 - Execution")
    print(f"Project: {project_name}")
    print("=" * 80)
    
    # キャッシュ設定
    from workflow_cache_helper import clear_project_cache, get_project_cache_summary
    
    if use_cache == "clear":
        print(f"\n🗑️ Clearing cache for {project_name}...")
        clear_project_cache(project_name)
        use_cache_bool = True
    elif use_cache == "no":
        use_cache_bool = False
    else:
        use_cache_bool = True
    
    # キャッシュ状況表示
    if use_cache_bool:
        cache_summary = get_project_cache_summary(project_name)
        if cache_summary['cached']:
            print(f"\n💾 Cache Status:")
            for step in cache_summary['steps']:
                print(f"   ✅ {step['step_name']}: {len(step['files'])} files")
        else:
            print(f"\n⚠️ No cache found (first run)")
    
    # 実行設定の構築
    print(f"\n⚙️ Building execution configuration...")
    
    if execution_mode == "full":
        config = ExecutionPlanner.create_full_workflow(
            generate_xmi=generate_xmi,
            generate_code=True,
            generate_tests=generate_tests,
            run_security=run_security
        )
    elif execution_mode == "resume":
        step_map = {
            1: SkillStep.SCENARIO_TO_ACTIVITY,
            2: SkillStep.ACTIVITY_TO_USECASE,
            3: SkillStep.USECASE_TO_CLASS,
            4: SkillStep.CLASS_TO_STATEMACHINE,
            5: SkillStep.USECASE_TO_SEQUENCE,
            6: SkillStep.MODEL_VALIDATOR,
            7: SkillStep.SECURITY_DESIGN,
            8: SkillStep.USECASE_TO_CODE,
            9: SkillStep.USECASE_TO_TEST,
        }
        config = ExecutionPlanner.create_resume_from(
            start_step=step_map.get(start_step, SkillStep.SCENARIO_TO_ACTIVITY),
            generate_xmi=generate_xmi,
            generate_code=True
        )
    elif execution_mode == "models_only":
        config = ExecutionPlanner.create_models_only(
            include_diagrams=True,
            generate_xmi=generate_xmi
        )
    elif execution_mode == "validate_only":
        config = ExecutionPlanner.create_validate_only()
    else:
        config = ExecutionPlanner.create_full_workflow(
            generate_xmi=generate_xmi,
            generate_code=True,
            generate_tests=generate_tests
        )
    
    # 統合実行管理の初期化
    executor = UnifiedWorkflowExecutor(project_name)
    executor.set_execution_config(config)
    executor.set_cache_usage(use_cache_bool)
    
    # 実行サマリー表示
    print(f"\n" + "=" * 80)
    executor.print_execution_summary()
    print("=" * 80)
    
    # Token削減効果の推定
    from interactive_workflow_executor import estimate_token_savings
    savings = estimate_token_savings(config)
    
    print(f"\n💡 Estimated Token Savings:")
    print(f"   Full workflow: {savings['full_workflow_tokens']:,} tokens")
    print(f"   This configuration: {savings['actual_tokens']:,} tokens")
    print(f"   Savings: {savings['saved_tokens']:,} tokens ({savings['savings_percent']:.1f}%)")
    if savings.get('xmi_savings', 0) > 0:
        print(f"   └─ XMI OFF: {savings['xmi_savings']:,} tokens")
    
    print(f"\n" + "=" * 80)
    
    # 実行計画の取得
    execution_plan = config.get_execution_plan()
    
    # 結果サマリー
    results = {
        "project_name": project_name,
        "execution_mode": execution_mode,
        "steps_executed": [],
        "steps_skipped": [],
        "steps_from_cache": [],
        "total_steps": len(execution_plan)
    }
    
    # 各ステップを実行
    for i, step in enumerate(execution_plan, 1):
        step_num = SkillStep.get_step_number(step)
        step_name = step.value
        
        print(f"\n{'='*80}")
        print(f"[{i}/{len(execution_plan)}] Step {step_num}: {step_name}")
        print(f"{'='*80}")
        
        # 実行判定
        should_execute, reason = executor.should_execute_step(step)
        
        if not should_execute:
            print(f"⏭️ SKIP - {reason}")
            results["steps_skipped"].append(step_name)
            continue
        
        # キャッシュチェック
        cache_info = executor.check_step_cache(step)
        
        if use_cache_bool and cache_info["has_cache"]:
            print(f"\n💾 Cache found:")
            for file_info in cache_info["files"]:
                print(f"   - {file_info['type']}")
            
            # 自動的にキャッシュを使用（デフォルト）
            print(f"\n✅ Using cached artifacts...")
            if executor.restore_from_cache(step):
                print(f"✅ Restored from cache successfully")
                results["steps_from_cache"].append(step_name)
                continue
            else:
                print(f"⚠️ Cache restore failed, will regenerate")
        
        # スキル実行が必要
        print(f"\n⚙️ Execution required")
        print(f"⚠️ Claude will need to call: {step_name}")
        print(f"   → This requires Claude to invoke the actual sub-skill")
        
        results["steps_executed"].append(step_name)
    
    # 完了サマリー
    print(f"\n" + "=" * 80)
    print(f"EXECUTION COMPLETE")
    print(f"=" * 80)
    print(f"Project: {project_name}")
    print(f"Steps executed: {len(results['steps_executed'])}")
    print(f"Steps from cache: {len(results['steps_from_cache'])}")
    print(f"Steps skipped: {len(results['steps_skipped'])}")
    print(f"\nActual token savings: ~{savings['savings_percent']:.0f}%")
    
    # 次のステップが必要なら表示
    if results["steps_executed"]:
        print(f"\n⚠️ ATTENTION:")
        print(f"The following steps require Claude to call sub-skills:")
        for step_name in results["steps_executed"]:
            print(f"   - {step_name}")
        print(f"\nClaude should now execute each of these sub-skills in sequence.")
    
    # 結果をJSONで保存
    output_file = f"/mnt/user-data/outputs/workflow_execution_result_{project_name}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Execution plan saved to: {output_file}")
    
    return results


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Execute UML Workflow v3')
    parser.add_argument('project_name', help='Project name')
    parser.add_argument('--cache', default='yes', choices=['yes', 'no', 'clear'],
                       help='Cache usage (default: yes)')
    parser.add_argument('--mode', default='full',
                       choices=['full', 'resume', 'models_only', 'validate_only'],
                       help='Execution mode (default: full)')
    parser.add_argument('--start-step', type=int, default=1, choices=range(1, 10),
                       help='Start step for resume mode (default: 1)')
    parser.add_argument('--xmi', action='store_true',
                       help='Generate XMI files (default: False)')
    parser.add_argument('--no-tests', action='store_true',
                       help='Skip test generation (default: False)')
    parser.add_argument('--no-security', action='store_true',
                       help='Skip security design (default: False)')
    
    args = parser.parse_args()
    
    run_workflow(
        project_name=args.project_name,
        use_cache=args.cache,
        execution_mode=args.mode,
        start_step=args.start_step,
        generate_xmi=args.xmi,
        generate_tests=not args.no_tests,
        run_security=not args.no_security
    )
