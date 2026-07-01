from datetime import datetime

from discovery.scanner import discover_wallet_candidates
from storage.db import upsert_wallet
from analysis.smart_money import compute_smart_wallets
from analysis.graph import add_connections
from analysis.centrality import compute_weighted_centrality
from analysis.behavior import classify_wallets


def discover_wallets_job():

    now = datetime.utcnow()

    print(f"\n🔁 [SCAN] {now}")

    wallets = discover_wallet_candidates()

    print(f"📊 {len(wallets)} wallets détectés")

    if not wallets:
        return

    # =========================
    # STORE
    # =========================
    for w in wallets:
        upsert_wallet(w)

    # =========================
    # GRAPH
    # =========================
    add_connections(wallets)

    # =========================
    # V3 SMART SCORE
    # =========================
    top = compute_smart_wallets()

    print("\n🔥 SMART MONEY (V3)")
    for w in top:
        print(f"- {w['wallet'][:6]} score={w['score']} appear={w['appearances']}")

    # =========================
    # V4 CENTRALITY
    # =========================
    central = compute_weighted_centrality()

    print("\n🧠 GRAPH LEADERS (V4)")
    for w in central:
        print(f"- {w['wallet'][:6]} centrality={w['score']}")

    # =========================
    # V5 BEHAVIOR CLASSIFICATION
    # =========================
    behavior = classify_wallets()

    print("\n🧬 WALLET BEHAVIOR (V5)")

    for w in behavior[:10]:
        print(
            f"- {w['wallet'][:6]} "
            f"{w['behavior']} "
            f"intensity={w['intensity']}"
        )