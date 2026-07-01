from analysis.graph import get_graph


def compute_weighted_centrality():

    graph = get_graph()

    scores = {}

    for node in graph:
        scores[node] = 1.0

    for _ in range(3):

        new_scores = {}

        for node, neighbors in graph.items():

            total = sum(neighbors.values())

            if total == 0:
                continue

            for n, w in neighbors.items():

                new_scores[n] = new_scores.get(n, 0) + (
                    scores[node] * (w / total)
                )

        scores = new_scores

    return sorted(
        [{"wallet": k, "score": round(v, 3)} for k, v in scores.items()],
        key=lambda x: x["score"],
        reverse=True
    )[:10]