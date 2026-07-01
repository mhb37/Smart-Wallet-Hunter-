import logging
import threading
import time

from datetime import datetime

from discovery.scanner import scan_wallets
from analysis.wallet_score import score_wallets
from storage.db import init_db, upsert_wallet

logger = logging.getLogger(__name__)


def start_scheduler():

    init_db()

    t = threading.Thread(
        target=_loop,
        daemon=True
    )

    t.start()


def _loop():

    while True:

        try:
            run_scan()

        except Exception as e:
            logger.exception(e)

        time.sleep(60)


def run_scan():

    logger.info(
        "🔁 [SCAN] %s",
        datetime.utcnow()
    )

    wallets = scan_wallets()

    logger.info(
        "📊 %s wallets détectés",
        len(wallets)
    )

    if not wallets:
        return

    for wallet in wallets:
        upsert_wallet(wallet)

    scored = score_wallets(wallets)

    top = sorted(
        scored,
        key=lambda x: x["score"],
        reverse=True
    )[:10]

    logger.info("🔥 SMART MONEY TOP 10")

    for w in top:

        logger.info(
            "- %s score=%.1f appear=%s",
            w["wallet"][:6],
            w["score"],
            w.get("appear", 1)
        )