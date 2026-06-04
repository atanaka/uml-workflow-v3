#!/usr/bin/env python3
"""
Environment Path Resolver
Web版 (Claude.ai Skills sandbox) とローカル版 (Claude Code) の両方で
動作させるためのパス解決ユーティリティ。

判定方針:
- スキル本体ディレクトリは、このファイルの位置 (__file__) から解決する。
  これは Web (/mnt/skills/user/...) でもローカル (~/.claude/skills/...) でも常に正しい。
- 成果物の出力ディレクトリは以下の優先順位で決定する:
    1. 環境変数 UML_WORKFLOW_OUTPUT_DIR が指定されていればそれを使う
    2. Web sandbox の /mnt/user-data/outputs が存在すればそれを使う
    3. それ以外 (ローカル) はカレントワーキングディレクトリを使う
"""

import os
from pathlib import Path

# Web sandbox の標準出力先（存在すれば Web 環境と判定）
_WEB_OUTPUT_DIR = Path("/mnt/user-data/outputs")


def is_web_environment() -> bool:
    """Web版 (Claude.ai Skills sandbox) で動作しているかを判定する。"""
    return _WEB_OUTPUT_DIR.exists()


def get_scripts_dir() -> Path:
    """このスキルの scripts ディレクトリを返す（環境非依存）。"""
    return Path(__file__).resolve().parent


def get_skill_dir() -> Path:
    """このスキルのルートディレクトリを返す（環境非依存）。"""
    return get_scripts_dir().parent


def get_output_dir() -> Path:
    """成果物の出力ディレクトリを返す（環境非依存）。

    優先順位:
      1. 環境変数 UML_WORKFLOW_OUTPUT_DIR
      2. Web sandbox の /mnt/user-data/outputs
      3. カレントワーキングディレクトリ（ローカル）
    """
    env = os.environ.get("UML_WORKFLOW_OUTPUT_DIR")
    if env:
        return Path(env)
    if _WEB_OUTPUT_DIR.exists():
        return _WEB_OUTPUT_DIR
    return Path.cwd()


def get_cache_dir() -> Path:
    """キャッシュディレクトリを返す（出力ディレクトリ配下）。"""
    return get_output_dir() / "workflow-cache"
