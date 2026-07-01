from collections import defaultdict


# wallet -> set(wallets liés)
GRAPH = defaultdict(set)


def add_connections(wallets):
    """
    Crée des liens entre wallets apparaissant dans le même scan
    """
    for w1 in wallets:
        for w2 in wallets:
            if w1 != w2:
                GRAPH[w1].add(w2)


def get_graph():
    return GRAPH