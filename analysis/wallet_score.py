from collections import defaultdict


def score_wallets(wallets):
    """
    V3 scoring engine.
    Les wallets récurrents montent progressivement.
    """

    stats = defaultdict(
        lambda: {
            "score": 50.0,
            "appear": 0
        }
    )

    for wallet in wallets:

        stats[wallet]["appear"] += 1

        appear = stats[wallet]["appear"]

        # bonus de récurrence
        stats[wallet]["score"] = 50.0 + (appear * 10)

    result = []

    for wallet, data in stats.items():

        result.append({
            "wallet": wallet[:6],   # affichage court dans les logs
            "full_wallet": wallet,
            "score": data["score"],
            "appear": data["appear"]
        })

    return sorted(
        result,
        key=lambda x: x["score"],
        reverse=True
    )