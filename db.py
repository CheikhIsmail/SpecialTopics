import sqlite3
from datetime import datetime


class UsageDB:
    def __init__(self, path="usage.db"):
        self.conn = sqlite3.connect(path)
        self._create_tables()

    def _create_tables(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS api_calls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ts TEXT NOT NULL,
                model TEXT NOT NULL,
                tokens_in INTEGER NOT NULL,
                tokens_out INTEGER NOT NULL,
                cost_usd REAL NOT NULL,
                note TEXT
            )
        """)
        self.conn.commit()

        self.conn.execute("""
    CREATE TABLE IF NOT EXISTS indexed_docs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        doc_hash TEXT UNIQUE NOT NULL,
        chunks INTEGER NOT NULL,
        indexed_at TEXT NOT NULL
    )
""")

    def log(self, model, tokens_in, tokens_out, cost_usd, note=""):
        self.conn.execute(
            """
            INSERT INTO api_calls
            (ts, model, tokens_in, tokens_out, cost_usd, note)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.utcnow().isoformat(),
                model,
                tokens_in,
                tokens_out,
                cost_usd,
                note
            )
        )
        self.conn.commit()

    def stats(self):
        cur = self.conn.execute(
            """
            SELECT
                model,
                COUNT(*) AS calls,
                SUM(tokens_in + tokens_out) AS total_tokens,
                ROUND(SUM(cost_usd), 6) AS total_cost
            FROM api_calls
            GROUP BY model
            """
        )

        for row in cur.fetchall():
            print(
                f"{row[0]:20s}  "
                f"{row[1]:4d} calls  "
                f"{row[2]:8d} tokens  "
                f"${row[3]:.6f}"
            )