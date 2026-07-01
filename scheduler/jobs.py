from datetime import datetime


def discover_wallets_job():
    print(f"[{datetime.now()}] Scan automatique lancé")

    # Plus tard :
    # wallets = discover_wallet_candidates()
    # analyze_wallets(wallets)
    # send_notifications()