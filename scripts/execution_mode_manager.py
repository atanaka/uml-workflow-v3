#!/usr/bin/env python3
"""
Workflow Execution Mode Manager
段階的実行モードを管理するヘルパーモジュール
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from dataclasses import dataclass

class ExecutionMode(Enum):
    """実行モード"""
    FULL = "full"                      # 全スキル実行
    RESUME_FROM = "resume_from"        # 指定スキルから再開
    SINGLE_SKILL = "single_skill"      # 1スキルのみ実行
    VALIDATE_ONLY = "validate_only"    # バリデーションのみ
    PARTIAL = "partial"                # 部分実行（開始と終了を指定）

class SkillStep(Enum):
    """ワークフローのステップ定義（9ステップ）"""
    SCENARIO_TO_ACTIVITY = "scenario-to-activity-v1"
    ACTIVITY_TO_USECASE = "activity-to-usecase-v1"
    USECASE_TO_CLASS = "usecase-to-class-v1"
    CLASS_TO_STATEMACHINE = "class-to-statemachine-v1"
    USECASE_TO_SEQUENCE = "usecase-to-sequence-v1"
    MODEL_VALIDATOR = "model-validator-v1"
    SECURITY_DESIGN = "security-design-v1"
    USECASE_TO_CODE = "usecase-to-code-v1"
    USECASE_TO_TEST = "usecase-to-test-v1"
    JSON_TO_MODELS = "json-to-models"

    @staticmethod
    def get_step_number(step: 'SkillStep') -> int:
        """ステップ番号を取得"""
        order = [
            SkillStep.SCENARIO_TO_ACTIVITY,      # 1
            SkillStep.ACTIVITY_TO_USECASE,       # 2
            SkillStep.USECASE_TO_CLASS,          # 3
            SkillStep.CLASS_TO_STATEMACHINE,     # 4
            SkillStep.USECASE_TO_SEQUENCE,       # 5
            SkillStep.MODEL_VALIDATOR,           # 6
            SkillStep.SECURITY_DESIGN,           # 7
            SkillStep.USECASE_TO_CODE,           # 8
            SkillStep.USECASE_TO_TEST,           # 9
        ]
        try:
            return order.index(step) + 1
        except ValueError:
            return 99  # 特殊スキル

    @staticmethod
    def from_string(step_str: str) -> Optional['SkillStep']:
        """文字列からSkillStepを取得"""
        for step in SkillStep:
            if step.value == step_str:
                return step
        return None

    @staticmethod
    def get_default_workflow() -> List['SkillStep']:
        """デフォルトのワークフロー順序（9ステップ）"""
        return [
            SkillStep.SCENARIO_TO_ACTIVITY,      # 1
            SkillStep.ACTIVITY_TO_USECASE,       # 2
            SkillStep.USECASE_TO_CLASS,          # 3
            SkillStep.CLASS_TO_STATEMACHINE,     # 4
            SkillStep.USECASE_TO_SEQUENCE,       # 5
            SkillStep.MODEL_VALIDATOR,           # 6
            SkillStep.SECURITY_DESIGN,           # 7
            SkillStep.USECASE_TO_CODE,           # 8
            SkillStep.USECASE_TO_TEST,           # 9
        ]

@dataclass
class ExecutionConfig:
    """実行設定"""
    mode: ExecutionMode
    start_step: Optional[SkillStep] = None
    end_step: Optional[SkillStep] = None
    single_step: Optional[SkillStep] = None
    skip_steps: List[SkillStep] = None
    generate_xmi: bool = False  # デフォルトOFF（40%パフォーマンス向上）
    generate_code: bool = True
    generate_tests: bool = True
    run_validation: bool = True
    run_security: bool = True  # セキュリティ設計
    
    def __post_init__(self):
        if self.skip_steps is None:
            self.skip_steps = []

    def should_execute_step(self, step: SkillStep) -> bool:
        """指定されたステップを実行すべきか判定"""
        
        # スキップリストにある場合は実行しない
        if step in self.skip_steps:
            return False
        
        # モードごとの判定
        if self.mode == ExecutionMode.FULL:
            return True
        
        elif self.mode == ExecutionMode.SINGLE_SKILL:
            return step == self.single_step
        
        elif self.mode == ExecutionMode.RESUME_FROM:
            if self.start_step is None:
                return True
            step_num = SkillStep.get_step_number(step)
            start_num = SkillStep.get_step_number(self.start_step)
            return step_num >= start_num
        
        elif self.mode == ExecutionMode.PARTIAL:
            step_num = SkillStep.get_step_number(step)
            start_num = SkillStep.get_step_number(self.start_step) if self.start_step else 1
            end_num = SkillStep.get_step_number(self.end_step) if self.end_step else 99
            return start_num <= step_num <= end_num
        
        elif self.mode == ExecutionMode.VALIDATE_ONLY:
            # バリデーションのみ実行
            return step == SkillStep.MODEL_VALIDATOR
        
        return False

    def get_execution_plan(self) -> List[SkillStep]:
        """実行計画を取得"""
        workflow = SkillStep.get_default_workflow()
        
        # コード生成が無効な場合は除外
        if not self.generate_code:
            workflow = [s for s in workflow if s != SkillStep.USECASE_TO_CODE]
        
        # テスト生成が無効な場合は除外
        if not self.generate_tests:
            workflow = [s for s in workflow if s != SkillStep.USECASE_TO_TEST]
        
        # バリデーションが無効な場合は除外
        if not self.run_validation:
            workflow = [s for s in workflow if s != SkillStep.MODEL_VALIDATOR]
        
        # セキュリティ設計が無効な場合は除外
        if not self.run_security:
            workflow = [s for s in workflow if s != SkillStep.SECURITY_DESIGN]
        
        # 実行すべきステップのみをフィルタ
        return [step for step in workflow if self.should_execute_step(step)]

    def get_summary(self) -> Dict[str, Any]:
        """設定のサマリーを取得"""
        plan = self.get_execution_plan()
        
        return {
            "mode": self.mode.value,
            "steps_to_execute": len(plan),
            "step_names": [step.value for step in plan],
            "generate_xmi": self.generate_xmi,
            "generate_code": self.generate_code,
            "generate_tests": self.generate_tests,
            "run_validation": self.run_validation,
            "run_security": self.run_security,
            "skip_steps": [step.value for step in self.skip_steps]
        }


class ExecutionPlanner:
    """実行計画を作成するヘルパークラス"""
    
    @staticmethod
    def create_full_workflow(
        generate_xmi: bool = False,  # デフォルトOFF
        generate_code: bool = True,
        generate_tests: bool = True,
        run_security: bool = True
    ) -> ExecutionConfig:
        """フルワークフローの設定を作成"""
        return ExecutionConfig(
            mode=ExecutionMode.FULL,
            generate_xmi=generate_xmi,
            generate_code=generate_code,
            generate_tests=generate_tests,
            run_security=run_security
        )
    
    @staticmethod
    def create_resume_from(
        start_step: SkillStep,
        generate_xmi: bool = False,  # デフォルトOFF
        generate_code: bool = True
    ) -> ExecutionConfig:
        """指定ステップからの再開設定を作成"""
        return ExecutionConfig(
            mode=ExecutionMode.RESUME_FROM,
            start_step=start_step,
            generate_xmi=generate_xmi,
            generate_code=generate_code
        )
    
    @staticmethod
    def create_single_skill(
        skill: SkillStep,
        generate_xmi: bool = False
    ) -> ExecutionConfig:
        """単一スキル実行の設定を作成"""
        return ExecutionConfig(
            mode=ExecutionMode.SINGLE_SKILL,
            single_step=skill,
            generate_xmi=generate_xmi,
            generate_code=False,
            generate_tests=False,
            run_validation=False
        )
    
    @staticmethod
    def create_validate_only() -> ExecutionConfig:
        """バリデーションのみの設定を作成"""
        return ExecutionConfig(
            mode=ExecutionMode.VALIDATE_ONLY,
            generate_xmi=False,
            generate_code=False,
            generate_tests=False,
            run_validation=True,
            run_security=False
        )
    
    @staticmethod
    def create_partial(
        start_step: SkillStep,
        end_step: SkillStep,
        generate_xmi: bool = False  # デフォルトOFF
    ) -> ExecutionConfig:
        """部分実行の設定を作成"""
        return ExecutionConfig(
            mode=ExecutionMode.PARTIAL,
            start_step=start_step,
            end_step=end_step,
            generate_xmi=generate_xmi,
            generate_code=False,
            generate_tests=False
        )
    
    @staticmethod
    def create_models_only(
        include_diagrams: bool = True,
        generate_xmi: bool = False  # デフォルトOFF（必要時のみ有効化）
    ) -> ExecutionConfig:
        """モデル生成のみ（コード生成なし）の設定を作成"""
        skip_steps = []
        if not include_diagrams:
            skip_steps.extend([
                SkillStep.CLASS_TO_STATEMACHINE,
                SkillStep.USECASE_TO_SEQUENCE
            ])
        
        return ExecutionConfig(
            mode=ExecutionMode.FULL,
            generate_xmi=generate_xmi,
            generate_code=False,
            generate_tests=False,
            skip_steps=skip_steps
        )


def print_execution_plan(config: ExecutionConfig):
    """実行計画を表示"""
    summary = config.get_summary()
    
    print("=" * 70)
    print("実行計画")
    print("=" * 70)
    print(f"モード: {summary['mode']}")
    print(f"実行ステップ数: {summary['steps_to_execute']}")
    print()
    print("実行するスキル:")
    for i, step_name in enumerate(summary['step_names'], 1):
        print(f"  {i}. {step_name}")
    
    print()
    print("オプション:")
    print(f"  - XMI生成: {'✅' if summary['generate_xmi'] else '❌'}")
    print(f"  - コード生成: {'✅' if summary['generate_code'] else '❌'}")
    print(f"  - テスト生成: {'✅' if summary['generate_tests'] else '❌'}")
    print(f"  - バリデーション: {'✅' if summary['run_validation'] else '❌'}")
    print(f"  - セキュリティ設計: {'✅' if summary['run_security'] else '❌'}")
    
    if summary['skip_steps']:
        print()
        print("スキップするステップ:")
        for step in summary['skip_steps']:
            print(f"  - {step}")
    
    print("=" * 70)


# 使用例
if __name__ == "__main__":
    print("Execution Mode Manager - Examples\n")
    
    # 例1: フルワークフロー
    print("例1: フルワークフロー")
    config1 = ExecutionPlanner.create_full_workflow()
    print_execution_plan(config1)
    print()
    
    # 例2: Step 3から再開
    print("例2: Step 3 (usecase-to-class) から再開")
    config2 = ExecutionPlanner.create_resume_from(
        SkillStep.USECASE_TO_CLASS,
        generate_xmi=False
    )
    print_execution_plan(config2)
    print()
    
    # 例3: 単一スキル実行
    print("例3: バリデーションのみ実行")
    config3 = ExecutionPlanner.create_single_skill(SkillStep.MODEL_VALIDATOR)
    print_execution_plan(config3)
    print()
    
    # 例4: モデルのみ（コード生成なし）
    print("例4: モデル生成のみ（コード生成なし）")
    config4 = ExecutionPlanner.create_models_only()
    print_execution_plan(config4)
    print()
    
    # 例5: 部分実行
    print("例5: Step 3からStep 5まで実行")
    config5 = ExecutionPlanner.create_partial(
        SkillStep.USECASE_TO_CLASS,
        SkillStep.USECASE_TO_SEQUENCE
    )
    print_execution_plan(config5)
