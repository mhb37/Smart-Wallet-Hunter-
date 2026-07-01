import logging
from datetime import datetime

from discovery.scanner import scan_wallets
from analysis.wallet_score import score_wallets
from telegram_bot.notifier import send_alert

logger = logging.getLogger(__name__)


# =========================
# STATE GLOBAL (important)
# =========================
_seen_wallets = set()
_last_scan_hash = None


def discover_wallets_job():
    """
    JOB principal exécuté par scheduler
    """

    global _seen_wallets, _last_scan_hash

    logger.info("🔁 [SCHEDULER] Scan exécuté à %s", datetime.utcnow())

    # 1. SCAN RAW TX
    wallets = scan_wallets()

    logger.debug("[DEBUG] raw wallets = %s", wallets)

    # ⚠️ FIX CRITIQUE : normalisation (cause 0 wallets bug)
    if not wallets:
        logger.debug("[DEBUG] empty scan → skip")
        return

    wallets = set(wallets)

    logger.debug("[DEBUG] unique wallets = %s", wallets)

    # 2. ANTI DUPLICATES ACROSS SCANS
    new_wallets = wallets - _seen_wallets

    logger.debug("[DEBUG] new wallets = %s", new_wallets)

    if not new_wallets:
        logger.debug("[DEBUG] no new wallets → skip scoring")
        return

    _seen_wallets |= new_wallets

    # 3. SCORE
    scored = score_wallets(list(new_wallets))

    logger.debug("[DEBUG] scored wallets = %s", scored)

    if not scored:
        logger.debug("[DEBUG] no scored wallets")
        return

    # 4. TOP 10 SAFE
    top = sorted(scored, key=lambda x: x["score"], reverse=True)[:10]

    logger.info("🔥 SMART MONEY TOP %s", len(top))

    for w in top:
        logger.info(
            "- %s score=%.1f appear=%s",
            w["wallet"],
            w["score"],
            w.get("appear", 1)
        )

    # 5. NOTIFY (optionnel)
    try:
        send_alert(top)
    except Exception as e:
        logger.exception("Telegram send error: %s", e)