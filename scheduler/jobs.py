from datetime import datetime

from discovery.scanner import discover_wallet_candidates
from storage.db import upsert_wallet
from analysis.smart_money import compute_smart_wallets
from analysis.graph import add_connections
from analysis.centrality import compute_centrality


def discover_wallets_job():

    now = datetime.utcnow()

    print(f"\n🔁 [SCAN] {now}")

    wallets = discover_wallet_candidates()

    print(f"📊 {len(wallets)} wallets détectés")

    if not wallets:
        return

    # =========================
    # STORAGE SQLITE
    # =========================
    for w in wallets:
        upsert_wallet(w)

    # =========================
    # GRAPH BUILDING (V4 CORE)
    # =========================
    add_connections(wallets)

    # =========================
    # OLD SMART SCORE (V3)
    # =========================
    top = compute_smart_wallets()

    print("\n🔥 SMART MONEY TOP (V3)")
    for w in top:
        print(f"- {w['wallet'][:6]}... score={w['score']} appear={w['appearances']}")

    # =========================
    # NEW GRAPH CENTRALITY (V4)
    # =========================
    central = compute_centrality()

    print("\n🧠 GRAPH LEADERS (V4)")
    for w in central:
        print(f"- {w['wallet'][:6]}... centrality={w['score']}")