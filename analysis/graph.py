from collections import defaultdict
import json
import os

GRAPH_FILE = "storage/graph.json"

GRAPH = defaultdict(dict)


def load_graph():

    global GRAPH

    if not os.path.exists(GRAPH_FILE):
        return

    try:
        with open(GRAPH_FILE, "r") as f:
            data = json.load(f)

        for k, v in data.items():
            GRAPH[k] = v

    except Exception:
        GRAPH = defaultdict(dict)


def save_graph():

    try:
        with open(GRAPH_FILE, "w") as f:
            json.dump(GRAPH, f)

    except Exception:
        pass


def add_connections(wallets):

    # graph pondéré simple
    for w1 in wallets:
        for w2 in wallets:

            if w1 == w2:
                continue

            if w2 in GRAPH[w1]:
                GRAPH[w1][w2] += 1
            else:
                GRAPH[w1][w2] = 1


def get_graph():
    return GRAPH