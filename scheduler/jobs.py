from datetime import datetime

def discover_wallets_job():
    now = datetime.utcnow()

    print(f"🔁 [SCHEDULER] Scan exécuté à {now}")

    wallets = ["wallet_1", "wallet_2", "wallet_3"]

    print(f"📊 {len(wallets)} candidats générés")