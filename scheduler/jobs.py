import logging
import threading
import time
from datetime import datetime

from discovery.scanner import scan_wallets
from analysis.wallet_score import score_wallets


logger = logging.getLogger(__name__)


SCAN_INTERVAL = 60


def start_scheduler():

    thread = threading.Thread(
        target=scheduler_loop,
        daemon=True
    )

    thread.start()

    logger.info(
        "Scheduler started (%ss)",
        SCAN_INTERVAL
    )


def scheduler_loop():

    while True:

        started = time.time()

        try:

            run_scan()

        except Exception as e:

            logger.exception(e)

        elapsed = time.time() - started

        sleep_time = max(
            5,
            SCAN_INTERVAL - elapsed
        )

        time.sleep(sleep_time)


def run_scan():

    logger.info(
        "SCAN %s",
        datetime.utcnow().isoformat()
    )

    wallets = scan_wallets()

    logger.info(
        "wallets found = %s",
        len(wallets)
    )

    if not wallets:
        logger.warning(
            "no wallets discovered"
        )
        return

    scored = score_wallets(wallets)

    top = sorted(
        scored,
        key=lambda x: (
            x["score"],
            x["appear"]
        ),
        reverse=True
    )[:20]

    logger.info("TOP 20")

    for index, wallet in enumerate(top, start=1):

        logger.info(
            "#%s %s score=%s appear=%s",
            index,
            wallet["wallet"],
            wallet["score"],
            wallet["appear"],
        )