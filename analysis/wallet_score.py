from storage.db import upsert_wallet, get_all_wallets


def score_wallets(wallets):

    for wallet in wallets:
        upsert_wallet(wallet)

    rows = get_all_wallets()

    results = []

    for wallet, first_seen, last_seen, appearances in rows:

        score = 50 + appearances * 10

        results.append({
            "wallet": wallet,
            "score": score,
            "appear": appearances
        })

    return sorted(
        results,
        key=lambda x: x["score"],
        reverse=True
    )