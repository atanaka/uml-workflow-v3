#!/usr/bin/env python3
"""
Verify Step Outputs
ワークフロー各ステップの出力完全性を検証するモジュール

主な機能:
- Step 2 (activity-to-usecase-v1) の出力完全性検証
  JSON 内 UC 数と usecase-specifications/*.md のファイル数が一致するか、
  各 .md に Cockburn 必須セクションが揃っているかを検査する。
- Phase A 全体（Step 1〜7）の成果物完全性検証
  Resume from Step 8+ モード開始時の事前条件チェックに使う。

設計方針:
- 各 Step の Expected Outputs を STEP_EXPECTED_OUTPUTS 辞書として一元定義
- 将来の改修候補 #3（共通検証フレームワーク）への拡張余地を残す
- 失敗時は WorkflowError を送出し、原因と推奨対処を含むメッセージで停止させる

導入: uml-workflow-v3 v3.4.0 改修 #1, #2 で追加
"""

import json
import os
import sys
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

# scripts ディレクトリを import パスに追加（環境非依存）
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from env_paths import get_output_dir

# 出力ディレクトリのデフォルト（Web/ローカル両対応・環境自動判定）
DEFAULT_OUTPUT_DIR = get_output_dir()


class WorkflowError(Exception):
    """ワークフロー検証で致命的な不整合を検出したときに送出する例外"""
    pass


# ---------------------------------------------------------------------------
# Step Expected Outputs Registry
# ---------------------------------------------------------------------------
# 各 Step の Expected Outputs を宣言的に管理する。
# 改修 #3（共通検証フレームワーク）で本辞書を全 Step に拡張する想定。
#
# files: プロジェクト名で format される、ディスク上に必ず存在すべきファイル
# directories: 必須ディレクトリ（空でないこと）
# cross_checks: 値同士の整合性チェック（型は "count_match" のみ現状サポート）
STEP_EXPECTED_OUTPUTS: Dict[str, Dict[str, Any]] = {
    "scenario_to_activity": {
        "files": [
            "{project}_activity-data.json",
            "{project}_activity.puml",
        ],
        "directories": [],
        "cross_checks": [],
    },
    "activity_to_usecase": {
        "files": [
            "{project}_usecase-output.json",
            "{project}_usecase-diagram.puml",
        ],
        "directories": [
            # usecase-specifications/ は配置場所がプロジェクトによって異なるため、
            # find_usecase_specifications_dir() で動的に解決する。
        ],
        "cross_checks": [
            {
                "type": "count_match",
                "left": "json_uc_count",
                "right": "md_file_count",
                "description": (
                    "JSON 内 UC 数と usecase-specifications/*.md のファイル数が一致すること"
                ),
            }
        ],
    },
    "usecase_to_class": {
        "files": [
            "{project}_domain-model.json",
            # class.puml は v3.3.0 まで class-diagram.puml と表記揺れがある
            # ため、verify 側では柔軟にどちらかが存在すれば OK とする。
        ],
        "directories": [],
        "cross_checks": [],
    },
    "class_to_statemachine": {
        "files": [
            "{project}_statemachine.puml",
        ],
        "directories": [],
        "cross_checks": [],
    },
    "usecase_to_sequence": {
        "files": [
            "{project}_sequence.puml",
        ],
        "directories": [],
        "cross_checks": [],
    },
    "model_validator": {
        "files": [
            "{project}_validation-report.md",
        ],
        "directories": [],
        "cross_checks": [],
    },
    "security_design": {
        "files": [
            "{project}_security-config.json",
        ],
        "directories": [],
        "cross_checks": [],
    },
}


# Cockburn 形式の use case spec に必須のセクション。
# 日英バイリンガル対応のため、日本語/英語のどちらかが含まれていれば OK とする。
COCKBURN_REQUIRED_SECTIONS: List[Tuple[str, ...]] = [
    ("ユースケース", "Use Case"),
    ("事前条件", "Precondition"),
    ("事後条件", "Postcondition", "Success Guarantee"),
    ("主成功シナリオ", "Main Success Scenario", "Main Scenario"),
    ("拡張", "Extension"),
]


