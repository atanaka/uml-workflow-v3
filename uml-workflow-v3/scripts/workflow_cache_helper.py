#!/usr/bin/env python3
"""
Workflow Cache Helper
中間成果物のキャッシュ管理を支援するヘルパーモジュール

v3.2.0 変更点:
- CACHE_DIR をローカルディレクトリに変更（セッション間でも /home/claude 配下に永続）
- 環境変数 UML_WORKFLOW_CACHE_DIR / UML_WORKFLOW_OUTPUT_DIR で上書き可能
- save_phase_a_state / load_phase_a_state を追加（Phase A→B ハンドオフの自動化）
- restore_all_cached_files を追加（SKILL.md から参照されていたが未実装だった）
"""

import os
import json
import hashlib
import shutil
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime


def _resolve_cache_dir() -> Path:
    """
    環境に応じたキャッシュディレクトリを決定する。
    優先順位:
      1. 環境変数 UML_WORKFLOW_CACHE_DIR
      2. カレントディレクトリ配下 .uml-workflow-cache
         （ただし /mnt/user-data 以下は除外 — Claude.ai のサンドボックスは
           セッションをまたいで消える可能性があるため）
      3. ホームディレクトリ配下 .uml-workflow-cache（Claude.ai computer use 環境）
    """
    if env_dir := os.environ.get("UML_WORKFLOW_CACHE_DIR"):
        return Path(env_dir)

    cwd = Path.cwd()
    if not str(cwd).startswith("/mnt/user-data"):
        return cwd / ".uml-workflow-cache"

    # Claude.ai computer use: /home/claude 配下はセッション中に永続する
    return Path.home() / ".uml-workflow-cache"


# キャッシュディレクトリ（モジュール読み込み時に一度だけ解決）
CACHE_DIR = _resolve_cache_dir()
CACHE_INDEX_FILE = CACHE_DIR / "cache_index.json"

# Phase A 状態ファイル名
_PHASE_A_STATE_FILE = "phase-a-state.json"

def ensure_cache_dir():
    """キャッシュディレクトリが存在することを保証"""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

