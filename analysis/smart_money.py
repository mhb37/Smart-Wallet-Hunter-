from storage.db import get_all_wallets
import time


def compute_smart_wallets():

    rows = get_all_wallets()
    now = int(time.time())

    results = []

    for wallet, first_seen, last_seen, appearances in rows:

        score = 0

        # 1. activité brute
        score += appearances * 10

        # 2. récence (plus récent = mieux)
        age = now - last_seen
        if age < 3600:
            score += 50
        elif age < 86400:
            score += 30
        elif age < 604800:
            score += 10

        # 3. ancienneté (bonus long terme)
        lifetime = now - first_seen
        score += min(lifetime / 100000, 20)

        results.append({
            "wallet": wallet,
            "score": round(score, 2),
            "appearances": appearances,
            "age_seconds": age
        })

    results.sort(key=lambda x: x["score"], reverse=True)

    return results[:10]