from collections import defaultdict


def score_wallets(wallets):
    stats = defaultdict(lambda: {"score": 0, "appear": 0})

    for w in wallets:
        stats[w]["appear"] += 1
        stats[w]["score"] += 10

    return [
        {"wallet": k, **v}
        for k, v in stats.items()
    ]