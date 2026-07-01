from collections import defaultdict
import time


WALLET_HISTORY = defaultdict(list)
WALLET_CONNECTIONS = defaultdict(set)


def update_wallet_activity(wallets):
    """
    Enregistre les wallets vus dans le scan
    et construit un réseau simple de connexions
    """

    timestamp = time.time()

    # historique
    for w in wallets:
        WALLET_HISTORY[w].append(timestamp)

    # réseau : tous les wallets vus ensemble sont connectés
    for w1 in wallets:
        for w2 in wallets:
            if w1 != w2:
                WALLET_CONNECTIONS[w1].add(w2)


def compute_wallet_score(wallet):

    now = time.time()

    history = WALLET_HISTORY.get(wallet, [])
    connections = WALLET_CONNECTIONS.get(wallet, set())

    # activité totale
    activity_score = min(len(history) * 2, 30)

    # récence (24h)
    recent = sum(1 for t in history if now - t < 86400)
    recency_score = min(recent * 3, 25)

    # réseau (clé du système C)
    network_score = min(len(connections) * 1.5, 35)

    # diversité du réseau
    diversity_score = min(len(set(connections)) * 0.5, 10)

    total_score = activity_score + recency_score + network_score + diversity_score

    return {
        "wallet": wallet,
        "score": round(total_score, 2),
        "connections": len(connections)
    }


def score_wallets(wallets):

    update_wallet_activity(wallets)

    results = [compute_wallet_score(w) for w in wallets]

    results.sort(key=lambda x: x["score"], reverse=True)

    return results