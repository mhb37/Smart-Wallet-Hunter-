from collections import defaultdict

GRAPH = defaultdict(dict)


def add_connections(wallets):

    for w1 in wallets:
        for w2 in wallets:

            if w1 == w2:
                continue

            # poids du lien (co-appearance)
            if w2 in GRAPH[w1]:
                GRAPH[w1][w2] += 1
            else:
                GRAPH[w1][w2] = 1


def get_graph():
    return GRAPH