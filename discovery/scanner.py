import logging

from discovery.solana_rpc import fetch_transactions
from discovery.wallet_extractor import load_tx


logger = logging.getLogger(__name__)


def scan_wallets():

    wallets = set()

    try:

        logger.info("===== SCANNER DEBUG START =====")

        transactions = fetch_transactions()

        logger.info(
            "[DEBUG] transactions count = %s",
            len(transactions)
        )

        for index, sig in enumerate(transactions):

            logger.info(
                "[DEBUG] TX #%s sig = %s",
                index,
                sig
            )

            data = load_tx(sig)

            if not data:

                logger.info(
                    "[DEBUG] empty transaction"
                )

                continue

            raw = data.get("wallets", [])

            logger.info(
                "[DEBUG] wallets raw = %s",
                raw
            )

            wallets.update(raw)

        logger.info("===== FINAL DEBUG =====")

        logger.info(
            "[DEBUG] discovered wallets = %s",
            len(wallets)
        )

        logger.info(
            "[DEBUG] sample = %s",
            list(wallets)[:5]
        )

        logger.info(
            "[DEBUG] FINAL OUTPUT = %s wallets",
            len(wallets)
        )

        return list(wallets)

    except Exception as e:

        logger.exception(e)

        return []