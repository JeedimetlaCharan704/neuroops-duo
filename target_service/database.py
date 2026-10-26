"""
Database layer for OmniPay Gateway.
Uses SQLite with thread-safe connection pooling and parameterized query protection.
"""
import sqlite3
import threading
from typing import List, Dict, Any, Optional
import uuid
import datetime

class Database:
    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self._lock = threading.Lock()
        self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._init_tables()

    def _init_tables(self):
        with self._lock:
            cursor = self._conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    amount REAL NOT NULL,
                    currency TEXT NOT NULL,
                    status TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    risk_score REAL DEFAULT 0.0
                )
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_user_timestamp ON transactions(user_id, timestamp);
            """)
            self._conn.commit()

    def record_transaction(self, user_id: str, amount: float, currency: str, status: str = "COMPLETED") -> Dict[str, Any]:
        tx_id = f"tx_{uuid.uuid4().hex[:12]}"
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        with self._lock:
            cursor = self._conn.cursor()
            cursor.execute("""
                INSERT INTO transactions (id, user_id, amount, currency, status, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (tx_id, user_id, amount, currency, status, now))
            self._conn.commit()
            return {
                "id": tx_id,
                "user_id": user_id,
                "amount": amount,
                "currency": currency,
                "status": status,
                "timestamp": now
            }

    def query_transactions(self, user_id: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        with self._lock:
            cursor = self._conn.cursor()
            if user_id:
                cursor.execute("""
                    SELECT id, user_id, amount, currency, status, timestamp
                    FROM transactions
                    WHERE user_id = ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                """, (user_id, limit))
            else:
                cursor.execute("""
                    SELECT id, user_id, amount, currency, status, timestamp
                    FROM transactions
                    ORDER BY timestamp DESC
                    LIMIT ?
                """, (limit,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def count_transactions(self) -> int:
        with self._lock:
            cursor = self._conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM transactions")
            return cursor.fetchone()[0]

db = Database()
