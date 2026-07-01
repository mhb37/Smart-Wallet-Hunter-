import logging
import threading
import time
from datetime import datetime

from discovery.scanner import scan_wallets

from storage.db import (
    init_db,
    upsert_wallet
)

from analysis.smart_money import compute_smart_wallets
from analysis.centrality import compute_weighted_centrality
from analysis.behavior import classify_wallets

from analysis.graph import (
    load_graph,
    save_graph,
    add_connections
)

from analysis.clusters import (
    update_clusters,
    compute_clusters,
    get_cluster_score
)


logger = logging.getLogger(__name__)


def start_scheduler():
    """
    Background scanner thread (Railway compatible)
    """

    init_db()
    load_graph()

    def loop():

        while True:

            try:
                run_scan()

            except Exception:
                logger.exception("Scheduler error")

            time.sleep(60)

    threading.Thread(
        target=loop,
        daemon=True
    ).start()


def run_scan():

    logger.info("🔁 [SCAN] %s", datetime.utcnow())

    wallets = scan_wallets()

    logger.info("📊 %s wallets détectés", len(wallets))

    if not wallets:
        return

    # =====================
    # STORAGE
    # =====================

    for wallet in wallets:
        upsert_wallet(wallet)

    # =====================
    # GRAPH
    # =====================

    add_connections(wallets)
    save_graph()

    # =====================
    # CLUSTERS
    # =====================

    update_clusters(wallets)

    # =====================
    # SMART MONEY V3
    # =====================

    logger.info("🔥 SMART MONEY (V3)")

    for row in compute_smart_wallets()[:10]:

        logger.info(
            "- %s score=%.1f appear=%s",
            row["wallet"][:6],
            row["score"],
            row["appearances"]
        )

    # =====================
    # GRAPH LEADERS V4
    # =====================

    logger.info("🧠 GRAPH LEADERS (V4)")

    for row in compute_weighted_centrality()[:10]:

        logger.info(
            "- %s centrality=%s",
            row["wallet"][:6],
            row["score"]
        )

    # =====================
    # WALLET BEHAVIOR V5
    # =====================

    logger.info("🧬 WALLET BEHAVIOR (V5)")

    for row in classify_wallets()[:10]:

        logger.info(
            "- %s %s intensity=%s",
            row["wallet"][:6],
            row["behavior"],
            row["intensity"]
        )

    # =====================
    # SMART CLUSTERS V9
    # =====================

    logger.info("🧬 SMART MONEY CLUSTERS (V9)")

    clusters = compute_clusters()

    for cluster in clusters[:10]:

        score = get_cluster_score(cluster)

        logger.info(
            "- cluster size=%s score=%s wallets=%s",
            len(cluster),
            score,
            [w[:6] for w in cluster[:5]]
        )