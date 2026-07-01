from analysis.graph import get_graph


def compute_weighted_centrality():

    graph = get_graph()

    scores = {}

    # init
    for node in graph:
        scores[node] = 1.0

    # propagation pondérée
    for _ in range(4):

        new_scores = {}

        for node, neighbors in graph.items():

            total_weight = sum(neighbors.values())

            if total_weight == 0:
                continue

            for n, weight in neighbors.items():

                new_scores[n] = new_scores.get(n, 0) + (
                    scores[node] * (weight / total_weight)
                )

        scores = new_scores

    return sorted(
        [{"wallet": k, "score": round(v, 3)} for k, v in scores.items()],
        key=lambda x: x["score"],
        reverse=True
    )[:10]