# ---------------------------------------------------------------------------
# Path resolution helpers
# ---------------------------------------------------------------------------

def find_usecase_specifications_dir(
    project_name: str,
    working_dir: Path,
) -> Optional[Path]:
    """
    usecase-specifications/ ディレクトリの実際の配置場所を探索する。

    探索順:
    1. {working_dir}/{project_name}/usecase-specifications/
    2. {working_dir}/usecase-specifications/
    3. {working_dir}/{project_name}_usecase-specifications/

    見つからない場合は None。
    """
    candidates = [
        working_dir / project_name / "usecase-specifications",
        working_dir / "usecase-specifications",
        working_dir / f"{project_name}_usecase-specifications",
    ]
    for candidate in candidates:
        if candidate.is_dir():
            return candidate
    return None


# ---------------------------------------------------------------------------
# Step 2 verification (改修候補 #1)
# ---------------------------------------------------------------------------

def verify_step2_outputs(
    project_name: str,
    working_dir: Optional[Path] = None,
    check_sections: bool = True,
) -> Dict[str, Any]:
    """
    Step 2 (activity-to-usecase-v1) の出力完全性を検証する。

    Args:
        project_name: プロジェクト名
        working_dir: 出力ディレクトリ（既定: get_output_dir() で環境自動判定）
        check_sections: 各 .md の Cockburn 必須セクションも検査するか

    Returns:
        検証結果 dict:
            - is_complete: bool
            - json_uc_count: int
            - md_file_count: int
            - missing_uc_ids: List[str]
            - extra_uc_ids: List[str]
            - section_issues: List[Dict]  # {file: str, missing_sections: List[str]}
            - spec_dir: Optional[str]
            - error_message: Optional[str]

    Raises:
        WorkflowError: 不整合を検出した場合（呼び出し側で raise 用のメッセージとして使う）
    """
    working_dir = Path(working_dir) if working_dir else DEFAULT_OUTPUT_DIR

    result: Dict[str, Any] = {
        "is_complete": False,
        "json_uc_count": 0,
        "md_file_count": 0,
        "missing_uc_ids": [],
        "extra_uc_ids": [],
        "section_issues": [],
        "spec_dir": None,
        "error_message": None,
    }

    # 1. JSON から UC ID 一覧を取得
    json_path = working_dir / f"{project_name}_usecase-output.json"
    if not json_path.exists():
        result["error_message"] = (
            f"Use case JSON not found: {json_path}\n"
            f"Step 2 (activity-to-usecase-v1) did not produce the required output."
        )
        return result

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        result["error_message"] = f"Failed to parse {json_path}: {e}"
        return result

    usecases = data.get("usecases") or data.get("use_cases") or []
    expected_ids: Set[str] = {uc.get("id") for uc in usecases if uc.get("id")}
    result["json_uc_count"] = len(expected_ids)

    # 2. usecase-specifications/ を探索して .md を列挙
    spec_dir = find_usecase_specifications_dir(project_name, working_dir)
    if spec_dir is None:
        result["error_message"] = (
            "usecase-specifications/ directory not found.\n"
            f"Searched: {working_dir}/{project_name}/usecase-specifications/, "
            f"{working_dir}/usecase-specifications/, "
            f"{working_dir}/{project_name}_usecase-specifications/\n"
            "Step 2 must create individual .md files (Cockburn format) for ALL use cases."
        )
        return result

    result["spec_dir"] = str(spec_dir)
    md_files = sorted(p for p in spec_dir.iterdir() if p.suffix == ".md")
    result["md_file_count"] = len(md_files)

    # 3. ファイル名から UC ID を抽出
    actual_ids: Set[str] = set()
    uc_pattern = re.compile(r"(UC-\d+)")
    for md in md_files:
        match = uc_pattern.match(md.name)
        if match:
            actual_ids.add(match.group(1))

    result["missing_uc_ids"] = sorted(expected_ids - actual_ids)
    result["extra_uc_ids"] = sorted(actual_ids - expected_ids)

    # 4. Cockburn 必須セクションのチェック（オプション）
    if check_sections:
        for md in md_files:
            try:
                content = md.read_text(encoding="utf-8")
            except OSError:
                continue
            missing = []
            for variants in COCKBURN_REQUIRED_SECTIONS:
                if not any(variant in content for variant in variants):
                    missing.append(variants[0])
            if missing:
                result["section_issues"].append({
                    "file": md.name,
                    "missing_sections": missing,
                })

    # 5. 完全性判定
    result["is_complete"] = (
        not result["missing_uc_ids"]
        and not result["extra_uc_ids"]
        and not result["section_issues"]
    )

    if not result["is_complete"]:
        parts = []
        if result["missing_uc_ids"]:
            parts.append(
                f"Missing {len(result['missing_uc_ids'])} use case spec file(s): "
                f"{result['missing_uc_ids']}"
            )
        if result["extra_uc_ids"]:
            parts.append(
                f"Extra unexpected file(s) for UC IDs: {result['extra_uc_ids']}"
            )
        if result["section_issues"]:
            parts.append(
                f"{len(result['section_issues'])} file(s) missing required Cockburn sections"
            )
        result["error_message"] = (
            f"Step 2 output verification failed.\n"
            f"  JSON has {result['json_uc_count']} UCs, "
            f".md files: {result['md_file_count']}.\n  "
            + "; ".join(parts)
            + "\nPossible causes: LLM output truncation, file write error.\n"
            "Action: Re-run Step 2, or generate missing files manually."
        )

    return result


