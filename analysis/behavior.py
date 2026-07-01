from storage.db import get_all_wallets
import time


def classify_wallets():

    rows = get_all_wallets()
    now = int(time.time())

    results = []

    for wallet, first_seen, last_seen, appearances in rows:

        age = now - first_seen
        recency = now - last_seen

        # =========================
        # 1. INTENSITY SCORE
        # =========================
        intensity = appearances / max(age / 3600, 1)

        # =========================
        # 2. BEHAVIOR RULES
        # =========================

        if appearances >= 10 and recency < 86400:
            behavior = "ACCUMULATOR"   # actif + récurrent

        elif appearances >= 5 and recency < 86400 * 3:
            behavior = "ACTIVE_TRADER"

        elif appearances == 1 and recency < 3600:
            behavior = "NEW_ACTIVE"

        elif recency > 86400 * 7:
            behavior = "INACTIVE"

        else:
            behavior = "NOISE"

        results.append({
            "wallet": wallet,
            "behavior": behavior,
            "intensity": round(intensity, 4),
            "appearances": appearances,
            "recency": recency
        })

    # tri par importance
    results.sort(key=lambda x: x["intensity"], reverse=True)

    return results[:20]