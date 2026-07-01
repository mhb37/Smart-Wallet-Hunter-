import logging

from discovery.solana_rpc import fetch_transactions, get_transaction
from discovery.wallet_extractor import extract_wallets_from_transaction


logger = logging.getLogger(__name__)


def scan_wallets():

    wallets = set()

    try:

        transactions = fetch_transactions()

        logger.info("TX count = %s", len(transactions))

        for i, signature in enumerate(transactions):

            logger.info("TX #%s = %s", i, signature)

            tx = get_transaction(signature)

            if not tx:
                logger.info("empty tx")
                continue

            extracted = extract_wallets_from_transaction(tx)

            logger.info(
                "wallets raw = %s",
                extracted
            )

            wallets.update(extracted)

        logger.info(
            "FINAL OUTPUT = %s wallets",
            len(wallets)
        )

        return list(wallets)

    except Exception as e:

        logger.exception(e)

        return []