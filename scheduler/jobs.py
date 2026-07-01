import logging
from datetime import datetime

from discovery.scanner import scan_wallets
from analysis.wallet_score import score_wallets


logger = logging.getLogger(__name__)


def start_scheduler():
    """
    Simple loop scheduler (Railway friendly)
    """

    import threading
    import time

    def loop():
        while True:
            try:
                run_scan()
            except Exception as e:
                logger.exception(e)

            time.sleep(60)  # 1 min scan

    t = threading.Thread(target=loop, daemon=True)
    t.start()


def run_scan():
    logger.info("🔁 [SCAN] %s", datetime.utcnow())

    wallets = scan_wallets()

    logger.info("📊 %s wallets détectés", len(wallets))

    if not wallets:
        return

    scored = score_wallets(wallets)

    top = sorted(scored, key=lambda x: x["score"], reverse=True)[:10]

    logger.info("🔥 SMART MONEY TOP 10")

    for w in top:
        logger.info("- %s score=%.1f appear=%s",
                    w["wallet"], w["score"], w.get("appear", 1))