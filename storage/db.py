import sqlite3
import time

DB_PATH = "storage/wallets.db"


def init_db():

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS wallets (
        wallet TEXT PRIMARY KEY,
        first_seen INTEGER,
        last_seen INTEGER,
        appearances INTEGER
    )
    """)

    conn.commit()
    conn.close()


def upsert_wallet(wallet):

    now = int(time.time())

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute(
        "SELECT * FROM wallets WHERE wallet = ?",
        (wallet,)
    )

    row = c.fetchone()

    if row:

        c.execute("""
        UPDATE wallets
        SET last_seen = ?,
            appearances = appearances + 1
        WHERE wallet = ?
        """, (now, wallet))

    else:

        c.execute("""
        INSERT INTO wallets (
            wallet,
            first_seen,
            last_seen,
            appearances
        )
        VALUES (?, ?, ?, 1)
        """, (wallet, now, now))

    conn.commit()
    conn.close()


def get_all_wallets():

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    SELECT wallet,
           first_seen,
           last_seen,
           appearances
    FROM wallets
    """)

    rows = c.fetchall()

    conn.close()

    return rows