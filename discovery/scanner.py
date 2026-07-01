import logging

from discovery.solana_rpc import (
    get_recent_signatures,
    get_transaction,
)
from discovery.wallet_extractor import load_tx


logger = logging.getLogger(__name__)

SEED_ADDRESS = "So11111111111111111111111111111111111111112"


def scan_wallets():
    wallets = set()

    try:
        logger.info("===== SCANNER DEBUG START =====")
        logger.info("[DEBUG] SEED: %s", SEED_ADDRESS)

        signatures = get_recent_signatures(
            SEED_ADDRESS,
            limit=10
        )

        logger.info(
            "[DEBUG] signatures raw type=%s",
            type(signatures)
        )

        logger.info(
            "[DEBUG] signatures count=%s",
            len(signatures)
        )

        for index, sig_data in enumerate(signatures):

            signature = sig_data.get("signature")

            if not signature:
                continue

            logger.info(
                "[DEBUG] TX #%s sig=%s",
                index,
                signature
            )

            tx = get_transaction(signature)

            if not tx:
                logger.info("[DEBUG] empty transaction")
                continue

            data = load_tx(tx)

            raw = data.get("wallets", [])

            logger.info(
                "[DEBUG] wallets raw = %s",
                set(raw)
            )

            if isinstance(raw, str):
                raw = [raw]

            cleaned = [
                wallet
                for wallet in raw
                if isinstance(wallet, str)
                and len(wallet) >= 32
            ]

            logger.info(
                "[DEBUG] wallets after filter = %s",
                cleaned
            )

            wallets.update(cleaned)

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

    except Exception:
        logger.exception("scan_wallets failed")
        return []