def assert_step2_complete(project_name: str, working_dir: Optional[Path] = None) -> None:
    """
    Step 2 出力完全性検証を実行し、失敗時は WorkflowError を送出する。

    SKILL.md からの呼び出し用ヘルパー。
    """
    result = verify_step2_outputs(project_name, working_dir)
    if not result["is_complete"]:
        raise WorkflowError(result["error_message"] or "Step 2 verification failed")


# ---------------------------------------------------------------------------
# Phase A verification (改修候補 #2)
# ---------------------------------------------------------------------------

def verify_phase_a_completeness(
    project_name: str,
    working_dir: Optional[Path] = None,
) -> Dict[str, Any]:
    """
    Resume from Step 8+ モード開始時に Phase A 成果物が揃っているか検証する。

    Args:
        project_name: プロジェクト名
        working_dir: 出力ディレクトリ（既定: get_output_dir() で環境自動判定）

    Returns:
        検証結果 dict:
            - is_complete: bool
            - missing_files: List[{step: str, file: str}]
            - missing_dirs: List[str]
            - cross_check_ok: bool
            - cross_check_detail: Optional[str]
            - step2_detail: Dict (verify_step2_outputs の結果)
            - recommendation: str
    """
    working_dir = Path(working_dir) if working_dir else DEFAULT_OUTPUT_DIR

    missing_files: List[Dict[str, str]] = []
    missing_dirs: List[str] = []

    # 1. STEP_EXPECTED_OUTPUTS に登録されたファイルの存在チェック
    for step_name, spec in STEP_EXPECTED_OUTPUTS.items():
        for file_template in spec["files"]:
            file_name = file_template.format(project=project_name)
            path = working_dir / file_name
            if not path.exists():
                missing_files.append({"step": step_name, "file": file_name})

    # 2. usecase-specifications/ ディレクトリのチェック（Step 2）
    spec_dir = find_usecase_specifications_dir(project_name, working_dir)
    if spec_dir is None or not any(spec_dir.iterdir()):
        missing_dirs.append("usecase-specifications/")

    # 3. Step 2 のクロスチェック（JSON UC 数 == .md ファイル数）
    step2_detail = verify_step2_outputs(
        project_name, working_dir, check_sections=False
    )
    cross_check_ok = (
        not step2_detail["missing_uc_ids"]
        and not step2_detail["extra_uc_ids"]
        # JSON 自体が無いケースは missing_files 側で検出されるため、
        # ここでは "JSON はあるが .md が足りない" だけを cross-check 失敗とみなす。
        and step2_detail["json_uc_count"] > 0
    )
    cross_check_detail = None
    if not cross_check_ok and step2_detail["json_uc_count"] > 0:
        cross_check_detail = (
            f"JSON has {step2_detail['json_uc_count']} UCs but "
            f"{step2_detail['md_file_count']} .md files. "
            "→ Step 2 (activity-to-usecase-v1) likely terminated incompletely."
        )

    is_complete = (
        not missing_files
        and not missing_dirs
        and cross_check_ok
    )

    if is_complete:
        recommendation = "Proceed to Step 8."
    else:
        recommendation = (
            "Phase A is incomplete. Either:\n"
            f"  1) Place missing artifacts in the output dir ({get_output_dir()}), OR\n"
            "  2) Re-run Phase A from the affected step(s) in a fresh session."
        )

    return {
        "is_complete": is_complete,
        "missing_files": missing_files,
        "missing_dirs": missing_dirs,
        "cross_check_ok": cross_check_ok,
        "cross_check_detail": cross_check_detail,
        "step2_detail": step2_detail,
        "recommendation": recommendation,
    }


