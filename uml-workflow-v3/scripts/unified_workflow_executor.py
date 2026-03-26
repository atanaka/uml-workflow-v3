#!/usr/bin/env python3
"""
Unified Workflow Executor
キャッシュ機能と段階的実行モードを統合したワークフロー実行補助スクリプト
"""

import sys
import os
import json
from pathlib import Path
from typing import Optional, List, Dict, Any

# スキルのscriptsディレクトリをパスに追加
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# フォールバック
sys.path.append('/mnt/skills/user/uml-workflow-v3/scripts')
sys.path.append(str(Path.home() / ".uml-workflow-cache"))  # フォールバック（直接参照不要）

from execution_mode_manager import (
    ExecutionConfig,
    SkillStep,
    ExecutionPlanner,
    print_execution_plan,
)

from workflow_cache_helper import (
    has_cached_step,
    get_cached_file,
    cache_file,
    get_project_cache_summary,
    clear_project_cache,
)

class UnifiedWorkflowExecutor:
    """キャッシュと段階的実行を統合した実行管理クラス"""
    
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.execution_config: Optional[ExecutionConfig] = None
        self.use_cache = True
        self.output_dir = Path(os.environ.get("UML_WORKFLOW_OUTPUT_DIR", "/mnt/user-data/outputs"))
        
    def set_execution_config(self, config: ExecutionConfig):
        """実行設定をセット"""
        self.execution_config = config
    
    def set_cache_usage(self, use_cache: bool):
        """キャッシュ使用の有効/無効"""
        self.use_cache = use_cache
    
    def _get_step_cache_key(self, step: SkillStep) -> str:
        """ステップに対応するキャッシュキーを取得"""
        # スキル名からキャッシュキーを生成（ハイフン除去してアンダースコアに）
        return step.value.replace('-v1', '').replace('-', '_')
    
    def _get_step_output_files(self, step: SkillStep) -> List[Dict[str, str]]:
        """ステップの出力ファイルリストを取得"""
        # 各ステップの主要な出力ファイル
        outputs = {
            SkillStep.SCENARIO_TO_ACTIVITY: [
                {"type": "activity-data", "ext": "json", "suffix": "_activity-data.json"},
                {"type": "activity-puml", "ext": "puml", "suffix": "_activity.puml"},
            ],
            SkillStep.ACTIVITY_TO_USECASE: [
                {"type": "usecase-output", "ext": "json", "suffix": "_usecase-output.json"},
                {"type": "usecase-diagram", "ext": "puml", "suffix": "_usecase-diagram.puml"},
            ],
            SkillStep.USECASE_TO_CLASS: [
                {"type": "domain-model", "ext": "json", "suffix": "_domain-model.json"},
                {"type": "class-puml", "ext": "puml", "suffix": "_class.puml"},
            ],
            SkillStep.CLASS_TO_STATEMACHINE: [
                {"type": "statemachine-puml", "ext": "puml", "suffix": "_statemachine.puml"},
            ],
            SkillStep.USECASE_TO_SEQUENCE: [
                {"type": "sequence-puml", "ext": "puml", "suffix": "_sequence.puml"},
            ],
            SkillStep.MODEL_VALIDATOR: [
                {"type": "validation-report", "ext": "md", "suffix": "_validation-report.md"},
            ],
            SkillStep.SECURITY_DESIGN: [
                {"type": "security-design", "ext": "md", "suffix": "_security-design.md"},
                {"type": "security-config", "ext": "json", "suffix": "_security-config.json"},
            ],
        }
        
        return outputs.get(step, [])
    
    def check_step_cache(self, step: SkillStep) -> Dict[str, Any]:
        """ステップのキャッシュ状態をチェック"""
        if not self.use_cache:
            return {"has_cache": False, "files": []}
        
        cache_key = self._get_step_cache_key(step)
        has_cache = has_cached_step(self.project_name, cache_key)
        
        cached_files = []
        if has_cache:
            output_files = self._get_step_output_files(step)
            for file_info in output_files:
                cached_path = get_cached_file(
                    self.project_name,
                    cache_key,
                    file_info["type"]
                )
                if cached_path:
                    cached_files.append({
                        "type": file_info["type"],
                        "path": cached_path,
                        "suffix": file_info["suffix"]
                    })
        
        return {
            "has_cache": has_cache,
            "files": cached_files,
            "step": step.value
        }
    
    def restore_from_cache(self, step: SkillStep) -> bool:
        """キャッシュからファイルを復元"""
        cache_info = self.check_step_cache(step)
        
        if not cache_info["has_cache"]:
            return False
        
        import shutil
        restored_count = 0
        
        for file_info in cache_info["files"]:
            output_path = self.output_dir / f"{self.project_name}{file_info['suffix']}"
            shutil.copy2(file_info["path"], output_path)
            print(f"  ✅ 復元: {output_path.name}")
            restored_count += 1
        
        return restored_count > 0
    
    def cache_step_outputs(self, step: SkillStep) -> int:
        """ステップの出力をキャッシュに保存"""
        if not self.use_cache:
            return 0
        
        cache_key = self._get_step_cache_key(step)
        output_files = self._get_step_output_files(step)
        
        cached_count = 0
        for file_info in output_files:
            source_path = self.output_dir / f"{self.project_name}{file_info['suffix']}"
            
            if source_path.exists():
                cache_file(
                    self.project_name,
                    cache_key,
                    file_info["type"],
                    str(source_path)
                )
                print(f"  💾 キャッシュ: {source_path.name}")
                cached_count += 1
        
        return cached_count
    
    def should_execute_step(self, step: SkillStep) -> tuple[bool, str]:
        """ステップを実行すべきか判定（理由も返す）"""
        if self.execution_config is None:
            return True, "設定なし（デフォルト実行）"
        
        # 実行設定による判定
        if not self.execution_config.should_execute_step(step):
            return False, "実行設定によりスキップ"
        
        # キャッシュチェック
        if self.use_cache:
            cache_info = self.check_step_cache(step)
            if cache_info["has_cache"]:
                # ユーザーに確認を促す（実際のインタラクションは別途実装）
                return True, "キャッシュあり（確認推奨）"
        
        return True, "実行必要"
    
    def get_execution_summary(self) -> Dict[str, Any]:
        """実行サマリーを取得"""
        if self.execution_config is None:
            return {"error": "実行設定が未設定"}
        
        plan = self.execution_config.get_execution_plan()
        
        steps_info = []
        for step in plan:
            should_exec, reason = self.should_execute_step(step)
            cache_info = self.check_step_cache(step)
            
            steps_info.append({
                "step": step.value,
                "step_number": SkillStep.get_step_number(step),
                "should_execute": should_exec,
                "reason": reason,
                "has_cache": cache_info["has_cache"],
                "cached_files": len(cache_info["files"])
            })
        
        return {
            "project_name": self.project_name,
            "use_cache": self.use_cache,
            "execution_mode": self.execution_config.mode.value,
            "total_steps": len(plan),
            "steps": steps_info
        }
    
    def print_execution_summary(self):
        """実行サマリーを表示"""
        summary = self.get_execution_summary()
        
        if "error" in summary:
            print(f"❌ {summary['error']}")
            return
        
        print("=" * 80)
        print(f"実行サマリー - {summary['project_name']}")
        print("=" * 80)
        print(f"実行モード: {summary['execution_mode']}")
        print(f"キャッシュ使用: {'✅ 有効' if summary['use_cache'] else '❌ 無効'}")
        print(f"総ステップ数: {summary['total_steps']}")
        print()
        print("ステップ詳細:")
        print("-" * 80)
        
        for step_info in summary['steps']:
            status = "🟢 実行" if step_info['should_execute'] else "⚪ スキップ"
            cache_status = f"💾 キャッシュあり({step_info['cached_files']}ファイル)" if step_info['has_cache'] else "⚠️ キャッシュなし"
            
            print(f"{status} Step {step_info['step_number']}: {step_info['step']}")
            print(f"     理由: {step_info['reason']}")
            if summary['use_cache']:
                print(f"     {cache_status}")
            print()
        
        print("=" * 80)
    
    def clear_cache(self):
        """プロジェクトのキャッシュをクリア"""
        clear_project_cache(self.project_name)
        print(f"✅ {self.project_name}のキャッシュをクリアしました")


