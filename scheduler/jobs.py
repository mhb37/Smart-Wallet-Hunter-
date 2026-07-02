import logging
import threading
import time
from datetime import datetime

from analysis.wallet_score import score_wallets
from discovery.scanner import scan_wallets


logger = logging.getLogger(__name__)


SCAN_INTERVAL = 60


def start_scheduler():
    thread = threading.Thread(
        target=_loop,
        daemon=True
    )
    thread.start()


def _loop():

    while True:

        try:
            run_scan()

        except Exception as e:
            logger.exception("Scheduler error: %s", e)

        time.sleep(SCAN_INTERVAL)


def run_scan():

    logger.info("SCAN %s", datetime.utcnow())

    wallets = scan_wallets()

    logger.info("wallets = %s", len(wallets))

    if not wallets:
        logger.info("No wallets found")
        return

    scored = score_wallets(wallets)

    # Tri :
    # 1) score décroissant
    # 2) nombre d'apparitions décroissant
    top = sorted(
        scored,
        key=lambda x: (
            x["score"],
            x["appear"]
        ),
        reverse=True
    )[:10]

    logger.info("TOP 10")

    for wallet in top:

        logger.info(
            "%s score=%s appear=%s",
            wallet["wallet"],
            wallet["score"],
            wallet["appear"]
        )