def format_phase_a_report(result: Dict[str, Any]) -> str:
    """
    verify_phase_a_completeness の結果を人間可読な文字列に整形する。
    SKILL.md からの呼び出しで表示用に使う。
    """
    lines: List[str] = []
    if result["is_complete"]:
        lines.append("✅ Phase A artifacts complete. Proceeding to Step 8.")
        return "\n".join(lines)

    lines.append("⚠️  Phase A artifacts INCOMPLETE.")
    if result["missing_files"]:
        lines.append(f"\nMissing files ({len(result['missing_files'])}):")
        for m in result["missing_files"]:
            lines.append(f"  - [{m['step']}] {m['file']}")
    if result["missing_dirs"]:
        lines.append("\nMissing directories:")
        for d in result["missing_dirs"]:
            lines.append(f"  - {d}")
    if not result["cross_check_ok"] and result["cross_check_detail"]:
        lines.append(f"\nCross-check failure: {result['cross_check_detail']}")
    lines.append(f"\n{result['recommendation']}")
    lines.append(
        "\nDo NOT proceed to Step 8 until all required artifacts are present."
    )
    return "\n".join(lines)


def assert_phase_a_complete(
    project_name: str,
    working_dir: Optional[Path] = None,
) -> None:
    """
    Phase A 完全性を検証し、不完全時は WorkflowError を送出する。

    SKILL.md の Resume Mode Prerequisite Check から呼び出される。
    """
    result = verify_phase_a_completeness(project_name, working_dir)
    if not result["is_complete"]:
        raise WorkflowError(format_phase_a_report(result))


# ---------------------------------------------------------------------------
# CLI entrypoint (debugging用)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print(
            "Usage: verify_step_outputs.py <command> <project_name> [working_dir]\n"
            "  command: step2 | phase_a"
        )
        sys.exit(2)

    command = sys.argv[1]
    project = sys.argv[2]
    workdir = Path(sys.argv[3]) if len(sys.argv) > 3 else DEFAULT_OUTPUT_DIR

    if command == "step2":
        res = verify_step2_outputs(project, workdir)
        print(json.dumps(res, indent=2, ensure_ascii=False))
        sys.exit(0 if res["is_complete"] else 1)
    elif command == "phase_a":
        res = verify_phase_a_completeness(project, workdir)
        print(format_phase_a_report(res))
        print("\n--- raw result ---")
        # step2_detail も含めて出力
        print(json.dumps(res, indent=2, ensure_ascii=False))
        sys.exit(0 if res["is_complete"] else 1)
    else:
        print(f"Unknown command: {command}")
        sys.exit(2)
