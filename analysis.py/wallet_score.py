from collections import defaultdict
import time


# mémoire simple en RAM (MVP)
WALLET_HISTORY = defaultdict(list)
WALLET_CONNECTIONS = defaultdict(set)


def update_wallet_activity(wallets):
    """
    Enregistre les wallets vus dans le scan courant
    et construit un graphe de connexions simples
    """

    timestamp = time.time()

    for w in wallets:
        WALLET_HISTORY[w].append(timestamp)

    # connexion simple : tous les wallets vus ensemble sont liés
    for w1 in wallets:
        for w2 in wallets:
            if w1 != w2:
                WALLET_CONNECTIONS[w1].add(w2)


def compute_wallet_score(wallet):
    """
    Smart Score version graph-based
    """

    now = time.time()

    history = WALLET_HISTORY.get(wallet, [])
    connections = WALLET_CONNECTIONS.get(wallet, set())

    # 1. activité
    activity_score = min(len(history) * 2, 30)

    # 2. récence
    recent_activity = 0
    for t in history:
        if now - t < 3600 * 24:  # 24h
            recent_activity += 1

    recency_score = min(recent_activity * 3, 25)

    # 3. réseau (clé du système)
    network_score = min(len(connections) * 1.5, 35)

    # 4. diversité du réseau (approx)
    diversity_score = min(len(set(connections)) * 0.5, 10)

    total_score = (
        activity_score +
        recency_score +
        network_score +
        diversity_score
    )

    return {
        "wallet": wallet,
        "score": round(total_score, 2),
        "activity_score": activity_score,
        "recency_score": recency_score,
        "network_score": network_score,
        "connections": len(connections)
    }


def score_wallets(wallets):
    """
    Score un batch complet
    """

    update_wallet_activity(wallets)

    results = []

    for w in wallets:
        results.append(compute_wallet_score(w))

    # tri par score décroissant
    results.sort(key=lambda x: x["score"], reverse=True)

    return results