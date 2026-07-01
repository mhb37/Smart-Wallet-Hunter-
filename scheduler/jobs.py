from datetime import datetime
from discovery.scanner import discover_wallet_candidates
from analysis.wallet_score import score_wallets


def discover_wallets_job():

    now = datetime.utcnow()

    wallets = discover_wallet_candidates()

    print(f"\n🔁 SCAN {now}")
    print(f"📊 {len(wallets)} wallets détectés")

    if wallets:

        scored = score_wallets(wallets)

        print("\n🏆 TOP 5 WALLETS")

        for w in scored[:5]:
            print(
                f"{w['wallet'][:6]}... "
                f"Score={w['score']} "
                f"Connexions={w['connections']}"
            )