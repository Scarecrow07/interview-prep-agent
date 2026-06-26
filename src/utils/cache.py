"""LLM 结果缓存（基于 SQLite）"""

import hashlib
import json
import sqlite3
from pathlib import Path


_CACHE_DB: Path | None = None


def _get_conn() -> sqlite3.Connection:
    global _CACHE_DB
    if _CACHE_DB is None:
        _CACHE_DB = Path.home() / ".interview_prep_cache.sqlite"
    conn = sqlite3.connect(str(_CACHE_DB))
    conn.execute(
        "CREATE TABLE IF NOT EXISTS cache "
        "(key TEXT PRIMARY KEY, value TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
    )
    return conn


def _make_key(model_name: str, *texts: str) -> str:
    raw = model_name + "|".join(texts)
    return hashlib.sha256(raw.encode()).hexdigest()


def get_cache(model_name: str, *texts: str) -> dict | None:
    """获取缓存结果"""
    key = _make_key(model_name, *texts)
    conn = _get_conn()
    row = conn.execute(
        "SELECT value FROM cache WHERE key = ?", (key,)
    ).fetchone()
    conn.close()
    if row:
        return json.loads(row[0])
    return None


def set_cache(model_name: str, value: dict, *texts: str) -> None:
    """写入缓存"""
    key = _make_key(model_name, *texts)
    conn = _get_conn()
    conn.execute(
        "INSERT OR REPLACE INTO cache (key, value) VALUES (?, ?)",
        (key, json.dumps(value, ensure_ascii=False)),
    )
    conn.commit()
    conn.close()