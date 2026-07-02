import sqlite3
from datetime import datetime


DB_PATH = "database/wallets.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS wallets (

            wallet TEXT PRIMARY KEY,

            first_seen TEXT NOT NULL,
            last_seen TEXT NOT NULL,

            appearances INTEGER DEFAULT 0,
            score INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()


def save_wallet(wallet):

    now = datetime.utcnow().isoformat()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT appearances, score FROM wallets WHERE wallet = ?",
        (wallet,)
    )

    row = cursor.fetchone()

    if row:

        appearances, score = row

        cursor.execute(
            """
            UPDATE wallets
            SET appearances = ?,
                score = ?,
                last_seen = ?
            WHERE wallet = ?
            """,
            (
                appearances + 1,
                score + 10,
                now,
                wallet,
            )
        )

    else:

        cursor.execute(
            """
            INSERT INTO wallets (
                wallet,
                first_seen,
                last_seen,
                appearances,
                score
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                wallet,
                now,
                now,
                1,
                10,
            )
        )

    conn.commit()
    conn.close()


def save_wallets(wallets):

    for wallet in wallets:
        save_wallet(wallet)


def get_top_wallets(limit=20):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            wallet,
            appearances,
            score,
            first_seen,
            last_seen
        FROM wallets
        ORDER BY score DESC, appearances DESC
        LIMIT ?
        """,
        (limit,)
    )

    rows = cursor.fetchall()

    conn.close()

    return [
        {
            "wallet": row[0],
            "appear": row[1],
            "score": row[2],
            "first_seen": row[3],
            "last_seen": row[4],
        }
        for row in rows
    ]


def wallet_exists(wallet):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT 1 FROM wallets WHERE wallet = ?",
        (wallet,)
    )

    result = cursor.fetchone()

    conn.close()

    return result is not None