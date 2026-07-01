import logging

logger = logging.getLogger(__name__)


def scan_wallets():
    """
    Retourne une LISTE propre de wallets
    """

    wallets = set()

    try:
        # simulate tx fetch (replace by real RPC)
        transactions = fetch_transactions()

        logger.debug("[DEBUG] signatures count=%s", len(transactions))

        for i, tx in enumerate(transactions):

            logger.debug("[DEBUG] TX #%s sig=%s", i, tx.get("signature"))

            try:
                tx_data = load_tx(tx)

                logger.debug("[DEBUG] tx loaded OK")

                raw_wallets = tx_data.get("wallets", set())

                logger.debug("[DEBUG] wallets raw = %s", raw_wallets)

                # ⚠️ FIX IMPORTANT : conversion FORCÉE
                if isinstance(raw_wallets, set):
                    raw_wallets = list(raw_wallets)

                if isinstance(raw_wallets, str):
                    raw_wallets = [raw_wallets]

                cleaned = [
                    w.strip()
                    for w in raw_wallets
                    if w and len(w) > 10
                ]

                logger.debug("[DEBUG] wallets after filter = %s", cleaned)

                wallets.update(cleaned)

            except Exception as e:
                logger.debug("[DEBUG] tx error: %s", e)
                continue

        logger.debug("[DEBUG] total discovered wallets=%s", len(wallets))

        final_wallets = list(wallets)

        logger.debug("[DEBUG] final wallets=%s", len(final_wallets))

        return final_wallets

    except Exception as e:
        logger.exception(e)
        return []