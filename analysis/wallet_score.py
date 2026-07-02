from collections import Counter


def score_wallets(wallets):

    counter = Counter(wallets)

    results = []

    for wallet, count in counter.items():

        results.append({
            "wallet": wallet,
            "appear": count,
            "score": count * count
        })

    return sorted(
        results,
        key=lambda x: x["score"],
        reverse=True
    )