def get_cache_index() -> Dict[str, Any]:
    """キャッシュインデックスを取得"""
    ensure_cache_dir()
    if CACHE_INDEX_FILE.exists():
        with open(CACHE_INDEX_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_cache_index(index: Dict[str, Any]):
    """キャッシュインデックスを保存"""
    ensure_cache_dir()
    with open(CACHE_INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

def compute_file_hash(filepath: str) -> str:
    """ファイルのSHA256ハッシュを計算"""
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256.update(chunk)
    return sha256.hexdigest()

# ---------------------------------------------------------------------------
# Phase A 状態ファイル (#2 対応)
# ---------------------------------------------------------------------------

def save_phase_a_state(project_name: str, state: Dict[str, Any]) -> str:
    """
    Phase A 完了時の状態（テックスタック選択など）をファイルに保存する。

    SKILL.md の AUTO-SPLIT CHECKPOINT から呼び出す。
    Phase B 開始時に load_phase_a_state() で読み込み、
    ユーザーへのコピペ依存を解消する。

    Args:
        project_name: プロジェクト名
        state: 保存する状態辞書。推奨キー:
               - backend_framework  (例: "TypeScript + Express")
               - frontend_framework (例: "React + TypeScript + Vite + Tailwind CSS")
               - architecture       (例: "monolith")
               - generate_tests     (例: True)
               - language           (例: "Japanese")
               - completed_steps    (例: [1, 2, 3, 4, 5, 6, 7])
    Returns:
        保存されたファイルのパス
    """
    project_cache_dir = CACHE_DIR / project_name
    project_cache_dir.mkdir(parents=True, exist_ok=True)

    state_path = project_cache_dir / _PHASE_A_STATE_FILE
    payload = {
        **state,
        "project_name": project_name,
        "saved_at": datetime.now().isoformat(),
        "schema_version": "3.2.0",
    }
    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    print(f"  💾 Phase A 状態を保存しました: {state_path}")
    return str(state_path)


def load_phase_a_state(project_name: str) -> Optional[Dict[str, Any]]:
    """
    Phase A の状態ファイルを読み込む。

    Phase B 開始時（Step 8 から再開）に呼び出す。
    ファイルが存在しない場合は None を返す。

    Returns:
        状態辞書、または None（状態ファイルがない場合）
    """
    state_path = CACHE_DIR / project_name / _PHASE_A_STATE_FILE
    if not state_path.exists():
        return None
    with open(state_path, "r", encoding="utf-8") as f:
        state = json.load(f)
    print(f"  📂 Phase A 状態を読み込みました: {state_path}")
    return state


def restore_all_cached_files(project_name: str) -> int:
    """
    キャッシュされた全ファイルを出力ディレクトリに復元する。

    SKILL.md の Step 8 前処理（Phase B 開始時）から呼び出す。
    これまで SKILL.md に記述されていたが実装が存在しなかった (#1 対応)。

    Returns:
        復元したファイル数
    """
    index = get_cache_index()
    if project_name not in index:
        print(f"  ⚠️  キャッシュが見つかりません: {project_name}")
        return 0

    output_dir = Path(os.environ.get("UML_WORKFLOW_OUTPUT_DIR", "/mnt/user-data/outputs"))
    output_dir.mkdir(parents=True, exist_ok=True)

    restored = 0
    for key, info in index[project_name].items():
        cache_path = Path(info["cache_path"])
        if not cache_path.exists():
            print(f"  ⚠️  キャッシュファイルが見つかりません: {cache_path.name}")
            continue
        dest = output_dir / Path(info["original_path"]).name
        shutil.copy2(cache_path, dest)
        print(f"  ✅ 復元: {dest.name}")
        restored += 1

    print(f"  合計 {restored} ファイルを復元しました")
    return restored


# ---------------------------------------------------------------------------
# ファイルキャッシュ操作（既存）
# ---------------------------------------------------------------------------

def cache_file(
    project_name: str,
    step_name: str,
    file_type: str,
    source_path: str,
) -> str:
    """
    ファイルをキャッシュに保存
    
    Args:
        project_name: プロジェクト名
        step_name: ステップ名（例: "scenario-to-activity"）
        file_type: ファイルタイプ（例: "activity-data-json", "activity-puml"）
        source_path: ソースファイルのパス
    
    Returns:
        キャッシュされたファイルのパス
    """
    ensure_cache_dir()
    
    # プロジェクト専用のキャッシュディレクトリ
    project_cache_dir = CACHE_DIR / project_name
    project_cache_dir.mkdir(parents=True, exist_ok=True)
    
    # ファイル名を構築
    source_file = Path(source_path)
    cache_filename = f"{step_name}_{file_type}{source_file.suffix}"
    cache_path = project_cache_dir / cache_filename
    
    # ファイルをコピー
    import shutil
    shutil.copy2(source_path, cache_path)
    
    # キャッシュインデックスを更新
    index = get_cache_index()
    if project_name not in index:
        index[project_name] = {}
    
    index[project_name][f"{step_name}:{file_type}"] = {
        "cache_path": str(cache_path),
        "original_path": source_path,
        "file_hash": compute_file_hash(source_path),
        "cached_at": datetime.now().isoformat(),
        "step": step_name,
        "file_type": file_type
    }
    
    save_cache_index(index)
    
    return str(cache_path)

def get_cached_file(
    project_name: str,
    step_name: str,
    file_type: str
) -> Optional[str]:
    """
    キャッシュされたファイルのパスを取得
    
    Returns:
        キャッシュファイルのパス（存在しない場合はNone）
    """
    index = get_cache_index()
    
    if project_name not in index:
        return None
    
    key = f"{step_name}:{file_type}"
    if key not in index[project_name]:
        return None
    
    cache_info = index[project_name][key]
    cache_path = cache_info["cache_path"]
    
    # ファイルが実際に存在するか確認
    if os.path.exists(cache_path):
        return cache_path
    
    return None

def has_cached_step(project_name: str, step_name: str) -> bool:
    """指定されたステップのキャッシュが存在するかチェック"""
    index = get_cache_index()
    
    if project_name not in index:
        return False
    
    # そのステップに関連するキャッシュがあるか
    for key in index[project_name].keys():
        if key.startswith(f"{step_name}:"):
            cache_path = index[project_name][key]["cache_path"]
            if os.path.exists(cache_path):
                return True
    
    return False

def get_step_cache_info(project_name: str, step_name: str) -> Dict[str, Any]:
    """ステップのキャッシュ情報を取得"""
    index = get_cache_index()
    
    if project_name not in index:
        return {}
    
    result = {}
    for key, value in index[project_name].items():
        if key.startswith(f"{step_name}:"):
            result[key] = value
    
    return result

def clear_project_cache(project_name: str):
    """プロジェクトのキャッシュをクリア"""
    index = get_cache_index()
    
    if project_name in index:
        # ファイルを削除
        project_cache_dir = CACHE_DIR / project_name
        if project_cache_dir.exists():
            import shutil
            shutil.rmtree(project_cache_dir)
        
        # インデックスから削除
        del index[project_name]
        save_cache_index(index)

def clear_step_cache(project_name: str, step_name: str):
    """特定のステップのキャッシュをクリア"""
    index = get_cache_index()
    
    if project_name not in index:
        return
    
    # 該当するキーを収集
    keys_to_delete = [
        key for key in index[project_name].keys()
        if key.startswith(f"{step_name}:")
    ]
    
    # ファイルとインデックスエントリを削除
    for key in keys_to_delete:
        cache_path = index[project_name][key]["cache_path"]
        if os.path.exists(cache_path):
            os.remove(cache_path)
        del index[project_name][key]
    
    save_cache_index(index)

def list_cached_projects() -> list:
    """キャッシュされているプロジェクトのリストを取得"""
    index = get_cache_index()
    return list(index.keys())

def get_project_cache_summary(project_name: str) -> Dict[str, Any]:
    """プロジェクトのキャッシュサマリーを取得"""
    index = get_cache_index()
    
    if project_name not in index:
        return {
            "project_name": project_name,
            "cached": False,
            "steps": []
        }
    
    # ステップごとに整理
    steps = {}
    for key, value in index[project_name].items():
        step = value["step"]
        if step not in steps:
            steps[step] = {
                "step_name": step,
                "files": [],
                "cached_at": value["cached_at"]
            }
        steps[step]["files"].append({
            "file_type": value["file_type"],
            "cache_path": value["cache_path"],
            "exists": os.path.exists(value["cache_path"])
        })
    
    return {
        "project_name": project_name,
        "cached": True,
        "steps": list(steps.values())
    }

if __name__ == "__main__":
    # テスト用
    print("Workflow Cache Helper")
    print(f"Cache directory: {CACHE_DIR}")
    print(f"Cached projects: {list_cached_projects()}")
