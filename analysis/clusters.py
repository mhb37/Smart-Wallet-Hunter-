from collections import defaultdict, Counter

# mémoire globale runtime
CO_OCCURRENCE = defaultdict(Counter)
CLUSTER_HISTORY = []


def update_clusters(wallets: list[str]):

    # enregistre co-occurrence entre wallets
    for w1 in wallets:
        for w2 in wallets:

            if w1 == w2:
                continue

            CO_OCCURRENCE[w1][w2] += 1


def compute_clusters(min_link=2):

    clusters = []

    visited = set()

    for wallet, neighbors in CO_OCCURRENCE.items():

        if wallet in visited:
            continue

        cluster = set([wallet])

        for n, count in neighbors.items():

            if count >= min_link:
                cluster.add(n)

        if len(cluster) >= 2:
            clusters.append(list(cluster))
            visited.update(cluster)

    return clusters


def get_cluster_score(cluster):

    score = 0

    for w in cluster:
        score += sum(CO_OCCURRENCE[w].values())

    return score