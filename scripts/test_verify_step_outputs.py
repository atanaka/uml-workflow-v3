#!/usr/bin/env python3
"""
Regression tests for verify_step_outputs.py

改修候補 #1 (Step 2 出力完全性検証) と #2 (Phase A 完全性検証) の
回帰テスト。`library-management` で発生した実例を再現できることを検証する。

実行:
    python3 test_verify_step_outputs.py
"""

import json
import shutil
import tempfile
import unittest
from pathlib import Path

import verify_step_outputs as vso


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")


def _write_uc_md(
    path: Path,
    *,
    include_all_sections: bool = True,
    omit_sections: tuple = (),
) -> None:
    """Cockburn 形式の最小限の UC spec を書き出す。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    blocks = {
        "ユースケース": "## ユースケース情報\n- ID: dummy\n",
        "事前条件": "## 事前条件\n- ユーザーがログイン済み\n",
        "事後条件": "## 事後条件\n- 注文が登録される\n",
        "主成功シナリオ": "## 主成功シナリオ\n1. ユーザーが商品を選ぶ\n",
        "拡張": "## 拡張\n2a. 在庫がない場合: ...\n",
    }
    if not include_all_sections:
        for s in omit_sections:
            blocks.pop(s, None)
    path.write_text("\n".join(blocks.values()), encoding="utf-8")


def _make_phase_a_complete_fixture(tmp: Path, project: str, uc_count: int) -> None:
    """Phase A 全成果物が揃った正常系のフィクスチャを作る。"""
    # Step 1
    _write_json(tmp / f"{project}_activity-data.json", {"activities": []})
    (tmp / f"{project}_activity.puml").write_text("@startuml\n@enduml\n")
    # Step 2: JSON + spec dir
    usecases = [
        {"id": f"UC-{i+1:03d}", "name": f"uc{i+1}"} for i in range(uc_count)
    ]
    _write_json(
        tmp / f"{project}_usecase-output.json",
        {"usecases": usecases},
    )
    (tmp / f"{project}_usecase-diagram.puml").write_text("@startuml\n@enduml\n")
    spec_dir = tmp / project / "usecase-specifications"
    for uc in usecases:
        _write_uc_md(spec_dir / f"{uc['id']}_{uc['name']}.md")
    # Step 3
    _write_json(tmp / f"{project}_domain-model.json", {"entities": []})
    # Step 4
    (tmp / f"{project}_statemachine.puml").write_text("@startuml\n@enduml\n")
    # Step 5
    (tmp / f"{project}_sequence.puml").write_text("@startuml\n@enduml\n")
    # Step 6
    (tmp / f"{project}_validation-report.md").write_text("# Validation\n")
    # Step 7
    _write_json(tmp / f"{project}_security-config.json", {"auth": {}})


class TestStep2Verification(unittest.TestCase):
    """改修候補 #1: Step 2 出力完全性検証"""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="vso-test-"))
        self.project = "library-management"

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_1_normal_case_passes(self):
        """Test 1: JSON UC 数 == .md ファイル数 → is_complete=True"""
        _make_phase_a_complete_fixture(self.tmp, self.project, uc_count=3)
        result = vso.verify_step2_outputs(self.project, self.tmp)
        self.assertTrue(
            result["is_complete"],
            f"Expected pass but got error: {result.get('error_message')}",
        )
        self.assertEqual(result["json_uc_count"], 3)
        self.assertEqual(result["md_file_count"], 3)
        self.assertEqual(result["missing_uc_ids"], [])

    def test_2_library_management_repro_case(self):
        """Test 2: library-management 実例再現
        12 UC 中 UC-001/005/006 の 3 件のみ .md 生成 → WorkflowError 検出
        """
        # JSON は 12 UC、.md は UC-001, UC-005, UC-006 のみ
        usecases = [
            {"id": f"UC-{i+1:03d}", "name": f"uc{i+1}"} for i in range(12)
        ]
        _write_json(
            self.tmp / f"{self.project}_usecase-output.json",
            {"usecases": usecases},
        )
        spec_dir = self.tmp / self.project / "usecase-specifications"
        for uc_id in ["UC-001", "UC-005", "UC-006"]:
            _write_uc_md(spec_dir / f"{uc_id}_dummy.md")

        result = vso.verify_step2_outputs(self.project, self.tmp)
        self.assertFalse(result["is_complete"])
        self.assertEqual(result["json_uc_count"], 12)
        self.assertEqual(result["md_file_count"], 3)
        # 9 件欠落していることを検証
        self.assertEqual(len(result["missing_uc_ids"]), 9)
        self.assertIn("UC-002", result["missing_uc_ids"])
        self.assertIn("UC-012", result["missing_uc_ids"])
        self.assertNotIn("UC-001", result["missing_uc_ids"])
        # エラーメッセージに原因の手がかりが含まれている
        self.assertIn("LLM output truncation", result["error_message"])

        # assert_step2_complete は WorkflowError を送出するはず
        with self.assertRaises(vso.WorkflowError):
            vso.assert_step2_complete(self.project, self.tmp)

    def test_3_md_missing_cockburn_section(self):
        """Test 3: .md に Cockburn 必須セクション欠落 → 検出"""
        usecases = [{"id": "UC-001", "name": "order"}]
        _write_json(
            self.tmp / f"{self.project}_usecase-output.json",
            {"usecases": usecases},
        )
        spec_dir = self.tmp / self.project / "usecase-specifications"
        # 主成功シナリオを欠落させる
        _write_uc_md(
            spec_dir / "UC-001_order.md",
            include_all_sections=False,
            omit_sections=("主成功シナリオ",),
        )

        result = vso.verify_step2_outputs(
            self.project, self.tmp, check_sections=True
        )
        self.assertFalse(result["is_complete"])
        self.assertEqual(len(result["section_issues"]), 1)
        self.assertIn(
            "主成功シナリオ",
            result["section_issues"][0]["missing_sections"],
        )

    def test_3b_section_check_skippable(self):
        """check_sections=False ならセクション検査はスキップ"""
        usecases = [{"id": "UC-001", "name": "order"}]
        _write_json(
            self.tmp / f"{self.project}_usecase-output.json",
            {"usecases": usecases},
        )
        spec_dir = self.tmp / self.project / "usecase-specifications"
        _write_uc_md(
            spec_dir / "UC-001_order.md",
            include_all_sections=False,
            omit_sections=("主成功シナリオ", "拡張"),
        )
        result = vso.verify_step2_outputs(
            self.project, self.tmp, check_sections=False
        )
        # セクション欠落は無視されるので完全とみなされる
        self.assertTrue(
            result["is_complete"],
            f"Expected pass when check_sections=False, got: {result.get('error_message')}",
        )

    def test_extra_md_files_detected(self):
        """JSON に無い UC ID の .md があれば extra_uc_ids として検出"""
        usecases = [{"id": "UC-001", "name": "order"}]
        _write_json(
            self.tmp / f"{self.project}_usecase-output.json",
            {"usecases": usecases},
        )
        spec_dir = self.tmp / self.project / "usecase-specifications"
        _write_uc_md(spec_dir / "UC-001_order.md")
        _write_uc_md(spec_dir / "UC-999_orphan.md")  # JSON に無い

        result = vso.verify_step2_outputs(self.project, self.tmp)
        self.assertFalse(result["is_complete"])
        self.assertIn("UC-999", result["extra_uc_ids"])

    def test_missing_json_returns_error(self):
        """JSON 自体が無い場合は error_message を返す"""
        result = vso.verify_step2_outputs(self.project, self.tmp)
        self.assertFalse(result["is_complete"])
        self.assertIn("not found", result["error_message"])


