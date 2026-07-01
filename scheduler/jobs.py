from datetime import datetime

from discovery.scanner import discover_wallet_candidates
from storage.db import upsert_wallet
from analysis.smart_money import compute_smart_wallets


def discover_wallets_job():

    now = datetime.utcnow()

    print(f"\n🔁 [SCAN] {now}")

    wallets = discover_wallet_candidates()

    print(f"📊 {len(wallets)} wallets détectés")

    if not wallets:
        return

    # =========================
    # STORE IN DATABASE
    # =========================

    for w in wallets:
        upsert_wallet(w)

    print("\n🏷️ EXEMPLES:")

    for w in wallets[:5]:
        print(" -", w)

    # =========================
    # SMART MONEY OUTPUT
    # =========================

    top = compute_smart_wallets()

    print("\n🔥 SMART MONEY TOP 10")

    for w in top:
        print(
            f"- {w['wallet'][:6]}... "
            f"score={w['score']} "
            f"appear={w['appearances']}"
        )