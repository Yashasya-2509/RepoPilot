import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


class TaskStore:
    """Small SQLite store. Each operation uses its own connection."""

    def __init__(self, database_path: Path):
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self):
        connection = sqlite3.connect(self.database_path, timeout=10)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self):
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    task_id TEXT PRIMARY KEY,
                    task_type TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                )
                """
            )

    def create_task(self, task_id: str, task_type: str, status: str, payload: dict) -> dict:
        created_at = datetime.now(timezone.utc).isoformat()
        with self._connect() as connection:
            connection.execute(
                "INSERT INTO tasks(task_id, task_type, status, created_at, payload_json) VALUES (?, ?, ?, ?, ?)",
                (task_id, task_type, status, created_at, json.dumps(payload)),
            )
        return {
            "task_id": task_id,
            "task_type": task_type,
            "status": status,
            "created_at": created_at,
            "payload": payload,
        }

    def get_task(self, task_id: str) -> dict | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT task_id, task_type, status, created_at, payload_json FROM tasks WHERE task_id = ?",
                (task_id,),
            ).fetchone()
        if row is None:
            return None
        return {
            "task_id": row["task_id"],
            "task_type": row["task_type"],
            "status": row["status"],
            "created_at": row["created_at"],
            "payload": json.loads(row["payload_json"]),
        }
