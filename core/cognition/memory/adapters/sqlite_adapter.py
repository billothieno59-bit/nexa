"""
NEXA Africa Operating System
File: core/cognition/memory/adapters/sqlite_adapter.py
Constitutional Owner: Bill Odhiambo Othieno
Description: Zero-dependency SQLite persistent adapter for the cognition
             memory layer. Defaults to a real file on disk so memory
             survives a restart; pass db_path=":memory:" explicitly for
             ephemeral/test use.
"""

import json
import os
import sqlite3
from typing import Any, Dict, List, Optional
from core.cognition.memory.adapters.base import BaseMemoryAdapter
from core.services.logging.logger import get_logger

logger = get_logger(__name__)

DEFAULT_DB_PATH = os.path.join("data", "cognition_memory.db")


class SQLiteMemoryAdapter(BaseMemoryAdapter):
    """
    Zero-dependency SQLite persistent adapter for the cognition memory layer.

    Defaults to a real file on disk (DEFAULT_DB_PATH) so stored memory
    survives a process restart. Pass db_path=":memory:" explicitly when
    ephemeral, isolated storage is actually wanted (e.g. in tests).
    """

    def __init__(self, db_path: str = DEFAULT_DB_PATH):
        self.db_path = db_path
        self._shared_conn: Optional[sqlite3.Connection] = None

        if self.db_path == ":memory:":
            self._shared_conn = sqlite3.connect(":memory:")
            self._shared_conn.row_factory = sqlite3.Row
        else:
            directory = os.path.dirname(self.db_path)
            if directory:
                os.makedirs(directory, exist_ok=True)

        self._init_db()
        logger.info("SQLiteMemoryAdapter initialized at db_path=%s", self.db_path)

    def _get_connection(self) -> sqlite3.Connection:
        if self._shared_conn:
            return self._shared_conn
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        conn = self._get_connection()
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS memory_ledger (
                key TEXT PRIMARY KEY,
                payload TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()

    def save(self, key: str, value: Dict[str, Any]) -> bool:
        payload = json.dumps(value)
        conn = self._get_connection()
        conn.execute(
            """
            INSERT INTO memory_ledger (key, payload)
            VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET payload=excluded.payload
            """,
            (key, payload),
        )
        conn.commit()
        return True

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        conn = self._get_connection()
        cursor = conn.execute(
            "SELECT payload FROM memory_ledger WHERE key = ?", (key,)
        )
        row = cursor.fetchone()
        if row:
            return json.loads(row["payload"])
        return None

    def delete(self, key: str) -> bool:
        conn = self._get_connection()
        cursor = conn.execute(
            "DELETE FROM memory_ledger WHERE key = ?", (key,)
        )
        conn.commit()
        return cursor.rowcount > 0

    def list_all(self) -> List[Dict[str, Any]]:
        conn = self._get_connection()
        cursor = conn.execute("SELECT payload FROM memory_ledger")
        rows = cursor.fetchall()
        return [json.loads(row["payload"]) for row in rows]