class TestPhaseAVerification(unittest.TestCase):
    """改修候補 #2: Phase A 完全性検証"""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="vso-test-"))
        self.project = "library-management"

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_4_phase_a_complete(self):
        """Test 4: Phase A 必須ファイル全揃い → is_complete=True"""
        _make_phase_a_complete_fixture(self.tmp, self.project, uc_count=5)
        result = vso.verify_phase_a_completeness(self.project, self.tmp)
        self.assertTrue(
            result["is_complete"],
            f"Expected complete, got: missing={result['missing_files']}, "
            f"dirs={result['missing_dirs']}, "
            f"cross_check_detail={result['cross_check_detail']}",
        )
        self.assertEqual(result["missing_files"], [])
        self.assertEqual(result["missing_dirs"], [])
        self.assertTrue(result["cross_check_ok"])

    def test_5_phase_a_domain_model_missing(self):
        """Test 5: domain-model.json 欠落 → 欠落ファイル正しく報告"""
        _make_phase_a_complete_fixture(self.tmp, self.project, uc_count=3)
        (self.tmp / f"{self.project}_domain-model.json").unlink()

        result = vso.verify_phase_a_completeness(self.project, self.tmp)
        self.assertFalse(result["is_complete"])
        missing_files_only = [m["file"] for m in result["missing_files"]]
        self.assertIn(
            f"{self.project}_domain-model.json",
            missing_files_only,
        )
        # 該当ステップが正しく紐づいている
        for m in result["missing_files"]:
            if m["file"].endswith("_domain-model.json"):
                self.assertEqual(m["step"], "usecase_to_class")

    def test_6_phase_a_cross_check_fails(self):
        """Test 6: JSON と spec ディレクトリの UC 数不整合 → cross_check_ok=False"""
        _make_phase_a_complete_fixture(self.tmp, self.project, uc_count=12)
        # 9 件の .md を削除（library-management の再現）
        spec_dir = self.tmp / self.project / "usecase-specifications"
        for md in sorted(spec_dir.iterdir())[3:]:
            md.unlink()

        result = vso.verify_phase_a_completeness(self.project, self.tmp)
        self.assertFalse(result["is_complete"])
        self.assertFalse(result["cross_check_ok"])
        self.assertIsNotNone(result["cross_check_detail"])
        self.assertIn("12 UCs", result["cross_check_detail"])
        self.assertIn("3 .md files", result["cross_check_detail"])

    def test_format_phase_a_report_complete(self):
        """完全なときのレポート文字列"""
        _make_phase_a_complete_fixture(self.tmp, self.project, uc_count=2)
        result = vso.verify_phase_a_completeness(self.project, self.tmp)
        report = vso.format_phase_a_report(result)
        self.assertIn("✅", report)
        self.assertIn("Phase A artifacts complete", report)

    def test_format_phase_a_report_incomplete(self):
        """不完全なときのレポート文字列"""
        # 何も作らない
        result = vso.verify_phase_a_completeness(self.project, self.tmp)
        report = vso.format_phase_a_report(result)
        self.assertIn("⚠️", report)
        self.assertIn("INCOMPLETE", report)
        self.assertIn("Missing files", report)

    def test_assert_phase_a_complete_raises(self):
        """不完全時に WorkflowError を送出"""
        with self.assertRaises(vso.WorkflowError) as ctx:
            vso.assert_phase_a_complete(self.project, self.tmp)
        self.assertIn("INCOMPLETE", str(ctx.exception))

    def test_spec_dir_in_alternative_location(self):
        """usecase-specifications/ が working_dir 直下にある配置も検出する"""
        _make_phase_a_complete_fixture(self.tmp, self.project, uc_count=2)
        # {project}/usecase-specifications/ を working_dir/usecase-specifications/ に移動
        old_dir = self.tmp / self.project / "usecase-specifications"
        new_dir = self.tmp / "usecase-specifications"
        shutil.move(str(old_dir), str(new_dir))

        result = vso.verify_phase_a_completeness(self.project, self.tmp)
        self.assertTrue(
            result["is_complete"],
            f"Should find spec dir at alt location, got: {result}",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
