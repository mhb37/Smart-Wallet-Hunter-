from datetime import datetime
from discovery.scanner import discover_wallet_candidates


def discover_wallets_job():

    now = datetime.utcnow()

    wallets = discover_wallet_candidates()

    print(f"🔁 [SCHEDULER] Scan exécuté à {now}")
    print(f"📊 {len(wallets)} wallets détectés")

    # debug affichage
    if wallets:
        print("Exemples:")
        for w in wallets[:5]:
            print(" -", w)