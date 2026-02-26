#!/usr/bin/env python3
"""
Workflow Cache Helper
中間成果物のキャッシュ管理を支援するヘルパーモジュール
"""

import os
import json
import hashlib
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

# キャッシュディレクトリ
CACHE_DIR = Path("/mnt/user-data/outputs/workflow-cache")
CACHE_INDEX_FILE = CACHE_DIR / "cache_index.json"

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

def cache_file(
    project_name: str,
    step_name: str,
    file_type: str,
    source_path: str
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