def demo():
    """デモンストレーション"""
    print("=" * 80)
    print("Unified Workflow Executor - Demo")
    print("=" * 80)
    print()
    
    # 例1: フルワークフロー（キャッシュあり）
    print("例1: フルワークフロー（キャッシュ有効）")
    print("-" * 80)
    
    executor1 = UnifiedWorkflowExecutor("demo-project")
    config1 = ExecutionPlanner.create_full_workflow(
        generate_xmi=False,
        generate_code=True,
        generate_tests=True
    )
    executor1.set_execution_config(config1)
    executor1.set_cache_usage(True)
    executor1.print_execution_summary()
    
    print("\n" + "=" * 80)
    print()
    
    # 例2: Step 3から再開（キャッシュ利用）
    print("例2: Step 3から再開（キャッシュ利用）")
    print("-" * 80)
    
    executor2 = UnifiedWorkflowExecutor("demo-project")
    config2 = ExecutionPlanner.create_resume_from(
        SkillStep.USECASE_TO_CLASS,
        generate_xmi=False,
        generate_code=True
    )
    executor2.set_execution_config(config2)
    executor2.set_cache_usage(True)
    executor2.print_execution_summary()
    
    print("\n" + "=" * 80)
    print()
    
    # 例3: モデルのみ生成
    print("例3: モデルのみ生成（コード生成なし）")
    print("-" * 80)
    
    executor3 = UnifiedWorkflowExecutor("demo-project")
    config3 = ExecutionPlanner.create_models_only(include_diagrams=True)
    executor3.set_execution_config(config3)
    executor3.set_cache_usage(True)
    executor3.print_execution_summary()
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    demo()
