from collections import defaultdict
import time


WALLET_HISTORY = defaultdict(list)
WALLET_CONNECTIONS = defaultdict(set)


def update_wallet_activity(wallets):
    timestamp = time.time()

    for w in wallets:
        WALLET_HISTORY[w].append(timestamp)

    for w1 in wallets:
        for w2 in wallets:
            if w1 != w2:
                WALLET_CONNECTIONS[w1].add(w2)


def compute_wallet_score(wallet):

    now = time.time()

    history = WALLET_HISTORY.get(wallet, [])
    connections = WALLET_CONNECTIONS.get(wallet, set())

    activity_score = min(len(history) * 2, 30)

    recent_activity = sum(
        1 for t in history if now - t < 86400
    )
    recency_score = min(recent_activity * 3, 25)

    network_score = min(len(connections) * 1.5, 35)

    diversity_score = min(len(set(connections)) * 0.5, 10)

    total = activity_score + recency_score + network_score + diversity_score

    return {
        "wallet": wallet,
        "score": round(total, 2),
        "connections": len(connections)
    }


def score_wallets(wallets):

    update_wallet_activity(wallets)

    results = [compute_wallet_score(w) for w in wallets]

    results.sort(key=lambda x: x["score"], reverse=True)

    return results