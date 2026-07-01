import os
from datetime import datetime

from discovery.scanner import discover_wallet_candidates


# =========================
# DEBUG BOOT (IMPORTANT)
# =========================

print("\n===== RAILWAY DEBUG START =====")
print("WORKING DIR:", os.getcwd())

try:
    print("FILES:", os.listdir("."))
except Exception as e:
    print("ERROR LISTING FILES:", str(e))

print("PYTHON MODULE PATH TEST OK")
print("================================\n")


# =========================
# JOB PRINCIPAL
# =========================

def discover_wallets_job():

    now = datetime.utcnow()

    print(f"\n🔁 [SCHEDULER] Scan exécuté à {now}")

    # 1. Discovery
    try:
        wallets = discover_wallet_candidates()
    except Exception as e:
        print("❌ ERROR discovery:", str(e))
        return

    print(f"📊 {len(wallets)} wallets détectés")

    if not wallets:
        print("⚠️ Aucun wallet trouvé")
        return

    # 2. Affichage simple (sans scoring pour debug)
    print("\n🏷️ EXEMPLES WALLETS:")

    for w in wallets[:10]:
        print(" -", w)


# =========================
# SAFE FALLBACK SCORE (TEMPORAIRE)
# =========================

def score_wallets(wallets):
    """
    TEMPORAIRE : évite crash si analysis pas OK
    """
    return [
        {
            "wallet": w,
            "score": 1,
            "connections": 0
        }
        for w in wallets
    ]