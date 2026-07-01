from analysis.graph import get_graph


def compute_centrality():
    """
    Score simple type PageRank léger (approximation)
    """

    graph = get_graph()

    scores = {}

    # init
    for node in graph:
        scores[node] = 1.0

    # itérations (diffusion influence)
    for _ in range(3):
        new_scores = {}

        for node in graph:
            neighbors = graph[node]

            if not neighbors:
                new_scores[node] = scores[node]
                continue

            share = scores[node] / len(neighbors)

            for n in neighbors:
                new_scores[n] = new_scores.get(n, 0) + share

        scores = new_scores

    # format final
    return sorted(
        [{"wallet": k, "score": round(v, 2)} for k, v in scores.items()],
        key=lambda x: x["score"],
        reverse=True
    )[:10]