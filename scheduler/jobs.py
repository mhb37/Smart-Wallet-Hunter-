from datetime import datetime

from discovery.scanner import discover_wallet_candidates
from storage.db import upsert_wallet

from analysis.graph import add_connections
from analysis.centrality import compute_weighted_centrality

from analysis.clusters import update_clusters, compute_clusters, get_cluster_score


def discover_wallets_job():

    now = datetime.utcnow()

    print(f"\n🔁 [SCAN] {now}")

    wallets = discover_wallet_candidates()

    print(f"📊 {len(wallets)} wallets détectés")

    if not wallets:
        return

    # =========================
    # STORE
    # =========================
    for w in wallets:
        upsert_wallet(w)

    # =========================
    # GRAPH (V4 toujours actif)
    # =========================
    add_connections(wallets)

    central = compute_weighted_centrality()

    print("\n🧠 GRAPH LEADERS (V4)")
    for w in central[:5]:
        print(f"- {w['wallet'][:6]} centrality={w['score']}")

    # =========================
    # V9 CLUSTERS ENGINE (NOUVEAU)
    # =========================
    update_clusters(wallets)

    clusters = compute_clusters()

    print("\n🧬 SMART MONEY CLUSTERS (V9)")

    if not clusters:
        print("- aucun cluster stable")
        return

    for c in clusters[:5]:

        score = get_cluster_score(c)

        print(f"\n🔥 CLUSTER (score={score})")

        for w in c[:5]:
            print(f"- {w[:6]}")