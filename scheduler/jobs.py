import logging
import threading
import time
from datetime import datetime

from discovery.scanner import scan_wallets
from analysis.wallet_score import score_wallets


logger = logging.getLogger(__name__)


SCAN_INTERVAL = 300


def start_scheduler():

    thread = threading.Thread(
        target=loop,
        daemon=True
    )

    thread.start()


def loop():

    while True:

        try:

            run_scan()

        except Exception as e:

            logger.exception(e)

        time.sleep(SCAN_INTERVAL)


def run_scan():

    logger.info(
        "SCAN %s",
        datetime.utcnow().isoformat()
    )

    wallets = scan_wallets()

    logger.info(
        "wallets discovered = %s",
        len(wallets)
    )

    if not wallets:
        return

    scored = score_wallets(wallets)

    scored.sort(
        key=lambda x: (
            x["appear"],
            x["score"]
        ),
        reverse=True
    )

    logger.info("TOP WALLET CANDIDATES")

    for wallet in scored[:20]:

        logger.info(
            "%s | score=%s | appear=%s",
            wallet["wallet"],
            wallet["score"],
            wallet["appear"]
        )