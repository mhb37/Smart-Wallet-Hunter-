from datetime import datetime

from discovery.scanner import discover_wallet_candidates
from analysis.wallet_score import score_wallets


def discover_wallets_job():

    now = datetime.utcnow()

    print(f"\n🔁 [SCHEDULER] Scan exécuté à {now}")

    # 1. Discovery
    wallets = discover_wallet_candidates()

    print(f"📊 {len(wallets)} wallets détectés")

    if not wallets:
        print("⚠️ Aucun wallet trouvé")
        return

    # 2. Scoring (si module OK)
    try:
        scored = score_wallets(wallets)

        print("\n🏆 TOP WALLETS")

        for w in scored[:5]:
            print(
                f"- {w['wallet'][:6]}... "
                f"Score={w['score']} "
                f"Connexions={w.get('connections', 0)}"
            )

    except Exception as e:
        print("⚠️ Erreur scoring:", str(e))
        print("RAW wallets:", wallets)