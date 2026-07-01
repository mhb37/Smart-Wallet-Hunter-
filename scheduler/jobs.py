import logging
import threading
import time
from datetime import datetime

from discovery.scanner import scan_wallets

from analysis.wallet_score import score_wallets
from analysis.centrality import compute_weighted_centrality
from analysis.behavior import classify_wallets


logger = logging.getLogger(__name__)


def start_scheduler():
    """
    Railway friendly scheduler
    """

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

    # =====================
    # V3 SMART MONEY
    # =====================

    scored = score_wallets(wallets)

    logger.info("🔥 SMART MONEY TOP 10")

    for w in scored[:10]:

        logger.info(
            "- %s score=%.1f appear=%s",
            w["wallet"],
            w["score"],
            w.get("appear", 1)
        )

    # =====================
    # V4 GRAPH
    # =====================

    try:

        leaders = compute_weighted_centrality()

        logger.info("🧠 GRAPH LEADERS (V4)")

        for item in leaders:

            logger.info(
                "- %s centrality=%.3f",
                item["wallet"][:6],
                item["score"]
            )

    except Exception:
        logger.exception("Centrality failed")

    # =====================
    # V5 BEHAVIOR
    # =====================

    try:

        behaviors = classify_wallets()

        logger.info("🧬 WALLET BEHAVIOR (V5)")

        for item in behaviors[:10]:

            logger.info(
                "- %s %s intensity=%.1f",
                item["wallet"][:6],
                item["behavior"],
                item["intensity"]
            )

    except Exception:
        logger.exception("Behavior failed")