import logging
import threading
import time
from datetime import datetime

from discovery.scanner import scan_wallets

from analysis.wallet_score import score_wallets
from analysis.centrality import compute_weighted_centrality
from analysis.behavior import classify_wallets
from analysis.clusters import (
    update_clusters,
    compute_clusters,
    get_cluster_score,
)
from analysis.graph import (
    load_graph,
    save_graph,
    add_connections,
)

logger = logging.getLogger(__name__)


def start_scheduler():
    """
    Railway-friendly scheduler
    """

    # Charge le graphe une seule fois au démarrage
    load_graph()

    def loop():

        logger.info("🟢 Scheduler STARTED")

        while True:

            try:
                run_scan()

            except Exception:
                logger.exception("Scheduler error")

            time.sleep(60)

    threading.Thread(
        target=loop,
        daemon=True,
        name="scanner-thread"
    ).start()


def run_scan():

    logger.info("🔁 [SCAN] %s", datetime.utcnow())

    wallets = scan_wallets()

    logger.info(
        "📊 %s wallets détectés",
        len(wallets)
    )

    if not wallets:
        return

    # ==========================
    # UPDATE GRAPH
    # ==========================

    try:

        add_connections(wallets)
        save_graph()

    except Exception:
        logger.exception("Graph update failed")

    # ==========================
    # V3 SMART MONEY
    # ==========================

    scored = score_wallets(wallets)

    logger.info("🔥 SMART MONEY TOP 10")

    for item in scored[:10]:

        logger.info(
            "- %s score=%.1f appear=%s",
            item["wallet"],
            item["score"],
            item.get("appear", 1)
        )

    # ==========================
    # V4 GRAPH
    # ==========================

    try:

        leaders = compute_weighted_centrality()

        logger.info("🧠 GRAPH LEADERS (V4)")

        for item in leaders[:10]:

            logger.info(
                "- %s centrality=%.3f",
                item["wallet"][:6],
                item["score"]
            )

    except Exception:
        logger.exception("Centrality failed")

    # ==========================
    # V5 BEHAVIOR
    # ==========================

    try:

        behaviors = classify_wallets()

        logger.info("🧬 WALLET BEHAVIOR (V5)")

        for item in behaviors[:10]:

            logger.info(
                "- %s %s intensity=%.2f",
                item["wallet"][:6],
                item["behavior"],
                item["intensity"]
            )

    except Exception:
        logger.exception("Behavior failed")

    # ==========================
    # V9 CLUSTERS
    # ==========================

    try:

        update_clusters(wallets)

        clusters = compute_clusters()

        logger.info("🧬 SMART MONEY CLUSTERS (V9)")

        for i, cluster in enumerate(clusters[:10], 1):

            score = get_cluster_score(cluster)

            logger.info(
                "- Cluster #%s | size=%s | score=%s | wallets=%s",
                i,
                len(cluster),
                score,
                [w[:6] for w in cluster[:5]]
            )

    except Exception:
        logger.exception("Clusters failed")