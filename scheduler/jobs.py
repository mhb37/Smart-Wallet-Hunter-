import logging
import threading
import time
from datetime import datetime

from discovery.scanner import scan_wallets

from analysis.wallet_score import score_wallets
from analysis.centrality import compute_centrality
from analysis.behavior import analyze_behavior
from analysis.clusters import detect_clusters


logger = logging.getLogger(__name__)


def start_scheduler():
    """
    Simple scheduler compatible Railway/Render.
    Une seule boucle daemon.
    """

    def loop():
        logger.info("🟢 Scheduler STARTED")

        while True:
            try:
                run_scan()

            except Exception:
                logger.exception("Scheduler error")

            time.sleep(60)

    thread = threading.Thread(
        target=loop,
        daemon=True,
        name="wallet-scanner"
    )

    thread.start()


def run_scan():

    logger.info("🔁 [SCAN] %s", datetime.utcnow())

    wallets = scan_wallets()

    logger.info("📊 %s wallets détectés", len(wallets))

    if not wallets:
        return

    # =====================
    # V3 - SMART MONEY
    # =====================

    scored = score_wallets(wallets)

    logger.info("🔥 SMART MONEY (V3)")

    for w in scored[:10]:

        logger.info(
            "- %s score=%.1f appear=%s",
            w["wallet"],
            w["score"],
            w.get("appear", 1),
        )

    # =====================
    # V4 - GRAPH
    # =====================

    try:

        leaders = compute_centrality(wallets)

        logger.info("🧠 GRAPH LEADERS (V4)")

        for w in leaders[:10]:

            logger.info(
                "- %s centrality=%.3f",
                w["wallet"],
                w["centrality"],
            )

    except Exception:
        logger.exception("V4 failed")

    # =====================
    # V5 - BEHAVIOR
    # =====================

    try:

        behaviors = analyze_behavior(wallets)

        logger.info("🧬 WALLET BEHAVIOR (V5)")

        for w in behaviors[:10]:

            logger.info(
                "- %s %s intensity=%.1f",
                w["wallet"],
                w["type"],
                w["intensity"],
            )

    except Exception:
        logger.exception("V5 failed")

    # =====================
    # V9 - CLUSTERS
    # =====================

    try:

        clusters = detect_clusters(wallets)

        logger.info("🧬 SMART MONEY CLUSTERS (V9)")

        for c in clusters[:10]:

            logger.info(
                "- cluster=%s size=%s score=%.2f",
                c["id"],
                c["size"],
                c["score"],
            )

    except Exception:
        logger.exception("V9 failed")